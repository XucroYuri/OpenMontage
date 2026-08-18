# OpenMontage 中文文档中心

> 简体中文（主文档） | [英文副本](README.en.md)

本仓库把面向用户和开发者的说明文档统一调整为“**中文主文档 + 英文副本**”：不带语言后缀的原路径用于简体中文，原有英文内容完整保存在同目录的 `*.en.md` 文件中。这样 GitHub、现有书签和代码注释默认进入中文说明，同时英文资料仍可审阅、比较和引用。

## 开始使用

- [项目概览与快速开始](../README.md)
- [提示词画廊](../PROMPT_GALLERY.md)
- [贡献指南](../CONTRIBUTING.md)
- [提供商配置、成本与能力说明](PROVIDERS.md)
- [Apple Silicon MPS 配置](apple-silicon-mps.md)

## 架构与开发

- [系统架构](ARCHITECTURE.md)
- [Pull Request 审查指南](PR_REVIEW_GUIDE.md)
- [ComfyUI 适配器计划](comfyui-adapter-plan.md)
- [赞助商维护说明](SPONSORS.md)
- [Backlot 制作看板](../backlot/README.md)
- [Ink Theater](../ink-theater/README.md)
- [Ink Theater 示例](../ink-theater/examples/README.md)
- [Ink Puppet 动捕说明](../ink-theater/mocap/NOTE.md)
- [Remotion 场景类型](../remotion-composer/SCENE_TYPES.md)
- [QA 计划](../tests/qa/QA_PLAN.md)
- [Codex 提示词入口](../.codex/prompts/README.md)

## Agent 运行时契约

以下文件直接参与 Agent 路由或跨工具兼容，不能像普通说明文档一样重命名、翻译机器值或把中文译文声明为运行时规范：

- [`AGENT_GUIDE.md`](../AGENT_GUIDE.md)：规范 Agent 的流水线、工具、审批与质量门槛；中文伴随说明见 [`AGENT_GUIDE.zh-CN.md`](../AGENT_GUIDE.zh-CN.md)。
- [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md)：Agent 共享的架构上下文；中文伴随说明见 [`PROJECT_CONTEXT.zh-CN.md`](../PROJECT_CONTEXT.zh-CN.md)。
- `AGENTS.md`、`CLAUDE.md`、`CODEX.md`、`COPILOT.md`、`CURSOR.md`、`.github/copilot-instructions.md` 与 `.cursor/rules/openmontage.mdc`：固定入口文件，必须保持工具可发现的文件名和契约语义。
- `skills/`、`.agents/skills/`、`pipeline_defs/`、`schemas/`：分别承载工作方法、提供商知识、流水线定义和机器校验契约。中文交互不意味着机械翻译这些内部内容。

这项例外用于保护功能完整性：用户看到中文决策、说明、审批、成本和错误信息；内部仍保留规范的 pipeline ID、stage 名、Schema 字段、枚举、工具/提供商/模型名、命令、路径、环境变量和高质量 provider prompt。

## 文件命名约定

| 用途 | 路径示例 | 地位 |
|---|---|---|
| 简体中文主文档 | `docs/PROVIDERS.md` | 默认入口，优先维护 |
| 英文副本 | `docs/PROVIDERS.en.md` | 保留英文原文，供对照与英文用户使用 |
| 历史兼容入口 | `README_zh-CN.md` | 仅重定向到新的中文主文档，避免旧链接失效 |
| 机器契约中文伴随说明 | `AGENT_GUIDE.zh-CN.md` | 帮助中文开发者理解；英文原文件仍是运行时规范 |

修改说明文档时，应同步检查中英文互链、相对路径、代码围栏、表格，以及命令和机器标识符是否保持原值。若两种语言出现事实冲突，以实时代码、Schema、注册表和流水线清单为准，并同时修正文档。
