# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icondata import ICONS, PALETTE, CATS, STROKE

ROOT = os.environ.get("IMT_ROOT", os.path.expanduser("~/imt-icons/dist"))
os.makedirs(f"{ROOT}/icons/glyph", exist_ok=True)
os.makedirs(f"{ROOT}/icons/badge", exist_ok=True)

def body(ops, stroke_attr='currentColor', fill_attr='currentColor', sw=STROKE):
    out = []
    s = [d for k, d in ops if k == "s"]
    f = [d for k, d in ops if k == "f"]
    if s:
        out.append(f'<g fill="none" stroke="{stroke_attr}" stroke-width="{sw}" '
                   f'stroke-linecap="round" stroke-linejoin="round">'
                   + "".join(f'<path d="{d}"/>' for d in s) + '</g>')
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
for name, ic in sorted(ICONS.items()):
    # ---- glyph (24x24, currentColor)
    g = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
         f'fill="none" role="img" aria-label="{name}">' + body(ic["ops"]) + '</svg>')
    open(f"{ROOT}/icons/glyph/{name}.svg", "w").write(g)

    # ---- badge (512x512, squircle + white glyph)
    base = PALETTE[ic["hue"]]
    s = 512 * GLYPH_SCALE / 24.0
    off = (512 - 512 * GLYPH_SCALE) / 2.0
    b = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="{name}">'
         f'<path d="{SQ}" fill="{base}"/>'
         f'<g transform="translate({off:.2f} {off:.2f}) scale({s:.5f})">'
         + body(ic["ops"], "#FFFFFF", "#FFFFFF") + '</g></svg>')
    open(f"{ROOT}/icons/badge/{name}.svg", "w").write(b)

    meta.append({"name": name, "cat": ic["cat"], "kw": ic["kw"], "hue": ic["hue"]})

# ---- sprite
sym = []
for name, ic in sorted(ICONS.items()):
    sym.append(f'<symbol id="i-{name}" viewBox="0 0 24 24">{body(ic["ops"])}</symbol>')
sprite = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
          + "".join(sym) + '</svg>')
open(f"{ROOT}/sprite.svg", "w").write(sprite)

json.dump({"icons": meta, "palette": PALETTE, "cats": CATS, "stroke": STROKE},
          open(f"{ROOT}/icons.json", "w"), ensure_ascii=False, indent=1)
print("glyph/badge/sprite OK:", len(meta), "| sprite bytes:", len(sprite))
