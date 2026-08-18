"""Backlot CLI.

    python -m backlot open [project-id]   # start server if needed, open browser
    python -m backlot serve [--port N]    # run the server in the foreground

``open`` is idempotent and non-fatal by design: agents call it at pipeline
initialization and must continue the production even if it fails.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.request
import webbrowser

from backlot import DEFAULT_PORT


def _port() -> int:
    try:
        return int(os.environ.get("BACKLOT_PORT", DEFAULT_PORT))
    except ValueError:
        return DEFAULT_PORT


def _server_alive(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=1.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def _spawn_server(port: int) -> None:
    """Start the server as a detached background process."""
    cmd = [sys.executable, "-m", "backlot", "serve", "--port", str(port)]
    if os.name == "nt":
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
            ),
        )
    else:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )


def cmd_open(project_id: str | None) -> int:
    port = _port()
    if not _server_alive(port):
        try:
            _spawn_server(port)
        except Exception as exc:
            print(f"制作看板：无法启动服务（{exc}），将继续执行但不打开看板")
            return 1
        deadline = time.time() + 15
        while time.time() < deadline:
            if _server_alive(port):
                break
            time.sleep(0.4)
        else:
            print("制作看板：服务未能及时启动，将继续执行但不打开看板")
            return 1
    url = f"http://127.0.0.1:{port}/"
    if project_id:
        url = f"http://127.0.0.1:{port}/p/{project_id}"
    try:
        webbrowser.open(url)
    except Exception:
        pass
    print(f"制作看板：{url}")
    return 0


def cmd_serve(port: int) -> int:
    import uvicorn

    uvicorn.run("backlot.server:app", host="127.0.0.1", port=port, log_level="warning")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="backlot",
        description="打开 OpenMontage 制作看板，查看项目、流水线阶段、素材和成片。",
    )
    sub = parser.add_subparsers(dest="command")

    p_open = sub.add_parser("open", help="在浏览器中打开看板（需要时自动启动服务）")
    p_open.add_argument("project_id", nargs="?", default=None, help="可选的项目 ID；省略时打开项目库")

    p_serve = sub.add_parser("serve", help="在前台运行制作看板服务")
    p_serve.add_argument("--port", type=int, default=_port(), help="监听端口")

    args = parser.parse_args(argv)
    if args.command == "open":
        return cmd_open(args.project_id)
    if args.command == "serve":
        return cmd_serve(args.port)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
