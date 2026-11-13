import pathlib,json,hashlib,datetime,subprocess
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1];E1=E.parent/'full-v9';P=R/'project'
rec=lambda p:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
qa=json.loads((E/'technical-qa.json').read_text());visual=json.loads((E/'visual-review.json').read_text());motion=json.loads((E/'motion-review.json').read_text());player=json.loads((E/'player-check.json').read_text());gate=json.loads((E/'gate-keyframes.json').read_text())
assert qa['decodedFrames']==6122 and player['status']=='PASS' and gate['status']=='PASS'
assert visual['reviewCompleted'] and motion['reviewCompleted']
changes=[v['path'] for v in json.loads((E/'render-inputs.json').read_text())['files'] if rec(pathlib.Path(v['path']))['sha256']!=v['sha256']];assert not changes
files=[R/'output/qianwen-go-full-v9-r2.mp4',R/'output/captions-bilingual-v9.srt',R/'full-review-v9-r2.html',R/'完整成片-v9复现.md',E/'manifest.json',P/'src/timeline.json',E/'technical-qa.json',E/'visual-review.json',E/'motion-review.json',E/'player-check.json',E1/'raw-audio-audit.json',E1/'preservation-check.json']
data={'content_id':'qianwen-go-case-20261013','version':'full-v9-r2','createdAt':datetime.datetime.now().astimezone().isoformat(),'ownerThreadId':'01a11a6f-49ef-7653-934a-4312979fd4e7','pmoThreadId':'01a11194-c40d-7bf0-8396-5bb5d6449444','authorization':rec(R/'完整成片制作-v9任务.md'),'status':'04_DELIVERED_PENDING_PMO_AND_05','technical':qa,'visualScope':visual,'motionReview':motion,'gates':{'libraryKeyframes':gate['status'],'player':player['status'],'pmoAcceptance':'PENDING','stage05':'NOT_RELEASED_BY_04','continuousAudiovisual':'NOT_PERFORMED','directListening':False},'artifacts':[rec(p) for p in files],'renderInputChanges':changes,'restrictions':'No private upload, publication, music addition, TTS, installation or deletion. Source originals and approved v8.1 preserved.','pmoReport':{'toolSend':'PENDING','pmoRead':'UNKNOWN','pmoAcceptance':'PENDING'}}
(R/'完整成片-v9交付索引.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
a=qa['audio'];video=qa['video'];vcount=visual['uniqueFullFramesReviewed'];fcount=visual['captionCropsReviewed'];report=f'''# 千问 Go 完整成片 v9｜04交付

2026-10-14。**最终候选为v9-r2，已完成04制作与本轮自查，交PMO待验；不代表05或用户终审通过。**

[完整成片](output/qianwen-go-full-v9-r2.mp4) · [本地审片页](full-review-v9-r2.html) · [双语字幕](output/captions-bilingual-v9.srt) · [复现入口](完整成片-v9复现.md) · [机器可读索引](完整成片-v9交付索引.json)

## 输出与内容

- 1080×1920，60fps，6122帧，视频时长102.033333秒（容器元数据可四舍五入为102.034秒）。H.264/AAC，原声，无BGM/SFX/TTS。
- 文件大小：{video['bytes']:,}字节；SHA-256：`{video['sha256']}`。
- 延续用户批准v8.1的近黑底、亮色语义图形与圆润动效；开场、案例桥接、观点和结尾用真实本人原片。费用与提醒段保持v8.1动作关系，移除用户拒绝的说明及ELI角标。
- 公开案例措辞保留；4500仍是预算，店铺A/B/C是抽象询价关系，不虚构成交/真实送达，不把案例写成本人亲测。原画面未加入替代免责声明。
- 第一轮v9检查发现较长静止区间后，只修箭头/结果分开进入、冰箱/双十一进入、条件确认、型号确认与结尾任务焦点。原声、43条字幕及CostScene未变。第一轮文件与工程保留，最终使用`project/src/v9r2/`。

## 实际检查

全6122帧FFmpeg解码成功，最大PTS记录误差{qa['maxPTSErrorSeconds']:.7f}秒；该误差含showinfo文本时间戳舍入。最终AAC对拼接原声相关系数{a['correlationAtZeroLag']:.8f}，四段测得最佳时间偏移均为0采样（±1ms搜索窗口）。四段响度差{a['loudnessRangeAcrossSectionsLU']:.2f} LU，最大真峰值{max(v['truePeakDBTP'] for v in a['sections']):.2f} dBTP。

原片到voice.wav全部6个保留区间已核PCM对应，相关系数均超过0.999999；内部空白共移除0.93秒，无调速或删掉已说句子。边缘4ms淡化与静态增益沿用已核剪辑方案。此项是信号/时间检查，不替代听感或逐字准确率。

本轮实际读过{vcount}个不同的完整导出画面（包含全片1fps、接缝10fps、需求进入10fps、费用/提醒10fps、真人5fps与关键帧），另读{fcount}条原尺寸字幕裁条。完整画面未读帧数{6122-vcount}；逐帧解码不算视觉阅读。机器动效标记逐项解释见`evidence/full-v9-r2/motion-review.json`，没有把工具阈值直接当观感验收。播放器实测加载、11个时间点seek、±1帧和短播放通过。

来源组件选择与AST实际调用绑定、关键帧门禁通过，证据为真实组件预览/来源文件/本片实际帧。门禁通过不替代PMO或05验收。

## 保留的限制与下一步

1. **没有实时连续看听，也没有本轮直接听音。** 专名“推出千问Go”沿03用户核听确认；原声信号、字幕时间与采样图不能证明所有语气、句首尾主观听感及连续视听节奏。需PMO顺序交05复核与用户终审。
2. 真人背景使用Apple Vision本地逐帧遮罩，采样中未看到私有屏幕/相框。原片④本身上方头发出框，完整保留源画幅也不能恢复；额头、下巴可见。眼镜外缘存在局部断裂，个别手指轮廓有遮罩损失，100.35秒附近有少量灰色椅背残留。未宣称无损、背景像素全部消失或全部6122帧视觉检查。
3. 原片、v8.1和第一轮v9均保留；没有上传、发布、安装、付费或删除。唯一共享流程状态由PMO维护，04没有自行放行05。

规则：ROUTING-2026-10-13-v4；目标模型gpt-6-astra/high，实际模型/effort/speed工具回执不可核，记UNKNOWN。主动回报另存工具真实回执；发送成功、PMO已读和PMO验收分别记录。
'''
(R/'完整成片-v9交付报告.md').write_text(report)
p=R/'README.md';s=p.read_text().replace('第二次渲染与最终自检进行中，PMO/05未验收。','最终候选v9-r2已完成制作与本轮自查，PMO/05待验。');s=s.replace('当前授权：','[v9交付报告](完整成片-v9交付报告.md) · [v9交付索引](完整成片-v9交付索引.json) · [v9复现](完整成片-v9复现.md)\n\n当前授权：');p.write_text(s)
(E/'df-end.txt').write_bytes(subprocess.run(['df','-k','/Volumes/EXTERNAL','/System/Volumes/Data'],capture_output=True,check=True).stdout)
roots=[E1,E,P/'src/v9',P/'src/v9r2',P/'public/v9'];paths=[p for root in roots for p in root.rglob('*') if p.is_file() and p.name!='artifact-inventory.json'];paths+= [P/'render-full-v9.cjs',P/'render-full-v9-r2.cjs',R/'full-review-v9.html',R/'full-review-v9-r2.html',R/'output/qianwen-go-full-v9.mp4',R/'output/qianwen-go-full-v9-r2.mp4',R/'output/captions-bilingual-v9.srt',R/'完整成片-v9交付报告.md',R/'完整成片-v9交付索引.json',R/'完整成片-v9复现.md'];paths=sorted(set(paths));rows=[{'path':str(p),'bytes':p.stat().st_size} for p in paths];(E/'artifact-inventory.json').write_text(json.dumps({'scope':'v9 task-created files within exact listed roots; bundle contains generated copies of existing inputs; sizes are logical bytes, not disk-space freed','roots':[str(p) for p in roots],'count':len(rows),'logicalBytes':sum(v['bytes'] for v in rows),'deleted':[],'files':rows},indent=2))
print(json.dumps({'video':video,'reviewedFullFrames':vcount,'artifacts':len(rows),'logicalBytes':sum(v['bytes'] for v in rows)},indent=2))
