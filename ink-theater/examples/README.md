<!-- generated-by: gsd-doc-writer -->
# Ink Theater 示例

**简体中文（主文档）** · [英文副本](README.en.md)

## `mocap-figure/`——标准可运行示例

这是一个自包含的 HyperFrames 合成项目：一条铅笔线先**将自己绘制成火柴人**，随后火柴人通过 `InkPuppet.choreograph(...)` 使用**真实 CMU 动作捕捉**（零手工调参）完成行走 / 奔跑 / 跳舞 / 踢腿 / 坐下 / 挥手。

它已打包所需的一切（`ink-theater.js`、`ink-puppet.js`、`clips.js`、`assets/patrickhand.ttf`），因此可以直接执行 lint 和渲染：

```bash
npx hyperframes lint ink-theater/examples/mocap-figure
```

> 请将 linter 指向一个**合成项目目录**（即包含 `index.html` 的目录），而不是 `examples/` 本身——linter 会查找 `index.html`，而 `examples/` 根目录中没有该文件。

要在自己的项目中复用该引擎，请将 `ink-theater.js`（角色动画还需 `ink-puppet.js` 和 `mocap/clips.js`，手写字体还需 `assets/patrickhand.ttf`）复制到项目根目录——参见 [`../README.md`](../README.md)。
