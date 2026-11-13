from pathlib import Path
import subprocess,json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v5';F='/Users/USER/.local/bin/ffmpeg';O=R/'output/sample-motion-v5.mp4'
def run(args):subprocess.run([F,'-v','error',*map(str,args)],check=True)
def contacts(files,prefix,start,cols=6,rows=4,w=180,h=320):
 for b in range(math.ceil(len(files)/(cols*rows))):
  im=Image.new('RGB',(cols*w,rows*(h+30)),'#d7d8d5');d=ImageDraw.Draw(im)
  for j,f in enumerate(files[b*cols*rows:(b+1)*cols*rows]):
   x=j%cols*w;y=j//cols*(h+30);im.paste(Image.open(f).resize((w,h)),(x,y+30));d.text((x+4,y+6),f'{start+(b*cols*rows+j)/60:.3f}s',fill='black')
  im.save(E/f'{prefix}-{b}.jpg')
if __name__=='__main__':
 assert not O.exists()
 cmd=[F,'-v','error','-i',str(R/'output/sample-motion-v4-final.mp4'),'-i',str(E/'tail-8to21.8.mp4'),'-filter_complex','[0:v]trim=end_frame=480,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-r','60','-c:a','copy','-movflags','+faststart',str(O)]
 (E/'mux-command.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2));subprocess.run(cmd,check=True)
 s=(R/'qa-sample-v2.py').read_text().split("D=E/'frames'")[0].replace('evidence/sample-v2','evidence/sample-v5').replace('output/sample-motion-v2.mp4','output/sample-motion-v5.mp4');exec(compile(s,str(R/'qa-sample-v2.py'),'exec'))
 D=E/'tail-all-frames';D.mkdir(exist_ok=True);run(['-ss',8,'-i',O,'-frames:v',828,'-q:v',3,D/'f-%04d.jpg']);fs=sorted(D.glob('*.jpg'));assert len(fs)==828;contacts(fs,'tail-all-contact',8)
 D=E/'seam-frames';D.mkdir(exist_ok=True);run(['-ss',7.9,'-i',O,'-frames:v',12,'-q:v',3,D/'f-%04d.jpg']);contacts(sorted(D.glob('*.jpg')),'seam',7.9,4,3,270,480)
 native=[8.1,9.2,9.8,10.7,11.5,12.6,13.2,14.2,15.4,16.7,17.3,17.8,18.4,19.1,19.6,20.2,20.7,21.2]
 for t in native:run(['-ss',t,'-i',O,'-frames:v',1,E/f'native-{t}.png'])
 for t in [9.8,15.4,19.6,21.2]:
  f=E/f'baseline-{t}.png';run(['-ss',t,'-i',R/'output/sample-motion-v4-final.mp4','-frames:v',1,f]);im=Image.new('RGB',(1080,1005),'#122D3B');d=ImageDraw.Draw(im)
  for j,p in enumerate([f,E/f'native-{t}.png']):im.paste(Image.open(p).resize((540,960)),(j*540,45));d.text((j*540+20,16),f'v{j+4} / {t}s',fill='white')
  im.save(E/f'pair-{t}.jpg')
 (E/'read-scope.json').write_text(json.dumps({'changed_interval':[8,21.8],'tail_frames':828,'contact_sheets':35,'contact_tile_pixels':[180,320],'native_times':native,'seam_interval':[7.9,8.0833333],'seam_frames':12,'assistant_viewed':False,'direct_listening':False,'realtime_continuous_av_review':False},indent=2))
 print(json.dumps(qa))
