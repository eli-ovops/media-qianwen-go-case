from pathlib import Path
import json,hashlib,sys,os,subprocess
E=Path(__file__).resolve().parent;R=E.parents[1];L=Path('/Users/USER/.codex/skill-repos/FredTalk');S=L/'skills/fred-remotion-output/scripts';sys.path.insert(0,str(S))
from library_gate import acceptance_signature
from component_distribution import analyze
from common import load_references
rec=lambda p:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
m=json.loads((E.parent/'full-v9-r2/manifest.json').read_text())
def update(x):
 if isinstance(x,str):
  x=x.replace('/src/v9r2/','/src/v9r3c/')
  for n in ['bridge-safe','opinion-safe','close-safe']:x=x.replace('/public/v9/'+n,'/public/v9r3-final/'+n)
  return x
 if isinstance(x,list):return [update(a) for a in x]
 if isinstance(x,dict):
  x={k:update(v) for k,v in x.items()}
  if 'path' in x and 'sha256' in x and Path(x['path']).is_file():x['sha256']=rec(Path(x['path']))['sha256']
  return x
 return x
m=update(m);m['revision']='v9-r3c';m['updatedTask']='bounded portrait repair with authorized existing-content coverage from97.3s';m['baselineManifest']=rec(E.parent/'full-v9-r2/manifest.json')
selected={'tools':[1406],'requirements':[2400],'execution':[3600,3864],'fees':[4474],'reminder':[4761],'outro':[5200,5830,5896,6021]}
for pg in m['pages']:
 if pg['stableId']=='close':pg['durationInFrames']=62;pg['componentPlan']['decisionReason']='保留96.27–97.3真人，后段按PMO明确允许由既有AI内容画面接管；保留完整原声。'
 if pg['stableId'] not in selected:continue
 frames=[dict(rec(E/'final-frames'/f'f{f:04d}.png'),timeSeconds=f/60) for f in selected[pg['stableId']]]
 pg['keyframeReview']={'status':'assistant-inspected','userConfirmation':'PENDING_PMO_FIRST','frames':frames,'sourceFiles':[rec(R/'project/src'/n) for n in ['v9r3c/Film.tsx','v9r3c/CostScene.tsx','v9r3c/Entry.tsx','v9r3c/captions.json','v8/theme.ts','v8/CostReminder.tsx']],'scope':'Current final MP4 sampled frames; limited portrait repair, source equivalence verified. No continuous audiovisual/direct listening claim.'}
 ac=pg['componentAcceptance'];ac.update(stage='keyframes',evidence=frames);ac['checks']['visualQuality']='实看当前最终MP4对应原生关键帧的图板；语义组件与原版保持，修正真人与结尾既有内容接管。无新增免责声明。全片连续视听仍待验。'
 if pg['stableId']=='outro':
  ac['checks']['semanticFit']='查问整理任务交给AI，结尾真人短接后用既有AI节点承接原声，最后决定留给自己。'
 ac['contextSha256']=acceptance_signature(m,pg,'keyframes')
for row in m['componentDistributionReview']['decisions']:
 row['evidence']=[rec(E/'native-keys-01.jpg'),rec(E/'native-keys-02.jpg')]
 for c in row.get('comparisons',[]):
  if c.get('stableId')=='outro':c['visibleState']='三个任务卡收向AI，短接真人后97.3秒返回既有AI节点；最后决定文字保留。'
_,cat=load_references(L);m['componentDistributionReview']['contextSha256']=analyze(m,cat)['contextSha256']
(E/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E.parent/'sample-v8/resolve-existing-typescript.cjs')
a=[sys.executable,str(S/'library_gate.py'),'--manifest',str(E/'manifest.json'),'--stage','keyframes','--output',str(E/'gate-keyframes.json')]
r=subprocess.run(a,capture_output=True,text=True,env=env);(E/'gate-keyframes.log').write_text(r.stdout+r.stderr);print(r.returncode,r.stdout,r.stderr);assert r.returncode==0
