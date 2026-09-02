# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icondata import ICONS, PALETTE, CATS, STROKE

ROOT = os.environ.get("IMT_ROOT", os.path.expanduser("~/imt-icons/dist"))
names = sorted(ICONS)
sprite = open(f"{ROOT}/sprite.svg").read()
sq = open(f"{ROOT}/icons/badge/{names[0]}.svg").read().split('<path d="')[1].split('"')[0]
DATA = {n: {"c": ICONS[n]["cat"], "k": ICONS[n]["kw"], "h": ICONS[n]["hue"],
            "o": [[k, d] for k, d in ICONS[n]["ops"]]} for n in names}

HTML = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IMT Icons</title>
<style>
:root{
  --bg:#F5F5F7; --card:#FFFFFF; --ink:#1D1D1F; --sub:#6E6E73; --line:#E3E3E6;
  --accent:#2F6BFF; --shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.06);
__PAL__
}
@media (prefers-color-scheme:dark){
  :root{--bg:#000000;--card:#1C1C1E;--ink:#F5F5F7;--sub:#8E8E93;--line:#2C2C2E;
        --shadow:0 1px 2px rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.4)}
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:400 15px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text","Pretendard","Apple SD Gothic Neo",system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px 96px}
header{padding:64px 0 28px;text-align:center}
h1{margin:0 0 8px;font-size:44px;line-height:1.08;letter-spacing:-.022em;font-weight:600}
.lede{margin:0;color:var(--sub);font-size:17px;letter-spacing:-.01em}
.bar{position:sticky;top:0;z-index:20;padding:14px 0 12px;background:color-mix(in srgb,var(--bg) 82%, transparent);
 backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px)}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.search{flex:1 1 280px;display:flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--line);
 border-radius:12px;padding:0 14px;height:42px;box-shadow:var(--shadow)}
.search input{flex:1;border:0;outline:0;background:transparent;color:inherit;font:inherit;height:100%}
.search svg{width:17px;height:17px;color:var(--sub);flex:none}
.seg{display:flex;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:3px;box-shadow:var(--shadow)}
.seg button{border:0;background:transparent;color:var(--sub);font:inherit;font-size:13px;font-weight:500;
 padding:7px 14px;border-radius:9px;cursor:pointer;letter-spacing:-.01em}
.seg button[aria-pressed=true]{background:var(--accent);color:#fff}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0 0;max-height:96px;overflow-y:auto}
.chip{border:1px solid var(--line);background:var(--card);color:var(--sub);border-radius:999px;
 padding:5px 11px;font-size:12.5px;font-weight:500;cursor:pointer;letter-spacing:-.01em;white-space:nowrap}
.chip[aria-pressed=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.count{color:var(--sub);font-size:13px;margin:20px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:10px}
.cell{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 8px 11px;text-align:center;
 cursor:pointer;transition:transform .15s cubic-bezier(.4,0,.2,1),box-shadow .15s;position:relative}
.cell:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.cell:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.cell .g{height:44px;display:grid;place-items:center;color:var(--ink)}
.cell .g svg{width:28px;height:28px}
.cell.badge .g svg{width:44px;height:44px}
.cell .n{margin-top:9px;font-size:11px;color:var(--sub);word-break:break-all;letter-spacing:-.005em}
.toast{position:fixed;left:50%;bottom:32px;transform:translate(-50%,20px);opacity:0;pointer-events:none;
 background:var(--ink);color:var(--bg);padding:11px 20px;border-radius:12px;font-size:13.5px;font-weight:500;
 transition:.22s cubic-bezier(.4,0,.2,1);z-index:50;max-width:80vw;text-align:center}
.toast.on{opacity:1;transform:translate(-50%,0)}
dialog{border:0;border-radius:20px;padding:0;background:var(--card);color:var(--ink);box-shadow:var(--shadow);
 max-width:440px;width:calc(100% - 40px)}
dialog::backdrop{background:rgba(0,0,0,.36);backdrop-filter:blur(3px)}
.dlg{padding:26px}
.dlg h3{margin:0 0 2px;font-size:20px;letter-spacing:-.015em}
.dlg .cat{color:var(--sub);font-size:13px;margin:0 0 18px}
.prev{display:flex;gap:14px;align-items:center;justify-content:center;padding:20px;background:var(--bg);border-radius:14px;margin-bottom:18px}
.prev svg{color:var(--ink)}
.copy{display:grid;gap:8px}
.copy button{text-align:left;border:1px solid var(--line);background:transparent;color:inherit;font:inherit;font-size:13.5px;
 padding:11px 14px;border-radius:11px;cursor:pointer;display:flex;justify-content:space-between;gap:10px;align-items:center}
.copy button:hover{border-color:var(--accent);color:var(--accent)}
.copy button span{color:var(--sub);font-size:11.5px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.close{position:absolute;top:16px;right:18px;border:0;background:transparent;color:var(--sub);font-size:22px;cursor:pointer;line-height:1}
footer{color:var(--sub);font-size:12.5px;text-align:center;margin-top:52px;line-height:1.8}
</style></head><body>
<div class="wrap">
<header><h1>IMT Icons</h1>
<p class="lede">__N__종 · 24 그리드 · 스트로크 __SW__ · 아이콘을 눌러 복사하세요</p></header>

<div class="bar">
 <div class="row">
  <label class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="10.6" cy="10.6" r="6.6"/><path d="M15.4 15.4L20 20"/></svg>
   <input id="q" type="search" placeholder="이름 · 한글 키워드로 검색 (예: 차트, 알림, chart)" autocomplete="off"></label>
  <div class="seg"><button id="mGlyph" aria-pressed="true">글리프</button><button id="mBadge" aria-pressed="false">배지</button></div>
 </div>
 <div class="chips" id="chips"></div>
</div>

<p class="count" id="count"></p>
<div class="grid" id="grid"></div>

<footer>IMT Icons v1.0 · imaketoo icon system<br>새 아이콘은 <code>src/icondata.py</code> 에 추가 후 빌드 스크립트를 다시 실행하세요.</footer>
</div>

<dialog id="dlg"><button class="close" onclick="dlg.close()">&times;</button><div class="dlg">
 <h3 id="dName"></h3><p class="cat" id="dCat"></p>
 <div class="prev" id="dPrev"></div>
 <div class="copy" id="dCopy"></div>
</div></dialog>

<div class="toast" id="toast"></div>

<script>
const DATA = __DATA__, CATS = __CATS__, PALETTE = __PALETTE__, SW = __SW__;
const SQ = "__SQ__", RATIO = 0.52;
const names = Object.keys(DATA).sort();
let mode = "glyph", cat = "all";

function glyphSVG(n, size){
  const o = DATA[n].o, s = o.filter(x=>x[0]==="s"), f = o.filter(x=>x[0]==="f");
  return `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" aria-hidden="true">`
   + (s.length?`<g fill="none" stroke="currentColor" stroke-width="${SW}" stroke-linecap="round" stroke-linejoin="round">${s.map(x=>`<path d="${x[1]}"/>`).join("")}</g>`:"")
   + (f.length?`<g fill="currentColor">${f.map(x=>`<path d="${x[1]}"/>`).join("")}</g>`:"") + `</svg>`;
}
function shade(hex,a){const n=parseInt(hex.slice(1),16);
 const c=[(n>>16)&255,(n>>8)&255,n&255].map(v=>Math.max(0,Math.min(255,Math.round(a>0?v+(255-v)*a:v*(1+a)))));
 return "#"+c.map(v=>v.toString(16).padStart(2,"0")).join("")}
function badgeSVG(n,size){
  const ic=DATA[n], base=PALETTE[ic.h];
  const s=ic.o.filter(x=>x[0]==="s"), f=ic.o.filter(x=>x[0]==="f");
  const sc=(512*RATIO)/24, off=(512-512*RATIO)/2;
  return `<svg viewBox="0 0 512 512" width="${size}" height="${size}" aria-hidden="true">`
  +`<path d="${SQ}" fill="${base}"/><g transform="translate(${off} ${off}) scale(${sc})">`
  +(s.length?`<g fill="none" stroke="#fff" stroke-width="${SW}" stroke-linecap="round" stroke-linejoin="round">${s.map(x=>`<path d="${x[1]}"/>`).join("")}</g>`:"")
  +(f.length?`<g fill="#fff">${f.map(x=>`<path d="${x[1]}"/>`).join("")}</g>`:"")+`</g></svg>`;
}

const chips=document.getElementById("chips");
chips.innerHTML = `<button class="chip" data-c="all" aria-pressed="true">전체</button>`
 + Object.entries(CATS).map(([k,v])=>`<button class="chip" data-c="${k}" aria-pressed="false">${v}</button>`).join("");
chips.onclick=e=>{const b=e.target.closest(".chip"); if(!b)return;
 cat=b.dataset.c; [...chips.children].forEach(c=>c.setAttribute("aria-pressed", c===b));
 render()};

const q=document.getElementById("q"); q.oninput=render;
mGlyph.onclick=()=>{mode="glyph";mGlyph.setAttribute("aria-pressed","true");mBadge.setAttribute("aria-pressed","false");render()};
mBadge.onclick=()=>{mode="badge";mBadge.setAttribute("aria-pressed","true");mGlyph.setAttribute("aria-pressed","false");render()};

function render(){
  const t=q.value.trim().toLowerCase();
  const list=names.filter(n=>(cat==="all"||DATA[n].c===cat) && (!t || n.includes(t) || DATA[n].k.toLowerCase().includes(t) || (CATS[DATA[n].c]||"").toLowerCase().includes(t)));
  document.getElementById("count").textContent = `${list.length}개`;
  grid.innerHTML = list.map(n=>`<button class="cell ${mode}" data-n="${n}"><div class="g">${
    mode==="glyph"?glyphSVG(n,28):badgeSVG(n,44)}</div><div class="n">${n}</div></button>`).join("");
}
grid.onclick=e=>{const c=e.target.closest(".cell"); if(c) open_(c.dataset.n)};

function toastMsg(m){toast.textContent=m;toast.classList.add("on");clearTimeout(toast._t);toast._t=setTimeout(()=>toast.classList.remove("on"),1500)}
function cp(text,label){navigator.clipboard.writeText(text).then(()=>toastMsg(label+" 복사됨"))}

function open_(n){
  dName.textContent=n; dCat.textContent=CATS[DATA[n].c]+" · "+DATA[n].k;
  dPrev.innerHTML=glyphSVG(n,20)+glyphSVG(n,28)+glyphSVG(n,40)+badgeSVG(n,56);
  const items=[
    ["이름", n, n],
    ["스프라이트", `<svg class="imt-i"><use href="#i-${n}"/></svg>`, "&lt;use href=\\"#i-"+n+"\\"&gt;"],
    ["React", `<Icon name="${n}" size={20} />`, "&lt;Icon name=…&gt;"],
    ["웹폰트", `<i class="imt imt-${n}"></i>`, "class=\\"imt imt-"+n+"\\""],
    ["SVG 원본", glyphSVG(n,24).replace(' aria-hidden="true"',' xmlns="http://www.w3.org/2000/svg"'), "inline svg"],
  ];
  dCopy.innerHTML=items.map((it,i)=>`<button data-i="${i}">${it[0]}<span>${it[2]}</span></button>`).join("");
  dCopy.onclick=e=>{const b=e.target.closest("button"); if(!b)return; const it=items[+b.dataset.i]; cp(it[1],it[0])};
  dlg.showModal();
}
render();
</script></body></html>
"""

pal = "\n".join(f"  --imt-{k}:{v};" for k, v in PALETTE.items())
out = (HTML.replace("__PAL__", pal)
           .replace("__N__", str(len(names)))
           .replace("__SW__", str(STROKE))
           .replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
           .replace("__CATS__", json.dumps(CATS, ensure_ascii=False))
           .replace("__PALETTE__", json.dumps(PALETTE))
           .replace("__SQ__", sq))
open(f"{ROOT}/catalog.html", "w").write(out)
print("catalog OK", len(out), "bytes")
