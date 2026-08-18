[简体中文主报告](EXTERNAL_DEPENDENCIES_AUDIT.md) | **English copy**

# OpenMontage External Dependency Audit Report

## Report information

| Item | Details |
|---|---|
| Audit date | 2026-08-18 |
| Audit branch | `agent/zh-cn-localization` |
| Baseline commit | `2a09cf3d29833092f9286e0fb5ec2f7cf6603522` |
| Scope | APIs, models, external programs, Python/Node dependencies, networking, storage, hardware, licensing, data boundaries, and host availability |
| Evidence | Tool registry, dependency manifests, runtime source, environment-variable contracts, provider documentation, and host probes |
| Nature | Read-only snapshot of the current code and host; provider status, pricing, and model identifiers may change over time |

## 1. Executive summary

OpenMontage uses a **local orchestration core with pluggable provider capabilities**. It is not a SaaS application that requires every cloud service to be configured at once, and the complete provider catalog must not be mistaken for a set of global mandatory dependencies.

The actual foundation is:

1. An AI coding agent that can read files and execute commands.
2. Python 3.10 or later.
3. FFmpeg and ffprobe.
4. A writable local filesystem with adequate working storage.
5. Node.js, npm, and npx when full Remotion or HyperFrames composition is required.

The project does not intrinsically require a database, Redis, a message queue, object storage, Docker, Kubernetes, or a public inbound service. Local files are the source of truth; the AI coding agent is the control plane, while Python supplies tools and persistence. The host agent determines any general-purpose LLM API use. OpenMontage does not initiate a generic LLM request merely because an `llm` section exists in `config.yaml`.

Cloud image, video, TTS, music, avatar, and 3D services are optional capability boundaries. A missing provider should reduce coverage for that capability without breaking local project state, schemas, checkpoints, Backlot, FFmpeg post-production, or other configured capabilities.

## 2. Dependency layers

### 2.1 Foundation and control

| Dependency | Requirement | Purpose |
|---|---:|---|
| AI coding agent | Required | Reads pipelines and skills, selects tools, and executes review, approval, and checkpoint protocols |
| Python 3.10+ | Required | Tool registry, schemas, checkpoints, provider adapters, and Backlot |
| FFmpeg + ffprobe | Core requirement | Encoding, stitching, trimming, subtitles, audio, probing, and QA |
| Local filesystem | Required | Projects, artifacts, assets, caches, checkpoints, and final renders |
| Git | Installation/collaboration | Clone, version control, and contribution workflows; not a video runtime dependency |
| `make` / `uv` | Optional helpers | Virtual-environment creation, dependency installation, tests, and preflight |

OpenMontage has no resident Python orchestrator. The LLM agent reads `pipeline_defs/`, `skills/`, and the tool registry and then drives execution. The `llm.provider` value in `config.yaml` is part of the configuration model; it does not mean the repository contains a generic Anthropic, OpenRouter, or Ollama client.

### 2.2 Composition and presentation

| Component | Runtime requirements | Notes |
|---|---|---|
| FFmpeg | `ffmpeg`, `ffprobe` | Local and offline-capable; foundation for composition, post-production, and QA |
| Remotion | Node.js, npm, `remotion-composer/node_modules` | React/TypeScript programmatic video composition |
| HyperFrames | Node.js >= 22, npm/npx, FFmpeg, executable `hyperframes` CLI | HTML/CSS/GSAP, Three.js, kinetic typography, and character animation |
| Backlot | FastAPI, uvicorn, watchfiles, modern browser | Read-only local board; listens on `127.0.0.1:4750` by default |

Node.js is not mandatory for the Python + FFmpeg core, but it is an important part of the default high-quality composition paths. README's Node.js 18+ baseline applies to Remotion; full HyperFrames coverage makes Node.js 22+ the effective unified minimum.

### 2.3 Pluggable capabilities

The following are configured only as needed:

- Cloud image, video, TTS, music, avatar, and 3D APIs.
- Local PyTorch, Diffusers, Transformers, and ComfyUI models.
- Stock-media sites and open archives.
- Blender, Manim, Piper, Wav2Lip, SadTalker, Real-ESRGAN, GFPGAN, rembg, and other specialist tools.
- Network research, model downloads, web scraping, screen recording, and browser automation.

## 3. Python and Node software dependencies

### 3.1 Core Python dependencies

`requirements.txt` declares:

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

Development and test dependencies are `pytest`, `pytest-asyncio`, and `httpx2`. The baseline GPU dependencies are `torch`, `torchvision`, and `torchaudio`; `make install-gpu` also installs `diffusers`, `transformers`, and `accelerate`.

### 3.2 Tool-specific Python extensions

| Capability | Additional dependencies |
|---|---|
| Local transcription | `faster-whisper`, optional `whisperx` |
| Video download and subtitles | Python `yt-dlp`, `youtube-transcript-api` |
| Video understanding and CLIP retrieval | `transformers`, `torch` |
| Background removal | `rembg`, optional `onnxruntime-gpu` |
| Upscaling and face restoration | `realesrgan`, `gfpgan`, `torch` |
| Face tracking and auto-reframing | `mediapipe`, `opencv-python` |
| Media corpus | `opencv-python`, `transformers`, `torch` |
| Stock sites without a formal API | `beautifulsoup4` |
| ComfyUI live progress | Optional `websocket-client`; falls back to REST polling |
| Offline TTS | `piper-tts` |
| Mathematical animation | `manim`, possibly LaTeX |
| Syntax highlighting | `Pygments` |
| Audio helper | `pydub` |

### 3.3 Remotion Node dependencies

`remotion-composer/package.json` declares React 18, React DOM 18, Remotion 4, TypeScript 5.3, plus `@remotion/cli`, `@remotion/captions`, `@remotion/google-fonts`, `@remotion/media`, `@remotion/player`, `@remotion/transitions`, D3 Geo, TopoJSON, and World Atlas.

Rendering also indirectly depends on Chromium or Chrome Headless Shell. Google Fonts components may introduce network access depending on the selected font-loading path.

### 3.4 HyperFrames runtime

HyperFrames is fetched dynamically through `npx hyperframes` rather than installed at a repository-pinned version. It depends on:

- Node.js >= 22.
- npm and npx.
- FFmpeg.
- The npm Registry.
- A browser-style validation and rendering environment.

The project does not currently pin an exact HyperFrames version, so first-run behavior, offline use, and supply-chain reproducibility depend on the npm cache and upstream releases.

## 4. Cloud APIs and credentials

All secrets belong in `.env` or process environment variables, never in artifacts, logs, or Git history.

| Provider | Primary environment variables | Capabilities |
|---|---|---|
| fal.ai | `FAL_KEY` / `FAL_AI_API_KEY` | FLUX, Recraft, Seedream, Kling, Veo, Seedance, MiniMax, Gemini Omni, 3D, ElevenLabs TTS/music |
| Atlas Cloud | `ATLASCLOUD_API_KEY`; aliases `ATLAS_CLOUD_API_KEY`, `ATLAS_API_KEY` | Multi-model image, video, and Tripo 3D gateway |
| Google | `GOOGLE_API_KEY` / `GEMINI_API_KEY` | Imagen, Veo, Gemini Omni, Lyria, Cloud TTS |
| Google Vertex | `GOOGLE_APPLICATION_CREDENTIALS`, project, location | Service-account access to Google generation services |
| OpenAI | `OPENAI_API_KEY` | GPT Image 2, OpenAI TTS, Sora 2 |
| xAI | `XAI_API_KEY` | Grok Imagine image and video |
| Kling Official | `KLING_API_KEY`, optional `KLING_API_BASE_URL` | Image, video, TTS, avatar, lip sync |
| Volcengine Ark | `ARK_API_KEY` | Direct Seedance 2.0/2.5 access |
| Volcengine Jimeng | `VOLC_ACCESSKEY` + `VOLC_SECRETKEY` | Jimeng video |
| MiniMax | `MINIMAX_API_KEY` | MiniMax image, H3/Hailuo video |
| Tencent TokenHub | `TENCENT_TOKENHUB_API_KEY` | Hunyuan image and video |
| DashScope | `DASHSCOPE_API_KEY` | Qwen image, TTS, and ASR |
| Azure AI Speech | `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` | Cloud STT and neural TTS |
| ElevenLabs | `ELEVENLABS_API_KEY` | TTS, music, sound effects, voice cloning |
| fish.audio | `FISH_AUDIO_API_KEY` | Expressive TTS and voice cloning |
| Doubao Speech | `DOUBAO_SPEECH_API_KEY` | Mandarin TTS |
| Runway | `RUNWAY_API_KEY` / `RUNWAYML_API_SECRET` | Runway and multi-model video routing |
| HeyGen | `HEYGEN_API_KEY` | Veo, Sora, Kling, Runway, Seedance, and other video routing |
| Higgsfield | key + secret or `HIGGSFIELD_KEY` | Multi-model video and character consistency |
| Replicate | `REPLICATE_API_TOKEN` | Hosted Seedance inference |
| SunoAPI | `SUNO_API_KEY` | Suno-style song and instrumental generation |
| Modal | `MODAL_LTX2_ENDPOINT_URL` | User-hosted LTX-2 cloud-GPU endpoint |
| ComfyUI | `COMFYUI_*_SERVER_URL` | Local/LAN GPU service; Partner Nodes also require an account, network, and credits |

Provider tools commonly submit asynchronous jobs, poll status, and download results. Output URLs may expire within hours or days, so tools must save results promptly into the project workspace.

## 5. Model dependencies

### 5.1 Image models

- FLUX Pro 1.1, FLUX Dev, and FLUX Pro.
- Recraft v4 and v4-pro.
- ByteDance Seedream v5.
- OpenAI `gpt-image-2`.
- Google Imagen 4, Fast, Ultra, and Gemini 2.5 Flash Image.
- Google Nano Banana 2 through Atlas Cloud.
- xAI `grok-imagine-image`.
- MiniMax `image-01` and `image-01-live`.
- DashScope `qwen-image-2.0-pro`, `qwen-image-max`, `wan2.7-image`, and `z-image-turbo`.
- Tencent `hy-image-v3.0`.
- Kling v1 through v3, `kling-image-o1`, and `kling-v3-omni`.
- Stable Diffusion 2.1 Base.
- ComfyUI FLUX.2 Dev NVFP4.

### 5.2 Video models

- Seedance 2.0, 2.0 Fast, 2.0 Mini, and 2.5.
- Google Veo 2, Veo 3, Veo 3.1, and Fast variants.
- Gemini Omni Flash.
- OpenAI Sora 2 and Sora 2 Pro.
- xAI Grok Imagine Video.
- Kling v1 through v3, Turbo, Master, Video O1, and Omni.
- MiniMax H3, Hailuo 2.3, Hailuo 02, and Director variants.
- Tencent `hy-video-1.5` and `yt-video-2.0`.
- Runway Gen-4 Turbo and Gen-4.5.
- Higgsfield Soul Cinema and Seedance/Kling/Veo/Sora/WAN routing.
- Jimeng 3.0 Pro.
- Local Wan 2.1 1.3B/14B, HunyuanVideo 1.5, CogVideoX 2B/5B, and LTX-2.
- ComfyUI WAN 2.2, MiniMax H3, and hosted Partner Nodes.

### 5.3 Speech, music, and analysis models

- OpenAI `gpt-4o-mini-tts`.
- ElevenLabs Multilingual v2 and Eleven v3.
- fish.audio s1, s2-pro, and s2.1-pro.
- DashScope Qwen3 TTS.
- Google Cloud TTS/Chirp, Azure Neural Voice, Kling official voice IDs, and local Piper voices.
- Google Lyria 3 Pro Preview, Suno V4/V4.5/V5, ElevenLabs Music, and ACE-Step 1.3 3.5B.
- faster-whisper tiny through large-v3, DashScope Qwen3 ASR, and Azure Fast Transcription.
- CLIP ViT-B/32, BLIP-2 OPT 2.7B, and LLaVA 1.5 7B.

### 5.4 Enhancement, avatar, and 3D models

- U2Net and ISNet for background removal.
- Real-ESRGAN and RealESRNet for upscaling.
- CodeFormer and GFPGAN for face restoration.
- MediaPipe for face and eye tracking.
- SadTalker, MuseTalk, and Wav2Lip for avatar and lip sync.
- Hunyuan 3D 3.1, SAM 3, and Tripo H3.1 for 3D generation.
- Blender and Three.js for procedural worlds and rendering; they are not generative models.

## 6. Stock media, licensing, and external content

### 6.1 Sources

The main key-based sources are Pexels, Pixabay, Unsplash, Freesound, and Videvo.

Keyless or optionally keyed sources include Archive.org, Wikimedia Commons, NASA, NARA, Library of Congress, Coverr, Pond5 Public Domain, Mixkit, ESA, NOAA, Dareful, JAXA, and Pixabay Music page search.

Mixkit, ESA, NOAA, Dareful, and JAXA depend on site structure and `beautifulsoup4`, which makes them more vulnerable to website changes than formal APIs.

### 6.2 Licensing boundaries

- Pexels, Pixabay, Coverr, and Mixkit commonly do not require attribution.
- Dareful, ESA, some Videvo assets, and Wikimedia content require attribution or per-file verification.
- NASA content is generally usable, but remains subject to NASA Media Usage Guidelines and third-party-mark exceptions.
- Archive.org, LOC, NARA, and Pond5 must follow the license and source fields on each asset record.
- Freesound requires checking the Creative Commons terms of each sound.
- Voice cloning, avatars, real-person likenesses, and brand assets also require authorization, privacy, and platform-policy review.
- Downloadable local weights still have their own licenses, such as Apache-2.0 or LTX-2-Community; downloadability does not imply unrestricted commercial use.

## 7. Network and data boundaries

### 7.1 Outbound network

Cloud generation, web research, model downloads, and stock-media retrieval require:

- DNS and outbound HTTPS on port 443.
- Access to provider APIs, result CDNs, npm, PyPI, GitHub, and Hugging Face.
- Long polling, large media uploads/downloads, and adequate proxy timeouts.
- Firewall rules that do not over-block temporary download URLs, signed URLs, or provider region domains.

### 7.2 Local ports

- Backlot uses `127.0.0.1:4750` by default.
- ComfyUI uses `localhost:8188` by default.
- Remotion, HyperFrames, and browser preview may start temporary local services.

### 7.3 Public inbound access and public media URLs

Most providers use polling by default and do not require an open public inbound port. Kling and similar providers support `callback_url`, but OpenMontage still polls by default.

The following paths may require a provider-accessible public media URL:

- Audio input for DashScope ASR.
- Some reference videos for Seedance Ark.
- Reference media for Jimeng, Tencent, and some video gateways.
- Provider operations that do not accept Data URIs or local paths.

Object storage, temporary signed URLs, or provider upload endpoints are therefore transit dependencies for particular workflows, not global OpenMontage infrastructure.

### 7.4 Data egress

Cloud-provider calls may send:

- Prompts, script fragments, and negative prompts.
- Reference images, video, audio, and voice samples.
- Project metadata, model parameters, and callback addresses.
- A `reference_id` or voice material for voice cloning.

Local FFmpeg, Piper, local models, and local ComfyUI workflows can reduce data egress, although first installation and model downloads may still require network access. Enabling a provider does not cause the project to upload the entire project directory automatically.

## 8. Hardware infrastructure

### 8.1 CPU, memory, and disk

- FFmpeg composition commonly needs 2 to 4 CPU cores.
- Backlot and ordinary Python tools have relatively low resource use.
- Local video models commonly need 16 to 32GB of system memory.
- Model weights, caches, source media, image sequences, and render intermediates can consume several to tens of GB.
- Production environments should budget storage separately for projects, model caches, and temporary rendering.

### 8.2 GPU and VRAM

| Model or tool | Typical VRAM requirement |
|---|---:|
| CogVideoX 2B | 6GB |
| Wan 2.1 1.3B | 8GB |
| LTX-2 | 12GB |
| CogVideoX 5B | 12GB |
| HunyuanVideo 1.5 | 14GB |
| Wan 2.1 14B | 24GB |
| ComfyUI low-VRAM quantized workflows | 8 to 12GB |
| Built-in WAN 2.2 14B FP8 workflow | Recommended 16GB VRAM + 32GB RAM |

The shared local video loader prefers CUDA, then Apple Silicon MPS, then CPU. Tool support for MPS is uneven: `video_understand` currently selects only CUDA or CPU explicitly; Wav2Lip, SadTalker, and similar paths are also more CUDA-oriented. Actual ComfyUI requirements depend on the model, quantization, resolution, frame count, custom nodes, and workflow.

### 8.3 Peripherals and system permissions

Only the corresponding features require:

- Screen-recording permission for `screen_recorder` and Cap.
- Microphone and camera access for capture, live-person material, and avatar acquisition.
- A Blender-capable GPU or display environment for 3D rendering.
- `DISPLAY`, Xvfb, or an equivalent display service on headless Linux.

## 9. Current host measurements

### 9.1 System environment

| Item | Measured result |
|---|---|
| Operating system | macOS 26.6.1, arm64 |
| CPU/GPU | Apple M4, 10-core integrated GPU, Metal 4 |
| Memory | 16GiB unified memory |
| Free workspace storage | Approximately 845GiB |
| Python | 3.10.19 |
| Node.js | 24.13.0 |
| npm/npx | 11.6.2 |
| FFmpeg/ffprobe | 8.1.2 |
| Installed helpers | Git, uv, Docker, GitHub CLI, `yt-dlp` command |
| Missing tools | Blender, ComfyUI, Ollama, Playwright, CUDA, ROCm |
| `.env` | Absent |

### 9.2 Registry status

The registry discovered 117 non-selector tools:

| Runtime type | Current status |
|---|---|
| Local tools | 33/43 available |
| Local GPU tools | 0/14 available |
| API tools | 1/55 available |
| Hybrid tools | 2 available, 1 degraded, 2 unavailable |
| Total | 36 available, 80 unavailable, 1 degraded |

Main capability status:

- FFmpeg provider tools: 17/17 available.
- Video post: 8/9; analysis: 7/13; local character-animation structure tools: 6/6.
- Screen capture: 2/2 available.
- Image generation: 0/16; video generation: 0/26; TTS: 0/10; music generation: 0/5; avatar: 0/4.
- 3D world authoring tools are available, but the production renderer is unavailable.
- Direct stock search has 7/16 sources available, mainly keyless open archives.

The only API-runtime tool currently marked available is keyless, network-dependent Pixabay Music page search. This does not mean that any cloud-generation account is configured.

### 9.3 Current composition and local-AI blockers

- FFmpeg is available.
- Remotion is unavailable because `remotion-composer/node_modules` is not installed.
- The HyperFrames npm package resolves to `0.8.2`, but the host npm cache contains root-owned files. Installation fails with `EACCES`, so the CLI is not currently executable.
- The virtual environment lacks `torch`, `diffusers`, `transformers`, `faster-whisper`, Piper, MediaPipe, OpenCV, rembg, Real-ESRGAN, GFPGAN, and related extensions.
- The system has a `yt-dlp` command, but the virtual environment lacks the Python `yt_dlp` module, so the registry's `video_downloader` remains unavailable.
- With no `.env` or cloud keys, cloud image, video, TTS, music, and avatar capabilities are unavailable.
- `corpus_builder` is degraded: open stock sources exist, but CLIP and visual-corpus dependencies are missing.

## 10. Dependency-contract findings

### 10.1 Incomplete `.env.example` coverage

The current sample does not expose every supported code-level variable as a directly fillable entry, notably:

- The main Atlas Cloud variable and aliases.
- `FREESOUND_API_KEY`, `COVERR_API_KEY`, `NARA_API_KEY`, `POND5_API_KEY`, and `VIDEVO_API_KEY`.
- `COMFYUI_IMAGE_SERVER_URL` and `COMFYUI_MUSIC_SERVER_URL`.
- Some Google, Runway, and Higgsfield aliases and Vertex runtime-mode variables.
- `OPENMONTAGE_PROJECTS_DIR`, cache directories, and capacity limits.
- `BACKLOT_PORT`, `BLENDER_PATH`, `MUSIC_LIBRARY_DIR`, `SADTALKER_PATH`, and `WAV2LIP_PATH`.
- Some endpoint, region, model, and cost override variables.

### 10.2 `setup.py` and `requirements.txt` are not equivalent

`setup.py` omits the complete set of dependencies, including `numpy`, `google-auth`, FastAPI, uvicorn, and watchfiles. `pip install .` therefore does not guarantee the same runtime environment as `make setup` or `pip install -r requirements.txt`.

### 10.3 Node.js version requirements are inconsistent

README uses Node.js 18+, while the HyperFrames contract requires Node.js 22+. Full-capability installation documentation and preflight should report Node.js 22+ as the unified minimum while still identifying Remotion's lower baseline.

### 10.4 Insufficient version locking

- Most Python requirements use `>=` lower bounds, with no Python lockfile.
- HyperFrames is fetched with unversioned `npx hyperframes`.
- Cloud model IDs, rates, quotas, and endpoints are mutable external state.
- Reproducibility for first-time installation and offline restoration is limited.

### 10.5 Dependency declarations are fragmented

Some tools use standard `dependencies` fields; others probe keys, servers, models, or installation state in custom `get_status()` methods. Scanning only `requirements.txt` or `BaseTool.dependencies` therefore undercounts real dependencies. A reliable audit must combine live `support_envelope()`, `provider_menu()`, and implementation review.

## 11. Recommended implementation order

1. Align `.env.example` with the Provider documentation and label required values, aliases, optional overrides, and operation-specific variables.
2. Unify the installation contract across `setup.py`, `requirements.txt`, and `make setup`, or explicitly retire incomplete installation entry points.
3. Unify Node.js version guidance and report Remotion and HyperFrames thresholds separately during preflight.
4. Add a Python lockfile and a validated version/offline-cache policy for HyperFrames.
5. Add automated dependency-audit tests for environment variables, model IDs, external commands, Python modules, and local services.
6. Document a consistent upload/signed-URL path for operations that require public URLs, while keeping object storage optional.
7. Continuously verify both the keyless local core and Chinese/English capability parity in CI so localization and provider changes cannot damage routing.

## 12. Verification commands

The following commands re-check dependencies on the current host without invoking paid generation APIs:

```bash
make preflight

uv run python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), ensure_ascii=False, indent=2))"

uv run python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), ensure_ascii=False, indent=2))"
```

`support_envelope()` produces a large response and is normally reserved for deep debugging or auditing. Routine preflight should prefer `provider_menu_summary()`.

## 13. Repository evidence

- [Architecture](ARCHITECTURE.en.md)
- [Provider guide](PROVIDERS.en.md)
- [Environment-variable example](../.env.example)
- [Core Python dependencies](../requirements.txt)
- [Python GPU dependencies](../requirements-gpu.txt)
- [Remotion dependencies](../remotion-composer/package.json)
- [Apple Silicon MPS support](apple-silicon-mps.en.md)
- [Backlot guide](../backlot/README.en.md)
- [Base tool contract](../tools/base_tool.py)
- [Tool registry](../tools/tool_registry.py)
- [Local video model metadata](../tools/video/_shared.py)
- [ComfyUI model stack](../tools/_comfyui/metadata.py)

---

This report describes the baseline commit and audited host as of 2026-08-18. If dependencies, credentials, models, providers, or hardware change, rerun preflight and update the current-host measurements instead of relying on stale availability counts.
