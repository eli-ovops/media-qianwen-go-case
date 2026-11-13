import pathlib,json,hashlib,sys,os,subprocess
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];S=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk/skills/fred-remotion-output/scripts');sys.path.insert(0,str(S));from library_gate import acceptance_signature
rec=lambda p:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
p=E/'manifest.json';m=json.loads(p.read_text());caps=json.loads((R/'project/src/v9r2/captions.json').read_text());framesById={c['id']:round((c['start']+c['end'])/2*60) for c in caps}
selected={'tools':[4,8,11],'requirements':[18,23,24,25],'execution':[26,27,28],'fees':[29,30,31,32],'reminder':[33,34],'outro':[38,39,40,41]}
for pg in m['pages']:
 if pg['stableId'] not in selected:continue
 frames=[dict(rec(E/'final-frames'/f'native-f{framesById[i]:04}.png'),timeSeconds=framesById[i]/60) for i in selected[pg['stableId']]]
 pg['keyframeReview']={'status':'assistant-inspected','userConfirmation':'PENDING_PMO_FIRST','frames':frames,'sourceFiles':[rec(R/'project/src'/name) for name in ['v9r2/Film.tsx','v9r2/CostScene.tsx','v9r2/Entry.tsx','v9r2/captions.json','v8/theme.ts','v8/CostReminder.tsx']],'scope':'Final MP4 sampled boards, per-cue native subtitle strips, native keys; reviewed image list is visual-review.json. No continuous audiovisual or direct listening claim.'}
 ac=pg['componentAcceptance'];ac.update(stage='keyframes',evidence=frames);ac['checks']['visualQuality']='实看最终导出关键帧、接缝/动作采样与字幕；内容对象、语义关系及文字边界可读，额外免责声明/ELI角标未出现。机器动态标记及阅读停留解释单列motion-review.json。';ac['contextSha256']=acceptance_signature(m,pg,'keyframes')
for row in m['componentDistributionReview']['decisions']:row['evidence']=[rec(E/f'overview-{i:02}.jpg') for i in range(1,6)]
p.write_text(json.dumps(m,ensure_ascii=False,indent=2));env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E.parent/'sample-v8/resolve-existing-typescript.cjs')
for name,args in [('gate-keyframes',['library_gate.py','--stage','keyframes','--output',str(E/'gate-keyframes.json')]),('workflow-representative',['workflow.py','--stage','representative'])]:
 r=subprocess.run([sys.executable,str(S/args[0]),'--manifest',str(p),*args[1:]],capture_output=True,text=True,env=env);(E/(name+'.log')).write_text(r.stdout+r.stderr);print(name,r.returncode,r.stdout);assert r.returncode==0
