"""
페이지 유형: 대시보드 — 쇼핑몰 관리자 화면
구성: 사이드바 메뉴, KPI 카드, 막대·도넛 차트, 최근 주문 표

단독 실행:  python3 scripts/page_types/dashboard.py > dashboard.html
전체 생성:  python3 scripts/build.py dashboard --out ./site
"""
import datetime  # noqa: F401  (날짜 계산에 쓰는 유형이 있습니다)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FONT, SERIF, page, won  # noqa: E402,F401

DASH_CSS = """
body{color:#0f172a;background:#f1f5f9;font-size:14px}
.app{display:grid;grid-template-columns:232px 1fr;min-height:100vh}
.side{background:#0f172a;color:#cbd5e1;padding:24px 16px;display:flex;flex-direction:column}
.side .logo{color:#fff;font-weight:800;font-size:19px;padding:0 10px 28px}
.side .logo span{color:#60a5fa}
.side small{font-size:11px;letter-spacing:1px;color:#64748b;padding:16px 10px 8px;display:block}
.side a{display:flex;align-items:center;gap:10px;padding:10px;border-radius:8px}
.side a.on{background:#1e293b;color:#fff;font-weight:600}
.side a:hover{background:#1e293b}
.side .me{margin-top:auto;display:flex;gap:10px;align-items:center;padding:10px;border-top:1px solid #1e293b}
.side .av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#60a5fa,#a78bfa)}
main{padding:28px 32px;min-width:0}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;gap:16px;flex-wrap:wrap}
.topbar h1{font-size:24px;letter-spacing:-.5px}
.topbar p{color:#64748b}
.topbar .r{display:flex;gap:10px}
.topbar select,.topbar .btn{border:1px solid #cbd5e1;background:#fff;border-radius:8px;padding:9px 14px}
.topbar .btn.p{background:#2563eb;color:#fff;border-color:#2563eb;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:16px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px}
.kpi .lab{color:#64748b}
.kpi .val{font-size:28px;font-weight:800;letter-spacing:-.5px;margin:6px 0}
.up{color:#16a34a;font-weight:600}
.down{color:#dc2626;font-weight:600}
.kpi .vs{color:#94a3b8}
.row{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:16px}
.card h3{font-size:16px;margin-bottom:4px}
.card .hint{color:#94a3b8;margin-bottom:20px}
.chart{display:flex;align-items:flex-end;gap:12px;height:240px;border-bottom:1px solid #e2e8f0;padding:0 4px;position:relative}
.chart::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(to top,#f1f5f9 0 1px,transparent 1px 60px)}
.col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;position:relative}
.col i{display:block;width:100%;max-width:36px;background:#bfdbfe;border-radius:6px 6px 0 0}
.col.last i{background:#2563eb}
.col em{font-style:normal;font-size:11px;color:#64748b;margin-bottom:4px}
.months{display:flex;gap:12px;padding:8px 4px 0}
.months span{flex:1;text-align:center;color:#94a3b8;font-size:12px}
.donut{width:180px;height:180px;border-radius:50%;margin:8px auto 20px;position:relative}
.donut::after{content:"";position:absolute;inset:34px;background:#fff;border-radius:50%}
.donut b{position:absolute;inset:0;display:grid;place-items:center;z-index:1;font-size:15px;text-align:center;line-height:1.3}
.legend li{display:flex;justify-content:space-between;padding:6px 0}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:8px}
table{width:100%;border-collapse:collapse}
th{text-align:left;color:#64748b;font-weight:500;padding:10px 12px;border-bottom:1px solid #e2e8f0;background:#f8fafc}
td{padding:12px;border-bottom:1px solid #f1f5f9}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.pill{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600}
.pill.ok{background:#dcfce7;color:#166534}.pill.ship{background:#dbeafe;color:#1e40af}
.pill.wait{background:#fef9c3;color:#854d0e}.pill.cancel{background:#fee2e2;color:#991b1b}
@media(max-width:1000px){.kpis{grid-template-columns:repeat(2,1fr)}.row{grid-template-columns:1fr}}
@media(max-width:720px){.app{grid-template-columns:1fr}.side{display:none}main{padding:20px}}
"""


def build_dashboard() -> str:
    # 월별 매출(만 원). 막대 높이는 최댓값 대비 비율로 파이썬이 계산
    monthly = [("5월", 3820), ("6월", 4150), ("7월", 3960), ("8월", 4710), ("9월", 5230), ("10월", 6080)]
    peak = max(v for _, v in monthly)
    bars = ""
    for i, (mon, v) in enumerate(monthly):
        last = " last" if i == len(monthly) - 1 else ""
        bars += f'<div class="col{last}"><em>{v:,}</em><i style="height:{v / peak * 88:.1f}%"></i></div>'
    months = "".join(f"<span>{m}</span>" for m, _ in monthly)

    # KPI: 이번 달과 지난달을 비교해 증감률 계산
    kpis = [("총 매출", 60800000, 52300000, "원"), ("주문 수", 1842, 1660, "건"),
            ("신규 고객", 512, 548, "명"), ("평균 주문 금액", 33008, 31506, "원")]
    kpi_html = ""
    for lab, cur, prev, unit in kpis:
        rate = (cur - prev) / prev * 100
        shown = f"{cur // 10000:,}만 원" if cur >= 10_000_000 else f"{cur:,}{unit}"
        cls, arrow = ("up", "▲") if rate >= 0 else ("down", "▼")
        kpi_html += (f'<div class="card kpi"><div class="lab">{lab}</div><div class="val">{shown}</div>'
                     f'<span class="{cls}">{arrow} {abs(rate):.1f}%</span> <span class="vs">지난달 대비</span></div>')

    # 채널별 비중 → conic-gradient 각도를 누적 비율로 계산
    channels = [("자사몰", 2790, "#2563eb"), ("오픈마켓", 1610, "#60a5fa"), ("앱", 1110, "#a78bfa"), ("오프라인", 570, "#cbd5e1")]  # 합계 = 10월 매출 6,080만 원
    total = sum(v for _, v, _ in channels)
    stops, acc, legend = [], 0.0, ""
    for name, v, color in channels:
        pct = v / total * 100
        stops.append(f"{color} {acc:.1f}% {acc + pct:.1f}%")
        acc += pct
        legend += f'<li><span><i style="background:{color}"></i>{name}</span><b>{pct:.1f}%</b></li>'
    conic = "conic-gradient(" + ", ".join(stops) + ")"

    status = {"결제 완료": "ok", "배송 중": "ship", "입금 대기": "wait", "취소": "cancel"}
    orders = [("#20261028-0142", "김민수", "울 블렌드 오버핏 코트", 202300, "결제 완료"),
              ("#20261028-0141", "이지은", "헤비 코튼 스웨트셔츠 외 1건", 109300, "배송 중"),
              ("#20261028-0139", "박준호", "클래식 레더 스니커즈", 100600, "입금 대기"),
              ("#20261027-0388", "최서연", "캐시미어 머플러", 58800, "배송 중"),
              ("#20261027-0377", "정우진", "나일론 데일리 백팩", 80100, "취소")]
    rows = "".join(
        f'<tr><td>{no}</td><td>{who}</td><td>{item}</td><td class="num">{won(amt)}</td>'
        f'<td><span class="pill {status[st]}">{st}</span></td></tr>' for no, who, item, amt, st in orders
    )
    today = datetime.date.today()

    body = f"""
<div class="app">
  <aside class="side">
    <div class="logo">mono<span>admin</span></div>
    <a class="on" href="#">📊 대시보드</a><a href="#">🧾 주문 관리</a><a href="#">📦 상품 관리</a><a href="#">👥 고객 관리</a>
    <small>마케팅</small>
    <a href="#">🎟️ 쿠폰·이벤트</a><a href="#">📈 광고 성과</a>
    <small>설정</small>
    <a href="#">⚙️ 스토어 설정</a>
    <div class="me"><div class="av"></div><div><b style="color:#fff">관리자</b><br><span style="font-size:12px">admin@mono.kr</span></div></div>
  </aside>
  <main>
    <div class="topbar">
      <div><h1>대시보드</h1><p>{today:%Y년 %m월 %d일} 기준 · 이번 달 운영 현황</p></div>
      <div class="r"><select><option>최근 6개월</option><option>최근 30일</option></select><a class="btn p" href="#">보고서 내려받기</a></div>
    </div>
    <div class="kpis">{kpi_html}</div>
    <div class="row">
      <div class="card"><h3>월별 매출</h3><div class="hint">단위: 만 원</div>
        <div class="chart">{bars}</div><div class="months">{months}</div></div>
      <div class="card"><h3>판매 채널 비중</h3><div class="hint">이번 달 매출 기준</div>
        <div class="donut" style="background:{conic}"><b>총 매출<br>{total:,}만 원</b></div>
        <ul class="legend">{legend}</ul></div>
    </div>
    <div class="card"><h3>최근 주문</h3><div class="hint">최근 들어온 주문 5건</div>
      <table><thead><tr><th>주문 번호</th><th>고객</th><th>상품</th><th style="text-align:right">결제 금액</th><th>상태</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
  </main>
</div>
"""
    return page("mono admin — 대시보드 홈 샘플", DASH_CSS, body)


META = {
    "key": "dashboard",
    "file": "dashboard.html",
    "kind": "대시보드",
    "title": "쇼핑몰 관리자 화면",
    "name": "mono admin",
    "desc": "사이드바 메뉴, KPI 카드, 막대·도넛 차트, 최근 주문 표",
    "thumb": "linear-gradient(135deg,#0f172a,#2563eb)",
}
build = build_dashboard

if __name__ == "__main__":
    import common
    common.SHOW_BACK = False
    sys.stdout.write(build())
