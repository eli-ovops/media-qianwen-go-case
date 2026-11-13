import pathlib,json,hashlib,datetime
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];dest=E/'new-files-inventory.json'
def info(p,purpose):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sourcePurpose':purpose}
def purpose(p):
 n=p.name
 if 'references' in p.parts:return 'Top3 public component previews, preserved source receipts and reviewed contact sheet; copied N026 identified in receipt'
 if 'final-frames' in p.parts or n.endswith('.jpg') or n=='comparison-player.png':return 'Final export frame extraction/contact sheet or local trial/player visual QA; exact generation in QA scripts and frame-index'
 if p.suffix in ['.mp4','.wav','.f32']:return 'Task-local trial/full render or audio decode for original-voice alignment; not an input original'
 if p.suffix in ['.py','.cjs']:return 'Task-local reproducible QA/gate/inventory utility'
 return 'Task-local QA evidence, log, gate manifest, resource measurement or delivery receipt'
files=[p for p in E.rglob('*') if p.is_file() and not p.is_symlink() and p!=dest]
entries=[info(p,purpose(p)) for p in files]
for p in (R/'project/src/v81').rglob('*'):
 if p.is_file() and not p.is_symlink():entries.append(info(p,'v8.1 new Remotion entry and scene source'))
for name in ['project/render-sample-v81.cjs','output/sample-motion-v8.1.mp4','sample-review-v8.1.html','sample-review-v8.1.md','sample-delivery-v8.1.json']:
 entries.append(info(R/name,'v8.1 rendering, final output or review/delivery artifact'))
reused=[R/n for n in ['project/src/v8/theme.ts','project/src/v8/CostReminder.tsx','project/src/v8/captions.json','evidence/sample-v8/source-voice.wav','evidence/sample-v8/resolve-existing-typescript.cjs']]
dest.write_text(json.dumps({'at':datetime.datetime.now().astimezone().isoformat(),'scope':'Only exact v8.1 paths; no broad project scan; excludes self hash to avoid recursion','count':len(entries),'bytes':sum(e['bytes'] for e in entries),'files':sorted(entries,key=lambda e:e['path']),'reusedDependenciesNotNew':[info(p,'Reused existing v8 dependency, unchanged by v8.1') for p in reused]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'count':len(entries),'bytes':sum(e['bytes'] for e in entries),'inventory':str(dest)}))
