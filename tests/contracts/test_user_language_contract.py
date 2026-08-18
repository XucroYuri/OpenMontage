import json
from pathlib import Path

from lib.config_model import InteractionConfig
from lib.pipeline_loader import (
    get_required_tools,
    get_stage_order,
    get_stage_skill,
    list_pipelines,
    load_pipeline,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _capability_fingerprint() -> dict[str, dict[str, object]]:
    fingerprint = {}
    for name in sorted(list_pipelines()):
        manifest = load_pipeline(name)
        stages = tuple(get_stage_order(manifest))
        fingerprint[name] = {
            "stages": stages,
            "stage_skills": tuple(get_stage_skill(manifest, stage) for stage in stages),
            "tools": tuple(sorted(get_required_tools(manifest))),
            "required_tools": tuple(
                (stage["name"], tuple(stage.get("required_tools", [])))
                for stage in manifest["stages"]
            ),
            "optional_tools": tuple(
                (stage["name"], tuple(stage.get("optional_tools", [])))
                for stage in manifest["stages"]
            ),
        }
    return fingerprint


def test_every_pipeline_requires_user_language_guard() -> None:
    for name in list_pipelines():
        manifest = load_pipeline(name)
        assert manifest.get("required_skills", [])[0] == "meta/user-language"
        assert "meta/user-language" not in get_required_tools(manifest)
        assert all(
            stage.get("skill") != "meta/user-language"
            for stage in manifest["stages"]
        )


def test_interaction_locale_does_not_change_pipeline_capabilities() -> None:
    fingerprints = []
    for locale in ("zh-CN", "en"):
        config = InteractionConfig(locale=locale)
        assert config.content_locale == "auto"
        assert config.provider_prompt_language == "auto"
        assert config.preserve_technical_identifiers is True
        assert config.preserve_source_language is True
        fingerprints.append(_capability_fingerprint())

    assert fingerprints[0] == fingerprints[1]


def test_user_language_skill_enforces_quality_boundaries() -> None:
    text = (REPO_ROOT / "skills/meta/user-language.md").read_text(encoding="utf-8")
    required_contracts = (
        "provider-optimized language",
        "Never mechanically translate",
        "schema keys",
        "enum values",
        "Source Fidelity",
        "remove or reorder pipeline stages",
        "change required, optional, preferred, fallback, or available tools",
        "same pipeline stages, tools, providers, quality gates, and review depth",
    )

    for contract in required_contracts:
        assert contract in text

    reviewer = (REPO_ROOT / "skills/meta/reviewer.md").read_text(encoding="utf-8")
    for contract in (
        "Language and Capability Review",
        "Interaction locale",
        "Deliverable language",
        "Provider working language",
        "locale-driven provider/model substitution",
    ):
        assert contract in reviewer


def test_backlot_localizes_every_decision_category() -> None:
    schema = json.loads(
        (REPO_ROOT / "schemas/artifacts/decision_log.schema.json").read_text(
            encoding="utf-8"
        )
    )
    categories = schema["properties"]["decisions"]["items"]["properties"][
        "category"
    ]["enum"]
    i18n = (REPO_ROOT / "backlot/ui/i18n.js").read_text(encoding="utf-8")

    for category in categories:
        assert f"{category}:" in i18n
