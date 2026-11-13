from pathlib import Path
import subprocess,json,os
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v2';F='/Users/USER/.local/bin/ffmpeg'
base=E/'pre-label-fix/sample-motion-v2.mp4';patch=E/'label-patch.mp4';out=E/'sample-v2-patched.mp4'
cmd=[F,'-v','error','-i',str(base),'-i',str(patch),'-filter_complex','[0:v]split=2[a][b];[a]trim=end_frame=132,setpts=PTS-STARTPTS[a0];[1:v]setpts=PTS-STARTPTS[p];[b]trim=start_frame=180,setpts=PTS-STARTPTS[b0];[a0][p][b0]concat=n=3:v=1:a=0[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-r','60','-c:a','copy','-movflags','+faststart',str(out)]
(E/'patch-command.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2));subprocess.run(cmd,check=True);os.replace(out,R/'output/sample-motion-v2.mp4')
# Reuse quality-only section, no overwrite of baseline visual evidence.
s=(R/'qa-sample-v2.py').read_text().split("D=E/'frames'")[0];exec(compile(s,str(R/'qa-sample-v2.py'),'exec'))
from PIL import Image,ImageDraw
D=E/'patched-frames';D.mkdir(exist_ok=True)
subprocess.run([F,'-v','error','-ss','2.1','-i',str(R/'output/sample-motion-v2.mp4'),'-frames:v','60','-vf','scale=270:480','-q:v','3',str(D/'f-%03d.jpg')],check=True)
fs=sorted(D.glob('f-*.jpg'));assert len(fs)==60
for b in range(5):
 im=Image.new('RGB',(1080,1530),'#d7d8d5');dr=ImageDraw.Draw(im)
 for j,f in enumerate(fs[b*12:(b+1)*12]):
  x=j%4*270;y=j//4*510;im.paste(Image.open(f),(x,y+30));dr.text((x+4,y+7),f'{2.1+(b*12+j)/60:.3f}',fill='black')
 im.save(E/f'patched-contact-{b}.jpg')
print(json.dumps(qa))
