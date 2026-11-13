from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,math
E=Path(__file__).resolve().parent;V=E.parents[1]/'output/qianwen-go-full-v9-r2.mp4';D=E/'motion-detail-frames';D.mkdir(exist_ok=True);groups={'tools':list(range(720,991,6)),'conditions':list(range(3138,3331,6))};ids=sorted(set(sum(groups.values(),[])));flt='select='+'+'.join('eq(n\\,%d)'%f for f in ids)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-v','error','-n','-i',str(V),'-vf',flt+',scale=270:480','-fps_mode','vfr','-q:v','2',str(D/'f-%03d.jpg')],check=True)
files=sorted(D.glob('f-*.jpg'));assert len(files)==len(ids);index=dict(zip(ids,files));boards=[]
for name,seq in groups.items():
 for k in range(0,len(seq),24):
  chunk=seq[k:k+24];im=Image.new('RGB',(1080,math.ceil(len(chunk)/4)*510),'#1c2324');d=ImageDraw.Draw(im)
  for j,f in enumerate(chunk):
   x=j%4*270;y=j//4*510;im.paste(Image.open(index[f]),(x,y));d.text((x+5,y+485),f'f{f} {f/60:.2f}s',fill='white')
  p=E/f'motion-{name}-{k//24+1:02}.jpg';im.save(p,quality=95);boards.append(str(p))
(E/'motion-detail-index.json').write_text(json.dumps({'frames':ids,'groups':groups,'boards':boards},indent=2));print('Created',len(ids),'frames')
