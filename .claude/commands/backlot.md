---
description: 打开 Backlot 动态故事板，在浏览器中实时查看制作中的 pipeline 阶段、脚本、场景计划和生成素材。
argument-hint: "[project-id（可选，默认当前或最近项目）]"
---

打开指定项目的 Backlot 看板：

```bash
python -m backlot open $ARGUMENTS
```

- 不传参数：使用 `python -m backlot open` 打开包含全部项目的资料库视图。
- 命令可重复执行：若 Backlot 服务尚未运行则先启动，再在浏览器中打开项目看板。
- 命令失败时应报告错误并继续用户原本的任务；看板只负责观察，不能阻塞制作。
- 看板从磁盘读取 `projects/<id>/` 下的 checkpoint、artifact、asset 和 event。不要手动更新 UI；按照 `skills/meta/checkpoint-protocol.md` 如实写入检查点和产物即可。
