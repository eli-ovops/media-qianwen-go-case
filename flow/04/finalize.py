from pathlib import Path
import json,hashlib,subprocess,datetime,os
R=Path(__file__).resolve().parent
qa=json.loads((R/'evidence/final-verified/qa-v1.json').read_text());scope=json.loads((R/'evidence/final-verified/frame-read-scope.json').read_text());player=json.loads((R/'evidence/player-check.json').read_text())
assert scope['viewed_by_assistant'] is True
inputs=json.loads((R/'evidence/input-verification.json').read_text())
for x in inputs:assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']
(R/'evidence/input-unchanged-final.json').write_text(json.dumps({'time':datetime.datetime.now().astimezone().isoformat(),'files':inputs,'all_unchanged':True},ensure_ascii=False,indent=2))
df=subprocess.check_output(['df','-k',str(R)],text=True);(R/'evidence/storage-after.txt').write_text(df)
files=[]
for root,dirs,names in os.walk(R,followlinks=False):
 dirs[:]=[d for d in dirs if not (Path(root)/d).is_symlink()]
 for name in names:
  p=Path(root)/name
  if p.is_symlink() or name in ['file-inventory-v1.json','delivery-v1.json']:continue
  files.append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'purpose':'source/asset' if '/project/' in str(p) else 'QA evidence' if '/evidence/' in str(p) else 'output' if '/output/' in str(p) else 'task/reproduction/receipt'})
(R/'file-inventory-v1.json').write_text(json.dumps({'files':files,'bytes':sum(x['bytes'] for x in files),'dependencies_symlink':str(R/'project/node_modules'),'dependency_target':str((R/'project/node_modules').resolve()),'followed_dependency_symlink':False,'disk_after':df,'retention':'media, project, revision evidence retained for05/user review; known one-time cache cleanup separately recorded'},ensure_ascii=False,indent=2))
d={'content_id':'qianwen-go-case-20261013','stage':'04','version':'candidate-v1','owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','status':'DELIVERED_FOR_PMO_REVIEW','video':str(R/'output/candidate-v1.mp4'),'sha256':qa['sha256'],'bytes':qa['bytes'],'duration_seconds':6122/60,'audio_seconds':102.02,'frames':qa['frames'],'resolution':[1080,1920],'fps':60,'codec':'H264/AAC','cover':str(R/'output/cover-v1.png'),'project':str(R/'project'),'reproduce':str(R/'project/render.sh'),'cut_plan':str(R/'cut-plan.json'),'captions':str(R/'output/captions-bilingual-v1.srt'),'review':str(R/'review.md'),'evidence':{'technical':str(R/'evidence/final-verified/qa-v1.json'),'visual':str(R/'evidence/final-verified/frame-read-scope.json'),'player':str(R/'evidence/player-check.json'),'files':str(R/'file-inventory-v1.json')},'visual_scope':scope,'no_source_background_in_output':True,'source_media_unchanged':True,'routing':{'version':'ROUTING-2026-10-13-v4','requested_model':'gpt-6-astra','requested_effort':'high','actual_model':'UNKNOWN','actual_effort':'UNKNOWN','actual_speed':'UNKNOWN'},'mandatory_fixes_found':[],'unverified':['full-film subjective audio audition','word-perfect subtitle timing','human dynamic/style judgment','05 independent QA and same-version user approval'],'boundary':'No shared status changes, cloud upload, new dependencies, BGM, publishing or downstream wakeup. Full-screen graphics with actual narration; no portrait in this candidate.','report':{'target':'01a11194-c40d-7bf0-8396-5bb5d6449444','tool_send':'PENDING','pmo_received':'UNKNOWN','pmo_accepted':'PENDING'}}
(R/'delivery-v1.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
p=R/'README.md';s=p.read_text().replace('成片预计入口','已导出候选').replace('，生成完成前不视为交付','，待PMO及05/用户审片');p.write_text(s)
p=R/'review.md';s=p.read_text().replace('当前：制作中，未交付、未自评PASS。','当前：candidate-v1已导出并完成列明自查，待PMO审原件；未自评PASS。');s+='\n## 最终MP4检查\n\n'+f"{qa['frames']}帧，1080×1920/60fps，时间线{6122/60:.6f}秒。全解码exit0、PTS严格递增。音轨与剪辑参考逐秒相关性最低{qa['min_correlation']:.7f}，峰值{qa['peak_dbfs']:.3f}dBFS，满幅样本{qa['clipped_samples']}。全片响度原文在qa-v1.json；实际视频SHA `{qa['sha256']}`。\n\n"+'最终图像读取范围、发现及限制在frame-read-scope.json，未把设计图代替最终MP4。浏览器以默认静音实测元数据、78.5秒定位、播放推进与暂停；未发声，未假称全片听感已通过。源原片SHA前后不变。\n';p.write_text(s)
print(json.dumps({'video':d['video'],'sha256':d['sha256'],'files':len(files),'total_bytes':sum(x['bytes'] for x in files)},ensure_ascii=False))
