#!/usr/bin/env bash
# Playwright를 저장소 밖(/tmp/uxpw)에 설치한다. 저장소의 package.json을 건드리지 않는다.
# 사용: bash <skill-dir>/scripts/setup_playwright.sh
# 이후 측정: cd /tmp/uxpw && node <skill-dir>/scripts/audit.mjs ...
set -e
DIR=/tmp/uxpw
mkdir -p "$DIR"
cd "$DIR"

# 이미 쓸 수 있으면 건너뜀 (전역 설치나 사전 설치 포함)
if node -e "require('playwright').chromium.executablePath()" >/dev/null 2>&1; then
  if node -e "const fs=require('fs');process.exit(fs.existsSync(require('playwright').chromium.executablePath())?0:1)" >/dev/null 2>&1; then
    echo "Playwright와 Chromium이 이미 있습니다. ($DIR 에서 실행하세요)"
    exit 0
  fi
fi

[ -f package.json ] || npm init -y >/dev/null
echo "Playwright 설치 중 (/tmp/uxpw)…"
if ! npm i playwright >/dev/null 2>&1; then
  echo "설치 실패: 네트워크가 막혔을 수 있습니다. 측정 없이 코드 정적 검토로 진행하고 보고서에 '실측 미실시'라고 적으세요."
  exit 2
fi
if ! npx playwright install chromium >/dev/null 2>&1; then
  echo "Chromium 다운로드 실패: 네트워크가 막혔을 수 있습니다. 측정 없이 코드 정적 검토로 진행하세요."
  exit 2
fi
echo "완료. 측정: cd $DIR && node <skill-dir>/scripts/audit.mjs <url> --out /tmp/ux-audit-out"
