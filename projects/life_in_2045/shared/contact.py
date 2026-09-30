import sys,glob
from PIL import Image,ImageDraw,ImageFont
out,cols,labels=sys.argv[1],int(sys.argv[2]),sys.argv[3:]
fs=[];labs=[]
for spec in labels:
    tag,pat=spec.split('=',1)
    for i,p in enumerate(sorted(glob.glob(pat))): fs.append(p);labs.append(f'{tag}{i+1}')
W=360;rows=(len(fs)+cols-1)//cols
sheet=Image.new('RGB',(W*cols,W*rows),'white');d=ImageDraw.Draw(sheet);f=ImageFont.truetype('arialbd.ttf',26)
for i,(p,l) in enumerate(zip(fs,labs)):
    im=Image.open(p).convert('RGB');im.thumbnail((W,W));x,y=(i%cols)*W,(i//cols)*W
    sheet.paste(im,(x+(W-im.width)//2,y+(W-im.height)//2));d.rectangle([x,y,x+len(l)*17+12,y+34],fill='black');d.text((x+6,y+3),l,fill='yellow',font=f)
sheet.save(out,quality=90)
