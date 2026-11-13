from pathlib import Path
import subprocess,json,hashlib,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v3';F='/Users/USER/.local/bin/ffmpeg'
O=R/'output/sample-motion-v3.mp4'
def run(args): subprocess.run([F,'-v','error',*map(str,args)],check=True)
def contacts(files,prefix,start=0,step=1,cols=4,rows=3,w=270,h=480):
 for b in range(math.ceil(len(files)/(cols*rows))):
  im=Image.new('RGB',(cols*w,rows*(h+30)),'#d7d8d5');d=ImageDraw.Draw(im)
  for j,f in enumerate(files[b*cols*rows:(b+1)*cols*rows]):
   x=j%cols*w;y=j//cols*(h+30);im.paste(Image.open(f).resize((w,h)),(x,y+30));d.text((x+4,y+6),f'{start+(b*cols*rows+j)*step:.3f}s',fill='black')
  im.save(E/f'{prefix}-{b}.jpg')
if __name__=='__main__':
 import sys
 if sys.argv[1]=='internal':
  D=E/'internal-frames';D.mkdir(exist_ok=True)
  run(['-i',E/'internal-test-fixed-8.4to12.4.mp4','-vf','fps=15,scale=270:480','-q:v','3',D/'f-%03d.jpg'])
  fs=sorted(D.glob('*.jpg'));assert len(fs)==60;contacts(fs,'internal-contact',8.4,1/15)
 elif sys.argv[1]=='final':
  assert not O.exists()
  cmd=[F,'-v','error','-i',str(R/'output/sample-motion-v2.mp4'),'-i',str(E/'tail-8to21.8.mp4'),'-filter_complex','[0:v]trim=end_frame=480,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-r','60','-c:a','copy','-movflags','+faststart',str(O)]
  (E/'mux-command.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2));subprocess.run(cmd,check=True)
  s=(R/'qa-sample-v2.py').read_text().split("D=E/'frames'")[0].replace("evidence/sample-v2","evidence/sample-v3").replace("output/sample-motion-v2.mp4","output/sample-motion-v3.mp4")
  exec(compile(s,str(R/'qa-sample-v2.py'),'exec'))
  D=E/'frames';D.mkdir(exist_ok=True);run(['-i',O,'-vf','select=not(mod(n\\,60)),scale=360:640','-vsync','0','-q:v','3',D/'f-%03d.jpg']);contacts(sorted(D.glob('*.jpg')),'contact',0,1,3,2,360,640)
  native=[2.3,8,8.8,9.6,11.5,12.1,13.8,15.5,17.6,18.5,20.5,20.9,21.75]
  for t in native:run(['-ss',t,'-i',O,'-frames:v','1',E/f'native-{t}.png'])
  windows=[(474,54),(570,36),(714,30),(822,30),(1026,48),(1146,18)]
  for n,(start,count) in enumerate(windows):
   D=E/f'dense-{n}';D.mkdir(exist_ok=True);run(['-ss',start/60,'-i',O,'-frames:v',count,'-vf','scale=270:480','-q:v','3',D/'f-%03d.jpg']);fs=sorted(D.glob('*.jpg'));assert len(fs)==count;contacts(fs,f'dense-{n}-contact',start/60,1/60)
  for t in [2.3,11.5,20.5]:
   f=E/f'baseline-{t}.png';run(['-ss',t,'-i',R/'output/sample-motion-v2.mp4','-frames:v','1',f]);im=Image.new('RGB',(1080,1005),'#122D3B');d=ImageDraw.Draw(im)
   for j,p in enumerate([f,E/f'native-{t}.png']):im.paste(Image.open(p).resize((540,960)),(j*540,45));d.text((j*540+20,16),f'v{j+2} / {t}s',fill='white')
   im.save(E/f'pair-{t}.jpg')
  D=E/'tail-all-frames';D.mkdir(exist_ok=True)
  run(['-ss','8','-i',O,'-frames:v','828','-q:v','3',D/'f-%04d.jpg'])
  fs=sorted(D.glob('*.jpg'));assert len(fs)==828;contacts(fs,'tail-all-contact',8,1/60,6,4,180,320)
  (E/'read-scope.json').write_text(json.dumps({'whole_sample_frames':22,'native_times':native,'dense_windows':[{'start_frame':s,'frames':n,'fps':60} for s,n in windows],'dense_total':sum(n for s,n in windows),'tail_all_frames':{'start_seconds':8,'last_frame_seconds':1307/60,'count':828,'fps':60,'native_jpeg_directory':str(D),'contact_sheets':35},'assistant_viewed':False,'limits':'full tail-frame evidence supplied; actual viewed scope must be recorded separately; not realtime audiovisual review'},indent=2))
  print(json.dumps(qa))
