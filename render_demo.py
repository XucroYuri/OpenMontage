"""Render the curated zero-key Remotion demos.

This script is Remotion-specific by design — the demos live in
`remotion-composer/public/demo-props/` as JSON props for existing React
scene components. It is NOT a cross-runtime demo harness.

For a HyperFrames demo, run `make hyperframes-doctor` to verify the runtime
floor, then either scaffold a real composition via `npx hyperframes init`
or drive `hyperframes_compose` from the Agent SDK. HyperFrames demos are
authored as HTML + GSAP in a project workspace, not as JSON props here.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from lib.config_model import OpenMontageConfig


ROOT_DIR = Path(__file__).resolve().parent
COMPOSER_DIR = ROOT_DIR / "remotion-composer"
PROPS_DIR = COMPOSER_DIR / "public" / "demo-props"
OUTPUT_DIR = ROOT_DIR / "projects" / "demos" / "renders"

SUPPORTED_LOCALES = ("zh-CN", "en")

DEMO_DESCRIPTIONS = {
    "zh-CN": {
        "world-in-numbers": "由标题、统计数据和图表构成的全球规模叙事",
        "code-to-screen": "包含对比和 KPI 卡片的开发者工作流讲解",
        "focusflow-pitch": "完全由 Remotion 组件构建的初创产品提案",
    },
    "en": {
        "world-in-numbers": "Global scale story with titles, stats, and charts",
        "code-to-screen": "Developer workflow explainer with comparison and KPI cards",
        "focusflow-pitch": "Startup-style pitch built only from Remotion components",
    },
}

MESSAGES = {
    "zh-CN": {
        "description": "使用仓库内置的 Remotion 参数渲染无需 API 密钥的 OpenMontage 演示视频。",
        "demo_help": "只渲染指定名称的演示；省略时渲染全部演示。",
        "list_help": "列出可用的演示并退出。",
        "lang_help": "界面语言；默认读取 config.yaml 的 interaction.locale。",
        "node_required": "错误：需要 Node.js，请从 https://nodejs.org/ 安装。",
        "npm_required": "错误：需要 npm，但在 PATH 中未找到。",
        "npx_required": "错误：需要 npx，但在 PATH 中未找到。",
        "installing": "正在安装 Remotion 依赖……",
        "cuts_required": "错误：{path} 必须至少定义一个 cut。",
        "rendering": "正在渲染",
        "props": "参数文件",
        "output": "输出文件",
        "done": "完成",
        "missing_output": "渲染已结束，但没有生成预期的输出文件。",
        "no_demos": "错误：在 {path} 中没有找到演示参数文件。",
        "available": "可用的免密钥演示：",
        "fallback_description": "仓库内置的 Remotion 演示",
        "unknown": "未知演示“{name}”。可用演示：{available}",
    },
    "en": {
        "description": "Render zero-key OpenMontage demo videos from checked-in Remotion props.",
        "demo_help": "Render one named demo instead of all demos.",
        "list_help": "List available demo fixtures and exit.",
        "lang_help": "Interface language; defaults to interaction.locale in config.yaml.",
        "node_required": "Error: Node.js is required. Install it from https://nodejs.org/",
        "npm_required": "Error: npm is required but was not found on PATH.",
        "npx_required": "Error: npx is required but was not found on PATH.",
        "installing": "Installing Remotion dependencies...",
        "cuts_required": "Error: {path} must define at least one cut.",
        "rendering": "Rendering",
        "props": "Props",
        "output": "Output",
        "done": "Done",
        "missing_output": "Render finished without creating the expected output file.",
        "no_demos": "Error: No demo prop files were found in {path}.",
        "available": "Available zero-key demos:",
        "fallback_description": "Checked-in Remotion demo",
        "unknown": "Unknown demo '{name}'. Available demos: {available}",
    },
}


def discover_demos() -> dict[str, Path]:
    if not PROPS_DIR.exists():
        return {}
    return {path.stem: path for path in sorted(PROPS_DIR.glob("*.json"))}


def find_command(*names: str) -> str | None:
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def ensure_demo_environment(messages: dict[str, str]) -> str:
    if not find_command("node", "node.exe"):
        raise SystemExit(messages["node_required"])

    npm_cmd = find_command("npm.cmd", "npm", "npm.exe")
    if not npm_cmd:
        raise SystemExit(messages["npm_required"])

    npx_cmd = find_command("npx.cmd", "npx", "npx.exe")
    if not npx_cmd:
        raise SystemExit(messages["npx_required"])

    if not (COMPOSER_DIR / "node_modules").exists():
        print(messages["installing"])
        subprocess.run([npm_cmd, "install"], cwd=COMPOSER_DIR, check=True)

    return npx_cmd


def validate_props_file(path: Path, messages: dict[str, str]) -> None:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload.get("cuts"), list) or not payload["cuts"]:
        raise SystemExit(messages["cuts_required"].format(path=path))


def render_demo(
    name: str,
    props_path: Path,
    npx_cmd: str,
    messages: dict[str, str],
) -> None:
    validate_props_file(props_path, messages)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{name}.mp4"

    print()
    print(f"{messages['rendering']}: {name}")
    print(f"{messages['props']}: {props_path}")
    print(f"{messages['output']}: {output_path}")
    print()

    subprocess.run(
        [
            npx_cmd,
            "remotion",
            "render",
            "src/index.tsx",
            "Explainer",
            str(output_path),
            "--props",
            str(props_path),
            "--codec",
            "h264",
        ],
        cwd=COMPOSER_DIR,
        check=True,
    )

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"{messages['done']}: {output_path} ({size_mb:.1f} MB)")
    else:
        print(messages["missing_output"])


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    default_locale = OpenMontageConfig.load().interaction.locale
    if default_locale not in SUPPORTED_LOCALES:
        default_locale = "en"

    locale_parser = argparse.ArgumentParser(add_help=False)
    locale_parser.add_argument("--lang", choices=SUPPORTED_LOCALES, default=default_locale)
    locale_args, _ = locale_parser.parse_known_args(raw_argv)
    locale = locale_args.lang
    messages = MESSAGES[locale]

    parser = argparse.ArgumentParser(
        description=messages["description"]
    )
    parser.add_argument("demo", nargs="?", help=messages["demo_help"])
    parser.add_argument("--list", action="store_true", help=messages["list_help"])
    parser.add_argument(
        "--lang",
        choices=SUPPORTED_LOCALES,
        default=default_locale,
        help=messages["lang_help"],
    )
    args = parser.parse_args(raw_argv)

    demos = discover_demos()
    if not demos:
        raise SystemExit(messages["no_demos"].format(path=PROPS_DIR))

    if args.list:
        print(messages["available"])
        for name in demos:
            description = DEMO_DESCRIPTIONS[locale].get(
                name, messages["fallback_description"]
            )
            print(f"  {name:20} {description}")
        return 0

    if args.demo and args.demo not in demos:
        available = ", ".join(demos)
        raise SystemExit(messages["unknown"].format(name=args.demo, available=available))

    npx_cmd = ensure_demo_environment(messages)
    selected = {args.demo: demos[args.demo]} if args.demo else demos

    for name, props_path in selected.items():
        render_demo(name, props_path, npx_cmd, messages)

    return 0


if __name__ == "__main__":
    sys.exit(main())
