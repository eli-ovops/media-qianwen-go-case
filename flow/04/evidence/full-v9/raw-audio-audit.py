import pathlib,json,subprocess,numpy as np,hashlib
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];F='/Users/USER/.local/bin/ffmpeg'
def pcm(p,flt=None):
 cmd=[F,'-v','error','-i',str(p)];cmd+=['-af',flt] if flt else [];cmd+=['-ar','48000','-ac','1','-f','f32le','-'];return np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,dtype='<f4')
x=pcm(R/'project/public/voice.wav');timeline=json.loads((R/'project/src/timeline.json').read_text());rows=[]
for src in timeline['sources']:
 for seg in src['segments']:
  original=pcm(src['path'],f"atrim=start={seg['source_start']}:end={seg['source_end']},asetpts=PTS-STARTPTS,volume={src['gain_db']}dB")
  a=round(seg['output_start']*48000);n=min(len(original),round((seg['output_end']-seg['output_start'])*48000),len(x)-a);q=original[960:n-960];y=x[a+960:a+n-960];rows.append({'source':src['index'],'sourceRange':[seg['source_start'],seg['source_end']],'outputRange':[seg['output_start'],seg['output_end']],'comparedSamples':len(q),'correlationAtMappedTime':float(np.corrcoef(q,y)[0,1]),'normalizedRMSError':float(np.sqrt(np.mean((q-y)**2))/np.sqrt(np.mean(q*q)))})
result={'scope':'Original source PCM compared with assembled voice at exact retained time ranges, excluding20ms per edge containing4ms fade. Signal identity and timing only; not direct listening/word transcription.','voiceSHA256':hashlib.sha256((R/'project/public/voice.wav').read_bytes()).hexdigest(),'checks':rows,'status':'PASS' if all(r['correlationAtMappedTime']>.999 for r in rows) else 'REVIEW'};(E/'raw-audio-audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
