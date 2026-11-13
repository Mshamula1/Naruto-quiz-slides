import sys, os
base=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'base.html')).read()
css=base[base.index('<style>'):base.index('</style>')+8]
cover=base[base.index('<!-- 1. COVER -->'):base.index('<!-- 2. CLUE 1')]
final=base[base.index('<!-- 7. FINAL -->'):base.index('<script>')]
clues=open(sys.argv[1]).read()
defs='''<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="parch" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#f7e9c8"/><stop offset=".6" stop-color="#ead2a0"/><stop offset="1" stop-color="#cfae72"/></linearGradient>
<linearGradient id="roll" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#e9d2a0"/><stop offset=".5" stop-color="#fff2d4"/><stop offset="1" stop-color="#b8925a"/></linearGradient>
<linearGradient id="gold" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffe9a0"/><stop offset=".5" stop-color="#d4a42c"/><stop offset="1" stop-color="#7a5510"/></linearGradient>
<linearGradient id="cane" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#5a3a24"/><stop offset=".45" stop-color="#2a170b"/><stop offset="1" stop-color="#120a05"/></linearGradient>
<linearGradient id="steel2" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#cdd6e3"/><stop offset="1" stop-color="#7c889c"/></linearGradient>
<pattern id="grille" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#9aa0a8"/><circle cx="6" cy="6" r="3" fill="#3a3d42"/></pattern>
<filter id="dropsh"><feDropShadow dx="12" dy="16" stdDeviation="5" flood-opacity=".5"/></filter>
<filter id="fogblur"><feGaussianBlur stdDeviation="22"/></filter>
<g id="stormsea"><path d="M0 800 Q60 760 120 800 T240 800 T360 800 T480 800 T600 800 T720 800 T840 800 T960 800 T1080 800 L1080 960 L0 960Z" fill="#14435e" stroke="#06202f" stroke-width="8"/>
 <path d="M0 860 Q70 815 140 860 T280 860 T420 860 T560 860 T700 860 T840 860 T980 860 T1120 860 L1080 960 L0 960Z" fill="#0f3249" stroke="#06202f" stroke-width="8"/>
 <g fill="#fff" opacity=".85"><path d="M110 795 q20 -30 45 -8 q-25 -6 -45 8z"/><path d="M470 795 q20 -30 45 -8 q-25 -6 -45 8z"/><path d="M830 795 q20 -30 45 -8 q-25 -6 -45 8z"/><path d="M290 855 q20 -30 45 -8 q-25 -6 -45 8z"/><path d="M650 855 q20 -30 45 -8 q-25 -6 -45 8z"/></g></g>
<g id="bluesea"><path d="M0 820 Q45 790 90 820 T180 820 T270 820 T360 820 T450 820 T540 820 T630 820 T720 820 T810 820 T900 820 T990 820 T1080 820 L1080 960 L0 960Z" fill="#1f7fc4" stroke="#0b3f6e" stroke-width="8"/>
 <path d="M0 880 Q60 850 120 880 T240 880 T360 880 T480 880 T600 880 T720 880 T840 880 T960 880 T1080 880 L1080 960 L0 960Z" fill="#16679f" stroke="#0b3f6e" stroke-width="8"/>
 <g fill="#fff"><circle cx="90" cy="812" r="8"/><circle cx="450" cy="812" r="8"/><circle cx="810" cy="812" r="8"/><circle cx="300" cy="872" r="7"/><circle cx="660" cy="872" r="7"/></g></g>
<g id="rope"><path d="M30 30 Q540 -10 1050 30" stroke="#c89a55" stroke-width="16" fill="none" stroke-dasharray="22 8"/></g>
</defs></svg>'''
script='''<script>
// crew list rows (abstract scribbles, all crossed out)
document.querySelectorAll('#rows').forEach(g=>{let h='';for(let i=0;i<8;i++){const y=-180+i*55,w=180+((i*73)%140);
 h+=`<path d="M-200 ${y} q15 -18 30 0 t30 0 t30 0 t30 0 t30 0" stroke="#3a2210" stroke-width="7" fill="none" transform="scale(${w/150} 1) translate(${-200*(w/150-1)/(w/150)} 0)"/>`;
 h+=`<line x1="-215" y1="${y-6}" x2="${-200+w+30}" y2="${y-4}" stroke="#c8262c" stroke-width="9" stroke-linecap="round"/>`;
 h+=`<text x="210" y="${y+12}" font-family="DejaVu Serif" font-weight="bold" font-size="40" fill="#3a2210">†</text>`;}g.innerHTML=h});
// tally marks: 10 groups shown as 5-bars
document.querySelectorAll('#tally').forEach(g=>{let h='';for(let k=0;k<4;k++){const x0=-95+k*78;for(let i=0;i<4;i++)h+=`<line x1="${x0+i*13}" y1="-40" x2="${x0+i*13}" y2="6"/>`;h+=`<line x1="${x0-8}" y1="-6" x2="${x0+50}" y2="-30"/>`;}g.innerHTML=h});
// crowd of raised hands
document.querySelectorAll('#crowd').forEach(g=>{let h='';for(let i=0;i<14;i++){const x=40+i*75,y=900-(i%3)*25;
 h+=`<ellipse cx="${x}" cy="${y+60}" rx="48" ry="70"/><rect x="${x-10}" y="${y-110}" width="22" height="150" rx="10" transform="rotate(${(i%2?12:-10)} ${x} ${y})"/><circle cx="${x+(i%2?-12:12)}" cy="${y-118}" r="20" transform="rotate(${(i%2?12:-10)} ${x} ${y})"/>`;}g.innerHTML=h});
// laurel wreath: two symmetric arcs of leaves around the medal
document.querySelectorAll('#laurel').forEach(g=>{let h='';const cx=540,cy=470,R=185;
 for(const side of [-1,1])for(let i=0;i<9;i++){const t=(200+i*16)*Math.PI/180;
  const x=cx+side*R*Math.cos(t)*-1, y=cy-R*Math.sin(t);
  const rot=side*(-(i*16)+70);h+=`<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="34" ry="15" transform="rotate(${rot} ${x.toFixed(1)} ${y.toFixed(1)})"/>`;}
 g.innerHTML=h});
// lots of candles
document.querySelectorAll('#candles').forEach(g=>{let h='';let k=0;
 for(let row=0;row<3;row++)for(let i=0;i<9-row*2;i++){const x=-200+row*50+i*50,y=-120-row*14;k++;
  h+=`<rect x="${x-6}" y="${y-60}" width="12" height="60" rx="3" fill="${['#4fb3ff','#ffd34d','#7dffbf','#ff8fb0'][k%4]}" stroke="#2a0f1e" stroke-width="3"/>`;
  h+=`<path d="M${x} ${y-92} C${x+12} ${y-74} ${x+8} ${y-62} ${x} ${y-60} C${x-8} ${y-62} ${x-12} ${y-74} ${x} ${y-92}Z" fill="#ffb020" stroke="#c8262c" stroke-width="2"/>`;}
 g.innerHTML=h});
// snowfall
document.querySelectorAll('#snow').forEach(g=>{let h='';let s=7;const r=()=>{s=(s*16807)%2147483647;return s/2147483647};
 for(let i=0;i<90;i++)h+=`<circle cx="${(r()*1080).toFixed(0)}" cy="${(r()*940).toFixed(0)}" r="${(2+r()*6).toFixed(1)}" opacity="${(.4+r()*.6).toFixed(2)}"/>`;g.innerHTML=h});
// five open empty chests on a cliff top
document.querySelectorAll('#chests').forEach(g=>{let h='';
 [[330,330,-8],[430,320,4],[540,316,0],[650,320,-4],[750,330,8]].forEach(([x,y,r])=>{
  h+=`<g transform="translate(${x} ${y}) rotate(${r})" filter="url(#dropsh)">
   <path d="M-45 -40 L45 -40 L40 -95 C20 -110 -20 -110 -40 -95Z" fill="#b06a2c" stroke="#2a1306" stroke-width="6"/>
   <rect x="-50" y="-40" width="100" height="70" rx="6" fill="#9a5a24" stroke="#2a1306" stroke-width="6"/>
   <path d="M-44 -38 L44 -38 L40 -24 L-40 -24Z" fill="#120804"/>
   <rect x="-12" y="-14" width="24" height="22" rx="4" fill="#d4a42c" stroke="#2a1306" stroke-width="4"/></g>`;});
 g.innerHTML=h});
// calendar of crossed-out days
document.querySelectorAll('#xgrid').forEach(g=>{let h='';
 for(let r=0;r<4;r++)for(let c=0;c<6;c++){const x=-140+c*50,y=-90+r*55;
  h+=`<rect x="${x}" y="${y}" width="40" height="44" rx="4" fill="#f2f2f2" stroke="#999" stroke-width="2"/><path d="M${x+6} ${y+6} L${x+34} ${y+38} M${x+34} ${y+6} L${x+6} ${y+38}" stroke="#c8262c" stroke-width="5" stroke-linecap="round"/>`;}
 g.innerHTML=h});
</script>'''
html='<!DOCTYPE html><html><head><meta charset="utf-8">'+css+'</head><body>'+defs+cover+clues+final+script+'</body></html>'
open(sys.argv[2] if len(sys.argv)>2 else 'slides_current.html','w').write(html)
