"""
페이지 유형: 마케팅 랜딩 — 업무 자동화 서비스 소개
구성: 히어로, 기능, 사용 방법, 후기, 요금제, FAQ, CTA 순서로 설득하는 구조

단독 실행:  python3 scripts/page_types/landing.py > landing.html
전체 생성:  python3 scripts/build.py landing --out ./site
"""
import datetime  # noqa: F401  (날짜 계산에 쓰는 유형이 있습니다)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FONT, SERIF, page, won  # noqa: E402,F401

LANDING_CSS = """
body{color:#1a1a2e;background:#fff}
nav{position:sticky;top:0;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid #eee;z-index:10}
nav .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-weight:800;font-size:21px;color:#4f46e5;letter-spacing:-.5px}
.menu{display:flex;gap:28px;font-size:15px;color:#555}
.btn{display:inline-block;padding:12px 22px;border-radius:10px;font-weight:600;font-size:15px}
.btn-primary{background:#4f46e5;color:#fff}
.btn-ghost{border:1px solid #d4d4d8;color:#333;background:#fff}
.hero{padding:96px 0 64px;text-align:center;background:radial-gradient(ellipse at top,#eef2ff,#fff 70%)}
.badge{display:inline-block;padding:6px 14px;border-radius:999px;background:#e0e7ff;color:#4338ca;font-size:13px;font-weight:600;margin-bottom:20px}
.hero h1{font-size:clamp(34px,5vw,56px);line-height:1.2;letter-spacing:-1.5px;margin-bottom:20px}
.hero h1 em{font-style:normal;color:#4f46e5}
.hero p{font-size:18px;color:#555;max-width:600px;margin:0 auto 32px}
.actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.mock{margin:56px auto 0;max-width:900px;border-radius:14px;border:1px solid #e5e7eb;box-shadow:0 30px 60px -20px rgba(79,70,229,.3);background:#fff;overflow:hidden;text-align:left}
.mock-bar{height:36px;background:#f3f4f6;display:flex;align-items:center;gap:6px;padding:0 14px}
.mock-bar span{width:10px;height:10px;border-radius:50%;background:#d1d5db}
.mock-body{display:grid;grid-template-columns:180px 1fr;min-height:280px}
.mock-side{background:#fafafa;border-right:1px solid #eee;padding:18px}
.mock-side div{height:10px;background:#e5e7eb;border-radius:4px;margin-bottom:16px}
.mock-side div:first-child{background:#c7d2fe;width:70%}
.mock-main{padding:20px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;align-content:start}
.mcard{height:90px;border-radius:10px;background:linear-gradient(135deg,#eef2ff,#e0e7ff)}
.mcard.wide{grid-column:span 3;height:130px;background:linear-gradient(135deg,#f5f3ff,#ede9fe)}
.logos{padding:40px 0 24px;text-align:center;color:#999;font-size:14px}
.logos .row{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;margin-top:16px;font-weight:800;font-size:20px;color:#c4c4cc;letter-spacing:-.5px}
section{padding:80px 0}
.sec-title{text-align:center;margin-bottom:48px}
.sec-title small{color:#4f46e5;font-weight:700;font-size:14px}
.sec-title h2{font-size:34px;letter-spacing:-.8px;margin:6px 0 10px}
.sec-title p{color:#666}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}
.feature{padding:28px;border:1px solid #eee;border-radius:14px}
.icon{width:46px;height:46px;border-radius:12px;background:#eef2ff;display:grid;place-items:center;font-size:22px;margin-bottom:16px}
.feature h3{font-size:18px;margin-bottom:8px}
.feature p{color:#666;font-size:15px}
.steps{background:#f9fafb}
.step{text-align:center;padding:0 12px}
.step .num{width:48px;height:48px;border-radius:50%;background:#4f46e5;color:#fff;font-weight:700;display:grid;place-items:center;margin:0 auto 14px;font-size:18px}
.step h3{margin-bottom:6px}
.step p{color:#666;font-size:15px}
.quote{padding:28px;border-radius:14px;background:#fff;border:1px solid #eee}
.quote .stars{color:#f59e0b;margin-bottom:10px;letter-spacing:2px}
.quote p{margin-bottom:16px}
.quote .who{font-size:14px;color:#888}
.price{padding:32px;border:1px solid #e5e7eb;border-radius:16px;display:flex;flex-direction:column;background:#fff}
.price.pop{border:2px solid #4f46e5;box-shadow:0 20px 40px -20px rgba(79,70,229,.45);position:relative}
.price.pop::before{content:"가장 인기";position:absolute;top:-13px;left:32px;background:#4f46e5;color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}
.price h3{font-size:18px}
.price .amt{font-size:38px;font-weight:800;margin:12px 0 4px;letter-spacing:-1px}
.price .amt small{font-size:15px;color:#888;font-weight:400}
.price .desc{color:#777;font-size:14px}
.price ul{margin:20px 0 28px;flex:1}
.price li{padding:6px 0;color:#444;font-size:15px}
.price li::before{content:"✓  ";color:#4f46e5;font-weight:700}
.price .btn{text-align:center}
.faq{max-width:720px;margin:0 auto}
details{border-bottom:1px solid #eee;padding:20px 0}
summary{cursor:pointer;font-weight:600;font-size:17px}
details p{margin-top:10px;color:#666}
.cta{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;text-align:center;border-radius:24px;padding:72px 24px}
.cta h2{font-size:34px;letter-spacing:-.8px;margin-bottom:10px}
.cta p{opacity:.85}
.cta .btn{background:#fff;color:#4f46e5;margin-top:24px}
footer{border-top:1px solid #eee;padding:32px 0;color:#999;font-size:14px;margin-top:80px}
footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
@media(max-width:760px){.menu{display:none}.mock-body{grid-template-columns:1fr}.mock-side{display:none}}
"""


def build_landing() -> str:
    features = [
        ("⚡", "반복 업무 자동화", "매일 하는 보고서 작성, 데이터 정리, 알림 발송을 클릭 몇 번으로 자동화합니다."),
        ("🔗", "200개 앱 연동", "메일, 메신저, 스프레드시트, CRM을 코드 없이 하나의 흐름으로 연결합니다."),
        ("📊", "실시간 현황판", "자동화가 언제, 몇 번 실행됐는지 한 화면에서 확인할 수 있습니다."),
        ("🔒", "기업 수준 보안", "모든 데이터는 암호화해서 저장하고, 권한을 팀 단위로 관리합니다."),
    ]
    steps = [
        ("앱 연결", "사용 중인 서비스 계정을 연결합니다."),
        ("흐름 만들기", "템플릿을 고르거나 블록을 끌어다 놓습니다."),
        ("실행과 확인", "자동화를 켜고 결과를 현황판에서 확인합니다."),
    ]
    reviews = [
        ("주간 보고서 만드는 데 쓰던 3시간이 10분으로 줄었습니다.", "박지민 · 스타트업 운영팀장"),
        ("개발자에게 부탁하지 않고 마케팅팀이 직접 자동화를 만듭니다.", "이서준 · 커머스 마케터"),
        ("도입 첫 달에 고객 응답 시간이 절반으로 줄었습니다.", "최유나 · CS 매니저"),
    ]
    plans = [
        ("무료", 0, "개인이 가볍게 시작할 때", ["자동화 5개", "월 실행 1,000회", "기본 앱 연동"], False),
        ("프로", 19000, "성장하는 팀을 위해", ["자동화 무제한", "월 실행 50,000회", "모든 앱 연동", "우선 지원"], True),
        ("엔터프라이즈", None, "대규모 조직을 위해", ["전용 서버", "SSO·감사 로그", "전담 매니저", "SLA 보장"], False),
    ]
    faqs = [
        ("코딩을 몰라도 사용할 수 있나요?", "네. 모든 기능은 끌어다 놓기 방식으로 만들 수 있고, 자주 쓰는 흐름은 템플릿으로 제공합니다."),
        ("무료 체험 기간이 끝나면 자동으로 결제되나요?", "아니요. 결제 수단을 등록하기 전에는 자동으로 결제되지 않습니다."),
        ("언제든 해지할 수 있나요?", "네. 설정 화면에서 바로 해지할 수 있고, 남은 기간은 일할 계산해서 환불합니다."),
    ]

    feature_html = "".join(
        f'<div class="feature"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in features
    )
    step_html = "".join(
        f'<div class="step"><div class="num">{n}</div><h3>{t}</h3><p>{d}</p></div>'
        for n, (t, d) in enumerate(steps, 1)
    )
    review_html = "".join(
        f'<div class="quote"><div class="stars">★★★★★</div><p>“{q}”</p><div class="who">{w}</div></div>'
        for q, w in reviews
    )
    plan_html = ""
    for name, price, desc, items, pop in plans:
        amt = "문의" if price is None else (f"{price:,}원<small> / 월</small>" if price else "0원")
        lis = "".join(f"<li>{x}</li>" for x in items)
        btn = "btn-primary" if pop else "btn-ghost"
        label = "영업팀 문의" if price is None else "시작하기"
        plan_html += (
            f'<div class="price{" pop" if pop else ""}"><h3>{name}</h3><div class="amt">{amt}</div>'
            f'<div class="desc">{desc}</div><ul>{lis}</ul><a class="btn {btn}" href="#">{label}</a></div>'
        )
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    logos = "".join(f"<span>{x}</span>" for x in ["NOVA", "Bluepeak", "ORBIT", "hanul", "Kite&Co", "PIXELA"])

    body = f"""
<nav><div class="wrap">
  <div class="logo">Flowly</div>
  <div class="menu"><a href="#">기능</a><a href="#">고객 사례</a><a href="#">요금제</a><a href="#">자주 묻는 질문</a></div>
  <a class="btn btn-primary" href="#">무료로 시작하기</a>
</div></nav>

<header class="hero"><div class="wrap">
  <span class="badge">NEW · AI 자동화 추천 기능 출시</span>
  <h1>반복 업무는 맡기고,<br><em>중요한 일</em>에 집중하세요</h1>
  <p>Flowly는 흩어진 업무 도구를 하나로 연결해 반복 작업을 자동으로 처리하는 업무 자동화 서비스입니다.</p>
  <div class="actions"><a class="btn btn-primary" href="#">14일 무료 체험</a><a class="btn btn-ghost" href="#">소개 영상 보기</a></div>
  <div class="mock">
    <div class="mock-bar"><span></span><span></span><span></span></div>
    <div class="mock-body">
      <div class="mock-side"><div></div><div></div><div></div><div></div><div></div></div>
      <div class="mock-main"><div class="mcard wide"></div><div class="mcard"></div><div class="mcard"></div><div class="mcard"></div></div>
    </div>
  </div>
</div></header>

<div class="logos wrap">3,000개가 넘는 팀이 Flowly를 사용합니다<div class="row">{logos}</div></div>

<section><div class="wrap">
  <div class="sec-title"><small>FEATURES</small><h2>업무 시간을 줄이는 핵심 기능</h2><p>필요한 기능만 골라서 바로 사용할 수 있습니다.</p></div>
  <div class="grid">{feature_html}</div>
</div></section>

<section class="steps"><div class="wrap">
  <div class="sec-title"><small>HOW IT WORKS</small><h2>세 단계면 준비가 끝납니다</h2></div>
  <div class="grid">{step_html}</div>
</div></section>

<section><div class="wrap">
  <div class="sec-title"><small>REVIEWS</small><h2>먼저 사용한 고객의 이야기</h2></div>
  <div class="grid">{review_html}</div>
</div></section>

<section class="steps"><div class="wrap">
  <div class="sec-title"><small>PRICING</small><h2>팀 규모에 맞는 요금제</h2><p>모든 유료 요금제는 14일 동안 무료로 체험할 수 있습니다.</p></div>
  <div class="grid">{plan_html}</div>
</div></section>

<section><div class="wrap">
  <div class="sec-title"><small>FAQ</small><h2>자주 묻는 질문</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>

<div class="wrap"><div class="cta">
  <h2>지금 바로 첫 자동화를 만들어 보세요</h2>
  <p>신용카드 등록 없이 무료로 시작할 수 있습니다.</p>
  <a class="btn" href="#">무료로 시작하기</a>
</div></div>

<footer><div class="wrap"><span>© 2026 Flowly Inc.</span><span>이용약관 · 개인정보처리방침 · 문의하기</span></div></footer>
"""
    return page("Flowly — 업무 자동화 (마케팅 랜딩 페이지 샘플)", LANDING_CSS, body)


META = {
    "key": "landing",
    "file": "landing.html",
    "kind": "마케팅 랜딩",
    "title": "업무 자동화 서비스 소개",
    "name": "Flowly",
    "desc": "히어로, 기능, 사용 방법, 후기, 요금제, FAQ, CTA 순서로 설득하는 구조",
    "thumb": "linear-gradient(135deg,#4f46e5,#7c3aed)",
}
build = build_landing

if __name__ == "__main__":
    import common
    common.SHOW_BACK = False
    sys.stdout.write(build())
