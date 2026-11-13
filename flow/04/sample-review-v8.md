> **当前可用性（2026-10-15）：本内容发布后生成视频已按授权清理，本地最终成片不存在。以下视频路径及“保留”文字为历史记录；当前删除/保留清单和重导出入口见[清理报告](发布后视频清理-20261015报告.md)。**

# 费用计算→设置提醒：v8 内部交付

2026-10-14，04 Owner `01a11a6f-49ef-7653-934a-4312979fd4e7`。状态：**样片材料已完成，待 PMO 审阅**。本报告的技术/截图检查不代表 PMO 放行、用户风格确认或连续看听验收。完整片及 05 未放行。

## 审阅入口与版本

- [同区间双播放器](sample-review-v8.html)：左侧 v7 的 8.200–21.800 秒，右侧 v8 的 0–13.600 秒；支持同步拖动、逐帧、0.5×，仅右侧出声。
- [最终 MP4](output/sample-motion-v8.mp4)：1080×1920、60fps、816 帧、13.600 秒、1,095,535 字节；SHA256 `2ea32be0211d5cdde889da2942f44d805aead2537820d0046e04e9033a38ec3d`。
- [工程](project/src/v8/CostReminder.tsx)、[入口](project/src/v8/Entry.tsx)、[渲染脚本](project/render-sample-v8.cjs)、[交付索引](sample-delivery-v8.json)。所有旧版和原片保留。
- [当前原件与放行回执](evidence/sample-v8/start-receipt.json)：原片 SHA、03 冻结交接、02 录后定稿、v7 基线及启动 allowed=true。路由目标 gpt-6-astra/high；实际模型/effort/speed 无可核回执，保持 UNKNOWN。

音轨直接取冻结原片 37.2966667–50.8966667 秒，未变速、未合成、未加 BGM。字幕沿 v7 时间减 8.2 秒，保留 6 条中英字幕；只去掉区间开头上一句 id28 残留的 0.0633 秒，未重写其余文案。4500 元是原口播预算条件，图中没有虚构成交价。

## 实际变化与同区间对比

| 阶段 | v8 实现 | 与 v7 的区别及审阅重点 |
|---|---|---|
| 0–5.1s 费用 | 同一冰箱、优惠券扣除、回收/上楼安装服务加入；轨迹汇总 | 费用对象有文字和功能，减少只靠色块理解；服务写明具体收付以询价为准 |
| 5.1–6.5s 计算 | 费用对象向公式位置缩合，然后形成预计总支出 | 保留同一载体；费用文字先退场再显示总价，避免多个层同时压字 |
| 6.5–8.8s 读数 | 商品报价 − 优惠 + 服务费用 | 无金额时直接解释计算关系，不伪造报价 |
| 8.8–9.8s 承接 | 同一冰箱缩为附件，总支出移到提醒条件上方 | v7 对照在这段进入“第1天/每日重新查价”画面；v8 将计算结果连续带入设置面 |
| 10.1–13.6s 设置 | 每天查价、条件开关、设置反馈 | 日历对应频次，光标启用开关；标明案例流程示意，非真实通知 |

主体白色载体约占 85% 画宽，主要内容与底部中英字幕分区。比较页的 9.35 秒实际截图见 [comparison-player.png](evidence/sample-v8/comparison-player.png)。上述是构图与信息组织观察，不是观众理解度测试或优于 v7 的用户结论。

## Skills 研究与采用

主流程使用 `fred-remotion-output`，辅以 `frame-smith` 和 `remotion-best-practices`，本任务竖屏/60fps/冻结原声优先。

| 已读材料 | 学到与实际采用 |
|---|---|
| 主 SKILL 与 CODEX-ELI-ADAPTER | 候选→真实预览→源码→改写→实际调用→导出证据；未带入 Fred 品牌、私人声音、机器或授权 |
| DESIGN.md | 圆润形体、软阴影、留白和稳定可读；应用于冰箱、优惠券、服务面、统一字重 |
| content-to-component.md | 按语义先找动作；分别检索费用与提醒 Top3，不按相似颜色选组件 |
| library-delivery-gate.md | 绑定预览 SHA、源码 SHA、改写函数及 JSX 调用；实际运行 suggestion/keyframes 门禁 |
| object-transitions.md | 对象身份与空间承接优先；冰箱及同一白色载体跨段持续存在 |
| production-defaults.md | 有目的的动作与读数停顿；本任务不套 30fps、Logo、大片片头或 BGM |
| episode-assembly.md | 使用一个全局帧时钟，字幕和动效同一时间基准；本次仅短样片，未组装整片 |
| components-and-dependencies.md | 核真实本地源码/素材依赖，needs-auth 不当可用；复用既有本地字体/runtime |
| implementation.md | 先关键帧和短段，再完整样片；保留失败/修正中间证据，不伪造一次通过 |
| production-gates.md | 文件、动态、原声与人工检查分层；机器 PASS 不代替审美或看听 |
| 实际 kit/theme.ts 与 ui | 读了实现；复制 theme.ts 的 p/q/mix/springAt，采用缓动与有限反馈弹性。SVG/场景布局为本片重写，没有声称完整移植 UI 库 |
| frame-smith：environment、motion-floor、beat-structure、reveals、anti-cheap-motion、preflight | 现有环境；费用收束作为主要动作，预算/开关为辅助揭示；依口播安排停顿，避免无意义漂移/粒子 |
| remotion-best-practices：animations、timing、fonts | 帧驱动、固定 fps、静态字体加载；先确认 MiSans 500/600/900 可渲染 |

补读 01 的 [实读分析](../../../动效参考对比-20261012/FredTalk自动剪辑-20261014/实读分析.md)与 PMO 验收原件；实际看过 90/120/150 秒参考图及 relayout/category/zoom 六页密集帧。采用“保留承载对象、改变焦点和层级”；没有把其技术自述、静帧或节选当作完整实时看听。

## 候选取舍与调用证据

实际看过 **7 个不同组件的 21 张核心帧**，下载回执逐项核 catalog media-manifest SHA。未安装付费组件。`top3-coreframes.jpg` 是初次本地素材缺失时的空白诊断图，不能计入实读；有效汇总为 references 下 verified/gather/t19c 图与 fetch 回执。

| 检索 | 实际候选与决定 |
|---|---|
| 费用：商品 优惠 费用 多项汇合 总价 计算 | T15d 费用账单语义最近，但 needs-auth 源码不可用；N008 是提问/角色不对应扣除；N044 是商品进入输入面，移到提醒段采用 |
| 提醒：界面 点击 开关 反馈，custom/object-transition | 实际 scene.py Top3 为 T19c/N026/T09a。T19c 人物惊叹不解释设置；N026 上传会增加本段没有发生的步骤；T09a 源码 needs-auth。无 sceneGuide 的早期检索返回 N026/T09a/N044，保留两次真实结果，不冒称它们相同 |
| 费用补充：多物体 汇聚 | 选可读取源码的 new30-op09；保留辅助对象收束、主载体持续，改为本片费用图解 |
| 提醒补充 | 选可读取源码的 library-new10-n044；保留商品缩成附件与设置面前景化 |

| 动作来源 | 本片函数与真实调用 | 导出帧 |
|---|---|---|
| new30-op09 的 OP09；source-view 文件 SHA `7ffd8e123f571e373a7012bed97ca238ce3ecc22631da6637ed284e3ec4451fe` | `CostGather`，`CostReminder` 中 `<CostGather t={t}/>` | 5.7–6.5s 密集帧；native-f390.png |
| N044 的 BatchB.tsx / MediaScenesB 分支；SHA `159a69df982c5184c08ef7d8a152ee80bf7e7a3d3128ef67fab3d51060dd8c03` | `ProductToReminder`，`CostReminder` 中 `<ProductToReminder t={t}/>` | 8.8–9.9s 密集帧；native-f546/f561/f759.png |

完整绝对路径、SHA、预览观察、函数、调用及输出绑定见 [manifest.json](evidence/sample-v8/manifest.json)。这属于场景级改写，不是声称原组件原封不动运行。原光标/日历、冰箱和文案均为本片语义图解。

## 最终检查与边界

- **解码/时间**：FFmpeg 全文件 video decode exit0，816 帧；PTS 0–13.5833 秒，帧间时间符合 60fps（日志小数精度误差最大 0.0000334 秒）。AVFoundation 元数据核实 1080×1920/H.264/AAC/13.6 秒。
- **音轨信号**：冻结 WAV 652800 samples；最终 AAC 解码 653312 samples（尾部编码填充 512 samples），共同 13.6 秒相关系数 0.999970，±1ms 搜索峰值在 0 sample。v7 8.2–21.8 秒与冻结 WAV 相关系数 0.999822。容器和浏览器时长均13.6秒；这些不证明直接听音、语气或逐字转录正确。
- **实际图像**：查看最终 MP4 的287个采样帧，另5张原尺寸关键帧中有1个新增帧，累计288/816个不同帧，未逐帧查看528帧。全段每6帧一张（0–13.5s）加最后帧；5.7–6.5、8.8–9.9、11.6–12.7 秒逐帧密集检查。15张汇总页全部查看，另查看1.85/6.5/9.1/9.35/12.65秒5张原尺寸关键帧。可见长字幕、公式、条件、反馈无裁切或相互压字；进场对象在画边的短暂裁切属于滑入过程。未检查到黑帧或突然换载体。
- **修正**：短段首轮发现费用缩合路径不合适、总价与费用交叠、旧“商品报价”与移动总价交叠。已改收束位置及显示时序；trial2 和最终密集帧未再出现。旧测试产物保留，不作为最终证据。
- **动效检测**：原始 motion_audit exit0，0 blocking、3 hold-warn，不设置豁免。2.1–5.0s 为费用阅读+汇总轨迹；6.3–8.7s 为公式阅读；9.6–12.0s 为条件阅读、日历及开关动作。默认192×108取样会弱化竖屏局部动作；提醒仍保留，节奏是否合适交 PMO 连续观看判断。
- **门禁**：suggestion、keyframes、clock-lint、workflow planning/representative 均有真实 PASS 回执。keyframes AST 使用本机既有 TypeScript 的进程级精确路径适配，不修改上游校验逻辑/全局配置，不安装。workflow bounded-revision 只越过用户逐步等待，不代表用户已确认方向/关键帧；真实视觉检查独立记录。
- **播放器**：本地 Chrome 实载两个MP4、0/5.5/9.1/末帧定位、前后1帧、0.5×播放暂停通过；静态定位误差≤1µs，实际半速播放测得两播放器约42ms偏差。对照页允许80ms内播放偏差；精确比帧请暂停/拖动。无直接听音或实时完整看听结论。
- **首尾**：首帧为承接费用段，前0.0633s不闪上一句字幕；末帧保留已设置图解，字幕按既定时间结束。不是循环素材，也未验完整片上下游接缝。

待验：PMO 连续观看/听音、节奏与风格判断、是否提交用户；用户风格确认；完整片整合及05。没有真实监控、真实通知、下单或商业成果验收。

## 复现与文件保护

使用既有 Node 22.16.0、Remotion4.0.535、Chrome、FFmpeg；无安装、付费、外传、旧版删除。先在新的本地副本中运行，脚本拒绝覆盖已存在的 full-muted.mp4。

```sh
cd '/Volumes/EXTERNAL/自媒体/qianwen-go-case-20261013/flow/04/project'
/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin/node render-sample-v8.cjs full
```

在04目录，用 `ffmpeg -n -i evidence/sample-v8/full-muted.mp4 -i evidence/sample-v8/source-voice.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -t 13.6 -movflags +faststart output/sample-motion-v8.mp4` 合入原声。具体 QA 命令见 `evidence/sample-v8/final-qa.py`、`keyframe-gates.py`、`player-check.cjs`；抽帧脚本也拒绝覆盖，不应直接在已交付证据目录重复运行。

现有 ffprobe 报 `bad CPU type in executable`，已查 LOCAL_BLOCKERS 对应已知架构问题；不安装 Rosetta、不替换全局工具，改用现有 AVFoundation 适配器及 FFmpeg 解码。TypeScript 适配记录见 parser-runtime.json。工作尾声 df 剩余外盘约1.48TiB、内部约12.5GiB；未清理文件，不声称释放空间。精确本轮文件清单及字节数见 new-files-inventory.json。

主动回报与验收分开：工具发送回执写入 `evidence/sample-v8/pmo-report-receipt.json`；发送成功不等于 PMO 已阅读/验收。遵守禁止轮询，发送后不自行查进度。
