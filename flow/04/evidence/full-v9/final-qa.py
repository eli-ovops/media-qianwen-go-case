import pathlib,subprocess,json,hashlib,re,os,math
import numpy as np
from PIL import Image,ImageDraw
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];V=R/'output/qianwen-go-full-v9.mp4';F='/Users/USER/.local/bin/ffmpeg'
def run(args):return subprocess.run(args,capture_output=True,check=True)
def rec(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
meta=json.loads(run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(V)]).stdout);(E/'avfoundation-metadata.json').write_text(json.dumps(meta,indent=2))
d=run([F,'-hide_banner','-v','info','-xerror','-i',str(V),'-map','0:v:0','-vf','showinfo','-an','-f','null','-']);(E/'decode-showinfo.log').write_bytes(d.stderr)
pts=[float(x) for x in re.findall(rb'\bn:\s*\d+\s+pts:\s*\d+\s+pts_time:([0-9.]+)',d.stderr)]
def pcm(path):return np.frombuffer(run([F,'-v','error','-xerror','-i',str(path),'-map','0:a:0','-f','f32le','-ar','48000','-ac','1','-']).stdout,dtype='<f4')
x=pcm(R/'project/public/voice.wav');y=pcm(V);n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1]);sections=[]
for a,b in [(0,4.9),(4.9,28.57),(28.57,79.37),(79.37,102.02)]:
 aa=int(a*48000);bb=min(int(b*48000),n);sx=x[aa:bb];sy=y[aa:bb];lagbuf=range(-48,49);ss=aa+2400;ee=min(bb-2400,ss+96000);lag=list(lagbuf)[int(np.argmax([np.dot(x[ss:ee],y[ss+k:ee+k]) for k in lagbuf]))]
 r=run([F,'-hide_banner','-ss',str(a),'-t',str(b-a),'-i',str(V),'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-']);log=r.stderr.decode();(E/f'audio-section-{len(sections)+1}.log').write_text(log);stats=json.loads(re.search(r'\{\s*"input_i"[\s\S]+?\}',log).group())
 sections.append(dict(start=a,end=b,correlation=float(np.corrcoef(sx,sy)[0,1]),bestLagWithinOneMsSamples=lag,integratedLUFS=float(stats['input_i']),truePeakDBTP=float(stats['input_tp'])))
qa={'video':rec(V),'metadataProvider':'existing AVFoundation adapter; frame count and PTS independently decoded by FFmpeg','decodeExit':d.returncode,'decodedFrames':len(pts),'firstPTS':pts[0],'lastPTS':pts[-1],'maxPTSErrorSeconds':max(abs(t-i/60) for i,t in enumerate(pts)),'audio':{'source':rec(R/'project/public/voice.wav'),'sourceSamples':len(x),'decodedSamples':len(y),'commonSamples':n,'correlationAtZeroLag':corr,'samplePeakDBFS':20*math.log10(float(np.max(np.abs(y)))),'sections':sections,'loudnessRangeAcrossSectionsLU':max(s['integratedLUFS'] for s in sections)-min(s['integratedLUFS'] for s in sections),'directListening':False},'scope':'machine metadata/decode/audio-signal verification only'}
(E/'technical-qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2),flush=True)
frames=E/'final-frames';frames.mkdir(exist_ok=True)
groups={'overview':list(range(0,6122,60))+[6121],'portrait':sorted(set(sum([list(range(a,b,12)) for a,b in [(0,294),(1407,1714),(4762,5030),(5776,6122)]],[]))),'fees-reminder':list(range(3946,4762,6)), 'seams':sorted(set(sum([list(range(c-24,c+25,6)) for c in [294,1407,1714,3448,3946,4474,4762,5030,5776]],[]))),'condition-entries':sorted(set(sum([list(range(round(t*60)-12,round(t*60)+49,6)) for t in [36.39,39.55,40.83,42.91,48.59]],[])))}
indices=sorted(set(sum(groups.values(),[])));flt='select='+ '+'.join('eq(n\\,%d)'%i for i in indices)
run([F,'-v','error','-n','-i',str(V),'-vf',flt+',scale=270:480','-fps_mode','vfr','-q:v','2',str(frames/'small-%04d.jpg')]);small=sorted(frames.glob('small-*.jpg'));assert len(small)==len(indices)
index={f:{'path':str(p),'frame':f,'timeSeconds':f/60} for f,p in zip(indices,small)}
boards=[]
for name,ids in groups.items():
 for k in range(0,len(ids),24):
  chunk=ids[k:k+24];im=Image.new('RGB',(1080,math.ceil(len(chunk)/4)*510),'#1c2324');draw=ImageDraw.Draw(im)
  for j,f in enumerate(chunk):
   xx=j%4*270;yy=j//4*510;im.paste(Image.open(index[f]['path']),(xx,yy));draw.text((xx+6,yy+484),f'f{f} / {f/60:.4f}s',fill='white')
  dest=E/f'{name}-{k//24+1:02}.jpg';im.save(dest,quality=90);boards.append(str(dest))
caps=json.loads((R/'project/src/v9/captions.json').read_text());cueFrames=[round((c['start']+c['end'])/2*60) for c in caps]
keys=sorted(set(cueFrames+[0,293,1407,1713,3448,3946,4474,4762,5776,6121]))
for f in keys:
 p=frames/f'native-f{f:04}.png';run([F,'-v','error','-n','-ss',str(f/60),'-i',str(V),'-frames:v','1',str(p)])
for start in range(0,len(caps),12):
 chunk=caps[start:start+12];im=Image.new('RGB',(1080,len(chunk)*255),'#1c2324');dr=ImageDraw.Draw(im)
 for j,c in enumerate(chunk):
  f=cueFrames[start+j];im.paste(Image.open(frames/f'native-f{f:04}.png').crop((0,1550,1080,1780)),(0,j*255));dr.text((15,j*255+230),f'cue {c["id"]}  {c["start"]:.2f}-{c["end"]:.2f}s / f{f}',fill='white')
 im.save(E/f'caption-strip-{start//12+1:02}.jpg',quality=95)
(E/'frame-index.json').write_text(json.dumps({'video':rec(V),'sampledUniqueFrames':len(indices),'omittedFramesInSampling':6122-len(indices),'groups':groups,'frames':list(index.values()),'nativeKeyFrames':keys,'boards':boards,'scope':'Generated evidence; actual reviewed images recorded separately, not continuous video viewing'},indent=2))
print('Frames ready',len(indices),'boards',len(boards),flush=True)
