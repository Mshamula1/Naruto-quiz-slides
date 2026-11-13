# Naruto "Ink & Washi" slide builder (deliberately unlike the One Piece style).
# usage: python3 build.py ../work/clues_<name>.html ../work/<name>.html
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = 'file://' + os.path.join(HERE, 'fonts')
base = open(os.path.join(HERE, 'base.html')).read()
cover = base[base.index('<!-- 1. COVER -->'):base.index('<!-- 2. CLUE 1')].replace('src="cover_art.jpg"', 'src="file://' + os.path.join(HERE, 'cover_art.jpg') + '"')
cover_css = base[base.index('<style>') + 7:base.index('</style>')]
clues = open(sys.argv[1]).read()

css = '''<style>
@font-face{font-family:Anton;src:url(%(F)s/anton-latin-400-normal.woff2)}
@font-face{font-family:Oswald;font-weight:500;src:url(%(F)s/oswald-latin-500-normal.woff2)}
@font-face{font-family:Oswald;font-weight:700;src:url(%(F)s/oswald-latin-700-normal.woff2)}
%(cover)s
/* ---------- NARUTO INK & WASHI STYLE ---------- */
.ink{width:1080px;height:1920px;position:relative;overflow:hidden;color:#141210;font-family:Oswald,sans-serif;background:#f1e7d2}
.ink .paper-tex{position:absolute;inset:0;pointer-events:none}
.ink .sun{position:absolute;border-radius:50%%;pointer-events:none}
.ink .label{position:absolute;top:92px;right:70px;font-family:Anton;font-size:34px;letter-spacing:6px;color:#141210;writing-mode:vertical-rl;text-orientation:mixed;line-height:1}
.ink .stamp{position:absolute;top:88px;left:70px;width:170px;height:170px;background:#d8361f;color:#f8efe0;border-radius:10px;transform:rotate(-6deg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Anton;line-height:.95;box-shadow:inset 0 0 0 7px #f1e7d2,inset 0 0 0 11px #d8361f;
  filter:url(#roughen)}
.ink .stamp b{font-size:30px;font-weight:400;letter-spacing:4px}.ink .stamp i{font-style:normal;font-size:84px}
.ink .art{position:absolute;left:0;top:270px;width:1080px;height:900px}
.ink .band{position:absolute;left:0;right:0;top:1190px;height:520px}
.ink .band svg{position:absolute;inset:0;width:100%%;height:100%%}
.ink .cluebox{position:absolute;left:96px;right:96px;top:1270px;color:#f4ecdc}
.ink .num{font-family:Anton;font-size:34px;letter-spacing:8px;color:#ff6a3d;margin-bottom:18px}
.ink .clue{font-family:Oswald;font-weight:700;font-size:72px;line-height:1.16;letter-spacing:.3px;text-transform:uppercase}
.ink .clue em{font-style:normal;color:#141210;background:linear-gradient(transparent 10%%,#ff6a3d 10%%,#ff6a3d 94%%,transparent 94%%);padding:0 10px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.ink .lvl{position:absolute;right:70px;top:1735px;font-family:Anton;font-size:34px;letter-spacing:3px;color:#141210;text-align:right}
.ink .lvl span{color:#d8361f}
.ink .swipe{position:absolute;left:70px;top:1735px;font-family:Anton;font-size:34px;letter-spacing:5px;color:#141210}
</style>''' % {'F': F, 'cover': cover_css}

defs = '''<svg width="0" height="0" style="position:absolute"><defs>
<filter id="roughen"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="3"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter>
<filter id="brush" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.02 0.09" numOctaves="4" seed="8"/><feDisplacementMap in="SourceGraphic" scale="14"/></filter>
<filter id="wash" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="40" result="d"/><feGaussianBlur in="d" stdDeviation="10"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .27  0 0 0 0 .15  0 0 0 .22 0"/></filter>
<filter id="fibers"><feTurbulence type="turbulence" baseFrequency="0.004 0.06" numOctaves="2" seed="11"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 .18 0"/></filter>
<radialGradient id="vsun"><stop offset="0" stop-color="#e2492b"/><stop offset=".7" stop-color="#d8361f"/><stop offset="1" stop-color="#b8261a"/></radialGradient>
<linearGradient id="mist" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f1e7d2" stop-opacity="0"/><stop offset="1" stop-color="#f1e7d2"/></linearGradient>
</defs></svg>'''

PAPER = '<svg class="paper-tex" viewBox="0 0 1080 1920"><rect width="1080" height="1920" filter="url(#fibers)"/><rect width="1080" height="1920" filter="url(#grain)"/></svg>'
BAND = ('<div class="band"><svg viewBox="0 0 1080 520" preserveAspectRatio="none">'
        '<path d="M-20 40 C120 10 260 46 420 22 C600 0 760 44 900 18 C980 6 1040 24 1100 14 L1100 470 C960 500 820 478 660 500 C480 520 300 488 140 506 C60 514 0 500 -20 506Z" fill="#141210" filter="url(#brush)"/>'
        '<path d="M60 60 C300 48 600 70 1000 52" stroke="#2c2724" stroke-width="10" fill="none" filter="url(#brush)"/></svg></div>')

def expand(html):
    # each clue <section class="ink"> gets the paper texture and the ink band injected
    return html.replace('<!--PAPER-->', PAPER).replace('<!--BAND-->', BAND)

final = '''<!-- 7. FINAL -->
<section class="slide ink" style="background:#141210;color:#f1e7d2">
  <svg class="paper-tex" viewBox="0 0 1080 1920"><rect width="1080" height="1920" filter="url(#grain)" opacity=".6"/></svg>
  <svg style="position:absolute;left:0;top:180px;width:1080px;height:1000px" viewBox="0 0 1080 1000">
    <!-- brush enso circle -->
    <path d="M540 120 C800 110 930 300 920 500 C910 720 740 860 540 870 C320 880 150 720 150 500 C150 300 300 150 470 128" fill="none" stroke="#d8361f" stroke-width="64" stroke-linecap="round" filter="url(#brush)"/>
    <text x="540" y="690" text-anchor="middle" font-family="Anton" font-size="520" fill="#f1e7d2">?</text>
  </svg>
  <div style="position:absolute;top:96px;left:0;right:0;text-align:center;font-family:Anton;font-size:34px;letter-spacing:10px;color:#d8361f">THE REVEAL</div>
  <div style="position:absolute;left:0;right:0;top:1170px;text-align:center;font-family:Anton;font-size:150px;line-height:.95;letter-spacing:2px">WHO WAS IT?</div>
  <div style="position:absolute;left:0;right:0;top:1360px;text-align:center">
    <div style="display:inline-block;background:#f1e7d2;color:#141210;font-family:Oswald;font-weight:700;font-size:50px;padding:18px 40px;text-transform:uppercase;letter-spacing:1px;filter:url(#roughen)">Drop your guess below</div>
    <div style="margin-top:40px;font-family:Oswald;font-weight:500;font-size:42px;letter-spacing:1px">and tell us which clue gave it away</div>
  </div>
  <div style="position:absolute;left:0;right:0;top:1700px;text-align:center;font-family:Anton;font-size:32px;letter-spacing:6px;color:#d8361f">ANSWER PINNED LATER</div>
</section>'''

html = ('<!DOCTYPE html><html><head><meta charset="utf-8">' + css + '</head><body>' + defs
        + cover + expand(clues) + final + '</body></html>')
open(sys.argv[2] if len(sys.argv) > 2 else 'slides_current.html', 'w').write(html)
