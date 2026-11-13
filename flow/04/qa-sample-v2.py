from pathlib import Path
import subprocess,hashlib,json,re,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v2';O=R/'output/sample-motion-v2.mp4';F='/Users/USER/.local/bin/ffmpeg';old=R/'output/sample-motion-v1.mp4'
with (E/'full-decode.log').open('w') as l:q=subprocess.run([F,'-hide_banner','-i',str(O),'-vf','showinfo','-af','ebur128=peak=true','-f','null','-'],stderr=l,stdout=subprocess.DEVNULL)
log=(E/'full-decode.log').read_text();pts=[float(x) for x in re.findall(r'\bn:\s*\d+\s+pts:.*?pts_time:([\d.]+)',log)];assert q.returncode==0 and len(pts)==1308 and all(b>a for a,b in zip(pts,pts[1:]))
m=subprocess.run([F,'-hide_banner','-i',str(O),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=json.loads(m.stderr[m.stderr.rfind('{'):])
def pcm(p):return subprocess.run([F,'-v','error','-i',str(p),'-vn','-f','f32le','-'],capture_output=True,check=True).stdout
v1=pcm(old);v2=pcm(O);assert v1==v2
meta=subprocess.run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe','-v','error','-show_format','-show_streams','-of','json',str(O)],capture_output=True,text=True,check=True);(E/'metadata.json').write_text(meta.stdout)
qa={'duration':21.8,'frames':1308,'fps':60,'width':1080,'height':1920,'decode_exit':q.returncode,'monotonic_pts':True,'max_frame_gap':max(np.diff(pts)),'native_loudness_lufs':float(m['input_i']),'native_true_peak_dbtp':float(m['input_tp']),'audio_decoded_pcm_identical_to_v1':True,'audio_pcm_sha256':hashlib.sha256(v2).hexdigest(),'sha256':hashlib.sha256(O.read_bytes()).hexdigest(),'bytes':O.stat().st_size,'direct_audio_listening':False,'continuous_realtime_av_review':False}
(E/'qa.json').write_text(json.dumps(qa,indent=2))
D=E/'frames';D.mkdir(exist_ok=True);subprocess.run([F,'-v','error','-i',str(O),'-vf','select=not(mod(n\\,60)),scale=360:640','-vsync','0','-q:v','3',str(D/'f-%03d.jpg')],check=True)
fs=sorted(D.glob('f-*.jpg'))
for n in range(math.ceil(len(fs)/6)):
 im=Image.new('RGB',(1080,1340),'#d7d8d5');d=ImageDraw.Draw(im)
 for j,f in enumerate(fs[n*6:(n+1)*6]):
  x=j%3*360;y=j//3*670;im.paste(Image.open(f),(x,y+30));d.text((x+5,y+8),f'{n*6+j}s',fill='black')
 im.save(E/f'contact-{n}.jpg')
native=[0,2.3,4.8,6.9,9.8,11.5,13.9,15.8,17.9,20.5,21.75]
for t in native:subprocess.run([F,'-v','error','-ss',str(t),'-i',str(O),'-frames:v','1',str(E/f'native-{t}.png')],check=True)
windows=[(144,30),(384,42),(474,42),(792,54),(864,72),(1026,54)]
for n,(start,count) in enumerate(windows):
 d=E/f'dense-{n}';d.mkdir(exist_ok=True);subprocess.run([F,'-v','error','-ss',str(start/60),'-i',str(O),'-frames:v',str(count),'-vf','scale=270:480','-q:v','3',str(d/'f-%03d.jpg')],check=True);fs=sorted(d.glob('f-*.jpg'));assert len(fs)==count
 for b in range(math.ceil(count/12)):
  im=Image.new('RGB',(1080,1530),'#d7d8d5');dr=ImageDraw.Draw(im)
  for j,f in enumerate(fs[b*12:(b+1)*12]):
   x=j%4*270;y=j//4*510;im.paste(Image.open(f),(x,y+30));dr.text((x+4,y+7),f'{(start+b*12+j)/60:.3f}',fill='black')
  im.save(E/f'dense-{n}-contact-{b}.jpg')
for t in [2.3,11.5,20.5]:
 f=E/f'baseline-{t}.png';subprocess.run([F,'-v','error','-ss',str(t),'-i',str(old),'-frames:v','1',str(f)],check=True)
 im=Image.new('RGB',(1080,1005),'#122D3B');dr=ImageDraw.Draw(im)
 for j,p in enumerate([f,E/f'native-{t}.png']):im.paste(Image.open(p).resize((540,960)),(540*j,45));dr.text((540*j+20,16),f'v{j+1} / {t}s',fill='white')
 im.save(E/f'pair-{t}.jpg')
(E/'read-scope.json').write_text(json.dumps({'whole_sample_frames':22,'native_times':native,'dense_windows':[{'start':s,'frames':n,'fps':60} for s,n in windows],'dense_total':sum(n for s,n in windows),'assistant_viewed':False,'limits':'sampled and window frames, not all1308 final frames or realtime AV review'},indent=2))
print(json.dumps(qa))
