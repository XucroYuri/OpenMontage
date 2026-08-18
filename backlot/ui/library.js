import { el, fmtAgo, getJSON, subscribe, thumbURL } from "/ui/lib.js";
import { getLocale, pipelineLabel, setLocale, stageLabel, statusLabel, t } from "/ui/i18n.js";

const grid = document.getElementById("grid");
const THEME_KEY = "backlot.theme";
let currentTheme = localStorage.getItem(THEME_KEY) === "light" ? "light" : "dark";

function applyTheme(theme) {
  currentTheme = theme === "light" ? "light" : "dark";
  document.documentElement.dataset.theme = currentTheme;
  localStorage.setItem(THEME_KEY, currentTheme);
}

function renderThemeToggle() {
  const next = currentTheme === "light" ? "dark" : "light";
  const title = t(next === "light" ? "theme.toLight" : "theme.toDark");
  return el("button", {
    class: "theme-toggle",
    type: "button",
    title,
    "aria-label": title,
    "aria-pressed": currentTheme === "light" ? "true" : "false",
    onclick: () => {
      applyTheme(next);
      const replacement = renderThemeToggle();
      document.querySelector(".theme-toggle").replaceWith(replacement);
    },
  }, el("span", { class: "theme-toggle-icon", "aria-hidden": "true" }, currentTheme === "light" ? "☾" : "☀"));
}

function applyLocaleText() {
  document.title = `${t("app.backlot")} — ${t("app.library")}`;
  document.querySelector(".wordmark").textContent = t("app.backlot");
  document.querySelector("h1").textContent = t("app.library");
  document.getElementById("empty").textContent = t("library.empty");
}

function renderLocaleToggle() {
  return el("button", {
    class: "locale-toggle",
    type: "button",
    title: t("language.switch"),
    "aria-label": t("language.switch"),
    onclick: () => {
      setLocale(getLocale() === "zh-CN" ? "en" : "zh-CN");
      applyLocaleText();
      document.querySelector(".locale-toggle").replaceWith(renderLocaleToggle());
      document.querySelector(".theme-toggle").replaceWith(renderThemeToggle());
      render().catch(console.error);
    },
  }, getLocale() === "zh-CN" ? "EN" : "中文");
}

applyTheme(currentTheme);
applyLocaleText();
document.getElementById("liveBadge").before(renderLocaleToggle(), renderThemeToggle());

function miniRail(states) {
  const rail = el("div", { class: "mini-rail" });
  for (const s of states) {
    const cls = s.status === "completed" ? "d"
      : s.status === "in_progress" ? "a"
      : s.status === "awaiting_human" ? "w" : "";
    rail.append(el("i", { class: cls, title: `${stageLabel(s.name)}：${statusLabel(s.status)}` }));
  }
  return rail;
}

function card(p) {
  const poster = el("div", { class: "lib-poster" });
  if (p.poster) {
    poster.append(el("img", { src: thumbURL(p.project_id, p.poster, 640), loading: "lazy", alt: "" }));
  } else {
    poster.append(el("span", { class: "lp-txt" }, t("library.noMedia")));
  }
  if (p.live && p.active_stage) {
    poster.append(el("span", { class: "lp-live" },
      el("span", { class: "dot" }),
      p.awaiting_human ? `◈ ${t("library.awaiting")}` : t("library.stageLive", { stage: stageLabel(p.active_stage) })));
  } else if (p.awaiting_human) {
    poster.append(el("span", { class: "lp-live" }, `◈ ${t("library.awaiting")}`));
  }

  const meta = el("div", { class: "lb-meta" },
    el("span", { class: "chip" }, pipelineLabel(p.pipeline_type)),
    p.scene_count ? el("span", { class: "chip" }, t("library.scenes", { count: p.scene_count })) : null,
    p.render_count ? el("span", { class: "chip" }, t("library.renders", { count: p.render_count })) : null,
    el("span", { class: "when" }, fmtAgo(p.last_activity)),
  );

  const staticSuffix = new URLSearchParams(location.search).has("static") ? "?static=1" : "";
  return el("a", { class: `lib-card${p.live ? " live-card" : ""}`, href: `/p/${p.project_id}${staticSuffix}`, style: "text-decoration:none;color:inherit" },
    poster,
    el("div", { class: "lib-body" },
      el("h3", {}, (p.title || p.project_id).toUpperCase()),
      meta,
      p.stage_states.length ? miniRail(p.stage_states) : null,
    ),
  );
}

async function render() {
  const projects = await getJSON("/api/projects");
  document.getElementById("count").textContent = t("library.projects", { count: projects.length });
  const liveCount = projects.filter((p) => p.live).length;
  const badge = document.getElementById("liveBadge");
  badge.classList.toggle("idle", liveCount === 0);
  document.getElementById("liveText").textContent = liveCount
    ? t("library.live", { count: liveCount })
    : t("library.idle");
  grid.innerHTML = "";
  document.getElementById("empty").style.display = projects.length ? "none" : "block";
  for (const p of projects) grid.append(card(p));
}

render().catch(console.error);
if (!new URLSearchParams(location.search).has("static")) {
  subscribe("/api/library/events", () => render().catch(console.error));
}
