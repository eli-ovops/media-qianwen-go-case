from pathlib import Path
import subprocess,json,re,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;O=R/'output/candidate-v1.mp4';E=R/'evidence/final-verified';E.mkdir(exist_ok=True);F='/Users/USER/.local/bin/ffmpeg';A='/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe'
assert O.is_file()
meta=subprocess.run([A,'-v','error','-show_format','-show_streams','-of','json',str(O)],capture_output=True,text=True,check=True)
(E/'metadata-v1.json').write_text(meta.stdout)
with (E/'full-decode-v1.log').open('w') as log:
 q=subprocess.run([F,'-hide_banner','-i',str(O),'-vf','showinfo','-af','ebur128=peak=true','-f','null','-'],stdout=subprocess.DEVNULL,stderr=log)
assert q.returncode==0
log=(E/'full-decode-v1.log').read_text();pts=[float(x) for x in re.findall(r'\bn:\s*\d+\s+pts:.*?pts_time:([\d.]+)',log)]
assert len(pts)>6000 and all(b>a for a,b in zip(pts,pts[1:]))
def audio(path):
 p=subprocess.run([F,'-v','error','-i',str(path),'-vn','-ac','1','-ar','48000','-f','f32le','-'],capture_output=True,check=True);return np.frombuffer(p.stdout,dtype='<f4')
ref=audio(R/'project/public/voice.wav');a=audio(O);n=min(len(a),len(ref));a=a[:n];ref=ref[:n]
corr=[]
for st in range(0,n-48000,48000):
 x=ref[st:st+48000];y=a[st:st+48000];corr.append(float(np.corrcoef(x,y)[0,1]))
metrics={'decode_exit':q.returncode,'frames':len(pts),'first_pts':pts[0],'last_pts':pts[-1],'monotonic_pts':True,'max_frame_gap':max(np.diff(pts)),'reference_audio_samples':len(ref),'decoded_audio_samples_compared':n,'one_second_correlations':corr,'min_correlation':min(corr),'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(a*a)))),'peak_dbfs':float(20*np.log10(np.max(np.abs(a)))),'clipped_samples':int(np.sum(np.abs(a)>=1)),'loudness_summary':log[log.rfind('Summary:'):],'sha256':hashlib.sha256(O.read_bytes()).hexdigest(),'bytes':O.stat().st_size,'direct_listening':False,'caption_sync':'ASR sentence timing with manual subdivisions; not word-perfect audition','lip_sync':'not applicable; no human video frames used'}

measure=subprocess.run([F,'-hide_banner','-i',str(O),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
lm=json.loads(measure.stderr[measure.stderr.rfind('{'):]);metrics['native_loudness']={'integrated_lufs':float(lm['input_i']),'true_peak_dbtp':float(lm['input_tp']),'lra_lu':float(lm['input_lra']),'method':'FFmpeg loudnorm measurement on native output channels; no rewrite'}
metrics['peak_dbfs_scope']='decoded 48kHz mono downmix used for correlation; differs from native stereo per-channel true peak'
metrics['native_audio_layout']='stereo' if re.search(r'Audio:.*stereo',log) else 'UNKNOWN'

(E/'qa-v1.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
# Full-film sampling, original exports at 2s; each image named and traceable.
D=E/'final-frames';D.mkdir(exist_ok=True)
subprocess.run([F,'-v','error','-i',str(O),'-vf','select=not(mod(n\\,120)),scale=540:960','-vsync','0','-q:v','3',str(D/'frame-%03d.jpg')],check=True)
files=sorted(D.glob('frame-*.jpg'))
for batch in range(math.ceil(len(files)/6)):
 fs=files[batch*6:(batch+1)*6];im=Image.new('RGB',(1080,1340),'#ddd');dr=ImageDraw.Draw(im)
 for i,p in enumerate(fs):
  idx=files.index(p);x=(i%3)*360;y=(i//3)*670;im.paste(Image.open(p).resize((360,640)),(x,y+30));dr.text((x+8,y+8),f'frame {idx*120}; {idx*2}s',fill='black')
 im.save(E/f'final-contact-{batch:02}.jpg')
# Native emphasis frames and dense 60fps transition windows.
for t in [2.7,17,50.8,56,64.9,70,75.5,78.5,89.5,100.5]:
 subprocess.run([F,'-v','error','-ss',str(t),'-i',str(O),'-frames:v','1',str(E/f'final-native-{t}.png')],check=True)
windows=[(35.95,108),(65.45,90),(79.0,90),(94.25,90)]
for j,(start,count) in enumerate(windows):
 d=E/f'transition-{j}';d.mkdir(exist_ok=True)
 subprocess.run([F,'-v','error','-ss',str(start),'-i',str(O),'-frames:v',str(count),'-vf','scale=270:480','-q:v','3',str(d/'f-%03d.jpg')],check=True)
 fs=sorted(d.glob('f-*.jpg'));assert len(fs)==count
 for batch in range(math.ceil(count/12)):
  im=Image.new('RGB',(1080,1530),'#ddd');dr=ImageDraw.Draw(im)
  for k,p in enumerate(fs[batch*12:(batch+1)*12]):
   x=k%4*270;y=k//4*510;im.paste(Image.open(p),(x,y+30));dr.text((x+5,y+6),f'{start+(batch*12+k)/60:.3f}s',fill='black')
  im.save(E/f'transition-{j}-contact-{batch}.jpg')
(E/'frame-read-scope.json').write_text(json.dumps({'whole_film_sampling':{'files':len(files),'filter':'select every120th frame','limits':'one exact decoded frame per2sec; inspect native exact requests separately'},'native_times':[2.7,17,50.8,56,64.9,70,75.5,78.5,89.5,100.5],'dense_windows':[{'start':x,'frames':n,'fps':60} for x,n in windows],'viewed_by_assistant':False,'remaining_frames':'outside378 dense frames and listed samples not individually viewed; no real-time full audiovisual viewing'},ensure_ascii=False,indent=2))
print(json.dumps({k:metrics[k] for k in ['frames','min_correlation','peak_dbfs','clipped_samples','sha256','bytes']}))
