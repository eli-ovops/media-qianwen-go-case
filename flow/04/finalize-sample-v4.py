from pathlib import Path
import json,datetime,subprocess
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v4'
qa=json.loads((E/'qa.json').read_text());scope=json.loads((E/'read-scope.json').read_text());frames=json.loads((E/'frame-player-check.json').read_text());player=json.loads((E/'comparison-player-check.json').read_text());source=json.loads((R/'evidence/sample-export.json').read_text())
assert scope['assistant_viewed'] and qa['audio_decoded_pcm_identical_to_v1'] and frames['dayPlayback'] and frames['rate']==.5 and not frames['media']['error'] and not player['mediaErrors'] and all(x['loaded'] for x in player['images'])
d={'content_id':'qianwen-go-case-20261013','version':'sample-motion-v4','at':datetime.datetime.now().astimezone().isoformat(),'owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','pmo_thread_id':'01a11194-c40d-7bf0-8396-5bb5d6449444','status':'INTERNAL_PMO_VISUAL_REVIEW_PENDING','user_preview':'WITHHELD_PENDING_PMO_VISUAL_ACCEPTANCE','sample':str(R/'output/sample-motion-v4.mp4'),'review':str(R/'sample-review-v4.md'),'comparison':str(R/'comparison-v3-v4.html'),'frame_review':str(R/'tail-frame-review-v4.html'),'changed_interval_seconds':[13,21.8],'first13_seconds':'v3 reused; no new visual read of unaffected interval','raw_source':source['raw_source'],'raw_video_seconds':source['raw_video_seconds'],'qa':qa,'visual_scope':scope,'routing':json.loads((E/'start-receipt.json').read_text()),'full_film':'PAUSED','stage05':'NOT_RELEASED','report':{'tool_sent':'PENDING','pmo_received':'UNKNOWN','pmo_acceptance':'PENDING'}}
(R/'sample-delivery-v4.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
report=f'''# v4局部退修候选 · PMO先验收

2026-10-13。04唯一Owner按PMO样片v3审阅的两点修订。保留0—13秒原画面、21.8秒原声和原字幕；只重渲染13—21.8秒，不扩整片，不直接展示给用户。

入口：[修订区间动态与原尺寸逐帧](tail-frame-review-v4.html) · [v3/v4同步对照](comparison-v3-v4.html) · [MP4](output/sample-motion-v4.mp4) · [机器索引](sample-delivery-v4.json)。

## 两点对应修改

1. 汇总不再14秒收完动作后等到17秒。13.30—15.32秒费用层持续压合，跟随“计算清楚/最后给价格估算”；15.48—16.60秒合成盘从商品底部移出并立起为估算对象，16.6—17.18秒短留后接报价。保留已认可的优惠抽离、服务层加入和主体比例；冰箱只为腾出估算对象位置向左移，末段缩放仍沿v3的0.90。
2. 取消扫描冰箱与围绕家电的日月。原合成费用盘留场，两个带¥—的小报价票据先后进入该盘；放大镜检查同一估算对象，第一轮画出回查路径，第二轮后进入“若条件成立”分支。同一高亮信号从估算盘流经需求、预算两个关口，逐个勾选后连接铃铛。铃铛没有独立提前出现，检查对象和通路在画面里接续。

¥—没有填具体金额；¥4,500仅为条件阈值。报价、勾选和铃铛均为逻辑示意，非真实价格检查或通知回执。短标签辅助辨认，没有恢复大文字卡或用转圈填时长。仍为二维SVG图解，不宣称真实3D。

## 实际检查与限制

最终导出21.8秒，1080×1920/60fps，1308帧，H264/AAC，{qa['bytes']:,}字节；SHA256 `{qa['sha256']}`。源③29.0966667—50.8966667秒。全解码exit0、时间戳递增，原声解码PCM与v1相同（因此也与已核v2/v3相同），{qa['native_loudness_lufs']} LUFS、{qa['native_true_peak_dbtp']} dBTP。

- 实际查看最终修改区间13.000—21.783秒全部528帧的22张连续接触表，每格180×320；不是528张全部原尺寸查看。
- 原尺寸实际查看13个时点：13.5、14.5、15.5、16.2、16.7、17.5、18.0、18.6、19.1、19.6、20.1、20.6、21.2秒；另看12.9—13.083秒接缝12帧和15.5/18.6/21.2秒三组v3/v4对照。具体清单见evidence/sample-v4/read-scope.json。
- 初版关键帧发现报价票据遮住估算标签，最终版已将标签移至右侧；初版仍保留test-*.png。连续帧用于核对象轨迹、状态连接、遮挡及突变，主观动感仍须PMO独立审原件。
- 两个本地审阅页的静音功能检查有回执：播放/暂停/拖动、两视频同步、声音开关、三张对照图加载、原尺寸前后帧/末帧528、日程段播放、0.5倍。没有直接听音或实时连续看听；不把控件运行等同于动态审美通过。

0—13秒为v3已审部分，本轮不重复视觉扩大检查。该区间拼接时重编码，全片解码有覆盖。全量原片、旧样片、工程及失败中间证据均保留；没有媒体清理、外传、安装、付费或发布。

## 复现与停点

工程project/src/SampleV4.tsx、PhysicalWorldV4.tsx；既有Node执行project/render-sample-v4.cjs tail（在project目录），渲染780—1307帧，采用已验证的单并发PNG模式；qa-sample-v4.py记录拼接与检查。重跑需使用新输出路径，现有脚本在最终MP4已存在时停止，不能覆盖交付。整片render.sh仍暂停。

目标路由Astra/high，版本ROUTING-2026-10-13-v4；实际model/effort/speed UNKNOWN，未修改设置。当前只交PMO待验，完成主动报告后停止，不轮询、不自行放行05或展示候选给用户。
'''
(R/'sample-review-v4.md').write_text(report)
p=R/'README.md';s=p.read_text();a=s.index('当前交付：');b=s.index('\n## 复现');s=s[:a]+'''当前交付：**21.8秒样片v4局部退修候选，仅交PMO先验收；不直接给用户看。整片暂停。**

[v4审阅记录](sample-review-v4.md) · [v4索引](sample-delivery-v4.json) · [v3/v4对照](comparison-v3-v4.html) · [13秒后连续帧](tail-frame-review-v4.html)。

v3改善确认但两点退修：汇总节奏及查价条件因果。v4仅修这两点，未自行视觉PASS，05未释放。v1—v3、原片、工程保留。以下旧整片复现命令保留，当前不执行。
''' +s[b:];p.write_text(s)
files=[]
for p in E.rglob('*'):
 if p.is_file() and not p.is_symlink():files.append({'path':str(p),'bytes':p.stat().st_size,'source':'v4 render, extraction, browser QA or delivery record','purpose':'PMO review and reproducibility'})
for p in [R/'output/sample-motion-v4.mp4',R/'project/src/SampleV4.tsx',R/'project/src/PhysicalWorldV4.tsx',R/'project/render-sample-v4.cjs',R/'qa-sample-v4.py',R/'finalize-sample-v4.py',R/'sample-v4-design.md',R/'sample-review-v4.md',R/'sample-delivery-v4.json',R/'tail-frame-review-v4.html',R/'comparison-v3-v4.html',R/'project/check-frame-review-v4.cjs',R/'project/check-comparison-v4.cjs']:
 files.append({'path':str(p),'bytes':p.stat().st_size,'source':'v4 local revision','purpose':'delivery, source or QA'})
(E/'delivery-inventory.json').write_text(json.dumps({'files':files,'cleanup':'none; evidence and reproducibility retained'},ensure_ascii=False,indent=2))
(E/'storage-delivery.txt').write_text(subprocess.check_output(['df','-k',str(R)],text=True))
print(json.dumps({'status':d['status'],'sha256':qa['sha256'],'bytes':qa['bytes']}))
