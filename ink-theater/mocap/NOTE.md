<!-- generated-by: gsd-doc-writer -->
# 动捕来源与许可

**简体中文（主文档）** · [英文副本](NOTE.en.md)

所有随附片段均源自 **CMU Graphics Lab Motion Capture Database**（http://mocap.cs.cmu.edu），该数据库**允许免费用于包括研究和商业用途在内的所有用途**。BVH 文件获取自 `una-dinosauria/cmu-mocap` 镜像；`clips.js` / `clips/*.json` 是由 `bvh2clip.mjs` 生成的 2D 衍生数据。每个片段的来源 trial ID 记录在 `catalog.json` 中（例如 `wave` = CMU 141_16，`shuffle` = CMU 77_29）。完整署名参见 [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md)。

## 添加动作（自扩展，无需修改代码）

```
node add-motion.mjs <name> <cmu-id|url|path> [category] "[description]"
# e.g.  node add-motion.mjs backflip 90_01 dance "a backflip"
```

该命令会获取 BVH 并转换它（自动映射 fair1 / CMU / Mixamo 骨架）、重新打包 `clips.js`，再更新 `catalog.json`。CMU 提供数千个片段（walk、run、dance、wave、jump……）。对于任何需要随项目分发的内容，都应优先使用 CMU，以保持动作库的许可清晰。不同骨架可能需要在 `bvh2clip.mjs` 的 `ALIAS` 表中添加别名，并通过 `--axis xy|zy` 选择投影平面。
