# OpenMontage 中文术语表

> 简体中文（主文档） | [英文副本](TERMINOLOGY.en.md)

本表用于统一面向用户的简体中文文案。机器契约中的英文标识符保持不变：JSON/YAML 字段、enum、pipeline ID、stage、artifact 名、工具/提供商/模型名、命令、路径和环境变量均不得翻译。

| 规范英文 | 中文显示 | 使用说明 |
|---|---|---|
| asset | 素材 | 指图像、视频、音频、字幕、3D 模型等制作资源；机器字段仍为 `asset` / `assets` / `asset_manifest` |
| artifact | 产物 | 指阶段输出的结构化契约，例如 `brief`、`scene_plan`、`render_report` |
| pipeline | 流水线 | 用户文案使用“流水线”；机器 ID 如 `animated-explainer` 不变 |
| stage | 阶段 | 用户文案可写“脚本阶段”；机器值如 `scene_plan`、`assets` 不变 |
| checkpoint | 检查点 | 指可恢复的阶段状态文件；文件名 `checkpoint_<stage>.json` 不变 |
| render runtime | 合成引擎 | 指 `ffmpeg`、`remotion`、`hyperframes`；字段 `render_runtime` 不变 |
| renderer family | 渲染器系列 | 与 `render_runtime` 区分；字段 `renderer_family` 不变 |
| provider | 提供商 | 首次出现可写“提供商（provider）”；规范值如 `kling_official` 不变 |
| selector | 选择器 | 指按 capability 路由的工具，例如 `tts_selector` |
| storyboard | 故事板 | 指按场景组织的视觉计划和审查界面 |
| filmstrip | 分镜条 | 指 Backlot 中按时间排列的场景/候选画面条带 |
| contact sheet | 候选缩略图总览 | 指同时检查多张候选或验证帧的网格图，不译作“联系表” |
| brief | 创意简报 | 字段和 artifact 名 `brief` 不变 |
| review | 审查 | 质量判断使用“审查”；人工确认使用“审批” |
| approval gate | 审批门 | 指必须等待用户明确批准的阶段边界 |
| fallback | 后备方案 | 若会改变已批准的 provider、model、runtime 或成片性质，执行前仍须重新批准 |
| preflight | 制作前检查 | 首次出现可写“制作前检查（preflight）” |
| raw data | 原始数据 | 必须保留规范字段和枚举，不能为汉化而改写 |

## 编辑规则

- 中文优先表达含义，技术标识紧随其后并使用代码格式。
- 同一概念不混用“资产 / 素材”、“工件 / 产物”、“管线 / 流水线”。
- “生成素材”描述制作动作；“阶段产物”描述结构化 JSON 契约。
- `runtime` 单独出现且明确指视频合成时译为“合成引擎”；若指 Python/Node 运行环境，则译为“运行环境”。
- provider prompt、用户源内容、品牌名和专有名词按来源与相关 Skill 保持最佳语言，不做机械翻译。
