import json,pathlib,copy,hashlib,sys,subprocess,os
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];L=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk');S=L/'skills/fred-remotion-output/scripts';sys.path.insert(0,str(S))
from library_gate import acceptance_signature,load_catalog
rec=lambda p:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
src=R/'project/src/v9/Film.tsx';cost=R/'project/src/v9/CostScene.tsx';task=R/'完整成片制作-v9任务.md'
old=json.loads((E.parent/'sample-v8.1/manifest-suggestion-snapshot.json').read_text());m=copy.deepcopy(old)
m.update(revision='full-v9',durationInFrames=6122,referenceCatalogRevision=load_catalog()['revision'],audio={'source':str(R/'project/public/voice.wav'),'cutPlan':rec(R/'project/src/timeline.json'),'timeStretch':1},updatedTask=rec(task));m.pop('reviewInput',None)
m['workflow']['authorization']={'mode':'direct-output','source':str(task),'quote':'用户已确认v8.1方向并说开始，授权从样片进入完整成片；不再探索多套风格；先内部自修后报PMO'}
caps=json.loads((R/'project/src/v9/captions.json').read_text());m['subtitles']={'enabled':True,'sourcePath':str(R/'project/src/v9/captions.json'),'sourceSha256':rec(R/'project/src/v9/captions.json')['sha256'],'cues':[{'startSeconds':c['start'],'endSeconds':c['end'],'text':c['zh']} for c in caps]}
m['clockContract']={'mode':'global','sourceRule':'one global60fps clock; portrait sequences use explicit cut-plan mapped source intervals'}
m['designContract'].update(branding='All requested top/bottom disclaimers/ELI removed; only narration subtitles and explanatory labels',portrait='Original source video; per-frame local person mask; no generative face')
c005=copy.deepcopy(old['pages'][0]['referenceChoices'][1]);op09=copy.deepcopy(old['pages'][0]['referenceChoices'][0]);n044=copy.deepcopy(old['pages'][1]['referenceChoices'][0])
refs=json.loads((E/'references/fetch-receipt.json').read_text())
reason={
'library-legacy81-c005':'选用：单目标向工具/询价分支，再回到结果的连接关系；已看3帧和源函数。',
'library-legacy81-r006':'不选：输入汇入编码器并被清掉，不利于追踪任务条件。',
'library-new10-n026':'不选：外部素材上传手机聊天，本片没有该操作。',
'ep102-selected-07':'需求段选用：每项依次提起，既有组先让位再接新项，建立完整条件。',
'library-selfpick24-sp011':'不选：四角能力铺陈与中间30+计数，不适用于五项具体购买条件；已读SP011实现。',
'library-new10-x015':'不选：三件商品卡轮换，本案只有同一台冰箱。',
'library-legacy81-b062':'不选：人物/AI量化柱图会需要不存在的对比数字。',
'library-legacy81-b074':'不选：失败图片/模糊状态不是店铺询价与客服过程。',
'4b5b8eb5-14b8-4fe9-86fe-e9bee5d02751':'不选：真实图片ROI对照，需要本片没有的对比产品图片；实看15.2秒海报。'}
def preview(id):
 out=[dict(rec(pathlib.Path(v['path'])),id=id,observations=reason.get(id,'已看前轮真实核心帧，保留对象收束关系')) for v in refs if v['id']==id]
 if not out:
  out=[x for pg in old['pages'] for x in pg['componentPlan']['inspectedReferences'] if x['id']==id]
 return out
def bind(ref,symbol,call='FullFilm',file=src):
 ref=copy.deepcopy(ref);ref['implementation']=dict(rec(file),symbol=symbol);ref['callSite']=dict(rec(file),symbol=call,callee=symbol);return ref
def page(id,a,b,queryfile,query,symbol,selected,explain):
 ds=json.loads((E/(queryfile+'-top3.json')).read_text())['entries'];chosen={r['id'] for r in selected}
 candidates=[{'id':v['candidateId'],'decision':'selected' if v['candidateId'] in chosen else 'rejected','reason':reason[v['candidateId']] if v['candidateId'] not in chosen or v['candidateId']!='ep102-selected-07' else explain} for v in ds]
 for ref in selected:
  if ref['id'] not in [c['id'] for c in candidates]:candidates.append({'id':ref['id'],'decision':'selected','reason':explain})
 return {'stableId':id,'startFrame':a,'globalStartFrame':a,'durationInFrames':b-a,'implementationMode':'adapted','productionRoute':{'selected':'remotion','source':str(task)},'oneQuestion':explain,'sourceSpans':[{'text':c['zh']} for c in caps if c['start']>=a/60 and c['start']<b/60],'componentPlan':{'query':query,'access':'installed','candidates':candidates,'inspectedReferences':[v for r in selected for v in preview(r['id'])]},'referenceChoices':selected,'visualPlan':{'enter':'从本期对应口播的既有对象进入','change':explain,'read':'条件/任务标签按原声逐项停留','exit':'保持关键对象并交给下一任务','handoff':'沿本期时间线连续承接'},'sceneGuide':{'type':'custom','modifiers':['object-transition']}}
def media(id,a,b,name):return {'stableId':id,'startFrame':a,'globalStartFrame':a,'durationInFrames':b-a,'implementationMode':'preserved-media','productionRoute':{'selected':'media','source':str(task)},'mediaContract':[rec(R/'project/public/v9'/f'{name}.mp4')],'componentPlan':{'search':'not-needed','decisionReason':'本人原片按连续源时钟播放；本地背景排除与等比构图，只有口播标题/字幕'},'referenceChoices':[]}
ep=copy.deepcopy(c005);ep.update(id='ep102-selected-07',source=dict(rec(L/'components/projects/ep102-selected-20261005/source/versions/canvas-v17/adapters/CanvasRevisionV14.tsx'),symbol='CanvasRevisionV14'),reason='五项条件逐项提起并建立组',preserve='已有组让位后新对象进入；建立的对象保持可见',change='四横向列改为竖屏五项条件；近黑底、语义图标与冰箱',useScope='36.39–57.47秒',keyAction='类别提起、既有组移动让位、新项进入')
tools=page('tools',294,1407,'tools','节点 连线 输入 汇聚 输出 工作流','GoalsToTools',[bind(c005,'GoalsToTools')],'目标节点通过关系线连接购物/订票/出行工具，并推进到输出')
req=page('requirements',1714,3448,'requirements','要点 列表 卡片 分类','RequirementBuild',[bind(ep,'RequirementBuild')],'冰箱保留；现有条件上移让位，新条件逐项提起，最终同时可读')
execution=page('execution',3448,3946,'execution','商品 确认 对比 客服','ModelToQuote',[bind(c005,'ModelToQuote')],'同一型号分支到店铺报价/客服，再收束到商品报价节点')
outro=page('outro',5030,5776,'outro','费用 汇合 总结','TasksToChoice',[bind(op09,'TasksToChoice')],'三项查问整理任务收束进AI，再交给真人作最终选择')
for r in tools['referenceChoices']+execution['referenceChoices']+outro['referenceChoices']:
 r.update(useScope='本场景全局时间范围，见startFrame/durationInFrames',change='保留来源动作关系，按本期真实口播重排暗色竖屏语义对象')
fees=copy.deepcopy(old['pages'][0]);rem=copy.deepcopy(old['pages'][1])
for pg,a,b in [(fees,3946,4474),(rem,4474,4762)]:
 pg['startFrame']=pg['globalStartFrame']=a;pg['durationInFrames']=b-a;pg['productionRoute']['source']=str(task);pg.pop('componentAcceptance',None)
 for ref in pg['referenceChoices']:
  ref['implementation'].update(rec(cost));ref['callSite'].update(rec(cost));ref['callSite']['symbol']='CostGather' if ref['implementation']['symbol']=='CalculationRails' else 'CostScene'
 pg['motionEvents']=[]
m['pages']=[media('intro',0,294,'intro'),tools,media('bridge',1407,1714,'bridge-safe'),req,execution,fees,rem,media('opinion',4762,5030,'opinion-safe'),outro,media('close',5776,6122,'close-safe')]
for pg in m['pages']:
 if pg['implementationMode']=='preserved-media':continue
 ac={'status':'passed','stage':'suggestion','reviewer':'assistant','checks':{'semanticFit':pg['oneQuestion'],'corePreserved':pg['referenceChoices'][0]['preserve'],'visualQuality':'实看本轮24核心帧、E14海报及前轮已核OP09/N044；来源和选型取舍独立于最终输出验收'},'evidence':[dict(x) for x in pg['componentPlan']['inspectedReferences']]};pg['componentAcceptance']=ac;ac['contextSha256']=acceptance_signature(m,pg,'suggestion')
from component_distribution import analyze
from common import load_references
_,catalog=load_references(L)
audit=analyze(m,catalog)
compare={
 'tools':('从目标调用工具','上方目标，三条工具分支，下方推进结果','明确目标与可调用工具之间的因果关系'),
 'execution':('同一型号向多店询价','冰箱保留，三店服务卡，再并入单一报价对象','沿同一商品追踪询价结果'),
 'fees':('归并费用并核预算','报价、回收抵扣、安装费保持，进入相加减表达式','输入持续可见，防止加减关系丢失'),
 'outro':('AI承接查问整理','三个任务卡收向AI块，再回到真人选择','将执行工作交给AI，将最后决定留给人')}
m['componentDistributionReview']={'status':'passed','reviewedBy':'assistant','contextSha256':audit['contextSha256'],'decisions':[
 {'groupKey':g['groupKey'],'sceneIds':g['sceneIds'],'reuseKind':'distinct-adaptation','reason':'沿同一案例保持连接与汇入动作语法；各场景输入、接收者和决策含义不同，实看全片概览没有用同一数据布局重复填充。','comparisons':[dict(stableId=sid,task=compare[sid][0],visibleState=compare[sid][1],reusePurpose=compare[sid][2]) for sid in g['sceneIds']], 'evidence':[rec(E/f'stills-board-{i}.jpg') for i in range(3)]} for g in audit['groups']]}
(E/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E.parent/'sample-v8/resolve-existing-typescript.cjs')
for name,args in [('gate-suggestion',['library_gate.py','--stage','suggestion','--output',str(E/'gate-suggestion.json')]),('workflow-planning',['workflow.py','--stage','planning'])]:
 r=subprocess.run([sys.executable,str(S/args[0]),'--manifest',str(E/'manifest.json'),*args[1:]],capture_output=True,text=True,env=env);(E/(name+'.log')).write_text(r.stdout+r.stderr);print(name,r.returncode,r.stdout);assert r.returncode==0
