# /backlot：打开动态故事板

打开指定项目的 Backlot 看板；浏览器界面会实时显示 pipeline 阶段、脚本、场景计划和生成素材：

```bash
python -m backlot open <project-id>
```

- 不传 project id：使用 `python -m backlot open` 打开资料库视图。
- 命令可重复执行：需要时自动启动 Backlot 服务，再打开项目看板。
- 失败时报告错误并继续用户原本的任务；看板只负责观察，不能阻塞制作。
- 看板从磁盘上的 `projects/<id>/` 派生全部状态；不要手动更新 UI。按照 `skills/meta/checkpoint-protocol.md` 如实维护 checkpoint 和 artifact。
