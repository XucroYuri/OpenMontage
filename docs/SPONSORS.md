> **简体中文（主版本）** | [English (secondary version)](SPONSORS.en.md)

# 赞助商

本文档说明如何将赞助商徽标添加到 OpenMontage README。

## 赞助商素材规范

- 将赞助商徽标存放在 `assets/sponsors/`。
- 根据赞助商名称使用全小写 kebab-case 文件名，例如 `acme-video.svg`。
- 优先使用 SVG。只有在赞助商无法提供矢量图时才使用 PNG。
- 徽标应使用透明背景、紧密裁切，并确保在 `44px` 高度下清晰可辨。
- 链接目标应使用赞助商的官方网站或产品页面。
- 使用描述明确的替代文本，例如 `Acme Video logo`，不要只写 `logo`。

## README 代码片段

在 `README.md` 顶部附近的 `Sponsors` 部分中，将每个赞助商添加为一个表格行：

```html
<tr>
<td width="180" align="center"><a href="https://example.com"><img src="assets/sponsors/example-sponsor.svg" alt="Example Sponsor" width="150"></a></td>
<td><strong>Example Sponsor</strong> 帮助 OpenMontage 用户实现具体目标。先说明产品能带来的实用成果，最后附上简短的<a href="https://example.com">行动号召链接</a>。</td>
</tr>
```

如果赞助商分别提供浅色和深色徽标，请使用 `picture` 元素：

```html
<tr>
<td width="180" align="center">
  <a href="https://example.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/sponsors/example-sponsor-dark.svg">
      <img src="assets/sponsors/example-sponsor-light.svg" alt="Example Sponsor" width="150">
    </picture>
  </a>
</td>
<td><strong>Example Sponsor</strong> 帮助 OpenMontage 用户实现具体目标。先说明产品能带来的实用成果，最后附上简短的<a href="https://example.com">行动号召链接</a>。</td>
</tr>
```

## 接入检查清单

添加赞助商之前，请收集：

- 赞助商显示名称
- 赞助商 URL
- 徽标文件，最好使用 SVG
- OpenMontage 获准在 README 中展示该徽标的确认信息
- 赞助商要求使用的任何商标声明（如有）

除非项目维护者明确批准，否则不要添加跟踪 URL、联盟营销重定向，也不要声称赞助商对项目背书。
