import pathlib,subprocess,json,hashlib,re,os,wave
import numpy as np
from PIL import Image,ImageDraw
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];V=R/'output/sample-motion-v8.1.mp4';F='/Users/USER/.local/bin/ffmpeg'
def run(args): return subprocess.run(args,capture_output=True,check=True)
def rec(p): return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta=json.loads(run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(V)]).stdout)
(E/'avfoundation-metadata.json').write_text(json.dumps(meta,indent=2))
d=run([F,'-hide_banner','-v','info','-xerror','-i',str(V),'-map','0:v:0','-vf','showinfo','-an','-f','null','-'])
(E/'decode-showinfo.log').write_bytes(d.stderr)
pts=[float(x) for x in re.findall(rb'\bn:\s*\d+\s+pts:\s*\d+\s+pts_time:([0-9.]+)',d.stderr)]
a=run([F,'-v','error','-xerror','-i',str(V),'-map','0:a:0','-f','f32le','-ar','48000','-ac','1','-']).stdout
orig=run([F,'-v','error','-i',str(E.parent/'sample-v8/source-voice.wav'),'-f','f32le','-ar','48000','-ac','1','-']).stdout
x=np.frombuffer(orig,dtype='<f4');y=np.frombuffer(a,dtype='<f4');n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1])
lags=range(-48,49);s=slice(4800,min(n,48000*5));scores=[float(np.dot(x[s],y[4800+k:s.stop+k])) for k in lags];lag=list(lags)[int(np.argmax(scores))]
qa={'video':rec(V),'metadataProvider':'existing AVFoundation adapter; ffprobe incompatible CPU; frame count and PTS independently decoded by FFmpeg','decodeExit':d.returncode,'decodedFrames':len(pts),'firstPTS':pts[0],'lastPTS':pts[-1],'maxPTSErrorSeconds':max(abs(t-i/60) for i,t in enumerate(pts)),'audio':{'sourceSamples':len(x),'decodedSamples':len(y),'commonSamples':n,'correlationAtZeroLag':corr,'bestLagWithinOneMsSamples':lag,'peak':float(np.max(np.abs(y))),'directListening':False},'scope':'machine metadata/decode/audio-signal verification only'}
(E/'technical-qa.json').write_text(json.dumps(qa,indent=2))
frames=E/'final-frames';frames.mkdir(exist_ok=True)
# Native frame numbers ensure exact timestamps, no fps filter rounding.
indices=sorted(set(range(0,816,6))|{815}|set(range(216,256))|set(range(342,391))|set(range(528,595))|set(range(696,763)))
flt='select='+ '+'.join('eq(n\\,%d)'%i for i in indices)
run([F,'-v','error','-n','-i',str(V),'-vf',flt+',scale=270:480','-fps_mode','vfr','-q:v','2',str(frames/'small-%04d.jpg')])
small=list(sorted(frames.glob('small-*.jpg')));assert len(small)==len(indices)
index={f:{'path':str(p),'frame':f,'timeSeconds':f/60} for f,p in zip(indices,small)}
groups={'overview':list(range(0,816,6))+[815],'dock-dense':list(range(216,256)),'gather-dense':list(range(342,391)),'handoff-dense':list(range(528,595)),'toggle-dense':list(range(696,763))}
for name,ids in groups.items():
 for k in range(0,len(ids),24):
  chunk=ids[k:k+24];im=Image.new('RGB',(1080,6*510),'#1c2324');draw=ImageDraw.Draw(im)
  for j,f in enumerate(chunk):
   x0=j%4*270;y0=j//4*510;im.paste(Image.open(index[f]['path']),(x0,y0));draw.text((x0+6,y0+484),f'f{f} / {f/60:.4f}s',fill='white')
  im.save(E/f'{name}-{k//24+1:02}.jpg',quality=90)
keys=[0,111,234,330,342,354,360,365,366,378,390,528,534,540,546,552,558,561,579,708,723,744,759,815]
for f in keys:
 p=frames/f'native-f{f:03}.png';run([F,'-v','error','-n','-i',str(V),'-vf',f'select=eq(n\\,{f})','-frames:v','1',str(p)])
(E/'frame-index.json').write_text(json.dumps({'video':rec(V),'sampledUniqueFrames':len(indices),'omittedFrames':816-len(indices),'groups':groups,'frames':list(index.values()),'nativeKeyFrames':keys},indent=2))
print(json.dumps(qa,indent=2));print('Extracted',len(indices),'unique frames; boards and native keys ready')
