import pathlib,json,math
from PIL import Image,ImageDraw
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];caps=json.loads((R/'project/src/v9r2/captions.json').read_text());ids=[4,8,11,18,23,24,25,26,27,28,29,30,31,32,33,34,38,39,40,41]
frames=[round((caps[i-1]['start']+caps[i-1]['end'])/2*60) for i in ids]
for k in range(0,len(frames),4):
 chunk=frames[k:k+4];im=Image.new('RGB',(1080,math.ceil(len(chunk)/2)*990),'#1c2324');d=ImageDraw.Draw(im)
 for j,f in enumerate(chunk):
  x=j%2*540;y=j//2*990;im.paste(Image.open(E/'final-frames'/f'native-f{f:04}.png').resize((540,960)),(x,y));d.text((x+8,y+966),f'f{f} {f/60:.4f}s / cue{ids[k+j]}',fill='white')
 im.save(E/f'key-board-{k//4+1:02}.jpg',quality=96)
(E/'key-board-index.json').write_text(json.dumps(dict(frames=frames,cues=ids),indent=2))
