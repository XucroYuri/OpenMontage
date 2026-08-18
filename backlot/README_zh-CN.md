# 制作看板

[English](README.md) · 简体中文

制作看板是一个只读的本地界面，用于实时查看视频制作过程：流水线阶段会依次点亮，脚本以预览卡片展示，故事板会随着素材生成逐步填充，同时显示制作决策、费用和活动记录。所有信息都来自流水线已经写入 `projects/<id>/` 的文件。

```bash
python -m backlot open <project-id>   # 启动服务并打开指定项目
python -m backlot open                # 打开全部项目的项目库
python -m backlot serve --port 4750   # 在前台运行服务
```

## 实时更新原理

智能体无需额外操作。文件监视器会监听 `projects/` 的变化，通过 SSE 通知浏览器重新获取看板状态。

| 看板内容 | 磁盘数据来源 |
|---|---|
| 项目标识与阶段顺序 | `project.json` + `pipeline_defs/<type>.yaml` |
| 阶段状态、审批节点与版本 | `checkpoint_<stage>.json` + `history/` |
| 脚本卡片与完整预览 | `artifacts/script.json` |
| 故事板场景卡片 | `scene_plan × script × asset_manifest` 关联结果 |
| 生成动画与活动记录 | `events.jsonl` |
| 费用进度 | 检查点中的 `cost_snapshot` |
| 成片 | `renders/*.mp4` |

没有检查点的旧项目仍可降级显示磁盘上发现的媒体、快照和成片。完整制作任务还可以通过“回放制作过程”按时间顺序重现阶段和素材的出现。

不需要真实制作任务也能体验：

```bash
python scripts/backlot_simulate_run.py
python -m backlot open backlot-demo-run
```

界面默认使用简体中文，右上角可切换 English；选择会保存在浏览器中。
