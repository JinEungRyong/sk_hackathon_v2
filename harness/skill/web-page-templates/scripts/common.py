#!/usr/bin/env python3
"""
모든 페이지 유형이 함께 쓰는 공통 요소 (폰트, 기본 CSS, page(), won())

원래 설명: 웹 페이지 유형별 홈 화면 샘플 생성기

- 사용 기술: Python 3 표준 라이브러리 + HTML/CSS
- JavaScript, 외부 이미지, 외부 폰트, CDN을 사용하지 않습니다.
- 이미지 자리는 CSS 그라데이션으로 대신합니다.
- 상품 가격, 할인율, 카운트다운, 차트 높이처럼 계산이 필요한 값은 파이썬이 계산해서 HTML에 넣습니다.

실행 방법:
    python3 build_templates.py
실행하면 같은 폴더의 templates/ 안에 index.html과 7개 페이지가 만들어집니다.
"""
import datetime
from pathlib import Path

SHOW_BACK = True  # build.py가 여러 페이지를 만들 때만 "전체 템플릿" 링크를 켭니다.
FONT = '-apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif'
SERIF = '"Nanum Myeongjo", "AppleMyungjo", "Batang", Georgia, serif'

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:%s;line-height:1.6;word-break:keep-all;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
ul{list-style:none}
button,input,select,textarea{font:inherit}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.__back{position:fixed;right:16px;bottom:16px;z-index:999;background:#111;color:#fff;
  font-size:13px;padding:8px 14px;border-radius:999px;box-shadow:0 6px 20px rgba(0,0,0,.25)}
""" % FONT


def won(n: int) -> str:
    """숫자를 '12,300원' 형식으로 바꿉니다."""
    return f"{n:,}원"


def page(title: str, css: str, body: str, back: bool = True) -> str:
    back_link = '<a class="__back" href="index.html">← 전체 템플릿</a>' if (back and SHOW_BACK) else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{BASE_CSS}{css}</style>
</head>
<body>
{body}
{back_link}
</body>
</html>"""


