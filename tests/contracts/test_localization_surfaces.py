from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml
from dotenv import dotenv_values


REPO_ROOT = Path(__file__).resolve().parents[2]
CHINESE = re.compile(r"[\u3400-\u9fff]")


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
    bug = yaml.safe_load((issue_dir / "bug_report.yml").read_text(encoding="utf-8"))
    feature = yaml.safe_load(
        (issue_dir / "feature_request.yml").read_text(encoding="utf-8")
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
