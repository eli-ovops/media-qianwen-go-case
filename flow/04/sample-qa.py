from pathlib import Path
import json,subprocess,re,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v1';E.mkdir(exist_ok=True);F='/Users/USER/.local/bin/ffmpeg';O=R/'output/sample-motion-v1.mp4'
with (E/'full-decode.log').open('w') as l:q=subprocess.run([F,'-hide_banner','-i',str(O),'-vf','showinfo','-af','ebur128=peak=true','-f','null','-'],stderr=l,stdout=subprocess.DEVNULL)
log=(E/'full-decode.log').read_text();pts=[float(x) for x in re.findall(r'\bn:\s*\d+\s+pts:.*?pts_time:([\d.]+)',log)];assert q.returncode==0 and len(pts)==1308 and all(b>a for a,b in zip(pts,pts[1:]))
measure=subprocess.run([F,'-hide_banner','-i',str(O),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=json.loads(measure.stderr[measure.stderr.rfind('{'):])
def pcm(p):return np.frombuffer(subprocess.run([F,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','-'],capture_output=True,check=True).stdout,dtype='<f4')
a=pcm(O);ref=pcm(R/'project/public/voice.wav')[round(3454/60*48000):round(4762/60*48000)];n=min(len(a),len(ref));co=[]
for x in range(0,n-48000,48000):co.append(float(np.corrcoef(a[x:x+48000],ref[x:x+48000])[0,1]))
meta=subprocess.run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe','-v','error','-show_format','-show_streams','-of','json',str(O)],capture_output=True,text=True,check=True);(E/'metadata.json').write_text(meta.stdout)
qa={'frames':len(pts),'fps':60,'duration':21.8,'decode_exit':q.returncode,'monotonic_pts':True,'pts_first_last':[pts[0],pts[-1]],'max_frame_gap':float(max(np.diff(pts))),'native_loudness_lufs':float(m['input_i']),'native_true_peak_dbtp':float(m['input_tp']),'lra_lu':float(m['input_lra']),'one_second_audio_correlation':co,'minimum_correlation':min(co),'mono_downmix_clipped_samples':int(np.sum(np.abs(a)>=1)),'sha256':hashlib.sha256(O.read_bytes()).hexdigest(),'bytes':O.stat().st_size,'direct_audio_listening':False,'subtitle_sync':'43-group full-source mapping subset, ASR sentence timings/manual subdivisions; not word-perfect listening','no_source_video_pixels':True}
(E/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
D=E/'frames';D.mkdir(exist_ok=True)
subprocess.run([F,'-v','error','-i',str(O),'-vf','select=not(mod(n\\,60)),scale=540:960','-vsync','0','-q:v','3',str(D/'f-%03d.jpg')],check=True)
fs=sorted(D.glob('f-*.jpg'))
for b in range(math.ceil(len(fs)/6)):
 im=Image.new('RGB',(1080,1340),'#ddd');dr=ImageDraw.Draw(im)
 for i,p in enumerate(fs[b*6:(b+1)*6]):
  x=i%3*360;y=i//3*670;im.paste(Image.open(p).resize((360,640)),(x,y+30));dr.text((x+5,y+8),f'sample {b*6+i}s',fill='black')
 im.save(E/f'contact-{b}.jpg')
for t in [.1,4.5,8.6,13,17.8,20.5,21.75]:
 subprocess.run([F,'-v','error','-ss',str(t),'-i',str(O),'-frames:v','1',str(E/f'native-{t}.png')],check=True)
windows=[(240,48),(474,90),(1014,48)]
for j,(start,count) in enumerate(windows):
 d=E/f'dense-{j}';d.mkdir(exist_ok=True)
 subprocess.run([F,'-v','error','-ss',str(start/60),'-i',str(O),'-frames:v',str(count),'-vf','scale=270:480','-q:v','3',str(d/'f-%03d.jpg')],check=True);fs=sorted(d.glob('f-*.jpg'));assert len(fs)==count
 for b in range(math.ceil(count/12)):
  im=Image.new('RGB',(1080,1530),'#ddd');dr=ImageDraw.Draw(im)
  for k,p in enumerate(fs[b*12:(b+1)*12]):
   x=k%4*270;y=k//4*510;im.paste(Image.open(p),(x,y+30));dr.text((x+4,y+6),f'{(start+b*12+k)/60:.3f}s',fill='black')
  im.save(E/f'dense-{j}-contact-{b}.jpg')
(E/'read-scope.json').write_text(json.dumps({'whole_sample_frames':22,'sampling':'exact every60th frame;0–21s','native_times':[.1,4.5,8.6,13,17.8,20.5,21.75],'dense_windows':[{'start_frame':s,'frames':n,'fps':60} for s,n in windows],'dense_total':sum(n for s,n in windows),'assistant_viewed':False,'limits':'sampled pixels and all186 dense frames, not real-time full audiovisual playback'},ensure_ascii=False,indent=2))
print(json.dumps(qa,ensure_ascii=False))
