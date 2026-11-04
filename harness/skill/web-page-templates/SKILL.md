---
name: web-page-templates
description: 웹 페이지 홈 화면을 7가지 유형(마케팅 랜딩, 쇼핑몰, 기업 소개, 포트폴리오, 블로그·매거진, 이벤트·프로모션, 관리자 대시보드) 템플릿으로 만들 때 사용합니다. HTML+CSS와 Python 표준 라이브러리만으로 정적 페이지를 만들고, 자바스크립트·외부 라이브러리·CDN은 쓰지 않습니다. Use when asked for a landing page, shop/e-commerce home, corporate site, portfolio, blog/magazine, event/promotion page, or admin dashboard as static HTML. React·Vue 같은 프레임워크 앱이나 실제 결제·로그인 기능 구현에는 사용하지 않습니다.
---

# 웹 페이지 유형별 홈 화면 템플릿

이 스킬은 자주 쓰는 웹 페이지 7가지 유형의 홈 화면을 빠르고 일관되게 만들기 위한 스킬입니다. 유형마다 설명 문서, 파이썬 샘플 코드, 완성된 샘플 HTML이 들어 있습니다.

## 이 스킬의 제약

- **HTML + CSS + Python 3 표준 라이브러리만 사용합니다.** 자바스크립트, 외부 CSS·JS 라이브러리, CDN, 웹 폰트, 외부 이미지를 쓰지 않습니다.
- 사진 자리는 CSS 그라데이션으로, 아이콘은 이모지나 글자로 채웁니다.
- 가격·할인율·비율·날짜·차트 높이처럼 계산이 필요한 값은 **파이썬이 계산해서 HTML에 넣습니다.**
- HTML만으로 되는 상호작용은 사용해도 됩니다. 예: `<details>`로 FAQ 펼치기, `:hover` 효과, `<form>` 모양.
- 장바구니 담기, 실시간 카운트다운, 폼 전송처럼 자바스크립트나 서버가 필요한 기능은 이 스킬의 범위 밖입니다. 사용자가 이런 기능을 요청하면 범위 밖이라는 점을 먼저 알리고, 모양만 만들지 여부를 확인합니다.

## 1. 유형 고르기

| 유형 | key | 목적 | 이런 요청이면 이 유형 | 설명 문서 |
|---|---|---|---|---|
| 마케팅 랜딩 | `landing` | 방문자가 가입·구매·문의 중 **한 가지 행동**을 하도록 설득 | 서비스 소개, 앱 홍보, SaaS, 사전 신청, 제품 출시 | `references/landing.md` |
| 쇼핑몰 | `shop` | 많은 상품을 **찾고 고르게** 함 | 온라인 스토어, 상품 목록, 기획전, 브랜드몰 | `references/shop.md` |
| 기업 소개 | `corporate` | 회사의 **신뢰와 정보**를 전달 | 회사 홈페이지, 사업 소개, IR, 채용 | `references/corporate.md` |
| 포트폴리오 | `portfolio` | 개인·스튜디오의 **작업물**을 보여 줌 | 디자이너·개발자·사진작가 개인 사이트 | `references/portfolio.md` |
| 블로그·매거진 | `blog` | 글을 **읽고 구독**하게 함 | 블로그, 웹진, 뉴스레터, 기술 블로그 | `references/blog.md` |
| 이벤트·프로모션 | `event` | **기간 한정** 행사 참여를 유도 | 세일, 쿠폰, 응모, 런칭 이벤트, 행사 신청 | `references/event.md` |
| 대시보드 | `dashboard` | 운영 **수치를 한눈에** 보여 줌 | 관리자 화면, KPI 현황판, 백오피스 | `references/dashboard.md` |

요청이 두 유형에 걸치면 사용자가 방문자에게 기대하는 **주된 행동**으로 고릅니다. 예를 들어 "신제품을 알리고 사전 예약을 받는 페이지"는 `landing`이고, "한정 기간 할인 쿠폰 페이지"는 `event`입니다. 그래도 정할 수 없으면 사용자에게 한 번만 묻습니다.

## 2. 작업 순서

1. 위 표에서 유형을 고릅니다.
2. 해당 `references/<key>.md`를 읽습니다. 섹션 순서, 디자인 규칙, 파이썬이 계산할 데이터가 정리되어 있습니다.
3. 완성된 모습은 `assets/samples/<key>.html`에서 확인합니다.
4. `scripts/common.py`와 `scripts/page_types/<key>.py`를 **사용자 프로젝트로 복사한 뒤** 수정합니다. 스킬 폴더 안의 파일은 직접 고치지 않습니다.
5. `build()` 함수 맨 앞의 데이터 목록(브랜드명, 문구, 상품, 수치)을 사용자의 내용으로 바꿉니다. 색상은 모듈 상단의 CSS 문자열에서 바꿉니다.
6. 페이지를 생성합니다.
   ```bash
   python3 scripts/page_types/shop.py > shop.html          # 한 유형만, 표준 출력으로
   python3 scripts/build.py shop event --out ./site        # 여러 유형 + index.html
   python3 scripts/build.py all --out ./site               # 7개 유형 전부
   python3 scripts/build.py --list                         # 유형 목록 보기
   ```
7. 아래 "검증 체크리스트"를 확인합니다.

## 3. 코드 작성 규칙

- 모든 페이지는 `common.page(title, css, body)`로 감쌉니다. 기본 CSS(`BASE_CSS`)에는 초기화 규칙, `.wrap`(최대 너비 1160px, 좌우 여백 24px), 한글 줄바꿈 규칙(`word-break:keep-all`)이 들어 있습니다.
- CSS는 **f-string이 아닌 일반 문자열**로 둡니다. f-string 안에서는 CSS의 `{ }`가 충돌합니다.
- CSS에 다른 값을 끼워 넣어야 하면 `%` 포맷 대신 `"...SERIF_FONT...".replace("SERIF_FONT", SERIF)`처럼 자리표시자를 바꿉니다. `%` 포맷을 쓰면 `50%` 같은 값이 오류를 냅니다.
- 데이터는 `build()` 안에 튜플이나 딕셔너리 목록으로 두고, HTML은 `"".join(f"..." for ...)`로 만듭니다.
- 금액은 `won(12300)` → `12,300원`처럼 공통 함수로 표시합니다.
- 여러 위젯에 같은 숫자가 나오면(예: KPI 매출과 차트 합계) **같은 데이터에서 계산**해 값이 서로 맞게 합니다.
- 반응형은 `grid-template-columns:repeat(auto-fit,minmax(…))`와 `@media` 1~2개로 처리합니다.
- 실존 회사명, 로고, 인물 사진을 쓰지 않습니다. 샘플 데이터라면 푸터에 "가상의 정보"라고 적습니다.

## 4. 자주 생기는 문제

| 증상 | 원인 | 해결 |
|---|---|---|
| 섹션 내용이 화면 왼쪽 끝에 붙음 | 같은 요소에 `.wrap`과 `padding:72px 0`을 함께 써서 좌우 여백이 0이 됨 | `padding-top`, `padding-bottom`만 지정 |
| `header{padding:…}`이 적용되지 않음 | 요소 선택자가 `.wrap` 클래스 선택자보다 우선순위가 낮음 | `header.wrap{…}`처럼 클래스를 붙여 지정 |
| 한글 단어가 중간에서 끊김 | 기본 줄바꿈 규칙 | `word-break:keep-all` (기본 CSS에 포함) |
| flex 안의 `.wrap`이 가운데로 좁아짐 | flex 자식이 내용 너비로 줄어듦 | `.hero .wrap{width:100%}` |
| KPI 카드의 큰 숫자가 두 줄로 넘어감 | 자릿수가 많음 | `6,080만 원`처럼 단위를 바꿔 표시 |
| 파이썬 실행 시 `unsupported format character` | CSS 문자열에 `%` 포맷 사용 | 자리표시자 `.replace()` 방식으로 변경 |

## 5. 검증 체크리스트

- [ ] 파이썬 스크립트가 오류 없이 실행된다.
- [ ] 결과 HTML에 `<script`와 외부 주소(`http://`, `https://`)가 없다.
  ```bash
  grep -nE '<script|https?://' site/*.html || echo "OK: 스크립트·외부 리소스 없음"
  ```
- [ ] 너비 1280px(데스크톱)과 390px(모바일)에서 레이아웃이 깨지지 않는다. Playwright가 있으면 스크린샷으로 확인한다.
  ```bash
  python3 - <<'PY'
  from playwright.sync_api import sync_playwright
  import pathlib
  with sync_playwright() as p:
      b = p.chromium.launch()
      for w in (1280, 390):
          pg = b.new_page(viewport={"width": w, "height": 900})
          for f in pathlib.Path("site").glob("*.html"):
              pg.goto(f.resolve().as_uri())
              pg.screenshot(path=f"shot_{f.stem}_{w}.png", full_page=True)
      b.close()
  PY
  ```
- [ ] 유형별 설명 문서의 "필수 섹션"이 모두 들어 있다.
- [ ] 같은 숫자가 여러 곳에 나오면 값이 서로 일치한다.
- [ ] 샘플 데이터를 썼다면 푸터에 가상의 정보라고 적혀 있다.

## 6. 파일 구조

```
web-page-templates/
├── SKILL.md                    이 문서 (유형 선택표, 작업 순서, 규칙)
├── agents/openai.yaml          Codex 앱에 표시할 이름·설명
├── references/<key>.md         유형별 설명: 목적, 필수 섹션 순서, 디자인 규칙, 데이터
├── scripts/
│   ├── common.py               공통 CSS, page(), won()
│   ├── build.py                여러 유형을 한 번에 생성하는 명령줄 도구
│   └── page_types/<key>.py     유형별 샘플 코드 (META, build())
└── assets/samples/<key>.html   유형별 완성 샘플 HTML과 index.html
```
