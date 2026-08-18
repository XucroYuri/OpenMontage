<!-- generated-by: gsd-doc-writer -->
> **简体中文（主版本）** | [English (secondary version)](ARCHITECTURE.en.md)

# OpenMontage 架构

> 最后更新：2026-03-28 | 基于代码探索整理，而非源自既有文档。

OpenMontage 是一个**由 Agent 编排的视频制作平台**。LLM 编码助手（Claude Code、Cursor、Copilot 等）充当编排器：读取流水线清单、遵循 Skill 指令、调用 Python 工具并为状态写入检查点。系统不存在运行时 Python 编排器；Agent 本身就是控制平面。

---

## 高层流程

```
用户提供主题/创意
        |
        v
Agent 读取流水线清单（YAML）
        |
        v
对于每个阶段：
   1. Agent 读取阶段导演 Skill（Markdown）
   2. Agent 通过工具注册表调用 Python 工具
   3. Agent 将检查点（JSON）及工件写入磁盘
   4. Agent 使用 meta/reviewer Skill 进行自审
   5. 人工审批门禁（如已配置）
        |
        v
最终视频输出
```

---

## 仓库布局

```
OpenMontage/
├── lib/                    # 核心运行时基础设施（Python）
│   ├── config_model.py     # Pydantic 配置：LLM、预算、检查点、输出、路径
│   ├── checkpoint.py       # 流水线状态持久化与阶段转换
│   ├── pipeline_loader.py  # YAML 清单加载与验证
│   ├── media_profiles.py   # 平台专用渲染配置（YouTube、TikTok 等）
│   ├── env_loader.py       # .env 变量管理
│   └── providers/          # （为未来的 Provider 抽象预留）
│
├── tools/                  # 57+ 个 Python 工具实现
│   ├── base_tool.py        # 抽象基类——工具契约
│   ├── tool_registry.py    # 自动发现的单例注册表
│   ├── cost_tracker.py     # 预算治理（估算 → 预留 → 核销）
│   ├── analysis/           # 转录、场景检测、帧采样、视频理解
│   ├── audio/              # TTS（ElevenLabs、OpenAI、Piper、Azure、Google）、音乐生成、混音、增强
│   ├── avatar/             # 说话人头像动画、口型同步
│   ├── enhancement/        # 超分辨率、背景移除、人脸增强/修复、调色
│   ├── graphics/           # 图像生成（FLUX、GPT Image、Recraft、本地扩散）、素材库、图表、代码片段、数学动画
│   ├── publishers/         # （预留）
│   ├── subtitle/           # 根据时间戳生成 SRT/VTT
│   └── video/              # 13 个视频生成 Provider，以及合成、拼接、裁剪工具
│
├── pipeline_defs/          # YAML 流水线清单
├── schemas/                # 用于验证的 JSON Schema 定义
│   ├── artifacts/          # 11 种工件 Schema（brief → publish_log）
│   ├── checkpoints/        # 检查点状态 Schema
│   ├── pipelines/          # 流水线清单 Schema
│   ├── styles/             # 风格 Playbook Schema
│   └── tools/              # 工具专用 Schema
│
├── skills/                 # 第 2 层：OpenMontage 专用 Agent 指令
│   ├── core/               # FFmpeg、Remotion、WhisperX、调色 Skill
│   ├── creative/           # 视频剪辑、增强、数据可视化、提示词工程
│   ├── meta/               # reviewer、checkpoint-protocol、skill-creator
│   └── pipelines/          # 各流水线的阶段导演 Skill
│
├── .agents/skills/         # 第 3 层：外部技术 Skill（FFmpeg、HyperFrames、GSAP 等）
├── styles/                 # 视觉风格 Playbook（YAML）及其加载器
├── remotion-composer/      # Node.js/React——Remotion 视频合成渲染器
├── tests/                  # 契约测试、QA 集成测试、评估工具链
├── docs/                   # 最佳实践指南、会话交接文档、审计文档
└── config.yaml             # 全局运行时配置
```

---

## 核心架构原则

### 1. Agent 优先的编排方式

系统中**没有 Python 编排器**。LLM Agent 负责：

- 读取流水线清单以了解阶段顺序
- 读取每个阶段的导演 Skill 以获取详细指令
- 调用工具、评估结果并作出创意决策
- 写入检查点，在阶段之间持久化状态

Python 仅提供**工具与持久化能力**。所有智能都存在于 Skill 指令（Markdown）和流水线清单（YAML）中。

### 2. 运行时无需 LLM API Key

OpenMontage 在运行时不会调用 LLM API。运行于用户 IDE 中的编码助手本身就是 LLM。需要生成能力（图像、视频、TTS）的工具会直接调用相应领域的 API（ElevenLabs、fal.ai、HeyGen 等），而不是通用 LLM 端点。

### 3. 双 Provider 支持

每项能力都必须同时支持 **API Provider**（云端、付费）与**本地/开源替代方案**（免费、依赖 GPU）。Selector 模式通过将请求路由到当前可用的实现来执行这一原则。

---

## 工具系统

### BaseTool 契约

所有工具都继承自 `BaseTool`（ABC），并声明以下字段：

| 字段 | 用途 |
|-------|------|
| `name`, `version` | 身份标识 |
| `tier` | CORE、VOICE、ENHANCE、GENERATE、SOURCE、ANALYZE、PUBLISH |
| `capability` | 工具的能力（例如 `tts`、`image_generation`、`video_post`） |
| `provider` | 所属服务（例如 `elevenlabs`、`ffmpeg`、`selector`） |
| `runtime` | LOCAL、LOCAL_GPU、API、HYBRID |
| `stability` | EXPERIMENTAL、BETA、PRODUCTION |
| `dependencies` | 所需二进制文件（`cmd:ffmpeg`）、环境变量（`env:ELEVENLABS_API_KEY`）、Python 包（`python:torch`） |
| `input_schema`, `output_schema` | 输入/输出的 JSON Schema |
| `fallback_tools` | 有序回退链 |
| `agent_skills` | 指向第 3 层知识 Skill 的链接 |
| `resource_profile` | CPU、RAM、VRAM、磁盘、网络需求 |
| `retry_policy` | 最大重试次数、退避策略 |

**必需方法：** `execute(inputs) -> ToolResult`

`ToolResult` 携带：`success`、`data`、`artifacts`（文件路径）、`error`、`cost_usd`、`duration_seconds`、`seed`、`model`。

### 工具注册表

`ToolRegistry` 是一个单例，通过 `pkgutil.walk_packages()` 自动发现所有 `BaseTool` 子类，无需手动注册。

关键查询：

- `get_by_capability("tts")`——所有 TTS 工具
- `get_by_provider("elevenlabs")`——所有 ElevenLabs 工具
- `get_available()`——依赖项均已满足的工具
- `find_fallback("elevenlabs_tts")`——解析回退链
- `support_envelope()`——供 Agent 使用的完整能力报告
- `gpu_required_tools()`、`network_required_tools()`

### Selector 模式

三个 Selector 工具对多 Provider 能力进行抽象：

| Selector | 能力 | 选择方式 |
|----------|------|----------|
| `tts_selector` | 文本转语音 | 根据任务适配度、质量、可控性、可靠性、成本、延迟和连续性对已发现的 Provider 排名 |
| `image_selector` | 图像生成 | 根据实时注册表对已发现的 Provider 排名；没有硬编码的 Provider 顺序 |
| `video_selector` | 视频生成 | 根据实时注册表对已发现的 Provider 排名；用户明确给出偏好时会尊重该偏好 |
| `atlas_image` / `atlas_video` | Atlas Cloud 生成 | 为图像生成/编辑，以及文生视频、图生视频、参考视频和视频编辑提供精确的逐模型路由目录 |

Selector 的路由依据依次是：用户明确设置的偏好，然后是对可用 Provider 的评分排序。Selector 还会透明地适配不同 Provider 的输入 Schema。

### 按类别划分的工具清单

**分析（5）：** transcriber（WhisperX）、azure_stt、scene_detect、frame_sampler、video_understand（CLIP/BLIP-2）

**音频（9）：** elevenlabs_tts、google_tts、openai_tts、piper_tts、azure_tts、tts_selector、music_gen、audio_mixer、audio_enhance

**Avatar（2）：** talking_head（SadTalker/MuseTalk）、lip_sync（Wav2Lip）

**增强（5）：** upscale（Real-ESRGAN）、bg_remove（rembg/U2Net）、face_enhance、face_restore（CodeFormer/GFPGAN）、color_grade（FFmpeg LUT）

**图形（13）：** flux_image、grok_image、google_imagen、openai_image、recraft_image、local_diffusion、pexels_image、pixabay_image、image_selector、code_snippet、diagram_gen、math_animate（ManimCE）、image_gen（已弃用）

**字幕（1）：** subtitle_gen

**视频（18）：** grok_video、heygen_video、higgsfield_video、veo_video、kling_video、runway_video、minimax_video、wan_video、hunyuan_video、cogvideo_video、ltx_video_local、ltx_video_modal、pexels_video、pixabay_video、video_selector、video_compose（FFmpeg）、video_stitch、video_trimmer

---

## 流水线系统

### 流水线清单

每条流水线都由 `pipeline_defs/` 下的一个 YAML 文件定义：

```yaml
name: animated-explainer
version: "2.0"
category: generated          # talking_head | generated | hybrid | screen_recording | animation | cinematic | custom
default_checkpoint_policy: guided

orchestration:
  mode: executive-producer
  skill: pipelines/explainer/executive-producer
  budget_default_usd: 2.00
  max_revisions_per_stage: 3

compatible_playbooks:
  - clean-professional
  - flat-motion-graphics

stages:
  - name: research
    skill: pipelines/explainer/research-director
    produces: [research_brief]
    tools_available: []
    checkpoint_required: false
    human_approval_default: false
    review_focus: [...]
    success_criteria: [...]
  # ... 一直到 publish
```

### 可用流水线

| 流水线 | 类别 | 说明 |
|--------|------|------|
| `animated-explainer` | generated | 使用 AI 制作的解说视频，涵盖调研、旁白、视觉内容和音乐 |
| `animation` | animation | 动态图形、动态排版 |
| `avatar-spokesperson` | talking_head | 由 Avatar 驱动的出镜人视频 |
| `character-animation` | animation | 使用 SVG Rig、姿势库、GSAP Timeline 和 HyperFrames 渲染的本地绑定卡通角色 |
| `cinematic` | cinematic | 预告片、先导片、情绪驱动型剪辑 |
| `clip-factory` | custom | 从长素材批量生成短视频 |
| `hybrid` | hybrid | 源素材与 AI 生成的辅助视觉内容相结合 |
| `localization-dub` | custom | 为现有视频制作字幕、配音和翻译版本 |
| `podcast-repurpose` | hybrid | 将播客亮点转化为视频 |
| `screen-demo` | screen_recording | 软件屏幕录制和操作演示 |
| `talking-head` | talking_head | 以人物讲话素材为主的视频 |
| `framework-smoke` | custom | 用于框架验证的最小烟雾测试 |

### 标准阶段推进顺序

大多数制作流水线遵循一套规范的 8 阶段流程：

```
research → proposal → script → scene_plan → assets → edit → compose → publish
```

每个阶段：

1. 都有一个**阶段导演 Skill**（面向 Agent 的 Markdown 指令）
2. 声明 **`tools_available`**（Agent 可调用的工具）
3. **产出**一个或多个规范工件
4. 包含 **`review_focus`** 标准和 **`success_criteria`**
5. 可以要求在继续前完成**人工审批**

专业流水线可能插入特定领域的阶段。例如，`character-animation` 会在 `scene_plan` 之前添加 `character_design` 和 `rig_plan`，随后输出 HyperFrames 工作区和最终交付物 `projects/<project-name>/renders/final.mp4`。

---

## 检查点系统

检查点以 JSON 形式将流水线状态持久化到项目的 `pipeline/` 目录。

```json
{
  "version": "1.0",
  "project_id": "my-video",
  "stage": "script",
  "status": "completed",
  "timestamp": "2026-03-28T10:00:00Z",
  "checkpoint_policy": "guided",
  "human_approval_required": false,
  "human_approved": true,
  "artifacts": { "script": { ... } },
  "review": { ... },
  "cost_snapshot": { ... }
}
```

**状态值：** `pending` | `in_progress` | `awaiting_human` | `completed` | `failed`

**检查点策略：**

- `guided`——在关键创意阶段设置检查点，机械性阶段自动继续
- `manual_all`——每个阶段都需人工审批
- `auto_noncreative`——除非阶段属于创意阶段（assets、edit），否则自动继续

**函数：** `write_checkpoint()`、`read_checkpoint()`、`get_latest_checkpoint()`、`get_completed_stages()`、`get_next_stage()`

### 规范工件（11 种，全部通过 JSON Schema 验证）

| 工件 | 阶段 | 包含内容 |
|------|------|----------|
| `research_brief` | research | 领域格局分析、数据点、受众洞察、切入角度 |
| `proposal_packet` | proposal | 概念选项、制作计划、成本估算、审批门禁 |
| `brief` | idea | 标题、Hook、关键点、基调、风格、平台、时长 |
| `script` | script | 带时间戳的段落、增强提示、发音指南 |
| `scene_plan` | scene_plan | 包含类型、说明和时间的场景定义 |
| `asset_manifest` | assets | 生成的资产及其路径、来源工具、场景关联关系 |
| `edit_decisions` | edit | 带入点/出点时间的剪辑决策 |
| `render_report` | compose | 输出元数据（格式、分辨率、时长） |
| `publish_log` | publish | 带状态的平台发布条目 |
| `review` | （任意阶段） | 审查反馈和审批记录 |
| `cost_log` | （任意阶段） | 预算跟踪条目 |

---

## 预算治理

`CostTracker` 在整条流水线中执行支出控制。

### 生命周期

```
estimate(tool, operation, $) → entry_id
        |
reserve(entry_id)          # 锁定预算
        |
reconcile(entry_id, $)     # 记录实际支出
```

### 预算模式

| 模式 | 行为 |
|------|------|
| `observe` | 跟踪成本，但不实施限制 |
| `warn` | 超支时记录警告，但允许执行 |
| `cap` | 拒绝会超出剩余预算的操作 |

### 控制项

- **总预算**（默认：$10.00）
- **预留储备**（默认：10%）——作为安全余量保留
- **单次操作审批阈值**（默认：$0.50）——超过该金额时暂停并请求审批
- **新付费工具审批**——首次使用任何付费工具时都需确认
- 按项目持久化至 `cost_log.json`

---

## 三层知识架构

```
第 3 层：.agents/skills/          外部技术知识（47 个 Skill）
         “技术如何工作”               FFmpeg、ElevenLabs API、FLUX、Remotion、Three.js 等
              ^
              | agent_skills[] 引用
              |
第 2 层：skills/                  OpenMontage 约定
         “本项目如何使用技术”          流水线集成、质量检查清单、工件映射
              ^
              | 阶段 Skill 引用
              |
第 1 层：tools/ + pipeline_defs/  可执行能力 + 编排定义
         “存在哪些能力以及何时使用”     BaseTool 契约、流水线清单
```

每个工具的 `agent_skills[]` 字段将第 1 层与第 2、3 层连接起来。例如：

- `video_compose.agent_skills = ["remotion-best-practices", "remotion", "ffmpeg"]`
- `tts_selector.agent_skills = ["text-to-speech", "elevenlabs", "openai-docs"]`

---

## 配置

### config.yaml

```yaml
llm:
  provider: anthropic
  temperature: 0.7
  max_tokens: 4096

budget:
  mode: warn
  total_usd: 10.00
  reserve_pct: 0.10
  single_action_approval_usd: 0.50

checkpoint:
  policy: guided
  storage_dir: pipeline

output:
  default_format: mp4
  default_codec: libx264
  default_audio_codec: aac
  default_resolution: 1920x1080
  default_fps: 30
  default_crf: 23

paths:
  pipeline_dir: pipeline
  library_dir: library
  styles_dir: styles
  skills_dir: skills
  output_dir: output
```

所有配置均通过 `lib/config_model.py` 中的 Pydantic 模型验证。

### 环境变量（.env）

| 变量 | 使用方 | 用途 |
|------|--------|------|
| `ELEVENLABS_API_KEY` | elevenlabs_tts, music_gen | TTS、音乐、音效 |
| `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` | azure_stt, azure_tts | Azure AI Speech 云端转录与神经网络 TTS（一个资源，双向使用） |
| `OPENAI_API_KEY` | openai_tts, openai_image | TTS 回退方案、GPT Image 2 |
| `XAI_API_KEY` | grok_image, grok_video | Grok 图像编辑/生成、Grok 视频生成 |
| `FAL_KEY` | flux_image, kling_video, veo_video, minimax_video, recraft_image | fal.ai 托管模型（FLUX、Veo、Kling、MiniMax、Recraft） |
| `KLING_API_KEY` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | Kling 官方直连 API，用于视频、图像、TTS、Avatar 和口型同步 |
| `KLING_API_BASE_URL` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | 可选的 Kling 官方 API 端点覆盖值 |
| `HEYGEN_API_KEY` | heygen_video | 多 Provider 视频生成 |
| `PEXELS_API_KEY` | pexels_image, pexels_video | 素材库媒体 |
| `PIXABAY_API_KEY` | pixabay_image, pixabay_video | 素材库媒体 |
| `GOOGLE_API_KEY` | google_imagen, google_tts | Google Imagen 图像、Google Cloud TTS |
| `RUNWAY_API_KEY` | runway_video | Runway Gen-3/Gen-4 直连 |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | higgsfield_video | Higgsfield 多模型视频 |
| `MODAL_LTX2_ENDPOINT_URL` | ltx_video_modal | 自托管 LTX-2 |
| `VIDEO_GEN_LOCAL_ENABLED` | 本地视频工具 | 启用本地 GPU 生成 |
| `VIDEO_GEN_LOCAL_MODEL` | wan, hunyuan, ltx, cogvideo | 选择本地模型 |

Kling Official 支持保持在现有的 Provider 和能力模型之内。`kling_official_video` 与 `kling_official_image` 负责处理 Classic、Turbo 和 Omni 请求形态；Elements 与 Account Usage 则作为 `tools/_kling/` 下的内部辅助模块，分别用于 element ID 引用和低频账户诊断。它们不是独立的流水线阶段、Selector 或生成资产能力。

Kling Official 也只会在 OpenMontage 已有匹配能力槽位时添加 Provider 工具：`kling_tts` 对应 `tts`，`kling_avatar` 和 `kling_lip_sync` 对应 `avatar`。Kling 官方音效与视频特效目前未注册为工具，因为现有流水线尚未定义稳定的 `sound_effects` 或 `video_effects` 能力路由。

---

## 视觉风格系统

`styles/` 中的风格 Playbook 为流水线定义视觉语言：

- `clean-professional.yaml`——企业级精致视觉风格
- `flat-motion-graphics.yaml`——现代扁平化设计
- `minimalist-diagram.yaml`——技术型极简图表

这些 Playbook 由 `styles/playbook_loader.py` 加载。每条流水线都会在其清单中声明 `compatible_playbooks`，并根据 `schemas/styles/playbook.schema.json` 进行验证。

---

## 媒体配置

`lib/media_profiles.py` 中包含针对各平台的渲染配置：

| Profile | 分辨率 | 宽高比 | 说明 |
|---------|--------|--------|------|
| `youtube_landscape` | 1920x1080 | 16:9 | 标准 YouTube |
| `youtube_4k` | 3840x2160 | 16:9 | 4K YouTube |
| `youtube_shorts` | 1080x1920 | 9:16 | 最长 60 秒 |
| `instagram_reels` | 1080x1920 | 9:16 | 最长 90 秒 |
| `instagram_feed` | 1080x1080 | 1:1 | 正方形 |
| `tiktok` | 1080x1920 | 9:16 | 竖屏 |
| `linkedin` | 1920x1080 | 16:9 | 横屏 |
| `cinematic` | 2560x1080 | 21:9 | 超宽屏 |

每个 Profile 都会指定编解码器、音频编解码器、CRF、像素格式、最大文件大小、最长时长和字幕格式。`ffmpeg_output_args(profile)` 会生成相应的 FFmpeg 参数。

---

## 合成运行时

OpenMontage 具有一个多运行时合成层。`video_compose` 背后包含三个引擎；它们在 proposal 阶段被选定，并锁定在 `edit_decisions.render_runtime` 中：

### Remotion（基于 React）

这是 `remotion-composer/` 中一个独立的 Node.js/React 子项目，使用 [Remotion](https://www.remotion.dev/)。

- **React 18** + **Remotion 4.0** + **TypeScript 5.3**
- 处理现有场景组件栈（`text_card`、`stat_card`、图表、字幕、`TalkingHead`、`CinematicRenderer`）
- 脚本：`start`（Studio）、`build`（渲染）、`upgrade`

### HyperFrames（HTML/CSS/GSAP）

通过 `npx hyperframes` 使用，无需检出 monorepo。运行时最低要求为 Node.js ≥ 22、FFmpeg 和 `npx`。

- 处理动态排版、产品宣传片、发布短片、网站转视频、Registry Block，以及 SVG/GSAP 角色 Rig
- 驱动器：`tools/video/hyperframes_compose.py` 在 `projects/<name>/hyperframes/` 下构建工作区，然后依次运行 `lint → validate → render`
- 第 3 层 Skill 位于 `.agents/skills/hyperframes*/`；第 2 层指南位于 `skills/core/hyperframes.md`
- `character-animation` 流水线使用 HyperFrames 作为生产渲染包。浏览器预览仅用于 QA/调试，不是正式渲染路径。

### FFmpeg（回退方案/简单剪辑）

- 在不需要合成时处理纯拼接/裁剪
- 也用于在后处理阶段烧录字幕

`video_compose` 读取 `edit_decisions.render_runtime`，并通过 `_render_via_hyperframes`、`_remotion_render` 或 `_render_via_ffmpeg` 进行分派。禁止静默切换运行时——当选定的运行时不可用时，工具会返回结构化阻断信息。完整决策矩阵请参阅 `AGENT_GUIDE.md` 中的“Composition Runtimes (Inside video_compose)”以及 `skills/core/hyperframes.md`。

---

## 测试架构

```
tests/
├── contracts/              # 第 0-3 阶段：工具契约验证、Schema 检查、注册表测试
├── qa/                     # 集成测试：TTS、图像生成、音乐、混音、视频合成/拼接、E2E
├── eval/                   # 用于回归测试的黄金场景重放工具链
├── pipelines/              # 流水线级测试
├── tools/                  # 单个工具测试
└── styles/                 # 风格 Playbook 测试
```

**契约测试**会验证每个工具是否满足 `BaseTool` 契约：身份字段、Schema、依赖声明和继承关系。

**QA 测试**调用真实工具（使用真实 API/二进制文件）并检查输出质量。

**评估工具链**（`tests/eval/replay_harness/`）会使用基于容差的比较方式重放黄金场景，以适应随机输出。

---

## 系统依赖

**必需：**

- Python >= 3.10
- FFmpeg（约 15 个工具使用）

**可选（扩展能力）：**

- Node.js（用于 Remotion Composer）
- GPU + CUDA（用于本地视频/图像生成）
- Piper（离线 TTS）
- ManimCE（数学动画）
- Mermaid CLI（图表生成）

**Python 包：** pyyaml、pydantic、jsonschema、python-dotenv（核心）；pytest、pytest-asyncio（开发）；torch、torchvision、torchaudio（GPU）

---

## 关键设计决策

1. **没有运行时编排器**——LLM Agent 读取 YAML 和 Markdown 并驱动所有流程。这使系统易于调试（只需阅读 Skill），且与模型无关。

2. **基于检查点的恢复**——任意阶段都可能失败，流水线会从最后一个检查点继续，无需重新运行已经完成的阶段。

3. **经过 Schema 验证的工件**——每个阶段的输出都会在写入检查点前根据 JSON Schema 验证，以防无效内容向后续阶段传播。

4. **将预算作为一等概念**——执行前进行成本估算、预算预留和实际费用核销，Agent 不能静默超支。

5. **以 Selector 模式取代硬编码 Provider**——系统能力可以优雅降级。缺少 API Key 时，Selector 会继续尝试下一个 Provider 或本地替代方案。

6. **以 Skill 而非代码承载智能**——创意决策、质量检查清单、审查标准和提示词模板都存在于 Markdown Skill 中，而不是 Python 代码中。因此，只需编辑文本文件即可调整 Agent 行为，无须修改代码。
