# 当前候选 v9-r3b

仅在v9-r2基础上替换三段真人遮罩。v9-r3试导后，在连续帧f1488发现细椅背碎片，进一步对bridge/close做局部灰色清除，并清除眼镜以下独立小碎片。未改变opinion修正版；未改变intro。当前最终引用public/v9r3-final，源码src/v9r3b。

完整影片字节：待实际assemble/verify记录，不手填成功。
复现顺序：full-v9-r3/person-matte-r3e.swift及prepare-final-portraits.py生成bridge/close；opinion复用full-v9-r3的person-matte-r3d结果；project/render-patches-v9-r3b.cjs渲染bridge/close；opinion片段复用full-v9-r3/patch-opinion.mp4；本目录assemble.py从v9-r2按帧拼接并复制原AAC。所有生成器已有输出拒绝覆盖。

早期pilot、public/v9r3、public/v9r3-fixed、output/qianwen-go-full-v9-r3.mp4属于过程记录，不是当前交付。最终交付指向qianwen-go-full-v9-r3b.mp4。
