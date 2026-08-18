# /ink-art：手绘墨线涂鸦动画

角色先自我绘制，再行走、跳舞或挥手；也可制作冷面机械装置讲解。使用矢量和确定性输出，通过 HyperFrames 渲染为 MP4。

读取 `skills/creative/ink-theater.md` 和 `ink-theater/README.md`，再制作用户要求的作品：

- **Ink Theater** 引擎（`ink-theater/ink-theater.js`）提供可变宽墨线、可安全 seek 的抖线、闭式弹簧缓动、FABRIK IK 和机械装置语法。
- 角色需要**行走 / 跳舞 / 挥手 / 跳跃**时，使用 **Ink Puppet** 动捕系统：`InkPuppet.create` → `p.drawIn`（自绘显现）→ `InkPuppet.choreograph([{clip:'wave'},{clip:'twist'},…])`。名称来自 `ink-theater/mocap/catalog.json` 中的 12 个 CMU 动作。**不得手调动作**；通过 `node ink-theater/mocap/add-motion.mjs` 添加动作。
- 字幕使用 **HTML overlay `<div>`**，因为 HyperFrames 不会把 Web 字体应用到 SVG `<text>`。
- 渲染前运行 `npx hyperframes lint` 和 `snapshot`。
