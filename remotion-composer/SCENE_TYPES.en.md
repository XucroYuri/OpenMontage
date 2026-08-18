<!-- generated-by: gsd-doc-writer -->
> [简体中文（主文档）](SCENE_TYPES.md) | English copy

# Remotion Composer scene and overlay cheat sheet

This is the authoritative list of `cut.type` and `overlay.type` values accepted by the `Explainer` composition. Every row maps to an implemented dispatch branch in `src/Explainer.tsx`.

The base `Cut` fields are `id`, `source`, `in_seconds`, and `out_seconds`. Component scenes still carry them; use an empty string for `source` when the scene has no media source. “Required fields” below lists only the additional values needed to enter that component's dispatch branch.

## Scene types (`cut.type`)

| `type` | Component | Required fields | Common fields | Purpose |
|---|---|---|---|---|
| *omitted, video source* | `OffthreadVideo` | `source` (video path) | `source_in_seconds`, `animation`, `transition_in`, `transition_out`, `transition_duration` | Play a video clip directly |
| *omitted, image source* | `Img` | `source` (image path) | `animation` | Show a still image with camera motion |
| `text_card` | `TextCard` | `text` | `fontSize`, `backgroundImage`, `backgroundVideo`, `backgroundOverlay`, `color` | Large-typography beat |
| `hero_title` | `HeroTitle` | `text` | `heroSubtitle`, `subtitle`, `backgroundImage`, `backgroundVideo` | Title or end card |
| `stat_card` | `StatCard` | `stat` | `subtitle`, `accentColor`, `backgroundVideo` | One prominent number |
| `callout` | `CalloutBox` | `text` | `callout_type` (`info`, `warning`, `tip`, `quote`), `title`, `backgroundVideo` | Emphasized box with a title or bullets |
| `comparison` | `ComparisonCard` | `leftLabel`, `leftValue`, `rightLabel`, `rightValue` | `title`, `backgroundColor` | Side-by-side comparison |
| `bar_chart` | `BarChart` | `chartData` | `title`, `chartColors`, `chartAnimation`, `showValues`, `showGrid` | Animated bars |
| `line_chart` | `LineChart` | `chartSeries` | `title`, `chartColors`, `chartAnimation`, `xLabel`, `yLabel`, `showMarkers`, `showLegend` | Animated line chart |
| `pie_chart` | `PieChart` | `chartData` | `title`, `chartColors`, `chartAnimation`, `donut`, `centerLabel`, `centerValue`, `showLegend` | Pie or donut chart |
| `kpi_grid` | `KPIGrid` | `chartData` | `title`, `columns`, `chartColors`, `chartAnimation` | Two-to-four-column KPI grid |
| `progress_bar` | `ProgressBar` | `progress` | `title`, `progressLabel`, `progressColor`, `progressAnimation`, `progressSegments` | Animated progress bar |
| `anime_scene` | `AnimeScene` | `images` (non-empty list) | `animation`, `particles`, `particleColor`, `particleCount`, `particleIntensity`, `lightingFrom`, `lightingTo`, `vignette` | Multi-image scene with particles, lighting, and camera motion |
| `terminal_scene` | `TerminalScene` | `steps` | `terminalTitle`, `prompt`, `accentColor`, `backgroundColor` | Deterministic synthetic terminal animation; see the [synthetic-screen-recording skill](../.agents/skills/synthetic-screen-recording/SKILL.md) |
| `screenshot_scene` | `ScreenshotScene` | `backgroundImage`, `screenshotSteps` | `screenshotSize`, `cursorStartAt`, `accentColor` | Script cursor motion, clicks, typing, bubbles, highlights, and callouts over a still screenshot; see [`ScreenshotScene.tsx`](src/components/ScreenshotScene.tsx) |

Media sources are resolved by `src/lib/resolveAsset.ts`, which supports HTTP(S), `data:`, absolute file paths, and relative assets under `public/`.

## Data field reference

Chart data follows the component interfaces:

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

`steps` for `terminal_scene` uses this exact type:

```ts
type TerminalStep =
  | { kind: "cmd"; text: string; typeSpeed?: number; holdSeconds?: number }
  | { kind: "out"; text: string; holdSeconds?: number }
  | { kind: "pause"; seconds: number }
  | { kind: "pill"; text: string; color?: string; durationSeconds?: number };
```

`screenshotSteps` for `screenshot_scene` supports these `kind` values:

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

Screenshot coordinates are normalized to `0`–`1` against the contain-fitted image rectangle, not the full composition canvas.

## Overlay types (`overlay.type`)

Every overlay also requires `in_seconds` and `out_seconds`.

| `type` | Component | Required fields | Common fields | Purpose |
|---|---|---|---|---|
| `section_title` | `SectionTitle` | `text` | `subtitle`, `accentColor`, `position` | Small section label |
| `stat_reveal` | `StatReveal` | `text` | `subtitle`, `accentColor`, `position` | Corner statistic badge |
| `hero_title` | `HeroTitle` | `text` | `subtitle` | Full-frame title overlay |
| `provider_chip` | `ProviderChip` | `providers` (string list) | `cycleSeconds`, `position`, `accentColor`, `label` | Badge that cycles through provider names at a fixed cadence |

## Add a scene type

1. Create the React component in `src/components/MyScene.tsx`. Drive animation with `useCurrentFrame()`, `useVideoConfig()`, `interpolate(...)`, and `spring(...)`.
2. Export the component and any public types from `src/components/index.ts`.
3. Add new prop fields to the `Cut` interface in `src/Explainer.tsx`. `type` is currently a `string`, so it does not need a new enum member.
4. Add a dispatch branch to `SceneRenderer`:

   ```tsx
   if (cut.type === "my_scene" && cut.mySceneData) {
     return maybeWrapWithBg(<MyScene ... />);
   }
   ```

5. Add the new `cut.type`, required fields, and data shape to this document so callers can discover it.

The existing synthetic UI components are `TerminalScene` and `ScreenshotScene`. New components in this family should continue using frame-driven step lists; avoid CSS transitions or CSS animations that make rendering nondeterministic.
