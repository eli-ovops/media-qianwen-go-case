from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parent;F='/Users/USER/.local/bin/ffmpeg';ws=json.loads((R/'evidence/patch-windows.json').read_text())
base=R/'evidence/first-export/candidate-before-motion-fix.mp4';cmd=[F,'-hide_banner','-threads','2','-i',str(base)]
for i in range(len(ws)):cmd+=['-threads','1','-i',str(R/f'evidence/patch-{i}.mp4')]
segments=[];pos=0
for i,w in enumerate(ws):
 if w['start_frame']>pos:segments.append(('original',pos,w['start_frame']))
 segments.append(('patch',i,w['end_frame_exclusive']-w['start_frame']));pos=w['end_frame_exclusive']
if pos<6122:segments.append(('original',pos,6122))
n=sum(s[0]=='original' for s in segments);filters=['[0:v]split='+str(n)+''.join(f'[orig{i}]' for i in range(n))];oi=0;labels=[]
for j,s in enumerate(segments):
 if s[0]=='original':
  filters.append(f'[orig{oi}]trim=start_frame={s[1]}:end_frame={s[2]},setpts=PTS-STARTPTS,setsar=1[v{j}]');oi+=1
 else:filters.append(f'[{s[1]+1}:v]trim=end_frame={s[2]},setpts=PTS-STARTPTS,setsar=1[v{j}]')
 labels.append(f'[v{j}]')
filters.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=0[v]')
cmd+=['-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-r','60','-c:a','copy','-movflags','+faststart',str(R/'output/candidate-v1-corrected.mp4')]
(R/'evidence/assembly-command.json').write_text(json.dumps({'argv':cmd,'segments':segments,'audio':'original AAC stream copy','patch_frames':sum(w['end_frame_exclusive']-w['start_frame'] for w in ws),'unaffected_frames':'original export decoded/reencoded during assembly; full final QA required'},ensure_ascii=False,indent=2))
with (R/'evidence/assembly.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=log,check=True)
(R/'output/candidate-v1-corrected.mp4').replace(R/'output/candidate-v1.mp4')
print('assembled correction; first export preserved')
