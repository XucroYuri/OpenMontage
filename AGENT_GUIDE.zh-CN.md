# OpenMontage Agent 运行指南（中文伴随说明）

> **人类可读的简体中文说明** | [英文规范机器契约](AGENT_GUIDE.md)

本文帮助中文开发者理解 OpenMontage Agent 的运行方式和不可削弱的质量边界。Agent 运行时仍必须读取并执行 [`AGENT_GUIDE.md`](AGENT_GUIDE.md)；本文不会替换该文件，也不能作为修改 pipeline ID、Schema 字段、命令或 provider prompt 的依据。若两份文件存在差异，以英文规范契约、实时注册表、流水线清单和 Schema 为准。

## 最重要的原则

OpenMontage 是一个**由指令驱动、由 Agent 编排**的视频制作系统。Python 负责工具能力和状态持久化；Agent 负责读取流水线清单与 Skill、进行创意和技术决策、调用工具、自审、写入检查点并请求人工批准。

任何视频制作请求都必须进入 `pipeline_defs/` 中定义的流水线，不能跳过 preflight、阶段导演 Skill、provider Skill、质量审查、成本治理或人工审批门。

```text
选择 pipeline
  -> 读取 pipeline manifest
  -> 运行 preflight 并展示真实能力范围
  -> 逐阶段读取 director skill
  -> 调用 registry 中的工具
  -> 自审并写入 canonical artifact / checkpoint
  -> 在规定的 gate 等待用户批准
  -> 渲染并验证交付物
```

## 三种语言必须相互独立

| 层级 | 控制内容 | 中文环境下的行为 |
|---|---|---|
| 交互语言 | 对话、方案、成本、审批、进度、警告、错误和交付说明 | 使用清晰的简体中文 |
| 成片内容语言 | 脚本、旁白、对白、画面文字、字幕和发布文案 | 默认跟随交互语言，也可由用户单独指定 |
| provider 工作语言 | 生成提示词、搜索词、结构化工具输入和模型专用术语 | 采用相关 Layer 2 / Layer 3 Skill 推荐的最佳语言和结构 |

汉化不能改变或翻译以下机器值：Schema key、JSON/YAML 字段、enum、pipeline ID、stage 名、artifact 名、tool/provider/model 名、API 参数、locale code、命令、路径、环境变量和源 URL。中文界面应解释这些值，而不是改写它们。

## 请求入口与路由

- 用户只是笼统询问“能做什么”或“帮我做视频”时，先读取 `skills/meta/onboarding.md`，完成能力发现和需求澄清。
- 用户已经给出明确、可执行的视频需求时，直接选择匹配的 pipeline。
- 用户提供视频 URL 或本地视频并要求“做成类似风格”时，先读取 `skills/meta/video-reference-analyst.md`，分析转录、节奏、结构、场景、关键帧和风格，再提出 2–3 个有差异的创意方向。
- 用户要求剪辑其原始素材时，使用素材审查和 footage-led pipeline，不能把它误判成参考视频模仿。

## 制作前必须完成 preflight

先调用工具注册表的 `provider_menu_summary()`，并把结果翻译成用户能理解的能力菜单。必须说明：

- 每类能力当前配置数量与总数；
- 已经可用的工具和能够立即完成的制作路径；
- 简单配置即可解锁的能力及其实际收益；
- 本地、免费路径与付费 API 的成本和质量差异；
- runtime warning、缺失依赖及受影响的功能；
- 所选 pipeline 的 `required_tools`、可用 fallback，以及状态是 `passed`、`degraded` 还是 `blocked`。

不允许硬编码 provider、API key 名或安装 URL；它们必须来自注册表的 `install_instructions`、`dependencies` 与实时状态。受限共享安装环境中的用户不应被要求自行写入凭据，应把这类需求表述为管理员配置事项。

## 方案阶段必须让用户知道并批准什么

在付费或会显著影响成片的调用之前，说明准确的 tool、provider、model/variant、选择理由，以及当前是样本还是批量生成。

以下变更必须重新征得批准：

- 更换 provider 或 model family；
- 更换已批准的 `render_runtime`；
- 从视频主导改为静帧主导，或反向切换；
- 删除旁白、音乐或其他已批准元素；
- 从样本模式进入批量生成；
- 已批准路径受阻后采用替代方案。

所有重要选择写入 append-only 的 `decision_log`。同一决策发生变化时，必须使用相同的 `(category, subject)` 新增一条修订记录，不能静默覆盖旧记录或只改下游 artifact。

## 合成 runtime 与创作模式

`render_runtime` 和 `composition_mode` 是两个不同决定。

当机器同时具备 Remotion 与 HyperFrames 时，方案阶段必须把两者都展示给用户，分别说明针对当前 brief 的优势和代价，再给出推荐并等待明确批准。若某个 runtime 不可用，应明确说明，并在 `decision_log` 中记录不可用原因。

| runtime | 典型用途 |
|---|---|
| `ffmpeg` | 裁剪、拼接、字幕烧录和纯视频后期 |
| `remotion` | React 场景、图表、卡片、字幕、图片动画和确定性 UI/终端演示 |
| `hyperframes` | HTML/CSS/GSAP、动态排版、产品宣传、SVG 角色和定制网页式动画 |

| `composition_mode` | 行为 |
|---|---|
| `templated` | 组合现有 scene type；速度快、成本低、适合批量和草稿 |
| `atelier` | 针对单个作品从头手工设计视觉语言和运动；适合发布、品牌、营销与 hero work |

运动是交付承诺的一部分时，不能在失败后静默降级为 Ken Burns 静帧、animatic 或其他性质不同的成片。应立即报告尝试内容、失败原因、问题类型、可选方案和推荐方案，等待用户批准后再继续。

## 项目工作区与看板

每次制作都在 `projects/<project-id>/` 下建立工作区：

```text
projects/<project-id>/
├── artifacts/
├── assets/
│   ├── images/
│   ├── video/
│   ├── audio/
│   └── music/
└── renders/final.mp4
```

初始化时调用 `lib.checkpoint.init_project(...)`，随后运行 `python -m backlot open <project-id>`。Backlot 是观察者；它启动失败不能阻塞制作。所有工具都必须把输出写入该项目目录中的明确 `output_path`，否则 artifact、看板和恢复流程无法追踪它们。

## 流水线与阶段契约

当前主要 pipeline 包括：`animated-explainer`、`talking-head`、`screen-demo`、`clip-factory`、`podcast-repurpose`、`cinematic`、`documentary-montage`、`animation`、`character-animation`、`hybrid`、`avatar-spokesperson`、`localization-dub` 与测试用 `framework-smoke`。实际可用阶段、工具、gate 和稳定性以对应 manifest 为准。

典型阶段顺序为：

```text
idea -> script -> scene_plan -> assets -> edit -> compose -> publish
```

每个阶段都要先读取其 director Skill，并产生供下一阶段使用的 canonical artifact。常见映射如下：

| stage | canonical artifact |
|---|---|
| `idea` | `brief` |
| `script` | `script` |
| `scene_plan` | `scene_plan` |
| `assets` | `asset_manifest` |
| `edit` | `edit_decisions` |
| `compose` | `render_report` |
| `publish` | `publish_log` |

artifact 必须通过 `schemas/artifacts/` 中的 JSON Schema。进入阶段时写入 `in_progress` checkpoint；完成或等待人工批准时必须携带 canonical artifact。manifest 中的 `human_approval_default` 是强制规则：需要批准的阶段必须写为 `awaiting_human` 并结束当前回合，收到明确批准后才能继续。

## 审查、成本与音乐

- 每个阶段完成后、写 checkpoint 前，使用 `skills/meta/reviewer.md` 自审。
- `critical` 问题必须修复；最多进行两轮自审，之后带警告前进。
- `tools/cost_tracker.py` 按 estimate → reserve → reconcile 管理预算。
- 任何有音频的 pipeline 都必须在方案阶段说明音乐来源：用户 `music_library/`、免版税搜索、音乐生成 API、用户自行提供，或明确选择无音乐。
- 在素材阶段第一次暴露“没有音乐来源”属于流程缺陷。

## 工具与 Skill 的三层关系

1. `tools/` 与 registry 说明**有什么、是否可用、成本和 fallback**。
2. `skills/` 说明 **OpenMontage 在当前 pipeline 中如何使用能力**。
3. `.agents/skills/` 说明 **具体 provider 或技术怎样取得最佳效果**。

调用生成工具前，必须读取工具的 `agent_skills` 指向的 Layer 3 Skill。不能因为界面使用中文，就机械翻译或缩短经过验证的 provider prompt。

所有工具类使用不带 `Tool` 后缀的 PascalCase，并通过 `.execute(params_dict)` 返回 `ToolResult`。能力选择应通过 registry 和 selector（如 `tts_selector`、`image_selector`、`video_selector`），不能依赖记忆中的硬编码工具清单。

## 禁止事项

- 不得绕过 pipeline，直接写临时脚本调用生成 API。
- 不得跳过 stage director Skill 或 provider Layer 3 Skill。
- 不得跳过 preflight、成本说明、审查、checkpoint 或人工审批门。
- 不得在用户不知情时更换 provider、model、runtime 或视觉处理路径。
- 不得用不可用工具的单点报错代替完整能力菜单。
- 不得为了表面汉化翻译机器标识、用户源素材或品牌专名。
- 不得让仍在等待人工批准的阶段继续执行。

开发和排错时，请直接查阅 [英文规范契约](AGENT_GUIDE.md)、[中文项目上下文](PROJECT_CONTEXT.zh-CN.md)、[系统架构](docs/ARCHITECTURE.md)、实时 registry、相关 pipeline manifest 与 Schema。
