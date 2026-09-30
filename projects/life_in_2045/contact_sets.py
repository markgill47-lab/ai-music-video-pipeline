import sys,glob,os
from PIL import Image,ImageDraw,ImageFont
out,cols,W,H=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]); fs=[]
for pat in sys.argv[5:]: fs+=sorted(glob.glob(pat))
ft=ImageFont.truetype('arialbd.ttf',20);rows=(len(fs)+cols-1)//cols
s=Image.new('RGB',(W*cols,H*rows),'white');d=ImageDraw.Draw(s)
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB');im.thumbnail((W,H));x,y=(i%cols)*W,(i//cols)*H;s.paste(im,(x+(W-im.width)//2,y+(H-im.height)//2))
    l=os.path.basename(f).split('/')[-1].replace('set_','').replace('_000','').replace('_.png','');d.rectangle([x,y,x+len(l)*11+10,y+26],fill='black');d.text((x+5,y+2),l,fill='yellow',font=ft)
s.save(out,quality=88)
