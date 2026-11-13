from pathlib import Path
import json,datetime,subprocess
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v5-final';now=datetime.datetime.now().astimezone().isoformat()
qa=json.loads((E/'qa.json').read_text());scope=json.loads((E/'read-scope.json').read_text());player=json.loads((E/'frame-player-check.json').read_text());source=json.loads((R/'evidence/sample-export.json').read_text())
assert scope['assistant_viewed'] and qa['audio_decoded_pcm_identical_to_v1'] and player['dayPlayback'] and player['rate']==.5 and not player['media']['error']
d={'content_id':'qianwen-go-case-20261013','version':'sample-motion-v5','at':now,'owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','pmo_thread_id':'01a11194-c40d-7bf0-8396-5bb5d6449444','status':'INTERNAL_PMO_VISUAL_REVIEW_PENDING','user_preview':'WITHHELD_PENDING_PMO_VISUAL_ACCEPTANCE','sample':str(R/'output/sample-motion-v5-final.mp4'),'review':str(R/'sample-review-v5.md'),'frame_review':str(R/'tail-frame-review-v5.html'),'changed_interval_seconds':[8,21.8],'first8_seconds':'v4 source reused; seam reviewed, remaining unchanged interval not visually reread','raw_source':source['raw_source'],'raw_video_seconds':source['raw_video_seconds'],'qa':qa,'visual_scope':scope,'routing':json.loads((R/'evidence/sample-v5/start-receipt.json').read_text()),'full_film':'PAUSED','stage05':'NOT_RELEASED','report':{'tool_sent':'PENDING','pmo_received':'UNKNOWN','pmo_acceptance':'PENDING'}}
(R/'sample-delivery-v5.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(R/'sample-review-v5.md').write_text(f'''# v5尾段镜头重组候选 · 仅供PMO先验

按PMO样片v4审阅重做8—21.8秒；前8秒复用v4，原声与字幕冻结。整片暂停，05未释放；不直接向用户展示候选。

入口：[动态与原尺寸逐帧](tail-frame-review-v5.html) · [MP4](output/sample-motion-v5-final.mp4) · [机器索引](sample-delivery-v5.json)。

## 对应重组

- 8—13.2秒：商品费用单近景，绿色优惠联向左抽离、纸张缩短；镜头拉远，服务小车驶入，橙色搬旧/安装费用联进入费用单。主体不再是常驻冰箱。
- 13.2—17.2秒：压辊经过费用单，正向近景变成支出估算单，再随估算单缩小移动进入查价桌面。短暂落定服务于“价格估算”的辨认。
- 17.2—21.8秒：日历两次翻页、报价先后进入；估算单继续移入需求和预算条件挡板，条件成立的示意分支才打开挡片，镜头随估算单移向桌面铃铛并触发按压。移除固定章节编号、冰箱、圆盘、勾选连线。条件阈值保留¥4,500；报价和估算不填虚构数字。

使用二维SVG拟物与镜头平移、景别变化；不宣称真实3D、真实软件操作、价格核验或通知。挡板与铃铛仍是图解物件，是否已充分摆脱PPT感由PMO审原件决定。

## 实际验证

导出21.8秒、1080×1920、60fps、1308帧、H264/AAC，{qa['bytes']:,}字节。SHA256 `{qa['sha256']}`。全解码exit0，PTS递增；原声解码PCM与v1完全相同，{qa['native_loudness_lufs']} LUFS、{qa['native_true_peak_dbtp']} dBTP。音频相同不代表本轮直接听过。

本轮实际查看范围记录于[evidence/sample-v5-final/read-scope.json](evidence/sample-v5-final/read-scope.json)：先查看本轮初次导出8—21.8秒全部828帧的35张接触表；修复服务联交接后，最终版定向重看11.2—12.783秒96帧的4张接触表，每格180×320。最终版另看18个1080×1920关键原图、8秒接缝12帧及4组v4/v5对照；其余连续帧未重复全量查看。没有直接听音或实时连续看听，不能把接触表等同动态审美验收。

自检修正：优惠虚线不再穿字；服务费用与条码分开；日历退出条件近景，条件说明避开亮纸；估算单持续承接新报价和提醒，不将原估算对象丢弃；末尾估算标题抬高避开铃铛主体。连续帧另发现服务费用联重复，已在11.2—12.4秒改为同一费用联落位后交接，旧导出保留为sample-motion-v5.mp4。最终观察详见read-scope，不自行标视觉PASS。

审阅页已做静音功能检查：逐帧前后、末帧828、日程播放、0.5倍、媒体元数据和截图。功能播放不等于直接听音或主观动态通过。

## 复现与边界

工程project/src/CinematicV5.tsx与SampleV5.tsx；在project以既有Node执行render-sample-v5.cjs tail，渲染480—1307帧；qa-sample-v5.py先拼接前480帧并拷贝原AAC；随后render-sample-v5-handoff.cjs重渲染672—743帧，qa-sample-v5-final.py替换此72帧形成最终版。已有输出时脚本拒绝覆盖，复跑须新路径。采用已验证单并发PNG/swangle，不安装依赖、不改媒体工具。

保留原片、旧版、测试帧与全部工程，无删除、上传或发布。路由规则ROUTING-2026-10-13-v4，目标Astra/high，实际model/effort/speed UNKNOWN。完成工具报告后停止，不轮询PMO，不自行放行05或整片。
''')
p=R/'README.md';s=p.read_text();a=s.index('当前交付：');b=s.index('\n## 复现');s=s[:a]+'''当前交付：**21.8秒样片v5尾段镜头重组候选，仅交PMO先验收；不直接展示用户。整片暂停。**

[v5审阅记录](sample-review-v5.md) · [v5索引](sample-delivery-v5.json) · [8秒后动态与连续帧](tail-frame-review-v5.html)。

v4因仍有PPT感被PMO退修；v5重做8—21.8秒，未自行视觉PASS，05未释放。原片及v1—v4保留。以下旧整片复现命令保留，当前不执行。
'''+s[b:];p.write_text(s)
files=[p for p in E.rglob('*') if p.is_file() and not p.is_symlink() and 'browser-profile' not in str(p)]
files += [R/x for x in ['output/sample-motion-v5-final.mp4','project/src/CinematicV5.tsx','project/src/SampleV5.tsx','project/render-sample-v5.cjs','qa-sample-v5.py','qa-sample-v5-final.py','project/render-sample-v5-handoff.cjs','finalize-sample-v5.py','sample-v5-design.md','sample-review-v5.md','sample-delivery-v5.json','tail-frame-review-v5.html','project/check-frame-review-v5.cjs']]
(E/'delivery-inventory.json').write_text(json.dumps({'files':[{'path':str(p),'bytes':p.stat().st_size,'source':'v5 render, extraction, source or delivery record'} for p in files],'cleanup':'none; browser profile retained separately under evidence/sample-v5-final/frame-browser-profile'},ensure_ascii=False,indent=2))
(E/'storage-delivery.txt').write_text(subprocess.check_output(['df','-k',str(R)],text=True));print(json.dumps({'status':d['status'],'sha256':qa['sha256'],'bytes':qa['bytes']}))
