from pathlib import Path
import subprocess,json,math,sys
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v7';F='/Users/USER/.local/bin/ffmpeg';O=R/'output/sample-motion-v7.mp4'
def run(args):subprocess.run([F,'-v','error',*map(str,args)],check=True)
def sheets(files,prefix,times,w=180,h=320,cols=6,rows=4):
 for b in range(math.ceil(len(files)/(cols*rows))):
  im=Image.new('RGB',(cols*w,rows*(h+28)),'#D7DCD6');d=ImageDraw.Draw(im)
  for j,f in enumerate(files[b*cols*rows:(b+1)*cols*rows]):
   x=j%cols*w;y=j//cols*(h+28);im.paste(Image.open(f).resize((w,h)),(x,y+28));d.text((x+5,y+6),f'{times[b*cols*rows+j]:.3f}s',fill='black')
  im.save(E/f'{prefix}-{b:02d}.jpg')
if sys.argv[-1]=='trial':
 D=E/'trial-frames';D.mkdir(exist_ok=True);run(['-i',E/'trial-10to14.8.mp4','-q:v',3,D/'f-%04d.jpg']);fs=sorted(D.glob('*.jpg'));assert len(fs)==288;sheets(fs,'trial-contact',[10+i/60 for i in range(288)]);print('TRIAL_288_READY');sys.exit()
if sys.argv[-1]=='evidence':
 import hashlib
 qa=json.loads((E/'qa.json').read_text());assert hashlib.sha256(O.read_bytes()).hexdigest()==qa['sha256']
else:
 assert not O.exists()
 run(['-i',E/'full-muted.mp4','-i',R/'output/sample-motion-v6-final2.mp4','-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',O])
 s=(R/'qa-sample-v2.py').read_text().split("D=E/'frames'")[0].replace('evidence/sample-v2','evidence/sample-v7').replace('output/sample-motion-v2.mp4','output/sample-motion-v7.mp4');exec(compile(s,str(R/'qa-sample-v2.py'),'exec'))
meta=json.loads((E/'metadata.json').read_text());v=next(x for x in meta['streams'] if x['codec_type']=='video');num,den=map(float,v['avg_frame_rate'].split('/'));assert v['width']==1080 and v['height']==1920 and abs(num/den-60)<.001;assert abs(float(meta['format']['duration'])-21.8)<.05
D=E/'all-frames';D.mkdir(exist_ok=True);run(['-i',O,'-q:v',4,D/'f-%04d.jpg']);fs=sorted(D.glob('*.jpg'));assert len(fs)==1308
ids=list(range(0,1308,6));sheets([fs[i] for i in ids],'whole-10fps',[i/60 for i in ids])
windows=[(642,72),(1002,54),(1218,90)]
for w,(start,count) in enumerate(windows):sheets(fs[start:start+count],f'dense-{w}',[(start+i)/60 for i in range(count)])
native=[1.2,2.35,5.2,7.2,8.2,9.3,10.7,11.25,12.3,14.8,16.9,17.9,19.55,20.5,21.6]
for t in native:
 run(['-ss',t,'-i',O,'-frames:v',1,E/f'native-{t}.png'])
for t in [9.3,11.25,16.9,20.5]:
 run(['-ss',t,'-i',R/'output/sample-motion-v6-final2.mp4','-frames:v',1,E/f'v6-{t}.png'])
 im=Image.new('RGB',(1080,1004),'#12313A');d=ImageDraw.Draw(im)
 for j,f in enumerate([E/f'v6-{t}.png',E/f'native-{t}.png']):im.paste(Image.open(f).resize((540,960)),(j*540,44));d.text((j*540+20,15),f'v{6+j} / {t:.2f}s',fill='white')
 im.save(E/f'pair-{t}.jpg')
(E/'read-scope.json').write_text(json.dumps({'assistant_viewed':False,'generated_all_frames':1308,'whole_sample_10fps_frames':218,'dense_windows_frames':windows,'native_times':native,'direct_listening':False,'continuous_realtime_AV_review':False},indent=2))
print(json.dumps(qa))
