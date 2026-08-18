<!-- generated-by: gsd-doc-writer -->
# Ink Theater

**简体中文（主文档）** · [英文副本](README.en.md)

一个确定性、可安全跳转的手绘**“动态艺术”**引擎——在极简的白底黑墨世界里，一个面无表情的吉祥物通过操作荒诞的低技术装置，亲自*演绎*抽象概念。它为 OpenMontage 的 **atelier** 路径打造，并通过 **HyperFrames** 渲染（HTML/SVG/CSS + 一条暂停的 GSAP 时间线 → MP4）。

灵感来自 Ian 的 `小黑 / Xiaohei` 插画技能（MIT——相关技法归功于 Ian）；这是一个原创、通用、以英文为默认内容且动画优先的引擎，并非复刻。

## 存在的意义

这种插画风格足够简洁，**插画本身就是动画**——无需扩散模型。矢量形状 + 数学就能构成完整作品：免费、确定、可无限编辑，而且角色会真正把概念表演出来。该引擎将研究成果（`memory: project_ink_atelier_animation`，以及关于矢量、物理和隐喻基础的深度研究）转化为可复用的原语。

## 五项能力（`ink-theater.js`，全局对象 `InkTheater`）

| 模块 | 功能 | 关键 API |
|---|---|---|
| **墨线** | 自信的手绘线条——可变宽度的笔刷带 + 摇曳的中心线 | `inkPath(pts, opt)`, `inkRibbon(pts, {width,taper,seed})` |
| **线条沸动** | 可安全跳转的手绘线条“沸动”——沿时间线分步切换 `feTurbulence` seed（约 9fps），而非 SMIL | `boil(turbEl, tl, {duration,fps})` |
| **弹簧物理** | 闭式阻尼弹簧缓动（预备/过冲/稳定）——完全由进度决定的纯函数，可安全跳转 | `springEase({stiffness,damping,mass})`, `ease.{settle,overshoot,bouncy,soft}` |
| **骨架 / IK** | 2D FABRIK 逆向运动学 + 可绑定骨架的吉祥物，双臂可伸向目标 | `fabrik(lengths,origin,target)`, `mascot({x,y,scale})` → `.reachL/.reachR([x,y])` |
| **装置语法** | 参数化、可组合的机器部件 | `parts.{crank,gauge,hopper,slot,lever,box}` |

## 确定性（HyperFrames 渲染契约）

每一帧都必须能仅由时间重现。该引擎通过以下方式遵守此契约：

- **闭式弹簧**——`springEase` 计算解析形式的阻尼振荡器阶跃响应，因此任意进度 `p` 都能确定性映射（无数值积分、无状态累积）。
- **可安全跳转的线条沸动**——由时间线上的 GSAP 分步 seed 补间驱动，绝不使用 SMIL / 渲染时钟。
- **通过 `onUpdate` 跟随 IK**——手臂姿态取决于位置由时间线设置的目标；GSAP 在跳转时会触发 `onUpdate`，因此它是时间的纯函数。
- 所有“看似随机”的摇曳均使用带 seed 的 PRNG（`rng`）——运行时不使用 `Math.random`。
- 不使用 `repeat:-1`（仅有限次数），且只动画化 transform/opacity/attrs。

## ⚠ 字体陷阱（真正的根因）

长期以来，自定义手写字体在每次渲染中都显示成**衬线体**。根因**并非** SVG 与 HTML 的差异，而是**字体子集陷阱**：从 Google Fonts `css2` API 只抓取一个 woff2（`grep … | head -1`），拿到的是单个 *unicode-range 子集*（通常为 cyrillic / vietnamese / latin-ext），其中**不包含 basic-latin（ASCII）**。因此每个英文单词都会静默回退为衬线体——即使渲染器仍然记录 `Fonts: 1 loaded`。（这意味着早期演示里那些“看起来像手写”的字幕其实是衬线体。）

**修复方式（已验证）：**嵌入**完整字体文件**——TrueType，或确实覆盖 basic-latin 的 woff2：

```html
@font-face { font-family: "InkHand"; src: url("assets/patrickhand.ttf") format("truetype"); font-display: block; }
```

可用的 Patrick Hand TTF 随项目提供，路径为 **`ink-theater/assets/patrickhand.ttf`**（SIL Open Font License——许可证文件位于同目录的 `assets/OFL.txt`；另见 `THIRD_PARTY_NOTICES.md`）——将其复制到项目的 `assets/`，并使用 `font-family: "InkHand"`。它能在普通的 **HTML 叠加层 `<div>`** 上渲染真正的手写体（已验证——将字幕 div 放在 SVG 场景之上）。不要热链接 Google Fonts（渲染时网络请求会破坏确定性）；本地 `@font-face` 文件会在构建时由编译器自动内联。

> 注意：HyperFrames 还预置了约 18 种字体（均非手写体）——参见 `hyperframes-creative/references/typography.md`。若要使用手写体，必须像上面一样嵌入自己的完整字体。

## 在 HyperFrames 项目中使用

1. 将 `ink-theater.js` 复制到项目根目录；在 gsap 之后引入 `<script src="ink-theater.js">`。
2. 以编程方式在挂载点 `<g>` 内构建场景，并保留节点引用。
3. 对墨线组应用 `filter="url(#boil)"`；调用一次 `InkTheater.boil(...)`。
4. 字幕 = HTML 叠加层 div（参见上面的字体陷阱）。
5. 在 `window.__timelines["<id>"]` 上注册一条 `gsap.timeline({paused:true})`。

## Ink Puppet——手绘人物的真正动捕（角色动画推荐方案）

为涂鸦*角色*制作动画（行走 / 跳舞 / 挥手 / 跳跃）的正确方式**不是**手工调数学参数，而是将**真实动作捕捉重定向到火柴人**。智能体只应选择角色并编排具名动作，绝不能手调运动。系统包含两部分：

- **`mocap/bvh2clip.mjs`**——离线转换器：将 3D BVH 动捕文件转换为紧凑的 2D“片段”（逐帧关节轨迹、相对髋部的姿态 + 根运动，并缩放到固定人物高度）。每个动作只需运行一次；将片段与 `clips.js` 一起打包。
- **`ink-puppet.js`**——运行时：构建火柴人、播放片段，并提供**声明式编舞 API**：

```js
var p = InkPuppet.create(mount, { cx: 960, ground: 902, boil: "boil" });
p.drawIn(tl, { start: 0.4 });                         // pencil sketches the figure limb-by-limb
InkPuppet.choreograph(tl, p, [                          // then plays named mocap clips — zero hand-tuning
  { clip: "walk" }, { clip: "dance_spin" }, { clip: "kick" }, { clip: "wave" }
], { start: 3.7 });

// speak — comic balloon tethered to the mouth (HTML text = webfont works)
InkTheater.balloon(tl, { into: fxGroup, overlay: htmlOverlay, at: 5, dur: 2, text: "hello!", boil: "boil" });
```

确定且可安全跳转（姿态是各片段局部时间的纯函数）。

**动作库（`mocap/catalog.json`）**随附 12 个各具特色、可由智能体按名称选择的动作——移动（`walk`、`run`、`climb`、`march`、`shuffle`）、动作（`jump`、`kick`）、姿态（`sit`）、手势（`wave`）、舞蹈（`dance_spin`、`dance_glide`、`twist`）。所有片段均来自 CMU（可免费用于任何用途）。**请阅读目录并选择符合故事的动作——不要只循环一个片段。**

**一条命令即可扩展**（自扩展，无需修改代码）——转换器会自动映射 fair1 / CMU / Mixamo 骨架：

```
node mocap/add-motion.mjs backflip 05_20 dance "a backflip"   # CMU id, or a URL, or a local .bvh
```

免费的 **CMU mocap**（`una-dinosauria/cmu-mocap`）包含数千个动作。这也是 Meta 的 *Animated Drawings* 所采用的方式，但这里始终保持**矢量、白墨风格，并带有绘制显现效果**（AD 为栅格、仅支持类人形，且没有显现过程）。来源说明（所有片段均来自 CMU，可免费用于任何用途）：`mocap/NOTE.md` · `THIRD_PARTY_NOTICES.md`。

### 对话气泡——`InkTheater.balloon(tl, opts)`

从嘴部生长出来的漫画气泡，文字使用 HTML 叠加层（因此 webfont 可以生效）。`opts`：`into`（一个 SVG `<g>`）、`overlay`（一个 HTML div）、`at`、`dur`、`text`、`mouth:[x,y]`、`center:[x,y]`、`w`、`size`、`boil`。

## 演示

- `examples/mocap-figure/`——铅笔人物先绘制出自身，再通过**真实 CMU 动捕**行走 / 奔跑 / 跳舞 / 踢腿 / 坐下 / 挥手。示例自包含且可执行 lint（`npx hyperframes lint ink-theater/examples/mocap-figure`）；参见 `examples/README.md`。
