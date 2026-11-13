from pathlib import Path
import subprocess,json,hashlib,re,math
from PIL import Image,ImageDraw
E=Path(__file__).resolve().parent;R=E.parents[1];V=R/'output/qianwen-go-full-v9-r3b.mp4';OLD=R/'output/qianwen-go-full-v9-r2.mp4';F='/Users/USER/.local/bin/ffmpeg'
def run(a):return subprocess.run(a,capture_output=True,check=True)
def rec(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta=json.loads(run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(V)]).stdout);(E/'metadata.json').write_text(json.dumps(meta,indent=2))
d=run([F,'-hide_banner','-v','info','-xerror','-i',str(V),'-map','0:v:0','-vf','showinfo','-an','-f','null','-']);(E/'decode.log').write_bytes(d.stderr);pts=[float(x) for x in re.findall(rb'\bn:\s*\d+\s+pts:\s*\d+\s+pts_time:([0-9.]+)',d.stderr)]
ticks=[int(x) for x in re.findall(rb'\bn:\s*\d+\s+pts:\s*(\d+)',d.stderr)]
assert len(ticks)==6122 and len(set(b-a for a,b in zip(ticks,ticks[1:])))==1
def aachash(p):return hashlib.sha256(run([F,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-']).stdout).hexdigest()
ah=aachash(V);oldah=aachash(OLD)
source={}
for f in ['CostScene.tsx','Entry.tsx','captions.json']:source[f]=(R/'project/src/v9r2'/f).read_bytes()==(R/'project/src/v9r3b'/f).read_bytes()
s1=(R/'project/src/v9r2/Film.tsx').read_text();s2=(R/'project/src/v9r3b/Film.tsx').read_text();source['Film.tsx_only_portrait_asset_path']=s1.replace('staticFile(`v9/${name}.mp4`)','staticFile(`${name===\'intro\'?\'v9\':\'v9r3-final\'}/${name}.mp4`)')==s2
qa={'video':rec(V),'decodedFrames':len(pts),'firstPTS':pts[0],'lastPTS':pts[-1],'maxPrintedPTSError':max(abs(t-i/60) for i,t in enumerate(pts)),'ptsTickDelta':sorted(set(b-a for a,b in zip(ticks,ticks[1:]))),'decodeExit':0,'audioAACPayloadIdentical':ah==oldah,'audioAACSHA256':ah,'sourcePreservation':source,'oldVersion':rec(OLD),'rawVoice':rec(R/'project/public/voice.wav'),'scope':'technical checks only, no direct listening or continuous audiovisual review'}
assert len(pts)==6122 and ah==oldah and all(source.values());(E/'technical-qa.json').write_text(json.dumps(qa,indent=2));print('TECHNICAL PASS',flush=True)
groups={'native-keys':[1499,4840,6021],'portrait-sampled':list(range(1407,1714,12))+list(range(4762,5030,12))+list(range(5776,6122,12)), 'glasses-bridge-contiguous':list(range(1487,1512)), 'glasses-chair-close-contiguous':list(range(6003,6040)), 'hand-close-contiguous':list(range(5850,5893)), 'context-seams':sorted(set([66,2400,3946,4474,5200]+sum([[f-1,f,f+1] for f in [1407,1714,4762,5030,5776]],[])))}
ids=sorted(set(sum(groups.values(),[])));folder=E/'final-frames';folder.mkdir(exist_ok=True)
flt='select='+ '+'.join('eq(n\\,%d)'%i for i in ids)
run([F,'-v','error','-n','-i',str(V),'-vf',flt,'-fps_mode','vfr',str(folder/'seq-%04d.png')])
files=sorted(folder.glob('seq-*.png'));assert len(files)==len(ids)
for f,p in zip(ids,files):p.rename(folder/f'f{f:04d}.png')
boards=[]
for name,frames in groups.items():
 for k in range(0,len(frames),12):
  chunk=frames[k:k+12];portrait=name!='context-seams';cw,ch=(300,540) if portrait else (270,480);im=Image.new('RGB',(cw*4,(ch+24)*math.ceil(len(chunk)/4)),'#253035');dr=ImageDraw.Draw(im)
  for j,f in enumerate(chunk):
   src=Image.open(folder/f'f{f:04d}.png');src=src.crop((105,480,605,1369)) if 1407<=f<1714 and portrait else (src.crop((270,460 if f>=5776 else 480,810,1420 if f>=5776 else 1440)) if portrait else src)
   src.thumbnail((cw,ch));x=j%4*cw;y=j//4*(ch+24);im.paste(src,(x,y));dr.text((x+4,y+ch+3),f'f{f} {f/60:.4f}s',fill='white')
  dest=E/f'{name}-{k//12+1:02d}.jpg';im.save(dest,quality=94);boards.append(str(dest))
(E/'frame-index.json').write_text(json.dumps({'video':rec(V),'groups':groups,'uniqueFrames':len(ids),'omitted':6122-len(ids),'boards':boards,'scope':'generated evidence; viewing recorded separately'},indent=2));print('FRAMES',len(ids),len(boards),flush=True)
