# OpenMontage 共享项目上下文（中文伴随说明）

> **人类可读的简体中文说明** | [英文规范上下文](PROJECT_CONTEXT.md)

本文面向中文开发者解释项目架构和约定。`CLAUDE.md`、`CODEX.md`、`CURSOR.md`、`COPILOT.md` 等平台入口仍应指向 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)，避免 Agent 从多份翻译中读取分叉规则。若本文与实时代码、Schema、registry、pipeline manifest 或英文规范文件冲突，以这些规范来源为准。

## 项目定位

OpenMontage 是一个开源、由 AI Agent 编排的视频制作平台。

## Agent 优先的指令驱动架构

AI Agent 本身就是智能与控制平面。Python 只负责工具能力和状态持久化；编排、创意决策、审查与阶段转换由 Agent 按照 YAML manifest 和 Markdown Skill 完成。

```text
Agent 读取 pipeline manifest (YAML)
  -> 读取 stage director skill (MD)
  -> 使用 Python BaseTool
  -> 通过 meta skill 自审
  -> 使用 Python utility 写 checkpoint
  -> 在规定的 gate 请求人工批准
```

项目没有 Python orchestrator、Python reviewer 或 Python handler。新增功能时也不能把这些 Agent 决策迁回 Python。

## 规范来源

| 内容 | 规范位置 |
|---|---|
| Agent 指南与运行契约 | `AGENT_GUIDE.md` |
| Skill 索引 | `skills/INDEX.md` |
| 工具注册表 | `tools/tool_registry.py` |
| 流水线清单 | `pipeline_defs/` |
| artifact Schema | `schemas/artifacts/` |
| 风格 playbook | `styles/*.yaml` |
| stage director Skill | `skills/pipelines/<pipeline>/<stage>-director.md` |
| meta Skill | `skills/meta/*.md` |
| 架构深度说明 | `docs/ARCHITECTURE.md` |

## 三层知识架构

```text
Layer 1: tools/tool_registry.py  -> 有哪些工具、实时能力、状态与成本
Layer 2: skills/                 -> OpenMontage 如何在项目中使用这些能力
Layer 3: .agents/skills/         -> 通用技术或 provider API 的最佳实践
```

每个工具的 `agent_skills[]` 字段把 Layer 1 连接到 Layer 3。完整映射见 `skills/INDEX.md`。

## 核心模式

- 典型状态机：`idea -> script -> scene_plan -> assets -> edit -> compose -> publish`。
- 每个 stage 都有 Markdown director Skill，负责说明 Agent 应如何执行。
- pipeline manifest 是声明式 YAML，定义阶段、Skill、工具、审查重点和人工审批门。
- 主要能力族采用 selector + provider tool：例如 `tts_selector` 路由到各 TTS provider，`video_selector` 路由到各视频 provider。
- 风格 playbook 使用 YAML 描述视觉语言、排版、运动、音频和资产约束。
- `brief`、`script`、`scene_plan`、`asset_manifest`、`edit_decisions`、`render_report`、`publish_log` 是 canonical artifact。
- 每个工具都继承 `tools/base_tool.py` 中的 `BaseTool`。
- checkpoint policy 来自 manifest 的 `human_approval_default` 与 `skills/meta/checkpoint-protocol.md`。
- reviewer 是 `skills/meta/reviewer.md`，提供建议，最多两轮。
- `tools/cost_tracker.py` 按 estimate → reserve → reconcile 管理预算。
- canonical artifact 必须通过 `schemas/artifacts/` 的 JSON Schema。

## 关键文件

| 文件 | 用途 |
|---|---|
| `config.yaml` | 全局配置 |
| `lib/config_model.py` | Pydantic 运行时配置加载器 |
| `lib/checkpoint.py` | checkpoint 读写 |
| `lib/pipeline_loader.py` | manifest 加载与辅助函数 |
| `lib/media_profiles.py` | 平台专用渲染配置 |
| `styles/playbook_loader.py` | playbook 加载、校验与设计智能 |
| `tools/base_tool.py` | ToolContract 基类 |
| `tools/tool_registry.py` | 工具发现与能力报告 |
| `tools/cost_tracker.py` | 预算治理 |
| `tools/video/video_stitch.py` | 多片段拼接、空间布局、验证与预览 |
| `tools/video/video_compose.py` | 按 `edit_decisions.render_runtime` 路由到 Remotion、HyperFrames 或 FFmpeg |
| `tools/video/hyperframes_compose.py` | HyperFrames workspace、检查与渲染 |
| `tools/graphics/threejs_world.py` | 本地语义 3D 世界创作 |
| `tools/graphics/threejs_asset_catalog.py` | CC0 GLTF/GLB 目录、资产清单与来源记录 |
| `tools/graphics/atlas_3d.py` | Atlas Cloud Tripo H3.1 文生 3D |
| `tools/graphics/fal_3d.py` | fal.ai Hunyuan 3D 与 SAM 3D 路径 |
| `tools/graphics/blender_world.py` | Blender 4.5 LTS 世界组装、灯光、镜头与 Eevee Next 渲染 |
| `tools/character/character_animation.py` | 角色规范、SVG rig、pose library、动作时间线、HyperFrames package 和 QA |
| `lib/hyperframes_style_bridge.py` | playbook 到 CSS custom properties 与 `DESIGN.md` 的桥接 |
| `remotion-composer/src/components/` | Remotion 组件 |
| `.agents/skills/hyperframes*/` | HyperFrames Layer 3 Skill |
| `skills/core/hyperframes.md` | HyperFrames 与 Remotion 的 Layer 2 选择指南 |
| `schemas/styles/playbook.schema.json` | playbook Schema v2 |
| `tests/qa/` | 工具和成片质量验证脚本 |

## 可用流水线

| pipeline | manifest | 用途 |
|---|---|---|
| `talking-head` | `pipeline_defs/talking-head.yaml` | 以人物素材为主 |
| `animated-explainer` | `pipeline_defs/animated-explainer.yaml` | AI 生成解说 |
| `screen-demo` | `pipeline_defs/screen-demo.yaml` | 屏幕演示 |
| `clip-factory` | `pipeline_defs/clip-factory.yaml` | 批量提取短视频 |
| `podcast-repurpose` | `pipeline_defs/podcast-repurpose.yaml` | 播客再利用 |
| `cinematic` | `pipeline_defs/cinematic.yaml` | 电影感剪辑 |
| `documentary-montage` | `pipeline_defs/documentary-montage.yaml` | 从真实素材与开放档案中检索并制作主题蒙太奇 |
| `animation` | `pipeline_defs/animation.yaml` | 动画优先 |
| `character-animation` | `pipeline_defs/character-animation.yaml` | 本地 rigged character 动画 |
| `hybrid` | `pipeline_defs/hybrid.yaml` | 原始素材与辅助视觉混合 |
| `avatar-spokesperson` | `pipeline_defs/avatar-spokesperson.yaml` | Avatar 主播 |
| `localization-dub` | `pipeline_defs/localization-dub.yaml` | 本地化与配音 |
| `framework-smoke` | `pipeline_defs/framework-smoke.yaml` | 测试框架 |

pipeline 的稳定性、阶段和工具以实时 manifest 为准，不能从本文表格推断或硬编码。

## 新增流水线

1. 在 `pipeline_defs/` 创建通过 `pipeline_manifest.schema.json` 校验的 YAML manifest。
2. 在 `skills/pipelines/<pipeline-name>/` 创建各阶段 director Skill。
3. 在 manifest 中引用 reviewer 与 checkpoint-protocol 等 meta Skill。
4. 添加与该 pipeline 兼容的 playbook。
5. 在 `tests/contracts/` 添加契约测试。

## 新增工具

1. 继承 `tools/base_tool.py` 中的 `BaseTool`。
2. 放入正确的 capability package，例如 `tools/audio/`、`tools/video/`、`tools/enhancement/`、`tools/analysis/`、`tools/graphics/`、`tools/avatar/` 或 `tools/subtitle/`。
3. 优先采用 selector + provider tool 模式。
4. 填写所有 contract 字段，包括 `name`、`version`、`tier`、`capability`、`provider`、`supports`、`fallback_tools` 与 `agent_skills`。
5. 实现返回 `ToolResult` 的 `execute()`。
6. 让 `tools/tool_registry.py` 自动发现，不能依赖临时 import。
7. 复杂输入输出应在 `schemas/tools/` 中添加 JSON Schema。
8. 运行时路径正确后再补充测试。

更完整的人类说明见 [中文 Agent 运行指南](AGENT_GUIDE.zh-CN.md) 和 [中文系统架构](docs/ARCHITECTURE.md)。开发时仍应直接核对英文规范上下文与实时代码。
