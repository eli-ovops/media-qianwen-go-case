import pathlib,json,hashlib,sys,copy
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];L=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk');S=L/'skills/fred-remotion-output/scripts';sys.path.insert(0,str(S));from library_gate import acceptance_signature
rec=lambda p:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m=json.loads((E.parent/'sample-v8/manifest-suggestion-snapshot.json').read_text());m['workflow']['authorization'].update(source=str(R/'Fred工作流费用提醒样片-v8任务.md'),quote='2026-10-14用户最新视觉纠正 + PMO样片v8审阅.md：独立v8.1，黑/近黑背景，增加承担语义动作的组件，内部自检后报PMO')
m['revision']='v8.1-dark';m['reviewInput']=rec(R/'PMO样片v8审阅.md');m['updatedTask']=rec(R/'Fred工作流费用提醒样片-v8任务.md');m['designContract']={'background':'#090D11','contrast':'bright lime/cyan/amber semantic roles','continuity':'Persistent quote/discount/service operands, connected output then same output budget predicate; no disappear/rebuild sum','sourcePriority':'latest user black-background instruction overrides Fred white default'}
src=R/'project/src/v81/CostReminder.tsx'
for page in m['pages']:
 page.pop('keyframeReview',None)
 for ref in page['referenceChoices']:
  for k in ['implementation','callSite']:ref[k].update(rec(src))
 if page['stableId']=='fees':
  ref=page['referenceChoices'][0];ref.update(preserve='多对象位置收束到同一运算列，保留原对象内容；主商品节点持续存在',change='保留三个操作数，不沿用末端缩小淡出；暗底，优惠减项/服务加项，逐级接入总支出',useScope='3.0–6.4秒操作数入位并形成输出',keyAction='辅助对象接入同一计算关系，输入保留')
  page['visualPlan'].update(change='优惠/服务原对象依次入运算位，三输入连线形成总支出',exit='保留全部操作数与总支出',handoff='整个计算组上移缩小，总支出原节点接预算条件')
  ent=json.loads((E/'semantic-components-top3.json').read_text())['entries'][0]
  page['componentPlan']['candidates'] += [{'id':'library-legacy81-c005','decision':'selected','reason':'真实3核心帧为有连线的输入分支→输出关系，源码已读；用于计算端口和总支出输出路径。'}, {'id':'library-legacy81-r006','decision':'rejected','reason':'真实3帧与源码呈多输入合成编码器并清掉输入；本次需保留费用依据，不选。'}]
  rr=[x for x in json.loads((E/'references/receipt.json').read_text()) if x['id']=='library-legacy81-c005']
  for x in rr:page['componentPlan']['inspectedReferences'].append({'id':x['id'],'path':x['path'],'sha256':x['sha256'],'observations':'上方根节点连接多个可读输入，随后收束成输入到输出连线；本片采用随操作数而变的端口与连接路径。'})
  page['referenceChoices'].append({'id':'library-legacy81-c005','reason':'费用输入需要可追踪的连接关系，收束到总支出后继续到条件','preserve':'输入分支通过显性线条进入输出关系','change':'三项算术而非分类树；暗底竖屏；保留输入','useScope':'3.02–6.18秒计算端口/连线','useMode':'local','keyAction':'分支连接后显现输出路径','source':dict(rec(L/ent['sourceFiles'][0]['path']),symbol='RebuiltC005'),'implementation':dict(rec(src),symbol='CalculationRails'),'callSite':dict(rec(src),symbol='CostGather',callee='CalculationRails')})
 else:
  ref=page['referenceChoices'][0];ref.update(preserve='同一主对象组缩小成为提醒控制的输入附件',change='从单商品改为包含所有费用与总支出的计算组；预算比较直接附着原结果节点',useScope='8.8–9.72秒计算组变为提醒条件',keyAction='同一计算组等比收束，当前设置控件进入前景')
  page['visualPlan'].update(change='总支出原位置附加<4500元，整组等比让位于每天查价开关',exit='保留计算依据与已启用状态')
 ac=page['componentAcceptance'];ac.update(stage='suggestion',status='passed',reviewer='assistant');ac['checks']['corePreserved']=page['referenceChoices'][0]['preserve'];ac['checks']['visualQuality']='实际查看预览核心帧与安装源码；本次暗色结构由用户指定，最终画面另验。';ac['contextSha256']=acceptance_signature(m,page,'suggestion')
(E/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));print('Revision manifest created')
