> **当前可用性（2026-10-15）：本内容发布后生成视频已按授权清理，本地最终成片不存在。以下视频路径及“保留”文字为历史记录；当前删除/保留清单和重导出入口见[清理报告](发布后视频清理-20261015报告.md)。**

# 千问Go v9-r3c｜局部收尾交付

2026-10-14。04修订制作与本轮有限自查完成，交PMO待验；05未释放。

[完整成片](output/qianwen-go-full-v9-r3c.mp4) · [审片页](full-review-v9-r3c.html) · [检查记录](evidence/full-v9-r3c/visual-review.json) · [技术检查](evidence/full-v9-r3c/technical-qa.json)

修订：补回衔接/观点段眼镜外沿与手部原像素，去掉衔接处椅背碎片；结尾原遮罩仍在98.27秒附近残留，按PMO已允许的现有内容覆盖方案，保留96.27–97.3秒真人，随后由原有AI节点接管至结束。原声、全部43条双语字幕、开场真人与其余内容动画保持。没有用生成图补画脸或手，没有增加免责声明/角标。

最终文件：1080×1920，60fps，6122帧，102.033333秒视频时长（容器102.034秒），H.264/AAC，9,693,641字节。

SHA256：`797426b66fec27431ecf298b9df67f9869b2cddfaa456b1c851009dd6b84ab10`。

最终视频和音频完整解码通过；PTS逐帧间隔恒定256 ticks。AAC payload与v9-r2逐字节相同，SHA为`3a6508908ff69a78ade981ba84bc7a6693d0aacc510a4009005eb2f40516ac54`。未重新录音、变速、增删口播或重混。局部片段拼接后视频整体重编码，不称画面压缩流无损复制。播放器加载、11处seek、逐帧按钮和短播放检查通过。

本轮实际核了196个不同帧：106帧完整画面、90帧仅人像裁条；22张图板和1张原尺寸全帧。其余5926帧未做视觉阅读。连续逐帧证据包括24.7833–25.1833秒（25帧）、97.5–98.2秒（43帧，已换现有AI画面）、100.05–100.65秒（37帧，已换现有AI画面）。详见frame-index.json和visual-review.json。关键词源码检查及抽样未见被拒角标；不是逐帧读完全部文本。

关键帧组件门禁已对当前源码/当前截图重新通过，见gate-keyframes.json；不是PMO、05或用户通过。完整连续视听、直接听音与最终观感仍待验。保留镜框/发丝的细小分割痕迹说明，不宣称全片无损抠像。原片④本身部分头发出画，未合成补齐。

复现：当前源码project/src/v9r3c；人物资产project/public/v9r3-final；bridge补丁来自evidence/full-v9-r3b/patch-bridge.mp4，opinion补丁来自evidence/full-v9-r3/patch-opinion.mp4，close补丁由project/render-patches-v9-r3c.cjs产生。本目录evidence/full-v9-r3c/assemble.py按准确帧区间合并v9-r2及三个补丁，复制整条原AAC；verify-final.py生成技术与截图证据。现有输出拒绝覆盖，复现先使用新版本路径。

原片、v8.1、v9、v9-r2及本次r3/r3b试导均保留。本次只维护04材料，未改PMO唯一状态、未派05、未上传/发布/付费/安装/删除。主动回报与真实回执单列，不把工具成功写成PMO已读或已验。

主动回报：send_message_to_thread已成功发送至PMO 01a11194-c40d-7bf0-8396-5bb5d6449444，原始回执为evidence/full-v9-r3c/pmo-report-receipt.json。PMO实际已读/验收仍UNKNOWN/PENDING；未轮询。
