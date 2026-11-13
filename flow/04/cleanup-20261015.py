from pathlib import Path
import os,json,hashlib,stat,subprocess,datetime,re,sys
R=Path(__file__).resolve().parent;E=R/'evidence/cleanup-20261015';E.mkdir(exist_ok=True)
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
NOW=lambda:datetime.datetime.now().astimezone().isoformat()
def walk(base):
 for root,ds,fs in os.walk(base,followlinks=False):
  ds[:]=[d for d in ds if not Path(root,d).is_symlink() and d not in {'node_modules','.git','Default','Cache','Code Cache','GPUCache'} and 'browser-profile' not in d]
  for f in fs:yield Path(root,f)
def snapshot(p):
 s=p.lstat();return {'path':str(p),'dev':s.st_dev,'ino':s.st_ino,'bytes':s.st_size,'mtimeNs':s.st_mtime_ns,'mode':s.st_mode,'links':s.st_nlink,'allocatedBytes':s.st_blocks*512}
def df():
 p=subprocess.run(['df','-k',str(R)],capture_output=True,text=True,check=True);v=p.stdout.splitlines()[-1].split();return {'at':NOW(),'raw':p.stdout,'filesystem':v[0],'availableBytes':int(v[3])*1024}
if sys.argv[1]=='plan':
 texts=[]
 for p in walk(R):
  if p==Path(__file__) or E in p.parents or 'bundle' in p.parts or p.suffix not in {'.md','.json','.py','.cjs','.tsx','.ts','.sh','.html','.txt'} or p.stat().st_size>2000000:continue
  try:
   s=p.read_text()
   if p.suffix=='.json':s=json.dumps(json.loads(s),ensure_ascii=False,indent=2)
   texts.append((p,s))
  except (UnicodeError,json.JSONDecodeError):continue
 videos=[p for p in walk(R) if p.suffix.lower() in {'.mp4','.mov','.mkv','.webm','.m4v'}]
 rows=[]
 for p in sorted(videos):
  q=p.relative_to(R);ss=snapshot(p);sha=H(p) if stat.S_ISREG(ss['mode']) else None
  refs=[{'file':str(t),'line':i,'text':line[:350]} for t,s in texts for i,line in enumerate(s.splitlines(),1) if str(p) in line or str(q) in line or (p.name in line and t.suffix in {'.py','.cjs','.sh'})]
  proof=[x for x in refs if Path(x['file']).suffix in {'.py','.cjs','.sh'}]
  if re.fullmatch(r'patch-\d+\.mp4',p.name) and p.parent==R/'evidence':proof=[{'file':str(R/'project/patch-render.cjs'),'line':5,'text':'renderMedia ../evidence/patch-${i}.mp4; consumed by assemble.py'}]
  protected=('public' in q.parts or 'bundle' in q.parts or p.is_symlink())
  decision='KEEP_INPUT_ASSET' if protected else ('DELETE_GENERATED' if proof else 'KEEP_UNKNOWN_SOURCE')
  if p==R/'output/sample-motion-v1.mp4':decision='KEEP_CROSS_CONTENT_REFERENCE_UNKNOWN';refs.append({'file':'/Volumes/EXTERNAL/自媒体/动效参考对比-20261012/近期两账号-20261013/读取覆盖.json','text':'Other research references this exact sample; current downstream need not independently closed, preserve conservatively.'})
  if not stat.S_ISREG(ss['mode']) or ss['links']!=1:decision='KEEP_NONREGULAR_OR_HARDLINK'
  rows.append({**ss,'sha256':sha,'decision':decision,'sourceEvidence':proof[:8],'references':refs[:25],'referenceCount':len(refs),'reason':'Published content generated render/intermediate, approved cleanup' if decision=='DELETE_GENERATED' else 'Retain source pixels / project input and reproduction dependencies, or uncertainty'})
 candidates=[x for x in rows if x['decision']=='DELETE_GENERATED'];paths=[x['path'] for x in candidates]
 l=subprocess.run(['/usr/sbin/lsof','-nP','-Fpcfn','--',*paths],capture_output=True,text=True)
 (E/'lsof-before.txt').write_text(l.stdout+l.stderr)
 assert l.returncode in [0,1] and not l.stderr.strip(), 'lsof uncertain; stop'
 openpaths=[line[1:] for line in l.stdout.splitlines() if line.startswith('n')]
 for x in rows:
  if x['path'] in openpaths:x['decision']='KEEP_OPEN_PROCESS'
 ps=subprocess.run(['ps','-axo','pid=,comm=,args='],capture_output=True,text=True,check=True)
 matching=[line for line in ps.stdout.splitlines() if ('qianwen-go-case-20261013' in line and any(n in line for n in ['ffmpeg','remotion','render-','assemble.py'])) and 'cleanup-20261015.py' not in line and 'python3 - <<' not in line]
 (E/'process-check.json').write_text(json.dumps({'at':NOW(),'matchingTaskRenderOrAssembly':matching,'lsofExit':l.returncode,'openCandidatePaths':openpaths},ensure_ascii=False,indent=2))
 assert not matching,'Active task producer uncertain; stop before deleting'
 plan={'at':NOW(),'content_id':'qianwen-go-case-20261013','owner':'01a11a6f-49ef-7653-934a-4312979fd4e7','task':str(R/'发布后视频清理-20261015任务.md'),'publicationTrigger':str(R.parent/'06/X重试上传-20261014.md'),'targetModel':'gpt-6.1-sol/medium','actualModelEffort':'UNKNOWN','ruleVersions':['PERMISSIONS-2026-10-14-v1','ROUTING-2026-10-13-v4'],'boundary':'Only explicit regular files under this04. No symlink following, no directories removed. motion-components-20261014 and all other content excluded. Input/public/bundle video assets retained. External upload copies not found in task history; no global disk scan.','rows':rows}
 (E/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
 existing=R/'evidence/full-v9-r3c/artifact-inventory.json';d=json.loads(existing.read_text());d['postPublicationCleanup20261015']={'state':'PLANNED_NOT_DELETED','plan':str(E/'plan.json'),'rows':rows};existing.write_text(json.dumps(d,ensure_ascii=False,indent=2))
 counts={k:sum(x['decision']==k for x in rows) for k in sorted({x['decision'] for x in rows})};print(json.dumps({'counts':counts,'deleteBytes':sum(x['bytes'] for x in rows if x['decision']=='DELETE_GENERATED'),'unknown':[(x['path'],x['decision']) for x in rows if 'UNKNOWN' in x['decision']]},ensure_ascii=False))
elif sys.argv[1]=='execute':
 plan=json.loads((E/'plan.json').read_text());targets=[x for x in plan['rows'] if x['decision']=='DELETE_GENERATED'];assert len(targets)==66
 protected=[]
 for p in walk(R/'project'):
  if p.is_file() and not p.is_symlink():protected.append({'path':str(p),'sha256':H(p)})
 raw=json.loads((R/'evidence/input-verification.json').read_text())
 for x in raw:
  p=Path(x['path']);protected.append({'path':str(p),'sha256':H(p)})
 for v in ['v6','v7','v7.1']:
  p=Path('/Volumes/EXTERNAL/自媒体/motion-components-20261014/flow/04/output')/f'sample-{v}.mp4';protected.append({'path':str(p),'sha256':H(p)})
 for x in plan['rows']:
  if x['decision']!='DELETE_GENERATED':protected.append({'path':x['path'],'sha256':H(x['path'])})
 (E/'protected-baseline.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2))
 paths=[x['path'] for x in targets]
 for x in targets:
  p=Path(x['path']);assert p.is_relative_to(R) and 'motion-components' not in str(p)
  assert all(not q.is_symlink() for q in [p,*p.parents] if q!=Path('/'))
  cur=snapshot(p);assert all(cur[k]==x[k] for k in ['dev','ino','bytes','mtimeNs','mode','links']);assert stat.S_ISREG(cur['mode']) and cur['links']==1 and H(p)==x['sha256']
 l=subprocess.run(['/usr/sbin/lsof','-nP','-Fpcfn','--',*paths],capture_output=True,text=True);(E/'lsof-execute.txt').write_text(l.stdout+l.stderr)
 assert l.returncode==1 and not l.stdout.strip() and not l.stderr.strip(),'Open handle or lsof uncertainty; nothing deleted'
 ps=subprocess.run(['ps','-axo','pid=,comm=,args='],capture_output=True,text=True,check=True)
 active=[s for s in ps.stdout.splitlines() if 'qianwen-go-case-20261013' in s and any(k in s for k in ['ffmpeg','remotion','render-','assemble.py']) and 'cleanup-20261015.py' not in s]
 assert not active,'Active producer; nothing deleted'
 result={'at':NOW(),'before':df(),'deleted':[],'failure':None};(E/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 try:
  for x in targets:
   p=Path(x['path']);cur=snapshot(p);assert cur['ino']==x['ino'] and cur['mtimeNs']==x['mtimeNs'] and cur['bytes']==x['bytes']
   p.unlink();result['deleted'].append(x);(E/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 except Exception as e:result['failure']=repr(e)
 result['after']=df();result['actualAvailableBytesDelta']=result['after']['availableBytes']-result['before']['availableBytes'];result['deletedLogicalBytes']=sum(x['bytes'] for x in result['deleted']);result['deletedAllocatedBytes']=sum(x['allocatedBytes'] for x in result['deleted']);result['protectedCheck']=[{'path':x['path'],'unchanged':Path(x['path']).exists() and H(x['path'])==x['sha256']} for x in protected];result['allDeletedPathsAbsent']=all(not Path(x['path']).exists() for x in result['deleted']);result['limits']='df measures volume-wide available-space delta; concurrent writes and APFS allocation prevent exact causal attribution to logical bytes.'
 (E/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));assert result['failure'] is None and all(x['unchanged'] for x in result['protectedCheck']) and result['allDeletedPathsAbsent']
 print({'deleted':len(result['deleted']),'logicalBytes':result['deletedLogicalBytes'],'availableBytesDelta':result['actualAvailableBytesDelta'],'protectedChecks':len(protected),'allUnchanged':True})
