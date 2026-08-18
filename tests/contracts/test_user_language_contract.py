import json
import re
from pathlib import Path

import yaml

from lib.config_model import InteractionConfig
from lib.pipeline_loader import (
    get_required_tools,
    get_stage_order,
    get_stage_skill,
    list_pipelines,
    load_pipeline,
)
from tools.tool_registry import registry


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
            "required_skills": tuple(manifest.get("required_skills", [])),
            "required_tools": tuple(
                (stage["name"], tuple(stage.get("required_tools", [])))
                for stage in manifest["stages"]
            ),
            "optional_tools": tuple(
                (stage["name"], tuple(stage.get("optional_tools", [])))
                for stage in manifest["stages"]
            ),
            "tools_available": tuple(
                (stage["name"], tuple(stage.get("tools_available", [])))
                for stage in manifest["stages"]
            ),
            "approval_gates": tuple(
                (stage["name"], bool(stage.get("human_approval_default", False)))
                for stage in manifest["stages"]
            ),
            "review_focus": tuple(
                (stage["name"], tuple(stage.get("review_focus", [])))
                for stage in manifest["stages"]
            ),
            "success_criteria": tuple(
                (stage["name"], tuple(stage.get("success_criteria", [])))
                for stage in manifest["stages"]
            ),
        }
    return fingerprint


def _tool_fingerprint() -> tuple[tuple[object, ...], ...]:
    registry.ensure_discovered()
    rows = []
    for name in registry.list_all():
        tool = registry.get(name)
        assert tool is not None
        rows.append((
            tool.name,
            tool.capability,
            tool.provider,
            tool.tier.value,
            tool.stability.value,
            tuple(tool.agent_skills),
            tuple(tool.fallback_tools),
        ))
    return tuple(sorted(rows))


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
    pipeline_fingerprints = []
    tool_fingerprints = []
    for locale in ("zh-CN", "en"):
        config = InteractionConfig(locale=locale)
        assert config.content_locale == "auto"
        assert config.provider_prompt_language == "auto"
        assert config.preserve_technical_identifiers is True
        assert config.preserve_source_language is True
        pipeline_fingerprints.append(_capability_fingerprint())
        tool_fingerprints.append(_tool_fingerprint())

    assert pipeline_fingerprints[0] == pipeline_fingerprints[1]
    assert tool_fingerprints[0] == tool_fingerprints[1]


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


def _object_keys(source: str, start: str, end: str) -> set[str]:
    block = source.split(start, 1)[1].split(end, 1)[0]
    return set(re.findall(r"\b([a-z][a-z0-9_]*)\s*:", block))


def test_backlot_localizes_every_manifest_artifact_and_schema_field() -> None:
    i18n = (REPO_ROOT / "backlot/ui/i18n.js").read_text(encoding="utf-8")
    artifact_labels = _object_keys(
        i18n, "const artifactNames = {", "const statusNames"
    )
    field_labels = _object_keys(i18n, "const fieldNames = {", "const reviewDecisionNames")

    produced = set()
    for path in (REPO_ROOT / "pipeline_defs").glob("*.yaml"):
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
        for stage in manifest.get("stages", []):
            produced.update(stage.get("produces") or [])

    schema_fields = set()
    for path in (REPO_ROOT / "schemas/artifacts").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema_fields.update(schema.get("properties", {}))

    assert produced <= artifact_labels
    assert schema_fields <= field_labels


def test_checkpoint_error_contract_keeps_localized_and_technical_layers() -> None:
    schema = json.loads(
        (REPO_ROOT / "schemas/checkpoints/checkpoint.schema.json").read_text(
            encoding="utf-8"
        )
    )
    properties = schema["properties"]
    assert {"error", "error_message", "technical_error", "error_category", "next_actions"} <= properties.keys()
    assert "error" not in schema["required"]
    assert properties["technical_error"]["type"] == "string"
    assert properties["next_actions"]["items"]["type"] == "string"
