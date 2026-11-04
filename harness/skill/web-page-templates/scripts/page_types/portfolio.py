"""
페이지 유형: 포트폴리오 — 프로덕트 디자이너 개인 사이트
구성: 큰 소개 문구, 작업물 그리드, 자기소개, 연락처

단독 실행:  python3 scripts/page_types/portfolio.py > portfolio.html
전체 생성:  python3 scripts/build.py portfolio --out ./site
"""
import datetime  # noqa: F401  (날짜 계산에 쓰는 유형이 있습니다)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FONT, SERIF, page, won  # noqa: E402,F401

PORT_CSS = """
body{color:#1c1c1c;background:#f4f1ea}
header .wrap{display:flex;justify-content:space-between;align-items:center;height:80px;font-size:15px}
header b{font-weight:700}
header nav{display:flex;gap:28px}
header .dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#16a34a;margin-right:6px}
.intro{padding-top:72px;padding-bottom:88px}
.intro h1{font-family:SERIF_FONT;font-weight:400;font-size:clamp(36px,6vw,76px);line-height:1.2;letter-spacing:-2px;max-width:1000px}
.intro h1 i{font-style:italic;color:#c2410c}
.intro p{margin-top:28px;font-size:18px;color:#555;max-width:520px}
.filter{display:flex;gap:10px;margin-bottom:28px;flex-wrap:wrap}
.filter span{border:1px solid #1c1c1c;border-radius:999px;padding:6px 16px;font-size:14px}
.filter span.on{background:#1c1c1c;color:#f4f1ea}
.works{display:grid;grid-template-columns:repeat(2,1fr);gap:48px 32px}
.work .img{border-radius:6px;aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;margin-bottom:16px;overflow:hidden;transition:transform .3s}
.work:hover .img{transform:scale(.985)}
.work .img span{font-family:SERIF_FONT;font-size:42px;color:rgba(255,255,255,.9);letter-spacing:-1px}
.work:nth-child(odd){margin-top:0}
.work:nth-child(even){margin-top:80px}
.work h3{font-size:20px;font-weight:600}
.work .info{display:flex;justify-content:space-between;color:#777;font-size:14px;margin-top:2px}
.about{display:grid;grid-template-columns:1fr 1fr;gap:64px;padding-top:140px;padding-bottom:100px;border-bottom:1px solid #d6d1c4}
.about h2{font-family:SERIF_FONT;font-weight:400;font-size:40px;line-height:1.3;letter-spacing:-1px}
.about p{color:#444;margin-bottom:16px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:32px}
.cols h4{font-size:13px;color:#888;font-weight:600;margin-bottom:8px;letter-spacing:1px}
.cols li{padding:3px 0}
.contact{padding-top:100px;padding-bottom:100px;text-align:center}
.contact small{color:#888}
.contact a.mail{display:block;font-family:SERIF_FONT;font-size:clamp(32px,6vw,72px);letter-spacing:-2px;margin:12px 0 24px;border-bottom:2px solid transparent}
.contact a.mail:hover{color:#c2410c}
.sns{display:flex;justify-content:center;gap:24px;color:#555}
footer{text-align:center;font-size:13px;color:#999;padding:24px 0 48px}
@media(max-width:760px){.works{grid-template-columns:1fr}.work:nth-child(even){margin-top:0}.about{grid-template-columns:1fr}header nav{display:none}}
""".replace("SERIF_FONT", SERIF)


def build_portfolio() -> str:
    works = [
        ("모바일 뱅킹 앱 리디자인", "UX/UI · 2026", "Bank", "#1e3a8a", "#60a5fa"),
        ("친환경 화장품 브랜드 아이덴티티", "Branding · 2025", "Verde", "#365314", "#a3e635"),
        ("도서관 예약 키오스크", "Product · 2025", "Kiosk", "#7c2d12", "#fb923c"),
        ("여행 큐레이션 웹사이트", "Web · 2024", "Trip", "#134e4a", "#5eead4"),
        ("음악 스트리밍 위젯 시스템", "Design System · 2024", "Play", "#581c87", "#e879f9"),
        ("헬스케어 대시보드", "UX/UI · 2023", "Care", "#3f3f46", "#d4d4d8"),
    ]
    works_html = "".join(
        f'<a class="work" href="#"><div class="img" style="background:linear-gradient(135deg,{c1},{c2})"><span>{k}</span></div>'
        f'<h3>{t}</h3><div class="info"><span>{cat}</span><span>사례 보기 ↗</span></div></a>'
        for t, cat, k, c1, c2 in works
    )
    # 필터 칩은 작업물 카테고리에서 파이썬이 자동으로 추출
    cats = sorted({w[1].split(" · ")[0] for w in works})
    filter_html = '<span class="on">전체 ' + str(len(works)) + "</span>" + "".join(f"<span>{c}</span>" for c in cats)

    body = f"""
<header><div class="wrap">
  <b>김하늘 — Product Designer</b>
  <nav><a href="#">작업물</a><a href="#">소개</a><a href="#">연락하기</a></nav>
  <span><span class="dot"></span>새 프로젝트 가능</span>
</div></header>

<section class="intro wrap">
  <h1>사람들의 하루를 <i>조금 덜 복잡하게</i> 만드는 디지털 제품을 디자인합니다.</h1>
  <p>서울에서 활동하는 8년 차 프로덕트 디자이너입니다. 금융, 헬스케어, 커머스 분야의 앱과 웹 서비스를 만들어 왔습니다.</p>
</section>

<section class="wrap">
  <div class="filter">{filter_html}</div>
  <div class="works">{works_html}</div>
</section>

<section class="wrap about">
  <h2>복잡한 문제를 단순한 화면으로 정리하는 일을 좋아합니다.</h2>
  <div>
    <p>사용자 인터뷰와 데이터 분석으로 문제를 정의하고, 빠르게 시안을 만들어 검증합니다.</p>
    <p>디자인이 실제 제품으로 구현될 때까지 개발자와 가까이에서 협업합니다.</p>
    <div class="cols">
      <div><h4>SERVICES</h4><ul><li>UX 리서치</li><li>UI 디자인</li><li>디자인 시스템</li><li>브랜딩</li></ul></div>
      <div><h4>CLIENTS</h4><ul><li>가상은행</li><li>그린코스메틱</li><li>트립노트</li><li>케어온</li></ul></div>
    </div>
  </div>
</section>

<section class="contact wrap">
  <small>함께 일하고 싶으시다면</small>
  <a class="mail" href="#">hello@haneul.design</a>
  <div class="sns"><a href="#">Behance</a><a href="#">Dribbble</a><a href="#">LinkedIn</a><a href="#">Instagram</a></div>
</section>
<footer>© 2026 Kim Haneul. 이 페이지의 인물과 작업물은 모두 가상의 예시입니다.</footer>
"""
    return page("김하늘 — 포트폴리오 홈 샘플", PORT_CSS, body)


META = {
    "key": "portfolio",
    "file": "portfolio.html",
    "kind": "포트폴리오",
    "title": "프로덕트 디자이너 개인 사이트",
    "name": "Kim Haneul",
    "desc": "큰 소개 문구, 작업물 그리드, 자기소개, 연락처",
    "thumb": "linear-gradient(135deg,#c2410c,#f4f1ea)",
}
build = build_portfolio

if __name__ == "__main__":
    import common
    common.SHOW_BACK = False
    sys.stdout.write(build())
