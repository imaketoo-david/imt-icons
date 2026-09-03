# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icondata import ICONS, PALETTE, CATS, STROKE, C, SR
from derive import derive

# 파생 3축(.circle .square .slash) — 그림이 아니라 변환으로 만든다.
DER = derive(ICONS, C, SR)

ROOT = os.environ.get("IMT_ROOT", os.path.expanduser("~/imt-icons/dist"))
os.makedirs(f"{ROOT}/icons/glyph", exist_ok=True)
os.makedirs(f"{ROOT}/icons/badge", exist_ok=True)

def body(ops, stroke_attr='currentColor', fill_attr='currentColor', sw=STROKE,
         inherit=False):
    """inherit=True 면 획 속성을 심볼에 박지 않고 바깥 CSS 에서 상속받게 둔다.

    <use> 로 꺼내 쓰는 스프라이트 전용이다. 그림자 DOM 은 바깥 CSS '선택자'
    가 못 넘어가지만 '상속되는 속성'은 넘어간다 — 그래서 <g> 에 박힌
    표현 속성을 빼야 .imt-i 의 stroke-width 가 안까지 닿는다.
    이 한 가지로 334개 전부가 굵기 축을 갖는다(애플은 9벌을 그려야 한다).

    단독 파일(icons/glyph/*.svg)은 우리 CSS 없이도 그대로 보여야 하므로
    inherit=False 로 속성을 박아 둔다.
    """
    out = []
    s = [d for k, d in ops if k == "s"]
    f = [d for k, d in ops if k == "f"]
    if s:
        attrs = f'fill="none" stroke="{stroke_attr}"'
        if not inherit:
            attrs += f' stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
        out.append(f'<g {attrs}>' + "".join(f'<path d="{d}"/>' for d in s) + '</g>')
    if f:
        out.append(f'<g fill="{fill_attr}" stroke="none">'
                   + "".join(f'<path d="{d}"/>' for d in f) + '</g>')
    return "".join(out)

def lighten(hexc, amt):
    r, g, b = (int(hexc[i:i+2], 16) for i in (1, 3, 5))
    f = lambda v: max(0, min(255, round(v + (255 - v) * amt if amt > 0 else v * (1 + amt))))
    return "#%02X%02X%02X" % (f(r), f(g), f(b))

def squircle(size=512, n=5.0, steps=180):
    """Superellipse |x|^n + |y|^n = 1 -> continuous-corner squircle."""
    import math
    a = size / 2.0
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        ct, st = math.cos(t), math.sin(t)
        x = a * (abs(ct) ** (2.0 / n)) * (1 if ct >= 0 else -1)
        y = a * (abs(st) ** (2.0 / n)) * (1 if st >= 0 else -1)
        pts.append((a + x, a + y))
    return "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"

SQ = squircle()
GLYPH_SCALE = 0.52

meta = []
# 낱개 글리프는 파생분까지 전부 내보낸다(가져다 쓰는 사람이 파일 하나만 받으면 되게).
# 앱 배지는 원본만 만든다 — 감싼 아이콘을 다시 사각 배지에 넣을 일이 없다.
for name, ic in sorted({**ICONS, **DER}.items()):
    # ---- glyph (24x24, currentColor)
    g = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
         f'fill="none" role="img" aria-label="{name}">' + body(ic["ops"]) + '</svg>')
    open(f"{ROOT}/icons/glyph/{name}.svg", "w").write(g)

    meta.append({"name": name, "cat": ic["cat"], "kw": ic["kw"], "hue": ic["hue"],
                 "base": "." not in name})
    if "." in name:
        continue

    # ---- badge (512x512, squircle + white glyph)
    base = PALETTE[ic["hue"]]
    s = 512 * GLYPH_SCALE / 24.0
    off = (512 - 512 * GLYPH_SCALE) / 2.0
    b = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="{name}">'
         f'<path d="{SQ}" fill="{base}"/>'
         f'<g transform="translate({off:.2f} {off:.2f}) scale({s:.5f})">'
         + body(ic["ops"], "#FFFFFF", "#FFFFFF") + '</g></svg>')
    open(f"{ROOT}/icons/badge/{name}.svg", "w").write(b)

# ---- 스프라이트는 둘로 나눈다.
#      한 파일에 1,333개를 담으면 330KB 가 되어 원본만 쓰는 화면까지 벌을 받는다.
#      sprite.svg = 원본 334 (기본 로드) · sprite-derived.svg = 파생 999 (필요할 때만)
def make_sprite(d):
    sym = [f'<symbol id="i-{n}" viewBox="0 0 24 24">{body(i["ops"], inherit=True)}</symbol>'
           for n, i in sorted(d.items())]
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
            + "".join(sym) + '</svg>')

sprite = make_sprite(ICONS)
open(f"{ROOT}/sprite.svg", "w").write(sprite)
sprite_d = make_sprite(DER)
open(f"{ROOT}/sprite-derived.svg", "w").write(sprite_d)

json.dump({"icons": meta, "palette": PALETTE, "cats": CATS, "stroke": STROKE,
           "count": {"base": len(ICONS), "derived": len(DER), "total": len(meta)}},
          open(f"{ROOT}/icons.json", "w"), ensure_ascii=False, indent=1)
# 카탈로그가 «파생 포함» 을 켤 때만 받아가는 데이터
json.dump({n: {"c": i["cat"], "k": i["kw"], "h": i["hue"],
               "o": [[k, d] for k, d in i["ops"]]} for n, i in sorted(DER.items())},
          open(f"{ROOT}/icons-derived.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(f"glyph {len(meta)} (원본 {len(ICONS)} + 파생 {len(DER)}) | "
      f"sprite {len(sprite)}B · 파생 {len(sprite_d)}B")
