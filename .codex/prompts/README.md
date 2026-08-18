<!-- generated-by: gsd-doc-writer -->
> 简体中文（主文档） | [英文副本](README.en.md)

# Codex 自定义提示词入口

此目录保存 OpenMontage 的可复用 Codex 自定义提示词，并将它们纳入版本控制。Codex 不会从项目级 `.codex/prompts/` 自动加载这些文件；自定义提示词需要安装到用户级 `~/.codex/prompts/`。

> 自定义提示词已被 Codex 标记为 deprecated。新建可复用工作流时应优先使用 skills；本目录继续保留现有入口的兼容源文件。参见 [OpenAI 官方 Custom Prompts 文档](https://learn.chatgpt.com/docs/custom-prompts)。

## 可用提示词

| 文件 | 调用命令 | 用途 |
|---|---|---|
| `ink-art.md` | `/prompts:ink-art` | 从零创建矢量墨线动画或 Ink Puppet 动捕角色动画 |
| `animated-drawing.md` | `/prompts:animated-drawing` | 使用 Meta AnimatedDrawings 为已有的人形绘画或照片制作栅格动画 |
| `backlot.md` | `/prompts:backlot` | 打开指定项目的 Backlot 制作看板，或打开项目库 |

## 安装

在仓库根目录运行：

```bash
mkdir -p ~/.codex/prompts
cp .codex/prompts/ink-art.md .codex/prompts/animated-drawing.md .codex/prompts/backlot.md ~/.codex/prompts/
```

也可以创建符号链接，让仓库修改自动生效：

```bash
mkdir -p ~/.codex/prompts
ln -s "$PWD/.codex/prompts/ink-art.md" ~/.codex/prompts/ink-art.md
ln -s "$PWD/.codex/prompts/animated-drawing.md" ~/.codex/prompts/animated-drawing.md
ln -s "$PWD/.codex/prompts/backlot.md" ~/.codex/prompts/backlot.md
```

安装或修改文件后，重启 Codex CLI 会话；使用 IDE 扩展时还需重新加载扩展。然后在 `/` 菜单中输入 `prompts:` 过滤这些命令。

## 调用示例

```text
/prompts:ink-art 一名用墨线画成的角色先自我勾勒，再挥手并跳舞
/prompts:animated-drawing assets/character.png motion=wave
/prompts:backlot backlot-demo-run
```

提示词中的 `$ARGUMENTS` 会接收命令名之后的全部参数；不要改写该占位符。
