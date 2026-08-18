# OpenMontage 的 ComfyUI 提供商适配器

> **文档语言：** 本文是**简体中文主文档**；[英文副本](comfyui-adapter-plan.en.md) 完整保留原始英文内容。

**RFC：用于图像和视频生成的原生 ComfyUI 后端**

---

## 动机

OpenMontage 的本地 GPU 工具（`wan_video`、`hunyuan_video`、`cogvideo_video`、
`local_diffusion`）直接使用 HuggingFace `diffusers`。这套方案可在 x86 +
消费级 GPU 上运行，但在 PyTorch 生态尚未跟上的新硬件上会失效：

| 问题 | 详情 |
|------|------|
| **NVIDIA Blackwell (sm_121)** | 没有适用于 aarch64 + CUDA 13.0 的稳定 PyTorch wheel 包，需要 NGC 容器或每夜构建版本。 |
| **Flash Attention** | 不支持 sm_121，必须替换为 SageAttention v3 或原生 SDPA。 |
| **统一内存（GB10/DGX Spark）** | `nvidia-smi` 无法报告 VRAM，导致 Diffusers 的内存估算失效。 |
| **模型格式不匹配** | Diffusers 期望使用 HF 仓库，而生产部署使用带量化变体（NVFP4、FP8）的 `.safetensors` 模型检查点，diffusers 无法原生加载这些格式。 |

ComfyUI 已经解决了上述所有问题。NVIDIA 为 DGX Spark 提供官方 ComfyUI 容器。
社区也为 Blackwell 优化了工作流（SageAttention、NVFP4 量化、LightX2V 4 步
LoRA）。WAN 2.2、FLUX 2 和 ACE-Step 等模型，可以通过 ComfyUI 在 diffusers
无法工作的硬件上可靠运行。

ComfyUI 适配器让 OpenMontage 无需随项目分发或维护 PyTorch 构建版本，
就能在任何可运行 ComfyUI 的硬件上访问 ComfyUI 支持的任意模型。

---

## 设计

### 架构

```
OpenMontage Agent
    |
    v
video_selector / image_selector
    |
    v
comfyui_video    comfyui_image    (new tools)
    |                |
    v                v
ComfyUI REST API  (POST /prompt, GET /history, GET /view)
    |
    v
GPU (any hardware ComfyUI supports)
```

### 集成模型

两个新的 `BaseTool` 子类，加上一个共享客户端库：

```
tools/
  _comfyui/
    __init__.py
    client.py              # Shared ComfyUI REST client
    workflows/             # Bundled workflow templates
      flux2-txt2img.json
      wan22-t2v-4step.json
      wan22-i2v-4step.json
  graphics/
    comfyui_image.py       # capability="image_generation", provider="comfyui"
  video/
    comfyui_video.py       # capability="video_generation", provider="comfyui"
```

### 注册表与选择器集成

这些工具将 `capability` 和 `provider` 声明为类属性。
`tool_registry.discover()` 通过 `pkgutil.walk_packages` 自动发现它们。
`video_selector` 和 `image_selector` 通过 `registry.get_by_capability()` 找到它们。
选择器唯一需要的改动，是在 `video_selector` 中增加按操作类型过滤：
如果只安装了文生视频内置模型，ComfyUI 就不会被选用于
`image_to_video`；反之亦然。

---

## 共享客户端：`tools/_comfyui/client.py`

它封装了已经在生产环境中验证过的 ComfyUI REST API 模式（Bard 项目的
Airflow DAG 已用它完成数千次生成）：

端点契约已经对照当前 ComfyUI 服务器文档和 2026 年 4 月的第三方
开发者指南进行核查：

- 官方文档列出的服务器路由包括：`POST /prompt`、`GET /history/{prompt_id}`、
  `GET /view`、`POST /upload/image`、`GET /object_info/{node_class}`、
  `GET /models/{folder}`、`GET /system_stats` 和 `WS /ws`。
- `/prompt` 在 `prompt` 键下接收 API 格式工作流，并在验证时返回
  `prompt_id`、`number` 和 `node_errors`。
- `/history/{prompt_id}` 返回已完成的节点输出；制品记录包含
  `filename`、`subfolder` 和 `type`。客户端会将这三个值全部传给 `/view`，
  而不是假定 `type=output`。
- 工作流必须导出为 ComfyUI API 格式，而不是常规的可视化画布工作流格式。

参考资料：

- https://docs.comfy.org/development/comfyui-server/comms_routes
- https://www.runflow.io/blog/comfyui-api-developer-guide

```python
class ComfyUIClient:
    """Thin client for the ComfyUI REST API."""

    def __init__(self, server_url: str | None = None):
        self.server_url = server_url or os.environ.get(
            "COMFYUI_SERVER_URL", "http://localhost:8188"
        )

    def is_available(self) -> bool:
        """Health check -- can we reach the server?"""

    def submit(self, workflow: dict) -> str:
        """POST /prompt. Returns prompt_id. Raises on node_errors."""

    def poll(self, prompt_id: str, timeout: int = 600, interval: int = 5) -> dict:
        """GET /history/{prompt_id} until complete. Returns outputs dict."""

    def download(self, filename: str, subfolder: str, dest: Path) -> Path:
        """GET /view?filename=...&type=output. Writes bytes to dest."""

    def upload_image(self, local_path: Path, name: str) -> str:
        """POST /upload/image. Returns server-side filename for LoadImage nodes."""

    def generate(self, workflow: dict, output_node: str, dest: Path,
                 timeout: int = 600) -> Path:
        """Full cycle: submit -> poll -> download. Returns artifact path."""
```

**为什么使用共享客户端？** 对于图像和视频生成，`submit`/`poll`/`download`
循环完全相同。区别仅在于：使用哪个工作流模板、要自定义哪些节点，
以及从哪个输出节点读取结果。

---

## 工具规格

### `comfyui_image` -- 图像生成

| 字段 | 值 |
|------|----|
| capability | `image_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_image`、`image_to_image` |
| dependencies | （运行时：ComfyUI 服务器可访问） |
| fallback_tools | `flux_image`、`local_diffusion`、`openai_image` |
| cost | `$0.00`（本地计算） |

**内置工作流：** `flux2-txt2img.json`

加载带 Mistral 文本编码器的 FLUX 2 Dev (NVFP4)。模板化节点：

| 节点 | 类 | 模板化字段 |
|------|----|------------|
| 4 | CLIPTextEncode | `text`（提示词） |
| 6 | EmptyFlux2LatentImage | `width`、`height` |
| 7 | RandomNoise | `noise_seed` |
| 10 | Flux2Scheduler | `steps` |
| 13 | SaveImage | `filename_prefix` |

**输入 schema：**

```yaml
prompt:        string    # required
width:         integer   # default 1024
height:        integer   # default 1024
steps:         integer   # default 20
seed:          integer   # optional (random if omitted)
guidance:      number    # default 3.5
output_path:   string    # where to save the image
workflow_json: string    # optional custom workflow; requires output_node
workflow_path: string    # optional path to workflow JSON; requires output_node
output_node:   string    # required for custom workflows
workflow_name: string    # optional custom workflow provenance label
workflow_model: string   # optional custom model/provenance label
workflow_model_stack: [] # optional custom dependency provenance
```

**get_status()：** 探测 ComfyUI 服务器，并通过 `/object_info` 检查内置 FLUX
模型名称。当服务器和内置模型集都就绪时返回 `AVAILABLE`；
服务器可访问但缺少内置模型时返回 `DEGRADED`；服务器无法访问时返回
`UNAVAILABLE`。

**execute() 流程：**
1. 深拷贝工作流模板
2. 将 `prompt`、`seed`、尺寸和 `steps` 注入模板化节点
3. `client.generate(workflow, output_node="13", dest=output_path)`
4. 返回包含制品路径、seed 和模型信息的 `ToolResult`

对于自定义工作流，调用者必须提供 `workflow_json` 或 `workflow_path`，
以及 `output_node`。工具不会为自定义工作流假定内置节点 ID；
除非调用者提供 `workflow_model`，否则来源信息会报告为 `user_supplied`。
结果还会包含最终工作流的 SHA-256 哈希；对于内置工作流，还会包含
已知的模型栈。

---

### `comfyui_video` -- 视频生成

| 字段 | 值 |
|------|----|
| capability | `video_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_video`、`image_to_video` |
| dependencies | （运行时：ComfyUI 服务器可访问） |
| fallback_tools | `wan_video`、`hunyuan_video`、`ltx_video_local` |
| cost | `$0.00`（本地计算） |

**内置工作流：**

1. **`wan22-i2v-4step.json`** -- 图生视频（WAN 2.2 14B、fp8、4 步 LightX2V LoRA）
2. **`wan22-t2v-4step.json`** -- 文生视频（WAN 2.2 14B、fp8、4 步 LightX2V LoRA）

这些内置 WAN 2.2 14B FP8 工作流属于高质量配置，建议使用约
16GB VRAM。这并不是 ComfyUI 的统一要求。`comfyui_video` 工具的顶层
`resource_profile` 将 8GB 作为提供商下限，因此预检不会暗示
ComfyUI 本身需要 16GB。低显存用户应使用自定义工作流，例如
Wan 2.1 1.3B、LTX-Video/LTXV FP8 或量化图，或者 Wan 2.2
GGUF/量化社区工作流，并按需减少帧数和降低分辨率。

**I2V 工作流——模板化节点：**

| 节点 | 类 | 模板化字段 |
|------|----|------------|
| 93 | CLIPTextEncode | `text`（正向提示词） |
| 97 | LoadImage | `image`（上传后的服务器文件名） |
| 98 | WanImageToVideo | `width`、`height`、`length` |
| 86 | KSamplerAdvanced | `noise_seed` |
| 108 | SaveVideo | `filename_prefix` |

**输入 schema：**

```yaml
prompt:               string    # required
operation:            string    # "text_to_video" | "image_to_video" (default: t2v)
reference_image_path: string    # local path (for i2v)
reference_image_url:  string    # URL (for i2v, downloaded first)
width:                integer   # default 640
height:               integer   # default 640
num_frames:           integer   # default 81 (5s at 16fps)
seed:                 integer   # optional
output_path:          string    # where to save the video
workflow_json:        string    # optional custom workflow; requires output_node
workflow_path:        string    # optional path to workflow JSON; requires output_node
output_node:          string    # required for custom workflows
workflow_name:        string    # optional custom workflow provenance label
workflow_model:       string    # optional custom model/provenance label
workflow_model_stack: []        # optional custom dependency provenance
timeout_seconds:      integer   # optional, default 3600 (see below)
resume_prompt_id:     string    # optional, resume a timed-out job without resubmitting
```

**execute() 流程（i2v）：**
1. 通过 `client.upload_image()` 上传参考图像
2. 深拷贝 i2v 工作流模板
3. 注入 `prompt`、已上传图像的名称、`seed` 和尺寸
4. `client.generate(workflow, output_node="108", dest=output_path, timeout=inputs.get("timeout_seconds", 3600), resume_prompt_id=inputs.get("resume_prompt_id"))`
5. 返回 `ToolResult`

**execute() 流程（t2v）：**
1. 深拷贝 t2v 工作流模板
2. 注入 `prompt`、`seed` 和尺寸
3. `client.generate(workflow, output_node="16", dest=output_path, timeout=inputs.get("timeout_seconds", 3600), resume_prompt_id=inputs.get("resume_prompt_id"))`
4. 返回 `ToolResult`

**超时与恢复（根据真实本地 GPU 测试新增）：** 客户端的默认等待时长
已从 900s 提升至 3600s。在性能一般的本地 GPU 上，未经加速的自定义 Wan 1.3B
工作流在 832x480/81-97 帧配置下，实测耗时约为 1360-1630s；旧的
900s 默认值会将这些任务误报为失败，即使 ComfyUI 仍在服务器端继续渲染。
`ComfyUIError` 现在会在执行错误和超时两种情况下携带
`prompt_id`（`ComfyUIError.prompt_id`）；`ComfyUIVideo` 的
`ToolResult.error`/`.data` 也会在超时时暴露它，因此调用者不用猜测
任务是否已经终止。要恢复一个已超时但仍在运行的任务，调用者可再次调用
`execute()`，并将 `resume_prompt_id` 设为该 `prompt_id`（如有需要，同时设置
更长的 `timeout_seconds`）。此时 `client.generate()` 会完全跳过 `submit()`，
只恢复对现有任务的轮询和下载，不会排队提交重复任务。

`comfyui_video` 在 `get_info()` 中发布 `operation_statuses`，并实现
`is_operation_available(operation)` 以支持选择器路由。这样，部分安装
的 ComfyUI 可以继续用于已安装的模式，同时不会把尚不可用的操作模式
宣传为就绪。`video_selector` 在 `operation="rank"` 时也会使用
`target_operation` 应用这项就绪检查，因此预检排序不会为
内置模型缺失的操作推荐 ComfyUI。

---

### `comfyui_music` -- 音乐生成（已交付，并带有使用原生节点的内置工作流）

`tools/audio/comfyui_music.py`。`capability="music_generation"`，
`provider="comfyui"`。

**内置默认方案：** ACE-Step v1 (3.5B) 文本转音频，通过
`tools/_comfyui/workflows/ace-step-1-t2a.json` 提供。
最初阻碍此工具的节点包分裂问题（`AceStepModelLoader` 与原生
`TextEncodeAceStepAudio` 等）后来被证明不适用于 ACE-Step v1：
ComfyUI 将 `TextEncodeAceStepAudio`/`EmptyAceStepLatentAudio` 作为
**原生核心节点**（`comfy_extras/nodes_ace.py`）提供，而不是第三方包。
Comfy-Org 自己的
[`workflow_templates`](https://github.com/Comfy-Org/workflow_templates)
仓库也内置了官方 ACE-Step-v1 模板；该模板完全由这些原生节点
和长期稳定的核心节点（`CheckpointLoaderSimple`、`KSampler`、
`ModelSamplingSD3`、`VAEDecodeAudio`、`SaveAudioMP3`）组成。
`ace-step-1-t2a.json` 中每个节点的 `class_type` 与输入名称，都对照
ComfyUI 自身源码（`comfy_extras/nodes_ace.py`、`nodes_audio.py`、
`nodes_latent.py`、`nodes.py`）逐一核查过，并非从 UI 导出结果猜测而来；
这是因为 Comfy-Org 提供的 UI 格式模板不能直接作为此客户端提交的
API 格式 JSON 使用。

`prompt` 映射到 ACE-Step 的 `tags` 字段（风格/流派/情绪描述，与
`suno_music` 既有的“prompt = 期望音乐的描述”约定一致）。`lyrics` 是单独的
可选字段（纯音乐时为空）。`duration_seconds`、`steps`、`cfg`、
`lyrics_strength` 和 `seed` 均可修改；`shift` 与色调映射的
`multiplier` 则保留官方模板的默认值。

新版本或不同的配置也不会被排除：`workflow_json`/`workflow_path` +
`output_node` 覆盖路径与图像/视频工具的行为完全相同，可用于
ACE-Step 1.5、其他节点包，甚至完全不同于 ACE-Step 的音频模型。

**选择器集成：** OpenMontage 没有专用的 `music_selector`（不同于
`tts_selector`/`image_selector`/`video_selector`）——音乐工具已经通过
`registry.get_by_capability("music_generation")` 直接路由，
`comfyui_music` 以与 `suno_music`/`music_gen` 相同的方式参与其中。
`fallback_tools = ["suno_music", "music_gen"]`。

**音频制品 schema：** `ToolResult.data` 遵循与图像/视频工具相同的
结构（`provider`、`model`、`output`、`format`、
`workflow_provenance`），并额外包含 `lyrics` 和 `duration_seconds`。
后者是对已下载文件尽力执行的 `ffprobe` 探测（如果 PATH 中没有
`ffprobe`，则为 `None`），因为即使内置工作流也不会通过
`/history` 回报实际渲染时长。

**工作流/输出节点契约：** 与图像/视频完全相同——
`output_node` 必须是写入最终制品的节点 ID（内置工作流使用
ComfyUI 原生音频保存节点 `SaveAudioMP3`）。`ComfyUIClient.generate()`
提取制品时，现在也会检查 `"audio"` 输出键（此前只检查
`"images"`/`"gifs"`）；`SaveAudioMP3`/`SaveAudio` 正是把结果写入
ComfyUI `/history` 响应的这个键。

---

## 工作流覆盖机制

图像和视频工具接受 `workflow_json` 或 `workflow_path`。提供其中一项后，
自定义工作流会完全替换内置模板，调用者也必须同时提供
`output_node`。之所以需要这项更严格的契约，是因为社区工作流
会使用任意节点 ID。

- 无需修改代码即可使用较新的模型检查点
- 自定义采样策略（不同的调度器、步数、LoRA）
- 原样接入社区工作流
- 对不同生成方案做 A/B 测试

代理也可以从 `tools/_comfyui/workflows/` 读取工作流文件，
以编程方式修改后再传给 `execute()`。

自定义工作流的结果元数据会将 `workflow_provenance.source`
报告为 `user_supplied`；如果提供了 `workflow_model`、`model` 或
`workflow_name`，则将其作为模型标签。若未提供任何自定义标签，
则模型会被报告为 `custom-comfyui-workflow`，而不是某个内置模型名称。
来源信息载荷还会记录 `workflow_hash_sha256`。对于用户提供的工作流，
调用者应在已知的情况下提供 `workflow_model_stack`，其中包含基础模型、
文本编码器、VAE、LoRA 及其强度、调度器、步数和引导系数。

---

## Agent 技能与配置契约

两个 ComfyUI 工具都会声明 Layer 3 `comfyui` 技能。代理在调用任一工具前，
必须阅读 `.agents/skills/comfyui/SKILL.md`，以了解如何加载社区工作流、
识别输出节点、处理 LoRA 加载器链，以及记录自定义工作流的来源信息。

不可用的 ComfyUI 工具会在 `get_info()`、`provider_menu()` 和
`provider_menu_summary().setup_offers[]` 中暴露结构化的 `setup_offer`：

```yaml
kind: local_server
env_var: COMFYUI_SERVER_URL
default_url: http://localhost:8188
health_check: GET /system_stats
```

缺少内置模型时，工具会返回机器可读的
`data.missing_models[]` 列表，其中包含文件名、角色、目标位置提示，
以及 OpenMontage 已知规范来源时的下载 URL。代理应直接
呈现该载荷，而不是解析自然语言错误文本。

---

## 配置

**环境变量：**

```bash
# .env
COMFYUI_SERVER_URL=http://localhost:8188    # ComfyUI API endpoint
COMFYUI_POLL_INTERVAL=5                     # seconds between status checks
COMFYUI_POLL_TIMEOUT=600                    # max wait for image gen
COMFYUI_VIDEO_TIMEOUT=900                   # max wait for video gen
```

**多服务器（可选）：** 通过按能力覆盖，可将
`comfyui_image`、`comfyui_video` 和 `comfyui_music` 指向不同的
ComfyUI 实例，例如一块 GPU 运行 FLUX 2，另一块运行 WAN 2.2，还有一块
运行 ACE-Step。每个覆盖项都仅针对自己的工具，并且优先于
`COMFYUI_SERVER_URL`；三个值全部不设置时，所有工具都会连接同一个
共享服务器。

```bash
COMFYUI_IMAGE_SERVER_URL=http://gpu-a:8188
COMFYUI_VIDEO_SERVER_URL=http://gpu-b:8188
COMFYUI_MUSIC_SERVER_URL=http://gpu-c:8188
```

**对于 Docker Compose 配置**（ComfyUI 位于容器中）：

```bash
COMFYUI_SERVER_URL=http://host.docker.internal:8188
# or
COMFYUI_SERVER_URL=http://comfyui:8188      # if on same docker network
```

---

## 提供商选择行为

适配器可用时，选择器会使用 OpenMontage 的七维评分，
将它与其他提供商一起排序：

| 维度 | ComfyUI 得分 | 理由 |
|------|--------------|------|
| 任务适配度 | 高 | 支持 t2i、i2v、t2v |
| 质量 | 高 | 最新模型（FLUX 2、WAN 2.2 14B） |
| 控制力 | 最高 | 可完整自定义工作流 |
| 可靠性 | 高 | 已在生产环境中验证 |
| 成本 | $0 | 本地计算 |
| 延迟 | 中 | 受 GPU 性能制约，无网络往返 |
| 连续性 | 高 | 使用 seed 时具有确定性 |

ComfyUI 不可用（服务器离线）时，选择器会继续尝试其他可用
提供商。如果只配置了一种视频操作，`video_selector` 会利用工具的
操作级就绪状态，避免为缺失的模式选择 ComfyUI。

---

## 由此解锁的能力

### 立即可用（使用现有模型）

- **FLUX 2 Dev NVFP4** 图像生成 -- 针对 Blackwell 优化，每张图约 60s
- **WAN 2.2 14B FP8 高质量配置** i2v，带 4 步加速 -- 每个 5s 片段约 3.5 min，建议约 16GB VRAM
- **WAN 2.2 14B FP8 高质量配置** t2v（模型已下载，工作流已包含），建议约 16GB VRAM

### 低显存配置

当用户提供适当的 `workflow_json` 或 `workflow_path` 时，ComfyUI 在
8GB-12GB GPU 上仍然可以发挥作用。合适的候选包括：

- 使用 Wan 2.1 1.3B 工作流进行低内存文生视频。
- 使用 LTX-Video/LTXV FP8 或量化工作流快速生成短片段。
- 使用较低分辨率和帧数的 Wan 2.2 GGUF/量化社区工作流。

在经过认可的低显存工作流被内置之前，OpenMontage 应将这些方案视为
自定义工作流配置。对于自定义工作流，资源要求由
工作流提供，而不是从内置 WAN 2.2 14B 配置推断。

### 未来能力（向 ComfyUI 添加模型，OpenMontage 无需修改代码）

- 较新的模型检查点（WAN 3.x、FLUX 3 等）-- 只需更新工作流 JSON
- ControlNet、IP-Adapter、AnimateDiff -- 通过 ComfyUI 自定义节点支持
- 放大、局部重绘、外扩绘制 -- ComfyUI 中已有相应节点
- ComfyUI 生态支持的任意模型

### 硬件可移植性

同一个适配器可用于：
- NVIDIA DGX Spark（GB10、aarch64、CUDA 13.0）
- 消费级 GPU（RTX 3090/4090、x86）
- 云实例（A100、H100）
- 多 GPU 配置（ComfyUI 处理设备分配）

无需固定 PyTorch 版本，无需特定架构的 wheel 包，也无需 CUDA
兼容性矩阵。ComfyUI 就是抽象层。

---

## 实现范围

| 组件 | 文件 | 预计规模 |
|------|------|----------|
| 共享客户端 | `tools/_comfyui/client.py` | ~180 行 |
| 共享元数据 | `tools/_comfyui/metadata.py` | 配置、模型栈和来源信息辅助函数 |
| 图像工具 | `tools/graphics/comfyui_image.py` | ~140 行 |
| 视频工具 | `tools/video/comfyui_video.py` | ~190 行 |
| Layer 3 技能 | `.agents/skills/comfyui/SKILL.md` | 使用契约 |
| 注册表摘要 | `tools/tool_registry.py` | 暴露配置提议 |
| 选择器就绪过滤器 | `tools/video/video_selector.py` | 小型操作就绪检查 |
| 工作流模板 | `tools/_comfyui/workflows/*.json` | 3 个文件 |
| 测试 | `tests/contracts/test_comfyui_tools.py` | ~200 行 |
| 文档 | `docs/comfyui-adapter-plan.md` | 本文件 |

**总计：** 约 500 行 Python + 3 个工作流 JSON。

无需修改：`base_tool.py`、现有的非 ComfyUI 生成提供商、任何
流水线定义或任何 schema。

---

## 待决问题

1. **工作流版本管理：** 工作流 JSON 应存放在仓库中，还是由用户
   通过配置目录提供？内置方案能保证可复现性，
   外部提供则更灵活。

2. ~~**异步生成：**~~ **已解决。** `ComfyUIClient.generate()` 现在默认
   通过 ComfyUI 的 WebSocket feed（`wait_ws()`）等待，立即响应
   `executing`/`execution_error` 事件，而不是在 REST 轮询之间休眠。
   因此，完成和错误都能在没有 `interval` 秒延迟的情况下被
   捕获，可选的 `on_progress` 回调也会收到实时 `progress` 事件
   （`comfyui_video` 用它在长时间渲染时输出步骤进度）。
   没有新增硬依赖：`websocket-client` 是可选导入；
   未安装或连接失败时，`_wait()` 会透明回退到原有的
   `poll()` REST 循环，`resume_prompt_id` 恢复在两条路径上的行为完全一致。

3. ~~**多服务器：**~~ **已解决。**
   `ComfyUIClient(capability="image"|"video"|"music")` 会优先从
   按能力划分的环境变量（`COMFYUI_IMAGE_SERVER_URL` /
   `COMFYUI_VIDEO_SERVER_URL` / `COMFYUI_MUSIC_SERVER_URL`）解析
   服务器 URL，然后依次使用共享的 `COMFYUI_SERVER_URL` 和默认值
   `http://localhost:8188`。三个工具都会在构造时传入各自 capability，
   因此图像、视频和音乐生成可以分别指向不同的 ComfyUI
   实例（不同 GPU、不同模型集），无需修改任何代码。单服务器
   配置不需要额外操作，因为三个环境变量均为可选。
   `client.capability`/`client.is_default_url`/`client.unavailable_reason()`
   都会考虑该覆盖项；`COMFYUI_SETUP_OFFER.per_capability_env_var_overrides`
   则为 `provider_menu()` 中呈现配置提议的逻辑记录了这项能力。

4. ~~**音乐生成：**~~ **已解决——已随内置 ACE-Step v1 工作流
   交付。** `comfyui_music` 现在是真实工具（不是隐藏的图像/视频覆盖项），
   通过现有的 `registry.get_by_capability("music_generation")` 路径进行路由，
   与 `suno_music`/`music_gen` 相同。最初造成阻塞的节点包分裂问题
   后来被证明不适用于 ACE-Step v1：它的 ComfyUI 节点是原生核心节点，
   而不是第三方包，因此 `ace-step-1-t2a.json` 作为默认值随项目提供，并已
   对照 ComfyUI 自身源码逐个节点验证。其他版本/包仍可使用自定义
   `workflow_json`/`workflow_path` + `output_node`。完整契约请参阅上文
   `comfyui_music` 一节。
