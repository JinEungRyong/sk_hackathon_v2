#!/usr/bin/env node
// UX 시나리오 따라 하기 (ux-ui-audit-hackathon 스킬용)
// 사용법: node walk.mjs <scenario.json> [--out /tmp/ux-walk]
// scenario.json 예:
// {
//   "id": "UX-S1", "storageState": "/tmp/ux-state-admin.json", "viewport": "1440x900",
//   "steps": [
//     {"goto": "http://localhost:3000/admin"},
//     {"expectText": "검토 대기"},
//     {"click": "text=E260123"},
//     {"fill": ["textarea[name=reason]", "영수증 금액과 청구 금액이 다릅니다"]},
//     {"click": "button:has-text('반려하기')"},
//     {"expectText": "반려"},
//     {"screenshot": "after-reject"}
//   ]
// }
// 단계 종류: goto, click, fill [선택자, 값], select [선택자, 값], press 키, expectText 글자, expectNoText 글자,
//           expectUrl 글자, wait 밀리초, screenshot 이름
// 결과: <out>/<id>/result.json, 단계별 스크린샷. 판단은 하지 않고, 어디서 막혔는지와 걸린 시간만 남긴다.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

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
  console.error('Playwright를 찾을 수 없습니다. 먼저 실행하세요: bash <skill-dir>/scripts/setup_playwright.sh');
  process.exit(2);
}

const args = process.argv.slice(2);
if (!args.length || args[0] === '-h' || args[0] === '--help') {
  console.log('node walk.mjs <scenario.json> [--out /tmp/ux-walk]');
  process.exit(args.length ? 0 : 1);
}
const file = args[0];
const outBase = args.includes('--out') ? args[args.indexOf('--out') + 1] : '/tmp/ux-walk';
const sc = JSON.parse(fs.readFileSync(file, 'utf8'));
const id = sc.id || path.basename(file, '.json');
const outDir = path.join(outBase, id);
fs.mkdirSync(outDir, { recursive: true });
const [vw, vh] = (sc.viewport || '1440x900').split('x').map(Number);

const { chromium } = loadPlaywright();
const browser = await chromium.launch();
const ctxOpt = { viewport: { width: vw, height: vh } };
if (sc.storageState) {
  if (!fs.existsSync(sc.storageState)) { console.error(`로그인 상태 파일이 없습니다: ${sc.storageState}`); process.exit(1); }
  ctxOpt.storageState = sc.storageState;
}
const context = await browser.newContext(ctxOpt);
const page = await context.newPage();
const consoleErrors = [];
page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 200)); });
page.on('pageerror', (e) => consoleErrors.push(String(e.message || e).slice(0, 200)));
const httpErrors = [];
page.on('response', (r) => { if (r.status() >= 400) httpErrors.push(`${r.status()} ${r.url()}`); });

const result = { id, title: sc.title || '', startedAt: new Date().toISOString(), steps: [], passed: true };
let n = 0;
for (const st of sc.steps || []) {
  n++;
  const kind = Object.keys(st)[0];
  const val = st[kind];
  const rec = { n, kind, value: val, ok: true };
  const t0 = Date.now();
  try {
    if (kind === 'goto') { const r = await page.goto(val, { waitUntil: 'networkidle', timeout: 30000 }); rec.status = r ? r.status() : null; }
    else if (kind === 'click') { await page.locator(val).first().click({ timeout: 8000 }); await page.waitForLoadState('networkidle').catch(() => {}); }
    else if (kind === 'fill') await page.locator(val[0]).first().fill(String(val[1]), { timeout: 8000 });
    else if (kind === 'select') await page.locator(val[0]).first().selectOption(String(val[1]), { timeout: 8000 });
    else if (kind === 'press') { await page.keyboard.press(val); await page.waitForLoadState('networkidle').catch(() => {}); }
    else if (kind === 'expectText') { await page.getByText(val, { exact: false }).first().waitFor({ timeout: 8000 }); }
    else if (kind === 'expectNoText') { if (await page.getByText(val, { exact: false }).count()) throw new Error(`보이면 안 되는 글자가 보임: ${val}`); }
    else if (kind === 'expectUrl') { if (!page.url().includes(val)) throw new Error(`주소에 '${val}' 없음: ${page.url()}`); }
    else if (kind === 'wait') await page.waitForTimeout(Number(val));
    else if (kind === 'screenshot') { const p = path.join(outDir, `${String(n).padStart(2, '0')}-${val}.png`); await page.screenshot({ path: p, fullPage: true }); rec.screenshot = p; }
    else throw new Error(`모르는 단계: ${kind}`);
  } catch (e) {
    rec.ok = false;
    rec.error = String(e.message || e).split('\n')[0].slice(0, 300);
    const p = path.join(outDir, `${String(n).padStart(2, '0')}-실패.png`);
    await page.screenshot({ path: p, fullPage: true }).catch(() => {});
    rec.screenshot = p;
  }
  rec.ms = Date.now() - t0;
  rec.url = page.url();
  result.steps.push(rec);
  if (!rec.ok) { result.passed = false; result.stoppedAt = n; break; }
}
result.consoleErrors = consoleErrors.slice(0, 20);
result.httpErrors = httpErrors.slice(0, 20);
await context.close();
await browser.close();
fs.writeFileSync(path.join(outDir, 'result.json'), JSON.stringify(result, null, 2));

console.log(`=== ${id} ${result.title} : ${result.passed ? '끝까지 진행' : `${result.stoppedAt}단계에서 막힘`}`);
for (const s of result.steps) console.log(`  ${s.ok ? '✓' : '✗'} ${s.n}. ${s.kind} ${JSON.stringify(s.value)} (${s.ms}ms)${s.error ? ' → ' + s.error : ''}`);
if (result.consoleErrors.length) console.log(`  콘솔 오류 ${result.consoleErrors.length}건: ${result.consoleErrors[0]}`);
if (result.httpErrors.length) console.log(`  HTTP 오류 ${result.httpErrors.length}건: ${result.httpErrors[0]}`);
console.log(`  결과: ${path.join(outDir, 'result.json')}`);
process.exit(result.passed ? 0 : 3);
