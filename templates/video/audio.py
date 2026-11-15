import json, numpy as np, soundfile as sf
from scipy.signal import resample_poly
import os; V=os.environ['VD']; SR=48000
P=json.load(open(f'{V}/plan.json')); N=int((P['T']+0.1)*SR)
voice=np.zeros(N); fx=np.zeros(N); mus=np.zeros(N)
def put(buf,t,x,g=1.0):
    i=int(t*SR); x=x[:max(0,N-i)]; buf[i:i+len(x)]+=x*g
for t,k in P['timeline']:
    a,sr=sf.read(f'{V}/a_{k}.wav'); a=resample_poly(a,2,1) if sr==24000 else a; put(voice,t,a)
rng=np.random.default_rng(1)
def env(n,dec): return np.exp(-np.arange(n)/(dec*SR))
def hit():
    n=int(.7*SR); tt=np.arange(n)/SR; f=70*np.exp(-tt*3)+45
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.18)*0.9+rng.normal(0,1,n)*env(n,.02)*0.25
def whoosh():
    n=int(.45*SR); w=rng.normal(0,1,n); 
    from scipy.signal import butter,lfilter; b,a=butter(2,[600/(SR/2),3500/(SR/2)],'band'); w=lfilter(b,a,w)
    e=np.sin(np.linspace(0,np.pi,n))**2; return w*e*0.35
def tick():
    n=int(.06*SR); return np.sin(2*np.pi*1800*np.arange(n)/SR)*env(n,.012)*0.35
def ding():
    n=int(.9*SR); tt=np.arange(n)/SR; return (np.sin(2*np.pi*1320*tt)+.5*np.sin(2*np.pi*2640*tt))*env(n,.25)*0.22
def shing():
    n=int(.9*SR); tt=np.arange(n)/SR
    from scipy.signal import butter,lfilter; b,a_=butter(2,[4000/(SR/2),12000/(SR/2)],'band'); w=lfilter(b,a_,rng.normal(0,1,n))
    sweep=np.sin(2*np.pi*np.cumsum(2500+3000*tt)/SR)
    att=np.clip(tt/0.03,0,1)
    return (w*0.5*env(n,.12)+sweep*0.25*env(n,.35)+np.sin(2*np.pi*5200*tt)*0.12*env(n,.5))*att
def gong():
    n=int(3.5*SR); tt=np.arange(n)/SR
    return sum(np.sin(2*np.pi*f*tt)*g for f,g in [(98,1),(196.5,.5),(263,.35),(410,.25),(587,.15)])*env(n,1.2)*0.5*np.clip(tt/0.01,0,1)
G={'shing':shing,'gong':gong,'hit':hit,'whoosh':whoosh,'tick':tick,'ding':ding}
for t,k in P['sfx']: put(fx,max(0,t-(0.2 if k=='whoosh' else 0)),G[k]())
# music bed: taiko ensemble + low drone + sparse koto, 92 bpm
beat=60/112; scale=[146.83,155.56,196.0,220.0,233.08,293.66,311.13,392.0]
def pluck(f,dur=2.0):
    n=int(dur*SR); p=int(SR/f); buf=rng.uniform(-1,1,p); out=np.zeros(n)
    for i in range(n): out[i]=buf[i%p]; buf[i%p]=0.997*0.5*(buf[i%p]+buf[(i+1)%p])
    return out
def taiko(f0=60,dec=.25,g=1.0):
    n=int(.8*SR); tt=np.arange(n)/SR
    return (np.sin(2*np.pi*(f0+40*np.exp(-tt*25))*tt)*env(n,dec)+rng.normal(0,1,n)*env(n,.015)*0.3)*g
cache={}; big=taiko(55,.35); small=taiko(110,.12,.5); rim=np.sin(2*np.pi*900*np.arange(int(.05*SR))/SR)*env(int(.05*SR),.01)*0.4
pat=[big,None,small,small,None,small,big,None]
t=0.0;k=0
while t<P['T']:
    x=pat[k%8]
    if x is not None: put(mus,t,x,0.32)
    if k%8==4: put(mus,t,rim,0.6)
    if k%16 in (0,6,11):
        f=scale[[0,4,2,5,3,7,1,6][(k//16)%8]]
        if f not in cache: cache[f]=pluck(f)
        put(mus,t,cache[f],0.2)
    t+=beat/2;k+=1
tt=np.arange(N)/SR; mus+=0.0*(np.sin(2*np.pi*73.4*tt)+0.5*np.sin(2*np.pi*110*tt))*(0.7+0.3*np.sin(2*np.pi*0.1*tt))
# duck music under voice
venv=np.convolve(np.abs(voice),np.ones(4800)/4800,'same'); duck=1-0.55*np.clip(venv*12,0,1)
mix=voice*1.0+fx*0.9+mus*duck*0.9
fade=int(1.2*SR); mix[-fade:]*=np.linspace(1,0,fade)
mix=mix/np.max(np.abs(mix))*0.89
sf.write(f'{V}/mix.wav',np.stack([mix,mix],1),SR)
print('ok',P['T'])
