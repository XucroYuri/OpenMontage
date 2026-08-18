# OpenMontage Agent 运行指南（完整中文伴随翻译）

> **人类可读的简体中文伴随说明** | [英文规范机器契约](AGENT_GUIDE.md)
>
> 对应英文源文件 Blob：`5bbd9a5bbe93c3abfdf80527b4d2f67ecf494dfb`
> 同步日期：2026-08-18

从这里开始了解 OpenMontage 的完整运行方式。Agent 运行时仍必须读取并执行 [`AGENT_GUIDE.md`](AGENT_GUIDE.md)；本文逐节翻译英文规范，帮助中文开发者审阅，但不会替代英文机器契约。若两者存在差异，以英文规范、实时代码、registry、pipeline manifest 和 Schema 为准。

架构、关键文件和工程约定见 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)；中文伴随说明见 [`PROJECT_CONTEXT.zh-CN.md`](PROJECT_CONTEXT.zh-CN.md)。中文术语统一规则见 [`docs/TERMINOLOGY.md`](docs/TERMINOLOGY.md)。

## 用户语言：任何面向用户的输出前必须阅读（User Language — Read Before Any User-Facing Output）

开始面向用户的工作或流水线工作前，读取 `skills/meta/user-language.md`。它把交互语言、成片内容语言和 provider 工作语言分开，避免汉化降低制作质量或工具能力。

展示接入说明、能力、提案、审批、错误、成本、进度或交付说明前，从 `config.yaml` 读取 `interaction.locale`。仓库默认值为 `zh-CN`。

当有效 locale 为 `zh-CN` 时：

1. 使用清晰的简体中文与用户交流，不能要求用户理解英文标题、状态、取舍、警告或下一步。
2. 除非用户指定其他内容语言，否则人类可读的产物也使用中文，包括概念、脚本、旁白、画面文字、字幕、审查摘要、发布元数据和决策理由。
3. provider prompt 和搜索词采用相关 Layer 2 / Layer 3 Skill 推荐的最佳语言和结构。不得仅因界面使用中文就机械翻译成熟提示词。
4. 机器标识保持不变：Schema key、JSON/YAML 字段、stage、pipeline ID、路径、命令、tool/provider/model 名、API 参数、locale code 和 artifact 文件名。向用户展示时用中文解释。
5. 将 provider 错误转成可执行的中文说明；有助排错时，另行保留原始技术错误。
6. 用户明确指定的语言覆盖当前对话或交付物的配置默认值。除非 brief 要求翻译，否则不得翻译用户源内容。

内部指令文件可以保留英文。指令中引用的英文用户文案只是语义模板，不构成语言锁；实现细节不能导致面向用户的界面只能使用英文。

## 首次交互：接入引导（First Interaction — Onboarding）

当用户第一条消息含糊、探索性较强，或只问“能做什么”“帮我做个视频”“我想做内容”时，任何其他操作前先读取：

`skills/meta/onboarding.md`

该 Skill 指导能力发现、环境分类、通俗能力菜单和适合现有工具的起步提示。目标是在 60 秒内让用户从好奇进入实际创作。

若用户已经给出具体、可执行的请求，例如“制作一段 60 秒黑洞解说”，跳过接入引导，直接执行 Rule Zero。

## 参考视频入口（Reference Video Entry Point）

用户提供视频 URL 或本地视频作为灵感，并要求“做一个类似的”时，不得把它当成普通网络搜索或提示词编写任务。这是 OpenMontage 的一级工作流。

### 必须执行的行为（Required behavior）

1. 读取 `skills/meta/video-reference-analyst.md`。
2. 使用本地分析工具执行参考视频分析：`video_analyzer`、转录提取、场景检测和帧采样。
3. 基于证据总结参考视频的内容、节奏、结构、风格和有效原因。
4. 然后执行正常的能力审计和流水线选择。
5. 为用户版本提出 2–3 个差异明显的概念，不能直接复制原片。

### 关键区别（Important distinction）

- 参考驱动：“做一个像这个的视频” → 使用 `video-reference-analyst.md`。
- 源素材剪辑：“剪辑这段素材”“把它切成短片” → 使用 `source_media_review` 和匹配的 footage-led pipeline。

把两者混淆后退回“搜索 + 猜测”不符合 OpenMontage 契约。

## Rule Zero：所有制作必须进入流水线（Rule Zero — All Production Goes Through a Pipeline）

**每个视频制作请求都必须经过 pipeline system，没有例外。**

用户要求制作、创建或生成任何视频内容时，Agent 必须：

1. **识别 pipeline。** 在 `pipeline_defs/` 中匹配；无法确定时询问用户。
2. **读取 pipeline manifest。** 打开 `pipeline_defs/<pipeline>.yaml`，掌握阶段、工具和质量门槛。
3. **运行 preflight。** 通过 registry 发现真实工具并展示能力菜单。
4. **逐阶段执行。** 每个 stage 开始工作前，先读取 `skills/pipelines/<pipeline>/<stage>-director.md`。
5. **调用工具前读取 Layer 3 Skill。** 工具有 `agent_skills` 时，先读 `.agents/skills/` 中对应 Skill，获取 provider 专用提示、参数和质量技巧。

不得：

- 编写临时 Python 脚本直接调用生成 API；
- 绕过 pipeline 直接发起 API 请求；
- 未读 stage director Skill 就生成素材；
- 未检查 Layer 3 Skill 就调用工具；
- 绕过 preflight、checkpoint 或 review。

系统智能来自 Skill，而不是临时代码。遵循 director Skill 和 Layer 3 知识的 Agent，质量显著高于使用通用提示直接调用工具的 Agent。

## OpenMontage 是什么（What OpenMontage Is）

OpenMontage 是指令驱动的视频制作系统。AI Agent 本身就是智能控制平面：读取 pipeline manifest、stage director Skill 和 meta Skill，再驱动工具。

```text
Agent 读取 pipeline manifest（YAML）→ 读取 stage director Skill（MD）
→ 使用工具（Python BaseTool 子类）→ 通过 meta Skill 自审
→ 使用 Python utility 写 checkpoint → 在审批门向用户请求批准
```

**Python = 工具 + 持久化。** 编排逻辑、创意决策、审查逻辑和 checkpoint policy 不应写进 Python；Agent 按指令做这些决定。

核心循环：选择 pipeline → preflight → 从 registry 发现真实工具 → 展示概念、工具路径、制作计划与成本 → 逐阶段执行并写入 checkpoint。

## 决策沟通契约（Decision Communication Contract）

任何有意义的制作决定都必须在执行前告诉用户。用户不应在事后猜测使用了哪个 provider、model 或合成路径。

### 执行前声明（Announce Before Execution）

任何付费或会显著影响结果的生成调用前，说明：

- 准确 tool 名；
- provider；
- model 或 provider variant；
- 选择理由；
- 当前是样本还是批量运行。

### 重大变更前询问（Ask Before Major Changes）

以下变更必须先询问用户：

- 更换 provider；
- 更换 model family 或 provider variant；
- 在视频主导和静帧主导之间切换；
- 更换会改变输出性质的 composition engine；
- 删除旁白、音乐或其他已批准元素；
- 从样本模式进入批量模式。

已批准 provider/model 路径内的小幅提示优化无需单独批准，除非它实质改变创意方向。

### 决策变化后必须重新记录（Re-log Changed Decisions (Binding)）

`decision_log` 是 Backlot 的决策栏和制作审计记录；它是**只追加的历史，不是草稿区**。

已记录的选择发生变化时，例如用户更换 voice、Agent 更换 provider/model/runtime/music，或 fallback 覆盖原选择，必须新增 `decision_log` 条目，并复用相同的 `category` 和 `subject`。把旧选项移入 `options_considered`，在 `rejected_because` 中说明变更原因。

只改 `asset_manifest` 或 props 而保留旧决策属于缺陷。Backlot 用 `(category, subject)` 识别同一决策，并把该键的最新条目标为“已修订”；改写 `subject` 会被当作另一项决策。这个规则适用于所有阶段。

### 必须同时展示两种合成引擎（Present Both Composition Runtimes (HARD RULE)）

当机器同时可用 Remotion 与 HyperFrames 时，通过 `video_compose.get_info()["render_engines"]` 核实，并在 proposal 阶段锁定 `render_runtime` 前同时向用户展示两者。Agent 可以推荐，但不得静默选择默认值。

每种 runtime 都必须说明：

1. 针对此 brief 最擅长什么；
2. 一项诚实取舍；
3. Agent 推荐及其与 `delivery_promise`、视觉方案的关系。

等待用户明确批准后再前进。`render_runtime_selection` 决策的 `options_considered` 必须记录两个 runtime，以及适用时的 `ffmpeg`。两者均可用却只记录一个，是 CRITICAL reviewer finding。

只有一个 runtime 可用时，可以继续，但必须明确告诉用户另一个为何不可用；决策中仍记录不可用项，并写入 `rejected_because: "runtime not available on this machine"`。

该规则适用于所有调用 `video_compose` 的 pipeline。director Skill 的推荐只是与用户讨论的输入，不是已经作出的决定。

### 合成创作模式：Templated 与 Atelier（Composition Authoring Mode — Templated vs Atelier）

`composition_mode` 与 runtime 正交，表示作品**如何被构建**，必须作为独立 proposal 决策记录为 `category: "composition_mode"`。

- **Templated**：组合 `text_card`、`stat_card`、`bar_chart` 等现有 `cut.type`。快速、便宜、可靠，但容易同质化；适合批量、本地化变体、快速草稿和低风险内部视频。
- **Atelier**：从零手工制作场景、一次性主题和专属动效，使用 `composition_mode: "atelier"` 走 `_render_via_atelier`。每次建立新的视觉语言，不复用创意组件。

营销、发布、品牌和必须令人印象深刻的单一交付 hero work 默认优先 Atelier。原则是：**复用引擎知识，不复用创意组件。** Atelier 中不得使用 stock scene-type catalog、`hyperframes-registry` block、fixture 或成品组件。

制作前先用 `skills/meta/taste-direction.md` 确定设计判断和审美参数，再读取 `skills/meta/bespoke-composition.md`，依次完成：艺术指导（`visual-style`）→ 运动原则（`framer-motion` / `lottie-bodymovin` 中的 Disney 12）→ 引擎机制（`remotion-best-practices`，stock component 只作为机制参考）→ Atelier 渲染。最后做差异性审查：“这会不会像任何其他产品的视频？是否复用了过去的外观？”

Atelier 比 templated 消耗更多 token 和迭代时间，proposal 时必须明确说明。

### 明确升级阻塞问题（Escalate Blockers Explicitly）

出现 blocker 时立即说明：

1. 尝试了什么；
2. 哪里失败；
3. 属于 auth、provider access、tool bug 还是 prompt/design quality；
4. 接下来有哪些选项；
5. 推荐哪个选项及理由。

用户批准前不得继续替代路径。

### 推荐表达方式（Recommendation Style）

请用户选择时，提供短名单、简要取舍和明确推荐，然后等待批准。不能只罗列选项。

### 禁止单方面替代（No Unilateral Substitutions）

已批准路径受阻时可以调查并准备备选，但未经用户批准不得执行。尤其包括 provider/model 互换、fallback tool、用纯提示词替代参考驱动生成，以及用静帧 animatic 替代真实运动画面。

## 编排器（Orchestrator）

Agent 自己编排状态机：

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose`

Agent：

1. 读取 `pipeline_defs/*.yaml`；
2. 调用 `checkpoint.get_next_stage()` 确定恢复点；
3. 读取当前 stage 的 director Skill；
4. 使用 `tools/` 中的具体能力；
5. 使用 `skills/meta/reviewer.md` 自审；
6. 按 `skills/meta/checkpoint-protocol.md` 写 checkpoint；
7. 在 `human_approval_default: true` 时向用户请求批准。

基础设施：`lib/checkpoint.py` 负责检查点读写和阶段校验，`tools/cost_tracker.py` 负责预算治理，`lib/pipeline_loader.py` 负责 manifest 加载。

## 项目目录约定（Project Directory Convention）

每次制作在 gitignored 的 `projects/` 下建立工作区：

```text
projects/<project-name>/
├── artifacts/          # 各阶段 JSON 产物
├── assets/
│   ├── images/         # 图像素材（PNG）
│   ├── video/          # 视频片段（MP4）
│   ├── audio/          # 旁白片段与最终混音（MP3/WAV）
│   ├── music/          # 背景音乐（MP3）
│   └── subtitles.srt   # 字幕
└── renders/
    └── final.mp4       # 最终交付物
```

项目名使用从视频标题派生的 kebab-case，例如 `hidden-math-of-nature`。

pipeline 初始化时：

1. 运行 `python -c "from lib.checkpoint import init_project; init_project('<project-id>', title='<Title>', pipeline_type='<pipeline>')"`，创建目录并写入 Backlot 读取的 `project.json`。
2. 运行 `python -m backlot open <project-id>`。服务启动失败时继续制作；Backlot 只是观察者。Agent 不需要手工同步 UI。

所有 tool 和 Agent 输出都必须显式传入 `projects/<project-id>/` 下的 `output_path`。写入仓库根目录、cwd 或临时目录的素材不会显示在看板上，并违反工作区契约。

Atelier 和 HyperFrames Skill 运行同样受此约束：必须写入已有的 canonical artifact（脚本或 beats plan、等价 `scene_plan`、`asset_manifest`）和 checkpoint。Backlot 与 runtime 无关；只有跳过产物的制作会降级显示。

## 音乐库（Music Library）

用户可把免版税曲目放入 gitignored 的 `music_library/`：

```text
music_library/
├── ambient_track.mp3
├── cinematic_epic.mp3
└── ...
```

asset director 在调用音乐生成 API 前先检查此目录。存在曲目时，proposal 和 assets 阶段应把本地曲目与生成音乐一起列为选项。

## 可用流水线（Available Pipelines）

| Pipeline | 最适用场景 | Stability |
|---|---|---|
| `animated-explainer` | 从主题生成完整解说 | `production` |
| `talking-head` | 人物源素材视频 | `beta` |
| `screen-demo` | 录屏与操作讲解 | `production` |
| `clip-factory` | 从长素材批量切片 | `beta` |
| `podcast-repurpose` | 播客亮点与衍生内容 | `beta` |
| `cinematic` | 预告、先导片和氛围剪辑 | `production` |
| `documentary-montage` | 从真实影像和开放档案检索制作主题蒙太奇 | `beta` |
| `animation` | 动效和动画优先视频 | `production` |
| `character-animation` | 本地绑定卡通角色和可复用表演 | `beta` |
| `hybrid` | 源素材与辅助视觉内容 | `production` |
| `avatar-spokesperson` | Avatar 主播与口型同步视频 | `production` |
| `localization-dub` | 字幕、配音和多语言变体 | `beta` |
| `framework-smoke` | 最小两阶段冒烟测试 | `test` |

`beta` pipeline 尚未完整审计，使用时应告诉用户可能存在粗糙边缘。实时 manifest 是阶段、工具和稳定性的事实来源。

## 强制制作前检查（Mandatory Preflight）

任何创意工作前先执行。优先使用面向人的 `provider_menu_summary()`；不要把可能达到数 MB 的 `support_envelope()` 原始 JSON 粘贴给用户。

```bash
python -c "
from tools.tool_registry import registry
import json
registry.discover()
print(json.dumps(registry.provider_menu_summary(), indent=2))
"
```

摘要包含：

- `composition_runtimes`：`ffmpeg`、`remotion`、`hyperframes` 可用性，是“两种合成引擎必须同时展示”规则的事实来源。
- `capabilities[]`：每个能力族的 `configured / total` 以及 provider 列表。
- `setup_offers[]`：通过简单环境变量即可修复的不可用工具。
- `runtime_warnings[]`：例如 HyperFrames npm package 无法解析等具体警告；必须向用户展示。

需要深入排错时才使用：

```bash
# 按能力分组的完整 provider 菜单
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"

# 每个工具的完整原始契约；仅用于调试
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
```

随后读取 manifest，核对全部 `required_tools` 与 `fallback_tools`，报告 `passed`、`degraded` 或 `blocked`。用户理解真实能力范围前不得开始制作。

### Provider 能力菜单（Provider Menu (Mandatory at Preflight)）

把 `provider_menu_summary()` 翻译为按 capability 分组的用户菜单，不要展示平铺工具列表。每项展示“已配置 X / 共 Y”，先说明现在能做什么，再说明能快速解锁什么。

```text
你的可用能力

  视频生成：       已配置 0 / 共 13
  图像生成：       已配置 1 / 共 7
  Text-to-Speech：已配置 1 / 共 3
  音乐生成：       已配置 1 / 共 1
  视频合成：       已配置 3 / 共 3

  当前可用图像 + TTS + FFmpeg 制作视频。
```

对于不可用 provider，从 menu 的 `install_instructions` 和 `dependencies` 读取实际配置方法，并按难度分组：一分钟环境变量、五分钟安装、复杂 GPU/模型下载。本地与免费路径单列；已经可用的能力也必须明确展示。

规则：

- 不得硬编码 provider 名、API key 名或安装 URL；
- 始终展示 X/Y 比例；
- 按 capability 分组；
- 先说明可立即使用的能力，再说明升级项；
- 用户拒绝配置后继续最佳可用路径，不重复劝说；
- 共用环境变量的工具按 `dependencies` 合并说明。

### 配置帮助协议（Setup Offer Protocol）

| 修复复杂度 | 行为 |
|---|---|
| 一分钟（环境变量） | 读取 `install_instructions`，主动提供配置帮助 |
| 五分钟（安装依赖） | 说明安装内容和价值 |
| 复杂（GPU、模型下载） | 说明限制与可解锁能力，然后继续 |

始终告诉用户缺少什么、获得什么、免费本地与付费 API 的成本差异。用户拒绝后不纠缠。

### `video_compose` 中的合成引擎（Composition Runtimes (Inside video_compose)）

`video_compose` 有三个并列的 render engine，不按优劣排序。proposal 阶段选定并锁定到 `edit_decisions.render_runtime`。

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry._tools['video_compose'].get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
print('HyperFrames note:', info.get('hyperframes_note'))
"
```

| Engine | 用途 | 要求 |
|---|---|---|
| FFmpeg | 纯视频剪切、拼接、裁剪和字幕烧录 | `ffmpeg` binary |
| Remotion | React 合成、静帧动画、文字/统计/图表/字幕、TalkingHead Avatar | Node.js、`npx`、`remotion-composer/`、`node_modules` |
| HyperFrames | HTML/CSS/GSAP、动态排版、产品宣传、网站转视频、SVG 角色 | Node.js ≥ 22、FFmpeg、`npx hyperframes` |

`proposal_packet.production_plan.render_runtime` 锁定后，必须原样传入 `edit_decisions`。compose 时不可用属于结构化 blocker，禁止静默切换。完整决策矩阵见 `skills/core/hyperframes.md`。

### 运动是硬要求的请求（Critical Rule: Motion-Required Requests）

科幻预告、电影感先导片、hype edit、Avatar/Agent 视频，以及承诺依赖动态镜头的 brief，都把运动视为硬要求：

- proposal 时确认所选 runtime 可用；
- 禁止静默降级成 Ken Burns 静帧、animatic 或幻灯片；
- 若改变了视频主导的承诺，禁止 FFmpeg-only fallback；
- `render_runtime="hyperframes"` 锁定后不可用时，先报告、提方案、获批并追加 `render_runtime_selection` 决策；
- runtime 或关键 clip provider 失败时立即停止并告知用户；
- 未获批准不得继续消耗时间制作降级输出。

Remotion 可用时：`flat-motion-graphics` 解说使用 Remotion 动画场景；数据视频使用 stat card 和 chart；静态图片使用 spring animation；CLI/terminal/install 演示优先 `TerminalScene` 合成录屏，而不是操作系统级捕获。真实应用 UI 或不可预测现场行为才使用 `screen_recorder`、`cap_recorder` 或 `playwright-recording`。

### `remotion-composer/` 可用场景类型（Remotion scene types available in `remotion-composer/`）

权威清单和 cut schema 见 `remotion-composer/SCENE_TYPES.md`。当前 `cut.type` 包括：

`text_card`, `stat_card`, `callout`, `comparison`, `hero_title`, `terminal_scene`, `anime_scene`, `bar_chart`, `line_chart`, `pie_chart`, `kpi_grid`, `progress_bar`

overlay 包括 `section_title`, `stat_reveal`, `hero_title`, `provider_chip`。

这些属于 templated 路径。Hero work 优先 Atelier；stock scene 只作为机制参考。未锁定 Remotion 时，Remotion 不可用可由 FFmpeg Ken Burns 提供较弱的动态，但 proposal 必须说明取舍。已经锁定的 runtime 不可用时必须升级为 blocker。

`video_compose` 会根据 `edit_decisions.render_runtime` 自动路由 `_render_via_hyperframes`、`_remotion_render` 或 `_render_via_ffmpeg`；Agent 仍必须在 proposal 时了解两种主 runtime，按 brief 有意识选择。

## 能力发现（Capability Discovery）

能力选择分两层：selector tool 提供 capability-level routing，provider tool 调用具体后端。始终先查询 registry：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

对最终候选检查 `capability`、`provider`、`usage_location`、`supports`、`fallback_tools` 和 `related_skills`。registry 能回答时，不依赖记忆或旧文档。

## 工具能力族（Tool Families）

不得维护硬编码工具列表。运行时查询 registry。重点能力族：

- `tts`：Text-to-Speech，通过 `tts_selector` 路由；
- `video_generation`：云端、本地 GPU 和库存视频，通过 `video_selector`；
- `image_generation`：云端、本地 GPU 和库存图像，通过 `image_selector`；
- `music_generation`：音乐和音效生成；
- `video_post`：本地 FFmpeg 合成、拼接和裁剪；
- `audio_processing`：本地 FFmpeg 混音和增强；
- `analysis`：转录、场景检测和帧采样；
- `avatar`：talking head 和 lip sync；
- `character_animation`：角色规范、SVG rig、pose library、action timeline、preview 和 QA；
- `3d_world_generation`：语义地形、程序化 biome、地标、诊断和确定性 HyperFrames/Three.js 飞行镜头。使用 `threejs_world`，并读取 `skills/creative/3d-world-generation.md` 与 `.agents/skills/threejs-world-generation/SKILL.md`；
- `3d_asset_acquisition`：权利清晰的 GLTF/GLB catalog。使用 `threejs_asset_catalog`；详细或参考级环境不得用 blockout primitive 冒充；
- `3d_asset_generation`：从文本或概念图生成纹理/PBR mesh。文本 hero 素材使用 `atlas_3d`，图像条件和区域对象提取使用 `fal_3d`，并读取 `.agents/skills/3d-asset-generation/SKILL.md`。首次付费调用前说明 provider/model/单价，批量前先采样；
- `3d_world_rendering`：Blender 中的制作级场景组装、地形、灯光、材质、镜头和 image sequence。使用 `blender_world`；参考级密度要求下不能用 Three.js 替代 Blender；
- `enhancement`：upscale、background removal、face enhance 和 color grading。

每个工具声明 `best_for`、`install_instructions`、`runtime`（LOCAL / API / LOCAL_GPU / HYBRID）和 `status`；必须读取这些字段。

### 工具类命名约定（Tool Class Naming Convention）

工具类使用无 `Tool` 后缀的 PascalCase：

| Module | Class Name | 禁止使用 |
|---|---|---|
| `tools.audio.music_gen` | `MusicGen` | `MusicGenTool` |
| `tools.video.video_compose` | `VideoCompose` | `VideoComposeTool` |
| `tools.audio.audio_mixer` | `AudioMixer` | `AudioMixerTool` |
| `tools.tts.elevenlabs_tts` | `ElevenLabsTTS` | `ElevenLabsTTSTool` |
| `tools.analysis.transcriber` | `Transcriber` | `TranscriberTool` |
| `tools.subtitle.subtitle_gen` | `SubtitleGen` | `SubtitleGenTool` |

不确定时运行 `grep "^class " tools/<path>.py`。工具通过 `.execute(params_dict)` 调用，返回含 `.success`、`.data`、`.error` 的 `ToolResult`；不得调用 `.run()`。

### Selector 模式（Selector Pattern）

三个 selector 从 registry 自动发现 provider，新增 provider tool 后无需修改 selector：

| Selector | 路由目标 | 发现方式 |
|---|---|---|
| `tts_selector` | 全部 `capability="tts"` 工具 | `registry.get_by_capability("tts")` |
| `image_selector` | 全部 `capability="image_generation"` 工具 | `registry.get_by_capability("image_generation")` |
| `video_selector` | 全部 `capability="video_generation"` 工具 | `registry.get_by_capability("video_generation")` |

路由优先级：用户偏好 → 可用性 → 发现顺序。selector 负责适配不同 provider 的输入 schema。

## 面向用户的制作计划协议（User-Facing Planning Protocol）

执行前必须展示：

1. brief 仍开放时的 4–5 个概念方向；
2. 推荐 pipeline；
3. 推荐 tool path；
4. 实际可用的替代 tool path；
5. 成本估算和质量取舍；
6. 有音频 pipeline 的强制音乐计划；
7. 按 stage 的制作计划；
8. 素材生成前的审批门。

用户偏好某 vendor 且工具可用时，应直接展示，不能隐藏 provider 选择。

### 音乐计划（Music Plan (Mandatory)）

所有含音频的 pipeline 必须在 proposal/idea 时说明音乐，不能拖到 assets 阶段才暴露失败。按顺序检查：

1. `registry.get_by_capability("music_library")` 与 `music_library/`，列出曲目和时长；
2. `music_search` 的免版税搜索/下载工具，说明许可证与密钥；
3. `music_generation`，如实说明状态、额度、成本和质量；
4. 用户自行把曲目放入 `music_library/`。

始终让用户明确选择：本地哪首曲目、另行提供、通过可用 API 生成，或无音乐继续。没有任何音乐来源时立即告知，并把决定写入 proposal/brief artifact。

## 流水线素材预期（Pipeline Asset Expectations）

manifest 中每个 stage 的 `tools_available` 是权威工具范围。多 provider 能力使用 selector，由 selector 路由到真实可用 provider。

## 阶段 Agent（Stage Agents）

每个 stage 产生一个 canonical artifact，作为下一阶段契约：

| Stage | Director Skill | Canonical output | 核心质量标准 |
|---|---|---|---|
| `idea` | `*-director.md` | `brief` | hook、平台、时长、基调和意图明确 |
| `script` | `*-director.md` | `script` | 结构、计时、叙事和旁白有效 |
| `scene_plan` | `*-director.md` | `scene_plan` | 场景有序，时间和素材要求明确 |
| `assets` | `*-director.md` | `asset_manifest` | 来源、路径、model/tool metadata 和场景关联完整 |
| `edit` | `*-director.md` | `edit_decisions` | cut、overlay、字幕和音乐决策具体 |
| `compose` | `*-director.md` | `render_report` | 路径、编码配置和验证记录完整 |

`completed` 或 `awaiting_human` checkpoint 必须包含当前 stage 的 canonical artifact，并通过 `schemas/artifacts/` 对应 JSON Schema。媒体文件放在阶段专用目录；记录 seed 和 model version 以便复现。

## Reviewer 协议（Reviewer Protocol）

`skills/meta/reviewer.md` 是建议型 meta Skill，不直接阻止阶段推进。

- 每个 stage 执行后、写 checkpoint 前自审；
- 从 manifest 读取该 stage 的 `review_focus`；
- 最多两轮，之后带警告前进；
- finding 分为 `critical`、`suggestion`、`nitpick`；
- `critical` 必须修复并复审，`suggestion` 记录后继续；
- playbook `quality_rules` 是约束，不是建议。

## 人工检查点协议（Human Checkpoint Protocol）

`skills/meta/checkpoint-protocol.md` 规定何时暂停：

- manifest 的 `human_approval_default` 具有约束力，Agent 不得重新判断；`lib/checkpoint.py` 禁止未带 `human_approved=True` 的 gated stage 写成 `completed`。
- 常见 gate 包括 `idea`/`proposal`、`script`、`scene_plan`、`assets` 和部分 `publish`；`documentary-montage` 还会 gate `edit`。只有当前 manifest 是权威来源。
- 需要批准时写 `awaiting_human`，展示 artifact 摘要、review finding 和成本快照，然后**结束当前回合**。同一回复中继续后续 stage 属于 gate violation。
- 每个 gate 分别批准。早期“继续”不覆盖后续 gate；只有写入 `decision_log` 且 `category: "approval_policy"` 的明确全程预授权才有效。

## 沟通协议（Communication Protocol）

Agent 通过 canonical JSON artifact、checkpoint、pipeline manifest 和 tool registry 协作。主要文件：

- Artifact Schema：`schemas/artifacts/`
- Checkpoint Schema：`schemas/checkpoints/checkpoint.schema.json`
- Pipeline manifest Schema：`schemas/pipelines/pipeline_manifest.schema.json`
- Pipeline manifest：`pipeline_defs/`
- Style playbook：`styles/*.yaml`
- Tool contract：`tools/base_tool.py`
- Tool registry：`tools/tool_registry.py`
- Stage director Skill：`skills/pipelines/<pipeline>/<stage>-director.md`
- Meta Skill：`skills/meta/*.md`

Checkpoint 规则：

- 位于 `projects/<project_id>/checkpoint_<stage>.json`；
- `status` 只能是 `completed`、`failed`、`awaiting_human` 或 `in_progress`；
- 进入 stage 时写 `in_progress`；`assets`/`compose` 每完成一个场景或素材单元后刷新 `metadata.partial_progress`；
- `completed` 和 `awaiting_human` 必须带 canonical artifact；
- gated stage 只有 `human_approved=True` 才能写 `completed`；
- 被替换的 checkpoint 自动归档到 `history/`；
- 无效 checkpoint 或 canonical artifact 必须快速失败。

Pipeline manifest 规则：

- `pipeline_defs/` 中的声明式 YAML 是事实来源；
- stage 声明 `skill`、`produces`、`tools_available`、`review_focus`、`success_criteria`、`human_approval_default`；
- 新 pipeline 需要 manifest 和全部 stage director Skill。

Tool 规则：每个制作工具继承 `BaseTool`，从 registry 发现，support envelope 是能力、状态和资源要求的事实来源。

## 风格 Playbook（Style Playbooks）

| Playbook | 最适用场景 |
|---|---|
| `clean-professional` | 企业、教育、SaaS |
| `premium-minimalist` | 投资人更新、专家讲解、产品叙事 |
| `flat-motion-graphics` | 社交媒体、TikTok、初创公司 |
| `minimalist-diagram` | 技术深潜、架构 |
| `ink-sketch` | 白底手绘墨线、会自绘/行走/跳舞的角色、机械装置讲解 |

定制、Atelier、品牌、发布或 hero work 在选择 playbook 前读取 `skills/meta/taste-direction.md`，把 `taste_profile` 传入 proposal，确保后续阶段保留设计判断、视觉差异、运动强度、信息密度、参考策略和反例。

### 手绘涂鸦动画（Hand-drawn "doodle" animation → Ink Theater / Ink Puppet）

手绘墨线、草图活过来、铅笔/火柴人行走或跳舞、whiteboard doodle explainer 等 brief 使用 `skills/creative/ink-theater.md` 和 `ink-theater/README.md`。这是风格与可复用引擎，不是新 pipeline：插画/机械装置走 `animation`，动捕角色走 `character-animation`。入口 `/ink-art` 用于从零创建矢量涂鸦；`/animated-drawing` 用于让用户提供的光栅图画动起来。角色动作只能选命名 mocap clip，不得手调。

## 三层知识地图（Layer Map）

1. `tools/`：有哪些能力、可用性、成本、runtime、fallback 和相关 Skill。
2. `skills/`：OpenMontage 如何在 pipeline 中使用能力。
3. `.agents/skills/`：原始 vendor 或技术知识。

读取顺序：registry/tool contract → 相关 pipeline 或 creative Skill → 底层 vendor Skill。

优先从 Skill 学工具用法，不必在常规使用中阅读实现源码。调试、审计和验证治理契约时可以读源码；若 Skill 与工具不一致，应考虑同步 Skill。

Layer 3 不是可选项。每个生成工具的 `agent_skills` 指向 provider 专用提示、参数和质量技巧。例：调用 `kling_video` 前读取 `ai-video-gen`，再使用 Kling 特定提示结构和镜头语法。

### 按类别查找 Layer 3 Skill（Layer 3 skills, by category）

| 类别 | Skills |
|---|---|
| 合成引擎 | `remotion`, `remotion-best-practices`, `synthetic-screen-recording`, `threejs-world-generation` |
| 通用动画 | `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-scrolltrigger`, `gsap-frameworks`, `framer-motion`, `lottie-bodymovin` |
| 角色动画 | `character-rigging`, `svg-character-animation`, `pose-library-design`, `canvas-procedural-animation`, `character-animation-qa` |
| 图像生成 | `bfl-api`, `flux-best-practices` |
| 视频生成 | `seedance-2-0`, `gemini-omni`, `ai-video-gen`, `ltx2` |
| 音频 | `elevenlabs`, `music`, `sound-effects`, `acestep`, `text-to-speech`, `azure-text-to-speech`, `setup-api-key` |
| Speech-to-Text | `speech-to-text`, `azure-speech-to-text` |
| Avatar / lip-sync | `avatar-video`, `heygen`, `create-video`, `faceswap`, `video-translate`, `agents` |
| 捕获 | `playwright-recording`, `ffmpeg` |
| 可视化 | `beautiful-mermaid`, `d3-viz`, `manim-composer`, `manimce-best-practices`, `manimgl-best-practices` |
| 媒体编辑 | `video-edit`, `video-download`, `video-understand`, `video-toolkit`, `visual-style` |

不确定动画 runtime 时先读 `skills/meta/animation-runtime-selector.md`；选择真实录屏或合成终端时，读取 `pipeline_defs/screen-demo.yaml` 与 `skills/pipelines/screen-demo/idea-director.md`。

## 快速查找（Quick Lookup）

| 问题 | 位置 |
|---|---|
| 有哪些工具？ | `tools/tool_registry.py` 和 `registry.support_envelope()` |
| 某 capability 有哪些 provider？ | `registry.capability_catalog()` |
| 某 vendor 有哪些工具？ | `registry.provider_catalog()` |
| 工具怎样工作？ | registry 中的 `usage_location` |
| 某 stage 应怎样执行？ | `skills/pipelines/<pipeline>/...` |
| checkpoint/review 规则？ | `skills/meta/` |

## 禁止事项（What Not To Do）

- 不得绕过 pipeline，编写临时脚本直接调用工具；所有制作遵循 Rule Zero。
- 不得在未读取 `agent_skills` 指向的 Layer 3 Skill 前调用生成工具。
- 不得跳过 stage director Skill。
- 不得使用已删除的旧名称 `tts_cloud`、`tts_engine` 或 `video_gen`。
- 不得硬编码 provider 名、API key 名或配置 URL；从 registry 的 `install_instructions` 和 `dependencies` 读取。
- 受限共享安装用户不得被要求自行添加 credential、创建 `.env` 或导出 key；应向管理员提出配置请求，并只使用集中提供的能力。
- 提供 vendor credential 前，先检查 registry 是否已有配置好的 wrapper，例如 fal.ai 上的合作模型。
- 用户批准制作计划前不得开始素材生成。
- 不得隐藏降级路径；替代和受阻选项必须明确记录。
- 不得只展示一个不可用工具；始终呈现完整 capability 范围，例如“已配置 X / 共 Y 个 provider”。
- preflight 不得跳过 Provider Menu。
- 未告知用户并在重大变化时获得批准前，不得更换 provider、model 或 render path。
