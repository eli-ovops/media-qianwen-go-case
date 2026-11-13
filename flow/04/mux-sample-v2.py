from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v2';out=R/'output/sample-motion-v2.mp4';assert not out.exists()
cmd=['/Users/USER/.local/bin/ffmpeg','-hide_banner','-i',str(E/'sample-v2-video-only.mp4'),'-i',str(R/'output/sample-motion-v1.mp4'),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(out)]
(E/'mux-command.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2))
with (E/'mux.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
