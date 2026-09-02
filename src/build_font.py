# -*- coding: utf-8 -*-
"""스트로크 아이콘 -> 아웃라인 폴리곤 -> TTF/WOFF2 아이콘 폰트."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icondata import ICONS, STROKE
from svgpathtools import parse_path
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import unary_union
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT = os.environ.get("IMT_ROOT", os.path.expanduser("~/imt-icons/dist"))
UPM, GRID = 1000, 24.0
SC = UPM / GRID

def sample(seg, n):
    return [(c.real, c.imag) for c in (seg.point(i / n) for i in range(n + 1))]

def subpath_points(sub):
    pts = []
    for seg in sub:
        L = max(seg.length(error=1e-3), 0.01)
        n = max(3, min(60, int(L * 6)))
        p = sample(seg, n)
        pts.extend(p if not pts else p[1:])
    return pts

def geoms(d, kind):
    path = parse_path(d)
    out = []
    for sub in path.continuous_subpaths():
        pts = subpath_points(sub)
        if len(pts) < 3:
            continue
        if kind == "f":
            g = Polygon(pts)
            if not g.is_valid:
                g = g.buffer(0)
            out.append(g)
        else:
            closed = abs(sub.start - sub.end) < 1e-6
            if closed and pts[0] != pts[-1]:
                pts.append(pts[0])
            out.append(LineString(pts).buffer(STROKE / 2.0, cap_style=1,
                                              join_style=1, resolution=10))
    return out

def polys(name):
    gs = []
    for kind, d in ICONS[name]["ops"]:
        gs.extend(geoms(d, kind))
    u = unary_union(gs)
    return list(u.geoms) if isinstance(u, MultiPolygon) else [u]

def simplify_ring(coords, tol=0.35):
    from shapely.geometry import LinearRing
    r = LinearRing(coords).simplify(tol / SC, preserve_topology=True)
    return list(r.coords)

names = sorted(ICONS)
START = 0xE900
cmap, glyphs, order = {}, {}, [".notdef"]
pen0 = TTGlyphPen(None); glyphs[".notdef"] = pen0.glyph()

for i, n in enumerate(names):
    cp = START + i
    gname = "imt-" + n
    pen = TTGlyphPen(None)
    for poly in polys(n):
        rings = [poly.exterior] + list(poly.interiors)
        for ring in rings:
            cs = simplify_ring(list(ring.coords))
            pen.moveTo((round(cs[0][0] * SC), round((GRID - cs[0][1]) * SC)))
            for x, y in cs[1:-1]:
                pen.lineTo((round(x * SC), round((GRID - y) * SC)))
            pen.closePath()
    glyphs[gname] = pen.glyph()
    cmap[cp] = gname
    order.append(gname)

fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder(order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
metrics = {g: (UPM, 0) for g in order}
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=UPM, descent=0)
fb.setupNameTable({"familyName": "IMT Icons", "styleName": "Regular",
                   "psName": "IMTIcons-Regular", "version": "1.0",
                   "copyright": "imaketoo icon system"})
fb.setupOS2(sTypoAscender=UPM, sTypoDescender=0, usWinAscent=UPM, usWinDescent=0)
fb.setupPost()
os.makedirs(f"{ROOT}/font", exist_ok=True)
fb.save(f"{ROOT}/font/imt-icons.ttf")

from fontTools.ttLib import TTFont
f = TTFont(f"{ROOT}/font/imt-icons.ttf"); f.flavor = "woff2"
f.save(f"{ROOT}/font/imt-icons.woff2")

css = ["""@font-face{font-family:"IMT Icons";src:url("imt-icons.woff2") format("woff2"),url("imt-icons.ttf") format("truetype");font-weight:400;font-style:normal;font-display:block}
.imt{font-family:"IMT Icons";font-weight:400;font-style:normal;line-height:1;speak:never;-webkit-font-smoothing:antialiased;display:inline-block;vertical-align:-0.125em}"""]
for i, n in enumerate(names):
    css.append(f'.imt-{n}::before{{content:"\\{START+i:x}"}}')
open(f"{ROOT}/font/imt-icons.css", "w").write("\n".join(css))
json.dump({n: f"U+{START+i:04X}" for i, n in enumerate(names)},
          open(f"{ROOT}/font/codepoints.json", "w"), indent=1)
print("font OK:", len(names), "glyphs |",
      os.path.getsize(f"{ROOT}/font/imt-icons.woff2"), "bytes woff2")
