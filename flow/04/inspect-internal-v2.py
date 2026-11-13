from pathlib import Path
import subprocess,math,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v2';D=E/'internal-frames';D.mkdir(exist_ok=True)
subprocess.run(['/Users/USER/.local/bin/ffmpeg','-v','error','-i',str(E/'internal-test-final-3to7.mp4'),'-vf','scale=180:320','-vsync','0','-q:v','3',str(D/'f-%03d.jpg')],check=True)
fs=sorted(D.glob('f-*.jpg'));assert len(fs)==240
for n in range(10):
 im=Image.new('RGB',(1080,1400),'#d7d8d5');d=ImageDraw.Draw(im)
 for j,f in enumerate(fs[n*24:(n+1)*24]):
  x=j%6*180;y=j//6*350;im.paste(Image.open(f),(x,y+30));d.text((x+4,y+5),f'{3+(n*24+j)/60:.3f}',fill='black')
 im.save(E/f'internal-contact-{n}.jpg')
(E/'internal-read-scope.json').write_text(json.dumps({'source':'internal-test-final-3to7.mp4','source_sample_interval':[3,7],'frames':240,'fps':60,'all_frames_extracted':True,'assistant_viewed':False,'limitations':'contact sheets, not continuous real-time playback or audio'},indent=2))
