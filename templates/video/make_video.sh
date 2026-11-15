# usage (from repo root, after build.py made work/<name>.html):
#   nohup sh templates/video/make_video.sh <name> > work/<name>_video.log 2>&1 &
# then poll the log until it prints FIN. Output: work/<name>_video/<name>.mp4 (1080x1920, ~55s, voice + music)
set -e
N=$1; R=$(cd "$(dirname "$0")/../.." && pwd); VD=$R/work/${N}_video; export VD
mkdir -p $VD
cd $R/templates
sed 's#</style>#.ink .clue{visibility:hidden}.ink .swipe{visibility:hidden}</style>#' ../work/$N.html > ../work/${N}_blank.html
sed 's#</style>#.ink .swipe{visibility:hidden}</style>#' ../work/$N.html > ../work/${N}_full.html
python3 shoot.py ../work/${N}_blank.html $VD/blank
python3 shoot.py ../work/${N}_full.html $VD/full
cd $R/templates/video
python3 make_script.py $R/work/clues_$N.html $VD
python3 tts.py $VD af_heart 1.15
python3 render.py video
python3 audio.py
printf "file '$VD/scene_%s.mp4'\n" hook c1 c2 c3 c4 c5 outro > $VD/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $VD/list.txt -c copy $VD/v.mp4
ffmpeg -y -loglevel error -i $VD/v.mp4 -i $VD/mix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart $VD/$N.mp4
ffmpeg -y -loglevel error -ss 20 -i $VD/$N.mp4 -frames:v 1 -vf scale=540:960 $VD/check_20s.jpg
ffprobe -v error -show_entries format=duration -of csv=p=0 $VD/$N.mp4
echo FIN
