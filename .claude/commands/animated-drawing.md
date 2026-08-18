---
description: 使用 Meta AnimatedDrawings 的真实动作捕捉，让用户提供的角色图画/照片动起来并输出光栅 GIF/MP4。若要从零创建矢量涂鸦，请使用 /ink-art。
argument-hint: "[图画路径] [动作: dance|walk|jump|wave]"
---

读取 `skills/creative/animated-drawing.md`，然后配置并运行 Meta 开源的 **AnimatedDrawings**，让用户提供的图画执行指定动作。

- 仅用于用户已经提供人形图画/照片的情况。若要从零创建会自我绘制的矢量涂鸦，请改用 `/ink-art`。
- 输出为**光栅图像**（原图发生形变），不是矢量，也不包含描线显现。请确认输入是浅色纯背景上的单个人形。
- 优先使用内置角色的即用路径；自动绑定路径需要 Docker 和约 670 MB 模型。

图画与动作：$ARGUMENTS
