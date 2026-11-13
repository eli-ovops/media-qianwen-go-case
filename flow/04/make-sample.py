from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parent;F='/Users/USER/.local/bin/ffmpeg';start=3454;end=4762;a=start/60;b=end/60
src=R/'output/candidate-v1.mp4';out=R/'output/sample-motion-v1.mp4'
cmd=[F,'-hide_banner','-i',str(src),'-filter_complex',f'[0:v]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS[v];[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-r','60','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
with (R/'evidence/sample-export.log').open('w') as l:subprocess.run(cmd,stdout=l,stderr=l,check=True)
cs=json.loads((R/'output/captions-v1.json').read_text());sample=[]
for c in cs:
 if c['end']<=a or c['start']>=b:continue
 sample.append({**c,'full_start':c['start'],'full_end':c['end'],'start':round(max(0,c['start']-a),4),'end':round(min(b-a,c['end']-a),4)})
(R/'output/sample-captions-v1.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2))
def stamp(t):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(R/'output/sample-captions-v1.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['zh']}\n{c['en']}" for i,c in enumerate(sample))+'\n')
receipt={'sample':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'source_intermediate':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_frames_inclusive':[start,end-1],'source_seconds':[a,b],'frames':end-start,'duration_seconds':(end-start)/60,'raw_source':str(R.parent/'03/evidence-v3/e404afe47f88fa4affadf7f5fa273814_raw'),'raw_video_seconds':[a-28.57+.1,b-28.57+.1],'selection':'确认型号→店铺比价→客服→费用整理→估算→每天查价设置，连续完整口播。略超20秒以保留开头完整案例句，不拼效果集锦。','first_phrase':'案例里面千问首先需要确认型号','last_phrase':'每天查价的一个提醒','boundary_energy':'source③28.8–29.3秒低能量，29.4秒进入下一句；起点源29.0967秒留约0.3秒余量','full_film_status':'PAUSED_PENDING_USER_SAMPLE_APPROVAL; existing intermediate preserved, not submitted for full QA','command':cmd}
(R/'evidence/sample-export.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2));print(json.dumps({k:receipt[k] for k in ['duration_seconds','frames','sha256']}))
