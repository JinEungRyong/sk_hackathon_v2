"""
페이지 유형: 쇼핑몰 — 패션·라이프스타일 쇼핑몰
구성: 검색창, 카테고리, 기획전 배너, 랭킹·세일 상품 그리드, 혜택 안내

단독 실행:  python3 scripts/page_types/shop.py > shop.html
전체 생성:  python3 scripts/build.py shop --out ./site
"""
import datetime  # noqa: F401  (날짜 계산에 쓰는 유형이 있습니다)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FONT, SERIF, page, won  # noqa: E402,F401

SHOP_CSS = """
body{color:#111;background:#fff}
.notice{background:#111;color:#fff;text-align:center;font-size:13px;padding:8px}
header .wrap{display:flex;align-items:center;gap:32px;height:76px}
.logo{font-size:26px;font-weight:900;letter-spacing:-1.5px}
.search{flex:1;max-width:440px;display:flex;border:2px solid #111;border-radius:999px;overflow:hidden}
.search input{flex:1;border:0;padding:10px 18px;font-size:14px;outline:0;min-width:0}
.search button{border:0;background:#111;color:#fff;padding:0 22px;font-weight:600;cursor:pointer}
.util{margin-left:auto;display:flex;gap:22px;font-size:14px;color:#444}
.cats{border-top:1px solid #eee;border-bottom:1px solid #eee;position:sticky;top:0;background:#fff;z-index:5}
.cats .wrap{display:flex;gap:30px;height:50px;align-items:center;font-size:15px;font-weight:600;overflow-x:auto;white-space:nowrap}
.cats .sale{color:#e11d48}
.banner{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-top:24px}
.bn{border-radius:18px;padding:40px;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;min-height:380px}
.bn.main{background:linear-gradient(135deg,#334155 0%,#94a3b8 100%)}
.bn.sub{background:linear-gradient(160deg,#f59e0b,#e11d48)}
.bn small{opacity:.85;font-weight:600}
.bn h2{font-size:36px;line-height:1.25;margin:8px 0 18px;letter-spacing:-1px}
.bn.sub h2{font-size:28px}
.bn .more{font-size:14px;font-weight:600;border-bottom:1px solid #fff;align-self:flex-start}
.circles{display:grid;grid-template-columns:repeat(8,1fr);gap:14px;text-align:center;margin-top:44px;font-size:14px;font-weight:500}
.circle{aspect-ratio:1;border-radius:50%;margin-bottom:8px;display:grid;place-items:center;font-size:30px;background:#f4f4f5}
.sec-head{display:flex;justify-content:space-between;align-items:end;margin:56px 0 20px}
.sec-head h3{font-size:23px;letter-spacing:-.5px}
.sec-head p{font-size:14px;color:#888}
.sec-head a{font-size:14px;color:#777}
.products{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:32px 16px}
.thumb{aspect-ratio:3/4;border-radius:10px;position:relative;margin-bottom:12px;overflow:hidden}
.thumb .rank{position:absolute;top:0;left:0;background:#111;color:#fff;font-weight:800;font-size:14px;width:30px;height:30px;display:grid;place-items:center}
.tag{position:absolute;bottom:10px;left:10px;background:#fff;font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px}
.heart{position:absolute;bottom:10px;right:12px;color:#fff;font-size:20px}
.brand{font-size:13px;font-weight:700}
.name{font-size:14px;color:#444;margin:2px 0 6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dc{color:#e11d48;font-weight:800;margin-right:6px}
.now{font-weight:800}
.orig{font-size:13px;color:#aaa;text-decoration:line-through;margin-left:6px}
.meta{font-size:12px;color:#999;margin-top:4px}
.benefits{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:64px}
.benefit{background:#f5f5f4;border-radius:14px;padding:22px}
.benefit b{display:block;font-size:16px;margin-bottom:4px}
.benefit span{font-size:14px;color:#666}
footer{background:#f7f7f7;padding:44px 0;font-size:13px;color:#888;margin-top:72px}
footer b{color:#333;font-size:15px;display:block;margin-bottom:8px}
@media(max-width:820px){.banner{grid-template-columns:1fr}.circles{grid-template-columns:repeat(4,1fr)}.util{display:none}}
"""


def build_shop() -> str:
    categories = [("👕", "상의"), ("👖", "하의"), ("🧥", "아우터"), ("👟", "신발"),
                  ("👜", "가방"), ("⌚", "액세서리"), ("🛋️", "리빙"), ("🧴", "뷰티")]
    # (브랜드, 상품명, 정가, 할인율 %, 리뷰 수, 태그, 그라데이션 시작색, 끝색)
    products = [
        ("LOWFIELD", "울 블렌드 오버핏 코트", 289000, 30, 1284, "단독", "#a8a29e", "#57534e"),
        ("MONO BASIC", "헤비 코튼 스웨트셔츠", 59000, 15, 3921, "무료배송", "#cbd5e1", "#64748b"),
        ("ARCHIVE 9", "와이드 데님 팬츠", 79000, 0, 842, "신상", "#93c5fd", "#1e3a8a"),
        ("SOFTSTEP", "클래식 레더 스니커즈", 129000, 22, 2210, "베스트", "#fde68a", "#b45309"),
        ("NORDIK", "캐시미어 머플러", 98000, 40, 512, "시즌오프", "#fecaca", "#b91c1c"),
        ("CARRY ON", "나일론 데일리 백팩", 89000, 10, 1677, "무료배송", "#bbf7d0", "#166534"),
        ("LOWFIELD", "퀼팅 경량 패딩 조끼", 119000, 25, 905, "단독", "#ddd6fe", "#5b21b6"),
        ("HOMEMADE", "리넨 쿠션 커버 2종", 32000, 0, 388, "신상", "#fed7aa", "#c2410c"),
        ("MONO BASIC", "램스울 라운드 니트", 69000, 20, 2754, "베스트", "#e7e5e4", "#78716c"),
        ("SOFTSTEP", "스웨이드 첼시 부츠", 159000, 18, 631, "단독", "#d6d3d1", "#44403c"),
    ]

    def product_card(i, p, show_rank):
        brand, name, price, dc, reviews, tag, c1, c2 = p
        now = round(price * (100 - dc) / 100, -2)  # 100원 단위 반올림
        rank = f'<span class="rank">{i}</span>' if show_rank else ""
        price_html = (f'<span class="dc">{dc}%</span><span class="now">{won(int(now))}</span>'
                      f'<span class="orig">{won(price)}</span>') if dc else f'<span class="now">{won(price)}</span>'
        return (f'<a class="item" href="#"><div class="thumb" style="background:linear-gradient(160deg,{c1},{c2})">'
                f'{rank}<span class="tag">{tag}</span><span class="heart">♡</span></div>'
                f'<div class="brand">{brand}</div><div class="name">{name}</div><div>{price_html}</div>'
                f'<div class="meta">★ 4.{(reviews % 5) + 5} · 리뷰 {reviews:,}</div></a>')

    best = sorted(products, key=lambda p: p[4], reverse=True)[:5]  # 리뷰 수 기준 베스트
    sale = sorted([p for p in products if p[3] >= 20], key=lambda p: p[3], reverse=True)[:5]  # 할인율 높은 순
    best_html = "".join(product_card(i, p, True) for i, p in enumerate(best, 1))
    sale_html = "".join(product_card(i, p, False) for i, p in enumerate(sale, 1))
    cat_html = "".join(f'<a href="#"><div class="circle">{e}</div>{n}</a>' for e, n in categories)

    body = f"""
<div class="notice">신규 가입 시 15% 할인 쿠폰 즉시 지급 · 5만 원 이상 구매 시 무료배송</div>
<header><div class="wrap">
  <div class="logo">monomarket</div>
  <form class="search" action="#"><input placeholder="브랜드, 상품명을 검색해 보세요"><button type="button">검색</button></form>
  <div class="util"><a href="#">로그인</a><a href="#">마이페이지</a><a href="#">장바구니 (2)</a></div>
</div></header>
<nav class="cats"><div class="wrap">
  <a href="#">랭킹</a><a href="#">신상품</a><a href="#">여성</a><a href="#">남성</a><a href="#">신발</a>
  <a href="#">가방</a><a href="#">리빙</a><a href="#">브랜드</a><a class="sale" href="#">시즌오프 SALE</a>
</div></nav>

<main class="wrap">
  <div class="banner">
    <a class="bn main" href="#"><small>26 F/W COLLECTION</small><h2>겨울을 준비하는<br>아우터 기획전</h2><span class="more">최대 40% 할인 보러 가기</span></a>
    <a class="bn sub" href="#"><small>오늘만 특가</small><h2>타임세일<br>최대 50%</h2><span class="more">지금 확인하기</span></a>
  </div>

  <div class="circles">{cat_html}</div>

  <div class="sec-head"><div><h3>실시간 랭킹</h3><p>리뷰가 가장 많은 상품</p></div><a href="#">전체 보기 →</a></div>
  <div class="products">{best_html}</div>

  <div class="sec-head"><div><h3>시즌오프 SALE</h3><p>20% 이상 할인 상품만 모았습니다</p></div><a href="#">전체 보기 →</a></div>
  <div class="products">{sale_html}</div>

  <div class="benefits">
    <div class="benefit"><b>🚚 오늘 출발</b><span>오후 2시 전 주문은 당일 발송합니다.</span></div>
    <div class="benefit"><b>↩️ 무료 반품</b><span>받은 날로부터 7일 안에 무료로 반품할 수 있습니다.</span></div>
    <div class="benefit"><b>✅ 정품 보증</b><span>모든 상품은 브랜드 공식 유통 상품입니다.</span></div>
    <div class="benefit"><b>💳 적립금 5%</b><span>구매 확정 후 결제 금액의 5%를 적립합니다.</span></div>
  </div>
</main>

<footer><div class="wrap">
  <b>monomarket</b>
  (주)모노마켓 · 대표 홍길동 · 사업자등록번호 000-00-00000 · 통신판매업 신고 제0000-서울-0000호<br>
  고객센터 1588-0000 (평일 10:00–18:00) · 이용약관 · 개인정보처리방침<br>
  ※ 이 페이지는 템플릿 샘플이며, 회사 정보는 모두 가상의 정보입니다.
</div></footer>
"""
    return page("monomarket — 쇼핑몰 홈 샘플", SHOP_CSS, body)


META = {
    "key": "shop",
    "file": "shop.html",
    "kind": "쇼핑몰",
    "title": "패션·라이프스타일 쇼핑몰",
    "name": "monomarket",
    "desc": "검색창, 카테고리, 기획전 배너, 랭킹·세일 상품 그리드, 혜택 안내",
    "thumb": "linear-gradient(135deg,#111,#525252)",
}
build = build_shop

if __name__ == "__main__":
    import common
    common.SHOW_BACK = False
    sys.stdout.write(build())
