import json, subprocess, os, sys, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(os.path.dirname(HERE)); F=os.path.join(REPO,'templates','fonts')+'/'
W,H,FPS=1080,1920,30
VD=os.environ['VD']; V=VD; D=json.load(open(f'{VD}/dur.json')); S={k:v.replace('|','') for k,v in json.load(open(f'{VD}/script.json')).items()}
ANTON=lambda s: ImageFont.truetype(F+'anton-latin-400-normal.woff2',s)
OSW=lambda s: ImageFont.truetype(F+'oswald-latin-700-normal.woff2',s)
INK=(20,18,16); CREAM=(241,231,210); RED=(216,54,31); ORANGE=(255,106,61)
cover=Image.open(os.path.join(REPO,'slides','cover.jpg')).convert('RGB')
blank=[Image.open(f'{V}/blank/slide_{i}.png').convert('RGB') for i in range(2,8)]
full=[Image.open(f'{V}/full/slide_{i}.png').convert('RGB') for i in range(2,8)]

def zoom(img,z,cy=0.4):
    w,h=int(W/z),int(H/z); x=(W-w)//2; y=int((H-h)*cy)
    return img.crop((x,y,x+w,y+h)).resize((W,H),Image.BILINEAR)

def chunks(text,n=3):
    w=text.split(); return [' '.join(w[i:i+n]) for i in range(0,len(w),n)]
def caption_at(text,t,dur):
    cs=chunks(text); tot=sum(len(c)+2 for c in cs); acc=0
    for c in cs:
        d=(len(c)+2)/tot*dur
        if t<acc+d: return c
        acc+=d
    return cs[-1]

def soft_caption(im,txt,y):
    f=OSW(62); d0=ImageDraw.Draw(im); tw=d0.textlength(txt,font=f); x=(W-tw)/2
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(gl).rounded_rectangle((x-40,y-10,x+tw+40,y+92),radius=50,fill=(10,20,40,95))
    gl=gl.filter(ImageFilter.GaussianBlur(28)); im.paste(gl,(0,0),gl)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((x,y+3),txt,font=f,fill=(0,0,0,210))
    sh=sh.filter(ImageFilter.GaussianBlur(5)); im.paste(sh,(0,0),sh)
    ImageDraw.Draw(im).text((x,y),txt,font=f,fill=(255,255,255))
    return im
def draw_caption(im,txt,y,style='band',scale=1.0,bottom=None):
    d=ImageDraw.Draw(im); txt=txt.upper()
    f=ANTON(int(96*scale))
    # wrap
    words=txt.split(); lines=[]; cur=''
    for w_ in words:
        t=(cur+' '+w_).strip()
        if d.textlength(t,font=f)>880 and cur: lines.append(cur); cur=w_
        else: cur=t
    lines.append(cur)
    lh=int(110*scale)
    if bottom: y=bottom-len(lines)*lh
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=f); x=(W-tw)/2; yy=y+i*lh
        if style=='band':
            d.rectangle((x-26,yy-8,x+tw+26,yy+lh-4),fill=INK)
            d.text((x,yy-6),l,font=f,fill=CREAM)
        else: # sticker
            d.rectangle((x-30,yy-10,x+tw+30,yy+lh-2),fill=RED)
            d.text((x,yy-8),l,font=f,fill=CREAM)
    return im

def countdown(im,t):  # t in [0,1.8)
    n=3-int(t/0.5); frac=(t%0.5)/0.5
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.rectangle((0,0,W,1200),fill=(241,231,210,150))
    cx,cy,r=540,560,210
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=INK+(255,),width=18)
    d.arc((cx-r,cy-r,cx+r,cy+r),-90,-90+360*(1-frac),fill=RED+(255,),width=30)
    s=1.0+0.25*(1-min(1,frac*4))
    f=ANTON(int(260*s)); tw=d.textlength(str(n),font=f)
    d.text((cx-tw/2,cy-int(185*s)),str(n),font=f,fill=INK+(255,))
    f2=ANTON(70); l='LOCK IN YOUR GUESS'; tw=d.textlength(l,font=f2)
    d.rectangle((540-tw/2-24,840,540+tw/2+24,940),fill=INK+(255,))
    d.text((540-tw/2,842),l,font=f2,fill=CREAM+(255,))
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')

def enc(name,frames_fn,n):
    tmp=f'{VD}/scene_{name}.tmp.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frames_fn(i/FPS).tobytes())
    p.stdin.close(); assert p.wait()==0; os.rename(tmp,f'{VD}/scene_{name}.mp4')

GAP=0.12; timeline=[]  # (abs_time, wavkey) and sfx list
sfx=[]; T=0.0
def nf(d): return int(round(d*FPS))

# ---- HOOK
t1=0.15; t2=t1+D['h1']+GAP; hd=t2+D['h2']+0.2
def hook(t):
    im=zoom(cover,1+0.05*t/hd)
    if t1<=t<t1+D['h1']: soft_caption(im,caption_at(S['h1'],t-t1,D['h1']),1180)
    elif t>=t2 and t<t2+D['h2']: soft_caption(im,caption_at(S['h2'],t-t2,D['h2']),1180)
    return im
scenes=[('hook',hook,nf(hd))]; timeline+= [(T+t1,'h1'),(T+t2,'h2')]; sfx.append((T,'hit')); T+=nf(hd)/FPS

# ---- CLUES
for i in range(5):
    a=0.12; b=a+D[f'c{i+1}a']+0.05; c=b+D[f'c{i+1}b']+0.2; q=c+1.5+0.05; end=q+D[f'q{i+1}']+0.3
    def clue(t,i=i,a=a,b=b,c=c,q=q,end=end):
        z=1+0.06*t/end
        if t<b-0.15: im=zoom(blank[i],z)
        elif t<b+0.05: im=Image.blend(zoom(blank[i],z),zoom(full[i],z),(t-(b-0.15))/0.2)
        else: im=zoom(full[i],z)
        if c<=t<c+1.5: im=countdown(im,t-c)
        if t>=q: draw_caption(im,caption_at(S[f'q{i+1}'],t-q,D[f'q{i+1}']),0,'sticker',0.8,bottom=1185)
        return im
    scenes.append((f'c{i+1}',clue,nf(end)))
    timeline+=[(T+a,f'c{i+1}a'),(T+b,f'c{i+1}b'),(T+q,f'q{i+1}')]
    sfx+= [(T,'whoosh'),(T+a,'hit')]+[(T+c+k*0.5,'tick') for k in range(3)]+[(T+c+1.5,'ding')]
    T+=nf(end)/FPS

# ---- OUTRO
o1=0.2; o2=o1+D['o1']+GAP; od=o2+D['o2']+0.8
def outro(t):
    im=zoom(blank[5],1+0.04*t/od); ImageDraw.Draw(im).rectangle((0,1520,W,1610),fill=(27,24,21))
    if o1<=t<o1+D['o1']: draw_caption(im,caption_at(S['o1'],t-o1,D['o1']),0,'sticker',0.8,bottom=1625)
    elif t>=o2 and t<o2+D['o2']: draw_caption(im,caption_at(S['o2'],t-o2,D['o2']),0,'sticker',0.8,bottom=1625)
    return im
scenes.append(('outro',outro,nf(od))); timeline+=[(T+o1,'o1'),(T+o2,'o2')]; sfx.append((T,'whoosh')); T+=nf(od)/FPS
json.dump({'T':T,'timeline':timeline,'sfx':sfx},open(f'{VD}/plan.json','w'))

if sys.argv[1]=='stills':
    for name,fn,n in scenes:
        for tt in [n/FPS*0.3,n/FPS*0.62,n/FPS*0.85]:
            fn(tt).resize((540,960)).save(f'{V}/still_{name}_{tt:.1f}.jpg')
else:
    only=sys.argv[2:] 
    for name,fn,n in scenes:
        if not only or name in only: enc(name,fn,n); print('done',name,flush=True)
