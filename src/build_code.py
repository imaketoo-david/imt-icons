# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icondata import ICONS, PALETTE, CATS, STROKE

ROOT = os.environ.get("IMT_ROOT", os.path.expanduser("~/imt-icons/dist"))
names = sorted(ICONS)
DATA = {n: {"c": ICONS[n]["cat"], "k": ICONS[n]["kw"], "h": ICONS[n]["hue"],
            "o": [[k, d] for k, d in ICONS[n]["ops"]]} for n in names}

# ------------------------------------------------------------------ React
os.makedirs(f"{ROOT}/react", exist_ok=True)
jsx = '''// IMT Icons — React component (v1.0)
// <Icon name="chart-line" size={20} /> · <IconBadge name="chart-line" size={64} />
import React from "react";

export const ICONS = %s;

export const PALETTE = %s;

const GLYPH_RATIO = 0.52;

export function Icon({ name, size = 24, stroke = %s, title, ...rest }) {
  const ic = ICONS[name];
  if (!ic) { console.warn("[IMT Icons] unknown icon:", name); return null; }
  const s = ic.o.filter((o) => o[0] === "s");
  const f = ic.o.filter((o) => o[0] === "f");
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         role={title ? "img" : "presentation"} aria-hidden={title ? undefined : true}
         aria-label={title} {...rest}>
      {title && <title>{title}</title>}
      {s.length > 0 && (
        <g fill="none" stroke="currentColor" strokeWidth={stroke}
           strokeLinecap="round" strokeLinejoin="round">
          {s.map((o, i) => <path key={i} d={o[1]} />)}
        </g>
      )}
      {f.length > 0 && (
        <g fill="currentColor" stroke="none">
          {f.map((o, i) => <path key={i} d={o[1]} />)}
        </g>
      )}
    </svg>
  );
}

const SQ = "%s";

function shade(hex, amt) {
  const n = parseInt(hex.slice(1), 16);
  const ch = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) =>
    Math.max(0, Math.min(255, Math.round(amt > 0 ? v + (255 - v) * amt : v * (1 + amt))))
  );
  return "#" + ch.map((v) => v.toString(16).padStart(2, "0")).join("");
}

export function IconBadge({ name, size = 64, hue, radiusStyle, title, ...rest }) {
  const ic = ICONS[name];
  if (!ic) return null;
  const base = PALETTE[hue || ic.h];
  const sc = (512 * GLYPH_RATIO) / 24;
  const off = (512 - 512 * GLYPH_RATIO) / 2;
  const s = ic.o.filter((o) => o[0] === "s");
  const f = ic.o.filter((o) => o[0] === "f");
  return (
    <svg width={size} height={size} viewBox="0 0 512 512"
         role={title ? "img" : "presentation"} aria-label={title}
         style={radiusStyle} {...rest}>
      <path d={SQ} fill={base} />
      <g transform={`translate(${off} ${off}) scale(${sc})`}>
        {s.length > 0 && (
          <g fill="none" stroke="#fff" strokeWidth={%s}
             strokeLinecap="round" strokeLinejoin="round">
            {s.map((o, i) => <path key={i} d={o[1]} />)}
          </g>
        )}
        {f.length > 0 && <g fill="#fff">{f.map((o, i) => <path key={i} d={o[1]} />)}</g>}
      </g>
    </svg>
  );
}

export const ICON_NAMES = Object.keys(ICONS);
export default Icon;
'''
sq = open(f"{ROOT}/icons/badge/{names[0]}.svg").read()
sq = sq.split('<path d="')[1].split('"')[0]
open(f"{ROOT}/react/IMTIcon.jsx", "w").write(jsx % (
    json.dumps(DATA, ensure_ascii=False, separators=(",", ":")),
    json.dumps(PALETTE, indent=2), STROKE, sq, STROKE))

# ------------------------------------------------------------------ CSS
css = f""":root {{
{chr(10).join(f'  --imt-{k}: {v};' for k, v in PALETTE.items())}
}}
.imt-i {{ width: 1.5rem; height: 1.5rem; display: inline-block; vertical-align: -0.25em; color: inherit; }}
.imt-i--sm {{ width: 1rem;  height: 1rem;  }}
.imt-i--md {{ width: 1.5rem; height: 1.5rem; }}
.imt-i--lg {{ width: 2rem;  height: 2rem;  }}
.imt-i--xl {{ width: 2.75rem; height: 2.75rem; }}
"""
open(f"{ROOT}/imt-icons.css", "w").write(css)

print("react/css OK")
