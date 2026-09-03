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
/* ── IMT Icons — 굵기·크기 두 축 ──────────────────────────────
   애플 심볼은 굵기 9단을 만들려고 9벌을 그린다. 우리 아이콘은 '획' 이라
   경로 하나에 stroke-width 만 바꾸면 된다 — 334개 전부가 공짜로 9단을 갖는다.
   이게 애플 규격을 우리 방식으로 다시 만든 지점이다.

     --imt-w  굵기 (24 격자 단위). 옆 글자 굵기에 맞춘다.
     --imt-s  크기 (em 배수). 애플의 small / medium / large 에 대응.

   크기를 키워도 획은 굵어지지 않는다 — stroke-width 를 배율로 나눠
   화면상 굵기를 고정한다. 애플이 "크기를 바꿔도 글자와의 굵기 짝은
   유지된다" 고 규정한 동작을 그대로 구현한 것이다. */
.imt-i{{
  --imt-w:1.6; --imt-s:1;
  width:calc(1em * var(--imt-s)); height:calc(1em * var(--imt-s));
  display:inline-block; vertical-align:-.14em; flex:none;
  fill:none; stroke:currentColor;
  stroke-width:calc(var(--imt-w) / var(--imt-s));
  stroke-linecap:round; stroke-linejoin:round;
}}
/* 굵기 9단 — San Francisco 굵기와 짝을 이룬다.
   우리 타이포는 400·500·600 셋만 쓰므로 실제로 쓰는 것도 그 셋이다. */
.imt-i--ultralight{{--imt-w:.7}}  .imt-i--thin{{--imt-w:.9}}   .imt-i--light{{--imt-w:1.2}}
.imt-i--regular{{--imt-w:1.6}}    .imt-i--medium{{--imt-w:1.9}} .imt-i--semibold{{--imt-w:2.2}}
.imt-i--bold{{--imt-w:2.6}}       .imt-i--heavy{{--imt-w:3}}    .imt-i--black{{--imt-w:3.4}}
/* 크기 3단 — 애플은 cap height 를 기준으로 잡는다 */
.imt-i--scale-s{{--imt-s:.87}}  .imt-i--scale-m{{--imt-s:1}}  .imt-i--scale-l{{--imt-s:1.13}}

/* ── 크기별 광학 보정 (2026-09-03) ────────────────────────────
   획을 크기에 정비례로 키우면 큰 아이콘이 «굵어» 보인다. 24px 에서 1.6 인
   획은 48px 에서 3.2px 이 되는데, 눈은 그걸 더 굵다고 읽는다.
   그래서 커질수록 --imt-w 를 낮춰 화면상 굵기가 완만하게 자라게 한다.
     16px→1.15 · 24→1.60 · 32→1.95 · 40→2.25 · 48→2.50 · 64→3.00
   L-9.4 «크기는 강조를 조절하는 축이지 굵기를 바꾸는 축이 아니다» 를
   계산이 아니라 «눈» 기준으로 지키는 장치다. */
.imt-i--px16 {{ --imt-w:1.73; width:16px;  height:16px  }}
.imt-i--px20 {{ --imt-w:1.62; width:20px;  height:20px  }}
.imt-i--px24 {{ --imt-w:1.6;  width:24px;  height:24px  }}
.imt-i--px32 {{ --imt-w:1.46; width:32px;  height:32px  }}
.imt-i--px40 {{ --imt-w:1.35; width:40px;  height:40px  }}
.imt-i--px48 {{ --imt-w:1.25; width:48px;  height:48px  }}
.imt-i--px64 {{ --imt-w:1.13; width:64px;  height:64px  }}

/* 예전 이름 — rem 고정 크기. 광학 보정을 같이 걸어 둔다. */
.imt-i--sm {{ width: 1rem;   height: 1rem;   --imt-w:1.73 }}
.imt-i--md {{ width: 1.5rem; height: 1.5rem; --imt-w:1.6  }}
.imt-i--lg {{ width: 2rem;   height: 2rem;   --imt-w:1.46 }}
.imt-i--xl {{ width: 2.75rem; height: 2.75rem; --imt-w:1.3 }}
"""
open(f"{ROOT}/imt-icons.css", "w").write(css)

print("react/css OK")
