**简体中文主文档** | [英文副本](PROVIDERS.en.md)

# OpenMontage Provider 指南

全面了解 OpenMontage 中的每个 Provider，包括设置说明、定价、免费额度，以及各自能够解锁的能力。

---

## 快速开始：我应该设置哪些 Provider？

**从免费方案开始，再按需添加付费 Provider。** 建议按以下顺序配置：

| 步骤 | 成本 | 设置内容 | 解锁能力 |
|------|------|----------|----------|
| 1 | **$0** | Pexels + Pixabay | 素材照片和视频——足以制作基础视频 |
| 2 | **$0** | Google API key | 700+ 种语音的 TTS（每月免费 100 万字符）+ 新账户 $300 赠金 |
| 3 | **$0** | ElevenLabs | 高级 TTS + 音乐 + SFX（每月免费 1 万字符） |
| 4 | **$0** | Piper（本地安装） | 完全离线的 TTS——无需 API key、零成本、无需网络 |
| 5 | **~$0.03/image** | fal.ai | FLUX 图像 + Kling/Veo/MiniMax 视频 + Recraft——一个 key 即可广泛覆盖图像与视频 |
| 6 | **~$0.05/image** | OpenAI | GPT Image 2 图像 + OpenAI TTS |
| 7 | **~$0.04/image** | Google Imagen | Imagen 4 图像（与 Google API key 共用） |
| 8 | **pay-as-you-go** | Kling Official | Kling 官方直连的视频、图像、TTS、Avatar 和 lip-sync API，与 fal.ai Kling 相互独立 |
| 9 | **pay-as-you-go** | Volcengine Ark | Seedance 2.0 Standard/Fast/Mini 官方直连 API |
| 10 | **$12/month** | Runway | Gen-4 视频——质量最高的 AI 视频 |
| 11 | **pay-as-you-go** | Hunyuan cloud video | 中文友好的 T2V + I2V |
| 12 | **pay-as-you-go** | HeyGen | Avatar 视频、多模型视频网关 |
| 13 | **pay-as-you-go** | Suno | 带人声和歌词的完整歌曲生成 |
| 14 | **$0 + GPU** | Local video gen | WAN 2.1、Hunyuan、CogVideo、LTX——免费、离线 |
| 15 | **$0 + GPU** | Local Diffusion | Stable Diffusion 图像——免费、离线 |

### 环境变量汇总

```bash
# .env — add your keys here

# FREE (no cost, ever)
PEXELS_API_KEY=              # Stock photos + videos
PIXABAY_API_KEY=             # Stock photos + videos

# GOOGLE (one key, multiple tools, generous TTS free tier)
GOOGLE_API_KEY=              # Google TTS + Imagen + Lyria music + Gemini Omni/Veo video

# VOICE + MUSIC
ELEVENLABS_API_KEY=          # TTS, music, sound effects (10K chars/month free)
FISH_AUDIO_API_KEY=          # fish.audio TTS (voice cloning via reference_id, inline emotion tags)
OPENAI_API_KEY=              # OpenAI TTS + GPT Image 2 images
XAI_API_KEY=                 # xAI Grok image generation/editing + Grok video generation
DOUBAO_SPEECH_API_KEY=       # Volcengine Doubao Speech TTS (strong Mandarin narration)
DOUBAO_SPEECH_VOICE_TYPE=    # Default Doubao speaker/voice type
DASHSCOPE_API_KEY=           # Alibaba DashScope (Qwen image gen, TTS, ASR with word timestamps)

# AZURE AI SPEECH (optional cloud STT + TTS; one key unlocks both directions)
AZURE_SPEECH_KEY=            # Azure AI Speech — azure_stt (Fast Transcription) + azure_tts (neural narration)
AZURE_SPEECH_REGION=         # Speech resource region, e.g. eastus

# MULTI-MODEL GATEWAY (one key, 6+ tools)
FAL_KEY=                     # FLUX, Recraft, Kling, Veo, MiniMax video
MINIMAX_API_KEY=             # MiniMax first-party image + MiniMax H3 video generation
ATLASCLOUD_API_KEY=          # Atlas Cloud image/video gateway

# KLING OFFICIAL DIRECT API
KLING_API_KEY=               # Official Kling video, image, TTS, avatar, lip sync
KLING_API_BASE_URL=          # Optional; default https://api-singapore.klingai.com

# VOLCENGINE ARK DIRECT SEEDANCE 2.0 / 2.5 API
ARK_API_KEY=                 # API key body only; do not include the "Bearer " prefix

# VIDEO
HEYGEN_API_KEY=              # HeyGen avatar video gateway
RUNWAY_API_KEY=              # Runway native + Seedance 2.5, Gemini Omni, MiniMax H3
SUNO_API_KEY=                # Suno music generation

# TENCLOUD HUNYUAN VIDEO
TENCENT_TOKENHUB_API_KEY=    # Tencent Hunyuan cloud video via TokenHub API

# LOCAL (no keys needed — just GPU + install)
VIDEO_GEN_LOCAL_ENABLED=     # Set to "true" for local video gen
VIDEO_GEN_LOCAL_MODEL=       # wan2.1-1.3b, wan2.1-14b, hunyuan-1.5, ltx2-local, cogvideo-5b

# COMFYUI (optional overrides; localhost:8188 is the default)
COMFYUI_SERVER_URL=          # Local ComfyUI server for shared workflows
COMFYUI_VIDEO_SERVER_URL=    # Optional video-specific ComfyUI server
```

---

## 当前视频模型覆盖范围

以下集成基于已有文档且当前公开的模型标识符。对于未提供公开 API 契约的 Provider 页面，本文没有添加推测性的模型字符串。

| 模型 | 直连 Provider | fal.ai | Runway | ComfyUI Partner Nodes | Local ComfyUI |
|------|---------------|--------|--------|-----------------------|---------------|
| **Gemini Omni Flash** | Google `gemini_omni_video` | `gemini_omni_fal`（T2V、I2V、引用、编辑） | `runway_video` model `gemini_omni_flash` | `GeminiVideoOmni`（托管服务，使用付费 credits） | 不提供本地权重 |
| **Seedance 2.5** | Volcengine `seedance_ark` model variant `2.5` | `seedance_video` model version `2.5` | `runway_video` model `seedance2_5` | `ByteDance2TextToVideoNode`（托管服务，使用付费 credits） | 不提供本地权重 |
| **MiniMax H3** | `minimax_video` model `MiniMax-H3` | `minimax_fal_video`（`hailuo-03`） | `runway_video` model `hailuo3` | `MinimaxHailuo03TextToVideoNode`（托管服务，使用付费 credits） | 支持官方开放权重及导出的 API workflow |

ComfyUI Partner Nodes 在 ComfyUI graph 内运行，但会调用托管服务；它们需要网络连接、已登录的 Comfy 账户和预付 credits。此表中只有 MiniMax H3 开放权重 workflow 属于本地模型路径。

Replicate、HeyGen 和 Higgsfield 没有更新到这些确切的模型版本，因为在本次更新时，它们的公开 API 文档尚未公开当前且稳定的契约。

---

## 云端 Provider

### xAI — Grok 图像 + 视频

> **适合希望由一个 Provider 同时处理图像编辑和参考条件短视频的用户。** Grok 使用同一个 key 即可覆盖图像生成/编辑和视频生成。

**解锁的工具：** `grok_image`、`grok_video`
**环境变量：** `XAI_API_KEY`

#### 设置

1. 创建 xAI developer 账户
2. 在 xAI developer console 中生成 API key
3. 添加到 `.env`：`XAI_API_KEY=xai-...`

#### 最适合的场景

- 图像编辑与风格迁移
- 将多张图像合成为一张生成画面
- 人物、服装或产品需要延续到动态画面中的短参考图像视频

#### 定价

当前 xAI 文档中 Grok 媒体模型的定价：

| 模型 | 价格 |
|------|------|
| `grok-imagine-image` | 每张生成图像 $0.02 |
| `grok-imagine-image` 输入图像（编辑/合成） | 每张输入图像 $0.002 |
| `grok-imagine-video` 480p | $0.05/sec |
| `grok-imagine-video` 720p | $0.07/sec |
| `grok-imagine-video` 输入图像 | 每张输入图像 $0.002 |

OpenMontage 现在会在 Grok 工具的估算器中使用这些已公布费率。

---

### Volcengine Jimeng — 即梦 AI 视频生成

> **通过 V4 签名直连 ByteDance API。** 使用 IAM AK/SK 凭证进行 HMAC-SHA256 请求签名，调用 Volcengine visual API（visual.volcengineapi.com）。通过 Jimeng 3.0 Pro 支持 text-to-video 和 image-to-video。

**解锁的工具：** `jimeng_video`
**环境变量：** `VOLC_ACCESSKEY`（Access Key ID）+ `VOLC_SECRETKEY`（Secret Access Key）

#### 设置

1. 前往 [console.volcengine.com/iam/keymanage](https://console.volcengine.com/iam/keymanage)
2. 如果还没有 Volcengine 账户，请先创建账户
3. 创建一对 Access Key（AK + SK）
4. 确保账户有权使用 Jimeng AI（即梦）视频生成服务
5. 添加到 `.env`：`VOLC_ACCESSKEY=...` 和 `VOLC_SECRETKEY=...`

#### 最适合的场景

- 直接使用 ByteDance/Volcengine API 配额
- Jimeng 3.0 Pro text-to-video 和 image-to-video
- 中文提示词理解
- 可配置帧数（121=5s、241=10s）和宽高比

#### API 说明

身份验证使用 Volcengine IAM V4 签名（HMAC-SHA256），而不是 Bearer token。签名流程会构建 canonical request，按 SK → date → region → service 的顺序派生 signing key，并对请求签名。

API 流程：`POST ?Action=CVSync2AsyncSubmitTask` → 轮询 `POST ?Action=CVSync2AsyncGetResult` → 下载 `video_url`。

实现使用兼容的通用 `CVSync2Async*` 路由（API version `2022-08-31`），而不是公开 API explorer 中展示的模型专用 `2024-06-06` actions。这是有意设计：通用路由通过 `req_key` 支持相同的 Jimeng 3.0 Pro 模型，同时在模型更新时保持稳定。

视频的 `req_key` 是 `jimeng_ti2v_v30_pro`。成功代码为 `10000`。任务状态包括：`in_queue`、`generating`、`done`、`not_found`、`expired`。

**权威 API 参考：** [Jimeng TI2V V30 Pro SubmitTask](https://api.volcengine.com/api-docs/view?action=JimengTI2VV30PROSubmitTask&serviceCode=cv&version=2024-06-06)

**Schema 约束**（由 `input_schema` 强制执行，以防付费调用失败）：
- `prompt`：最多 800 个字符
- `frames`：必须恰好为 `121`（24fps 时为 5s）或 `241`（24fps 时为 10s）
- `seed`：随机时为 `-1`，或任意非负整数

#### 定价

| 模型 | 价格 |
|------|------|
| Jimeng 3.0 Pro（video） | ~$0.05/sec（实际费率请查看 Volcengine console） |

---

### Volcengine Ark — 直连 Seedance 2.0 和 2.5 视频生成

> **Seedance 官方直连 API。** 直接调用 Volcengine Ark，不经由 fal.ai 或 Replicate，同时保留这些既有 Provider 路径作为相互独立的 fallback。

**解锁的工具：** `seedance_ark`

**环境变量：** `ARK_API_KEY`

#### 设置

1. 打开 [Volcengine Ark API key console](https://console.volcengine.com/ark/region:cn-beijing/apiKey)
2. 启用 Seedance 模型系列，并确认账户有余额或有效资源包
3. 创建长期有效的 API key
4. 将 key body 添加到 `.env`：`ARK_API_KEY=...`

不要在环境变量值中包含 `Bearer ` 前缀。工具发送请求时会自行添加 authorization scheme。

可选覆盖项：

```bash
ARK_SEEDANCE_MODEL=doubao-seedance-2-0-260128
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_CNY_PER_USD=7.2
```

#### 模型与能力

| Variant | 默认 model ID | 输出 |
|---------|---------------|------|
| 2.5 | `doubao-seedance-2-5-260628` | 480p 或 720p；4–30 秒 |
| Standard | `doubao-seedance-2-0-260128` | 480p、720p、1080p 或 4K |
| Fast | `doubao-seedance-2-0-fast-260128` | 480p 或 720p |
| Mini | `doubao-seedance-2-0-mini-260615` | 480p 或 720p |

adapter 支持：

- text-to-video、首帧 image-to-video 和多模态 reference-to-video
- 编码为已验证 Data URI 的本地图像和音频输入
- 远程参考图像、视频和音频 URL
- 任务创建、查询、取消和有界轮询
- 同步音频、可选返回末帧、针对纯文本请求的 web search，以及输出下载
- 提交前 dry-run 和基于 token 的成本估算

Seedance 2.5 最多接受 30 个图像、10 个视频和 10 个音频引用。使用 `model: "2.5"`（或其确切 model ID）选择它。由于公开文档没有为此模型提供稳定的默认 token 价格，OpenMontage 要求先设置 `custom_price_cny_per_million_tokens`，再展示成本估算；未知价格绝不会被报告为免费。

由于公开 API 未说明支持 video Data URI，因此会有意拒绝本地参考视频。请改用 Provider 可访问的 HTTPS URL 或 Ark asset reference。

#### API 与计费说明

异步 API 流程如下：

`POST /contents/generations/tasks` → `GET /contents/generations/tasks/{id}` → 下载成功结果的 URL。

可以使用 `DELETE /contents/generations/tasks/{id}` 取消队列中的任务。任务记录仅保留有限时间，成功结果 URL 也会很快失效，因此工具会及时下载输出。

Ark 按 completion tokens 对 Seedance 计费。费率因模型、分辨率以及请求是否包含参考视频而异。OpenMontage 会在提交前估算成本，并在 Provider 返回 usage 时据此核算。付费运行前请查看 Ark console 中的当前费率；custom endpoint ID 和 Seedance 2.5 需要显式设置 custom price，确保未知价格不会被当作免费。

官方参考：[Seedance model list](https://www.volcengine.com/docs/82379/1366799)、[create task](https://www.volcengine.com/docs/82379/1520757?lang=zh)、[query task](https://www.volcengine.com/docs/82379/1521309?lang=zh)。

---

### Alibaba DashScope — Qwen 图像 + TTS + ASR

> **最适合中文内容制作。** 一个 key 即可解锁 Qwen-Image 生成、Qwen-TTS 普通话旁白，以及带词级时间戳的 Qwen-ASR——这是唯一能为字幕对齐提供词级粒度的 DashScope 路径。

**解锁的工具：** `dashscope_image`、`dashscope_tts`、`dashscope_asr`
**环境变量：** `DASHSCOPE_API_KEY`

#### 设置

1. 前往 [dashscope.aliyun.com](https://dashscope.aliyun.com/)
2. 如果还没有 Alibaba Cloud 账户，请先创建账户
3. 在 DashScope console 中生成 API key
4. 添加到 `.env`：`DASHSCOPE_API_KEY=sk-...`

#### 最适合的场景

- 提示词理解能力强的中文图像生成（Qwen-Image）
- 自然的普通话旁白（Qwen-TTS、Cherry voice）
- 用于字幕对齐的词级时间戳转录（Qwen-ASR filetrans）
- 替代已损坏的 ASR `whisperx` slot

#### API 说明

DashScope 的 `/compatible-mode/v1/` 仅支持 `/chat/completions` 和 `/embeddings`。图像生成、TTS 和 ASR 都使用 DashScope 原生 endpoint，request shape 为嵌套的 `{model, input, parameters}`，而不是 OpenAI-compatible 路径。

ASR 工具（`qwen3-asr-flash-filetrans`）使用异步 submit-poll 模式。音频必须位于可公开访问的 URL（不支持本地文件）。词级时间戳以毫秒为单位，工具会将其标准化为秒。

#### 定价

| 模型 | 价格 |
|------|------|
| `qwen-image-2.0-pro` | 每张图像约 $0.02（当前费率请查看 console） |
| `qwen3-tts-flash` | 每字符约 $0.000015 |
| `qwen3-asr-flash-filetrans` | 按分钟计费（请查看 console） |

---

### Tencent Hunyuan Cloud — 图像生成

> **中文友好的第一方图像生成。** `hunyuan_image` 通过 Tencent TokenHub 使用 Bearer-token 身份验证访问 Hunyuan Image 3.0。它支持带 seed 的 text-to-image、最多三张参考图像、自定义分辨率、提示词改写和水印控制。

**解锁的工具：** `hunyuan_image`

**环境变量：** `TENCENT_TOKENHUB_API_KEY`

在 Tencent Cloud TokenHub console 中生成 API key，并将其添加到 `.env`。工具根据 TokenHub 的 credit 价格，报告每张生成图像约 $0.08。该工具可通过 `image_selector` 使用；共享参考图像输入会标准化为该 Provider 的 `images` array。

---

### fal.ai — 多模型网关

> **用一个 key 广泛覆盖。** 一个 API key 即可解锁跨多个模型的图像和视频 Provider。

**解锁的工具：** `flux_image`、`recraft_image`、`seedream_image`、
`kling_video`、`veo_video`、`seedance_video`、`gemini_omni_fal`、
`minimax_fal_video`、`fal_elevenlabs_tts`、`fal_elevenlabs_music`
**环境变量：** `FAL_KEY`

#### 设置

1. 前往 [fal.ai](https://fal.ai/) 并点击 **Sign up**（GitHub 或 Google）
2. 打开 [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
3. 点击 **Create Key** 并复制它
4. 添加到 `.env`：`FAL_KEY=your-key-here`

#### 定价

无需订阅——纯 pay-as-you-go，没有最低消费。

**图像生成：**

| 模型 | 价格 | 每 $1 可生成 |
|------|------|-------------|
| FLUX Pro v1.1 | $0.05/image | 20 张图像 |
| FLUX Dev | $0.03/image | 33 张图像 |
| Recraft v3 | ~$0.04/image | 25 张图像 |
| Seedream 5 Pro（最高 1536x1536） | $0.0675/image | 约 14 张图像 |
| Seedream 5 Pro（最高 2048x2048） | $0.135/image | 约 7 张图像 |

**视频生成：**

| 模型 | 价格 | 每 $1 可生成 |
|------|------|-------------|
| Kling 2.5 Turbo Pro | $0.07/sec | 14 秒 |
| Seedance 2.5 | 取决于 endpoint | 4–30 秒 |
| Gemini Omni Flash | 取决于 endpoint | 3–10 秒 |
| MiniMax H3（`hailuo-03`） | 取决于 endpoint | 4–15 秒 |
| Veo 3 | $0.40/sec | 2.5 秒 |
| WAN 2.5 | $0.05/sec | 20 秒 |

**免费额度：** 无——但起步无需付费，只需为实际使用量付费。

同一个 key 还可通过 fal.ai 使用 ElevenLabs speech 和 music。direct ElevenLabs 凭证不可用时请使用 `fal_elevenlabs_tts`，也可以通过 `tts_selector` 并设置 `preferred_provider: "fal.ai"` 来选择它。

---

### MiniMax — 官方直连图像与视频 API

> **第一方图像和视频生成。** MiniMax 直连 API 支持带 seed 的图像生成，以及带文本、首/尾帧、图像/视频/音频引用和全球或中国大陆 routing 的 MiniMax H3 视频生成。

**解锁的工具：** `minimax_image`、`minimax_video`

**环境变量：** `MINIMAX_API_KEY`

**可选 region：** `MINIMAX_REGION=global`（默认）或 `cn`

#### 设置

1. 创建 MiniMax Open Platform 账户。
2. 在账户的 API-key 页面生成 API key。
3. 将 `MINIMAX_API_KEY=...` 添加到 `.env`。
4. 对于中国大陆账户，还需设置 `MINIMAX_REGION=cn`。

`MINIMAX_BASE_URL` 可用于已记录的 private/enterprise endpoint 覆盖。默认的全球和中国大陆 host 根据 `MINIMAX_REGION` 选择。

#### MiniMax H3 视频

使用 `minimax_video` 并设置 `model: "MiniMax-H3"`。工具使用 v2 task 契约（`POST /v2/video_generation`，然后 `GET /v2/query/video_generation/{task_id}`），支持 4–15 秒的 2K clip。较旧的 Hailuo 模型继续使用 v1 API。MiniMax H3 reference generation 可以组合图像、视频和音频；参考音频需要同时提供视觉引用。

#### 定价

| 模型 | 全球 pay-as-you-go 价格 |
|------|------------------------|
| `image-01`、`image-01-live` | 每张生成图像 $0.0035 |

MiniMax 也提供带每日图像额度的 subscription token plan。OpenMontage 会在成本估算和生成结果中保守地报告标准 pay-as-you-go 金额。

这些工具可通过图像和视频 selector 自动发现；设置 `preferred_provider: "minimax"` 即可选择它们。

---

### Atlas Cloud — 图像与视频网关

**工具：** `atlas_image`、`atlas_video`
**环境变量：** `ATLASCLOUD_API_KEY`（aliases：`ATLAS_CLOUD_API_KEY`、`ATLAS_API_KEY`）
**Skill：** `.agents/skills/atlas-cloud/SKILL.md`

Atlas Cloud 通过一个 endpoint 和 key 提供下列明确编目的路由。OpenMontage 会验证每个模型的真实 schema，而不会假设 task suffix 或参数名称可以互换。

| 系列 | 支持的路由 | 当前 Atlas 费率 |
|------|------------|----------------:|
| Seedance 2.5 | text/image/reference to video | $0.134/sec |
| Seedance 2.0 | text/image/reference to video | $0.112/sec |
| Gemini Omni Flash | text/image/reference to video；video edit；developer text/image/reference | $0.112–0.140/sec |
| MiniMax H3 | text/image/reference to video | $0.100/sec |
| Seedream 5.0 Pro | text to image；edit；layer decomposition | $0.022–0.045/image |
| GPT Image 2 | text to image；edit | $0.009–0.010/image |
| Nano Banana 2 | text to image；edit | $0.080/image |

通过 `get_info()["model_catalog"]` 查看确切的 ID、operations、media shapes、durations 和 resolutions。价格为从各模型 machine-readable Atlas 页面获得的估算值，付费批量运行前应再次确认。

---

### Kling Official — 直连 API

> **Kling 官方路径。** 此路径不同于经由 fal.ai 的 `kling_video`：它使用 Kling 官方 `Authorization: Bearer <KLING_API_KEY>` API、Provider 名称 `kling_official`，以及直连 Classic/Turbo/Omni task protocols。

**解锁的工具：** `kling_official_video`、`kling_official_image`、`kling_tts`、`kling_avatar`、`kling_lip_sync`
**环境变量：** `KLING_API_KEY`，可选 `KLING_API_BASE_URL`

#### 设置

1. 创建或打开 Kling AI Open Platform 账户。
2. 在 Kling API console 中生成官方 API key。
3. 添加到 `.env`：
   ```bash
   KLING_API_KEY=your-key-here
   # Optional, defaults to Singapore:
   KLING_API_BASE_URL=https://api-singapore.klingai.com
   ```

#### 最适合的场景

- 直接获得官方 Kling API provenance，而不是经由 fal.ai gateway routing
- 通过 `kling_official_video` 使用 text-to-video、image-to-video 和深度 Video Omni reference workflow
- 通过 `kling_official_image` 使用 text-to-image、image edit/reference 和 Image Omni 多参考或 series workflow
- 已知官方 Kling `voice_id` 时，通过 `kling_tts` 使用 text-to-speech
- 通过 `kling_avatar` 生成云端 Avatar 主播 clip，而不替换本地 `talking_head`
- 通过 `kling_lip_sync` 使用云端 lip-sync，并为多人视频显式选择面部
- 需要使用官方 Kling 模型权限、resource pack 或区域 endpoint 的账户

#### 说明

<!--
Compatibility sentinels for documentation contract tests:
Elements remain an internal Kling Official helper
Account Usage is available as a low-frequency diagnostic helper
Official Kling audio effects and video effects are documented but intentionally not registered
-->

- `provider="kling_official"` 有意与 fal.ai 的 `provider="kling"` 保持不同。
- Kling Official 是付费远程 API。OpenMontage 采用保守的成本估算，并计入 Omni references、series output、4k mode 和 native sound 等高成本因素。
- 本地图像路径会为受支持的 Classic/image-generation fields 以 raw base64 发送。Turbo image-to-video 需要 URL，不会静默通过 fal.ai 上传。
- Video Omni 和 Image Omni 可以通过 `element_list` 传递官方 `element_id` references；Elements 仍然是 Kling Official 的内部 helper，而不是独立的 OpenMontage capability。
- Account Usage 以低频 diagnostic helper 的形式提供，位于 `tools/_kling/account.py`；它不是 selector 或 pipeline tool。
- 提供 `callback_url` 时会透传并记录，但 OpenMontage 默认仍会轮询任务。
- `kling_tts` 要求显式提供 `voice_id`；OpenMontage 不会猜测默认的官方 voice。
- `kling_avatar` 和 `kling_lip_sync` 注册在现有 `avatar` capability 下，并与本地 SadTalker/Wav2Lip 工具共存。当前 Avatar pipeline 必须显式选择它们；仅有 registry discovery 不会替换本地工具。
- Kling 官方的 audio effects 和 video effects 已有文档说明，但暂未有意注册为 OpenMontage 工具，因为当前 pipeline 没有稳定的 sound-effects 或 video-effects capability slot。

---

### ElevenLabs — 语音、音乐、音效

> **高级语音质量。** 最适合旁白密集型视频的 TTS，也可生成音乐和音效。

**解锁的工具：** `elevenlabs_tts`、`music_gen`
**环境变量：** `ELEVENLABS_API_KEY`

#### 设置

1. 前往 [elevenlabs.io](https://elevenlabs.io) 并点击 **Sign up**
2. 打开 **Profile**（左下角）> **API Keys**，或访问 [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击 **Create API Key**，为其命名并复制
4. 添加到 `.env`：`ELEVENLABS_API_KEY=xi_your-key-here`

#### 定价

| 方案 | 价格 | 每月字符数 | 主要特性 |
|------|------|------------|----------|
| **Free** | $0 | 10,000 | 3 个自定义 voice、API access、要求 attribution |
| Starter | $5/mo | 30,000 | 无需 attribution |
| Creator | $22/mo | 100,000 | Professional voice cloning |
| Pro | $99/mo | 500,000 | 96kbps audio、usage analytics |
| Scale | $330/mo | 2,000,000 | Priority support |

**免费额度：** 每月 10,000 个字符（约 2–3 分钟旁白）。包含 API access。免费额度中也可使用音乐生成和音效，但 credits 有限。

---

### fish.audio — 富有表现力的 TTS + 语音克隆

> **高情绪表现力的旁白和可复用的克隆语音。** S2-generation 模型支持内联情绪标签（`[laugh]`、`[whispers]`）和 80+ 种语言。在 fish.audio playground 中创建的 voice 可通过 `reference_id` 跨运行复用。

**解锁的工具：** `fish_audio_tts`
**环境变量：** `FISH_AUDIO_API_KEY`

#### 设置

1. 在 [fish.audio](https://fish.audio) 注册
2. 在 [fish.audio/go-api/api-keys](https://fish.audio/go-api/api-keys/) 创建 API key
3. 添加到 `.env`：`FISH_AUDIO_API_KEY=your-key-here`
4. （可选）在 fish.audio playground 中创建或选择 voice model，并将其 ID 作为 `reference_id` 传入，以复用克隆语音

#### 后端模型

`model` 为**必填项——没有默认值**。可传入以下值之一：

| 模型 | 最适合的场景 |
|------|--------------|
| `s2.1-pro` | 最新旗舰——内联情绪标签、80+ 种语言、hero narration |
| `s2.1-pro-free` | s2.1-pro 的推广期免费访问——draft、sample、validation run（参见下方注意事项） |
| `s2-pro` | 第一代 S2——稳定的高质量并支持情绪标签 |
| `s1` | 为兼容性保留的上一代旗舰（不支持情绪标签） |

**`s2.1-pro-free` 注意事项——这是推广活动，不是长期免费额度。** 根据 [fish.audio announcement](https://fish.audio/ko/blog/s2-1-pro-free-api/?articleLocale=en)，免费 API access **持续到 2026 年 8 月 31 日**，受 Fair Use 限制，**不提供 SLA 或 latency 保证**，fish.audio **可能保留**请求，并且**限制商业使用**。不要将客户工作或生产旁白路由到此模型，也不要按 $0 规划长期成本——推广期结束后，`fish_audio_tts.estimate_cost()` 会回退到付费 `s2.1-pro` 费率。

fish.audio API 已移除旧版 `speech-1.x` tier 和 `s1-mini`，不再支持它们。

#### 定价

按输入文本的 **UTF-8 byte** 计费（不是按字符）——CJK 文本和 emoji 的成本，是相同可见长度 ASCII 字符的 3–4 倍。当前标价：`s1` / `s2-pro` / `s2.1-pro` = 每 100 万 bytes $15；`s2.1-pro-free` 仅在推广期内为 $0（持续到 2026 年 8 月 31 日——参见上述注意事项）。大批量生成前，请在[官方定价指南](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits)中核实当前价格。

---

### Doubao Speech — 普通话 TTS

> **出色的普通话旁白。** Volcengine Doubao Speech 很适合中文解说配音和需要字幕时间信息的长篇旁白。

**解锁的工具：** `doubao_tts`
**环境变量：** `DOUBAO_SPEECH_API_KEY`、`DOUBAO_SPEECH_VOICE_TYPE`

#### 设置

1. 打开 Volcengine Doubao Speech console 并启用 Speech Synthesis 2.0。
2. 创建 new-console API Key。
3. 选择 Speech 2.0 voice type，例如 `zh_female_vv_uranus_bigtts`。
4. 添加到 `.env`：
   ```bash
   DOUBAO_SPEECH_API_KEY=your-api-key
   DOUBAO_SPEECH_VOICE_TYPE=zh_female_vv_uranus_bigtts
   ```

#### API 说明

OpenMontage 使用 new-console API key 流程：

```text
X-Api-Key: ${DOUBAO_SPEECH_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
```

不要将 new-console API Key 作为 `X-Api-App-Id` 或 `X-Api-Access-Key` 传入。两者不匹配可能产生 `load grant: requested grant not found`。

#### 最适合的场景

- 面向中文解说视频的自然普通话旁白
- 通过 `/api/v3/tts/submit` 和 `/api/v3/tts/query` 生成异步长篇旁白
- 用于字幕对齐的字符级 timing metadata
- 视频时长可随已批准语音节奏调整的平静教育类 pacing

#### 语速

自然的普通话表达可从 `speech_rate: 0` 开始。如果已批准的格式需要更紧凑的时长，请先比较 `speech_rate: 25` 或 `50` 的短 sample，再生成完整旁白。除非用户明确需要这种权衡，否则不要强制 Doubao 匹配其他 Provider 的时长。

#### 定价

Doubao Speech 2.0 在 Volcengine 中按字符包或使用量计费。OpenMontage 根据文本长度估算成本，并在可用时优先采用 Provider 返回的 usage metadata。

---

### Tencent Hunyuan Cloud — 视频生成

> **通过 TokenHub API 使用 Tencent Hunyuan（腾讯混元）云端视频生成。** 通过 Tencent TokenHub API，使用 Tencent Hunyuan 模型从文本或图像生成视频。该 API 是一个 OpenAI-compatible gateway（tokenhub.tencentmaas.com），采用简单的 Bearer-token 身份验证，无需 TC3-HMAC-SHA256 签名。

**解锁的工具：** `hunyuan_cloud_video`
**环境变量：** `TENCENT_TOKENHUB_API_KEY`

#### 设置

1. 前往 [Tencent Cloud TokenHub console](https://console.cloud.tencent.com/tokenhub)。
2. 创建 application 或打开 **API Key** 部分。
3. 生成 API key 并复制其值。
4. 添加到 `.env`：
   ```bash
   TENCENT_TOKENHUB_API_KEY=your-tokenhub-api-key
   ```

#### 最适合的场景

- **中文友好的提示词理解**——Hunyuan 模型对中文提示词的原生理解优于大多数西方 API
- **简单的身份验证**——Bearer token，无需复杂签名（只需一个 HTTP Authorization header）
- **直用 Tencent Cloud 配额**——使用自己的 Tencent Cloud credits，而不是第三方网关加价
- **同时支持 T2V 和 I2V**——一个 API key 即可解锁 text-to-video 和 image-to-video

#### API 说明

TokenHub 使用 **submit-then-poll** 模式：

```text
# Submit a generation task
POST https://tokenhub.tencentmaas.com/v1/api/video/submit
Authorization: Bearer ${TENCENT_TOKENHUB_API_KEY}

# Poll for results
POST https://tokenhub.tencentmaas.com/v1/api/video/query
Authorization: Bearer ${TENCENT_TOKENHUB_API_KEY}
```

| 模型 | 类型 | 定价 |
|------|------|------|
| `hy-video-1.5` | Text-to-video | 1.5 credits（~$0.25） |
| `yt-video-2.0` | Image-to-video | 2–5 credits（~$0.33–0.83） |

分辨率选项：**720p**（默认）或 **1080p**。

默认会添加水印（`logo_add`）。设置 `logo_add: 0` 可将其关闭（需要 Tencent console 批准）。

**Schema 约束：**
- **Prompt：** 最多 200 个 UTF-8 字符
- **Image：** 最大 10MB，每边 50–5000 px，宽高比 1:4 到 4:1
- **Formats：** jpg、png、jpeg、webp、bmp、tiff

#### Fallback 工具

如果 `hunyuan_cloud_video` 返回错误，Agent 可使用以下工具重试：`jimeng_video`、`kling_official_video`、`minimax_video`

#### 定价

Tencent TokenHub 采用基于 credit 的定价体系（1 credit = 1.2 RMB ≈ $0.167 USD）：

| 模型 | 分辨率 | Credits | 预计 USD |
|------|--------|---------|----------|
| HY-Video-1.5 | any | 1.5 | ~$0.25 |
| YT-Video-2.0 | 480p | 2 | ~$0.33 |
| YT-Video-2.0 | 720p / 1080p | 5 | ~$0.83 |

> **免费额度：** Tencent 偶尔会为 TokenHub 提供新用户 credits。请在 [TokenHub console](https://console.cloud.tencent.com/tokenhub) 查看当前活动。

---

### Azure AI Speech — Speech-to-Text

> **云端转录。** Azure AI Speech Fast Transcription 可将本地音频转为文本，并提供词级时间戳、speaker diarization 和多语言识别，无需 GPU。可选方案：本地 faster-whisper `transcriber` 仍是默认的离线 STT 路径。设置 `AZURE_SPEECH_KEY` 后，Agent 会优先选择 `azure_stt` 进行云端转录。

**解锁的工具：** `azure_stt`
**环境变量：** `AZURE_SPEECH_KEY`、`AZURE_SPEECH_REGION`（或 `AZURE_SPEECH_ENDPOINT`）

#### 设置

1. 在 [Azure portal](https://portal.azure.com) 中创建 **Speech** resource（Azure AI services → Speech service）。
2. 打开该 resource 的 **Keys and Endpoint** 页面。
3. 复制 **KEY 1** 和 **Location/Region**（例如 `eastus`）。
4. 添加到 `.env`：
   ```bash
   AZURE_SPEECH_KEY=your-speech-resource-key
   AZURE_SPEECH_REGION=eastus
   # AZURE_SPEECH_ENDPOINT=https://<custom>...  # optional, overrides region
   ```

#### API 说明

OpenMontage 使用 **Fast Transcription** REST endpoint，它直接接受本地音频文件（multipart upload）并同步返回结果，无需 Azure Blob storage、SAS URL 或异步 job polling：

```text
POST https://{region}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15
Ocp-Apim-Subscription-Key: ${AZURE_SPEECH_KEY}
```

对于时长超过约 2 小时的文件或批量任务，请改用 Azure Batch Transcription（尚未接入 OpenMontage）。

#### 最适合的场景

- 无需本地 GPU、提供词级时间戳的云端转录
- 在候选 locale 集合中自动进行多语言检测
- 无需 HuggingFace token 的 speaker diarization
- 可直接流入 `subtitle_gen` 的字幕 timing metadata

#### 定价

Azure AI Speech Standard（S0）按音频小时对 speech-to-text 计费（撰写本文时约为 $1.00/audio-hour；免费 F0 tier 包含有限的每月额度）。OpenMontage 根据转录音频时长估算成本。当前费率请参阅 [Azure AI Speech pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)。

---

### Azure AI Speech — Text-to-Speech

> **云端神经网络旁白。** Azure neural TTS 提供高质量多语言 voice，支持 SSML prosody control 和 express-as style——与 `azure_stt` 使用同一个 Speech resource，因此一个 key/region 可解锁两个方向。可选方案：本地 `piper_tts` 仍是默认的离线 TTS 路径。设置 `AZURE_SPEECH_KEY` 后，Agent 可优先选择 `azure_tts` 生成云端旁白。

**解锁的工具：** `azure_tts`
**环境变量：** `AZURE_SPEECH_KEY`、`AZURE_SPEECH_REGION`（或 `AZURE_TTS_ENDPOINT`）

#### 设置

与上述 STT 设置相同——同一个 Speech resource key 和 region 可同时用于两者。如果已经配置 `azure_stt`，`azure_tts` 现在即可使用。

```bash
AZURE_SPEECH_KEY=your-speech-resource-key
AZURE_SPEECH_REGION=eastus
# AZURE_TTS_ENDPOINT=https://<region>.tts.speech.microsoft.com  # optional, overrides region
```

注意：TTS host（`<region>.tts.speech.microsoft.com`）不同于 STT endpoint，因此可选的 override var 是 `AZURE_TTS_ENDPOINT`，而不是 `AZURE_SPEECH_ENDPOINT`。

#### API 说明

OpenMontage 使用同步 REST v1 endpoint 和 SSML body，无需 token exchange、Blob storage 或 job polling：

```text
POST https://{region}.tts.speech.microsoft.com/cognitiveservices/v1
Ocp-Apim-Subscription-Key: ${AZURE_SPEECH_KEY}
Content-Type: application/ssml+xml
X-Microsoft-OutputFormat: audio-48khz-192kbitrate-mono-mp3
```

Voice shortlist aliases：`andrew`（默认——温暖、自信）、`brandon`（更低沉）、`ava`（明亮女声）、`guy`（权威）、`jenny`（友好）。可原样接受任何 Azure voice short name。有关 SSML `rate`/`pitch`/`style` 指南，请参阅 `azure-text-to-speech` skill。

#### 最适合的场景

- 使用现有 Azure 凭证的高质量 neural narration
- 平静、自信的 explainer / founder-register 表达
- 通过 *Multilingual* voice family 生成多语言旁白
- 确定性重新渲染（固定 voice + SSML → 相同音频）

不适合：完全离线制作（请使用 `piper_tts`）或语音克隆（请使用 `elevenlabs_tts`）。

#### 定价

Azure neural TTS Standard（S0）约按**每 100 万字符 $16** 计费（免费 F0 tier 包含有限的每月额度）。一段 150 词的旁白成本约为 $0.015。OpenMontage 根据字符数估算成本。当前费率请参阅 [Azure AI Speech pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)。

---

### Google — TTS + Imagen + 音乐 + 视频（共用 Key）

> **一个 key，五个工具。** Google Cloud TTS 提供 50+ 种语言的 700+ 种 voice，是最强的本地化选项。`google_imagen` 同时支持 Imagen 4 和 Gemini 2.5 Flash Image，包括没有 Imagen catalog access 的项目。Google Lyria 可生成高质量背景音乐。Gemini Omni Flash 支持会话式视频编辑，direct Veo generation 则覆盖高级短视频 clip。

**解锁的工具：** `google_tts`、`google_imagen`、`google_music`、`gemini_omni_video`、`veo_video`
**环境变量：** `GOOGLE_API_KEY`（或 `GEMINI_API_KEY`——两者均可；`GEMINI_API_KEY` 优先）

#### 设置

1. 前往 [Google AI Studio](https://aistudio.google.com/) 并登录
2. 打开 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. 点击 **Create API Key**，选择 Google Cloud project
4. 复制 key
5. 添加到 `.env`：`GOOGLE_API_KEY=AIza...`（或 `GEMINI_API_KEY=AIza...`）

**对于 TTS**，还需启用 Text-to-Speech API：
1. 访问 [console.cloud.google.com/apis/library/texttospeech.googleapis.com](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
2. 点击 **Enable**
3. 确保 API key 的 restrictions 允许 Text-to-Speech API

**对于 Imagen、Lyria Music、Gemini Omni video 和 direct Veo video**，请启用 Generative Language API：
1. 访问 [console.cloud.google.com/apis/library/generativelanguage.googleapis.com](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
2. 点击 **Enable**

#### Google TTS 定价

| Voice 类型 | 免费额度 | 付费（每 100 万字符） | 说明 |
|------------|----------|-----------------------|------|
| **Standard** | 1M chars/month | $4.00 | 基础质量、速度快 |
| **WaveNet** | 1M chars/month | $16.00 | 自然语音 |
| **Neural2** | 1M chars/month | $16.00 | 最佳质量 |
| **Studio** | — | $24.00 | 专业录音室 voice |
| **Chirp** | — | $4.00 | 会话式风格 |

各免费额度**相互独立**——每月可免费获得 1M Standard、1M WaveNet 和 1M Neural2 字符。折合每月 250+ 分钟旁白，成本为零。

#### Google Imagen 定价

| 模型 | 每张图像价格 |
|------|--------------|
| Imagen 4 Fast | $0.02 |
| Imagen 4 Standard | $0.04 |
| Imagen 4 Ultra | $0.06 |
| Gemini 2.5 Flash Image（`gemini-2.5-flash-image`） | $0.039 |

**Imagen 免费额度：** 无，仅有付费 tier。

要通过受治理的 `image_selector` 选择 Gemini backend，请传入 `preferred_provider: "google_imagen"` 和 `model_name: "gemini-2.5-flash-image"`。selector 会将其中立的 `model_name` field 映射到 Provider 的 `model` input。

#### Gemini Omni Video 定价

| 模型 | 价格 | 说明 |
|------|------|------|
| `gemini-omni-flash-preview` | 每秒视频约 $0.10 | 720p 视频按 5,792 output tokens/sec 计费，单价为 $17.50/1M tokens |

生成 3–10 秒、720p/24fps 且带合成音频的 clip，并支持有状态会话式编辑（通过 `previous_interaction_id` 执行 `edit_video`）。**仅限付费 tier——没有免费额度。** 一段典型的 8 秒 clip 约为 $0.80；每次编辑都会生成新 clip 并再次计费。

#### Google Music（Lyria）定价

| 模型 | 每次生成请求的价格 |
|------|--------------------|
| `lyria-3-pro-preview` | $0.08（固定费率，时长最长 184s） |

**Music 免费额度：** 无，仅有付费 tier。

**新账户奖励：** Google Cloud 为新账户提供 **$300 赠金**（90 天试用），可用于 TTS、Imagen、Music、Gemini Omni video 和 direct Veo video。

#### Google TTS Voice 类型

Google TTS 提供 50+ 种语言的 700+ 种 voice。Voice 名称遵循 `{language}-{type}-{letter}` 模式：

| 类型 | 示例 | 质量 | 成本 |
|------|------|------|------|
| **Chirp 3 HD** | `en-US-Chirp3-HD-Orus` | **最佳（2024 年，最自然）** | **中等——默认** |
| Standard | `en-US-Standard-A` | 良好 | 最低 |
| WaveNet | `en-US-WaveNet-D` | 很好 | 中等 |
| Neural2 | `en-US-Neural2-D` | 优秀 | 中等 |
| Studio | `en-US-Studio-O` | 专业 | 最高 |
| Journey | `en-US-Journey-D` | 会话式（长篇） | 中等 |

**推荐 voice：** `en-US-Chirp3-HD-Orus`（男声，浑厚/电影感）、`en-US-Chirp3-HD-Aoede`（女声，温暖）。这是 Google 最新的 tier，最自然，并会自动使用 v1beta1 endpoint。

**支持的语言包括：** 英语（美国、英国、澳大利亚、印度）、西班牙语、法语、德语、意大利语、葡萄牙语、日语、韩语、中文（普通话、粤语）、阿拉伯语、印地语、俄语、荷兰语、波兰语、土耳其语、越南语、泰语、印度尼西亚语，以及另外 30+ 种语言。

---

### OpenAI — TTS + 图像生成

> **全面而可靠。** GPT Image 2 擅长复杂的多元素构图和图内文字。TTS 快速且价格合理。

**解锁的工具：** `openai_tts`、`openai_image`
**环境变量：** `OPENAI_API_KEY`

#### 设置

1. 前往 [platform.openai.com/signup](https://platform.openai.com/signup) 并创建账户
2. 在 [platform.openai.com/account/billing](https://platform.openai.com/account/billing) 添加 payment method
3. 打开 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. 点击 **Create new secret key**，为其命名并复制
5. 添加到 `.env`：`OPENAI_API_KEY=sk-...`

#### TTS 定价

| 模型 | 每 100 万字符价格 |
|------|-------------------|
| tts-1 | $15.00 |
| tts-1-hd | $30.00 |
| gpt-4o-mini-tts | $12.00 |

#### 图像定价

| 模型 | 尺寸 | 质量 | 每张图像价格 |
|------|------|------|--------------|
| GPT Image 2 | 1024x1024 | low | $0.006 |
| GPT Image 2 | 1024x1024 | medium | $0.053 |
| GPT Image 2 | 1024x1024 | high | $0.211 |
| GPT Image 2 | 1024x1536 / 1536x1024 | low | $0.005 |
| GPT Image 2 | 1024x1536 / 1536x1024 | medium | $0.041 |
| GPT Image 2 | 1024x1536 / 1536x1024 | high | $0.165 |

> **注意：** OpenAI 已于 2026-05-12 停止 DALL-E 2/3，`gpt-image-1` 系列（`gpt-image-1-mini`、`gpt-image-1.5`）也将于 2026-12-01 退役——`gpt-image-2` 是 OpenAI 推荐的替代方案（参见 [deprecations](https://developers.openai.com/api/docs/deprecations)）。

**免费额度：** 无，需要预付费 billing。此前曾为新账户提供 $5 免费 credits（大多数注册已不再提供）。

---

### Runway — 原生及第三方视频模型

> **多模型制作 API。** OpenMontage 支持当前的 Runway-native 模型，以及已有文档说明的第三方 Seedance 2.5、Gemini Omni Flash 和 MiniMax H3/Hailuo 3.0 路由。

**解锁的工具：** `runway_video`
**环境变量：** `RUNWAY_API_KEY`

#### 设置

1. 前往 [dev.runwayml.com](https://dev.runwayml.com/) 并创建 developer 账户
2. 订阅付费方案（Standard 或更高版本——API 需要订阅）
3. 从 developer portal 生成 API key
4. 添加到 `.env`：`RUNWAY_API_KEY=key_...`

#### 定价

| 方案 | 价格 | Credits/month | 视频容量 |
|------|------|---------------|----------|
| **Free** | $0 | 125 one-time | 约 5 秒 Gen-4 |
| Standard | $12/mo | 625 | 约 25 秒 Gen-4 |
| Pro | $28/mo | 2,250 | 约 90 秒 Gen-4 |
| Unlimited | $76/mo | Unlimited（Explore Mode） | Unlimited Gen-4 Turbo |

**API 定价（Runway credits 每个 $0.01）：**

| 模型 | 每秒价格 |
|------|----------|
| Gen-4 Turbo | ~$0.05 |
| Gen-4.5 | ~$0.12 |
| Seedance 2.5 | 480p 约 $0.20 / 720p 约 $0.30 |
| Gemini Omni Flash | generation 约 $0.10 / video editing 约 $0.11 |
| MiniMax H3（`hailuo3`） | 768P 约 $0.10 / 2K 约 $0.15 |

Seedance 2.5 支持文本、图像和视频输入，输出时长 4–30 秒，最多支持 30 个图像、10 个视频和 10 个音频引用。Gemini Omni Flash 支持 3–10 秒的文本/图像生成，以及最多带五张图像引用的视频编辑。Hailuo 3.0 是 Runway 的 MiniMax H3 路由，支持 768P 或 2K、5–15 秒的输出。adapter 会将每个模型映射到其确切 request field name，而不是发送通用 payload。

Gen-3 Alpha Turbo 和 Gen-4 Aleph 已于 2026-07-30 从 Runway API 移除，工具不再提供它们。

**免费额度：** 一次性 125 credits（不会每月续期），足够生成约 5 秒的 Gen-4 视频。API access 需要付费订阅。

---

### Higgsfield — 多模型视频 Orchestrator

> **多模型视频平台。** 通过一个 API 路由到 Kling 3.0、Veo 3.1、Sora 2、WAN 2.5 和专有 Soul Cinema。包含 Soul ID，可在多个 clip 之间保持角色一致性。

**解锁的工具：** `higgsfield_video`
**环境变量：** `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET`（或组合形式 `HIGGSFIELD_KEY=key:secret`）

#### 设置

1. 前往 [cloud.higgsfield.ai](https://cloud.higgsfield.ai/) 并创建账户
2. 订阅方案（Starter 或更高版本才能使用 API access）
3. 打开 [cloud.higgsfield.ai/api-keys](https://cloud.higgsfield.ai/api-keys) 的 API Keys 部分
4. 生成 API key 和 secret
5. 添加到 `.env`：
   ```
   HIGGSFIELD_API_KEY=your-api-key
   HIGGSFIELD_API_SECRET=your-api-secret
   ```

#### 定价

| 方案 | 价格 | 说明 |
|------|------|------|
| Free | $0 | Limited credits |
| Starter | $15/mo | Basic allocation |
| Plus | $34/mo | Mid-tier，约 33–56 个 Kling 3.0 clip |
| Ultra | $84/mo | High volume |

**单次生成成本（近似值，按 credits 计算）：**

| 模型 | 每个 clip 的成本 |
|------|------------------|
| Kling 3.0 | ~$0.10（最低） |
| WAN 2.5 | ~$0.10 |
| Soul Cinema | ~$0.15 |
| Veo 3.1 | ~$0.50 |
| Sora 2 | ~$0.50 |

**免费额度：** 注册时提供有限 credits。免费方案不会每月续期。

---

### HeyGen — Avatar 视频网关

> **多模型视频网关。** 通过一个 API 使用 VEO、Sora、Runway、Kling 和 Seedance。

**解锁的工具：** `heygen_video`
**环境变量：** `HEYGEN_API_KEY`

#### 设置

1. 前往 [app.heygen.com/register](https://app.heygen.com/register) 并创建账户
2. 打开 settings 中的 API 部分
3. 生成 API key
4. 添加 API balance（预付，与 web plan credits 分开）
5. 添加到 `.env`：`HEYGEN_API_KEY=your-key-here`

#### 定价

| 服务 | 价格 |
|------|------|
| Avatar video（Engine III） | $0.017/sec |
| Avatar video（Engine IV） | $0.10/sec |
| Prompt to Video | $0.033/sec |
| Video Translation（Speed） | $0.05/sec |
| Video Translation（Precision） | $0.10/sec |

**Web 方案：**

| 方案 | 价格 | 说明 |
|------|------|------|
| Free | $0 | 1 credit（demo） |
| Creator | $24/mo | Limited credits |
| Business | $72/mo | API access、更多 credits |

**免费额度：** Web 平台提供 1 credit。API 采用 pay-as-you-go，需要预付 balance。

---

### Suno — AI 音乐生成

> **带人声和歌词的完整歌曲。** 支持任意流派，最长 8 分钟，可生成纯音乐或人声 track。

**解锁的工具：** `suno_music`
**环境变量：** `SUNO_API_KEY`

#### 设置

1. 前往 [suno.com](https://suno.com) 并创建 Suno 账户
2. 如需 API access，请前往 [sunoapi.org](https://sunoapi.org) 并创建账户
3. 打开 dashboard 并复制 API key
4. 添加 credits（1 credit = $0.005 USD）
5. 添加到 `.env`：`SUNO_API_KEY=your-key-here`

#### 定价

**Suno 平台：**

| 方案 | 价格 | Credits | 说明 |
|------|------|---------|------|
| Free | $0 | 50/day | 约 10 首歌曲/天，仅限非商业用途 |
| Pro | $10/mo | 2,500/mo | 商业许可 |
| Premier | $30/mo | 10,000/mo | 商业许可 |

**API（通过 sunoapi.org）：** Pay-as-you-go，1 credit = $0.005。每次生成会产生 2 条 track。

---

### Pexels — 免费素材媒体

> **完全免费。** 零成本，无需 attribution，允许商业使用。

**解锁的工具：** `pexels_image`、`pexels_video`
**环境变量：** `PEXELS_API_KEY`

#### 设置

1. 前往 [pexels.com/join](https://www.pexels.com/join/) 并创建免费账户
2. 打开 [pexels.com/api](https://www.pexels.com/api/)
3. 点击 **Your API Key** 或申请 API access
4. 从 dashboard 复制 key
5. 添加到 `.env`：`PEXELS_API_KEY=your-key-here`

#### 定价

**完全免费。** 没有付费 tier，无需 attribution，允许商业使用。

- 每小时 200 次请求
- 每月 20,000 次请求
- 照片和视频的搜索 + 下载

---

### Pixabay — 免费素材媒体

> **完全免费。** 500 万+ 张免版税图像和视频。

**解锁的工具：** `pixabay_image`、`pixabay_video`
**环境变量：** `PIXABAY_API_KEY`

#### 设置

1. 前往 [pixabay.com/accounts/register](https://pixabay.com/accounts/register/) 并创建免费账户
2. 打开 [pixabay.com/api/docs](https://pixabay.com/api/docs/)
3. 登录后，API key 会显示在 docs 页面顶部
4. 复制 key
5. 添加到 `.env`：`PIXABAY_API_KEY=your-key-here`

#### 定价

**完全免费。** 没有付费 tier，无需 attribution，允许商业使用。

- 约每分钟 100 次请求
- 每小时 5,000 次请求
- 照片和视频的搜索 + 下载
- Standard API 限制为 1280px 图像（full resolution 需要 editorial API）

---

## 本地 Provider（免费，无需 API Key）

这些 Provider 完全在本机运行。无需网络、无需 API key、零成本，其中一部分需要 GPU。

### Remotion — 程序化视频合成

> **基于 React 的视频渲染。** 将静态图像转为带 spring physics、动态 text card、stat card、chart 和 transition 的动画视频。**当未配置任何视频生成 Provider 时，这是关键的 fallback**——Agent 生成图像，再由 Remotion 将其制作成专业观感的视频。

**工具：** `video_compose`（使用 `operation="render"`——需要时自动路由到 Remotion）
**Runtime：** CPU（需要 Node.js）
**环境变量：** 无

#### 设置

```bash
# Included in make setup, or install manually:
cd remotion-composer && npm install && cd ..
```

需要 **Node.js 18+** 和 `npx`。仓库中已包含 `remotion-composer/` project。

#### Remotion 渲染内容

| Component | 生成内容 |
|-----------|----------|
| **TextCard** | 以 spring physics 进入的动态标题/正文文字 |
| **StatCard** | 带 count-up animation 的动态统计数据 |
| **ProgressBar** | 动态 progress indicator |
| **CalloutBox** | 带 icon animation 的高亮 callout panel |
| **ComparisonCard** | 并排比较布局 |
| **BarChart / LineChart / PieChart** | 动态数据可视化 |
| **KPIGrid** | 多指标 dashboard card |
| **Image scenes** | 带 spring animation motion 的静态图像（替代 Ken Burns） |

#### Remotion 何时启用？

`video_compose` 工具的 `render` operation 会自动检测何时需要 Remotion：
- Cut 包含静态图像（`.png`、`.jpg` 等）
- Cut 的 `type` 设置为 `text_card`、`stat_card`、`chart` 等
- Cut 指定了 `animation` 或 `transition_in`/`transition_out`

如果未安装 Remotion，composition 会 fallback 到 FFmpeg Ken Burns pan-and-zoom——功能可用，但吸引力较弱。

**成本：** 免费，始终在本地运行。

---

### HyperFrames - HTML/CSS/GSAP 视频合成

> **GSAP-native 本地渲染。** HyperFrames 是 motion-graphics-heavy HTML composition，以及 `character-animation` pipeline 中 rigged SVG 角色表演的首选 runtime。

**工具：** 直接使用 `hyperframes_compose`，或使用 `video_compose` 并设置 `edit_decisions.render_runtime="hyperframes"`
**Runtime：** CPU（需要 Node.js >= 22、FFmpeg 和 `npx`）
**环境变量：** 无

#### 设置

```bash
node --version
ffmpeg -version
npx --yes hyperframes doctor
```

CLI 以 `npx hyperframes` 的形式使用。不要使用 `npx @hyperframes/cli`；该 package name 不是 OpenMontage runtime 路径。

#### HyperFrames 渲染内容

| 使用场景 | 生成内容 |
|----------|----------|
| **Kinetic typography** | 由 GSAP timeline 驱动的 HTML/CSS 文字动画 |
| **Product / launch videos** | 结构化 HTML scene、registry block 和 transition |
| **Website-to-video** | 带 HyperFrames validation 的 browser-captured site composition |
| **Character animation** | 渲染为 `renders/final.mp4` 的 SVG character rig、pose/action timeline 和 GSAP acting beat |

HyperFrames workspace 位于 `projects/<project-name>/hyperframes/`。最终视频仍遵循正常的 OpenMontage 约定：`projects/<project-name>/renders/final.mp4`。

**成本：** 免费，始终在本地运行。

---

### Piper TTS — 离线 Text-to-Speech

> **完全免费、完全离线的 TTS。** 无需网络，质量良好，适合 draft 和预算受限的项目。

**工具：** `piper_tts`
**Runtime：** CPU（无需 GPU）
**环境变量：** 无

#### 设置

```bash
# Install via pip
pip install piper-tts

# Or download the binary from GitHub
# https://github.com/rhasspy/piper/releases

# Download a voice model (first run downloads automatically)
piper --download-dir ~/.piper/models --model en_US-lessac-medium
```

**可用 voice：** 约 30 种英语 voice，另有德语、法语、西班牙语、意大利语及其他语言的 voice。种类少于云端 Provider，但完全免费且离线。

**质量：** 适合 draft、内部视频和预算项目。面向客户的旁白请使用 ElevenLabs 或 Google TTS。

---

### ComfyUI Video — 本地 Workflow 与托管 Partner Node

**工具：** `comfyui_video`

**可选环境变量：** `COMFYUI_SERVER_URL`（默认 `http://localhost:8188`）和 `COMFYUI_VIDEO_SERVER_URL`（视频专用覆盖）。

捆绑的 WAN 2.2 workflow 和调用方提供的本地 workflow 在 ComfyUI 机器上执行。MiniMax H3 可作为官方开放权重的本地 workflow 使用；请通过 `workflow_json` 或 `workflow_path` 传入以 API 格式导出的官方 workflow，并提供其 `output_node`。

MiniMax H3 本地 stack 包含 pruned INT8 diffusion model、Qwen3-VL text encoder、video VAE 和 audio VAE。OpenMontage 会在工具 metadata 中提供官方下载 URL 和目标文件夹，而不会静默下载大型权重。

同一工具还支持以下 ComfyUI Partner Nodes：

| `model_family` | Node | 执行方式 | 近似成本 |
|----------------|------|----------|----------|
| `gemini_omni_flash` | `GeminiVideoOmni` | Hosted Partner Node | ~$0.146/sec |
| `seedance_2.5` | `ByteDance2TextToVideoNode` | Hosted Partner Node | 480p 约 $0.148/sec；720p 约 $0.333/sec |
| `minimax_h3_api` | `MinimaxHailuo03TextToVideoNode` | Hosted Partner Node | 768P 约 $0.129/sec；2K 约 $0.186/sec |
| `minimax_h3_local` | official MiniMax H3 graph | Local GPU | 无 API 费用 |

Partner Nodes 并非离线运行：它们需要当前版本的 ComfyUI、网络连接、已登录的 Comfy 账户和预付 credits。价格为根据 Comfy credits（211 credits = $1）换算的估算值；以实际 metered usage 为准。

官方参考：[Partner Node overview](https://docs.comfy.org/tutorials/partner-nodes/overview)、[pricing](https://docs.comfy.org/tutorials/partner-nodes/pricing) 和 [MiniMax H3 local tutorial](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)。

---

### 本地视频生成（需要 GPU）

> **免费 AI 视频生成。** 需要具有足够 VRAM 的 NVIDIA GPU。

**工具：** `wan_video`、`hunyuan_video`、`cogvideo_video`、`ltx_video_local`
**Runtime：** Local GPU（需要 CUDA）
**环境变量：** `VIDEO_GEN_LOCAL_ENABLED=true`、`VIDEO_GEN_LOCAL_MODEL=<model>`

#### 设置

```bash
# 1. Install the GPU stack
make install-gpu
# Or manually:
pip install diffusers transformers accelerate torch pillow requests

# 2. Enable local generation in .env
VIDEO_GEN_LOCAL_ENABLED=true

# 3. Choose a model based on your GPU VRAM
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b      # 6GB+ VRAM (entry-level)
VIDEO_GEN_LOCAL_MODEL=wan2.1-14b       # 24GB+ VRAM (best local quality)
VIDEO_GEN_LOCAL_MODEL=hunyuan-1.5      # 12GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=ltx2-local       # 8GB+ VRAM (fastest)
VIDEO_GEN_LOCAL_MODEL=cogvideo-5b      # 10GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=cogvideo-2b      # 6GB+ VRAM (lightest)
```

#### 模型比较

| 模型 | VRAM | 质量 | 速度 | 最适合的场景 |
|------|------|------|------|--------------|
| **WAN 2.1 (1.3B)** | 6GB | 良好 | 快 | 入门级 GPU、快速迭代 |
| **WAN 2.1 (14B)** | 24GB | 优秀 | 慢 | 最佳质量与 VRAM 比例 |
| **Hunyuan 1.5** | 12GB | 很好 | 中等 | 中端 GPU |
| **LTX-2** | 8GB | 良好 | 最快 | 快速 draft、最低 latency |
| **CogVideo (5B)** | 10GB | 良好 | 中等 | 均衡选项 |
| **CogVideo (2B)** | 6GB | 一般 | 快 | 低 VRAM 实验 |

**所有本地模型都支持：** Image-to-video、text-to-video、离线生成、带 seed 的可复现性。

---

### Local Diffusion — 离线图像生成（需要 GPU）

> **免费 Stable Diffusion 图像生成。** 无 API 成本，完全离线。

**工具：** `local_diffusion`
**Runtime：** Local GPU（需要 CUDA）
**环境变量：** 无（安装依赖项即可启用）

#### 设置

```bash
pip install diffusers transformers accelerate torch
```

首次运行会下载模型（约 4GB），后续运行使用缓存模型。

**VRAM 要求：** 4GB+（1024x1024 图像建议 8GB）

**支持：** Negative prompt、seed、自定义尺寸。质量低于 FLUX 或 GPT Image 2，但完全免费且离线。

---

### Modal 上的 LTX-2 — 自托管 Cloud GPU

> **在 Modal 的 cloud GPU 上运行 LTX-2。** 使用自己的 endpoint，按自己的规模扩展。比本地 GPU 更稳定，比商业 API 更便宜。

**工具：** `ltx_video_modal`
**Runtime：** Cloud（self-hosted）
**环境变量：** `MODAL_LTX2_ENDPOINT_URL`

#### 设置

1. 创建 [Modal](https://modal.com) 账户
2. 部署 LTX-2 endpoint（参见 Modal docs）
3. 在 `.env` 中设置 endpoint URL：`MODAL_LTX2_ENDPOINT_URL=https://your-modal-endpoint`

**Modal 定价：** A100 GPU 时间约 $0.99/hour。每个视频的成本取决于生成时间。

---

### 其他本地工具（始终可用）

这些工具仅需要 FFmpeg 或 Python package，无需 GPU 和 API key。

| 工具 | 安装 | 功能 |
|------|------|------|
| **FFmpeg tools**（video_compose、video_stitch、video_trimmer、audio_mixer、audio_enhance、color_grade、face_enhance、frame_sampler、scene_detect） | `brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install FFmpeg` | 视频编辑、音频处理、调色、分析 |
| **Transcriber** | `pip install faster-whisper` | 带词级时间戳的 speech-to-text |
| **Background Remove** | `pip install rembg`（CPU）或 `pip install rembg[gpu]` | 移除图像/视频背景 |
| **Upscale** | `pip install realesrgan`（需要 PyTorch + CUDA） | Real-ESRGAN 图像/视频放大 |
| **Face Restore** | `pip install gfpgan`（需要 PyTorch） | CodeFormer/GFPGAN 人脸修复 |
| **Code Snippet** | `pip install Pygments Pillow` | 带语法高亮的代码图像 |
| **Diagram Gen** | `npm install -g @mermaid-js/mermaid-cli` | Mermaid 图表渲染 |
| **Math Animate** | `pip install manim` | ManimCE 数学动画 |
| **Subtitle Gen** | 无需安装 | 生成 SRT/VTT 字幕文件 |
| **Video Understand** | `pip install transformers torch` | CLIP/BLIP-2 视觉分析 |
| **Talking Head** | Clone [SadTalker](https://github.com/OpenTalker/SadTalker) | 从照片 + 音频生成 Avatar 动画 |
| **Lip Sync** | Clone [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) | 音频驱动的唇形同步 |

---

## Provider 到工具的映射

| Provider | 环境变量 | 解锁的工具 | 成本 |
|----------|----------|------------|------|
| **Pexels** | `PEXELS_API_KEY` | `pexels_image`, `pexels_video` | 免费 |
| **Pixabay** | `PIXABAY_API_KEY` | `pixabay_image`, `pixabay_video` | 免费 |
| **Piper** | —（仅需安装） | `piper_tts` | 免费 |
| **Azure AI Speech** | `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` | `azure_stt`, `azure_tts` | 免费额度 + 付费 |
| **Google** | `GOOGLE_API_KEY`（或 `GEMINI_API_KEY`） | `google_tts`, `google_imagen`, `google_music`, `gemini_omni_video`, `veo_video` | 免费额度（TTS）+ 付费 |
| **ElevenLabs** | `ELEVENLABS_API_KEY` | `elevenlabs_tts`, `music_gen` | 免费额度 + 付费 |
| **fish.audio** | `FISH_AUDIO_API_KEY` | `fish_audio_tts` | 免费额度（s2.1-pro-free）+ 付费 |
| **fal.ai** | `FAL_KEY` | `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `seedance_video`, `gemini_omni_fal`, `minimax_fal_video` | Pay-as-you-go |
| **Atlas Cloud** | `ATLASCLOUD_API_KEY` | `atlas_image`, `atlas_video` | Pay-as-you-go |
| **Kling Official** | `KLING_API_KEY` | `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, `kling_lip_sync` | Pay-as-you-go |
| **Volcengine Ark** | `ARK_API_KEY` | `seedance_ark` | Pay-as-you-go |
| **MiniMax direct** | `MINIMAX_API_KEY` | `minimax_image`, `minimax_video` | Pay-as-you-go |
| **OpenAI** | `OPENAI_API_KEY` | `openai_tts`, `openai_image` | 仅付费 |
| **xAI** | `XAI_API_KEY` | `grok_image`, `grok_video` | 仅付费 |
| **Runway** | `RUNWAY_API_KEY` | `runway_video` | 免费试用 + 付费 |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | `higgsfield_video` | 订阅（$15-84/mo） |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video` | Pay-as-you-go |
| **Suno** | `SUNO_API_KEY` | `suno_music` | Pay-as-you-go |
| **Tencent Hunyuan** | `TENCENT_TOKENHUB_API_KEY` | `hunyuan_cloud_video` | Pay-as-you-go（~$0.25–0.83/gen） |
| **Local GPU** | `VIDEO_GEN_LOCAL_ENABLED` | `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local` | 免费（需要 GPU） |
| **Local Diffusion** | —（仅需安装） | `local_diffusion` | 免费（需要 GPU） |
| **Modal** | `MODAL_LTX2_ENDPOINT_URL` | `ltx_video_modal` | 自托管云端 |
| **ComfyUI** | 可选的 server URL 覆盖 | `comfyui_video` | Local GPU，或付费 Partner Node credits |

---

## 能力覆盖范围

各项能力对应的 Provider 数量：

| 能力 | 云端 Provider | 本地 Provider | 免费选项 |
|------|---------------|---------------|----------|
| **图像生成** | FLUX、Kling Official、Grok、Google Imagen、GPT Image 2、Recraft | Local Diffusion | Pexels、Pixabay（stock） |
| **视频生成** | Grok、Kling Official、fal.ai、通过 Volcengine Ark 使用 Seedance、Runway、Veo、Gemini Omni、Higgsfield、MiniMax、HeyGen、Tencent Hunyuan、ComfyUI Partner Nodes | WAN、Hunyuan、CogVideo、LTX、ComfyUI WAN、ComfyUI MiniMax H3 | Pexels、Pixabay（stock） |
| **Text-to-Speech** | Azure AI Speech、ElevenLabs、fish.audio、Google TTS、Kling Official、OpenAI | Piper | Piper、Google 免费额度、ElevenLabs 免费额度、Azure 免费额度、fish.audio s2.1-pro-free |
| **音乐生成** | ElevenLabs、Suno、Google Lyria | — | ElevenLabs 免费额度 |
| **后期制作** | — | FFmpeg（compose、stitch、trim、mix、enhance、grade） | 全部免费 |
| **分析** | — | WhisperX、Scene Detect、Frame Sampler、CLIP/BLIP-2 | 全部免费 |
| **增强** | — | Upscale、BG Remove、Face Enhance、Face Restore | 全部免费 |
| **Avatar** | Kling Official | SadTalker、Wav2Lip | 本地工具免费 |

---

## 常见问题

**问：制作视频的绝对最低要求是什么？**
答：FFmpeg + Node.js（两者均免费且在本地运行）。FFmpeg 负责视频组装、音频混合和字幕。有了 Node.js，Remotion 可以将静态图像渲染成动画视频；即使没有任何视频生成 API，Agent 也能生成图像，再由 Remotion 使用 spring animation、text card 和 transition 将它们制作为专业观感的视频。再添加 Piper TTS 可获得免费旁白，添加 Pexels/Pixabay 可获得免费素材画面。

**问：我没有任何视频生成 Provider，还能制作视频吗？**
答：可以。Agent 会生成静态图像（通过任何图像 Provider，甚至可以使用 Pexels/Pixabay 的免费 stock），再由 Remotion 使用 spring physics transition、text card、stat card 和 chart 将它们合成为动画视频。当未配置视频生成时，这是 explainer 和 animation pipeline 的默认路径。

**问：有什么低门槛的方法可以同时获得 AI 生成的图像和视频？**
答：fal.ai（`FAL_KEY`）是一种用单个 key 广泛覆盖的 pay-as-you-go 选项。它可解锁 FLUX 图像和多个视频 Provider。无需订阅，只需为实际生成内容付费。

**问：我有 GPU，可以免费在本地运行什么？**
答：设置 `VIDEO_GEN_LOCAL_ENABLED=true` 并安装 `diffusers`。这样即可获得 WAN 2.1、Hunyuan、CogVideo 和 LTX 视频生成，以及 Stable Diffusion 图像生成——全部免费、全部离线。

**问：我应该使用哪个 TTS Provider？**
答：追求质量 → ElevenLabs。需要本地化（50+ 种语言）→ Google TTS。预算有限 → Google 免费额度（每月 100 万字符）。离线使用 → Piper。

**问：我需要配置所有这些 Provider 吗？**
答：不需要。从现有配置开始即可。selector pattern 会自动路由到任何可用选项。缺少某个 Provider 时，系统会自动转到下一个。
