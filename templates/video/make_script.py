# usage: python3 make_script.py work/clues_<name>.html OUTDIR  -> OUTDIR/script.json (narration)
import re, sys, json, html, os
src=open(sys.argv[1]).read(); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
clues=[html.unescape(re.sub(r'<[^>]+>','',c)).replace('‑','-').strip() for c in re.findall(r'<div class="clue">(.*?)</div>',src,re.S)]
assert len(clues)==5, f'expected 5 clues, found {len(clues)}'
S={"h1":"Can you name this Naruto character in five clues?",
"h2":"Clue one is brutal. Clue five is basically free. Comment the clue you got it on!"}
names=["Clue one!","Clue two!","Clue three!","Clue four!","Last clue!"]
quips=["Already got it? That's Kage level!","Got it here? Jonin level. Still elite!","If you've got it now, that's Chunin level!","Getting warmer! This is Genin territory.","Got it on this one? Back to the Academy!"]
for i in range(5):
    S[f"c{i+1}a"]=names[i]; S[f"c{i+1}b"]=clues[i]; S[f"q{i+1}"]=quips[i]
S["o1"]="So, who is it? Comment your answer, and the clue that gave it away!"
S["o2"]="Follow for a new Naruto quiz every day!"
json.dump(S,open(f'{out}/script.json','w'),indent=1); print('\n'.join(clues))
