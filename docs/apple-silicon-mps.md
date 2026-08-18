> **简体中文（主版本）** | [English (secondary version)](apple-silicon-mps.en.md)

# Apple Silicon (MPS) 支持

OpenMontage 通过 PyTorch 的 Metal Performance Shaders (MPS) 后端支持 Apple Silicon Mac（M1/M2/M3/M4/M5）。本地 GPU 工具——包括视频生成、放大和人脸修复——会自动检测并使用可用的 MPS。

## 要求

- macOS 12.3 (Monterey) 或更高版本
- Apple Silicon Mac（M 系列芯片）
- Python 3.10+

## 快速设置

```bash
# 启用本地生成
export VIDEO_GEN_LOCAL_ENABLED=true

# 安装依赖——默认 torch wheel 已包含 MPS 支持
uv pip install diffusers transformers accelerate torch pillow requests

# 用于放大和人脸修复
uv pip install realesrgan gfpgan
```

无需特殊的 CUDA 构建或单独的 MPS 软件包——在 macOS 上运行 `uv pip install torch` 时会自动包含 MPS 支持。

## 工作原理

`tools/video/_shared.py` 中的 `get_torch_device()` 辅助函数会检测最佳可用设备：

1. **CUDA**（NVIDIA GPU）——可用时优先使用；运行扩散模型最快
2. **MPS**（Apple Silicon Metal）——用于 M 系列 Mac；性能良好
3. **CPU**——后备方案，始终可用，但速度明显更慢

设备选择会自动完成。所有本地 GPU 工具（`upscale`、`face_restore`、`ltx_video_local`、`wan_video_local` 等）都通过此辅助函数选择设备。

## 已知限制

- **VRAM**：Apple Silicon 使用统一内存。需要超过 16 GB VRAM 的模型可能无法在配备 16 GB 内存的 Mac 上运行。请检查工具的 `resource_profile.vram_mb`。
- **bfloat16**：MPS 不支持。流水线会在 MPS 上自动使用 float16，在 CPU 上使用 float32。
- **CPU 卸载**：`enable_model_cpu_offload()` 仅支持 CUDA。在 MPS 上，流水线会改用直接设备放置。
- **Real-ESRGAN 的半精度模式**：fp16 在 MPS 上可能产生 NaN 瑕疵，因此放大操作会在非 CUDA 设备上自动使用 fp32。

## 验证 MPS 是否启用

```python
from tools.video._shared import get_torch_device
print(get_torch_device())  # 在 Apple Silicon 上应输出 "mps"
```

如果这段代码在 Apple Silicon Mac 上输出 `"cpu"`，请确认：

- macOS 版本为 12.3+
- 已安装 PyTorch（`uv pip install torch`）
- 正在运行原生 ARM Python（而非 Rosetta x86）
