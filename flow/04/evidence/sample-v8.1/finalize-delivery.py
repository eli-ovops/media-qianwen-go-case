import pathlib,json,hashlib,subprocess,datetime
E=pathlib.Path(__file__).resolve().parent;R=E.parents[1]
def rec(p):
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
idx=json.loads((E/'frame-index.json').read_text())
native=[111,354,365,390,546,558,759]
viewed=sorted(set(f['frame'] for f in idx['frames'])|set(native))
boards=[E/f'{name}-{i:02}.jpg' for name,count in [('overview',6),('dock-dense',2),('gather-dense',3),('handoff-dense',3),('toggle-dense',3)] for i in range(1,count+1)]
visual={'at':now,'video':rec(R/'output/sample-motion-v8.1.mp4'),'reviewer':'04 assistant','method':'Actual final-export contact sheets plus native PNG inspection; not continuous audiovisual viewing','viewedUniqueFrames':len(viewed),'totalFrames':816,'omittedFrames':816-len(viewed),'viewedFrameNumbers':viewed,'coverage':idx['groups'],'nativeFramesViewed':native,'boardsViewed':[rec(p) for p in boards],'nativeEvidence':[rec(E/'final-frames'/f'native-f{n:03}.png') for n in native],'comparisonScreenshot':rec(E/'comparison-player.png'),'findings':['报价、优惠和服务对象在5.7–6.5s连续帧中保留，未再出现v8退修的清空后替换。','原计算组收束后保留，原结果附预算条件；9.1/9.3s旧标题未再撞顶部小字。','原尺寸关键帧中正文、符号、服务语义图形可读；稳定态未发现文字裁切或遮挡字幕。','总支出、预算阈值与反馈在进入遮罩过程中短暂呈现部分文字，稳定态完整；保留给PMO判断此揭示方式是否自然。','提醒开关与反馈沿顺序出现，反馈注明案例流程示意与非真实通知。'],'directListening':False,'continuousRealtimeAV':False,'visualAcceptance':'PENDING_PMO','userStyleConfirmation':'PENDING'}
save(E/'visual-review.json',visual)
df=subprocess.run(['df','-k',str(R),'/Users/USER'],capture_output=True,text=True,check=True).stdout;(E/'df-end.txt').write_text(df)
du=subprocess.run(['du','-sk',str(E),str(R/'project/src/v81'),str(R/'output/sample-motion-v8.1.mp4')],capture_output=True,text=True,check=True).stdout;(E/'scoped-du-end.txt').write_text(du)
def available(s):return {line.split()[-1]:int(line.split()[3]) for line in s.splitlines()[1:] if len(line.split())>=9}
start=available((E/'df-start.txt').read_text());end=available(df)
save(E/'disk-summary.json',{'beforeKiB':start,'afterKiB':end,'availableDeltaKiB':{k:end[k]-v for k,v in start.items() if k in end},'note':'Shared filesystem change, not attributable solely to this task; no files deleted, no space-release claim. Scoped du taken before final metadata writes.'})
baseline=[]
for v,sha in [('v7','143e33da6d75e006cca780b9badcbdf2a59561a27374b6fb7aa3e3c64cbae837'),('v8','2ea32be0211d5cdde889da2942f44d805aead2537820d0046e04e9033a38ec3d')]:
 d=rec(R/f'output/sample-motion-{v}.mp4');d['unchangedFromPriorReceipt']=d['sha256']==sha;assert d['unchangedFromPriorReceipt'];baseline.append(d)
checks={n:rec(E/n) for n in ['technical-qa.json','visual-review.json','clock-lint.json','gate-suggestion.json','manifest-suggestion-snapshot.json','gate-keyframes.json','workflow-planning.stdout.json','workflow-representative.stdout.json','motion-audit.json','player-check.json','disk-summary.json','manifest.json']}
for n in ['clock-lint.json','gate-suggestion.json','gate-keyframes.json','workflow-planning.stdout.json','workflow-representative.stdout.json','player-check.json']:assert json.loads((E/n).read_text())['status']=='PASS'
report=R/'sample-review-v8.1.md'
with report.open('a') as f:f.write('''
## 最终导出检查（2026-10-14）

最终MP4为1080×1920、60fps、13.6秒、816帧，1,456,919字节；SHA256 `b82e98437d0018b47e9010346e4087887b1edaea1d1eeda6597880b72410c1a8`。FFmpeg整段解码成功；PTS连续，最大舍入差0.00003334秒。v7/v8原文件SHA与先前回执相同。

原声比较：冻结WAV652,800采样；AAC解码多512个尾部填充采样，共同比较区间相关系数0.999970187，±1ms范围最优滞后0采样。此项是信号对齐检查，未直接听音。

实际查看17张最终导出图册：全区间每6帧抽1帧及末帧，另以60fps连续帧核3.6–4.25、5.7–6.5、8.8–9.9、11.6–12.7秒。再查看7张原尺寸帧111/354/365/390/546/558/759及对照页截图。共321/816不同帧，495帧未查看；具体编号及SHA见visual-review.json。抽查未发现稳定态正文或字幕被裁切/遮挡；标题接缝已修。揭示动画中部分文字暂被遮罩属于当前设计，已记录供PMO判断，不能据此宣称美感通过。

clock lint、library suggestion/keyframes、workflow planning/representative均实际PASS；均为执行者自检，不替代PMO或用户确认。motion audit无阻断，保留2项警告：2.6–6.3秒nonstop（费用入位及结果形成），6.3–8.7秒hold-warn（阅读计算结果），无allow豁免。不得把这两项描述成已经获PMO接受。

本地对照页加载、同区间seek、±1帧、0.5倍播放与v7偏移检查PASS；实测半速对照偏差8.154ms，v7对应偏差约1微秒。仅为播放器功能检查，未完成实时连续看听。完整片、05与用户风格确认均未放行。

容量前后df、限定目录du及新增文件精确清单分别在evidence/sample-v8.1/disk-summary.json、scoped-du-end.txt、new-files-inventory.json。没有删除文件；df变化属于共享文件系统，不归因成本任务释放。

交付状态：材料已完成，待PMO审原件。主动报告发送状态及真实工具回执以sample-delivery-v8.1.json和pmo-report-receipt.json为准；工具发送、PMO阅读与验收分别记录。
''')
delivery={'content_id':'qianwen-go-case-20261013','version':'v8.1','at':now,'ownerThreadId':'01a11a6f-49ef-7653-934a-4312979fd4e7','pmoThreadId':'01a11194-c40d-7bf0-8396-5bb5d6449444','status':'MATERIAL_READY_PMO_REVIEW_PENDING','scope':'费用计算→设置提醒13.6秒，黑底语义组件返修','video':rec(R/'output/sample-motion-v8.1.mp4'),'comparison':rec(R/'sample-review-v8.1.html'),'report':rec(report),'source':[rec(p) for p in [R/'project/src/v81/CostReminder.tsx',R/'project/src/v81/Entry.tsx',R/'project/render-sample-v81.cjs']],'reusedBaselines':baseline,'checks':checks,'skills':['fred-remotion-output','frame-smith','remotion-best-practices'],'selectedSourceComponents':['OP09','C005','N044'],'visualCoverage':{'viewedUniqueFrames':321,'total':816,'omitted':495},'motionWarnings':json.loads((E/'motion-audit.json').read_text())['findings'],'limits':{'continuousRealtimeAV':False,'directListening':False,'PMOAccepted':'PENDING','userStyleConfirmed':'PENDING','fullFilmReleased':False,'stage05Released':False},'reporting':{'toolSent':'NOT_YET','PMORead':'UNKNOWN','PMOAccepted':'PENDING'},'inventoryPath':str(E/'new-files-inventory.json')}
save(R/'sample-delivery-v8.1.json',delivery)
print(json.dumps({'video':delivery['video'],'viewed':len(viewed),'disk':json.loads((E/'disk-summary.json').read_text()),'baselinesPreserved':True},ensure_ascii=False))
