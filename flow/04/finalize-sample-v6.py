from pathlib import Path
import json,datetime,subprocess
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v6-final2';now=datetime.datetime.now().astimezone().isoformat()
qa=json.loads((E/'qa.json').read_text());scope=json.loads((E/'read-scope.json').read_text());player=json.loads((E/'frame-player-check.json').read_text());source=json.loads((R/'evidence/sample-export.json').read_text())
assert scope['assistant_viewed'] and qa['audio_decoded_pcm_identical_to_v1'] and player['dayPlayback'] and player['rate']==.5 and not player['media']['error']
d={'content_id':'qianwen-go-case-20261013','version':'sample-motion-v6','at':now,'owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','pmo_thread_id':'01a11194-c40d-7bf0-8396-5bb5d6449444','status':'INTERNAL_PMO_VISUAL_REVIEW_PENDING','user_preview':'WITHHELD_PENDING_PMO_VISUAL_ACCEPTANCE','sample':str(R/'output/sample-motion-v6-final2.mp4'),'review':str(R/'sample-review-v6.md'),'frame_review':str(R/'tail-frame-review-v6.html'),'changed_interval_seconds':[8,21.8],'first8_seconds':'v4 reused; current export sampled and seam checked','raw_source':source['raw_source'],'raw_video_seconds':source['raw_video_seconds'],'qa':qa,'visual_scope':scope,'routing':json.loads((R/'evidence/sample-v6/start-receipt.json').read_text()),'full_film':'PAUSED','stage05':'NOT_RELEASED','report':{'tool_sent':'PENDING','pmo_received':'UNKNOWN','pmo_acceptance':'PENDING'}}
(R/'sample-delivery-v6.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(R/'sample-review-v6.md').write_text(f'''# v6费用构成与重复查价候选 · PMO待验

依据PMO样片v5审阅重做8—21.8秒。前8秒沿用v4，原声和字幕冻结。仅交PMO；整片与05暂停，不直接向用户展示。

[MP4](output/sample-motion-v6-final2.mp4) · [动态/828张原尺寸逐帧页](tail-frame-review-v6.html) · [机器交付索引](sample-delivery-v6.json)。

## 本次变化

费用由实体部件承载：绿色优惠部件从原构成抽离；橙色服务部件分两次从前景进入，实际增加构成；分散部件缩短间距、归整高度、绑合为同一支出估算包。费用段扩大主体，镜头改变角度和尺度；不再用大纸票和压辊换标题表示计算。

估算包持续进入查价段。第1天报价进入并复查→日夜轮转、旧报价离开→次日报价再次进入、再次复查；使用相对日次，没有虚构真实日期。条件成立的图解分支打开两侧挡臂；铃铛处于右上方，估算包及说明留在左下方。没有条件大面板或穿字扫描线。

原始资料未给金额，全部金额为¥—；¥4,500仅为预算。部件大小与数量只用于关系图解，不对应实际金额比例或真实收费项目数量。画面保留此标识；铃铛与日次不代表真实查询/通知已经发生。工程为SVG透视图形，没有安装3D库，不声称真实3D或产品实操。

## 自检与证据

先导出17—21.8秒内部4.8秒试段并实际读取288帧接触表；发现挡臂方向/边缘残留及估算文字交叠后修正，再导出完整21.8秒样片。试段与旧版本保留。首次完整导出连续帧检查还发现服务部件经过说明文字区域，已把服务标签与构成说明移至上方空白区域，并重渲染8—17秒为final版；sample-motion-v6.mp4保留为修正前版本。之后原尺寸检查发现9.8秒重复的“扣除优惠”文字与蓝色部件边缘相叠，移除此行，重渲染8—10.4秒形成final2；旧final保留。

最终规格1080×1920、60fps、1308帧，H264/AAC，{qa['bytes']:,}字节；SHA256 `{qa['sha256']}`。全解码exit0，时间戳递增；原声解码PCM与v1完全相同，{qa['native_loudness_lufs']} LUFS、{qa['native_true_peak_dbtp']} dBTP。

实际读图范围详见[evidence/sample-v6-final2/read-scope.json](evidence/sample-v6-final2/read-scope.json)：上一版final已实际读取8—21.8秒全部828帧接触表（每格180×320）与18张原尺寸关键帧；final2只移除8—10.4秒的一行重叠文字，重新实际读取该修改区间及后接缝共168帧、3张原尺寸关键帧、全样片22张每秒采样及8秒接缝12帧。其余区间沿用上一轮已读证据，不冒称本轮重新读完全部828帧。逐帧页核视频加载、日程播放、0.5倍和末帧导航。未直接听音或按实时速度连续看听；机器播放与接触表不能代替动态审美验收。

本版把变化转成可见部件增减与两轮报价，但仍是抽象图解；是否易懂、空间与镜头是否达到参考风格，由PMO审原件判断，不自行标视觉PASS。

## 复现与边界

工程project/src/CinematicV6.tsx与SampleV6.tsx；project内以既有Node运行render-sample-v6.cjs tail，渲染480—1307帧；再于本目录运行qa-sample-v6.py拼接前480帧并复制原AAC，得到初版；render-sample-v6-label-patch.cjs重新渲染480—1019帧，qa-sample-v6-final2.py用此540帧替换并形成final；render-sample-v6-discount-patch.cjs渲染480—623帧，qa-sample-v6-final2.py拼接为final2。已有输出拒绝覆盖，复现用新路径。逐帧页功能检查project/check-frame-review-v6.cjs。单并发PNG/swangle；无安装、付费、上传、发布、删除。

路由ROUTING-2026-10-13-v4，目标Astra/high，实际model/effort/speed UNKNOWN。主动报告PMO并存回执后停止，不轮询，不自行放行整片或05。
''')
p=R/'README.md';s=p.read_text();a=s.index('当前交付：');b=s.index('\n## 复现');s=s[:a]+'''当前交付：**21.8秒样片v6费用/重复查价候选，仅供PMO先验收；不直接展示用户。整片暂停。**

[v6审阅记录](sample-review-v6.md) · [v6索引](sample-delivery-v6.json) · [动态与连续帧](tail-frame-review-v6.html)。

v5经PMO退修（PMO样片v5审阅.md）；v6已针对费用部件增减、每日重复和遮挡重做，视觉验收待PMO。05未释放。原片及v1—v5保留。以下旧整片命令仅保留，不执行。
'''+s[b:];p.write_text(s)
files=[p for p in E.rglob('*') if p.is_file() and not p.is_symlink() and 'browser-profile' not in str(p)]
files += [R/x for x in ['output/sample-motion-v6.mp4','evidence/sample-v6/tail-8to21.8.mp4','evidence/sample-v6/daily-test-17to21.8.mp4','evidence/sample-v6/cost-label-patch-8to17.mp4','output/sample-motion-v6-final2.mp4','project/src/CinematicV6.tsx','project/src/SampleV6.tsx','project/render-sample-v6.cjs','qa-sample-v6.py','qa-sample-v6-final2.py','project/render-sample-v6-label-patch.cjs','finalize-sample-v6.py','sample-v6-design.md','sample-review-v6.md','sample-delivery-v6.json','tail-frame-review-v6.html','project/check-frame-review-v6.cjs']]
(E/'delivery-inventory.json').write_text(json.dumps({'files':[{'path':str(p),'bytes':p.stat().st_size,'source':'v6 generated render, evidence or project record'} for p in files],'cleanup':'none; original and all prior versions retained'},ensure_ascii=False,indent=2))
(E/'storage-delivery.txt').write_text(subprocess.check_output(['df','-k',str(R)],text=True));print(json.dumps({'status':d['status'],'sha256':qa['sha256'],'bytes':qa['bytes']}))
