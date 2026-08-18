from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import TypedDict, cast

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.tool_registry import registry


CAPABILITY_LABELS = {
    "3d_asset_acquisition": "3D 素材获取",
    "3d_asset_generation": "3D 素材生成",
    "3d_world_generation": "3D 世界生成",
    "3d_world_rendering": "3D 世界渲染",
    "analysis": "媒体分析",
    "audio_processing": "音频处理",
    "avatar": "数字人",
    "character_animation": "角色动画",
    "clip_acquisition": "片段获取",
    "clip_retrieval": "片段检索",
    "corpus_population": "语料入库",
    "enhancement": "画质增强",
    "graphics": "图形制作",
    "image_generation": "图像生成",
    "music_generation": "音乐生成",
    "music_library": "本地音乐库",
    "music_search": "音乐检索",
    "publish": "发布",
    "screen_capture": "屏幕录制",
    "source_ingest": "源素材导入",
    "subtitle": "字幕",
    "tts": "语音合成",
    "video_generation": "视频生成",
    "video_post": "视频后期",
}

RUNTIME_LABELS = {
    "ffmpeg": "FFmpeg",
    "remotion": "Remotion",
    "hyperframes": "HyperFrames",
}


class CapabilitySummary(TypedDict):
    capability: str
    configured: int
    total: int
    available_providers: list[str]


class SetupOfferSummary(TypedDict, total=False):
    capability: str
    tool: str
    env_vars: list[str]


class PreflightSummary(TypedDict):
    composition_runtimes: dict[str, bool]
    capabilities: list[CapabilitySummary]
    setup_offers: list[SetupOfferSummary]
    runtime_warnings: list[str]


def _label(capability: str) -> str:
    return CAPABILITY_LABELS.get(capability, capability)


def format_preflight(summary: PreflightSummary) -> str:
    lines = ["OpenMontage 能力预检", "", "合成引擎："]
    for runtime, available in summary.get("composition_runtimes", {}).items():
        status = "可用" if available else "不可用"
        lines.append(f"  [{status}] {RUNTIME_LABELS.get(runtime, runtime)}")

    lines.extend(["", "能力概览："])
    for item in summary.get("capabilities", []):
        capability = str(item.get("capability", "unknown"))
        configured = int(item.get("configured", 0))
        total = int(item.get("total", 0))
        providers = ", ".join(item.get("available_providers", [])) or "暂无"
        label = _label(capability)
        lines.append(f"  {label} ({capability})：{configured}/{total} 已配置；可用提供商：{providers}")

    grouped: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"tools": set(), "capabilities": set()}
    )
    other_offers = 0
    for offer in summary.get("setup_offers", []):
        env_vars = offer.get("env_vars") or []
        if not env_vars:
            other_offers += 1
            continue
        primary = str(env_vars[0])
        grouped[primary]["tools"].add(str(offer.get("tool", "unknown")))
        grouped[primary]["capabilities"].add(
            _label(str(offer.get("capability", "unknown")))
        )

    lines.extend(["", "快速配置（按环境变量聚合）："])
    if grouped:
        ranked = sorted(
            grouped.items(), key=lambda item: (-len(item[1]["tools"]), item[0])
        )
        for env_var, details in ranked:
            capabilities = "、".join(sorted(details["capabilities"]))
            lines.append(
                f"  {env_var}：可启用 {len(details['tools'])} 个工具（{capabilities}）"
            )
    else:
        lines.append("  没有需要补充环境变量的快速配置项。")
    if other_offers:
        lines.append(f"  另有 {other_offers} 个安装或运行环境配置项。")

    warnings = summary.get("runtime_warnings", [])
    if warnings:
        lines.extend(
            [
                "",
                "运行环境警告：",
                "  部分本地合成能力当前不可用，请运行 make hyperframes-doctor 进一步检查。",
                "  技术原文：",
            ]
        )
        lines.extend(f"    - {warning}" for warning in warnings)

    lines.extend(["", "完整机器可读提供商明细：make preflight-json"])
    return "\n".join(lines)


def main() -> None:
    _ = registry.discover()
    raw_summary = cast(object, registry.provider_menu_summary())
    summary = cast(PreflightSummary, raw_summary)
    print(format_preflight(summary))


if __name__ == "__main__":
    main()
