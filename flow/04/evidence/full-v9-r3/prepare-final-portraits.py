import pathlib,subprocess,json,sys
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];F='/Users/USER/.local/bin/ffmpeg'
raw=json.loads((R.parent/'03/素材接收-v3.json').read_text())['raw_media']
clips=[('bridge-safe',1,19.48,5.12,23.45),('opinion-safe',3,.1,4.46,79.37),('close-safe',3,17,5.75,96.27)]
pilot=len(sys.argv)>1 and sys.argv[1]=='pilot'
if pilot:clips=[('pilot',0,1.6,1/60,0)]
clips=[c for c in clips if c[0]!='opinion-safe']
records=[]
for name,i,start,duration,at in clips:
 out=E/'pilot-v2.png' if pilot else R/'project/public/v9r3-final'/f'{name}.mp4'
 assert not out.exists(),out
 log=(E/f'matte-final-{name}.log').open('w')
 a=subprocess.Popen([F,'-hide_banner','-loglevel','error','-ss',str(start),'-i',raw[i]['path'],'-t',str(duration),'-an','-vf','scale=540:960,fps=60','-pix_fmt','bgra','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=log)
 b=subprocess.Popen([str(E/'person-matte-r3e')]+(['close'] if name in ['close-safe','bridge-safe'] else []),stdin=a.stdout,stdout=subprocess.PIPE,stderr=log);a.stdout.close()
 args=[F,'-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','bgra','-video_size','540x960','-framerate','60','-i','pipe:0','-an']
 args+=['-frames:v','1'] if pilot else ['-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart']
 c=subprocess.Popen(args+[str(out)],stdin=b.stdout,stderr=log);b.stdout.close()
 exits=[a.wait(),b.wait(),c.wait()];log.close();assert exits==[0,0,0],exits
 records.append({'name':name,'source':raw[i]['path'],'sourceStart':start,'duration':duration,'globalStart':at,'path':str(out),'processExit':exits,'method':'Apple Vision accurate person matte every decoded 60fps frame; same source frame composited over #090D11, retain full540x960 source framing; no face synthesis'})
 print(name,'COMPLETE',flush=True)
(E/('portrait-pilot.json' if pilot else 'portrait-final-index.json')).write_text(json.dumps(records,ensure_ascii=False,indent=2))
