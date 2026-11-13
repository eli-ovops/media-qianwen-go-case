from pathlib import Path
import json,re,datetime,hashlib
R=Path(__file__).resolve().parent;E=R/'evidence/cleanup-20261015';result=json.loads((E/'result.json').read_text());plan=json.loads((E/'plan.json').read_text());deleted={x['path'] for x in result['deleted']};names={str(Path(p).relative_to(R)) for p in deleted};at=datetime.datetime.now().astimezone().isoformat();report=R/'发布后视频清理-20261015报告.md'
availability={'at':at,'status':'POST_PUBLICATION_GENERATED_VIDEOS_CLEANED','latestLocalFinalExists':False,'latestFinalHistoricalPath':str(R/'output/qianwen-go-full-v9-r3c.mp4'),'latestFinalSHA256':'797426b66fec27431ecf298b9df67f9869b2cddfaa456b1c851009dd6b84ab10','deletedCount':len(deleted),'report':str(report),'exactList':str(E/'准确路径清单.md'),'reproduce':'完整成片-v9复现.md#发布后重导出说明2026-10-15','historicalRecords':'Original paths/SHA and checks are historical; deleted video paths are no longer usable downloads.'}
changed=[]
for p in list(R.glob('sample-delivery-*.json'))+list(R.glob('完整成片-*交付索引.json')):
 d=json.loads(p.read_text());d['currentLocalAvailability']=availability;p.write_text(json.dumps(d,ensure_ascii=False,indent=2));changed.append(str(p))
inventory=R/'evidence/full-v9-r3c/artifact-inventory.json';d=json.loads(inventory.read_text());d['postPublicationCleanup20261015'].update(state='EXECUTED',result=str(E/'result.json'),deletedCount=len(deleted),availability=availability);inventory.write_text(json.dumps(d,ensure_ascii=False,indent=2));changed.append(str(inventory))
notice='> **当前可用性（2026-10-15）：本内容发布后生成视频已按授权清理，本地最终成片不存在。以下视频路径及“保留”文字为历史记录；当前删除/保留清单和重导出入口见[清理报告](发布后视频清理-20261015报告.md)。**\n\n'
for p in R.glob('*.md'):
 if p.name.startswith('发布后视频清理-'):continue
 s=p.read_text()
 if p.name in ['README.md','完整成片-v9复现.md'] or any(n in s or Path(n).name in s for n in names):
  p.write_text(notice+s);changed.append(str(p))
banner='<aside id="postpublication-cleared" style="padding:18px;background:#fff2c9;color:#261e00;font:16px system-ui">2026-10-15：本内容发布后生成视频已清理，本地最终成片不存在。本页删除的视频播放/下载入口已停用，截图证据仍保留。详情：发布后视频清理-20261015报告.md</aside>'
for p in R.glob('*.html'):
 s=p.read_text();hit=False
 def attr(m):
  global hit
  kind,quote,value=m.group(1),m.group(2),m.group(3)
  match=value in names or value in deleted
  if not match:return m.group(0)
  hit=True
  return f'data-cleaned-{kind}={quote}{value}{quote}' if kind=='src' else f'href="#postpublication-cleared" data-cleaned-href={quote}{value}{quote}'
 out=re.sub(r'\b(src|href)=(\"|\x27)(.*?)(?:\2)',attr,s)
 if hit:
  body=re.search(r'<body[^>]*>',out,re.I)
  if body:out=out[:body.end()]+banner+out[body.end():]
  else:out=banner+out
  p.write_text(out);changed.append(str(p))
p=R/'完整成片-v9复现.md';p.write_text(p.read_text()+'''\n## 发布后重导出说明（2026-10-15）

生成的成片、样片、静音底片与补丁已清理，旧assemble.py依赖的r2成片/补丁不存在，不能直接运行该拼接命令。项目源、人物处理输入、字体、voice.wav和字幕仍在。

如以后确需重导，在新版本路径复制project/render-full-v9-r2.cjs，将入口改为src/v9r3c/Entry.tsx，将e目录改为新的本任务子目录；沿用6122帧、60fps、单并发PNG和本机Chrome设置，运行full，再按上方FFmpeg方法封装voice.wav。不要覆盖现有工程或自动开始渲染。此路径从保留源码重算全部画面，不能保证重新编码MP4与历史SHA逐字节相同；需重新解码和视觉验收。

历史r3c成片SHA256：797426b66fec27431ecf298b9df67f9869b2cddfaa456b1c851009dd6b84ab10。最终发布以06用户确认及原有回执为准。
''')
retained=[x for x in plan['rows'] if x['path'] not in deleted]
unknown=[x for x in retained if 'UNKNOWN' in x['decision']]
report.write_text(f'''# 千问Go发布后生成视频清理结果

{at}。content_id=qianwen-go-case-20261013；Owner04。本次清理已执行，PMO验收待定。

- 已删除66个明确生成的视频：最终母版、旧版、样片、静音底片、试渲和合成补丁；逻辑大小{result['deletedLogicalBytes']:,}字节（{result['deletedLogicalBytes']/1048576:.2f} MiB）。逐路径来源、大小、删除前SHA、引用见[准确清单](evidence/cleanup-20261015/准确路径清单.md)和[计划原件](evidence/cleanup-20261015/plan.json)。没有目录删除、通配删除或跟随软链接。
- 同一文件系统df可用空间增加{result['actualAvailableBytesDelta']:,}字节（{result['actualAvailableBytesDelta']/1048576:.2f} MiB）。这是卷级实测变化，不是把逻辑大小当释放量；并发磁盘活动及APFS分配影响精确归因。
- 删除前df：{result['before']['availableBytes']:,}字节可用；删除后：{result['after']['availableBytes']:,}字节可用。原始df和执行结果见[result.json](evidence/cleanup-20261015/result.json)。66条删除路径均已不存在。
- 删除前对66条准确路径执行lsof，退出1且stdout/stderr均空，无已打开句柄；限定进程检查未发现该内容渲染/合成进程。执行时再次核inode/mtime/size/SHA，未停止任何进程。
- 183项保护性SHA检查全部不变：本内容工程文件/字体/人物与音轨输入、4份指定原片、75个人物输入/工程副本视频、一个跨内容引用旧样片，以及motion-components的v6/v7/v7.1三份成片。其他内容不在删除范围。
- 保留76个视频：75个project/public人物工程素材及其bundle副本用于源码重导出；1个output/sample-motion-v1.mp4仍被其他研究记录引用，下游当前用途未独立关闭，保守保留。引用原件位于动效参考对比-20261012/近期两账号-20261013/读取覆盖.json；未为此唤醒其他Owner。未扫描Downloads/home查重，任务历史未指向其他上传临时副本，未声称清空全盘副本。

发布触发：06原件[用户确认9/9目标平台全部发布](../06/X重试上传-20261014.md)。依据本人确认，公开可见性/作品链接实核仍按06原件保留UNKNOWN，不操作平台作品。具体授权见[任务单](发布后视频清理-20261015任务.md)及项目常设发布后清理规则。

本地最新成片output/qianwen-go-full-v9-r3c.mp4已删除；SHA256 797426b66fec27431ecf298b9df67f9869b2cddfaa456b1c851009dd6b84ab10保留。04当前/历史交付索引已加当前可用性记录，README与涉及删除视频的历史报告加提示；本地HTML删除视频入口停用，截图保留。工程源码、字幕、封面、截图、SHA和发布回执均保留。新导出须按[重导出说明](完整成片-v9复现.md)从源码重算并重新验收；本轮没有启动制作。

规则PERMISSIONS-2026-10-14-v1、ROUTING-2026-10-13-v4及全局§4已读取。目标gpt-6.1-sol/medium；实际model/effort UNKNOWN。共享状态由PMO更新；本Owner完成后主动发送报告并保存回执，不轮询。
''')
(E/'index-updates.json').write_text(json.dumps({'at':at,'changed':changed,'scope':'04 local availability notices only; historical evidence retained','newFiles':[str(Path(__file__)),str(R/'cleanup-20261015.py'),str(report),str(E/'plan.json'),str(E/'result.json'),str(E/'准确路径清单.md'),str(E/'protected-baseline.json'),str(E/'process-check.json'),str(E/'lsof-before.txt'),str(E/'lsof-execute.txt')]},ensure_ascii=False,indent=2))
print({'updatedIndexesReportsPages':len(changed),'report':str(report),'deleted':len(deleted),'retainedVideo':len(retained),'dfDeltaMiB':result['actualAvailableBytesDelta']/1048576})
