<!-- generated-by: gsd-doc-writer -->
> [简体中文（主文档）](QA_PLAN.md) | English copy

# QA quality validation plan

## Purpose

`tests/qa/` validates audio mixing, video composition, video stitching, style playbooks, the full `animated-explainer` flow, and the optional HyperFrames composition path. The current scripts use locally generated FFmpeg fixtures, require no API keys, and incur no provider-call cost. Quality conclusions still require reviewing script output and listening to or watching the generated media.

## Test framework and setup

`test_04_audio_mix.py` through `test_08_end_to_end.py` are directly executable QA scripts; their checks run when the modules are imported. `test_09_hyperframes_compose.py` uses `pytest>=8.0` and real assertions.

Install development dependencies from the repository root:

```bash
make install-dev
```

Local test prerequisites are:

- `Python >= 3.10`; CI uses Python `3.11`.
- `ffmpeg` and `ffprobe` on `PATH`.
- HyperFrames QA additionally requires Node.js `>=22`, `npx`, FFmpeg, and a resolvable `hyperframes` npm package. Run `make hyperframes-doctor` first.

## Available tests

| Script | Coverage | Runner | API key / cost |
|---|---|---|---|
| `test_04_audio_mix.py` | `AudioMixer` `mix`, fades, `duck`, delayed music, and `ffprobe`/loudness output | Direct execution | None / `$0` |
| `test_05_video_compose.py` | `VideoCompose` cuts + audio, subtitle composition, standalone subtitle burn, `YOUTUBE_LANDSCAPE` encoding, and image overlay | Direct execution | None / `$0` |
| `test_06_video_stitch.py` | `VideoStitch` compatibility checks, cut/crossfade/fade, `auto_normalize`, preview, and three spatial layouts | Direct execution | None / `$0` |
| `test_07_playbook_intelligence.py` | Loading, contrast, harmony, color-vision safety, type hierarchy, and accessibility audit for every discovered playbook | Direct execution | None / `$0` |
| `test_08_end_to_end.py` | Eight `animated-explainer` stages, artifact schemas, checkpoints, cost tracking, and real `AudioMixer` + `VideoCompose` execution | Direct execution | None / `$0` |
| `test_09_hyperframes_compose.py` | `HyperFramesCompose` workspace scaffold, lint, browser validation, and optional real rendering | `pytest`, enabled by environment variables | No API key / first run downloads npm and browser dependencies over the network |

`test_01_tts.py`, `test_02_image_gen.py`, and `test_03_music.py` are not present in the repository and are not part of the runnable plan.

## Run the tests

Run the local, network-independent QA scripts first:

```bash
python tests/qa/test_04_audio_mix.py
python tests/qa/test_05_video_compose.py
python tests/qa/test_06_video_stitch.py
python tests/qa/test_07_playbook_intelligence.py
python tests/qa/test_08_end_to_end.py
```

`test_04`, `test_05`, and `test_06` write fixtures and results to the gitignored `tests/qa/output/` directory. Each `test_08` run recreates `tests/qa/output/e2e_pipeline/` and `tests/qa/output/e2e_assets/`; its final video is `tests/qa/output/e2e_final_output.mp4`.

HyperFrames scaffold, lint, and validation are explicit opt-ins:

```bash
HYPERFRAMES_QA=1 python -m pytest tests/qa/test_09_hyperframes_compose.py -q
```

Enable the real render as well:

```bash
HYPERFRAMES_QA=1 HYPERFRAMES_QA_RENDER=1 python -m pytest tests/qa/test_09_hyperframes_compose.py -q
```

Without `HYPERFRAMES_QA`, `test_09_hyperframes_compose.py` is skipped.

## Inspection protocol

1. **Script results:** confirm there is no traceback, every `ToolResult` prints `Success: True`, and the `test_07` and `test_08` summaries report `0 failed`. `test_04` through `test_08` primarily print results and do not turn every printed failure into a pytest assertion, so the process exit code alone is insufficient.
2. **Audio:** inspect duration, sample rate, channels, and codec with `ffprobe`, then listen. Speech should be clear, fades natural, ducking smooth, and the output free from clipping.
3. **Video:** inspect resolution, fps, duration, codec, and audio streams, then watch the files. Verify A/V sync, clip order, transitions, subtitles, overlays, and spatial layouts.
4. **Playbooks:** every discovered shipped playbook should pass its accessibility audit, while the deliberately low-contrast playbook must be reported as invalid.
5. **HyperFrames:** a fresh scaffold must lint, browser validation must produce a report, and an enabled real render must create an MP4 with a video stream readable by `ffprobe`.

## Known risks

| Area | Risk | Validation |
|---|---|---|
| Audio ducking | Music attenuation may be too strong, recover poorly, or clip | Listen to `mix_ducked.wav` and review the printed LUFS, dBTP, and LRA values |
| Subtitle burn | Font availability and platform differences may change layout | Watch `compose_subtitled.mp4` and `compose_burn_subs.mp4` |
| Video stitching | Mixed resolution, fps, or codec can cause transition and sync defects | Compare compatibility output with `stitch_normalized.mp4` and watch every stitch result |
| E2E state | Artifact, checkpoint, stage-order, or cost-snapshot contracts can drift | Require every `test_08` schema and final-stage check to pass |
| HyperFrames cold start | First-time `npx` and browser downloads are slow; offline environments cannot resolve the npm package | Run `make hyperframes-doctor` before the opt-in test |
| Cached fixtures | `test_04` through `test_06` reuse existing outputs, which can hide fixture-generation changes | Inspect the contents and timestamps under `tests/qa/output/` when validating fixture creation |

## Success criteria

- [ ] All four `test_04` audio results are created, probe cleanly, and have no obvious audible distortion.
- [ ] All five `test_05` video results are created, with subtitles, encoding, and overlay matching the script inputs.
- [ ] `test_06` distinguishes matching and mismatched clips, and all eight video outputs play correctly.
- [ ] `test_07` passes every shipped playbook check and rejects the low-contrast fixture.
- [ ] `test_08` completes eight stages, every canonical artifact is readable, and the final video has both audio and video streams.
- [ ] With `HYPERFRAMES_QA`, scaffold, lint, and validation pass; with `HYPERFRAMES_QA_RENDER`, the real MP4 render also passes.
- [ ] Every media artifact marked for human inspection has actually been listened to or watched.

## Write a new QA test

- Use the `test_NN_description.py` naming convention and write persistent local results under `tests/qa/output/`.
- Prefer self-generated FFmpeg or code fixtures; do not depend on removed scripts or real API keys.
- Invoke tools with `Tool.execute({...})` and inspect `ToolResult.success`, `error`, `data`, and artifact paths.
- Implement new automated gates as pytest test functions with assertions; do not only print failures.
- Keep `ffprobe` checks for media tests and explicitly list the artifacts that require human listening or viewing.

## Coverage and CI

No coverage threshold is currently configured.

GitHub Actions workflow `.github/workflows/ci.yml` runs the `Validate Python` job on pushes to `main` and pull requests targeting `main`. It installs Python `3.11` and FFmpeg, then runs `make install-dev`, `make lint`, and `make test`. `make test` executes `python -m pytest tests/ -v`; because CI does not set the HyperFrames opt-in variables, the deep checks in `test_09_hyperframes_compose.py` are skipped by default.
