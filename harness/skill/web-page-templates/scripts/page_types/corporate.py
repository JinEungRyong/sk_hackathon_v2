"""
페이지 유형: 기업 소개 — 기술 기업 코퍼레이트 사이트
구성: 비전 문구, 사업 영역, 숫자로 보는 회사, 뉴스룸, 채용 배너

단독 실행:  python3 scripts/page_types/corporate.py > corporate.html
전체 생성:  python3 scripts/build.py corporate --out ./site
"""
import datetime  # noqa: F401  (날짜 계산에 쓰는 유형이 있습니다)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FONT, SERIF, page, won  # noqa: E402,F401

CORP_CSS = """
body{color:#1f2937;background:#fff}
header{position:absolute;top:0;left:0;right:0;z-index:5;color:#fff}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:80px}
.logo{font-weight:800;font-size:22px;letter-spacing:-.5px}
.logo span{color:#38bdf8}
header nav{display:flex;gap:36px;font-size:15px;font-weight:500}
.lang{font-size:13px;opacity:.8}
.hero .wrap{width:100%}
.hero{min-height:600px;display:flex;align-items:center;color:#fff;
  background:linear-gradient(120deg,rgba(11,37,69,.96) 30%,rgba(19,64,116,.75)),
  repeating-linear-gradient(45deg,#13406f 0 2px,transparent 2px 24px),#0b2545}
.hero small{color:#7dd3fc;font-weight:700;letter-spacing:2px}
.hero h1{font-size:clamp(34px,5vw,58px);line-height:1.25;letter-spacing:-1.5px;margin:16px 0 24px}
.hero p{font-size:18px;opacity:.85;max-width:560px}
.hero .btns{margin-top:36px;display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-block;padding:14px 26px;font-weight:600;font-size:15px;border-radius:4px}
.btn.solid{background:#fff;color:#0b2545}
.btn.line{border:1px solid rgba(255,255,255,.6)}
section{padding:96px 0}
.label{color:#0369a1;font-weight:700;font-size:14px;letter-spacing:1.5px}
.title{font-size:36px;letter-spacing:-1px;margin:8px 0 48px;line-height:1.3}
.biz{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.biz a{display:block;border:1px solid #e5e7eb;border-radius:6px;overflow:hidden;transition:.2s}
.biz a:hover{box-shadow:0 16px 32px -16px rgba(11,37,69,.35);transform:translateY(-3px)}
.biz .img{height:180px}
.biz .txt{padding:24px}
.biz h3{font-size:20px;margin-bottom:8px}
.biz p{color:#6b7280;font-size:15px}
.biz .go{display:inline-block;margin-top:14px;color:#0369a1;font-weight:600;font-size:14px}
.stats{background:#0b2545;color:#fff;padding:72px 0}
.stats .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;text-align:center}
.stats b{display:block;font-size:44px;font-weight:800;letter-spacing:-1px}
.stats b small{font-size:20px;font-weight:600;margin-left:2px}
.stats span{opacity:.7;font-size:15px}
.two{display:grid;grid-template-columns:1.4fr 1fr;gap:48px}
.news li{display:flex;justify-content:space-between;gap:16px;padding:18px 0;border-bottom:1px solid #e5e7eb}
.news li:first-child{border-top:2px solid #0b2545}
.news .cat{font-size:12px;color:#0369a1;font-weight:700;margin-right:10px}
.news time{color:#9ca3af;font-size:14px;white-space:nowrap}
.recruit{background:linear-gradient(150deg,#0369a1,#0b2545);color:#fff;border-radius:8px;padding:40px;display:flex;flex-direction:column;justify-content:space-between;min-height:300px}
.recruit h3{font-size:26px;line-height:1.35;margin:10px 0}
.recruit p{opacity:.8}
.recruit .btn{align-self:flex-start;background:#fff;color:#0b2545;margin-top:20px}
footer{background:#111827;color:#9ca3af;font-size:14px;padding:48px 0}
footer .wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
footer b{color:#fff;font-size:18px}
@media(max-width:820px){header nav{display:none}.stats .wrap{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}}
"""


def build_corporate() -> str:
    biz = [
        ("스마트 팩토리", "센서와 데이터 분석으로 생산 설비의 고장을 미리 예측합니다.", "#0ea5e9", "#0b2545"),
        ("클라우드 인프라", "기업 시스템을 안정적인 클라우드 환경으로 옮기고 운영합니다.", "#6366f1", "#1e1b4b"),
        ("에너지 관리", "건물과 공장의 전력 사용량을 분석해 에너지 비용을 줄입니다.", "#10b981", "#064e3b"),
    ]
    founded = 2004
    years = datetime.date.today().year - founded  # 업력은 파이썬이 계산
    stats = [(f"{years}", "년", "설립 이후 업력"), ("1,200", "명", "임직원 수"),
             ("38", "개국", "글로벌 고객사 진출"), ("4,800", "억", "2025년 매출")]
    news = [
        ("보도자료", "한빛솔루션, 유럽 제조사와 스마트 팩토리 공급 계약 체결", "2026.10.21"),
        ("공지", "2026년 3분기 경영 실적 발표", "2026.10.15"),
        ("보도자료", "탄소 배출 30% 감축 목표 조기 달성", "2026.09.30"),
        ("수상", "대한민국 기술혁신 대상 산업통상자원부 장관상 수상", "2026.09.12"),
    ]
    biz_html = "".join(
        f'<a href="#"><div class="img" style="background:linear-gradient(135deg,{c1},{c2})"></div>'
        f'<div class="txt"><h3>{t}</h3><p>{d}</p><span class="go">자세히 보기 →</span></div></a>'
        for t, d, c1, c2 in biz
    )
    stat_html = "".join(f"<div><b>{n}<small>{u}</small></b><span>{l}</span></div>" for n, u, l in stats)
    news_html = "".join(
        f'<li><a href="#"><span class="cat">{c}</span>{t}</a><time>{d}</time></li>' for c, t, d in news
    )

    body = f"""
<header><div class="wrap">
  <div class="logo">HANBIT<span>.</span></div>
  <nav><a href="#">회사 소개</a><a href="#">사업 영역</a><a href="#">투자 정보</a><a href="#">지속가능경영</a><a href="#">인재 채용</a></nav>
  <div class="lang">KOR | ENG</div>
</div></header>

<div class="hero"><div class="wrap">
  <small>SINCE {founded}</small>
  <h1>기술로 산업의 내일을<br>더 단단하게 만듭니다</h1>
  <p>한빛솔루션은 제조, 인프라, 에너지 분야의 디지털 전환을 함께 설계하고 실행하는 기술 파트너입니다.</p>
  <div class="btns"><a class="btn solid" href="#">회사 소개 보기</a><a class="btn line" href="#">사업 문의하기</a></div>
</div></div>

<section><div class="wrap">
  <div class="label">BUSINESS</div>
  <h2 class="title">핵심 사업 영역</h2>
  <div class="biz">{biz_html}</div>
</div></section>

<div class="stats"><div class="wrap">{stat_html}</div></div>

<section><div class="wrap two">
  <div>
    <div class="label">NEWSROOM</div>
    <h2 class="title" style="margin-bottom:24px">새 소식</h2>
    <ul class="news">{news_html}</ul>
  </div>
  <div class="recruit">
    <div><small style="opacity:.8;font-weight:700;letter-spacing:1.5px">CAREERS</small>
    <h3>함께 성장할<br>동료를 찾습니다</h3>
    <p>2026년 하반기 신입·경력 공개 채용이 진행 중입니다.</p></div>
    <a class="btn" href="#">채용 공고 보기</a>
  </div>
</div></section>

<footer><div class="wrap">
  <div><b>HANBIT.</b><br><br>(주)한빛솔루션 · 서울특별시 OO구 OO로 000 · 대표전화 02-000-0000<br>
  © 2026 HANBIT Solution. 이 페이지의 회사 정보는 모두 가상의 정보입니다.</div>
  <div>개인정보처리방침 · 윤리경영 제보 · 사이트맵</div>
</div></footer>
"""
    return page("한빛솔루션 — 기업 소개 홈 샘플", CORP_CSS, body)


META = {
    "key": "corporate",
    "file": "corporate.html",
    "kind": "기업 소개",
    "title": "기술 기업 코퍼레이트 사이트",
    "name": "HANBIT.",
    "desc": "비전 문구, 사업 영역, 숫자로 보는 회사, 뉴스룸, 채용 배너",
    "thumb": "linear-gradient(135deg,#0b2545,#0369a1)",
}
build = build_corporate

if __name__ == "__main__":
    import common
    common.SHOW_BACK = False
    sys.stdout.write(build())
