import json,pathlib,urllib.request,hashlib,concurrent.futures
r=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk');d=pathlib.Path(__file__).parent; routes=json.loads((r/'library/routes.json').read_text());media=json.loads((r/'library/media-manifest.json').read_text())['files'];refs={}
for n in ['tools','requirements','execution','outro']:
 for e in json.loads((d/f'{n}-top3.json').read_text())['entries']:refs[e['candidateId']]=e
jobs=[]
for id,e in refs.items():
 for i,k in enumerate(e['previews'][0]['keyframes']):
  rp=routes[k['url']]; record=media.get(rp,{});sha=record.get('sha256');local=r/rp
  if not sha and k['url'].startswith('http'):sha=pathlib.Path(k['url']).stem
  url=k['url'] if k['url'].startswith('http') else 'https://www.fred-fu.com/visual-library-app/objects/'+sha+'.jpg' if sha else None
  jobs.append((id,i,local,url,sha))
def run(job):
 id,i,local,url,sha=job;p=d/'references'/f'{id}-{i}.jpg';out={'id':id,'index':i,'url':url,'path':str(p.resolve()),'expectedSha256':sha}
 try:
  if local.exists():data=local.read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=25) as res:data=res.read(2000000)
  actual=hashlib.sha256(data).hexdigest()
  if sha and actual!=sha:raise ValueError('SHA mismatch')
  p.write_bytes(data);out.update(status='verified',sha256=actual,bytes=len(data))
 except Exception as e:out.update(status='blocked',error=str(e))
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:out=list(ex.map(run,jobs))
(d/'references/fetch-receipt.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
