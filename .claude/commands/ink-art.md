---
description: 手绘白底墨线涂鸦动画：角色先自我绘制，再行走、跳舞或挥手；也可制作冷面机械装置讲解。矢量、确定性输出，通过 HyperFrames 渲染为 MP4。
argument-hint: "[要制作的动画]"
---

读取 `skills/creative/ink-theater.md`（隐喻方法、色彩语法、原型）和 `ink-theater/README.md`（引擎 API、确定性与 SVG 文本字体注意事项），再制作下述作品。

- 使用 **Ink Theater** 引擎（`ink-theater/ink-theater.js`）：可变宽墨线、可安全 seek 的抖线、闭式弹簧缓动、FABRIK IK 和机械装置语法。
- 角色需要**行走 / 跳舞 / 挥手 / 跳跃**时，使用 **Ink Puppet** 动捕系统：`InkPuppet.create(...)` → `p.drawIn(tl, ...)` 自绘显现 → `InkPuppet.choreograph(tl, p, [{clip:'wave'},{clip:'twist'},{clip:'walk'},...])`。clip 名来自 `ink-theater/mocap/catalog.json`（12 个 CMU 动作）。**不得手调动作**；用 `node ink-theater/mocap/add-motion.mjs <name> <cmu-id> …` 添加动作。
- 字幕使用 **HTML overlay `<div>`**，因为 HyperFrames 不会把 Web 字体应用到 SVG `<text>`。
- 渲染前运行 `npx hyperframes lint` 和 `snapshot`，人工检查候选缩略图总览。

在 OpenMontage 中，插画使用 `animation` pipeline，动捕木偶使用 `character-animation` pipeline；这是风格与引擎，不是独立 pipeline。

请求：$ARGUMENTS
