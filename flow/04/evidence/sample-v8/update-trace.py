import pathlib,json,hashlib,sys
r=pathlib.Path(__file__).resolve().parent;root=r.parents[1];lib=pathlib.Path('/Users/USER/.codex/skill-repos/FredTalk');sys.path.insert(0,str(lib/'skills/fred-remotion-output/scripts'));from library_gate import acceptance_signature
rec=lambda p:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
p=r/'manifest.json';m=json.loads(p.read_text());c=json.loads((root/'project/src/v8/captions.json').read_text());m['subtitles'].update(sourceSha256=rec(root/'project/src/v8/captions.json')['sha256'],cues=[{'startSeconds':x['start'],'endSeconds':x['end'],'text':x['zh']} for x in c]);m['subtitles']['edgeTrimNote']='Removed preceding id28 only, 0–0.0633s; other cue text and times unchanged from v7 minus8.2s.'
for page in m['pages']:
 sid=page['stableId'];ref=page['referenceChoices'][0]
 if sid=='fees':
  e=json.loads((r/'gather-source.json').read_text())['entries'][0];symbol='OP09';func='CostGather'
 else:
  e=next(x for x in json.loads((r/'reminder-top3.json').read_text())['entries'] if x['candidateId']=='library-new10-n044');symbol='MediaScenesB';func='ProductToReminder'
  page['componentPlan']['candidates'].insert(0,{'id':'fred-wave2-42-t19c','decision':'rejected','reason':'实际3核心帧是Fred动画人物对作品作惊叹短评；本段是设置提醒，人物反应不解释条件和开关，且源码needs-auth，不选。'})
 ref.update(useMode='local',keyAction=ref['preserve'],source={**rec(lib/e['sourceFiles'][0]['path']),'symbol':symbol},implementation={**rec(root/'project/src/v8/CostReminder.tsx'),'symbol':func},callSite={**rec(root/'project/src/v8/CostReminder.tsx'),'symbol':'CostReminder','callee':func})
 page['componentAcceptance']['contextSha256']=acceptance_signature(m,page,'suggestion')
p.write_text(json.dumps(m,ensure_ascii=False,indent=2));print('Source / adapted functions / actual calls bound; candidate T19c rejected from actual inspection')
