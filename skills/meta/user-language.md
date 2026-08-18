# User Language and Capability Preservation

Apply this skill before any user-facing pipeline work. Localization changes how
people experience OpenMontage; it must not change which pipeline, stage, tool,
provider, model, or quality technique the agent can use.

## Keep Three Language Layers Independent

1. **Interaction locale** controls chat, approvals, progress, costs, warnings,
   errors, delivery notes, and other user-facing interface copy.
2. **Deliverable language** controls scripts, narration, dialogue, on-screen
   copy, subtitles, descriptions, publish metadata, and other audience content.
3. **Provider working language** controls prompts, search queries, structured
   tool inputs, and vendor-specific terminology used to obtain the best result.

Resolve them independently:

- Read the interaction locale from `interaction.locale`.
- Use the user's explicit deliverable language when provided. Otherwise, when
  `interaction.content_locale` is `auto`, default new deliverable content to the
  interaction locale unless the brief or source requires another language.
- When `interaction.provider_prompt_language` is `auto`, use the
  provider-optimized language and structure required by the relevant Layer 2
  and Layer 3 skills. Never mechanically translate a proven provider prompt or
  search strategy merely because the interface is Chinese.
- A quoted English sentence in an instruction file is a semantic copy template,
  not a language lock. Render its meaning in the active interaction locale.

## Preserve the Machine Contract

Never translate or rename schema keys, JSON/YAML fields, enum values, pipeline
IDs, stage names, artifact names, tool/provider/model names, API parameters,
locale codes, commands, file paths, environment variables, or source URLs.

Use translated presentation labels around those canonical values. Persist only
the canonical value. Raw JSON views must remain byte-faithful to the artifact.

Localization must not:

- remove or reorder pipeline stages;
- change required, optional, preferred, fallback, or available tools;
- replace a provider/model with a Chinese-language alternative;
- weaken preflight, review, cost, checkpoint, approval, or quality gates;
- shorten or simplify a provider prompt in ways that discard skill guidance.

## Protect Source Fidelity

- Never translate source media, quotations, transcripts, brand names, product
  names, technical terms, or user-authored content unless translation is part of
  the brief.
- For localization work, preserve an auditable link between source-language and
  target-language content. Keep terminology and pronunciation decisions in the
  canonical artifacts.
- Search in the language that best matches the subject and source ecosystem.
  Preserve exact names and identifiers in queries.

## Present Results Clearly

For a Chinese interaction locale:

- Write all decisions, recommendations, tradeoffs, approval prompts, progress
  reports, costs, warnings, and next steps in clear Simplified Chinese.
- Explain unavoidable technical identifiers in Chinese without changing them.
- Translate provider errors into actionable Chinese and retain the original
  technical error on a separate line when it is useful for diagnosis.
- Keep generated decision rationales and review summaries in the interaction
  locale unless the user asks for another language.

## Preflight Check

Before a stage is checkpointed, verify all of the following:

- User-facing copy matches the interaction locale.
- Deliverable content matches the approved deliverable language.
- Provider prompts follow the provider skill rather than a blanket translation.
- Machine identifiers and enum values remain canonical.
- Source content was not translated without approval.
- The same pipeline stages, tools, providers, quality gates, and review depth
  would have been available with an English interaction locale.
