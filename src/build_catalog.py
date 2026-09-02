# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icondata import ICONS, PALETTE, CATS, STROKE

ROOT = os.environ.get("IMT_ROOT", os.path.expanduser("~/imt-icons/dist"))

# 디자인 시스템과 값을 공유한다 — 두 사이트가 따로 놀지 않게.
# imt-design 이 옆에 없으면(단독 배포) 예전 자체 값으로 떨어진다.
_TOK = os.path.join(os.path.dirname(ROOT), "imt-design", "tokens.css")
if not os.path.exists(_TOK):
    _TOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "..", "imt-design", "tokens.css")
TOKENS = open(_TOK, encoding="utf-8").read() if os.path.exists(_TOK) else ""
names = sorted(ICONS)
sprite = open(f"{ROOT}/sprite.svg").read()
sq = open(f"{ROOT}/icons/badge/{names[0]}.svg").read().split('<path d="')[1].split('"')[0]
DATA = {n: {"c": ICONS[n]["cat"], "k": ICONS[n]["kw"], "h": ICONS[n]["hue"],
            "o": [[k, d] for k, d in ICONS[n]["ops"]]} for n in names}

HTML = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#1d1d1f">
<title>IMT Icons</title>
<style>
__TOKENS__
/* 카탈로그 전용 별칭 — 예전 이름을 토큰에 연결한다 */
:root{
  --accent:var(--brand); --shadow:var(--sh);
__PAL__
}

/* ── 사이트 셸 — design.imaketoo.com 과 **같은 한 줄 내비** (2026-09-03) ──
   전에는 검은 띠 + 흰 띠 두 줄이었다. 값은 design 쪽 site.css 의 .gnav 와
   같게 유지한다 — 두 사이트가 한 도메인이 된 이상 상단바가 갈라지면 안 된다. */
.gnav{position:sticky;top:0;z-index:var(--z-nav);height:52px;
 display:flex;align-items:center;gap:var(--sp-6);padding:0 var(--sp-6);
 background:var(--mat);backdrop-filter:var(--mat-blur);-webkit-backdrop-filter:var(--mat-blur);
 border-bottom:var(--hairline) solid var(--line);font-size:var(--fs-md)}
.gnav__b{display:flex;align-items:center;gap:var(--sp-2);color:var(--ink);text-decoration:none;
 font-weight:var(--fw-sb);font-size:var(--fs-base);letter-spacing:var(--tr-xl);white-space:nowrap}
.gnav__b svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;
 stroke-linecap:round;stroke-linejoin:round}
.gnav__i{display:flex;gap:var(--sp-5);overflow-x:auto;scrollbar-width:none}
.gnav__i::-webkit-scrollbar{display:none}
.gnav__i a{position:relative;display:inline-flex;align-items:center;height:52px;
 color:var(--sub);text-decoration:none;white-space:nowrap}
.gnav__i a:hover{color:var(--ink)}
.gnav__i a.on{color:var(--ink);font-weight:var(--fw-m)}
.gnav__i a.on::after{content:'';position:absolute;left:0;right:0;bottom:0;height:2px;
 border-radius:var(--r-cap) var(--r-cap) 0 0;background:var(--ink)}
.gnav__sp{margin-left:auto}
.gnav__x{display:inline-flex;align-items:center;color:var(--sub);text-decoration:none;
 white-space:nowrap;font-size:var(--fs-sm)}
.gnav__x:hover{color:var(--ink)}
.gnav__t{background:var(--fill4);color:var(--ink2);border:0;border-radius:var(--r-cap);
 height:30px;padding:0 var(--sp-3);font:var(--fw-m) var(--fs-sm) var(--font);cursor:pointer}
.gnav__t:hover{background:var(--fill3);color:var(--ink)}
@media(max-width:640px){ .gnav{gap:var(--sp-4);padding:0 var(--sp-4)} .gnav__x{display:none} }
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:400 15px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text","Pretendard","Apple SD Gothic Neo",system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:1024px;margin:0 auto;padding:0 var(--sp-5) var(--sp-16)}
/* ── 머리말 — 가이드·랭귀지·토큰과 같은 모양 ── */
.phead{padding:var(--sp-10) 0 var(--sp-6);max-width:74ch;text-align:left}
.phead .phead__k{display:flex;align-items:center;gap:var(--sp-2);
 margin:0 0 var(--sp-3);font:var(--fw-sb) var(--fs-sm)/1 var(--font);
 letter-spacing:.04em;color:var(--sub2);text-transform:none}
.phead .phead__k .n{font-variant-numeric:tabular-nums;letter-spacing:.1em}
.phead .phead__k .n::after{content:"";display:inline-block;vertical-align:middle;
 width:20px;height:1px;margin:0 var(--sp-1) 0 var(--sp-2);background:var(--line)}
.phead h1{margin:0 0 var(--sp-3);font:var(--fw-sb) var(--fs-3xl)/1.12 var(--font);
 letter-spacing:var(--tr-3xl);color:var(--ink)}
.phead p{margin:0;font-size:var(--fs-lg);line-height:var(--lh-base);color:var(--sub)}
.phead--top{max-width:none;padding:var(--sp-16) 0 var(--sp-8);
 border-bottom:var(--hairline) solid var(--line-soft)}
.phead--top h1{margin-bottom:var(--sp-5);font-size:var(--fs-hero);line-height:1.06;
 letter-spacing:var(--tr-3xl)}
.phead--top>p:not(.phead__k):not(.phead__m){max-width:60ch;font-size:var(--fs-xl);
 line-height:1.5;color:var(--sub)}
.phead--top .phead__m{margin:var(--sp-6) 0 0;display:flex;flex-wrap:wrap;
 gap:var(--sp-1) var(--sp-4);font:var(--fw-m) var(--fs-sm)/1.4 var(--font);
 letter-spacing:.02em;color:var(--sub2)}
@media(max-width:900px){.phead--top{padding:var(--sp-10) 0 var(--sp-6)}
 .phead--top>p:not(.phead__k):not(.phead__m){font-size:var(--fs-lg)}}
.bar{position:sticky;top:96px;z-index:20;padding:14px 0 12px;background:color-mix(in srgb,var(--bg) 82%, transparent);
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
/* ── 왼쪽 목록 — 가이드·랭귀지·토큰과 같은 배치 ── */
.cols{display:grid;grid-template-columns:212px 1fr;gap:var(--sp-8);align-items:start}
.side{position:sticky;top:112px;align-self:start;display:flex;flex-direction:column;gap:1px;
 max-height:calc(100vh - 140px);overflow-y:auto;padding-bottom:var(--sp-6);scrollbar-width:thin}
.side b{display:block;margin:var(--sp-4) 0 var(--sp-1);padding:0 var(--sp-3);
 font:var(--fw-sb) var(--fs-xs)/1.6 var(--font);color:var(--sub2);
 text-transform:uppercase;letter-spacing:.06em}
.side b:first-child{margin-top:0}
.chip{display:flex;align-items:center;justify-content:space-between;gap:8px;
 border:0;background:transparent;color:var(--sub);border-radius:var(--r-in);
 padding:6px var(--sp-3);font:var(--fw-r) var(--fs-md)/1.4 var(--font);cursor:pointer;
 text-align:left;width:100%}
.chip:hover{color:var(--ink);background:var(--fill4)}
.chip[aria-pressed=true]{background:var(--fill3);color:var(--ink);font-weight:var(--fw-m)}
.chip i{font-style:normal;font:var(--fw-r) var(--fs-tag)/1 var(--font-num);color:var(--sub2)}
.chip[aria-pressed=true] i{color:var(--sub)}
@media(max-width:820px){.cols{grid-template-columns:1fr}
 .side{position:static;max-height:none;flex-direction:row;flex-wrap:wrap;gap:6px;
  margin-bottom:var(--sp-4)}
 .side b{display:none}
 .chip{width:auto;border-radius:var(--r-cap);background:var(--card);box-shadow:var(--edge);
  padding:5px 11px;font-size:var(--fs-sm)}
 .chip i{display:none}}
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
<nav class="gnav">
  <a class="gnav__b" href="/index.html">
   <svg viewBox="0 0 24 24"><path d="M12 3.8l8 4.2-8 4.2-8-4.2z"/><path d="M4.4 12.6L12 16.6l7.6-4"/><path d="M4.4 16.8L12 20.8l7.6-4"/></svg>IMT Design</a>
  <div class="gnav__i">
    <a href="/index.html">개요</a>
    <a href="/guide/index.html">가이드</a>
    <a href="/language.html">랭귀지</a>
    <a href="/index-full.html">토큰</a>
    <a href="catalog.html" class="on">아이콘</a>
    <a href="/resources.html">리소스</a>
  </div>
  <span class="gnav__sp"></span>
  <a class="gnav__x" href="https://github.com/imaketoo-david/imt-icons">GitHub</a>
  <button class="gnav__t" id="theme">다크</button>
</nav>
<div class="wrap">
<header class="phead phead--top">
  <p class="phead__k"><span class="n">04</span>아이콘</p>
  <h1>좌표로 그린 __N__종</h1>
  <p>24 그리드 위에 하나씩 직접 그렸다. 굵기 9단·크기 3단이 CSS 변수 두 개로 움직인다.
     아이콘을 누르면 코드가 복사된다.</p>
  <p class="phead__m"><span>24 그리드</span><span>굵기 9단 · 크기 3단</span><span>눌러서 복사</span></p>
</header>

<div class="bar">
 <div class="row">
  <label class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="10.6" cy="10.6" r="6.6"/><path d="M15.4 15.4L20 20"/></svg>
   <input id="q" type="search" placeholder="이름 · 한글 키워드로 검색 (예: 차트, 알림, chart)" autocomplete="off"></label>
  <div class="seg"><button id="mGlyph" aria-pressed="true">글리프</button><button id="mBadge" aria-pressed="false">배지</button></div>
 </div>
</div>

<div class="cols">
  <aside class="side" id="chips"></aside>
  <div>
    <p class="count" id="count"></p>
    <div class="grid" id="grid"></div>
  </div>
</div>

<footer>IMT Icons v1.0 · imaketoo icon system<br>새 아이콘은 <code>src/icondata.py</code> 에 추가 후 빌드 스크립트를 다시 실행하세요.</footer>
</div>

<dialog id="dlg"><button class="close" onclick="dlg.close()">&times;</button><div class="dlg">
 <h3 id="dName"></h3><p class="cat" id="dCat"></p>
 <div class="prev" id="dPrev"></div>
 <div class="copy" id="dCopy"></div>
</div></dialog>

<div class="toast" id="toast"></div>

<script>
(function(){
  var T=document.getElementById("theme");
  function ap(d){document.documentElement.setAttribute("data-theme",d?"dark":"light");
                 T.textContent=d?"라이트":"다크";}
  var d=matchMedia("(prefers-color-scheme: dark)").matches;
  try{var v=localStorage.getItem("imt-theme"); if(v) d=v==="dark";}catch(e){}
  ap(d);
  T.onclick=function(){d=!d;ap(d);try{localStorage.setItem("imt-theme",d?"dark":"light")}catch(e){}};
})();
</script>
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
const cnt = {}; names.forEach(n => cnt[DATA[n].c] = (cnt[DATA[n].c]||0) + 1);
chips.innerHTML = `<b>분류</b><button class="chip" data-c="all" aria-pressed="true">전체<i>${names.length}</i></button>`
 + Object.entries(CATS).filter(([k])=>cnt[k])
    .map(([k,v])=>`<button class="chip" data-c="${k}" aria-pressed="false">${v}<i>${cnt[k]}</i></button>`).join("");
chips.onclick=e=>{const b=e.target.closest(".chip"); if(!b)return;
 cat=b.dataset.c; [...chips.querySelectorAll(".chip")].forEach(c=>c.setAttribute("aria-pressed", c===b));
 render();};

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
out = (HTML.replace("__TOKENS__", TOKENS)
            .replace("__PAL__", pal)
           .replace("__N__", str(len(names)))
           .replace("__SW__", str(STROKE))
           .replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
           .replace("__CATS__", json.dumps(CATS, ensure_ascii=False))
           .replace("__PALETTE__", json.dumps(PALETTE))
           .replace("__SQ__", sq))
open(f"{ROOT}/catalog.html", "w").write(out)
print("catalog OK", len(out), "bytes")
