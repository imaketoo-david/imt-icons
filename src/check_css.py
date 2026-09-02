# -*- coding: utf-8 -*-
"""catalog.html 의 인라인 CSS를 검사한다.

블록 밖에 떠 있는 선언 하나가 바로 뒤 규칙을 통째로 삼킨다 —
2026-09-02 에 `:root{...}` 를 일찍 닫는 바람에 `.gnav` 가 사라졌고,
브라우저는 오류를 조용히 넘겨서 배포 뒤에야 눈으로 발견했다.
"""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, "catalog.html"), encoding="utf-8").read()
css = s[s.index("<style>") + 7: s.index("</style>")]
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

bad, depth = [], 0
for i, ln in enumerate(css.split("\n"), 1):
    t = ln.strip()
    if depth == 0 and t and "{" not in t and t.endswith(";"):
        bad.append((i, t[:70]))
    depth += ln.count("{") - ln.count("}")

if css.count("{") != css.count("}"):
    print(f"✗ 중괄호 불균형 — 여는 {css.count('{')} · 닫는 {css.count('}')}"); sys.exit(1)
if bad:
    print("✗ 블록 밖에 뜬 선언 — 뒤따르는 규칙이 통째로 무시된다")
    for i, t in bad[:8]: print(f"   {i}행  {t}")
    sys.exit(1)

# 셸 규칙이 실제로 살아 있는지
# .lnav 는 2026-09-03 에 없앴다 — 내비가 한 줄로 합쳐졌다.
# 대신 .gnav__i(섹션 링크)가 살아 있는지 본다: 그게 빠지면 내비가 이름표만 남는다.
need = [".gnav{", ".gnav__i{", ".phead{", ".cols{", ".side{"]
miss = [n for n in need if n not in css.replace(" {", "{")]
if miss:
    print("✗ 셸 규칙 누락:", " ".join(miss)); sys.exit(1)

print(f"✓ CSS 정상 · 규칙 {css.count('{')}개")
