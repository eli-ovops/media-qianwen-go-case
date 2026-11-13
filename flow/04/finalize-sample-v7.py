from pathlib import Path
import json,hashlib,datetime,subprocess
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v7';O=R/'output/sample-motion-v7.mp4'
qa=json.loads((E/'qa.json').read_text());scope=json.loads((E/'read-scope.json').read_text());player=json.loads((E/'frame-player-check.json').read_text());source=json.loads((R/'evidence/sample-export.json').read_text())
assert scope['assistant_viewed'] and qa['audio_decoded_pcm_identical_to_v1'] and player['playback'] and player['synchronizedSeeking'] and player['rate']==.5
assert hashlib.sha256(O.read_bytes()).hexdigest()==qa['sha256']
d={'content_id':'qianwen-go-case-20261013','stage':'04','version':'sample-motion-v7','at':datetime.datetime.now().astimezone().isoformat(),'status':'INTERNAL_PMO_VISUAL_REVIEW_PENDING','owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','sample':str(O),'review':str(R/'sample-review-v7.md'),'comparison_player':str(R/'sample-review-v7.html'),'reference_receipt':str(E/'start-receipt.json'),'raw_source':source['raw_source'],'raw_video_seconds':source['raw_video_seconds'],'qa':qa,'visual_scope':scope,'player_check':player,'full_film':'PAUSED','stage05':'NOT_RELEASED','user_preview':'WITHHELD_PENDING_PMO_VISUAL_ACCEPTANCE','report':{'tool_sent':'PENDING','pmo_received':'UNKNOWN','pmo_acceptance':'PENDING'}}
(R/'sample-delivery-v7.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=R/'sample-review-v7.md';p.write_text(p.read_text()+f"\n## 最终导出检查\n\n规格1080×1920/60fps，21.8秒/1308帧；{qa['bytes']:,}字节。SHA256 `{qa['sha256']}`。全解码成功、PTS递增，PCM与v1原样片一致；{qa['native_loudness_lufs']} LUFS、{qa['native_true_peak_dbtp']} dBTP。实际读图范围见read-scope.json；已实读全段10fps采样218帧、三个60fps连续窗口216帧、15张原尺寸关键帧与4组v6/v7同时间图。播放器同步定位、0.5倍与末帧导航验证通过。未直接听音或实时连续看听；机器与采样证据不能代替流畅度和审美验收。\n\n[当前样片](output/sample-motion-v7.mp4) · [v6/v7同时间与逐帧审阅](sample-review-v7.html) · [交付索引](sample-delivery-v7.json)。\n")
p=R/'README.md';s=p.read_text();a=s.index('当前交付：');b=s.index('\n## 复现');p.write_text(s[:a]+'''当前交付：**21.8秒v7圆润与运动质感候选，PMO待视觉验收。整片暂停，05未释放。**

[v7审阅记录](sample-review-v7.md) · [v7交付索引](sample-delivery-v7.json) · [v6/v7同时间与逐帧审阅](sample-review-v7.html)。

v6的两段过程表达通过PMO局部门槛，用户审美未批准；按最新v7任务重做形体、光影与动作。原片、基线和内部测试保留，不直接开放候选给用户。
'''+s[b:])
files=[p for p in E.rglob('*') if p.is_file() and not p.is_symlink() and 'browser-profile' not in str(p)]
files += [R/x for x in ['output/sample-motion-v7.mp4','project/src/CinematicV7.tsx','project/src/SampleV7.tsx','project/render-sample-v7.cjs','project/check-frame-review-v7.cjs','qa-sample-v7.py','finalize-sample-v7.py','sample-review-v7.md','sample-review-v7.html','sample-delivery-v7.json']]
rows=[{'path':str(p),'bytes':p.stat().st_size,'mtime':p.stat().st_mtime,'source':'v7 local render, derived evidence or reproducible source','purpose':'PMO verification and further revision','keep':True} for p in files]
(E/'file-inventory.json').write_text(json.dumps({'files':rows,'total_bytes':sum(x['bytes'] for x in rows),'scope':'only v7 generated artifacts; no scan of other projects','cleanup':'none; needed for PMO and restoration; no deletion'},ensure_ascii=False,indent=2))
(E/'storage-after.txt').write_text(subprocess.check_output(['df','-k',str(R)],text=True))
print(json.dumps({'sha256':qa['sha256'],'bytes':qa['bytes'],'status':d['status']}))
