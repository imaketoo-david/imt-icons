# -*- coding: utf-8 -*-
"""파생 축 — 그림을 새로 그리지 않고 기계로 만든다.

  .circle  원 안에 가두기        .square  둥근 사각 안에 가두기
  .slash   빗금(비활성·차단)

원전이 파일을 수천 벌 늘려 해결하는 자리를, 우리는 변환으로 푼다.
스트로크 굵기는 건드리지 않는다 — 안쪽 글리프만 줄이고 획은 1.6 그대로다.
그래야 감싼 것과 안 감싼 것의 획이 같아 나란히 놓아도 어긋나지 않는다.
"""
from svgpathtools import parse_path

RING   = 9.4      # 원 반지름
SQ     = (2.6, 2.6, 18.8, 18.8, 5.6)   # 둥근 사각
INNER  = 0.58     # 안쪽 글리프 축소율
SLASH  = "M4.9 4.9L19.1 19.1"

def _fit(d, k=INNER, cx=12.0, cy=12.0):
    """(12,12) 기준으로 k 배 축소."""
    p = parse_path(d)
    return p.scaled(k).translated(complex(cx * (1 - k), cy * (1 - k))).d()

def _round(d, n=2):
    import re
    return re.sub(r'-?\d+\.\d+', lambda m: f"{float(m.group()):.{n}f}".rstrip('0').rstrip('.'), d)

def derive(ICONS, C, SR):
    """ICONS 를 읽어 파생 항목 dict 를 돌려준다 (원본은 건드리지 않는다)."""
    out = {}
    ring = C(12, 12, RING)
    sq   = SR(*SQ)
    for name, ic in ICONS.items():
        if "." in name:            # 이미 파생된 것은 재파생하지 않는다
            continue
        inner = [["s", _round(_fit(d))] for tag, d in ic["ops"] if tag == "s"]
        if not inner:
            continue
        for suf, shape, kw in (("circle", ring, "원 안 circle"),
                               ("square", sq,   "사각 안 square")):
            out[f"{name}.{suf}"] = {
                "cat": ic["cat"], "hue": ic["hue"],
                "kw": f'{ic["kw"]} {kw}',
                "ops": [["s", shape]] + inner,
            }
        out[f"{name}.slash"] = {
            "cat": ic["cat"], "hue": ic["hue"],
            "kw": f'{ic["kw"]} 없음 끔 차단 slash off disabled',
            "ops": list(ic["ops"]) + [["s", SLASH]],
        }
    return out
