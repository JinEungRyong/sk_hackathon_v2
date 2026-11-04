#!/usr/bin/env python3
"""
웹 페이지 유형별 홈 화면 생성기 (Python 3 표준 라이브러리만 사용)

사용법:
    python3 scripts/build.py --list                 # 사용할 수 있는 유형 보기
    python3 scripts/build.py all --out ./site       # 7개 유형 + index.html 생성
    python3 scripts/build.py shop event --out ./site  # 원하는 유형만 생성

유형을 2개 이상 만들면 index.html(목록 페이지)과 "← 전체 템플릿" 링크를 함께 만듭니다.
"""
import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402
from common import page  # noqa: E402

TYPES = ["landing", "shop", "corporate", "portfolio", "blog", "event", "dashboard"]


# ---------------------------------------------------------------------------
# 목록 페이지 (index.html)
# ---------------------------------------------------------------------------
INDEX_CSS = """
body{background:#f8fafc;color:#0f172a}
header.wrap{padding-top:64px;padding-bottom:40px}
header h1{font-size:34px;letter-spacing:-1px}
header p{color:#64748b;margin-top:8px}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;padding-bottom:80px}
.list a{background:#fff;border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;transition:.2s;display:block}
.list a:hover{transform:translateY(-4px);box-shadow:0 20px 40px -20px rgba(15,23,42,.3)}
.thumb{height:150px;display:flex;align-items:flex-end;padding:18px;color:#fff;font-weight:800;font-size:22px;letter-spacing:-.5px}
.txt{padding:18px 20px 22px}
.txt small{color:#64748b;font-weight:600;font-size:12px}
.txt h2{font-size:18px;margin:2px 0 6px}
.txt p{color:#475569;font-size:14px}
"""


def build_index(metas) -> str:
    cards = "".join(
        f'<a href="{m["file"]}"><div class="thumb" style="background:{m["thumb"]}">{m["name"]}</div>'
        f'<div class="txt"><small>{num:02d} · {m["kind"]}</small><h2>{m["title"]}</h2><p>{m["desc"]}</p></div></a>'
        for num, m in enumerate(metas, 1)
    )
    body = f"""
<header class="wrap"><h1>웹 페이지 유형별 홈 화면 샘플</h1>
<p>HTML과 CSS만으로 만든 홈 화면입니다. 데이터 계산은 파이썬(scripts/build.py)이 맡았습니다.</p></header>
<div class="wrap list">{cards}</div>
"""
    return page("웹 페이지 템플릿 샘플 모음", INDEX_CSS, body, back=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description="웹 페이지 유형별 홈 화면 생성기")
    ap.add_argument("types", nargs="*", default=["all"], help="생성할 유형 (all 또는 " + ", ".join(TYPES) + ")")
    ap.add_argument("--out", default="site", help="결과를 저장할 폴더 (기본값: ./site)")
    ap.add_argument("--list", action="store_true", help="유형 목록만 출력")
    args = ap.parse_args(argv)

    modules = {k: importlib.import_module(f"page_types.{k}") for k in TYPES}
    if args.list:
        for k in TYPES:
            m = modules[k].META
            print(f"{k:10s} {m['kind']:10s} {m['desc']}")
        return

    chosen = TYPES if "all" in args.types else args.types
    unknown = [t for t in chosen if t not in TYPES]
    if unknown:
        ap.error("알 수 없는 유형: " + ", ".join(unknown))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    common.SHOW_BACK = len(chosen) > 1
    for k in chosen:
        path = out / modules[k].META["file"]
        path.write_text(modules[k].build(), encoding="utf-8")
        print("생성:", path)
    if len(chosen) > 1:
        (out / "index.html").write_text(build_index([modules[k].META for k in chosen]), encoding="utf-8")
        print("생성:", out / "index.html")


if __name__ == "__main__":
    main()
