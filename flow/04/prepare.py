from pathlib import Path
import json,subprocess,re,wave
R=Path(__file__).resolve().parent; F='/Users/USER/.local/bin/ffmpeg'
inputs=json.loads((R/'evidence/input-verification.json').read_text())
ranges=[[(.05,4.95)],[(.0,5.10),(5.65,19.10),(19.48,24.6)],[(.1,50.9)],[(.1,22.75)]]
plan=[];offset=0
for i,(info,rs) in enumerate(zip(inputs,ranges)):
 segs=[];base=offset
 for a,b in rs:
  segs.append({'source_start':a,'source_end':b,'output_start':round(offset,6),'output_end':round(offset+b-a,6),'speed':1});offset+=b-a
 plan.append({**info,'index':i+1,'segments':segs,'output_start':base,'output_end':offset})
 # concat source chunks with 4ms edge fades only; no speed or synthesis
 filters=[];names=[]
 for j,(a,b) in enumerate(rs):
  filters.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono,afade=t=in:d=0.004,afade=t=out:st={b-a-.004}:d=0.004[c{j}]');names.append(f'[c{j}]')
 filters.append(''.join(names)+f'concat=n={len(rs)}:v=0:a=1[a]')
 part=R/f'evidence/voice-part-{i+1}.wav'
 cmd=[F,'-hide_banner','-loglevel','error','-i',info['path'],'-filter_complex',';'.join(filters),'-map','[a]','-c:a','pcm_s24le',str(part)]
 subprocess.run(cmd,check=True)
 measure=subprocess.run([F,'-hide_banner','-i',str(part),'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 (R/f'evidence/loudnorm-part-{i+1}.log').write_text(measure.stderr)
 m=json.loads(measure.stderr[measure.stderr.rfind('{'):]);plan[-1]['loudness_measured']=m
 gain=min(-18-float(m['input_i']),-1.5-float(m['input_tp']))
 plan[-1]['gain_db']=gain
 out=R/f'evidence/voice-matched-{i+1}.wav'
 subprocess.run([F,'-hide_banner','-loglevel','error','-i',str(part),'-af',f'volume={gain}dB','-ar','48000','-c:a','pcm_s24le',str(out)],check=True)
(R/'evidence/voice-concat.txt').write_text(''.join(f"file '{R}/evidence/voice-matched-{i}.wav'\n" for i in range(1,5)))
subprocess.run([F,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(R/'evidence/voice-concat.txt'),'-c:a','pcm_s24le',str(R/'project/public/voice.wav')],check=True)
result={'version':'v1','fps':60,'total_seconds':round(offset,6),'duration_frames':round(offset*60),'sources':plan,'removed':{'head_tail':'See exact ranges; wider margins than03 recommendations to protect quiet syllables','internal':[{'source':2,'start':5.1,'end':5.65,'reason':'03 identified low-energy pause middle;0.55sec'},{'source':2,'start':19.1,'end':19.48,'reason':'03 identified low-energy pause middle;0.38sec'}]},'phrases_removed':[],'speed':1,'note':'保留完整句和同义追加，直接听感未验证；4ms片段边缘淡化，分段静态增益匹配，不合成声音。'}
(R/'cut-plan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));(R/'project/src/timeline.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'seconds':offset,'frames':round(offset*60),'section_starts':[x['output_start'] for x in plan],'gain_db':[x['gain_db'] for x in plan]}))
