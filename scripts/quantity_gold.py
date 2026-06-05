#!/usr/bin/env python3
"""Validate mirrored quantity-gold artifacts.

Generation, review, projection, and export belong in
/home/seancoughlin/Projects/aetius. This derived repo only validates the mirror.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPO = Path("/home/seancoughlin/Projects/aetius")
RECIPES_INDEX = ROOT / "data" / "recipes.json"
GOLD_ROOT = ROOT / "data" / "review" / "quantity_gold"
GOLD_RECIPE_DIR = GOLD_ROOT / "recipes"
GOLD_INDEX = GOLD_ROOT / "index.json"
GOLD_SCHEMA = GOLD_ROOT / "schema.json"
GOLD_MANIFEST = GOLD_ROOT / "manifest.json"
METROLOGY_VOCAB = GOLD_ROOT / "vocabularies" / "metrology.json"
TEMPORAL_VOCAB = GOLD_ROOT / "vocabularies" / "temporal.json"
QUALIFIER_VOCAB = GOLD_ROOT / "vocabularies" / "process_qualifiers.json"
COMPAT_PROJECTION = GOLD_ROOT / "projection" / "recipes.json"
RICH_PROJECTION = GOLD_ROOT / "projection" / "rich_recipes.json"

SCHEMA_VERSION = "quantity-gold-v2"
ARTIFACT_VERSION = "2026-06-05-codex-v1"

RECORD_TYPES = {
    "ingredient_measurement",
    "product_measurement",
    "process_measurement",
    "process_qualifier",
    "stage_qualifier",
    "standalone_temporal",
    "rejection",
}
DIMENSIONS = {"weight", "volume", "count", "length", "time", "temperature", "ratio", "rate", "other"}
VALUE_KINDS = {"integer", "decimal", "fraction", "range", "approximate", "text_unresolved", "condition_unresolved"}
TEMPORAL_LABELS = {"day", "hour", "month", "year", "overnight", "until_condition"}
QUALIFIER_KINDS = {
    "duration",
    "frequency",
    "repetition",
    "interval",
    "sequence",
    "condition",
    "temperature",
    "manner",
    "other",
}
REVIEW_STATUSES = {
    "generated_unreviewed",
    "machine_validated",
    "human_reviewed",
    "accepted_for_projection",
    "accepted_for_canonical_update",
    "rejected",
    "superseded",
}
REJECTION_REASON_CODES = {
    "not_quantity",
    "lexical_false_positive",
    "ingredient_name_not_measure",
    "process_word_not_measure",
    "ambiguous_unresolved",
    "duplicate_of_accepted_record",
    "outside_scope",
}
TARGET_TYPES = {"ingredient", "product", "process", "stage", "recipe", "variant", "unknown"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_recipe_index() -> list[dict[str, Any]]:
    payload = load_json(RECIPES_INDEX)
    recipes = payload.get("recipes")
    if not isinstance(recipes, list):
        raise ValueError("data/recipes.json missing recipes list")
    return recipes


def load_recipe(recipe_id: str) -> dict[str, Any]:
    path = ROOT / "data" / "recipes" / f"{recipe_id}.json"
    if not path.exists():
        raise KeyError(f"Unknown recipe id: {recipe_id}")
    return load_json(path)


def source_haystack(recipe: dict[str, Any]) -> str:
    line_text = " ".join(line.get("text") or "" for line in (recipe.get("citation") or {}).get("lines") or [])
    return " ".join(
        part for part in (recipe.get("lemma"), recipe.get("text"), recipe.get("original_text"), line_text) if part
    )


def load_gold_records(recipe_ids: list[str] | None = None) -> list[dict[str, Any]]:
    paths = sorted(GOLD_RECIPE_DIR.glob("*.json"))
    if recipe_ids:
        wanted = {f"{recipe_id}.json" for recipe_id in recipe_ids}
        paths = [path for path in paths if path.name in wanted]
    return [load_json(path) for path in paths]


def controlled_units() -> set[str]:
    if not METROLOGY_VOCAB.exists():
        return set()
    return {item["normalized_unit"] for item in load_json(METROLOGY_VOCAB).get("units", [])}


def rational_fraction(value: Any) -> Fraction | None:
    if not isinstance(value, dict):
        return None
    rational = value.get("rational")
    if not isinstance(rational, dict):
        return None
    numerator = rational.get("numerator")
    denominator = rational.get("denominator")
    if not isinstance(numerator, int) or not isinstance(denominator, int) or denominator == 0:
        return None
    return Fraction(numerator, denominator)


def validate_metadata(payload: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    meta = payload.get("metadata")
    if not isinstance(meta, dict):
        return [f"{prefix}: metadata object is required"]
    for key in (
        "schema_version",
        "artifact_version",
        "run_id",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "reviewed_by",
        "source_repo",
        "source_commit",
        "derived_repo",
        "derived_commit",
        "previous_version",
        "archive_path",
        "review_status",
    ):
        if key not in meta:
            errors.append(f"{prefix}: metadata.{key} is required")
    if meta.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{prefix}: metadata.schema_version must be {SCHEMA_VERSION}")
    if meta.get("artifact_version") != ARTIFACT_VERSION:
        errors.append(f"{prefix}: metadata.artifact_version must be {ARTIFACT_VERSION}")
    if meta.get("source_repo") != str(SOURCE_REPO):
        errors.append(f"{prefix}: metadata.source_repo must be {SOURCE_REPO}")
    if meta.get("derived_repo") != str(ROOT):
        errors.append(f"{prefix}: metadata.derived_repo must be {ROOT}")
    if meta.get("derived_commit") is not None:
        errors.append(f"{prefix}: metadata.derived_commit must remain null until a derived commit exists")
    if meta.get("review_status") not in REVIEW_STATUSES:
        errors.append(f"{prefix}: invalid metadata.review_status {meta.get('review_status')!r}")
    return errors


def validate_value(value: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{prefix}: value object is required"]
    if value.get("kind") not in VALUE_KINDS:
        errors.append(f"{prefix}: invalid value.kind {value.get('kind')!r}")
    if value.get("kind") == "fraction" and rational_fraction(value) is None:
        errors.append(f"{prefix}: fraction value must preserve numerator and denominator")
    if value.get("temporal_label") is not None and value.get("temporal_label") not in TEMPORAL_LABELS:
        errors.append(f"{prefix}: invalid value.temporal_label {value.get('temporal_label')!r}")
    return errors


def validate_record(record: dict[str, Any], recipe: dict[str, Any], unit_vocab: set[str], prefix: str) -> list[str]:
    errors: list[str] = []
    if record.get("record_type") not in RECORD_TYPES:
        errors.append(f"{prefix}: invalid record_type {record.get('record_type')!r}")
    if record.get("recipe_id") != recipe.get("recipe_id"):
        errors.append(f"{prefix}: recipe_id mismatch")
    if record.get("dimension") not in DIMENSIONS:
        errors.append(f"{prefix}: invalid dimension {record.get('dimension')!r}")
    if record.get("review_status") not in REVIEW_STATUSES:
        errors.append(f"{prefix}: invalid review_status {record.get('review_status')!r}")
    source = record.get("source")
    span = ((source or {}).get("span") or {}).get("source_span") if isinstance(source, dict) else None
    if not isinstance(span, str) or not span.strip():
        errors.append(f"{prefix}: source span is required")
    elif span not in source_haystack(recipe):
        errors.append(f"{prefix}: source span not found in recipe text: {span!r}")
    target = record.get("target")
    if not isinstance(target, dict):
        errors.append(f"{prefix}: target object is required")
    else:
        if target.get("target_type") not in TARGET_TYPES:
            errors.append(f"{prefix}: invalid target_type {target.get('target_type')!r}")
        target_span = target.get("source_span")
        if not isinstance(target_span, str) or not target_span.strip():
            errors.append(f"{prefix}: target source_span is required")
        elif target_span not in source_haystack(recipe):
            errors.append(f"{prefix}: target span not found in recipe text: {target_span!r}")
    normalized_unit = record.get("normalized_unit")
    if normalized_unit is not None and unit_vocab and normalized_unit not in unit_vocab:
        errors.append(f"{prefix}: normalized_unit {normalized_unit!r} is not controlled")
    if record.get("record_type") == "rejection":
        if record.get("reason_code") not in REJECTION_REASON_CODES:
            errors.append(f"{prefix}: invalid reason_code {record.get('reason_code')!r}")
        if record.get("review_status") != "rejected":
            errors.append(f"{prefix}: rejection must have review_status rejected")
        if "reviewed_by" not in record:
            errors.append(f"{prefix}: rejection reviewed_by must be explicit")
    else:
        errors.extend(validate_value(record.get("value"), prefix))
    if record.get("record_type") in {"process_qualifier", "stage_qualifier"}:
        if record.get("qualifier_kind") not in QUALIFIER_KINDS:
            errors.append(f"{prefix}: qualifier_kind is required")
        if record.get("dimension") not in {"time", "temperature", "rate", "count", "other"}:
            errors.append(f"{prefix}: invalid qualifier dimension {record.get('dimension')!r}")
    return errors


def validate_gold_payload(payload: dict[str, Any]) -> list[str]:
    errors = validate_metadata(payload, payload.get("recipe_id", "<unknown>"))
    recipe_id = payload.get("recipe_id")
    if not isinstance(recipe_id, str) or not recipe_id:
        return errors + ["gold record: recipe_id is required"]
    try:
        recipe = load_recipe(recipe_id)
    except KeyError as exc:
        return errors + [str(exc)]
    if payload.get("dataset_key") != recipe.get("dataset_key"):
        errors.append(f"{recipe_id}: dataset_key mismatch")
    records = payload.get("records")
    if not isinstance(records, list):
        return errors + [f"{recipe_id}: records must be a list"]
    seen: set[str] = set()
    unit_vocab = controlled_units()
    for index, record in enumerate(records):
        prefix = f"{recipe_id} records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: record must be an object")
            continue
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{prefix}: record_id is required")
        elif record_id in seen:
            errors.append(f"{prefix}: duplicate record_id {record_id!r}")
        else:
            seen.add(record_id)
        errors.extend(validate_record(record, recipe, unit_vocab, prefix))
    return errors


def validate_projection_regressions() -> list[str]:
    errors: list[str] = []
    compat = load_json(COMPAT_PROJECTION)
    errors.extend(validate_metadata(compat, str(COMPAT_PROJECTION.relative_to(ROOT))))
    kyphi = (compat.get("recipes") or {}).get("dioscorides-1-25-kyphi") or {}
    cyperus = ((kyphi.get("projected_quantities_by_host") or {}).get("ingredient:κυπέρου") or [{}])[0]
    if cyperus.get("normalized_number") != 0.5 or cyperus.get("normalized_unit") != "xestes":
        errors.append("projection: ἡμίξεστον must project to 1/2 xestes")
    process = ((kyphi.get("process_qualifiers_by_host") or {}).get("process:ἔασόν τε συμπιεῖν") or [{}])[0]
    if process.get("qualifier_kind") != "duration" or process.get("temporal_label") != "day":
        errors.append("projection: ἡμέραν μίαν process duration qualifier missing")
    rich = load_json(RICH_PROJECTION)
    errors.extend(validate_metadata(rich, str(RICH_PROJECTION.relative_to(ROOT))))
    rich_records = ((rich.get("recipes") or {}).get("dioscorides-1-25-kyphi") or {}).get("accepted_records") or []
    if "dioscorides-1-25-kyphi:q11" not in {record.get("record_id") for record in rich_records}:
        errors.append("rich projection: process duration q11 missing")
    return errors


def validate_repository_overlay(
    *,
    recipe_ids: list[str] | None = None,
    require_complete: bool = False,
    require_canonical_coverage: bool = False,
) -> list[str]:
    errors: list[str] = []
    required = [GOLD_INDEX, GOLD_SCHEMA, GOLD_MANIFEST, METROLOGY_VOCAB, TEMPORAL_VOCAB, QUALIFIER_VOCAB]
    for path in required:
        if not path.exists():
            errors.append(f"missing quantity-gold artifact: {path.relative_to(ROOT)}")
        else:
            errors.extend(validate_metadata(load_json(path), str(path.relative_to(ROOT))))
    for payload in load_gold_records(recipe_ids):
        errors.extend(validate_gold_payload(payload))
    errors.extend(validate_projection_regressions())
    if require_complete:
        corpus_ids = {recipe["recipe_id"] for recipe in load_recipe_index()}
        present_ids = {payload["recipe_id"] for payload in load_gold_records()}
        if present_ids != corpus_ids:
            errors.append(f"quantity-gold mirror coverage incomplete: {len(present_ids)}/{len(corpus_ids)} records")
    if require_canonical_coverage:
        errors.append("canonical coverage validation belongs in the aetius source workflow, not the mirror")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mirrored quantity-gold artifacts.")
    parser.add_argument("--validate", action="store_true", help="Validate mirrored artifacts.")
    parser.add_argument("--recipe-ids", nargs="+", help="Limit validation to recipe ids.")
    parser.add_argument("--require-complete", action="store_true", help="Require records for every mirrored recipe.")
    parser.add_argument("--generate", action="store_true", help="Refuse generation in this derived repo.")
    parser.add_argument("--write-artifacts", action="store_true", help="Refuse artifact generation in this derived repo.")
    parser.add_argument("--project-reviewed", action="store_true", help="Refuse projection generation in this derived repo.")
    args = parser.parse_args()

    if args.generate or args.write_artifacts or args.project_reviewed:
        print(
            "Quantity-gold generation/projection belongs in /home/seancoughlin/Projects/aetius; "
            "export here with scripts/quantity_gold.py --export-derived.",
            file=sys.stderr,
        )
        return 2
    if not args.validate:
        parser.print_help()
        return 0
    errors = validate_repository_overlay(recipe_ids=args.recipe_ids, require_complete=args.require_complete)
    if errors:
        for error in errors[:200]:
            print(f"FAIL: {error}", file=sys.stderr)
        if len(errors) > 200:
            print(f"FAIL: ... {len(errors) - 200} more", file=sys.stderr)
        return 1
    print("PASS: quantity-gold mirror validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
