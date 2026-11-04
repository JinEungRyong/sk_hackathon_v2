#!/usr/bin/env node
// 로그인 상태 파일 만들기 (ux-ui-audit-hackathon 스킬용)
// 사용법: node login.mjs --url <로그인 주소> --user <아이디> --pass <비밀번호> --out /tmp/ux-state.json
//         [--user-field 선택자] [--pass-field 선택자] [--submit 선택자] [--expect 로그인 뒤 주소에 들어갈 글자]
// 아이디·비밀번호는 --user/--pass 대신 환경변수 UX_USER, UX_PASS로도 줄 수 있다.
// 결과 파일은 audit.mjs --storage-state 로 넘긴다. 저장소 밖(/tmp)에 둔다.

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
const opt = { user: process.env.UX_USER || '', pass: process.env.UX_PASS || '' };
for (let i = 0; i < args.length; i++) {
  const k = args[i].replace(/^--/, '');
  if (['url', 'user', 'pass', 'out', 'user-field', 'pass-field', 'submit', 'expect'].includes(k)) opt[k] = args[++i];
  else if (k === 'h' || k === 'help') {
    console.log('node login.mjs --url <로그인 주소> --user <아이디> --pass <비밀번호> --out /tmp/ux-state.json [--user-field 선택자] [--pass-field 선택자] [--submit 선택자] [--expect 글자]');
    process.exit(0);
  }
}
if (!opt.url || !opt.out) {
  console.error('--url 과 --out 은 꼭 필요합니다. (--help 참고)');
  process.exit(1);
}
if (!opt.out.startsWith('/tmp')) console.error('주의: 로그인 상태 파일은 저장소 밖(/tmp)에 두세요. 커밋하면 안 됩니다.');

const { chromium } = loadPlaywright();
const browser = await chromium.launch();
const context = await browser.newContext();
const page = await context.newPage();
await page.goto(opt.url, { waitUntil: 'networkidle', timeout: 30000 });

// 입력창 찾기: 지정한 선택자 → 흔한 이름 순서
const firstVisible = async (sels) => {
  for (const s of sels) {
    const loc = page.locator(s).first();
    if (await loc.count() && await loc.isVisible().catch(() => false)) return loc;
  }
  return null;
};
const userBox = await firstVisible(opt['user-field'] ? [opt['user-field']] : [
  'input[name=username]', 'input[name=user]', 'input[name=id]', 'input[name=login]', 'input[name=email]',
  'input[name=employee_id]', 'input[name=emp_id]', 'input[name*=사번]', 'input[type=email]',
  'input[autocomplete=username]', 'form input[type=text]', 'input[type=text]',
]);
const passBox = await firstVisible(opt['pass-field'] ? [opt['pass-field']] : ['input[type=password]']);
if (!userBox || !passBox) {
  console.error(`입력창을 찾지 못했습니다 (아이디: ${userBox ? '찾음' : '없음'}, 비밀번호: ${passBox ? '찾음' : '없음'}). --user-field / --pass-field 로 선택자를 주세요.`);
  await browser.close();
  process.exit(1);
}
await userBox.fill(opt.user);
await passBox.fill(opt.pass);
const before = page.url();
const submit = await firstVisible(opt.submit ? [opt.submit] : ['form button[type=submit]', 'form input[type=submit]', 'button[type=submit]', 'form button']);
await Promise.all([
  page.waitForLoadState('networkidle').catch(() => {}),
  submit ? submit.click() : passBox.press('Enter'),
]);
await page.waitForTimeout(500);

const after = page.url();
const stillLogin = await page.locator('input[type=password]').first().isVisible().catch(() => false);
const ok = opt.expect ? after.includes(opt.expect) : !(after === before && stillLogin);
await context.storageState({ path: opt.out });
await browser.close();
console.log(`로그인 ${ok ? '성공으로 보임' : '실패로 보임'}: ${before} → ${after}`);
console.log(`상태 파일: ${opt.out}${ok ? '' : ' (실패해도 저장함. 아이디·비밀번호·선택자를 확인하세요)'}`);
process.exit(ok ? 0 : 3);
