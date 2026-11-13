from pathlib import Path
import json,hashlib,datetime,os,subprocess
R=Path(__file__).resolve().parent;E=R/'evidence/sample-v2';now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
qa=json.loads((E/'qa.json').read_text());scope=json.loads((E/'read-scope.json').read_text());player=json.loads((E/'comparison-player-check.json').read_text());assert scope['assistant_viewed'] and qa['audio_decoded_pcm_identical_to_v1'] and not player['mediaErrors'] and all(x['loaded'] for x in player['images'])
exp=json.loads((R/'evidence/sample-export.json').read_text())
d={'content_id':'qianwen-go-case-20261013','version':'sample-motion-v2','owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','pmo_thread_id':'01a11194-c40d-7bf0-8396-5bb5d6449444','updated_at':now,'status':'READY_FOR_PMO_REVIEW','sample':str(R/'output/sample-motion-v2.mp4'),'comparison':str(R/'comparison-v1-v2.html'),'sha256':qa['sha256'],'bytes':qa['bytes'],'duration_seconds':21.8,'width':1080,'height':1920,'fps':60,'source_video':exp['raw_source'],'raw_video_seconds':exp['raw_video_seconds'],'same_audio_as_v1':True,'captions':str(R/'output/sample-captions-v2.srt'),'project_entry':str(R/'project/src/SampleV2.tsx'),'routing':json.loads((E/'start-receipt.json').read_text()),'qa':qa,'actual_visual_scope':scope,'player_evidence':str(E/'comparison-player-check.json'),'full_film':'PAUSED_PENDING_USER_SAMPLE_APPROVAL','stage05_release':'NOT_RELEASED','user_style_approval':'PENDING','report':{'tool_sent':'PENDING','pmo_received':'UNKNOWN','pmo_acceptance':'PENDING'}}
(R/'sample-delivery-v2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
md=f'''# 千问Go 动效样片v2交付与自查

2026-10-13；04唯一Owner。本版交PMO审原件及用户看风格，不自评PASS，整片仍暂停，05未释放。

[同步对照v1/v2](comparison-v1-v2.html) · [直接播放v2](output/sample-motion-v2.mp4) · [v1保留](output/sample-motion-v1.mp4) · [工程入口](project/src/SampleV2.tsx) · [字幕](output/sample-captions-v2.srt) · [机器索引](sample-delivery-v2.json)。

21.8秒 / 1080×1920 / 60fps / H264与AAC / 1308帧，{qa['bytes']:,}字节。SHA256：`{qa['sha256']}`。

## 范围与实际变化

沿原片③`{exp['raw_source']}`的29.0966667—50.8966667秒；原声区间、字幕文字和时点与v1一致。音频直接复制v1 AAC，无重编码；导出后解码PCM逐字节相同。没有新增BGM、音效、合成或加速。

旧大标题、背景斜块与小冰箱侧栏布局全部放弃，另写独立SampleV2工程入口：大幅冰箱特写推进→提取型号标签→同款报价单展开/靠近核对项→费用纸条拆分和收束→同一个结果纸面扩展成估算→纸面接续日历。使用二维矢量与CSS透视，不声称真实3D物理相机。制作思路和参考阅读范围见[sample-v2-design.md](sample-v2-design.md)。

## 三组同时间对比

| 时间 | v1观察 | v2改变及理解作用 | 限制 |
|---|---|---|---|
| 2.30秒 | 冰箱约为小插画，旁边文字卡解释型号 | 冰箱推进占主要画幅，型号区域被框住，之后提取同一身份标签；焦点直接落在识别对象上 | 自绘型号铭牌示意，非真实产品识别截图 |
| 11.50秒 | 固定分支/费用文字列表 | 三份费用字段从纸面分离，随后转正、收束为同一估算纸面；动作表达拆解与汇合 | 没有真实价格；可判断结构，不能证明报价计算实测 |
| 20.50秒 | 小冰箱旁设置卡，主要靠文字讲 | 估算纸面接续大幅日历，时针落位，条件和预算进入主要阅读区 | 日历与时针是设置示意，不证明提醒已送达 |

三张原件为`evidence/sample-v2/pair-2.3.jpg`、`pair-11.5.jpg`、`pair-20.5.jpg`，左v1右v2。上述是可观察的变化，不把创作意图写成用户审美认可，也不宣称达到参考片全部效果。

## 已完成检查

- 全解码exit=0；1308帧时间戳严格递增，最大间隔{qa['max_frame_gap']:.4f}秒；首尾规格匹配。
- 原生立体声{qa['native_loudness_lufs']} LUFS、{qa['native_true_peak_dbtp']} dBTP；解码PCM与v1逐字节一致。只证明声音未变，不证明主观听感或字幕逐字准确。
- 修正前完整导出全段每秒采样22张实际查看；原尺寸11个时点实际查看：0、2.3、4.8、6.9、9.8、11.5、13.9、15.8、17.9、20.5、21.75秒。
- 修正前完整导出六个原帧率连续窗口共294帧实际查看：2.4—2.8833、6.4—7.0833、7.9—8.5833、13.2—14.0833、14.4—15.5833、17.1—17.9833秒。取样不是整1308帧全看；窗口/采样可有重叠，不累加冒充覆盖率。
- 在2.617秒发现旧型号铭牌与新标签透明交叉，改为旧铭牌先退场、新标签再显现。仅重渲染帧132—179，以FFmpeg按帧拼接并重编码画面，AAC直接复制；修正前导出、源码及QA保存在pre-label-fix。修正版2.10—3.0833秒60帧（包含两侧接缝）已实际查看，未再见交叉文字。未变区域复用上述读图证据；不声称修正版全1308帧重新读过。
- 内部先导出3—7秒240帧并完整读图，发现并修字幕侵入与透明文字混叠；另导出12.8—16.8秒检查费用接续，实际查看5设计时点，发现估算换行路径碰撞，改先下移再左对齐并查看3个修正时点。该换行在完整导出的14.4—15.5833秒72帧重新逐帧核查。
- 本地Chrome实际验证两视频加载、同步播放/暂停、拖动4.8秒、续播、声音开关及三张对照图加载；桌面与手机截图已读。默认静音，v1始终静音；对照误差以回执实际值为准。无网络服务器或上传。

**未完成**：直接听音、全段实时连续看听、主观动态审美和用户认可。字幕仍沿句级ASR映射与手工分句，部分时点近似。画面比v1显著放大主体，但纸面比喻是否足够符合用户“不要视频PPT”的偏好，必须由用户看本版确认；不能仅凭技术检查宣布满足审美。

## 事实、保留与停点

型号不写真实型号；A/B/C是示意，B标“当前核对项”，不暗示胜出；费用只示意字段，优惠仍须核条件；¥4,500仅预算阈值；“估算≠成交”“未展示送达”在画面。无源人像/屏幕/相框，无虚构后台成功。

v1、旧整片、全部源文件与工程保留。只写本条flow04，本轮无新依赖安装、外部AI调用、付费、上传、发布、删除或下游释放。文件清单与df见`evidence/sample-v2/delivery-inventory.json`及`storage-delivery.txt`，不将目录大小当释放空间。

路由规则ROUTING-2026-10-13-v4；目标gpt-6-astra/high，实际model/effort/speed UNKNOWN，依据本次无平台运行字段回执，未擅改设置。

完成后主动报告PMO并保存`sample-report-send-receipt-v2.json`；工具发送、PMO收到、PMO验收分别记录。发送后停止，不轮询，用户认可样片前整片继续暂停。

## 复现

在`project/`执行既有Node的`render-sample-v2.cjs full`得到仅视频中间件，再用既有FFmpeg映射该视频与v1音频、`-c copy`输出新的明确文件名。初次封装命令存`evidence/sample-v2/mux-command.json`；本次局部补片拼接脚本为`patch-final-sample-v2.py`，实际命令在`evidence/sample-v2/patch-command.json`。复现前指定新输出路径，保留现有交付。此为样片复现入口，原`render.sh`仍是暂停的整片入口，不误运行。依赖只读复用Remotion4.0.535/React19.3.0，无新安装；字体为工程实体文件，有提取脚本及来源SHA。
'''
(R/'sample-review-v2.md').write_text(md)
p=R/'README.md';s=p.read_text();start=s.index('当前交付：');end=s.index('\n## 复现');s=s[:start]+'''当前交付：**21.8秒动效样片v2重做，待PMO及用户确认风格；整片暂停。**

[同步播放v1/v2对照](comparison-v1-v2.html) · [直接播放v2](output/sample-motion-v2.mp4) · [v2自查与限制](sample-review-v2.md) · [v2交付索引](sample-delivery-v2.json) · [v2叙事设计](sample-v2-design.md)。默认静音，未自动播放。

v1被用户否定风格，文件保留供对照。旧`preview.html`为v1页面，当前请使用v2对照页。既有`output/candidate-v1.mp4`仍是未完成最终验收的整片中间版，不作本次整片交付。

v2独立入口：`project/src/SampleV2.tsx`及`project/render-sample-v2.cjs`；仅渲染样片。以下旧整片复现入口保留供以后明确授权，不在当前停点执行。
''' +s[end:];p.write_text(s)
files=[]
for base,dirs,names in os.walk(R,followlinks=False):
 dirs[:]=[x for x in dirs if not (Path(base)/x).is_symlink()]
 for n in names:
  p=Path(base)/n
  if not p.is_symlink(): files.append({'path':str(p),'bytes':p.stat().st_size})
(E/'delivery-inventory.json').write_text(json.dumps({'at':now,'scope':str(R),'follows_symlinks':False,'files':files,'cleanup':'none this revision'},ensure_ascii=False,indent=2))
(E/'storage-delivery.txt').write_text(subprocess.check_output(['df','-k',str(R)],text=True))
print(json.dumps({'status':d['status'],'sha256':qa['sha256'],'bytes':qa['bytes']},ensure_ascii=False))
