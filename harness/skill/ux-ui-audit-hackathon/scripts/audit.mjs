#!/usr/bin/env node
// UX/UI 자동 측정 스크립트 (ux-ui-audit 스킬용)
// 사용법: node audit.mjs <url|file.html> [...] [--out dir] [--viewport 1440x900] [--storage-state state.json]
// --storage-state: login.mjs가 만든 로그인 상태 파일. 로그인이 필요한 화면을 로그인한 상태로 측정한다.
// 결과: <out>/report.json, <out>/<n>-<slug>.png
// 판단은 하지 않습니다. 사람이(또는 에이전트가) 검토할 근거 수치만 모읍니다.

import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

// Playwright 찾기: 현재 프로젝트 → 스킬 폴더 → 전역(NODE_PATH, npm root -g)
function loadPlaywright() {
  const bases = [path.join(process.cwd(), 'noop.js'), import.meta.url];
  try {
    const { execSync } = createRequire(import.meta.url)('node:child_process');
    const g = execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
    if (g) bases.push(path.join(g, 'noop.js'));
  } catch {}
  for (const b of bases) {
    try { return createRequire(b)('playwright'); } catch {}
  }
  console.error('Playwright를 찾을 수 없습니다. 프로젝트에서 실행하세요:\n  npm i -D playwright && npx playwright install chromium');
  process.exit(2);
}
const { chromium } = loadPlaywright();

const args = process.argv.slice(2);
const targets = [];
let outDir = 'ux-audit-out';
let viewport = { width: 1440, height: 900 };
let storageState = null;
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--out') outDir = args[++i];
  else if (a === '--viewport') {
    const [w, h] = args[++i].split('x').map(Number);
    viewport = { width: w, height: h };
  }
  else if (a === '--storage-state') storageState = args[++i];
  else if (a === '-h' || a === '--help') {
    console.log('node audit.mjs <url|file.html> [...] [--out dir] [--viewport WxH] [--storage-state state.json]');
    process.exit(0);
  } else targets.push(a);
}
if (!targets.length) {
  console.error('검수할 URL 또는 HTML 파일을 하나 이상 지정하세요.');
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

const toUrl = (t) => (/^[a-z]+:\/\//i.test(t) ? t : pathToFileURL(path.resolve(t)).href);
const slug = (s) => s.replace(/^[a-z]+:\/\//i, '').replace(/[^a-z0-9가-힣]+/gi, '-').slice(0, 60);

// 브라우저 안에서 실행되는 측정 함수
function measure() {
  const MAX = 40; // 카테고리별 상세 항목 최대 개수
  const vis = (el) => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const sel = (el) => {
    if (el.id) return `#${CSS.escape(el.id)}`;
    const parts = [];
    let e = el;
    while (e && e.nodeType === 1 && parts.length < 4) {
      let p = e.tagName.toLowerCase();
      const cls = [...e.classList].filter((c) => !/^\d/.test(c)).slice(0, 2);
      if (cls.length) p += '.' + cls.map((c) => CSS.escape(c)).join('.');
      const sibs = e.parentElement ? [...e.parentElement.children].filter((x) => x.tagName === e.tagName) : [];
      if (sibs.length > 1) p += `:nth-of-type(${sibs.indexOf(e) + 1})`;
      parts.unshift(p);
      if (e.id) { parts[0] = `#${CSS.escape(e.id)}`; break; }
      e = e.parentElement;
    }
    return parts.join(' > ');
  };
  const text = (el) => (el.innerText || el.value || '').trim().replace(/\s+/g, ' ').slice(0, 40);

  // --- 색상 대비 ---
  const parse = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const blend = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  const lum = ({ r, g, b }) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const bgOf = (el) => {
    const layers = [];
    for (let e = el; e; e = e.parentElement) {
      const s = getComputedStyle(e);
      if (s.backgroundImage && s.backgroundImage !== 'none') return null; // 이미지/그라데이션 배경: 측정 불가
      const c = parse(s.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
    }
    let bg = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = layers.length - 1; i >= 0; i--) bg = blend(layers[i], bg);
    return bg;
  };

  // --- 텍스트 요소 수집 ---
  const textEls = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode;
    if (n.textContent.trim().length && n.parentElement && vis(n.parentElement)) textEls.add(n.parentElement);
  }

  const fontSizes = {}, families = {}, weights = {}, lineHeights = [];
  const smallText = [], lowContrast = [], unknownContrast = [];
  for (const el of textEls) {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue;
    const s = getComputedStyle(el);
    const fs = parseFloat(s.fontSize);
    const fw = Number(s.fontWeight) || 400;
    fontSizes[fs] = (fontSizes[fs] || 0) + 1;
    families[s.fontFamily.split(',')[0].trim().replace(/['"]/g, '')] = (families[s.fontFamily.split(',')[0].trim().replace(/['"]/g, '')] || 0) + 1;
    weights[fw] = (weights[fw] || 0) + 1;
    if (s.lineHeight !== 'normal') lineHeights.push(+(parseFloat(s.lineHeight) / fs).toFixed(2));
    if (fs < 12 && smallText.length < MAX) smallText.push({ selector: sel(el), text: text(el), fontSize: fs });

    const fg = parse(s.color);
    const bg = bgOf(el);
    if (!fg) continue;
    if (!bg) { if (unknownContrast.length < MAX) unknownContrast.push({ selector: sel(el), text: text(el) }); continue; }
    const r = ratio(blend(fg, bg), bg);
    const large = fs >= 24 || (fs >= 18.66 && fw >= 700);
    const need = large ? 3 : 4.5;
    const disabled = el.closest('[disabled],[aria-disabled="true"]');
    if (r < need && !disabled && lowContrast.length < MAX)
      lowContrast.push({ selector: sel(el), text: text(el), ratio: +r.toFixed(2), required: need, color: s.color, fontSize: fs });
  }

  // --- 인터랙티브 요소 ---
  const INTERACTIVE = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[role=tab],[role=checkbox],[role=radio],[role=switch],[role=menuitem],[onclick],[tabindex]:not([tabindex="-1"])';
  const inter = [...document.querySelectorAll(INTERACTIVE)].filter(vis);
  const noName = [], divButtons = [], positiveTabindex = [];
  for (const el of inter) {
    const name = (el.getAttribute('aria-label') || el.getAttribute('title') || text(el) || (el.getAttribute('aria-labelledby') && document.getElementById(el.getAttribute('aria-labelledby'))?.innerText) || el.querySelector('img[alt]:not([alt=""])')?.alt || '').trim();
    const isField = /^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName);
    if (!name && !isField && noName.length < MAX) noName.push({ selector: sel(el), tag: el.tagName.toLowerCase() });
    if (!/^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY)$/.test(el.tagName) && el.hasAttribute('onclick') && !el.getAttribute('role') && divButtons.length < MAX)
      divButtons.push({ selector: sel(el), text: text(el) });
    if (Number(el.getAttribute('tabindex')) > 0) positiveTabindex.push(sel(el));
  }

  // 선택 상태가 aria로 표현되지 않은 요소
  const selectedNoAria = [...document.querySelectorAll('[class]')]
    .filter((el) => vis(el) && [...el.classList].some((c) => /(^|[-_])(active|selected|current|checked|is-on|on)($|[-_])/i.test(c)))
    .filter((el) => !['aria-selected', 'aria-pressed', 'aria-checked', 'aria-current', 'aria-expanded'].some((a) => el.hasAttribute(a)) && !el.matches('input:checked,option:checked'))
    .slice(0, MAX)
    .map((el) => ({ selector: sel(el), text: text(el) }));

  // 폼 라벨
  const unlabeled = [...document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=reset]),select,textarea')]
    .filter(vis)
    .filter((el) => !(el.labels && el.labels.length) && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby') && !el.getAttribute('title'))
    .slice(0, MAX)
    .map((el) => ({ selector: sel(el), type: el.type || el.tagName.toLowerCase(), placeholderOnly: !!el.placeholder }));

  // 이미지 alt
  const imgNoAlt = [...document.querySelectorAll('img')].filter((i) => !i.hasAttribute('alt')).slice(0, MAX).map((i) => ({ selector: sel(i), src: (i.getAttribute('src') || '').slice(0, 80) }));

  // 제목 구조
  const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).map((h) => ({ level: +h.tagName[1], text: text(h) }));
  const skipped = [];
  for (let i = 1; i < heads.length; i++) if (heads[i].level > heads[i - 1].level + 1) skipped.push(`${'h' + heads[i - 1].level} → h${heads[i].level} ("${heads[i].text}")`);

  // 한글 줄바꿈
  const koNoKeepAll = [...textEls].filter((el) => /[가-힣]/.test(el.textContent) && getComputedStyle(el).wordBreak !== 'keep-all' && el.getBoundingClientRect().height > parseFloat(getComputedStyle(el).fontSize) * 2.2).length;

  // focus outline 제거 규칙 (CSS 정적 탐지)
  const outlineNone = [];
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch { continue; }
    for (const r of rules || []) {
      if (r.selectorText && /:focus/.test(r.selectorText) && /outline\s*:\s*(none|0)/.test(r.cssText) && !/box-shadow|border|outline-offset/.test(r.cssText.replace(/outline\s*:\s*(none|0)[^;]*;?/, '')))
        outlineNone.push(r.selectorText);
    }
  }

  const doc = document.documentElement;
  return {
    title: document.title,
    lang: doc.getAttribute('lang') || null,
    horizontalOverflow: doc.scrollWidth > doc.clientWidth + 1 ? { scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth } : null,
    typography: {
      fontSizes: Object.fromEntries(Object.entries(fontSizes).sort((a, b) => b[1] - a[1])),
      distinctFontSizes: Object.keys(fontSizes).length,
      fontFamilies: families,
      fontWeights: weights,
      lineHeightRange: lineHeights.length ? [Math.min(...lineHeights), Math.max(...lineHeights)] : null,
      smallTextUnder12px: smallText,
      koreanWithoutKeepAllMultiline: koNoKeepAll,
      headings: heads,
      h1Count: heads.filter((h) => h.level === 1).length,
      skippedHeadingLevels: skipped,
    },
    contrast: { failing: lowContrast, notMeasurableBackgroundImage: unknownContrast.length },
    interaction: {
      interactiveCount: inter.length,
      selectedStateWithoutAria: selectedNoAria,
      focusOutlineRemovedRules: outlineNone,
    },
    accessibility: {
      missingAccessibleName: noName,
      unlabeledFormFields: unlabeled,
      imagesWithoutAlt: imgNoAlt,
      clickableNonSemantic: divButtons,
      positiveTabindex,
    },
  };
}

if (storageState && !fs.existsSync(storageState)) {
  console.error(`로그인 상태 파일이 없습니다: ${storageState} (먼저 login.mjs 실행)`);
  process.exit(1);
}
const browser = await chromium.launch();
const context = await browser.newContext(storageState ? { viewport, storageState } : { viewport });
const report = { generatedAt: new Date().toISOString(), viewport, loggedIn: !!storageState, pages: [] };
let n = 0;
for (const t of targets) {
  n++;
  const page = await context.newPage();
  const url = toUrl(t);
  const entry = { target: t, url };
  try {
    const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(300);
    entry.status = resp ? resp.status() : null;
    entry.finalUrl = page.url();   // 로그인 페이지로 돌려보내졌는지 확인용
    Object.assign(entry, await page.evaluate(measure));
    // 키보드 Tab 이동 시 focus 표시 확인 (최대 25개)
    const noFocusVisible = [];
    for (let i = 0; i < 25; i++) {
      await page.keyboard.press('Tab');
      const r = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        const s = getComputedStyle(el);
        const has = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none');
        return { has, selector: el.tagName.toLowerCase() + (el.id ? '#' + el.id : el.classList[0] ? '.' + el.classList[0] : ''), text: (el.innerText || el.value || '').trim().slice(0, 30) };
      });
      if (!r) break;
      if (!r.has) noFocusVisible.push({ selector: r.selector, text: r.text });
    }
    entry.interaction.focusWithoutVisibleIndicator = noFocusVisible;
    const shot = path.join(outDir, `${n}-${slug(t)}.png`);
    await page.screenshot({ path: shot, fullPage: true });
    entry.screenshot = shot;
  } catch (e) {
    entry.error = String(e.message || e);
  }
  await page.close();
  report.pages.push(entry);
}
await context.close();
await browser.close();
fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2));

// 콘솔 요약
for (const p of report.pages) {
  console.log(`\n=== ${p.target} ${p.title ? `(${p.title})` : ''}`);
  if (p.error) { console.log('  오류:', p.error); continue; }
  const L = (label, v) => console.log(`  ${label}: ${v}`);
  L('HTTP 상태 / 최종 주소', `${p.status ?? '-'} / ${p.finalUrl}`);
  if (p.finalUrl && p.finalUrl.split('#')[0] !== p.url.split('#')[0]) console.log('  ⚠ 요청한 주소와 최종 주소가 다릅니다. 로그인 페이지로 돌려보내졌다면 --storage-state 를 주세요.');
  L('lang', p.lang ?? '없음');
  L('가로 넘침', p.horizontalOverflow ? `${p.horizontalOverflow.scrollWidth}px > ${p.horizontalOverflow.clientWidth}px` : '없음');
  L('폰트 크기 종류', `${p.typography.distinctFontSizes}개 (${Object.keys(p.typography.fontSizes).join(', ')}px)`);
  L('폰트 패밀리', Object.keys(p.typography.fontFamilies).join(', '));
  L('폰트 굵기', Object.keys(p.typography.fontWeights).join(', '));
  L('12px 미만 텍스트', p.typography.smallTextUnder12px.length);
  L('h1 개수 / 건너뛴 제목 단계', `${p.typography.h1Count} / ${p.typography.skippedHeadingLevels.length}`);
  L('대비 미달 텍스트', p.contrast.failing.length);
  L('aria 없는 선택 상태', p.interaction.selectedStateWithoutAria.length);
  L('focus 표시 없음(Tab)', p.interaction.focusWithoutVisibleIndicator.length);
  L('접근 가능한 이름 없음', p.accessibility.missingAccessibleName.length);
  L('라벨 없는 입력창', p.accessibility.unlabeledFormFields.length);
  L('alt 없는 이미지', p.accessibility.imagesWithoutAlt.length);
  L('div/span 클릭 요소', p.accessibility.clickableNonSemantic.length);
  L('스크린샷', p.screenshot);
}
console.log(`\n상세: ${path.join(outDir, 'report.json')}`);
