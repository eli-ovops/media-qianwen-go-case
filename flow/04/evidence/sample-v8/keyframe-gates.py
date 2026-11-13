import pathlib,json,hashlib,sys,os,subprocess
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];S=pathlib.Path('/Users/USER/.codex/skills/fred-remotion-output/scripts');sys.path.insert(0,str(S));from library_gate import acceptance_signature
rec=lambda p:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
p=E/'manifest.json';m=json.loads(p.read_text());(E/'manifest-suggestion-snapshot.json').write_text(p.read_text())
for page in m['pages']:
 fees=page['stableId']=='fees';ids=[111,390] if fees else [546,561,759]
 frames=[dict(rec(E/'final-frames'/f'native-f{f:03}.png'),id=f'final-f{f}',timeSeconds=f/60) for f in ids]
 page['keyframeReview']={'status':'assistant-inspected','userConfirmation':'PENDING_PMO_FIRST','frames':frames,'sourceFiles':[rec(R/'project/src/v8/CostReminder.tsx'),rec(R/'project/src/v8/theme.ts'),rec(R/'project/src/v8/captions.json')],'openIssues':[],'scope':'Final MP4 actual screenshots, 287 unique sampled frames plus 5 native frames. No direct listening or real-time continuous AV review.'}
 ac=page['componentAcceptance'];ac.update(status='passed',stage='keyframes',evidence=frames)
 ac['checks']['visualQuality']='最终MP4原尺寸帧可读；费用、字幕、页脚未裁切；汇合先移除小字再显估算。' if fees else '最终MP4原尺寸9.1/9.35/12.65秒，旧标题已退场；冰箱缩为附件，条件/开关/反馈位置分离，未发现压字或字幕遮挡。'
 ac['contextSha256']=acceptance_signature(m,page,'keyframes')
p.write_text(json.dumps(m,ensure_ascii=False,indent=2))
env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:/Users/USER/.local/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E/'resolve-existing-typescript.cjs')
ts=pathlib.Path('/Users/USER/.npm/_npx/6286e9339036798b/node_modules/typescript/package.json')
(E/'parser-runtime.json').write_text(json.dumps({'scope':'process-local exact dependency resolution only; upstream AST checker unchanged','adapter':rec(E/'resolve-existing-typescript.cjs'),'typescriptPackage':rec(ts),'typescriptVersion':json.loads(ts.read_text())['version'],'nodeOptions':env['NODE_OPTIONS']},indent=2))
commands=[('gate-keyframes',[sys.executable,str(S/'library_gate.py'),'--manifest',str(p),'--stage','keyframes','--output',str(E/'gate-keyframes.json')]),('workflow-representative',[sys.executable,str(S/'workflow.py'),'--manifest',str(p),'--stage','representative'])]
for name,cmd in commands:
 r=subprocess.run(cmd,capture_output=True,text=True,env=env);(E/(name+'.stdout.json')).write_text(r.stdout);(E/(name+'.stderr.txt')).write_text(r.stderr);print(name,r.returncode,r.stdout,r.stderr)
 if r.returncode: raise SystemExit(r.returncode)
