# OpenMontage 技能索引

> 简体中文（主文档） | [英文副本](INDEX.en.md)
>
> Agent 的完整接入与运行规范见项目根目录的 [`AGENT_GUIDE.md`](../AGENT_GUIDE.md)；面向中文开发者的非规范性伴随说明见 [`AGENT_GUIDE.zh-CN.md`](../AGENT_GUIDE.zh-CN.md)。

本索引汇总 OpenMontage 的 Layer 2 项目技能，并说明三层知识架构。技能名、文件路径、pipeline ID、stage、工具名和 provider 名均保留规范值；中文只用于解释其用途。

## 三层知识架构

```text
Layer 1: tools/tool_registry.py          “有哪些工具、具备什么能力”
         tools/base_tool.py               每个工具声明 capability、tier、status、
                                          dependencies、cost 和 agent_skills[]

         → agent_skills[] 指向 →

Layer 2: skills/                          “OpenMontage 如何使用这些工具”
         项目专属约定：                     流水线集成、产物映射、增强链顺序、
         {core,creative,meta,pipelines}/   质量检查表

         → 引用底层技术知识 →

Layer 3: .agents/skills/                  “技术本身如何使用”
         通用 API 与工程知识：              正确导入路径、代码模式、约束和参数；
         当前安装 89 个技能包              与具体项目无关
```

Agent 的读取顺序：

1. 编排器查询 Layer 1 的 `tool_registry.support_envelope()`，确认能力及可用状态。
2. 工具的 `agent_skills[]` 指明它依赖的 Layer 3 技能。
3. Layer 2 规定工具在 OpenMontage 流水线中的使用方式。
4. Layer 3 按需提供供应商和技术栈的具体用法。

## 能力族与工具发现

每个工具声明 `capability`（能做什么）和 `provider`（由谁提供）。注册表按能力聚合工具，让 Agent 能看到完整选项。

### Selector / Provider 模式

- **Selector 工具**：`tts_selector`、`video_selector`、`image_selector` 会根据需求、凭据可用性和成本，在注册表中自动发现并选择 provider。用户没有指定 provider 时优先使用 selector。
- **Provider 工具**：直接调用指定 provider。仅在用户明确选择或 selector 路由不合适时使用。

不要在文档中维护固定工具清单。注册表是唯一事实来源，运行时请查询：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

| Capability | Selector | 发现方式 |
|---|---|---|
| `tts` | `tts_selector` | 自动发现全部 `capability="tts"` 工具 |
| `video_generation` | `video_selector` | 自动发现全部 `capability="video_generation"` 工具 |
| `image_generation` | `image_selector` | 自动发现全部 `capability="image_generation"` 工具 |
| `audio_processing` | — | 本地 FFmpeg 工具 |
| `enhancement` | — | 多 provider 增强工具 |
| `analysis` | — | 多 provider 分析工具 |
| `character_animation` | — | 本地角色规范、SVG 绑定、姿势库、动作时间线、预览和 QA |
| `3d_world_generation` | — | 语义地形、程序化散布、地标、诊断和 HyperFrames/Three.js 飞行工作区 |
| `3d_asset_acquisition` | — | 权利清晰的本地 GLTF/GLB 目录和来源记录 |
| `3d_asset_generation` | — | Atlas/fal 纹理网格生成与重建 |
| `3d_world_rendering` | — | Blender 场景组装与制作级渲染 |
| `graphics` | — | 本地图形渲染工具 |
| `music_library` | — | 发现用户提供的本地音乐 |
| `music_search` | — | 发现免版税音乐搜索/下载 provider |
| `music_generation` | — | 发现付费或本地音乐生成 provider |
| `subtitle` | — | 纯 Python 实现 |
| `avatar` | — | 本地 GPU 模型 |
| `video_post` | — | 基于 FFmpeg 的后期工具 |

### 添加新工具

1. 把工具放到正确的 `tools/` 能力目录。
2. 在类定义中设置 `capability` 和 `provider`。
3. 若加入多 provider 能力族，现有 selector 会自动发现它。
4. 通过 `agent_skills[]` 关联相应 Layer 2 和 Layer 3 技能。
5. 注册表会自动发现工具，无需手动注册。
6. selector、manifest 和指令均从注册表派生，不需要同步维护固定列表。

## 核心技能

| 技能 | 文件 | 适用场景 | Agent Skills（Layer 3） |
|---|---|---|---|
| FFmpeg | `core/ffmpeg.md` | 视频编码、滤镜与合成 | `ffmpeg`, `video-toolkit` |
| Remotion | `core/remotion.md` | 基于 React 的合成，Phase 3+ | `remotion-best-practices`, `remotion` |
| HyperFrames | `core/hyperframes.md` | HTML/CSS/GSAP 合成；动态排版、音乐视频、产品宣传和网站捕获。内置 v0.7.17（2026-06-27） | `hyperframes`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-media`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `motion-graphics`, `music-to-video`, `website-to-video`, `remotion-to-hyperframes`, `gsap-core`, `gsap-timeline` |
| WhisperX | `core/whisperx.md` | 带词级时间戳的转录；默认离线 STT | `speech-to-text` |
| Azure STT | 工具 `azure_stt` | 可选云端 STT；配置 `AZURE_SPEECH_KEY` 时优先 | `azure-speech-to-text` |
| Azure TTS | 工具 `azure_tts` | 可选云端神经语音与 SSML；与 `azure_stt` 共用密钥 | `azure-text-to-speech` |
| Subtitle Sync | `core/subtitle-sync.md` | 字幕计时和对齐 | `remotion-best-practices` |
| Color Grading | `core/color-grading.md` | FFmpeg 色彩配置、LUT 和无障碍 | `ffmpeg` |

## 创作技能

| 技能 | 文件 | 适用场景 | Agent Skills（Layer 3） |
|---|---|---|---|
| Video Editing | `creative/video-editing.md` | 剪辑决策、节奏和韵律 | `ffmpeg`, `video-toolkit` |
| Enhancement Strategy | `creative/enhancement-strategy.md` | 叠加元素的位置和密度 | `ffmpeg` |
| Data Visualization | `creative/data-visualization.md` | 图表类型、动画和标签布局 | `d3-viz`, `remotion-best-practices` |
| Video Stitching | `creative/video-stitching.md` | 多片段组装、AI 片段串联和空间合成 | `ffmpeg`, `video-toolkit` |
| Video Gen Prompting | `creative/video-gen-prompting.md` | 通用视频生成词汇；规范五要素 Subject / Motion / Scene / Spatial / Camera | `ai-video-gen`, `ltx2`, `create-video` |
| ↳ Seedance Prompting | `creative/prompting/seedance-prompting.md` | 首选高质量方案；Seedance 2.0 八部分结构、多镜头、口型同步、参考图转视频 | `seedance-2-0`, `ai-video-gen` |
| ↳ Grok Prompting | `creative/prompting/grok-prompting.md` | Grok 图像/视频提示、编辑和参考图视频 | `grok-media` |
| ↳ Sora Prompting | `creative/prompting/sora-prompting.md` | Sora 2 结构化模板和高级字段 | `ai-video-gen` |
| ↳ VEO Prompting | `creative/prompting/veo-prompting.md` | VEO 3.1 十四部分结构和艺术流派 | `ai-video-gen` |
| ↳ LTX Prompting | `creative/prompting/ltx-prompting.md` | LTX-2 六元素结构和音频提示 | `ltx2` |
| ↳ HunyuanVideo Prompting | `creative/prompting/hunyuan-prompting.md` | HunyuanVideo 公式与 I2V 实践 | — |
| Storytelling | `creative/storytelling.md` | 叙事结构、钩子、节奏和 Mayer 原则 | — |
| Sound Design | `creative/sound-design.md` | 音频闪避、LUFS、音效计时和 TTS 混音 | `elevenlabs` |
| Typography | `creative/typography.md` | 字体、字号、安全区和字幕样式 | — |
| ManimCE Usage | `creative/manim-usage.md` | 场景编排、动画计时和色彩 | `manimce-best-practices` |
| Image Gen Usage | `creative/image-gen-usage.md` | 提示一致性、主参考图和批量策略 | `flux-best-practices`, `bfl-api` |
| Image Provider Usage | `creative/image-provider-usage.md` | FLUX/Grok/OpenAI/Recraft/stock 的成本质量取舍 | `flux-best-practices`, `bfl-api`, `grok-media` |
| 3D World Generation | `creative/3d-world-generation.md` | 语义世界规划、素材获取/生成、Blender 组装和保真审查 | `3d-asset-generation`, `threejs-world-generation` |
| B-Roll Planning | `creative/broll-planning.md` | 库存素材与生成素材决策、检索和评估 | — |
| Stock Sourcing Usage | `creative/stock-sourcing-usage.md` | Pexels/Pixabay 参数、许可和集成 | — |
| Scene Detect Usage | `creative/scene-detect-usage.md` | 阈值、算法和内容预设 | — |
| Diagram Gen Usage | `creative/diagram-gen-usage.md` | 复杂度、渐进构建和主题 | `beautiful-mermaid` |
| Music Gen Usage | `creative/music-gen-usage.md` | BPM、提示工程和时长匹配 | `music`, `elevenlabs` |
| Background Removal | `creative/bg-remove-usage.md` | 模型选择、Alpha 抠图和合成 | — |
| Upscaling | `creative/upscale-usage.md` | 放大倍率、模型和人脸感知放大 | — |
| Face Restoration | `creative/face-restore-usage.md` | CodeFormer/GFPGAN 与保真度调节 | — |
| Lip Sync | `creative/lip-sync-usage.md` | Wav2Lip、配音工作流和输入要求 | `faceswap` |
| Talking Head Gen | `creative/talking-head-gen-usage.md` | SadTalker/MuseTalk、照片转视频和表情调节 | `avatar-video` |
| Video Understanding | `creative/video-understand-usage.md` | 视觉 QA、质量门槛和场景分类 | `video-understand` |

## 流水线类型技能

| 技能 | 文件 | 适用场景 |
|---|---|---|
| Short-Form | `creative/short-form.md` | TikTok、Reels、Shorts；9:16、60 秒以内 |
| Long-Form | `creative/long-form.md` | YouTube 10 分钟以上；章节、留存和片尾 |
| Screen Recording | `creative/screen-recording.md` | 代码讲解、教程和软件演示 |
| Animation Pipeline | `creative/animation-pipeline.md` | 动效、缓动、转场和合成 |
| 3D World Generation | `creative/3d-world-generation.md` | 连续 Three.js 地形、语义区域、分层制作、授权 GLTF/PBR 素材和确定性镜头 |
| Character Animation Pipeline | `pipelines/character-animation/` | 本地绑定角色、姿势库、动作时间线和 SVG/Canvas/Remotion/HyperFrames 渲染 |
| Cinematic | `creative/cinematic.md` | 宽银幕、电影节奏、分层音频和调色 |

## 流水线阶段导演技能

阶段导演技能规定每个 stage 的执行方法、质量标准和自检规则。下表中的 stage 名均为机器值，不翻译。

| Pipeline | 总控技能 | Stage → director skill |
|---|---|---|
| Animated Explainer `pipelines/explainer/` | `executive-producer.md` | `research` → `research-director.md`; `proposal` → `proposal-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Talking Head `pipelines/talking-head/` | — | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Screen Demo `pipelines/screen-demo/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Clip Factory `pipelines/clip-factory/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Podcast Repurpose `pipelines/podcast-repurpose/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Cinematic `pipelines/cinematic/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Animation `pipelines/animation/` | `executive-producer.md` | `research` → `research-director.md`; `proposal` → `proposal-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Hybrid `pipelines/hybrid/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Avatar Spokesperson `pipelines/avatar-spokesperson/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |
| Localization Dub `pipelines/localization-dub/` | `executive-producer.md` | `idea` → `idea-director.md`; `script` → `script-director.md`; `scene_plan` → `scene-director.md`; `assets` → `asset-director.md`; `edit` → `edit-director.md`; `compose` → `compose-director.md`; `publish` → `publish-director.md` |

`explainer` 和 `animation` 的旧 `idea-director.md` 仅供参考，v2.0 已由 `research` + `proposal` 两阶段取代。`talking-head` 仍使用自己的 `idea-director.md`。

## 元技能

| 技能 | 文件 | 用途 |
|---|---|---|
| User Language | `meta/user-language.md` | 汉化用户界面，同时保持 provider prompt、来源忠实度和机器契约 |
| Onboarding | `meta/onboarding.md` | 首次问候、能力发现和起步提示 |
| Reviewer | `meta/reviewer.md` | 每阶段后的自检协议 |
| Checkpoint Protocol | `meta/checkpoint-protocol.md` | 检查点和人工审批规则 |
| Skill Creator | `meta/skill-creator.md` | 流水线运行期间动态创建技能 |
| Animation Runtime Selector | `meta/animation-runtime-selector.md` | 按场景选择合成引擎和动画库 |
| Taste Direction | `meta/taste-direction.md` | 将 brief 转换为审美参数、反例和参考策略 |
| Bespoke Composition (Atelier) | `meta/bespoke-composition.md` | 从零手工制作高价值合成作品，并路由艺术指导、动效原则和引擎机制 |

## 风格 Playbook

`styles/*.yaml` 定义视觉语言、字体、运动、音频和素材生成约束，并由 `schemas/styles/playbook.schema.json` 校验。

| Playbook | Category | 氛围 | 适用场景 |
|---|---|---|---|
| `clean-professional` | `motion-graphics` | 精致、可信 | 企业、教育、SaaS |
| `premium-minimalist` | `minimalist` | 冷静、编辑感 | 投资人更新、专家讲解、产品叙事 |
| `flat-motion-graphics` | `motion-graphics` | 活跃、醒目 | 社交媒体、TikTok、初创公司 |
| `minimalist-diagram` | `whiteboard` | 聚焦、技术感 | 技术深潜、架构说明 |

加载示例：`load_playbook("clean-professional")`（来自 `styles/playbook_loader.py`）。

## 已安装 Agent Skills（Layer 3）

Layer 3 技能位于 `.agents/skills/`，由 `npx skills add` 管理；当前仓库包含 **89 个** `SKILL.md` 技能包。Claude Code 通过 `.claude/skills/` 中的符号链接访问它们。

| 类别 | 已安装技能 | 来源 |
|---|---|---|
| 视频合成 | `remotion-best-practices`, `remotion`, `hyperframes`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-media`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `motion-graphics`, `music-to-video`, `remotion-to-hyperframes`, `website-to-video` | `remotion-dev/skills`, `digitalsamba/claude-code-video-toolkit`, `heygen-com/hyperframes` |
| 视频处理 | `ffmpeg`, `video-toolkit` | `digitalsamba/claude-code-video-toolkit` |
| TTS 与音频 | `text-to-speech`, `speech-to-text`, `azure-speech-to-text`, `music`, `sound-effects`, `elevenlabs`, `fish-audio-tts`, `agents`, `setup-api-key` | `elevenlabs/skills`、视频工具包与本地技能 |
| 图像生成 | `flux-best-practices`, `bfl-api`, `grok-media` | `black-forest-labs/skills` 与本地技能 |
| 数学动画 | `manimce-best-practices`, `manimgl-best-practices`, `manim-composer` | `adithya-s-k/manim_skill` |
| 3D 图形 | `threejs-world-generation`, `threejs-animation`, `threejs-fundamentals`, `threejs-geometry`, `threejs-interaction`, `threejs-lighting`, `threejs-loaders`, `threejs-materials`, `threejs-postprocessing`, `threejs-shaders`, `threejs-textures` | 本地技能与 `cloudai-x/threejs-skills` |
| 图表 | `beautiful-mermaid`, `d3-viz` | `intellectronica/agent-skills`, `davila7/claude-code-templates` |
| 动画 | `framer-motion`, `lottie-bodymovin` | `pproenca/dot-skills`, `dylantarre/animation-principles` |
| 设计 | `tailwind-design-system`, `web-design-guidelines`, `vercel-react-best-practices`, `vercel-composition-patterns` | `wshobson/agents`, `vercel-labs/agent-skills` |
| AI 视频（HeyGen） | `heygen`, `avatar-video`, `create-video`, `faceswap`, `ai-video-gen`, `video-download`, `video-edit`, `video-translate`, `video-understand`, `visual-style` | `heygen-com/skills` |
| Kling Official | `kling-official`；覆盖官方认证、Classic/Turbo/Omni、Omni 多参考语法、Elements/Account Usage 内部辅助能力、callback、TTS 参数、avatar/lip-sync face selection、错误处理和成本治理；对应 `kling_official_video`、`kling_official_image`、`kling_tts`、`kling_avatar`、`kling_lip_sync` | 本地技能 |
| 高质量 AI 视频 | `seedance-2-0`；首选高质量默认方案，可通过 `seedance_video`（fal.ai）或 `heygen_video` Avatar Shots 使用 | 本地技能 |
| 基础设施 | `acestep`, `ltx2`, `playwright-recording` | `digitalsamba/claude-code-video-toolkit` |
