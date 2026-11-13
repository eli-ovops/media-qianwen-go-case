from pathlib import Path
import json,subprocess,hashlib,wave,math,array
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'用户原片提交-20261013.json').read_text())
ff='/Users/USER/.local/bin/ffmpeg'; probe='/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe'
rows=[]
for i,src in enumerate(manifest['raw_media'],1):
 p=Path(src['path']); out=ROOT/'evidence-v3'/p.stem;out.mkdir(parents=True,exist_ok=False)
 row={'path':str(p),'directory':str(out),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 assert row['sha256']==src['sha256']
 r=subprocess.run([probe,str(p)],capture_output=True,text=True,check=True);(out/'metadata.json').write_text(r.stdout);row['metadata']=json.loads(r.stdout)
 subprocess.run([ff,'-nostdin','-hide_banner','-loglevel','error','-n','-i',str(p),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(out/'audio.wav')],check=True)
 with wave.open(str(out/'audio.wav')) as w:
  pcm=array.array('h',w.readframes(w.getnframes()));duration=len(pcm)/w.getframerate()
 rms=(sum(x*x for x in pcm)/len(pcm))**.5/32768
 peak=max(abs(x) for x in pcm)/32768
 row['audio']={'duration':duration,'rms_dbfs':20*math.log10(rms),'peak_dbfs':20*math.log10(peak),'clipped_samples':sum(abs(x)>=32767 for x in pcm),'samples':len(pcm),'rate':16000,'seconds_rms_dbfs':[round(20*math.log10(max(1e-9,(sum(x*x for x in pcm[n:n+16000])/len(pcm[n:n+16000]))**.5/32768)),2) for n in range(0,len(pcm),16000)]}
 row['samples']=[]
 for t in [round(duration*x,3) for x in [.02,.15,.3,.5,.7,.85,.97]]:
  image=out/f'frame-{t:08.3f}.jpg'
  subprocess.run([ff,'-nostdin','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=540:-2','-q:v','3',str(image)],check=True)
  row['samples'].append({'requested_seconds':t,'path':str(image),'read':False})
 rows.append(row);(ROOT/'evidence-v3/metadata-and-audio.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 print(json.dumps({'file':p.name,'duration':duration,'metadata':row['metadata'],'audio_rms_dbfs':row['audio']['rms_dbfs']},ensure_ascii=False),flush=True)
 with (out/'whisper.log').open('w') as log:
  subprocess.run(['/Volumes/EXTERNAL/Tools/Whisper/bin/whisper-cli','-m','/Volumes/EXTERNAL/Tools/Whisper/models/ggml-base.bin','-f',str(out/'audio.wav'),'-l','zh','-ml','40','-otxt','-osrt','-ovtt','-oj','-of',str(out/'transcript')],stdout=log,stderr=log,check=True)
 print('TRANSCRIBED '+p.name,flush=True)
print('DONE',flush=True)
