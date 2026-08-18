# Ink Theater 第三方资源说明（中文伴随说明）

> 本文仅帮助中文用户理解资源来源，不替代具有约束力的英文 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) 及完整许可证文本。

Ink Theater 随附两类第三方资源。两者均可免费用于包括商业用途在内的各种场景，但必须保留署名和相应许可说明。

## Patrick Hand 手写字体：SIL Open Font License 1.1

文件：`assets/patrickhand.ttf`

版权所有 © 2010–2012 Patrick Wagesreiter（mail@patrickwagesreiter.at）。该字体使用 SIL Open Font License 1.1。OFL 允许随项目分发、嵌入和再发布，也允许商业使用；但不允许单独销售字体，并要求发布时同时携带版权说明和许可证文本。完整许可证见 `assets/OFL.txt`。

## 动作捕捉片段：CMU Graphics Lab Motion Capture Database

文件：`mocap/clips/*.json`，并打包到 `mocap/clips.js`

这些 2D 动作片段由 `mocap/bvh2clip.mjs` 从 **CMU Graphics Lab Motion Capture Database**（http://mocap.cs.cmu.edu）的 BVH 文件派生，源文件经 `una-dinosauria/cmu-mocap` 镜像取得。CMU 数据库允许全球范围内免费用于研究和商业项目。每个片段的源 trial ID 记录在 `mocap/catalog.json` 中，例如 `walk` 对应 CMU 02_01，`wave` 对应 CMU 141_16。

项目没有打包 Meta / FAIR AnimatedDrawings 的动作捕捉数据。独立的 `/animated-drawing` 能力会说明 Meta AnimatedDrawings 工具，但 Ink Theater 自带的动作片段库全部来自 CMU。
