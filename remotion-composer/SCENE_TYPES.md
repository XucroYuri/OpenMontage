<!-- generated-by: gsd-doc-writer -->
> 简体中文（主文档） | [English copy](SCENE_TYPES.en.md)

# Remotion Composer 场景与叠加层速查

本文档是 `Explainer` composition 接受的 `cut.type` 与 `overlay.type` 权威清单。每一行都对应 `src/Explainer.tsx` 中的实际分发分支。

`Cut` 的基础字段是 `id`、`source`、`in_seconds` 和 `out_seconds`。组件场景仍需携带这些字段；不使用媒体源时，`source` 可以是空字符串。下表中的“必需字段”仅列出命中该组件分支所需的额外字段。

## 场景类型（`cut.type`）

| `type` | 组件 | 必需字段 | 常用字段 | 用途 |
|---|---|---|---|---|
| *省略，视频源* | `OffthreadVideo` | `source`（视频路径） | `source_in_seconds`, `animation`, `transition_in`, `transition_out`, `transition_duration` | 直接播放视频片段 |
| *省略，图片源* | `Img` | `source`（图片路径） | `animation` | 播放带相机运动的静态图 |
| `text_card` | `TextCard` | `text` | `fontSize`, `backgroundImage`, `backgroundVideo`, `backgroundOverlay`, `color` | 大字号文字节拍 |
| `hero_title` | `HeroTitle` | `text` | `heroSubtitle`, `subtitle`, `backgroundImage`, `backgroundVideo` | 标题卡或结尾卡 |
| `stat_card` | `StatCard` | `stat` | `subtitle`, `accentColor`, `backgroundVideo` | 单个突出数字 |
| `callout` | `CalloutBox` | `text` | `callout_type`（`info`, `warning`, `tip`, `quote`）, `title`, `backgroundVideo` | 带标题或项目符号的强调框 |
| `comparison` | `ComparisonCard` | `leftLabel`, `leftValue`, `rightLabel`, `rightValue` | `title`, `backgroundColor` | 左右并列对比 |
| `bar_chart` | `BarChart` | `chartData` | `title`, `chartColors`, `chartAnimation`, `showValues`, `showGrid` | 动画柱状图 |
| `line_chart` | `LineChart` | `chartSeries` | `title`, `chartColors`, `chartAnimation`, `xLabel`, `yLabel`, `showMarkers`, `showLegend` | 动画折线图 |
| `pie_chart` | `PieChart` | `chartData` | `title`, `chartColors`, `chartAnimation`, `donut`, `centerLabel`, `centerValue`, `showLegend` | 饼图或环形图 |
| `kpi_grid` | `KPIGrid` | `chartData` | `title`, `columns`, `chartColors`, `chartAnimation` | 2–4 列 KPI 网格 |
| `progress_bar` | `ProgressBar` | `progress` | `title`, `progressLabel`, `progressColor`, `progressAnimation`, `progressSegments` | 动画进度条 |
| `anime_scene` | `AnimeScene` | `images`（非空列表） | `animation`, `particles`, `particleColor`, `particleCount`, `particleIntensity`, `lightingFrom`, `lightingTo`, `vignette` | 带粒子、光照与相机运动的多图场景 |
| `terminal_scene` | `TerminalScene` | `steps` | `terminalTitle`, `prompt`, `accentColor`, `backgroundColor` | 确定性的合成终端动画；参见 [synthetic-screen-recording skill](../.agents/skills/synthetic-screen-recording/SKILL.md) |
| `screenshot_scene` | `ScreenshotScene` | `backgroundImage`, `screenshotSteps` | `screenshotSize`, `cursorStartAt`, `accentColor` | 在静态截图上按脚本绘制光标、点击、输入、气泡、高亮与标注；参见 [`ScreenshotScene.tsx`](src/components/ScreenshotScene.tsx) |

媒体源通过 `src/lib/resolveAsset.ts` 解析：HTTP(S)、`data:`、绝对文件路径以及 `public/` 下的相对资源都受支持。

## 数据字段速查

图表数据结构与组件接口保持一致：

```ts
// bar_chart
chartData: Array<{ label: string; value: number }>;

// pie_chart
chartData: Array<{ label: string; value: number; color?: string }>;

// line_chart
chartSeries: Array<{
  label: string;
  data: Array<{ x: number; y: number }>;
  color?: string;
}>;

// kpi_grid
chartData: Array<{
  label: string;
  value: number;
  prefix?: string;
  suffix?: string;
  change?: number;
  icon?: string;
}>;
```

`terminal_scene` 的 `steps` 使用以下精确类型：

```ts
type TerminalStep =
  | { kind: "cmd"; text: string; typeSpeed?: number; holdSeconds?: number }
  | { kind: "out"; text: string; holdSeconds?: number }
  | { kind: "pause"; seconds: number }
  | { kind: "pill"; text: string; color?: string; durationSeconds?: number };
```

`screenshot_scene` 的 `screenshotSteps` 支持以下 `kind`：

```ts
type ScreenshotStep =
  | { kind: "cursor_move"; to: [number, number]; durationSeconds?: number }
  | { kind: "click_pulse"; at?: [number, number]; durationSeconds?: number; color?: string }
  | { kind: "type_into"; region: Region; text: string; typeSpeed?: number; fontSize?: number; color?: string }
  | { kind: "bubble_append"; region: Region; text: string; role?: "user" | "assistant"; durationSeconds?: number; stream?: boolean; fontSize?: number }
  | { kind: "typing_dots"; at: [number, number]; durationSeconds?: number; color?: string }
  | { kind: "highlight_box"; region: Region; durationSeconds?: number; color?: string; pulses?: number }
  | { kind: "callout_balloon"; anchor: [number, number]; text: string; position?: "top" | "bottom" | "left" | "right"; durationSeconds?: number; color?: string }
  | { kind: "pause"; seconds: number };

type Region = { x: number; y: number; w: number; h: number };
```

截图坐标均使用 `0`–`1` 归一化值，并相对于 contain-fit 后的图片矩形计算，而不是相对于整个画布。

## 叠加层类型（`overlay.type`）

每个叠加层还需要 `in_seconds` 和 `out_seconds`。

| `type` | 组件 | 必需字段 | 常用字段 | 用途 |
|---|---|---|---|---|
| `section_title` | `SectionTitle` | `text` | `subtitle`, `accentColor`, `position` | 小型章节标签 |
| `stat_reveal` | `StatReveal` | `text` | `subtitle`, `accentColor`, `position` | 角落数据徽章 |
| `hero_title` | `HeroTitle` | `text` | `subtitle` | 全画幅标题叠加层 |
| `provider_chip` | `ProviderChip` | `providers`（字符串列表） | `cycleSeconds`, `position`, `accentColor`, `label` | 按固定节奏轮换 provider 名称的徽章 |

## 添加新场景类型

1. 在 `src/components/MyScene.tsx` 创建 React 组件。动画应由 `useCurrentFrame()`、`useVideoConfig()`、`interpolate(...)` 和 `spring(...)` 驱动。
2. 在 `src/components/index.ts` 导出组件和需要公开的类型。
3. 在 `src/Explainer.tsx` 的 `Cut` interface 中添加新 prop 字段。`type` 当前是 `string`，无需另建枚举值。
4. 在 `SceneRenderer` 添加分发分支：

   ```tsx
   if (cut.type === "my_scene" && cut.mySceneData) {
     return maybeWrapWithBg(<MyScene ... />);
   }
   ```

5. 在本文档中补充新 `cut.type`、必需字段和数据结构，使其可被调用方发现。

现有合成 UI 组件包括 `TerminalScene` 和 `ScreenshotScene`。新增同类组件时，应继续使用按帧推进的步骤列表，避免 CSS transition 或 CSS animation 导致渲染不确定。
