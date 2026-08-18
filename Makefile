PYTHON_VERSION ?= 3.10
VENV_DIR ?= .venv
BASE_PYTHON ?= $(shell command -v python$(PYTHON_VERSION) 2>/dev/null || command -v python3.14 2>/dev/null || command -v python3.13 2>/dev/null || command -v python3.12 2>/dev/null || command -v python3.11 2>/dev/null || command -v python3 2>/dev/null || command -v python 2>/dev/null)
RUN_PYTHON = $(shell for dir in "$$VIRTUAL_ENV" "$$CONDA_PREFIX" "$(VENV_DIR)"; do if [ -n "$$dir" ] && [ -x "$$dir/bin/python" ]; then printf "%s/bin/python" "$$dir"; exit 0; elif [ -n "$$dir" ] && [ -x "$$dir/Scripts/python.exe" ]; then printf "%s/Scripts/python.exe" "$$dir"; exit 0; fi; done; if [ "$(OS)" = "Windows_NT" ]; then printf "%s/Scripts/python.exe" "$(VENV_DIR)"; else printf "%s/bin/python" "$(VENV_DIR)"; fi)
PIP = $(RUN_PYTHON) -m pip

.DEFAULT_GOAL := setup

.PHONY: setup install install-dev install-gpu test test-contracts lint clean preflight demo demo-list hyperframes-doctor hyperframes-warm venv ensure-venv

# ---- Virtual environment ----

ensure-venv:
	@if [ -n "$$VIRTUAL_ENV" ] && { [ -x "$$VIRTUAL_ENV/bin/python" ] || [ -x "$$VIRTUAL_ENV/Scripts/python.exe" ]; }; then \
		echo "==> 使用当前虚拟环境：$$VIRTUAL_ENV"; \
	elif [ -n "$$CONDA_PREFIX" ] && { [ -x "$$CONDA_PREFIX/bin/python" ] || [ -x "$$CONDA_PREFIX/Scripts/python.exe" ]; }; then \
		echo "==> 使用当前 Conda 环境：$$CONDA_PREFIX"; \
	elif [ -x "$(VENV_DIR)/bin/python" ] || [ -x "$(VENV_DIR)/Scripts/python.exe" ]; then \
		echo "==> 使用已有虚拟环境：$(VENV_DIR)"; \
	elif command -v uv >/dev/null 2>&1; then \
		echo "==> 使用 uv 创建 Python $(PYTHON_VERSION)+ 虚拟环境：$(VENV_DIR)"; \
		uv venv --python $(PYTHON_VERSION) "$(VENV_DIR)"; \
	else \
		if [ -z "$(BASE_PYTHON)" ]; then \
			echo "错误：需要 Python $(PYTHON_VERSION)+，但没有找到 Python 可执行文件。"; \
			exit 1; \
		fi; \
		"$(BASE_PYTHON)" -c "import sys; required=tuple(map(int, '$(PYTHON_VERSION)'.split('.')[:2])); raise SystemExit(0 if sys.version_info[:2] >= required else 1)" || { \
			echo "错误：OpenMontage 需要 Python $(PYTHON_VERSION)+。"; \
			echo "请安装 uv 或 Python $(PYTHON_VERSION)+，然后重新运行 make。"; \
			exit 1; \
		}; \
		echo "==> 使用 Python venv 创建虚拟环境：$(VENV_DIR)"; \
		"$(BASE_PYTHON)" -m venv "$(VENV_DIR)" || { \
			echo "错误：无法创建 $(VENV_DIR)。请安装 uv 或确认 Python 支持 venv。"; \
			exit 1; \
		}; \
	fi
	@$(RUN_PYTHON) -c "import sys; required=tuple(map(int, '$(PYTHON_VERSION)'.split('.')[:2])); raise SystemExit(0 if sys.version_info[:2] >= required else 1)" || { \
		echo "错误：OpenMontage 需要 Python $(PYTHON_VERSION)+。"; \
		echo "当前解释器为 $$($(RUN_PYTHON) -c 'import sys; print(\".\".join(map(str, sys.version_info[:3])))' 2>/dev/null || echo 不可用)：$(RUN_PYTHON)"; \
		echo "请激活兼容环境，或删除当前环境后让 make 重新创建。"; \
		exit 1; \
	}
	@$(RUN_PYTHON) -m pip --version >/dev/null 2>&1 || $(RUN_PYTHON) -m ensurepip --upgrade >/dev/null

venv: ensure-venv
	@echo "==> 虚拟环境已就绪。"
	@echo "    Python：$(RUN_PYTHON)"
	@if [ -z "$$VIRTUAL_ENV" ] && [ -z "$$CONDA_PREFIX" ]; then if [ "$(OS)" = "Windows_NT" ]; then echo "    激活命令：$(VENV_DIR)\\Scripts\\Activate.ps1"; else echo "    激活命令：source $(VENV_DIR)/bin/activate"; fi; fi

# ---- One-command setup ----

setup: ensure-venv
	@echo "==> 正在安装 Python 依赖……"
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "==> 正在安装 Remotion 合成器……"
	cd remotion-composer && npm install
	@echo ""
	@echo "==> 正在安装免费离线语音合成工具 Piper……"
	$(PIP) install piper-tts || echo "  [跳过] Piper 安装失败，语音合成将改用云端提供商"
	@echo ""
	@echo "==> 正在安装 HyperFrames 运行环境（通过 npx 预热缓存）……"
	@echo "    将 hyperframes npm 包写入本地 npx 缓存，避免首次渲染等待 30–60 秒。"
	@echo "    预计占用约 20MB 磁盘空间。"
	@npx --yes hyperframes --version >/dev/null 2>&1 && echo "    HyperFrames CLI 已缓存（npx）" || echo "  [跳过] HyperFrames 缓存预热失败；离线或 npm 不可用时，首次渲染会按需下载"
	@$(RUN_PYTHON) -c "from tools.video.hyperframes_compose import HyperFramesCompose; HyperFramesCompose._npm_resolve_cache=None; c=HyperFramesCompose()._runtime_check(); print(f'    HyperFrames 可用={c[\"runtime_available\"]}，npm={c.get(\"npm_package_version\") or c.get(\"npm_resolve_error\")}'); [print(f'    说明：{r}') for r in c['reasons']]" || echo "  [跳过] HyperFrames 检查失败，可稍后再配置运行环境"
	@echo ""
	$(RUN_PYTHON) -c "import shutil, os; e=os.path.exists('.env'); shutil.copy('.env.example','.env') if not e else None; print('==> 已根据 .env.example 创建 .env，请在其中填写 API 密钥。' if not e else '==> .env 已存在，跳过创建。')"
	@echo ""
	@echo "安装完成！请在 AI 编程助手中打开本项目并开始创作。"
	@echo "  可选：在 .env 中添加 API 密钥以启用云端提供商。"
	@echo "  可选：如果有 NVIDIA GPU，请运行 'make install-gpu'。"
	@echo "  可选：运行 'make hyperframes-doctor' 完整检查 HyperFrames 运行环境。"
	@echo "  可选：运行 'make hyperframes-warm' 将 npx 缓存更新到最新版 HyperFrames。"

# ---- Individual installs ----

install: ensure-venv
	$(PIP) install -r requirements.txt

install-dev: ensure-venv
	$(PIP) install -r requirements-dev.txt

install-gpu: ensure-venv
	$(PIP) install -r requirements-gpu.txt
	$(PIP) install diffusers transformers accelerate

# ---- Testing ----

test: ensure-venv
	$(RUN_PYTHON) -m pytest tests/ -v

test-contracts: ensure-venv
	$(RUN_PYTHON) -m pytest tests/contracts/ -v

# ---- Utilities ----

preflight: ensure-venv
	$(RUN_PYTHON) -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"

hyperframes-doctor: ensure-venv
	@echo "==> 正在检查 HyperFrames 运行环境（Node、FFmpeg、npx 与 HyperFrames doctor）……"
	$(RUN_PYTHON) -c "from tools.video.hyperframes_compose import HyperFramesCompose; r=HyperFramesCompose().execute({'operation':'doctor'}); import json; print(json.dumps(r.data, indent=2)); print('OK' if r.success else f'FAIL: {r.error}')"

hyperframes-warm:
	@echo "==> 正在将 HyperFrames npx 缓存更新到最新版……"
	@echo "    使用 --prefer-online 获取上次运行后发布的新版本。"
	npx --yes --prefer-online hyperframes --version
	@echo "==> 缓存预热完成。"

demo: ensure-venv
	@echo "==> 正在渲染无需 API 密钥的演示视频……"
	@echo "    演示仅使用 Remotion 组件，包括动态图表、文字和数据可视化。"
	@echo ""
	$(RUN_PYTHON) render_demo.py

demo-list: ensure-venv
	$(RUN_PYTHON) render_demo.py --list

lint: ensure-venv
	$(RUN_PYTHON) -m py_compile tools/base_tool.py
	$(RUN_PYTHON) -m py_compile tools/tool_registry.py
	$(RUN_PYTHON) -m py_compile tools/cost_tracker.py
	$(RUN_PYTHON) -m py_compile tools/analysis/composition_validator.py

clean:
	$(BASE_PYTHON) -c "import pathlib, shutil; excluded=[pathlib.Path('$(VENV_DIR)'), pathlib.Path('venv')]; skip=lambda p: any(p == root or root in p.parents for root in excluded); roots=[p for p in pathlib.Path('.').rglob('__pycache__') if not skip(p)]; [shutil.rmtree(p) for p in roots]; files=[p for p in pathlib.Path('.').rglob('*.pyc') if not skip(p)]; [p.unlink() for p in files]"
