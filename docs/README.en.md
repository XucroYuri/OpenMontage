# OpenMontage Documentation

> [简体中文（主文档）](README.md) | English copy

The repository uses Chinese-first documentation for human-facing project guides. The unsuffixed path is the primary Simplified Chinese document, while the original English text is retained beside it as `*.en.md`.

## Getting started

- [Project overview and quick start](../README.en.md)
- [Prompt gallery](../PROMPT_GALLERY.en.md)
- [Contributing guide](../CONTRIBUTING.en.md)
- [Providers, setup, pricing, and capabilities](PROVIDERS.en.md)
- [Apple Silicon MPS setup](apple-silicon-mps.en.md)

## Architecture and development

- [Architecture](ARCHITECTURE.en.md)
- [Pull request review guide](PR_REVIEW_GUIDE.en.md)
- [Pull request template](../.github/PULL_REQUEST_TEMPLATE.en.md)
- [ComfyUI adapter plan](comfyui-adapter-plan.en.md)
- [Sponsor maintenance](SPONSORS.en.md)
- [Backlot production board](../backlot/README.en.md)
- [Ink Theater](../ink-theater/README.en.md)
- [Ink Theater examples](../ink-theater/examples/README.en.md)
- [Ink Puppet mocap notes](../ink-theater/mocap/NOTE.en.md)
- [Ink Theater third-party notices](../ink-theater/THIRD_PARTY_NOTICES.md)
- [Remotion scene types](../remotion-composer/SCENE_TYPES.en.md)
- [QA plan](../tests/qa/QA_PLAN.en.md)
- [Codex prompt entry point](../.codex/prompts/README.en.md)

## Runtime-contract exception

`AGENT_GUIDE.md`, `PROJECT_CONTEXT.md`, assistant entry files, skills, schemas, pipeline manifests, commands, paths, keys, enum values, provider/model names, and other machine-facing contracts keep their canonical identifiers. Their Chinese companion documents are for human understanding and do not replace the English runtime contract. This exception prevents localization from changing routing, tools, prompts, quality gates, or provider behavior.

When updating documentation, keep the language links, relative paths, code fences, tables, commands, and machine identifiers synchronized. Resolve factual conflicts against the live code, schemas, registry, and pipeline manifests.
