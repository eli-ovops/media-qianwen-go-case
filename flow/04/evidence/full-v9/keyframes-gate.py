import pathlib,json,hashlib,sys,os,subprocess
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];P=R/'project';S=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk/skills/fred-remotion-output/scripts');sys.path.insert(0,str(S))
from library_gate import acceptance_signature
rec=lambda p:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
p=E/'manifest.json';m=json.loads(p.read_text());(E/'manifest-suggestion-snapshot.json').write_bytes(p.read_bytes())
keys={'tools':[('still',6.8),('still',17.5),('still',21.6)],'requirements':[('fixed',40.1),('fixed',51.5),('fixed',56.5)],'execution':[('still',59.6),('still',62.8),('still',64.8)],'fees':[('fixed',65.8),('still',68.1),('still',72.1)],'reminder':[('still',75.1),('still',78.4)],'outro':[('still',86.5),('still',92.5),('still',95.5)]}
sources=[rec(P/'src'/x) for x in ['v9/Film.tsx','v9/CostScene.tsx','v9/Entry.tsx','v9/captions.json','v8/theme.ts','v8/CostReminder.tsx']]
for pg in m['pages']:
 if pg['stableId'] not in keys:continue
 frames=[dict(rec(E/f'{prefix}-{t}.png'),timeSeconds=t) for prefix,t in keys[pg['stableId']]]
 pg['keyframeReview']={'status':'assistant-inspected','userConfirmation':'PENDING_PMO_FIRST','frames':frames,'sourceFiles':sources,'openIssues':[],'scope':'代表关键帧实看：新修正需求与人像使用fixed；still范围的组件内容未被后续局部改动改变。成片实际导出仍须独立复核。'}
 ac=pg['componentAcceptance'];ac.update(stage='keyframes',evidence=frames);ac['checks']['visualQuality']='实际检查字距边界、当前对象保留、连接/汇入布局；图形与字幕分区，无要求删除的角标；只为关键帧验收，不代表整片动态验收。';ac['contextSha256']=acceptance_signature(m,pg,'keyframes')
p.write_text(json.dumps(m,ensure_ascii=False,indent=2))
env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E.parent/'sample-v8/resolve-existing-typescript.cjs')
for name,args in [('gate-keyframes',['library_gate.py','--stage','keyframes','--output',str(E/'gate-keyframes.json')]),('workflow-representative',['workflow.py','--stage','representative'])]:
 r=subprocess.run([sys.executable,str(S/args[0]),'--manifest',str(p),*args[1:]],capture_output=True,text=True,env=env);(E/(name+'.log')).write_text(r.stdout+r.stderr);print(name,r.returncode,r.stdout);assert r.returncode==0
