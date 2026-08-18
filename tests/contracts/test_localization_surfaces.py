from __future__ import annotations

import re
import subprocess
import sys
from hashlib import sha1
from pathlib import Path
from typing import TypedDict, cast

import yaml
from dotenv import dotenv_values
from scripts.preflight_summary import format_preflight


REPO_ROOT = Path(__file__).resolve().parents[2]
CHINESE = re.compile(r"[\u3400-\u9fff]")


class IssueForm(TypedDict):
    name: str
    labels: list[str]
    body: list[dict[str, object]]


def _demo_list(language: str | None = None) -> tuple[str, tuple[str, ...]]:
    command = [sys.executable, "render_demo.py", "--list"]
    if language:
        command.extend(["--lang", language])
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    demo_ids = tuple(
        line.split()[0]
        for line in result.stdout.splitlines()[1:]
        if line.strip()
    )
    return result.stdout, demo_ids


def test_demo_cli_defaults_to_chinese_and_preserves_english_capabilities() -> None:
    default_output, default_ids = _demo_list()
    chinese_output, chinese_ids = _demo_list("zh-CN")
    english_output, english_ids = _demo_list("en")

    assert default_output.startswith("可用的免密钥演示：")
    assert chinese_output.startswith("可用的免密钥演示：")
    assert english_output.startswith("Available zero-key demos:")
    assert default_ids == chinese_ids == english_ids
    assert set(chinese_ids) == {
        "code-to-screen",
        "focusflow-pitch",
        "world-in-numbers",
    }


def test_issue_forms_are_chinese_without_translating_machine_ids() -> None:
    issue_dir = REPO_ROOT / ".github/ISSUE_TEMPLATE"
    bug = cast(
        IssueForm,
        cast(
            object,
            yaml.safe_load(
                (issue_dir / "bug_report.yml").read_text(encoding="utf-8")
            ),
        ),
    )
    feature = cast(
        IssueForm,
        cast(
            object,
            yaml.safe_load(
                (issue_dir / "feature_request.yml").read_text(encoding="utf-8")
            ),
        ),
    )

    assert CHINESE.search(bug["name"])
    assert CHINESE.search(feature["name"])
    assert bug["labels"] == ["bug"]
    assert feature["labels"] == ["enhancement"]
    assert [item["id"] for item in bug["body"] if "id" in item] == [
        "summary",
        "os",
        "pipeline",
        "runtime",
        "repro",
        "expected",
        "actual",
        "logs",
    ]
    assert [item["id"] for item in feature["body"] if "id" in item] == [
        "problem",
        "solution",
        "alternatives",
        "context",
    ]


def test_command_menus_are_chinese_and_keep_canonical_commands() -> None:
    prompt_paths = [
        *(REPO_ROOT / ".claude/commands").glob("*.md"),
        *(REPO_ROOT / ".codex/prompts").glob("*.md"),
        *(REPO_ROOT / ".cursor/commands").glob("*.md"),
        *(REPO_ROOT / ".github/prompts").glob("*.prompt.md"),
    ]
    localized = [
        path
        for path in prompt_paths
        if path.stem.removesuffix(".prompt")
        in {"animated-drawing", "backlot", "ink-art"}
    ]

    assert len(localized) == 12
    for path in localized:
        text = path.read_text(encoding="utf-8")
        assert CHINESE.search(text), path
        if "animated-drawing" in path.name:
            assert "AnimatedDrawings" in text and "/ink-art" in text
        elif "backlot" in path.name:
            assert "python -m backlot open" in text
            assert "projects/<id>/" in text
        else:
            assert "InkPuppet.choreograph" in text
            assert "npx hyperframes lint" in text


def test_environment_example_keeps_keys_unset_with_chinese_guidance() -> None:
    text = (REPO_ROOT / ".env.example").read_text(encoding="utf-8")
    assert "不要提交包含真实密钥的 .env" in text
    values = dotenv_values(REPO_ROOT / ".env.example")
    credential_keys = {
        key
        for key in values
        if key.endswith(("_KEY", "_TOKEN", "_SECRET", "_ACCESSKEY"))
        or key in {"FAL_KEY", "HF_TOKEN", "GOOGLE_APPLICATION_CREDENTIALS"}
    }
    assert credential_keys
    assert all(values[key] in {None, ""} for key in credential_keys)


def test_preflight_summary_is_concise_chinese_without_changing_machine_ids() -> None:
    output = format_preflight(
        {
            "composition_runtimes": {"ffmpeg": True, "remotion": False},
            "capabilities": [
                {
                    "capability": "image_generation",
                    "configured": 1,
                    "total": 3,
                    "available_providers": ["local"],
                }
            ],
            "setup_offers": [
                {
                    "capability": "image_generation",
                    "tool": "provider_a",
                    "env_vars": ["EXAMPLE_API_KEY"],
                },
                {
                    "capability": "video_generation",
                    "tool": "provider_b",
                    "env_vars": ["EXAMPLE_API_KEY"],
                },
            ],
            "runtime_warnings": ["remotion: runtime unavailable"],
        }
    )

    assert "图像生成 (image_generation)：1/3 已配置" in output
    assert "EXAMPLE_API_KEY：可启用 2 个工具" in output
    assert "技术原文：" in output
    assert "remotion: runtime unavailable" in output
    assert "provider_a" not in output
    assert "完整机器可读提供商明细：make preflight-json" in output


def _git_blob_id(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def test_agent_guide_companion_tracks_every_normative_section() -> None:
    source_data = (REPO_ROOT / "AGENT_GUIDE.md").read_bytes()
    source = source_data.decode()
    companion = (REPO_ROOT / "AGENT_GUIDE.zh-CN.md").read_text(encoding="utf-8")
    source_headings = {
        line.lstrip("#").strip()
        for line in source.splitlines()
        if line.startswith("##")
    }

    assert f"对应英文源文件 Blob：`{_git_blob_id(source_data)}`" in companion
    assert all(heading in companion for heading in source_headings)
    assert len(companion.splitlines()) >= len(source.splitlines()) * 0.7
    for identifier in (
        "provider_menu_summary()",
        "human_approval_default",
        "render_runtime_selection",
        "composition_mode",
        "metadata.partial_progress",
        "registry.capability_catalog()",
        "threejs_asset_catalog",
        "blender_world",
    ):
        assert identifier in companion


def test_chinese_primary_docs_follow_the_terminology_contract() -> None:
    terminology = (REPO_ROOT / "docs/TERMINOLOGY.md").read_text(encoding="utf-8")
    for row in (
        "| asset | 素材 |",
        "| artifact | 产物 |",
        "| pipeline | 流水线 |",
        "| checkpoint | 检查点 |",
        "| render runtime | 合成引擎 |",
        "| contact sheet | 候选缩略图总览 |",
    ):
        assert row in terminology

    forbidden = ("资产生成", "规范工件", "逐场景联系表", "video video")
    for relative_path in (
        "README.md",
        "docs/ARCHITECTURE.md",
        "docs/PR_REVIEW_GUIDE.md",
        "PROJECT_CONTEXT.zh-CN.md",
        "AGENT_GUIDE.zh-CN.md",
    ):
        text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert not any(term in text for term in forbidden), relative_path
