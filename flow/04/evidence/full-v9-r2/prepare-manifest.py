import pathlib,json,hashlib,sys,os,subprocess,copy
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];L=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk');S=L/'skills/fred-remotion-output/scripts';sys.path.insert(0,str(S));from library_gate import acceptance_signature
from component_distribution import analyze
from common import load_references
rec=lambda p:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
m=json.loads((E.parent/'full-v9/manifest-suggestion-snapshot.json').read_text());m['revision']='full-v9-r2';m['subtitles']['sourcePath']=str(R/'project/src/v9r2/captions.json')
for pg in m['pages']:
 pg.pop('keyframeReview',None)
 for ref in pg['referenceChoices']:
  for key in ['implementation','callSite']:
   path=pathlib.Path(ref[key]['path'].replace('/src/v9/','/src/v9r2/'));ref[key].update(rec(path))
 if pg['implementationMode']=='preserved-media':continue
 ac=pg['componentAcceptance'];ac.update(stage='suggestion',evidence=pg['componentPlan']['inspectedReferences']);ac['checks']['visualQuality']='已核真实组件预览与前版布局；r2只按真实口播新增进入/确认/焦点转移，成片实际帧仍需复核。';ac['contextSha256']=acceptance_signature(m,pg,'suggestion')
_,cat=load_references(L);a=analyze(m,cat);m['componentDistributionReview']['contextSha256']=a['contextSha256']
# Group identity is source family based and unchanged; decisions remain traceable to viewed overview.
p=E/'manifest.json';p.write_text(json.dumps(m,ensure_ascii=False,indent=2));(E/'manifest-suggestion-snapshot.json').write_bytes(p.read_bytes())
env=os.environ.copy();env['PATH']='/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin:'+env['PATH'];env['NODE_OPTIONS']='--require='+str(E.parent/'sample-v8/resolve-existing-typescript.cjs')
for name,args in [('gate-suggestion',['library_gate.py','--stage','suggestion','--output',str(E/'gate-suggestion.json')]),('workflow-planning',['workflow.py','--stage','planning'])]:
 r=subprocess.run([sys.executable,str(S/args[0]),'--manifest',str(p),*args[1:]],capture_output=True,text=True,env=env);(E/(name+'.log')).write_text(r.stdout+r.stderr);print(name,r.returncode,r.stdout);assert r.returncode==0
