> **简体中文主报告** | [英文副本](EXTERNAL_DEPENDENCIES_AUDIT.en.md)

# OpenMontage 外部依赖审计报告

## 报告信息

| 项目 | 内容 |
|---|---|
| 审计日期 | 2026-08-18 |
| 审计分支 | `agent/zh-cn-localization` |
| 基准提交 | `2a09cf3d29833092f9286e0fb5ec2f7cf6603522` |
| 审计范围 | API、模型、外部程序、Python/Node 依赖、网络、存储、硬件、许可证、数据边界和本机可用性 |
| 事实来源 | 工具注册表、依赖清单、运行时源代码、环境变量契约、Provider 文档和本机探测 |
| 报告性质 | 当前代码与当前机器的只读审计快照；供应商状态、价格和模型标识符可能随时间变化 |

## 一、执行摘要

OpenMontage 采用“**本地编排核心 + 可插拔供应商能力**”架构。项目不是必须同时配置所有云端服务的 SaaS 系统，也不应把注册表中的全部 Provider 误解为全局强制依赖。

系统真正的基础依赖是：

1. 一款能够读取文件并执行命令的 AI 编程助手；
2. Python 3.10 或更高版本；
3. FFmpeg 与 ffprobe；
4. 可写的本地文件系统和足够的工作磁盘；
5. 需要 Remotion 或 HyperFrames 完整合成能力时，再增加 Node.js、npm 和 npx。

项目自身不强制依赖数据库、Redis、消息队列、对象存储、Docker、Kubernetes 或公网入站服务。项目以本地文件为事实来源；AI 编程助手本身是控制平面，Python 只提供工具与持久化能力。通用 LLM API 由宿主编程助手决定，OpenMontage 运行时不会因为 `config.yaml` 中存在 `llm` 配置而自行发起通用 LLM 调用。

云端图像、视频、TTS、音乐、Avatar 和 3D 服务均属于可选能力边界。缺少某个 Provider 应降低相应能力覆盖，而不应破坏本地项目状态、Schema、检查点、Backlot、FFmpeg 后期或其他已配置能力。

## 二、依赖分层

### 2.1 基础控制层

| 依赖 | 强制性 | 作用 |
|---|---:|---|
| AI 编程助手 | 必需 | 读取流水线和 Skill，选择工具，执行审查、审批和检查点协议 |
| Python 3.10+ | 必需 | 工具注册表、Schema、检查点、Provider 适配器和 Backlot |
| FFmpeg + ffprobe | 核心必需 | 编码、拼接、裁剪、字幕、音频、探测和 QA |
| 本地文件系统 | 必需 | 保存项目、产物、素材、缓存、检查点和最终渲染 |
| Git | 安装与协作需要 | 克隆、版本管理和贡献流程；不是视频运行时依赖 |
| `make` / `uv` | 可选辅助 | 自动创建虚拟环境、安装依赖、运行测试和预检 |

OpenMontage 没有常驻 Python 编排器。LLM Agent 读取 `pipeline_defs/`、`skills/` 和工具注册表后驱动执行。`config.yaml` 中的 `llm.provider` 当前属于配置模型的一部分，不等于仓库已经实现 Anthropic、OpenRouter、Ollama 等通用 LLM 客户端。

### 2.2 合成与展示层

| 组件 | 运行条件 | 说明 |
|---|---|---|
| FFmpeg | `ffmpeg`、`ffprobe` | 本地且可离线；承担基础合成、后期和 QA |
| Remotion | Node.js、npm、`remotion-composer/node_modules` | React/TypeScript 程序化视频合成 |
| HyperFrames | Node.js >= 22、npm/npx、FFmpeg、可执行的 `hyperframes` CLI | HTML/CSS/GSAP、Three.js、动态排版和角色动画 |
| Backlot | FastAPI、uvicorn、watchfiles、现代浏览器 | 只读本地看板；默认监听 `127.0.0.1:4750` |

Node.js 不是 Python + FFmpeg 核心的硬依赖，但它是默认高质量合成路径的重要组成部分。README 的 Node.js 18+ 适用于 Remotion 基线；完整覆盖 HyperFrames 时，应把统一最低版本理解为 Node.js 22+。

### 2.3 可插拔能力层

以下能力均按需配置：

- 云端图像、视频、TTS、音乐、Avatar 和 3D API；
- 本地 PyTorch、Diffusers、Transformers 和 ComfyUI 模型；
- 素材站点和开放档案源；
- Blender、Manim、Piper、Wav2Lip、SadTalker、Real-ESRGAN、GFPGAN、rembg 等专业工具；
- 网络研究、模型下载、网页抓取、屏幕录制和浏览器自动化。

## 三、Python 与 Node 软件依赖

### 3.1 Python 核心依赖

`requirements.txt` 声明：

- `pyyaml>=6.0`
- `pydantic>=2.0`
- `jsonschema>=4.20`
- `python-dotenv>=1.0`
- `Pillow>=10.0`
- `numpy>=1.24`
- `requests>=2.31`
- `google-auth>=2.0`
- `google-genai>=1.0.0`
- `openai>=2.44.0`
- `fastapi>=0.110`
- `uvicorn>=0.29`
- `watchfiles>=0.21`

开发与测试依赖为 `pytest`、`pytest-asyncio` 和 `httpx2`。GPU 基础依赖为 `torch`、`torchvision`、`torchaudio`，`make install-gpu` 还会安装 `diffusers`、`transformers` 和 `accelerate`。

### 3.2 按工具安装的 Python 扩展

| 能力 | 额外依赖 |
|---|---|
| 本地转录 | `faster-whisper`、可选 `whisperx` |
| 视频下载与字幕 | Python `yt-dlp`、`youtube-transcript-api` |
| 视频理解与 CLIP 检索 | `transformers`、`torch` |
| 抠图 | `rembg`、可选 `onnxruntime-gpu` |
| 超分与人脸修复 | `realesrgan`、`gfpgan`、`torch` |
| 人脸跟踪与自动构图 | `mediapipe`、`opencv-python` |
| 素材语料库 | `opencv-python`、`transformers`、`torch` |
| 无正式 API 的素材站点 | `beautifulsoup4` |
| ComfyUI 实时进度 | 可选 `websocket-client`；缺失时退回 REST 轮询 |
| 离线 TTS | `piper-tts` |
| 数学动画 | `manim`，并可能需要 LaTeX |
| 代码高亮 | `Pygments` |
| 音频辅助 | `pydub` |

### 3.3 Remotion Node 依赖

`remotion-composer/package.json` 声明 React 18、React DOM 18、Remotion 4、TypeScript 5.3，以及 `@remotion/cli`、`@remotion/captions`、`@remotion/google-fonts`、`@remotion/media`、`@remotion/player`、`@remotion/transitions`、D3 Geo、TopoJSON 和 World Atlas。

Remotion 渲染还间接依赖 Chromium/Chrome Headless Shell。使用 Google Fonts 组件时，具体字体加载路径也可能引入外部网络访问。

### 3.4 HyperFrames 运行时

HyperFrames 通过 `npx hyperframes` 动态获取，而不是作为仓库内固定版本安装。它依赖：

- Node.js >= 22；
- npm 与 npx；
- FFmpeg；
- npm Registry；
- 浏览器型校验和渲染环境。

当前项目没有锁定 HyperFrames 的确切版本，因此首次运行、离线运行和供应链可复现性取决于 npm 缓存与上游发布状态。

## 四、云端 API 与凭据

所有密钥应保存在 `.env` 或进程环境变量中，不应写入产物、日志或 Git 历史。

| Provider | 主要环境变量 | 能力 |
|---|---|---|
| fal.ai | `FAL_KEY` / `FAL_AI_API_KEY` | FLUX、Recraft、Seedream、Kling、Veo、Seedance、MiniMax、Gemini Omni、3D、ElevenLabs TTS/音乐 |
| Atlas Cloud | `ATLASCLOUD_API_KEY`；兼容 `ATLAS_CLOUD_API_KEY`、`ATLAS_API_KEY` | 图像、视频和 Tripo 3D 多模型网关 |
| Google | `GOOGLE_API_KEY` / `GEMINI_API_KEY` | Imagen、Veo、Gemini Omni、Lyria、Cloud TTS |
| Google Vertex | `GOOGLE_APPLICATION_CREDENTIALS`、project、location | 服务账号方式访问 Google 生成服务 |
| OpenAI | `OPENAI_API_KEY` | GPT Image 2、OpenAI TTS、Sora 2 |
| xAI | `XAI_API_KEY` | Grok Imagine 图像和视频 |
| Kling Official | `KLING_API_KEY`、可选 `KLING_API_BASE_URL` | 图像、视频、TTS、Avatar、Lip Sync |
| Volcengine Ark | `ARK_API_KEY` | Seedance 2.0/2.5 官方直连 |
| Volcengine Jimeng | `VOLC_ACCESSKEY` + `VOLC_SECRETKEY` | 即梦视频 |
| MiniMax | `MINIMAX_API_KEY` | MiniMax 图像、H3/Hailuo 视频 |
| Tencent TokenHub | `TENCENT_TOKENHUB_API_KEY` | Hunyuan 图像和视频 |
| DashScope | `DASHSCOPE_API_KEY` | Qwen 图像、TTS 和 ASR |
| Azure AI Speech | `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` | 云端 STT 和神经 TTS |
| ElevenLabs | `ELEVENLABS_API_KEY` | TTS、音乐、音效和声音克隆 |
| fish.audio | `FISH_AUDIO_API_KEY` | 表现型 TTS 和声音克隆 |
| Doubao Speech | `DOUBAO_SPEECH_API_KEY` | 普通话 TTS |
| Runway | `RUNWAY_API_KEY` / `RUNWAYML_API_SECRET` | Runway 及多模型视频路由 |
| HeyGen | `HEYGEN_API_KEY` | Veo、Sora、Kling、Runway、Seedance 等视频路由 |
| Higgsfield | key + secret 或 `HIGGSFIELD_KEY` | 多模型视频和角色一致性 |
| Replicate | `REPLICATE_API_TOKEN` | Seedance 托管推理 |
| SunoAPI | `SUNO_API_KEY` | Suno 风格歌曲和伴奏生成 |
| Modal | `MODAL_LTX2_ENDPOINT_URL` | 用户自托管的 LTX-2 云 GPU 端点 |
| ComfyUI | `COMFYUI_*_SERVER_URL` | 本地或局域网 GPU 服务；Partner Nodes 另需账号、网络和点数 |

Provider 工具通常采用异步提交、状态轮询和结果下载。输出 URL 可能在数小时或数天内失效，因此工具必须及时把结果保存到项目目录。

## 五、模型依赖

### 5.1 图像模型

- FLUX Pro 1.1、FLUX Dev、FLUX Pro；
- Recraft v4、v4-pro；
- ByteDance Seedream v5；
- OpenAI `gpt-image-2`；
- Google Imagen 4、Fast、Ultra，以及 Gemini 2.5 Flash Image；
- Google Nano Banana 2，经 Atlas Cloud 路由；
- xAI `grok-imagine-image`；
- MiniMax `image-01`、`image-01-live`；
- DashScope `qwen-image-2.0-pro`、`qwen-image-max`、`wan2.7-image`、`z-image-turbo`；
- Tencent `hy-image-v3.0`；
- Kling v1 至 v3、`kling-image-o1`、`kling-v3-omni`；
- Stable Diffusion 2.1 Base；
- ComfyUI FLUX.2 Dev NVFP4。

### 5.2 视频模型

- Seedance 2.0、2.0 Fast、2.0 Mini、2.5；
- Google Veo 2、Veo 3、Veo 3.1 及 Fast 变体；
- Gemini Omni Flash；
- OpenAI Sora 2、Sora 2 Pro；
- xAI Grok Imagine Video；
- Kling v1 至 v3、Turbo、Master、Video O1、Omni；
- MiniMax H3、Hailuo 2.3、Hailuo 02 和 Director 系列；
- Tencent `hy-video-1.5`、`yt-video-2.0`；
- Runway Gen-4 Turbo、Gen-4.5；
- Higgsfield Soul Cinema 及 Seedance/Kling/Veo/Sora/WAN 路由；
- 即梦 3.0 Pro；
- 本地 Wan 2.1 1.3B/14B、HunyuanVideo 1.5、CogVideoX 2B/5B、LTX-2；
- ComfyUI WAN 2.2、MiniMax H3 和托管 Partner Nodes。

### 5.3 语音、音乐和分析模型

- OpenAI `gpt-4o-mini-tts`；
- ElevenLabs Multilingual v2、Eleven v3；
- fish.audio s1、s2-pro、s2.1-pro；
- DashScope Qwen3 TTS；
- Google Cloud TTS/Chirp、Azure Neural Voice、Kling 官方 voice ID、Piper 本地音色；
- Google Lyria 3 Pro Preview、Suno V4/V4.5/V5、ElevenLabs Music、ACE-Step 1.3 3.5B；
- faster-whisper tiny 至 large-v3、DashScope Qwen3 ASR、Azure Fast Transcription；
- CLIP ViT-B/32、BLIP-2 OPT 2.7B、LLaVA 1.5 7B。

### 5.4 增强、Avatar 与 3D 模型

- U2Net、ISNet：背景移除；
- Real-ESRGAN、RealESRNet：超分；
- CodeFormer、GFPGAN：人脸修复；
- MediaPipe：人脸和眼部跟踪；
- SadTalker、MuseTalk、Wav2Lip：Avatar 与口型同步；
- Hunyuan 3D 3.1、SAM 3、Tripo H3.1：3D 生成；
- Blender、Three.js：程序化世界和渲染，不属于生成式模型。

## 六、素材、许可证与外部内容

### 6.1 素材来源

需要密钥的主要来源包括 Pexels、Pixabay、Unsplash、Freesound 和 Videvo。

无密钥或密钥可选的来源包括 Archive.org、Wikimedia Commons、NASA、NARA、Library of Congress、Coverr、Pond5 Public Domain、Mixkit、ESA、NOAA、Dareful、JAXA 和 Pixabay Music 页面检索。

其中 Mixkit、ESA、NOAA、Dareful 和 JAXA 依赖网页结构与 `beautifulsoup4`，比正式 API 更容易因站点改版失效。

### 6.2 许可证边界

- Pexels、Pixabay、Coverr、Mixkit 通常不要求署名；
- Dareful、ESA、部分 Videvo、Wikimedia 内容需要署名或逐文件核验；
- NASA 内容通常可用，但仍受 NASA Media Usage Guidelines 和第三方标识例外约束；
- Archive.org、LOC、NARA、Pond5 应以单个素材记录中的许可证和来源字段为准；
- Freesound 必须检查单个声音的 Creative Commons 条款；
- 语音克隆、数字人、真人肖像和品牌素材还受授权、隐私和平台政策约束；
- 本地开放权重也有独立许可证，例如 Apache-2.0 或 LTX-2-Community，不能仅凭“可下载”推断可任意商用。

## 七、网络与数据边界

### 7.1 出站网络

涉及云端生成、网络研究、模型下载或素材获取时，需要：

- DNS 和出站 HTTPS 443；
- 访问供应商 API、结果 CDN、npm、PyPI、GitHub 和 Hugging Face；
- 支持长轮询、较大媒体上传/下载和足够长的代理超时；
- 对临时下载 URL、签名 URL 和供应商区域域名不过度拦截。

### 7.2 本地端口

- Backlot 默认使用 `127.0.0.1:4750`；
- ComfyUI 默认使用 `localhost:8188`；
- Remotion、HyperFrames 和浏览器预览可能临时启动本地服务。

### 7.3 公网入站与公网素材 URL

绝大多数 Provider 默认采用轮询，不需要开放公网入站端口。Kling 等支持 `callback_url`，但 OpenMontage 默认仍会轮询。

以下路径可能要求 Provider 可访问的公网媒体 URL：

- DashScope ASR 的音频输入；
- Seedance Ark 的某些参考视频；
- 即梦、腾讯和部分视频网关的参考素材；
- 某些不接受 Data URI 或本地路径的 Provider 操作。

因此，对象存储、临时签名 URL 或供应商上传接口只是在特定工作流中的中转依赖，不是 OpenMontage 全局基础设施。

### 7.4 数据外发

调用云端 Provider 时，可能外发：

- 提示词、脚本片段和负面提示词；
- 参考图像、视频、音频和声音样本；
- 项目元数据、模型参数和回调地址；
- 需要声音克隆时的 `reference_id` 或声音素材。

本地 FFmpeg、Piper、本地模型和本地 ComfyUI 工作流可减少数据外发，但首次安装与模型下载仍可能需要网络。项目不会因为启用某个 Provider 而自动上传整个项目目录。

## 八、硬件基础设施

### 8.1 CPU、内存和磁盘

- FFmpeg 合成通常需要 2 至 4 个 CPU 核心；
- Backlot 和普通 Python 工具资源消耗较低；
- 本地视频模型普遍需要 16 至 32GB 系统内存；
- 模型权重、缓存、源素材、图像序列和渲染临时文件可能占用数 GB 至数十 GB；
- 生产环境应为项目、模型缓存和临时渲染预留独立磁盘预算。

### 8.2 GPU 与显存

| 模型或工具 | 典型显存要求 |
|---|---:|
| CogVideoX 2B | 6GB |
| Wan 2.1 1.3B | 8GB |
| LTX-2 | 12GB |
| CogVideoX 5B | 12GB |
| HunyuanVideo 1.5 | 14GB |
| Wan 2.1 14B | 24GB |
| ComfyUI 低显存量化工作流 | 8 至 12GB |
| 内置 WAN 2.2 14B FP8 工作流 | 建议 16GB VRAM + 32GB RAM |

共享本地视频加载器优先选择 CUDA，其次是 Apple Silicon MPS，最后是 CPU。但并非所有工具都同等支持 MPS：`video_understand` 当前实现仍只显式选择 CUDA 或 CPU；Wav2Lip、SadTalker 等路径也更偏向 CUDA。ComfyUI 的实际要求由模型、量化、分辨率、帧数、自定义节点和工作流决定。

### 8.3 外围设备与系统权限

只有相应功能需要以下资源：

- 屏幕录制权限：`screen_recorder`、Cap；
- 麦克风和摄像头：录制、真人素材和数字人采集；
- Blender GPU 或显示环境：3D 渲染；
- Linux 无头环境中的 `DISPLAY`、Xvfb 或等价显示服务。

## 九、当前机器实测状态

### 9.1 系统环境

| 项目 | 实测结果 |
|---|---|
| 操作系统 | macOS 26.6.1，arm64 |
| CPU/GPU | Apple M4，10 核集成 GPU，Metal 4 |
| 内存 | 16GiB 统一内存 |
| 工作盘可用空间 | 约 845GiB |
| Python | 3.10.19 |
| Node.js | 24.13.0 |
| npm/npx | 11.6.2 |
| FFmpeg/ffprobe | 8.1.2 |
| 已安装辅助工具 | Git、uv、Docker、GitHub CLI、`yt-dlp` 命令 |
| 未安装工具 | Blender、ComfyUI、Ollama、Playwright、CUDA、ROCm |
| `.env` | 不存在 |

### 9.2 注册表状态

注册表共发现 117 个非 Selector 工具：

| 运行类型 | 当前状态 |
|---|---|
| 本地工具 | 33/43 可用 |
| 本地 GPU 工具 | 0/14 可用 |
| API 工具 | 1/55 可用 |
| 混合工具 | 2 可用、1 降级、2 不可用 |
| 总计 | 36 可用、80 不可用、1 降级 |

主要能力状态：

- FFmpeg Provider 工具 17/17 可用；
- 视频后期 8/9、分析 7/13、本地角色动画结构工具 6/6 可用；
- 屏幕采集 2/2 可用；
- 图像生成 0/16、视频生成 0/26、TTS 0/10、音乐生成 0/5、Avatar 0/4；
- 3D 世界作者工具可用，但生产渲染器不可用；
- 直接素材搜索有 7/16 个来源可用，主要是无需密钥的开放档案源。

API 型工具中当前唯一被判为可用的是无需密钥但依赖网络的 Pixabay Music 页面检索；这不表示任何云端生成账号已经配置。

### 9.3 当前合成与本地 AI 阻断

- FFmpeg 可用；
- Remotion 不可用，因为 `remotion-composer/node_modules` 尚未安装；
- HyperFrames 的 npm 包可解析到 `0.8.2`，但本机 npm 缓存包含 root 所有权文件，安装时触发 `EACCES`，CLI 当前不可执行；
- 虚拟环境没有 `torch`、`diffusers`、`transformers`、`faster-whisper`、Piper、MediaPipe、OpenCV、rembg、Real-ESRGAN、GFPGAN 等扩展；
- 系统存在 `yt-dlp` 命令，但虚拟环境缺少 Python `yt_dlp` 模块，因此注册表中的 `video_downloader` 仍不可用；
- 没有 `.env` 和云端密钥，因此云端图像、视频、TTS、音乐和 Avatar 均不可用；
- `corpus_builder` 处于降级状态，因为开放素材源存在，但 CLIP/视觉语料库相关依赖未安装。

## 十、依赖契约发现的问题

### 10.1 `.env.example` 覆盖不完整

当前示例没有把所有代码支持的变量作为可直接填写条目完整列出，主要包括：

- Atlas Cloud 主变量及别名；
- `FREESOUND_API_KEY`、`COVERR_API_KEY`、`NARA_API_KEY`、`POND5_API_KEY`、`VIDEVO_API_KEY`；
- `COMFYUI_IMAGE_SERVER_URL`、`COMFYUI_MUSIC_SERVER_URL`；
- 部分 Google、Runway、Higgsfield 别名与 Vertex 运行模式变量；
- `OPENMONTAGE_PROJECTS_DIR`、缓存目录和容量限制；
- `BACKLOT_PORT`、`BLENDER_PATH`、`MUSIC_LIBRARY_DIR`、`SADTALKER_PATH`、`WAV2LIP_PATH`；
- 一些端点、区域、模型和成本覆盖变量。

### 10.2 `setup.py` 与 `requirements.txt` 不等价

`setup.py` 没有包含 `numpy`、`google-auth`、FastAPI、uvicorn、watchfiles 等完整依赖。使用 `pip install .` 不能保证得到与 `make setup` 或 `pip install -r requirements.txt` 相同的运行环境。

### 10.3 Node.js 版本门槛不统一

README 使用 Node.js 18+，HyperFrames 契约要求 Node.js 22+。面向完整能力的安装文档和预检应统一报告 Node.js 22+，同时说明 Remotion 自身的较低基线。

### 10.4 版本锁定不足

- Python 依赖大多采用 `>=` 下限，没有 Python lockfile；
- HyperFrames 通过未锁版本的 `npx hyperframes` 获取；
- 云端模型 ID、费率、配额和端点属于外部可变状态；
- 首次安装与离线重建的可复现性不足。

### 10.5 依赖声明方式不统一

部分工具使用标准 `dependencies` 字段，另一部分在自定义 `get_status()` 中动态探测密钥、服务器、模型或安装状态。因此只扫描 `requirements.txt` 或 `BaseTool.dependencies` 会低估真实依赖，必须结合实时 `support_envelope()`、`provider_menu()` 和工具实现审计。

## 十一、建议实施顺序

1. 补齐 `.env.example` 与 Provider 文档之间的变量覆盖，并标明“必需、别名、可选覆盖、仅特定操作使用”。
2. 统一 `setup.py`、`requirements.txt` 与 `make setup` 的安装契约，或明确废弃不完整的安装入口。
3. 统一 Node.js 版本说明，并在预检中分别报告 Remotion 和 HyperFrames 门槛。
4. 为 Python 依赖引入 lockfile；为 HyperFrames 增加经过验证的版本策略和离线缓存说明。
5. 将环境变量、模型 ID、外部命令、Python 模块和本地服务探测纳入自动化依赖审计测试。
6. 为必须使用公网 URL 的操作提供统一的上传/签名 URL 说明，同时保持对象存储为可选边界。
7. 在 CI 中持续验证“无密钥本地核心”与“中英文能力等价”，防止文档本地化或供应商变更误伤工具路由。

## 十二、复核命令

以下命令用于复核当前机器上的依赖状态；它们不会调用付费生成接口：

```bash
make preflight

uv run python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), ensure_ascii=False, indent=2))"

uv run python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), ensure_ascii=False, indent=2))"
```

`support_envelope()` 输出较大，通常只在深度调试或审计时使用。日常预检应优先使用 `provider_menu_summary()`。

## 十三、仓库内证据

- [系统架构](ARCHITECTURE.md)
- [Provider 指南](PROVIDERS.md)
- [环境变量示例](../.env.example)
- [Python 核心依赖](../requirements.txt)
- [Python GPU 依赖](../requirements-gpu.txt)
- [Remotion 依赖](../remotion-composer/package.json)
- [Apple Silicon MPS 支持](apple-silicon-mps.md)
- [Backlot 说明](../backlot/README.md)
- [工具基础契约](../tools/base_tool.py)
- [工具注册表](../tools/tool_registry.py)
- [本地视频模型元数据](../tools/video/_shared.py)
- [ComfyUI 模型栈](../tools/_comfyui/metadata.py)

---

本报告反映基准提交和审计机器在 2026-08-18 的状态。若依赖、凭据、模型、Provider 或硬件发生变化，应重新运行预检并更新“当前机器实测状态”，而不是继续引用旧的可用数量。
