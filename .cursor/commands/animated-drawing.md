# /animated-drawing：用真实动捕让用户提供的图画动起来

通过 Meta 开源的 AnimatedDrawings，把用户提供的人形图画/照片转成会跳舞、行走、跳跃或挥手的光栅 GIF/MP4。若要从零创建会自我绘制的矢量涂鸦，请使用 `/ink-art`。

读取 `skills/creative/animated-drawing.md`，然后配置并运行 AnimatedDrawings，让用户的图画执行指定动作。

- 仅用于已有的人形图画/照片（单个人形、浅色纯背景）。
- 输出为**光栅图像**（原图发生形变），不是矢量，也不包含描线显现。
- 优先使用内置角色的即用路径；自动绑定需要 Docker 和约 670 MB 模型。
