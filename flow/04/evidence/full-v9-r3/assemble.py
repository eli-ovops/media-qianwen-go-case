from pathlib import Path
import subprocess,json,hashlib
E=Path(__file__).resolve().parent;R=E.parents[1];F='/Users/USER/.local/bin/ffmpeg'
out=R/'output/qianwen-go-full-v9-r3.mp4';assert not out.exists()
args=[F,'-hide_banner','-n','-i',str(R/'output/qianwen-go-full-v9-r2.mp4')]
for name in ['bridge','opinion','close']:args+=['-i',str(E/f'patch-{name}.mp4')]
filt='[0:v]split=3[a][b][c];[a]trim=start_frame=0:end_frame=1407,setpts=PTS-STARTPTS[a0];[b]trim=start_frame=1714:end_frame=4762,setpts=PTS-STARTPTS[b0];[c]trim=start_frame=5030:end_frame=5776,setpts=PTS-STARTPTS[c0];[1:v]setpts=PTS-STARTPTS[p1];[2:v]setpts=PTS-STARTPTS[p2];[3:v]setpts=PTS-STARTPTS[p3];[a0][p1][b0][p2][c0][p3]concat=n=6:v=1:a=0[v]'
args+=['-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','60','-c:a','copy','-t','102.03333333333333','-movflags','+faststart',str(out)]
(E/'assemble-command.json').write_text(json.dumps(args,ensure_ascii=False,indent=2))
with (E/'assemble.log').open('w') as log:subprocess.run(args,stderr=log,check=True)
print(out,hashlib.sha256(out.read_bytes()).hexdigest(),flush=True)
