"""
페이지 유형: 블로그·매거진 — 라이프스타일 웹 매거진
구성: 커버 스토리, 최신 글 목록, 인기 글·태그·뉴스레터 사이드바

단독 실행:  python3 scripts/page_types/blog.py > blog.html
전체 생성:  python3 scripts/build.py blog --out ./site
"""
import datetime  # noqa: F401  (날짜 계산에 쓰는 유형이 있습니다)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FONT, SERIF, page, won  # noqa: E402,F401

BLOG_CSS = """
body{color:#222;background:#fbf8f3}
.top{border-bottom:1px solid #e7e0d4;font-size:13px;color:#888}
.top .wrap{display:flex;justify-content:space-between;height:40px;align-items:center}
.mast{text-align:center;padding-top:40px;padding-bottom:28px}
.mast h1{font-family:SERIF_FONT;font-size:clamp(40px,7vw,72px);letter-spacing:-2px;line-height:1}
.mast p{color:#8a7f6e;margin-top:10px;font-size:15px}
.catnav{border-top:2px solid #222;border-bottom:1px solid #222}
.catnav .wrap{display:flex;justify-content:center;gap:32px;height:48px;align-items:center;font-size:15px;font-weight:600;overflow-x:auto;white-space:nowrap}
.layout{display:grid;grid-template-columns:1fr 300px;gap:56px;padding-top:48px;padding-bottom:48px}
.featured{display:grid;grid-template-columns:1.2fr 1fr;gap:28px;padding-bottom:40px;border-bottom:1px solid #e7e0d4;margin-bottom:40px}
.featured .img{aspect-ratio:4/3;border-radius:4px}
.kicker{color:#b45309;font-size:13px;font-weight:700;letter-spacing:.5px}
.featured h2{font-family:SERIF_FONT;font-size:34px;line-height:1.3;letter-spacing:-1px;margin:10px 0 14px}
.featured p{color:#555}
.byline{font-size:13px;color:#999;margin-top:16px}
.posts{display:grid;grid-template-columns:repeat(2,1fr);gap:36px 28px}
.post .img{aspect-ratio:16/10;border-radius:4px;margin-bottom:14px}
.post h3{font-family:SERIF_FONT;font-size:21px;line-height:1.4;letter-spacing:-.5px;margin:6px 0 8px}
.post p{color:#666;font-size:15px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
aside .box{margin-bottom:40px}
aside h4{font-size:14px;letter-spacing:1px;border-bottom:2px solid #222;padding-bottom:8px;margin-bottom:12px}
.popular li{display:flex;gap:14px;padding:10px 0;border-bottom:1px solid #e7e0d4;font-size:15px}
.popular b{font-family:SERIF_FONT;font-size:22px;color:#b45309;line-height:1.1;min-width:20px}
.tags{display:flex;flex-wrap:wrap;gap:8px}
.tags a{border:1px solid #d6cdbd;border-radius:999px;padding:4px 12px;font-size:13px;color:#555}
.news{background:#222;color:#fbf8f3;padding:24px;border-radius:4px}
.news h4{border-color:#fbf8f3}
.news p{font-size:14px;opacity:.8;margin-bottom:14px}
.news input{width:100%;padding:10px 12px;border:0;border-radius:3px;margin-bottom:8px}
.news button{width:100%;padding:10px;border:0;background:#f59e0b;color:#222;font-weight:700;border-radius:3px;cursor:pointer}
footer{border-top:1px solid #e7e0d4;text-align:center;padding:32px 0;font-size:13px;color:#999}
@media(max-width:900px){.layout{grid-template-columns:1fr}.featured{grid-template-columns:1fr}}
@media(max-width:600px){.posts{grid-template-columns:1fr}}
""".replace("SERIF_FONT", SERIF)


def build_blog() -> str:
    today = datetime.date.today()
    posts = [
        ("에세이", "아침 10분 산책이 바꾼 것들", "거창한 결심 대신 작은 습관 하나를 1년 동안 지켜 본 기록입니다.", "#d9c7a7", "#8a6d3b", 4),
        ("일하는 법", "회의를 절반으로 줄인 팀의 규칙 다섯 가지", "회의 전에 문서를 먼저 쓰는 팀은 무엇이 달라졌을까요?", "#c7d2c0", "#4d6b45", 7),
        ("여행", "늦가을 경주에서 걷기 좋은 길", "관광지를 조금 벗어나면 조용한 골목과 오래된 나무가 기다립니다.", "#e8b89a", "#9a3412", 5),
        ("책", "올해 다시 읽은 고전 세 권", "학생 때와 지금, 같은 문장이 다르게 읽히는 이유를 생각해 봅니다.", "#b9c4d6", "#334e7a", 6),
    ]
    # 글 목록 날짜는 오늘을 기준으로 파이썬이 계산
    post_html = ""
    for i, (cat, title, desc, c1, c2, mins) in enumerate(posts, 1):
        d = today - datetime.timedelta(days=i * 3)
        post_html += (f'<a class="post" href="#"><div class="img" style="background:linear-gradient(135deg,{c1},{c2})"></div>'
                      f'<span class="kicker">{cat}</span><h3>{title}</h3><p>{desc}</p>'
                      f'<div class="byline">{d:%Y.%m.%d} · {mins}분 읽기</div></a>')
    popular = ["퇴근 후 1시간을 지키는 방법", "작은 집을 넓게 쓰는 수납 원칙", "혼자 떠나는 첫 해외여행 준비물", "읽기 쉬운 글은 문장이 짧다"]
    pop_html = "".join(f"<li><b>{i}</b><a href='#'>{t}</a></li>" for i, t in enumerate(popular, 1))
    tags = ["습관", "독서", "글쓰기", "국내여행", "생산성", "인테리어", "요리", "마음챙김"]
    tag_html = "".join(f"<a href='#'>#{t}</a>" for t in tags)

    body = f"""
<div class="top"><div class="wrap"><span>{today:%Y년 %m월 %d일}</span><span>로그인 · 구독하기</span></div></div>
<div class="mast wrap"><h1>주간 생각</h1><p>일상과 일, 여행과 책에 관한 느린 이야기</p></div>
<nav class="catnav"><div class="wrap"><a href="#">전체</a><a href="#">에세이</a><a href="#">일하는 법</a><a href="#">여행</a><a href="#">책</a><a href="#">인터뷰</a></div></nav>

<div class="wrap layout">
  <main>
    <article class="featured">
      <div class="img" style="background:linear-gradient(150deg,#f3d9b1,#b45309 70%,#78350f)"></div>
      <div>
        <span class="kicker">이번 주 커버 스토리</span>
        <h2>기록하는 사람은 왜 덜 불안할까</h2>
        <p>하루를 세 줄로 적는 습관을 가진 사람 열 명을 만났습니다. 그들은 기록이 생각을 정리하는 가장 쉬운 방법이라고 말했습니다.</p>
        <div class="byline">글 정다은 · {today:%Y.%m.%d} · 9분 읽기</div>
      </div>
    </article>
    <div class="posts">{post_html}</div>
  </main>
  <aside>
    <div class="box popular"><h4>많이 읽은 글</h4><ul>{pop_html}</ul></div>
    <div class="box"><h4>태그</h4><div class="tags">{tag_html}</div></div>
    <div class="box news"><h4>뉴스레터</h4><p>매주 금요일 아침, 새 글을 메일로 보내 드립니다.</p>
      <form action="#"><input type="email" placeholder="이메일 주소"><button type="button">구독하기</button></form></div>
  </aside>
</div>
<footer>© {today.year} 주간 생각 · 이 페이지의 글과 필자는 모두 가상의 예시입니다.</footer>
"""
    return page("주간 생각 — 블로그·매거진 홈 샘플", BLOG_CSS, body)


META = {
    "key": "blog",
    "file": "blog.html",
    "kind": "블로그·매거진",
    "title": "라이프스타일 웹 매거진",
    "name": "주간 생각",
    "desc": "커버 스토리, 최신 글 목록, 인기 글·태그·뉴스레터 사이드바",
    "thumb": "linear-gradient(135deg,#78350f,#d9c7a7)",
}
build = build_blog

if __name__ == "__main__":
    import common
    common.SHOW_BACK = False
    sys.stdout.write(build())
