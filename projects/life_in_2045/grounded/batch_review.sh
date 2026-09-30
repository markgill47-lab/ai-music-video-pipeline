# grid every finished render that has no grid yet, stack them into frames/<sheet>.jpg
PY=/d/Projects_26/Comfyu/ComfyUI/venv/Scripts/python.exe
new=""; for f in /d/Projects_26/Comfyu/ComfyUI/output/video/H3_s[0-9][0-9]*_0*.mp4; do n=$(basename $f | sed -E 's/^H3_//; s/_[0-9]{5}_\.mp4$//'); [ -f frames/$n.png ] || new="$new $n"; done
new=$(echo $new | tr ' ' '\n' | sort -u | tr '\n' ' '); echo NEW: $new
[ -z "$new" ] && exit 0
$PY review_shots.py $new 2>&1 | grep "frames$"
cd frames; /d/Projects_26/Minimax/.venv_audio/Scripts/python -c "
import sys
from PIL import Image,ImageDraw,ImageFont
out,fs=sys.argv[1],sys.argv[2:];ims=[Image.open(f+'.png') for f in fs]
W=ims[0].width;H=sum(i.height for i in ims)+30*len(ims);s=Image.new('RGB',(W,H),'black');d=ImageDraw.Draw(s);ft=ImageFont.truetype('arialbd.ttf',22);y=0
for f,i in zip(fs,ims): d.text((6,y+3),f,fill='yellow',font=ft);y+=30;s.paste(i,(0,y));y+=i.height
s.save(out,quality=85)" $1 $new
