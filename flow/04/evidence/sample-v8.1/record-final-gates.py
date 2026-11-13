import pathlib,json,hashlib,sys,os,subprocess
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];S=pathlib.Path('/Users/USER/.codex/skills/fred-remotion-output/scripts');sys.path.insert(0,str(S));from library_gate import acceptance_signature
rec=lambda p:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
p=E/'manifest.json';m=json.loads(p.read_text());(E/'manifest-suggestion-snapshot.json').write_text(p.read_text())
for page in m['pages']:
 ids=[111,354,365,390] if page['stableId']=='fees' else [546,558,759]
 frames=[dict(rec(E/'final-frames'/f'native-f{f:03}.png'),id=f'final-f{f}',timeSeconds=f/60) for f in ids]
 sourcePaths=[R/'project/src/v81/CostReminder.tsx',R/'project/src/v81/Entry.tsx',R/'project/src/v8/theme.ts',R/'project/src/v8/CostReminder.tsx',R/'project/src/v8/captions.json']
 page['keyframeReview']={'status':'assistant-inspected','userConfirmation':'PENDING_PMO_FIRST','frames':frames,'sourceFiles':[rec(p) for p in sourcePaths],'openIssues':[],'scope':'Final MP4 full-interval 10fps samples plus 60fps dense docking/gather/handoff/toggle ranges and native keys; no direct listening or real-time continuous AV claim.'}
 ac=page['componentAcceptance'];ac.update(status='passed',stage='keyframes',evidence=frames)
 ac['checks']['visualQuality']='最终MP4原尺寸帧：输入报价/优惠/服务在总支出显现前中后保持存在，无v8空档；黑底亮色、服务图标和字幕可读。' if page['stableId']=='fees' else '最终MP4接缝+0.1/0.3s原帧：旧标题不压顶标；同一计算组等比上移，原结果接阈值，开关/反馈不盖字幕。'
 ac['contextSha256']=acceptance_signature(m,page,'keyframes')
p.write_text(json.dumps(m,ensure_ascii=False,indent=2))
env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:/Users/USER/.local/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E.parent/'sample-v8/resolve-existing-typescript.cjs')
for name,args in [('gate-keyframes',['library_gate.py','--manifest',str(p),'--stage','keyframes','--output',str(E/'gate-keyframes.json')]),('workflow-planning',['workflow.py','--manifest',str(p),'--stage','planning']),('workflow-representative',['workflow.py','--manifest',str(p),'--stage','representative'])]:
 r=subprocess.run([sys.executable,str(S/args[0]),*args[1:]],env=env,capture_output=True,text=True);(E/(name+'.stdout.json')).write_text(r.stdout);(E/(name+'.stderr.txt')).write_text(r.stderr);print(name,r.returncode,r.stdout);assert r.returncode==0
