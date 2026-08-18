const LOCALE_KEY = "backlot.locale";

const messages = {
  "zh-CN": {
    "app.library": "项目库",
    "app.backlot": "制作看板",
    "theme.toLight": "切换到浅色主题",
    "theme.toDark": "切换到深色主题",
    "language.switch": "切换到 English",
    "library.empty": "还没有项目。开始一次制作后，项目会显示在这里。",
    "library.projects": "{count} 个项目",
    "library.live": "{count} 个进行中",
    "library.idle": "空闲",
    "library.noMedia": "暂无媒体",
    "library.awaiting": "等待你的确认",
    "library.stageLive": "进行中 · {stage}",
    "library.scenes": "{count} 个场景",
    "library.renders": "{count} 个成片",
    "slate.pipeline": "{pipeline} 流水线",
    "slate.sceneSummary": "{count} 个场景 · {duration}",
    "slate.awaiting": "等待你的确认",
    "slate.stalled": "可能已停滞",
    "slate.live": "制作中",
    "slate.idle": "空闲",
    "slate.spend": "生成费用",
    "stage.awaiting": "等待你的批准\n请在对话中回复后继续",
    "stage.stalled": "{minutes} 分钟没有新进展\n可向智能体询问状态",
    "stage.doneScenes": "已完成 {count} 个场景",
    "stage.inProgress": "正在进行",
    "stage.failed": "失败",
    "stage.approved": "已批准",
    "stage.unlisted": "未列入清单",
    "stage.undeclared": "“{stage}”已运行，但未在当前流水线清单中声明",
    "review.critical": "{count} 个严重问题",
    "review.suggestions": "{count} 条建议",
    "review.nitpicks": "{count} 个细节问题",
    "review.focus": "审查重点 {value}",
    "artifact.notRun": "此阶段尚未运行。",
    "artifact.notFound": "在磁盘上找不到此阶段的规范产物。",
    "artifact.gateSkipped": "已跳过审批门",
    "common.close": "关闭",
    "common.section": "段落",
    "common.moreSections": "还有 {count} 个段落",
    "common.approved": "已批准",
    "common.pendingApproval": "等待批准",
    "common.drafting": "编写中",
    "common.expandScript": "展开完整脚本",
    "common.scriptSummary": "脚本 · {duration} · {count} 个段落",
    "common.item": "项目 {index}",
    "common.selected": "已选择",
    "common.items": "{count} 项",
    "common.end": "结束",
    "approval.completeScript": "完整脚本预览显示在下方。",
    "approval.reviewStoryboard": "请在下方故事板中检查时间安排和镜头覆盖。",
    "approval.inspectAssets": "批准合成前，请检查下方分镜条中的每个生成结果。",
    "approval.whyConcept": "选择此概念的原因",
    "approval.publishDestination": "发布目标",
    "approval.productionProposal": "制作提案",
    "approval.researchBrief": "研究简报",
    "approval.scenePlan": "场景计划",
    "approval.generatedAssets": "生成素材",
    "approval.editDecisions": "剪辑决策",
    "approval.renderReport": "渲染报告",
    "approval.publishPlan": "发布计划",
    "approval.nothingFound": "没有找到可供审查的内容。",
    "approval.declaredMissing": "{stage} 检查点声明了 {artifacts}，但制作看板无法加载。",
    "approval.noDeclaration": "{stage} 检查点没有声明产物。",
    "approval.gate": "审批节点",
    "approval.ready": "{stage} 已准备好供你审查",
    "approval.instructions": "请在这里审查产物，然后在对话中批准或提出修改要求。",
    "approval.selfReview": "自检",
    "approval.unlocks": "批准后将进入 {stage}。",
    "approval.finalGate": "这是最后一个审批节点。",
    "approval.openArtifact": "打开完整产物",
    "scene.intent": "镜头意图",
    "decision.revised": "已修订",
    "decision.alsoConsidered": "还考虑过：",
    "panel.decisions": "决策",
    "panel.activity": "活动记录",
    "activity.running": "运行中",
    "scene.hero": "重点镜头",
    "scene.generating": "生成中",
    "scene.assetUnavailable": "素材不可用",
    "scene.snapshot": "快照",
    "scene.bespoke": "定制",
    "scene.handAuthored": "手工编排的合成",
    "scene.fileMissing": "清单中有素材记录，但文件缺失",
    "scene.noAsset": "尚无素材",
    "scene.take": "第 {index} 个备选",
    "scene.takes": "{count} 个备选",
    "scene.readNarration": "点击阅读完整旁白",
    "scene.playNarration": "播放旁白",
    "storyboard.title": "故事板",
    "storyboard.summary": "{count} 个场景{duration} · 卡片宽度随时长变化",
    "renders.title": "成片",
    "renders.versions": "{count} 个版本",
    "renders.root": "根目录",
    "watcher.title": "监视器发现的内容",
    "watcher.subtitle": "快照 / 验证帧",
    "notice.noStateTitle": "没有流水线状态。",
    "notice.noStateBody": "此项目没有检查点，制作看板正在显示磁盘上已发现的内容。遵循检查点协议的制作任务会显示完整看板。",
    "notice.awaitingTitle": "{stage} 阶段正在等待你的审查。",
    "notice.awaitingBodyBefore": "智能体已暂停在此审批节点，请",
    "notice.inChat": "在对话中回复",
    "notice.awaitingBodyAfter": "以批准或要求修改。",
    "replay.scrub": "回看完整制作过程",
    "replay.start": "回放制作过程",
    "replay.live": "返回实时",
    "error.projectNotFound": "未找到项目",
    "field.platform": "发布平台",
    "field.duration": "时长",
    "field.tone": "基调",
    "field.style": "风格",
    "field.runtime": "合成引擎",
    "field.pipeline": "流水线",
    "field.estimatedCost": "预估费用",
    "field.concepts": "概念方案",
    "field.sources": "来源",
    "field.dataPoints": "数据点",
    "field.angles": "内容角度",
    "field.sections": "段落",
    "field.scenes": "场景",
    "field.assets": "素材",
    "field.types": "类型",
    "field.generationCost": "生成费用",
    "field.cuts": "剪辑点",
    "field.outputs": "输出",
    "field.destinations": "发布目标"
  },
  en: {
    "app.library": "Library", "app.backlot": "Backlot",
    "theme.toLight": "Switch to light theme", "theme.toDark": "Switch to dark theme",
    "language.switch": "切换到中文", "library.empty": "No projects yet — run a production and it will appear here.",
    "library.projects": "{count} projects", "library.live": "{count} LIVE", "library.idle": "IDLE",
    "library.noMedia": "NO MEDIA YET", "library.awaiting": "AWAITING YOU", "library.stageLive": "LIVE · {stage}",
    "library.scenes": "{count} scenes", "library.renders": "{count} renders",
    "slate.pipeline": "{pipeline} pipeline", "slate.sceneSummary": "{count} scenes · {duration}",
    "slate.awaiting": "AWAITING YOU", "slate.stalled": "STALLED?", "slate.live": "LIVE", "slate.idle": "IDLE",
    "slate.spend": "generation spend", "stage.awaiting": "awaiting your approval\nreply in chat to continue",
    "stage.stalled": "stalled? no activity for {minutes}m\nask the agent for status", "stage.doneScenes": "{count} scenes done",
    "stage.inProgress": "in progress", "stage.failed": "failed", "stage.approved": "approved",
    "stage.unlisted": "unlisted", "stage.undeclared": "\"{stage}\" ran but isn't declared by this pipeline's manifest",
    "review.critical": "{count} critical", "review.suggestions": "{count} suggestions", "review.nitpicks": "{count} nitpicks",
    "review.focus": "review focus {value}", "artifact.notRun": "This stage hasn't run yet.",
    "artifact.notFound": "No canonical artifact found on disk for this stage.", "artifact.gateSkipped": "GATE SKIPPED",
    "common.close": "CLOSE", "common.section": "Section", "common.moreSections": "{count} more sections",
    "common.approved": "APPROVED", "common.pendingApproval": "PENDING APPROVAL", "common.drafting": "DRAFTING",
    "common.expandScript": "EXPAND SCRIPT", "common.scriptSummary": "script · {duration} · {count} sections",
    "common.item": "Item {index}", "common.selected": "SELECTED", "common.items": "{count} items", "common.end": "END",
    "approval.completeScript": "The complete script preview is shown directly below.",
    "approval.reviewStoryboard": "Review timing and shot coverage in the storyboard below.",
    "approval.inspectAssets": "Inspect every generated take in the filmstrip below before approving compose.",
    "approval.whyConcept": "WHY THIS CONCEPT", "approval.publishDestination": "Publish destination",
    "approval.productionProposal": "Production proposal", "approval.researchBrief": "Research brief",
    "approval.scenePlan": "Scene plan", "approval.generatedAssets": "Generated assets",
    "approval.editDecisions": "Edit decisions", "approval.renderReport": "Render report", "approval.publishPlan": "Publish plan",
    "approval.nothingFound": "Nothing reviewable was found.",
    "approval.declaredMissing": "The {stage} checkpoint declares {artifacts}, but Backlot could not load it.",
    "approval.noDeclaration": "The {stage} checkpoint does not declare an artifact.", "approval.gate": "REVIEW GATE",
    "approval.ready": "{stage} is ready for your review",
    "approval.instructions": "Review the artifact here, then reply in chat to approve it or request changes.",
    "approval.selfReview": "SELF-REVIEW", "approval.unlocks": "Approval unlocks {stage}.",
    "approval.finalGate": "This is the final approval gate.", "approval.openArtifact": "OPEN FULL ARTIFACT",
    "scene.intent": "Intent", "decision.revised": "revised", "decision.alsoConsidered": "also considered: ",
    "panel.decisions": "Decisions", "panel.activity": "Activity", "activity.running": "running",
    "scene.hero": "HERO", "scene.generating": "GENERATING", "scene.assetUnavailable": "asset unavailable",
    "scene.snapshot": "snapshot", "scene.bespoke": "BESPOKE", "scene.handAuthored": "hand-authored composition",
    "scene.fileMissing": "asset in manifest, file missing", "scene.noAsset": "no asset yet",
    "scene.take": "take {index}", "scene.takes": "{count} TAKES", "scene.readNarration": "Click to read the full narration",
    "scene.playNarration": "Play narration", "storyboard.title": "Storyboard",
    "storyboard.summary": "{count} scenes{duration} · card width ∝ duration", "renders.title": "Renders",
    "renders.versions": "{count} versions", "renders.root": "root", "watcher.title": "What the watcher found",
    "watcher.subtitle": "snapshots / verification frames", "notice.noStateTitle": "No pipeline state. ",
    "notice.noStateBody": "This project has no checkpoints — Backlot is showing what it found on disk. Runs that follow the checkpoint protocol get the full board.",
    "notice.awaitingTitle": "The {stage} stage is waiting for your review. ",
    "notice.awaitingBodyBefore": "The agent is paused at this gate — reply ", "notice.inChat": "in chat",
    "notice.awaitingBodyAfter": " to approve or request changes.", "replay.scrub": "scrub the whole run",
    "replay.start": "REPLAY RUN", "replay.live": "LIVE", "error.projectNotFound": "PROJECT NOT FOUND",
    "field.platform": "platform", "field.duration": "duration", "field.tone": "tone", "field.style": "style",
    "field.runtime": "runtime", "field.pipeline": "pipeline", "field.estimatedCost": "estimated cost",
    "field.concepts": "concepts", "field.sources": "sources", "field.dataPoints": "data points", "field.angles": "angles",
    "field.sections": "sections", "field.scenes": "scenes", "field.assets": "assets", "field.types": "types",
    "field.generationCost": "generation cost", "field.cuts": "cuts", "field.outputs": "outputs", "field.destinations": "destinations"
  }
};

const stageNames = {
  "zh-CN": {
    research: "研究", proposal: "提案", idea: "创意简报", script: "脚本", scene_plan: "场景规划",
    character_design: "角色设计", rig_plan: "绑定规划", assets: "素材", edit: "剪辑", compose: "合成", publish: "发布"
  }
};

const pipelineNames = {
  "zh-CN": {
    "animated-explainer": "动画解说", "talking-head": "真人口播", "screen-demo": "屏幕演示",
    "clip-factory": "批量切片", "podcast-repurpose": "播客再创作", cinematic: "电影感短片",
    animation: "动画", "character-animation": "角色动画", hybrid: "混合素材", "avatar-spokesperson": "数字人讲解",
    "localization-dub": "本地化配音", "documentary-montage": "纪录片蒙太奇", "framework-smoke": "框架测试"
  }
};

const artifactNames = {
  "zh-CN": {
    research_brief: "研究简报", proposal_packet: "制作提案", brief: "创意简报", script: "脚本",
    scene_plan: "场景计划", character_design: "角色设计", rig_plan: "绑定规划", asset_manifest: "素材清单",
    edit_decisions: "剪辑决策", render_report: "渲染报告", final_review: "最终审查", publish_log: "发布记录",
    decision_log: "决策记录"
  }
};

const statusNames = {
  "zh-CN": {
    completed: "已完成", in_progress: "正在进行", awaiting_human: "等待确认", failed: "失败", pending: "未开始", unknown: "未知"
  }
};

const fieldNames = {
  "zh-CN": {
    title: "标题", name: "名称", display_name: "显示名称", description: "描述", summary: "摘要", status: "状态",
    topic: "主题", hook: "开场钩子", target_platform: "发布平台", target_duration_seconds: "目标时长",
    total_duration_seconds: "总时长", duration_seconds: "时长", tone: "基调", style: "风格", platform: "平台",
    render_runtime: "合成引擎", pipeline: "流水线", locale: "语言区域", source_language: "源语言",
    target_languages: "目标语言", dub_mode_per_locale: "各语言配音模式", role: "角色", body_type: "体型",
    silhouette_notes: "轮廓说明", required_emotions: "所需情绪", required_actions: "所需动作", path: "路径"
  }
};

const reviewDecisionNames = {
  "zh-CN": { pass: "通过", revise: "需要修改", block: "阻塞", reject: "不通过" }
};

const decisionCategoryNames = {
  "zh-CN": {
    decision: "决策", pipeline_selection: "流水线选择", provider_selection: "提供商选择",
    render_runtime_selection: "合成引擎选择", composition_mode: "合成创作模式", voice_selection: "声音选择",
    visual_style: "视觉风格", music_selection: "音乐选择", tool_selection: "工具选择"
  }
};

const assetTypeNames = {
  "zh-CN": {
    image: "图像", video: "视频", diagram: "图表", animation: "动画", audio: "音频",
    narration: "旁白", music: "音乐", sfx: "音效", subtitle: "字幕"
  }
};

function normalizeLocale(value) {
  if (!value) return null;
  return String(value).toLowerCase().startsWith("zh") ? "zh-CN" : String(value).toLowerCase().startsWith("en") ? "en" : null;
}

const queryLocale = normalizeLocale(new URLSearchParams(location.search).get("lang"));
let activeLocale = queryLocale || normalizeLocale(localStorage.getItem(LOCALE_KEY)) || "zh-CN";
document.documentElement.lang = activeLocale;

export function getLocale() {
  return activeLocale;
}

export function setLocale(locale) {
  activeLocale = normalizeLocale(locale) || "zh-CN";
  localStorage.setItem(LOCALE_KEY, activeLocale);
  document.documentElement.lang = activeLocale;
}

export function t(key, values = {}) {
  const template = messages[activeLocale][key] ?? messages.en[key] ?? key;
  return String(template).replace(/\{(\w+)\}/g, (_, name) => String(values[name] ?? ""));
}

export function stageLabel(value) {
  return stageNames[activeLocale]?.[value] || String(value || "").replaceAll("_", " ");
}

export function pipelineLabel(value) {
  return pipelineNames[activeLocale]?.[value] || String(value || "unknown");
}

export function artifactLabel(value) {
  return artifactNames[activeLocale]?.[value] || String(value || "artifact").replaceAll("_", " ");
}

export function statusLabel(value) {
  return statusNames[activeLocale]?.[value] || String(value || "unknown").replaceAll("_", " ");
}

export function displayLabel(value) {
  return stageNames[activeLocale]?.[value]
    || artifactNames[activeLocale]?.[value]
    || fieldNames[activeLocale]?.[value]
    || String(value || "artifact").replaceAll("_", " ");
}

export function reviewDecisionLabel(value) {
  return reviewDecisionNames[activeLocale]?.[value] || String(value || "");
}

export function decisionCategoryLabel(value) {
  return decisionCategoryNames[activeLocale]?.[value] || String(value || "decision").replaceAll("_", " ");
}

export function assetTypeLabel(value) {
  return assetTypeNames[activeLocale]?.[value] || String(value || "");
}
