import json, re, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
import os
M=os.path.expanduser('~/tts')
k=Kokoro(M+'/v.onnx',M+'/voices.bin')
OUT=sys.argv[1]; V=sys.argv[2] if len(sys.argv)>2 else 'af_heart'; SPD=float(sys.argv[3]) if len(sys.argv)>3 else 1.15
import os; os.makedirs(OUT,exist_ok=True)
L=json.load(open(f'{OUT}/script.json')); dur={}
def trim(s):
    a=np.abs(s); idx=np.where(a>0.02)[0]; return s[max(0,idx[0]-240):idx[-1]+480]
for key,txt in L.items():
    # '|' = comedic beat. split into sentences/phrases
    segs=re.findall(r'[^.?!|]+[.?!]?\|?',txt)
    out=[]
    for sg in segs:
        beat=sg.endswith('|'); sg=sg.rstrip('|').strip()
        if not sg: continue
        sp=SPD
        s,sr=k.create(sg,voice=V,speed=sp,lang='en-us'); out.append(trim(s))
        gap=0.32 if beat else (0.11 if sg.endswith('?') else 0.07)
        out.append(np.zeros(int(gap*sr)))
    x=np.concatenate(out[:-1]); sf.write(f'{OUT}/a_{key}.wav',x,24000); dur[key]=len(x)/24000
json.dump(dur,open(f'{OUT}/dur.json','w'),indent=1); print('done',sum(dur.values()))
