# OpenMontage Chinese terminology reference

> [简体中文（主文档）](TERMINOLOGY.md) | English copy

This reference defines the Simplified Chinese labels used by the Chinese-first documentation and UI. It does not rename canonical JSON/YAML fields, enum values, pipeline IDs, stages, artifact names, tool/provider/model names, commands, paths, or environment variables.

| Canonical English | Chinese presentation label | Boundary |
|---|---|---|
| asset | 素材 | Production media/resources; keep `asset`, `assets`, and `asset_manifest` canonical |
| artifact | 产物 | Structured stage contract such as `brief`, `scene_plan`, or `render_report` |
| pipeline | 流水线 | Keep IDs such as `animated-explainer` canonical |
| stage | 阶段 | Keep values such as `scene_plan` and `assets` canonical |
| checkpoint | 检查点 | Keep `checkpoint_<stage>.json` filenames canonical |
| render runtime | 合成引擎 | Keep `render_runtime` and its enum values canonical |
| renderer family | 渲染器系列 | Distinct from `render_runtime` |
| provider | 提供商 | Keep provider IDs canonical |
| selector | 选择器 | Capability-level router such as `tts_selector` |
| storyboard | 故事板 | Scene-oriented visual plan and review surface |
| filmstrip | 分镜条 | Time-ordered scene/take strip in Backlot |
| contact sheet | 候选缩略图总览 | Grid of candidates or verification frames |
| brief | 创意简报 | Keep the `brief` artifact name canonical |
| review | 审查 | Use 审批 for human approval |
| approval gate | 审批门 | Stage boundary requiring explicit user approval |
| fallback | 后备方案 | Still requires approval when it changes a locked production choice |
| preflight | 制作前检查 | May be introduced as 制作前检查（preflight） |
| raw data | 原始数据 | Preserve canonical keys and enum values |

Chinese copy should consistently use 素材, 产物, and 流水线 rather than mixing near-synonyms. Provider prompts, source content, brands, and proper nouns retain the language required by their source and relevant skills.
