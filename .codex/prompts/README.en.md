<!-- generated-by: gsd-doc-writer -->
> [简体中文（主文档）](README.md) | English copy

# Codex custom prompt entry points

This directory keeps OpenMontage's reusable Codex custom prompts under version control. Codex does not automatically load project-level `.codex/prompts/`; custom prompts must be installed in the user-level `~/.codex/prompts/` directory.

> Codex has deprecated custom prompts. Prefer skills for new reusable workflows; this directory remains the compatibility source for the existing entry points. See the [official OpenAI Custom Prompts documentation](https://learn.chatgpt.com/docs/custom-prompts).

## Available prompts

| File | Invocation | Purpose |
|---|---|---|
| `ink-art.md` | `/prompts:ink-art` | Create a vector ink animation from scratch or animate an Ink Puppet character with mocap |
| `animated-drawing.md` | `/prompts:animated-drawing` | Animate an existing humanoid drawing or photo as raster output with Meta AnimatedDrawings |
| `backlot.md` | `/prompts:backlot` | Open a project's Backlot production board or the project library |

## Installation

Run from the repository root:

```bash
mkdir -p ~/.codex/prompts
cp .codex/prompts/ink-art.md .codex/prompts/animated-drawing.md .codex/prompts/backlot.md ~/.codex/prompts/
```

Alternatively, create symbolic links so repository edits propagate automatically:

```bash
mkdir -p ~/.codex/prompts
ln -s "$PWD/.codex/prompts/ink-art.md" ~/.codex/prompts/ink-art.md
ln -s "$PWD/.codex/prompts/animated-drawing.md" ~/.codex/prompts/animated-drawing.md
ln -s "$PWD/.codex/prompts/backlot.md" ~/.codex/prompts/backlot.md
```

After installing or editing a file, restart the Codex CLI session; reload the extension when using the IDE integration. Type `prompts:` in the `/` menu to filter these commands.

## Invocation examples

```text
/prompts:ink-art A hand-drawn ink character outlines itself, waves, and dances
/prompts:animated-drawing assets/character.png motion=wave
/prompts:backlot backlot-demo-run
```

`$ARGUMENTS` in each prompt receives everything after the command name; keep that placeholder unchanged.
