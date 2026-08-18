<!-- generated-by: gsd-doc-writer -->
> 简体中文（主文档） | [英文副本](QA_PLAN.en.md)

# QA 质量验证计划

## 目的

`tests/qa/` 验证音频混合、视频合成、视频拼接、样式 playbook、完整 `animated-explainer` 流程和可选的 HyperFrames 合成路径。当前脚本使用本地生成的 FFmpeg fixture，不需要 API key，也不会产生 provider 调用费用；质量结论仍需结合脚本输出和人工试听、观看。

## 测试框架与准备

`test_04_audio_mix.py` 至 `test_08_end_to_end.py` 是可直接执行的 QA 脚本；模块导入时就会运行检查。`test_09_hyperframes_compose.py` 使用 `pytest>=8.0` 和真正的断言。

从仓库根目录安装开发依赖：

```bash
make install-dev
```

运行本地测试前还需要：

- `Python >= 3.10`；CI 使用 Python `3.11`。
- `ffmpeg` 和 `ffprobe` 位于 `PATH`。
- HyperFrames QA 额外需要 Node.js `>=22`、`npx`、FFmpeg 以及可解析的 `hyperframes` npm 包。可先运行 `make hyperframes-doctor`。

## 现有测试

| 脚本 | 覆盖内容 | 运行方式 | API key / 费用 |
|---|---|---|---|
| `test_04_audio_mix.py` | `AudioMixer` 的 `mix`、淡入淡出、`duck`、延迟音乐，以及 `ffprobe`/loudness 输出 | 直接执行 | 无 / `$0` |
| `test_05_video_compose.py` | `VideoCompose` 的 cuts + audio、字幕合成、单独烧录字幕、`YOUTUBE_LANDSCAPE` 编码和图片 overlay | 直接执行 | 无 / `$0` |
| `test_06_video_stitch.py` | `VideoStitch` 的兼容性验证、cut/crossfade/fade、`auto_normalize`、预览和三种 spatial layout | 直接执行 | 无 / `$0` |
| `test_07_playbook_intelligence.py` | 所有已发现 playbook 的加载、对比度、配色、色觉安全、字体层级和 accessibility audit | 直接执行 | 无 / `$0` |
| `test_08_end_to_end.py` | 八个 `animated-explainer` 阶段、artifact schema、checkpoint、cost tracking、真实 `AudioMixer` + `VideoCompose` | 直接执行 | 无 / `$0` |
| `test_09_hyperframes_compose.py` | `HyperFramesCompose` 的 workspace scaffold、lint、browser validate 和可选真实 render | `pytest`，环境变量启用 | 无 API key / 首次运行需网络下载 npm 与浏览器依赖 |

脚本 `test_01_tts.py`、`test_02_image_gen.py` 和 `test_03_music.py` 当前不在仓库中，不属于本计划的可运行集合。

## 运行测试

先运行本地且无网络依赖的 QA 脚本：

```bash
python tests/qa/test_04_audio_mix.py
python tests/qa/test_05_video_compose.py
python tests/qa/test_06_video_stitch.py
python tests/qa/test_07_playbook_intelligence.py
python tests/qa/test_08_end_to_end.py
```

`test_04`、`test_05`、`test_06` 会把 fixture 和结果写入已被 gitignore 的 `tests/qa/output/`。`test_08` 每次运行会重新创建 `tests/qa/output/e2e_pipeline/` 和 `tests/qa/output/e2e_assets/`，最终视频为 `tests/qa/output/e2e_final_output.mp4`。

HyperFrames scaffold、lint 和 validate 是显式 opt-in：

```bash
HYPERFRAMES_QA=1 python -m pytest tests/qa/test_09_hyperframes_compose.py -q
```

同时启用真实 render：

```bash
HYPERFRAMES_QA=1 HYPERFRAMES_QA_RENDER=1 python -m pytest tests/qa/test_09_hyperframes_compose.py -q
```

未设置 `HYPERFRAMES_QA` 时，`test_09_hyperframes_compose.py` 会被跳过。

## 检查协议

1. **脚本结果**：确认进程无 traceback；所有 `ToolResult` 输出均为 `Success: True`；`test_07` 与 `test_08` 的汇总均为 `0 failed`。`test_04`–`test_08` 主要打印结果，不会为每个打印出的失败自动生成 pytest assertion，因此不能只看进程退出码。
2. **音频文件**：检查 `ffprobe` 的时长、采样率、声道和 codec，再实际试听。确认 speech 清晰、淡入淡出自然、ducking 平滑且没有 clipping。
3. **视频文件**：检查分辨率、fps、时长、codec 和音轨，再实际观看。确认 A/V sync、片段顺序、transition、字幕、overlay 与 spatial layout 正确。
4. **Playbook**：确认所有已发现的 shipped playbook 通过 accessibility audit；故意构造的低对比度 playbook 必须被识别为错误。
5. **HyperFrames**：确认新 scaffold 能通过 lint，validate 实际生成报告；真实 render 启用时，输出必须是可由 `ffprobe` 读取且含视频流的 MP4。

## 已知风险

| 区域 | 风险 | 验证方式 |
|---|---|---|
| 音频 ducking | 音乐压低过强、恢复不自然或出现 clipping | 试听 `mix_ducked.wav`，结合脚本打印的 LUFS、dBTP 和 LRA |
| 字幕烧录 | 字体可用性和平台差异导致排版变化 | 观看 `compose_subtitled.mp4` 与 `compose_burn_subs.mp4` |
| 视频拼接 | 不同分辨率、fps 或 codec 的片段可能产生 transition 或同步问题 | 比较 compatibility 检查与 `stitch_normalized.mp4`，观看所有 stitch 输出 |
| E2E 状态 | artifact、checkpoint、stage 顺序或 cost snapshot 发生漂移 | 确认 `test_08` 的 schema 与最终阶段检查全部 PASS |
| HyperFrames 冷启动 | 首次 `npx` 与浏览器下载较慢，离线环境无法解析 npm 包 | 先运行 `make hyperframes-doctor`，再执行 opt-in 测试 |
| 缓存 fixture | `test_04`–`test_06` 会复用已经存在的输出，旧文件可能掩盖 fixture 生成变化 | 需要验证 fixture 生成逻辑时，先检查 `tests/qa/output/` 的内容和时间戳 |

## 成功标准

- [ ] `test_04` 的四个音频结果均成功生成，格式信息可读，试听无明显失真。
- [ ] `test_05` 的五个视频结果均成功生成，字幕、编码与 overlay 符合脚本参数。
- [ ] `test_06` 正确识别匹配与不匹配片段，八个视频输出均可播放。
- [ ] `test_07` 对 shipped playbook 的检查全部通过，并能拒绝低对比度 fixture。
- [ ] `test_08` 完成八个阶段，所有 canonical artifact 可读，最终视频同时包含音频流和视频流。
- [ ] 启用 `HYPERFRAMES_QA` 时，scaffold、lint 和 validate 测试通过；启用 `HYPERFRAMES_QA_RENDER` 时真实 MP4 render 也通过。
- [ ] 所有需要人工检查的音频和视频均已实际试听或观看。

## 编写新的 QA 测试

- 使用 `test_NN_description.py` 命名，并把可保留的本地结果写入 `tests/qa/output/`。
- fixture 应尽量由 FFmpeg 或测试代码自行生成，不依赖已删除的旧脚本或真实 API key。
- 调用工具时使用 `Tool.execute({...})`，并检查 `ToolResult.success`、`error`、`data` 和 artifact 路径。
- 新的自动化 gate 应写成 pytest test function 并使用 assertion；不要只打印失败信息。
- 媒体测试必须保留 `ffprobe` 检查，同时明确需要人工试听或观看的项目。

## 覆盖率与 CI

仓库当前没有配置 coverage threshold。

GitHub Actions 的 `.github/workflows/ci.yml` 在向 `main` push 或发起针对 `main` 的 pull request 时运行 `Validate Python` job：安装 Python `3.11` 与 FFmpeg，执行 `make install-dev`、`make lint` 和 `make test`。`make test` 运行 `python -m pytest tests/ -v`；在 CI 未设置 HyperFrames opt-in 环境变量时，`test_09_hyperframes_compose.py` 默认跳过深度检查。
