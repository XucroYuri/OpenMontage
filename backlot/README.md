<!-- generated-by: gsd-doc-writer -->
> 简体中文（主文档） | [English copy](README.en.md)

# Backlot — 实时制作看板

Backlot 是一个只读的本地看板，用于实时查看 OpenMontage 制作过程：流水线阶段依次点亮，脚本以剧本页呈现，场景胶片会随素材生成逐步填充，同时展示制作决策、费用、活动记录和成片。所有状态都来自流水线已经写入 `projects/<id>/` 的文件。

## 打开看板

```bash
python -m backlot open <project-id>   # 按需启动服务并打开指定项目
python -m backlot open                # 打开全部项目的项目库
python -m backlot serve --port 4750   # 在前台运行服务
```

`open` 是幂等且非阻塞制作流程的入口：服务已运行时会直接复用；看板启动失败时，制作仍应继续。

## 实时更新原理

Backlot 不写入项目目录，也不要求 Agent 手动同步界面。`watchfiles` 监听 `projects/`，文件变化后通过 SSE 通知浏览器重新获取看板状态。

| 看板内容 | 磁盘数据来源 |
|---|---|
| 项目标识与阶段顺序 | `project.json` + `pipeline_defs/<type>.yaml` |
| 阶段状态、审批节点与版本 | `checkpoint_<stage>.json` + `history/` |
| 脚本卡片与完整预览 | `artifacts/script.json` |
| 场景胶片卡片 | `scene_plan × script × asset_manifest` 关联结果 |
| 生成动画与活动记录 | `events.jsonl`（由 `BaseTool` 插桩写入） |
| 费用进度 | 检查点中的 `cost_snapshot` |
| 成片 | `renders/*.mp4`，并兼容项目根目录中的 `.mp4` |

没有检查点的项目会降级为“磁盘发现”视图，仍可展示媒体、快照和成片。已完成的制作任务可以通过“回放制作过程”按检查点历史与事件时间戳回看完整过程。

界面默认使用简体中文；右上角可切换 English，选择保存在浏览器本地存储中。

## 运行演示

无需真实制作任务即可观察看板实时更新：

```bash
python scripts/backlot_simulate_run.py          # 模拟一次约 1 分钟的制作
python -m backlot open backlot-demo-run
```

需要快速自动验证时，可给模拟器添加 `--fast`；需要在结束后删除演示项目时，可添加 `--cleanup`。
