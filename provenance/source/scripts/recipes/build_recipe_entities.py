#!/usr/bin/env python3
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
import sys
import tempfile
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.recipes.common import (
    AETIUS_BOOK1_CANONICAL_AUTHORITY,
    AETIUS_BOOK1_EMENDATION_OVERLAY,
    AETIUS_BOOK1_EMENDED_PATCHES,
    AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY,
    AUTHORITY_MODEL,
    AUTHORITY_REASONING,
    AUTHORITY_VERSION,
    DATASETS,
    DERIVED_DIR,
    ENTITY_MODEL_VERSION,
    PROMPT_VERSION,
    RECIPE_ENTITY_DIR,
    REPORTS_DIR,
    REPO_ROOT,
    STRUCTURED_AUTHORITY_BY_DATASET,
    STRUCTURED_AUTHORITY_DIR,
    build_recipe_payload,
    default_authority_metadata,
    ensure_dirs,
    infer_normalized_unit,
    load_structured_authority_corpus,
    load_recipe_records,
    normalized_unit_prompt_list,
    normalized_unit_vocabulary,
    prompt_version_for_dataset,
    reset_recipe_caches,
    strip_diacritics,
    write_json,
    write_text,
)


CORPUS_LABELS = {
    "dioscorides_book1_perfumes_resins": "Dioscorides Book 1",
    "dioscorides_book2_fats": "Dioscorides Book 2 Fats",
    "aetius_book1_oils": "Aëtius Book 1",
    "aetius_book16_myrepsika": "Aëtius Book 16",
    "paul_book7_perfumes": "Paul Book 7.20",
}

TOP_LEVEL_KEYS = (
    "recipe_id",
    "preparation",
    "ingredients",
    "processes",
    "materials",
    "people",
    "places",
    "uses",
    "preparation_names",
    "other_preparations_mentioned",
    "works_mentioned",
    "notes",
)

PREPARATION_ONLY_KEYS = (
    "recipe_id",
    "preparation",
    "preparation_names",
    "other_preparations_mentioned",
)

STRUCTURED_TEMP_ROOT = "recipe_structured"
PREPARATION_TEMP_ROOT = "recipe_structured_preparation_v2"
REVIEW_STRUCTURED_AUTHORITY_BY_DATASET = {
    "aetius_book1_oils": "reports/entity_review/structured/aetius_book1_emended.json",
}
BOOK1_EMENDED_PATCH_FORMAT_VERSION = "aetius-book1-emended-patch-v1"
BOOK1_EMENDED_CHANGE_SCOPES = {"note_only", "field_patch"}
BOOK1_EMENDED_REVIEW_STATUSES = {"pending", "accepted", "rejected"}
BOOK1_EMENDED_ALLOWED_ROOTS = set(TOP_LEVEL_KEYS) - {"recipe_id"}
QUANTITY_UNIT_VALIDATION_JSON = REPORTS_DIR / "quantity_unit_validation.json"
QUANTITY_UNIT_ALLOWLIST: dict[str, dict[str, list[dict[str, str]]]] = {
    "aetius_book1_oils": {},
    "dioscorides_book1_perfumes_resins": {},
    "dioscorides_book2_fats": {},
    "aetius_book16_myrepsika": {},
    "paul_book7_perfumes": {},
}


def _ascii_letters(text: str) -> bool:
    return any("a" <= ch.lower() <= "z" for ch in text)


def _utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_book1_overlay_recipes() -> dict[str, Any]:
    payload = json.loads(AETIUS_BOOK1_EMENDATION_OVERLAY.read_text(encoding="utf-8"))
    recipes = payload.get("recipes")
    if not isinstance(recipes, dict):
        raise ValueError(
            f"Book 1 emendation overlay missing recipes map in {AETIUS_BOOK1_EMENDATION_OVERLAY.relative_to(REPO_ROOT)}"
        )
    return recipes


def _book1_emendation_refs(overlay_recipe: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for item in overlay_recipe.get("emendations", []):
        refs.append(
            {
                "locus": item.get("locus"),
                "start_citation": item.get("start_citation"),
                "end_citation": item.get("end_citation"),
                "operation": item.get("operation"),
            }
        )
    return refs


def _build_book1_patch_scaffold(canonical_metadata: dict[str, Any]) -> dict[str, Any]:
    overlay_recipes = _load_book1_overlay_recipes()
    patches: dict[str, Any] = {}
    for recipe_id in sorted(overlay_recipes):
        overlay_recipe = overlay_recipes[recipe_id]
        patches[recipe_id] = {
            "recipe_id": recipe_id,
            "emendation_refs": _book1_emendation_refs(overlay_recipe),
            "change_scope": "note_only",
            "fields": [],
            "reason": "",
            "review_status": "pending",
        }
    return {
        "metadata": {
            "patch_format_version": BOOK1_EMENDED_PATCH_FORMAT_VERSION,
            "base_authority_source": str(AETIUS_BOOK1_CANONICAL_AUTHORITY.relative_to(REPO_ROOT)),
            "base_authority_build_version": canonical_metadata.get("build_version"),
            "overlay_source": str(AETIUS_BOOK1_EMENDATION_OVERLAY.relative_to(REPO_ROOT)),
            "working_copy_path": str(AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY.relative_to(REPO_ROOT)),
            "created_at": _utc_timestamp(),
        },
        "patches": patches,
    }


def initialize_book1_emended_working_copy(*, force: bool = False) -> tuple[Path, Path]:
    canonical = load_structured_authority_corpus(
        AETIUS_BOOK1_CANONICAL_AUTHORITY,
        allow_legacy=False,
        dataset_key="aetius_book1_oils",
    )
    if not force:
        for path in (AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY, AETIUS_BOOK1_EMENDED_PATCHES):
            if path.exists():
                raise FileExistsError(
                    f"{path.relative_to(REPO_ROOT)} already exists; pass --force-working-copy-init to overwrite."
                )

    working_payload = {
        "metadata": dict(canonical["metadata"]),
        "working_copy": {
            "kind": "aetius_book1_emended_working",
            "base_authority_source": str(AETIUS_BOOK1_CANONICAL_AUTHORITY.relative_to(REPO_ROOT)),
            "overlay_source": str(AETIUS_BOOK1_EMENDATION_OVERLAY.relative_to(REPO_ROOT)),
            "created_at": _utc_timestamp(),
            "last_applied_at": None,
        },
        "recipes": deepcopy(canonical["recipes"]),
    }
    write_json(AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY, working_payload)
    write_json(AETIUS_BOOK1_EMENDED_PATCHES, _build_book1_patch_scaffold(canonical["metadata"]))
    return AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY, AETIUS_BOOK1_EMENDED_PATCHES


def _load_book1_patch_payload() -> dict[str, Any]:
    payload = json.loads(AETIUS_BOOK1_EMENDED_PATCHES.read_text(encoding="utf-8"))
    metadata = payload.get("metadata")
    patches = payload.get("patches")
    if not isinstance(metadata, dict):
        raise ValueError(
            f"Patch file metadata missing or invalid in {AETIUS_BOOK1_EMENDED_PATCHES.relative_to(REPO_ROOT)}"
        )
    if metadata.get("patch_format_version") != BOOK1_EMENDED_PATCH_FORMAT_VERSION:
        raise ValueError(
            f"Unsupported patch_format_version in {AETIUS_BOOK1_EMENDED_PATCHES.relative_to(REPO_ROOT)}"
        )
    if not isinstance(patches, dict):
        raise ValueError(
            f"Patch file patches map missing or invalid in {AETIUS_BOOK1_EMENDED_PATCHES.relative_to(REPO_ROOT)}"
        )
    return payload


def _validate_patch_path(path: str) -> list[str]:
    parts = [part for part in path.split(".") if part]
    if not parts:
        raise ValueError("Patch path cannot be empty")
    if parts[0] not in BOOK1_EMENDED_ALLOWED_ROOTS:
        raise ValueError(f"Patch path root `{parts[0]}` is not allowed")
    return parts


def _resolve_parent_for_path(container: dict[str, Any], path: str) -> tuple[dict[str, Any], str]:
    parts = _validate_patch_path(path)
    current: Any = container
    for part in parts[:-1]:
        if not isinstance(current, dict):
            raise ValueError(f"Patch path `{path}` traversed a non-object segment")
        if part not in current:
            raise ValueError(f"Patch path `{path}` missing segment `{part}`")
        current = current[part]
    if not isinstance(current, dict):
        raise ValueError(f"Patch path `{path}` parent is not an object")
    return current, parts[-1]


def _resolve_list_for_path(container: dict[str, Any], path: str) -> list[Any]:
    parts = _validate_patch_path(path)
    current: Any = container
    for part in parts:
        if not isinstance(current, dict):
            raise ValueError(f"Patch path `{path}` traversed a non-object segment")
        if part not in current:
            raise ValueError(f"Patch path `{path}` missing segment `{part}`")
        current = current[part]
    if not isinstance(current, list):
        raise ValueError(f"Patch path `{path}` does not resolve to a list")
    return current


def _matcher_matches(item: Any, matcher: dict[str, Any]) -> bool:
    if not isinstance(item, dict):
        return False
    for key, expected in matcher.items():
        if key not in item:
            return False
        actual = item[key]
        if isinstance(expected, dict):
            if not _matcher_matches(actual, expected):
                return False
        else:
            if actual != expected:
                return False
    return True


def _matching_indices(items: list[Any], matcher: dict[str, Any]) -> list[int]:
    return [index for index, item in enumerate(items) if _matcher_matches(item, matcher)]


def _apply_book1_patch_field(recipe: dict[str, Any], field: dict[str, Any], *, recipe_id: str) -> str:
    op = field.get("op")
    if op == "replace_scalar":
        path = field.get("path")
        parent, key = _resolve_parent_for_path(recipe, path)
        if key not in parent:
            raise ValueError(f"{recipe_id}: replace_scalar target `{path}` does not exist")
        if isinstance(parent[key], (dict, list)):
            raise ValueError(f"{recipe_id}: replace_scalar target `{path}` is not scalar")
        old_value = field.get("old_value")
        if parent[key] != old_value:
            raise ValueError(
                f"{recipe_id}: replace_scalar old_value mismatch at `{path}`: expected {old_value!r}, found {parent[key]!r}"
            )
        parent[key] = field.get("new_value")
        return path

    if op == "append_string":
        path = field.get("path")
        items = _resolve_list_for_path(recipe, path)
        if any(not isinstance(item, str) for item in items):
            raise ValueError(f"{recipe_id}: append_string target `{path}` is not a string list")
        value = field.get("value")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{recipe_id}: append_string requires a non-empty string value")
        if value in items:
            raise ValueError(f"{recipe_id}: append_string value already present at `{path}`")
        items.append(value)
        return path

    if op in {"replace_list_item", "delete_list_item", "insert_list_item"}:
        path = field.get("path")
        items = _resolve_list_for_path(recipe, path)
        if any(not isinstance(item, dict) for item in items):
            raise ValueError(f"{recipe_id}: {op} target `{path}` is not an object list")
        match = field.get("match")
        if op != "insert_list_item":
            if not isinstance(match, dict) or not match:
                raise ValueError(f"{recipe_id}: {op} requires a non-empty match object")
            indices = _matching_indices(items, match)
            if len(indices) != 1:
                raise ValueError(
                    f"{recipe_id}: {op} match at `{path}` must resolve to exactly one item, found {len(indices)}"
                )
            index = indices[0]
            if op == "replace_list_item":
                items[index] = field.get("new_value")
                return path
            del items[index]
            return path

        new_value = field.get("new_value")
        if not isinstance(new_value, dict):
            raise ValueError(f"{recipe_id}: insert_list_item requires object new_value")
        after_match = field.get("after_match")
        if after_match is None:
            items.append(new_value)
            return path
        if not isinstance(after_match, dict) or not after_match:
            raise ValueError(f"{recipe_id}: insert_list_item after_match must be a non-empty object")
        indices = _matching_indices(items, after_match)
        if len(indices) != 1:
            raise ValueError(
                f"{recipe_id}: insert_list_item after_match at `{path}` must resolve to exactly one item, found {len(indices)}"
            )
        items.insert(indices[0] + 1, new_value)
        return path

    raise ValueError(f"{recipe_id}: unsupported patch op `{op}`")


def apply_book1_emended_patches() -> list[dict[str, Any]]:
    working_payload = json.loads(AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY.read_text(encoding="utf-8"))
    recipes = working_payload.get("recipes")
    if not isinstance(recipes, dict):
        raise ValueError(
            f"Working copy missing recipes map in {AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY.relative_to(REPO_ROOT)}"
        )
    patches_payload = _load_book1_patch_payload()
    patch_records = patches_payload["patches"]
    applied: list[dict[str, Any]] = []

    for recipe_id in sorted(patch_records):
        patch = patch_records[recipe_id]
        if patch.get("review_status") != "accepted":
            continue
        if patch.get("recipe_id") != recipe_id:
            raise ValueError(f"Patch recipe_id mismatch for {recipe_id}")
        if patch.get("change_scope") not in BOOK1_EMENDED_CHANGE_SCOPES:
            raise ValueError(f"{recipe_id}: unsupported change_scope `{patch.get('change_scope')}`")
        fields = patch.get("fields")
        if not isinstance(fields, list):
            raise ValueError(f"{recipe_id}: fields must be a list")
        recipe = recipes.get(recipe_id)
        if not isinstance(recipe, dict):
            raise KeyError(f"{recipe_id}: missing recipe in working authority copy")
        touched_paths: list[str] = []
        for field in fields:
            if not isinstance(field, dict):
                raise ValueError(f"{recipe_id}: patch field entries must be objects")
            touched_paths.append(_apply_book1_patch_field(recipe, field, recipe_id=recipe_id))
        applied.append(
            {
                "recipe_id": recipe_id,
                "change_scope": patch["change_scope"],
                "field_paths": touched_paths,
                "reason": patch.get("reason", ""),
            }
        )

    if "working_copy" not in working_payload or not isinstance(working_payload["working_copy"], dict):
        working_payload["working_copy"] = {
            "kind": "aetius_book1_emended_working",
            "base_authority_source": str(AETIUS_BOOK1_CANONICAL_AUTHORITY.relative_to(REPO_ROOT)),
            "overlay_source": str(AETIUS_BOOK1_EMENDATION_OVERLAY.relative_to(REPO_ROOT)),
            "created_at": None,
        }
    working_payload["working_copy"]["last_applied_at"] = _utc_timestamp()
    working_payload["working_copy"]["last_applied_patch_count"] = len(applied)
    write_json(AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY, working_payload)
    return applied


def _greekish(text: str) -> str:
    return "".join(ch for ch in strip_diacritics(text.lower()) if ch.isalpha())


def _shares_stem(source_span: str, normalized_label: str) -> bool:
    source = _greekish(source_span)
    label = _greekish(normalized_label)
    if not source or not label:
        return False
    if source[:2] and label[:2] and source[:2] == label[:2]:
        return True
    for size in range(min(len(source), len(label), 8), 3, -1):
        for idx in range(0, len(label) - size + 1):
            piece = label[idx : idx + size]
            if piece in source:
                return True
    return label in source or source in label


def _looks_like_infinitive(label: str) -> bool:
    clean = _greekish(label)
    return clean.endswith(("ειν", "εσθαι", "σθαι", "ηναι", "ναι", "αι", "ουν", "αν"))


def _context_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["source_span", "normalized_label", "certainty", "notes"],
        "properties": {
            "source_span": {"type": "string"},
            "normalized_label": {"type": "string"},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }


def _regimen_note_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["source_span", "normalized_note", "certainty", "notes"],
        "properties": {
            "source_span": {"type": "string"},
            "normalized_note": {"type": "string"},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }


def _preparation_schema(qualifier: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "source_span",
            "normalized_label",
            "qualifiers",
            "regimen_notes",
            "certainty",
            "notes",
        ],
        "properties": {
            "source_span": {"type": "string"},
            "normalized_label": {"type": "string"},
            "qualifiers": {"type": "array", "items": qualifier},
            "regimen_notes": {"type": "array", "items": _regimen_note_schema()},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }


def _schema() -> dict[str, Any]:
    quantity = {
        "type": "object",
        "required": [
            "source_span",
            "raw_number",
            "normalized_number",
            "raw_unit",
            "normalized_unit",
            "certainty",
            "notes",
        ],
        "properties": {
            "source_span": {"type": "string"},
            "raw_number": {"type": ["string", "null"]},
            "normalized_number": {"type": ["number", "string", "null"]},
            "raw_unit": {"type": ["string", "null"]},
            "normalized_unit": {"type": ["string", "null"]},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    qualifier = {
        "type": "object",
        "required": ["qualifier_type", "source_span", "normalized_value", "certainty", "notes"],
        "properties": {
            "qualifier_type": {
                "enum": [
                    "duration",
                    "cycle_count",
                    "exposure",
                    "location",
                    "temperature",
                    "color",
                    "manner",
                    "other",
                ]
            },
            "source_span": {"type": "string"},
            "normalized_value": {"type": ["string", "null"]},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    ingredient = {
        "type": "object",
        "required": [
            "source_span",
            "base_label",
            "normalized_label",
            "alternative_set_id",
            "certainty",
            "linked_process_labels",
            "quantities",
            "qualifiers",
            "notes",
        ],
        "properties": {
            "source_span": {"type": "string"},
            "base_label": {"type": "string"},
            "normalized_label": {"type": "string"},
            "alternative_set_id": {"type": ["string", "null"]},
            "certainty": {"enum": ["certain", "uncertain"]},
            "linked_process_labels": {"type": "array", "items": {"type": "string"}},
            "quantities": {"type": "array", "items": quantity},
            "qualifiers": {"type": "array", "items": qualifier},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    process = {
        "type": "object",
        "required": [
            "source_span",
            "normalized_label",
            "target_type",
            "target_labels",
            "quantities",
            "qualifiers",
            "certainty",
            "notes",
        ],
        "properties": {
            "source_span": {"type": "string"},
            "normalized_label": {"type": "string"},
            "target_type": {"enum": ["ingredient", "recipe"]},
            "target_labels": {"type": "array", "items": {"type": "string"}},
            "quantities": {"type": "array", "items": quantity},
            "qualifiers": {"type": "array", "items": qualifier},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    material = {
        "type": "object",
        "required": [
            "source_span",
            "normalized_label",
            "role",
            "certainty",
            "quantities",
            "qualifiers",
            "notes",
        ],
        "properties": {
            "source_span": {"type": "string"},
            "normalized_label": {"type": "string"},
            "role": {
                "enum": ["tool", "apparatus", "fuel", "carrier", "adjunct_material", "uncertain_material"]
            },
            "certainty": {"enum": ["certain", "uncertain"]},
            "quantities": {"type": "array", "items": quantity},
            "qualifiers": {"type": "array", "items": qualifier},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    context = _context_schema()
    use = {
        "type": "object",
        "required": ["category", "source_span", "snippet", "certainty", "notes"],
        "properties": {
            "category": {"enum": ["medical", "ritual", "cosmetic", "other"]},
            "source_span": {"type": "string"},
            "snippet": {"type": "string"},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "required": list(TOP_LEVEL_KEYS),
        "properties": {
            "recipe_id": {"type": "string"},
            "preparation": _preparation_schema(qualifier),
            "ingredients": {"type": "array", "items": ingredient},
            "processes": {"type": "array", "items": process},
            "materials": {"type": "array", "items": material},
            "people": {"type": "array", "items": context},
            "places": {"type": "array", "items": context},
            "uses": {"type": "array", "items": use},
            "preparation_names": {"type": "array", "items": context},
            "other_preparations_mentioned": {"type": "array", "items": context},
            "works_mentioned": {"type": "array", "items": context},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }


def _preparation_only_schema() -> dict[str, Any]:
    qualifier = {
        "type": "object",
        "required": ["qualifier_type", "source_span", "normalized_value", "certainty", "notes"],
        "properties": {
            "qualifier_type": {
                "enum": ["duration", "cycle_count", "exposure", "location", "temperature", "manner", "other"]
            },
            "source_span": {"type": "string"},
            "normalized_value": {"type": ["string", "null"]},
            "certainty": {"enum": ["certain", "uncertain"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    context = _context_schema()
    return {
        "type": "object",
        "required": list(PREPARATION_ONLY_KEYS),
        "properties": {
            "recipe_id": {"type": "string"},
            "preparation": _preparation_schema(qualifier),
            "preparation_names": {"type": "array", "items": context},
            "other_preparations_mentioned": {"type": "array", "items": context},
        },
        "additionalProperties": False,
    }


def _dataset_prompt_addendum(dataset_key: str) -> str:
    if dataset_key != "aetius_book1_oils":
        return ""
    return """
- Treat the Book 1 emended experiment text as authoritative for this pass.
- Preserve the current Book 1 preparation splits rather than recombining them.
- Keep floral ounce/count phrases on the flowers or petals, not on the oil.
- Keep oil volume measures such as ξέστης on the oils they quantify.
- Exclude shared trailing quantity phrases from ingredient spans unless they are syntactically inside the local ingredient phrase.
- Preserve the current alternate-ingredient handling rather than collapsing disjunctive pairs.
- Normalize oblique preparation references lexically when the recoverable head noun is clear, and mark restored heads as uncertain when needed.
"""


def _prompt(recipe: dict[str, str], *, dataset_key: str) -> str:
    source = json.dumps(recipe, ensure_ascii=False, indent=2)
    return f"""You are extracting structured recipe authority from ancient Greek recipe text.

Use only the inline source data below as evidence. Do not run shell commands. Do not read or rely on any files. Ignore any prior extraction layers.

Source data:
{source}

Return ONLY a raw JSON object matching the provided schema.

Rules:
- Use only `lemma` and `text` as evidence.
- Preserve exact Greek `source_span` values from the source data.
- Use Greek `normalized_label` values where possible.
- Treat the input record as one preparation/text unit. If the passage still contains another clearly headed preparation block after the current unit, do not absorb that later block's ingredients, processes, people, or materials into the current record.
- If the procedure text does not restate the preparation name, use `lemma` for `preparation.source_span` and `preparation.normalized_label`.
- Separate ingredients, processes, and materials cleanly.
- `ingredients[*].source_span` must preserve only the exact local Greek ingredient phrase.
- Do not expand an ingredient span merely to absorb a shared trailing quantity phrase from a coordinated list.
- If quantity or count wording is syntactically inside the local ingredient phrase, it may remain inside the ingredient span.
- Preserve the full modified ingredient phrase in `ingredients[*].source_span` when local participles or adjectives belong to that ingredient.
- Split participial ingredient phrases into ingredient records plus linked process records.
- In `ingredients[*].normalized_label`, keep explicit subtype/color/material modifiers when they are part of the ingredient identity, while removing only inflection, articles, and quantities. Examples: prefer `λευκὰ πέταλα`, `ἔλαιον Ἰταλικόν`, `ἔλαιον ὀμφάκινον`.
- If the Greek marks alternatives with `ἢ`, extract each alternative as a separate ingredient record and link them with the same `alternative_set_id`.
- Do not collapse alternatives into one disjunctive ingredient label.
- If an alternative is elliptical, keep the transmitted Greek only in `source_span`; a cautiously restored head noun may appear in `normalized_label`, but mark it `uncertain` and note the restoration.
- Put quantities directly on the ingredient, process, or material they belong to.
- Preserve quantity `source_span`, `raw_number`, `normalized_number` when safe, `raw_unit`, `normalized_unit` when safe, `certainty`, and `notes`.
- `raw_unit` must stay source-facing Greek/sign notation. `normalized_unit` must use the controlled English/transliterated vocabulary when the unit is recoverable: {normalized_unit_prompt_list()}.
- If the source uses distributive `ἀνὰ`, do not include `ἀνὰ` in the quantity `source_span`; record only the measurable expression itself and add a recipe-level note that distributive `ἀνὰ` governs that ingredient cluster.
- Put qualifiers directly on the item they qualify.
- Do not misfile temporal counts or exposure phrases as ingredient quantities when they qualify a process instead.
- For `processes[*].source_span`, keep the minimal verbal or participial span and move duration, exposure, location, temperature, color, and manner into `qualifiers`.
- For `processes[*].normalized_label`, use a Greek infinitive by default such as `διαψύχειν`, `ἐμβάλλειν`, `καπνίζειν`, `ἀποτίθεσθαι`. Do not use finite forms, participles, action nouns, English glosses, or combined multi-verb labels.
- Split coordinated or sequential verbal spans into separate process records rather than combining them under one normalized label.
- Do not invent unnamed apparatus, tools, carriers, fuels, or adjuncts.
- If a material role or unit cannot be resolved safely, keep the Greek span and mark it `uncertain`.
- Do not paraphrase preparation labels into English.
- `preparation.qualifiers` is only for recipe-level regimen/style/subtype information. Do not migrate clearly step-local qualifiers onto `preparation` just for symmetry.
- `preparation.regimen_notes` should stay short and should only be used when a recipe-level method characterization is too specific for one qualifier.
- `uses` should be included only when the text explicitly gives application or use context.
- `places`, `people`, `preparation_names`, `other_preparations_mentioned`, and `works_mentioned` should only be included when explicitly present in `lemma` or `text`.
- If a later headed preparation block is visible in the source text, `other_preparations_mentioned` may note that it exists, but do not let that later block contribute substantive extracted entities to the current record.
- In compressed strings such as `νυχθήμερον α 𐆄 γ`, keep the duration and the quantity separate.
{_dataset_prompt_addendum(dataset_key)}
"""


def _preparation_prompt(recipe: dict[str, str], *, dataset_key: str) -> str:
    source = json.dumps(recipe, ensure_ascii=False, indent=2)
    return f"""You are extracting only preparation-focused authority from ancient Greek recipe text.

Use only the inline source data below as evidence. Do not run shell commands. Do not read or rely on any files. Ignore any prior extraction layers.

Source data:
{source}

Return ONLY a raw JSON object matching the provided schema.

Rules:
- Use only `lemma` and `text` as evidence.
- Preserve exact Greek `source_span` values from the source data.
- Treat the input record as one preparation/text unit. If the source still includes another clearly headed preparation later in the passage, keep `preparation` focused on the current unit headed by `lemma`.
- `preparation.normalized_label` must be Greek and lexical, not an English gloss or a long mixed alias/regimen string.
- If the running text does not restate the preparation name cleanly, use `lemma` for `preparation.source_span` and `preparation.normalized_label`.
- `preparation_names` should capture explicit same-recipe aliases and alternative names only, especially formulas such as `ἤτοι`, `ὃ καὶ`, `καλεῖται`, and `προσηγόρευσαν`.
- `other_preparations_mentioned` should capture genuinely distinct preparations referenced in the passage, not same-recipe aliases.
- If another headed preparation appears later in the same source text, mention it only as a minimal cross-reference; do not let it determine the current record's preparation label, qualifiers, or regimen notes.
- Add `preparation.qualifiers` only when the text explicitly characterizes the preparation as a whole by regimen, subtype, style, repeated cycle count, or comparable recipe-level method.
- Add `preparation.regimen_notes` only for short explicit recipe-level method characterizations that are not cleanly reducible to one qualifier.
- Do not migrate clearly process-local qualifiers onto `preparation` just for symmetry.
- Step-local qualifiers such as a single action's duration, exposure, location, temperature, or manner should stay off `preparation` unless the passage generalizes them as a whole-preparation regimen or variant.
- Do not turn a single explicit process step into a preparation-level regimen note just because it sounds methodologically important. For example, keep one step's sunning, open-air exposure, cooling in a well, burial, or drying on a cloth off `preparation` when those details belong to an explicit process record.
- Preparation-level cues may include overall repeated boilings, soakings, immersions, or repeated cycle counts such as first/second/third/fourth/seventh passes.
- Style/subtype cues such as `ἁπλοῦν`, `διπλοῦν`, `τριπλοῦν`, `ὑγιεινόν`, `καπνιστόν`, or comparable explicit recipe characterizations belong on `preparation`.
- Preserve Greek numeric phrases exactly in `source_span`. Be careful with compressed numeric strings. Example: in `νυχθήμερον α 𐆄 γ`, `νυχθήμερον α` belongs to duration while `𐆄 γ` is the quantity; do not collapse them.
- If a unit is recoverable, keep `raw_unit` source-facing and use the controlled `normalized_unit` vocabulary: {normalized_unit_prompt_list()}.
- Do not infer unnamed preparations.
- Do not dump long mixed strings into `preparation.normalized_label`.
{_dataset_prompt_addendum(dataset_key)}
"""


def _source_anchored(span: str, *, lemma: str, text: str, source_haystack: str) -> bool:
    return bool(span) and (span in {lemma, text} or span in source_haystack)


def _label_contains_alias_formula(label: str) -> bool:
    lowered = label.lower()
    return any(
        marker in lowered
        for marker in ("ἤτοι", "ὃ καὶ", "καλεῖται", "καλοῦσι", "προσηγόρευσ", "ὃ καλοῦσι")
    )


def _has_distributive_note(notes: list[str]) -> bool:
    return any("ἀνὰ" in note for note in notes)


def _validate_preparation(
    recipe_source: dict[str, str],
    preparation: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    text = recipe_source["text"]
    lemma = recipe_source["lemma"]
    source_haystack = f"{lemma} {text}"

    if not preparation.get("normalized_label"):
        errors.append("preparation missing normalized_label")
    elif _ascii_letters(preparation.get("normalized_label", "")):
        errors.append("preparation normalized_label contains ASCII letters")
    elif _label_contains_alias_formula(preparation.get("normalized_label", "")):
        errors.append("preparation normalized_label still contains alias formula text")

    if not _source_anchored(preparation.get("source_span", ""), lemma=lemma, text=text, source_haystack=source_haystack):
        errors.append("preparation source_span is not anchored in lemma/text")

    for qualifier in preparation.get("qualifiers", []):
        span = qualifier.get("source_span", "")
        if span and not _source_anchored(span, lemma=lemma, text=text, source_haystack=source_haystack):
            errors.append(f"preparation qualifier span not found in lemma/text: {span}")

    for note in preparation.get("regimen_notes", []):
        span = note.get("source_span", "")
        if span and not _source_anchored(span, lemma=lemma, text=text, source_haystack=source_haystack):
            errors.append(f"preparation regimen note span not found in lemma/text: {span}")
        if not note.get("normalized_note"):
            errors.append("preparation regimen note missing normalized_note")

    return errors


def _validate_context_items(
    recipe_source: dict[str, str],
    payload: dict[str, Any],
    *,
    section: str,
) -> list[str]:
    errors: list[str] = []
    text = recipe_source["text"]
    lemma = recipe_source["lemma"]
    source_haystack = f"{lemma} {text}"
    for item in payload.get(section, []):
        span = item.get("source_span", "")
        label = item.get("normalized_label", "")
        if not span:
            errors.append(f"{section} item missing source_span")
        elif not _source_anchored(span, lemma=lemma, text=text, source_haystack=source_haystack):
            errors.append(f"{section} source_span not found in lemma/text: {span}")
        if not label:
            errors.append(f"{section} item missing normalized_label")
        elif section in {"materials", "people", "places", "preparation_names", "other_preparations_mentioned", "works_mentioned"}:
            if _ascii_letters(label):
                errors.append(f"{section} normalized_label contains ASCII letters: {label}")
    return errors


def _validate_record(recipe_source: dict[str, str], payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    text = recipe_source["text"]
    lemma = recipe_source["lemma"]
    source_haystack = f"{lemma} {text}"

    for key in TOP_LEVEL_KEYS:
        if key not in payload:
            errors.append(f"missing top-level key {key}")
    if payload.get("recipe_id") != recipe_source["recipe_id"]:
        errors.append("recipe_id mismatch")

    errors.extend(_validate_preparation(recipe_source, payload.get("preparation") or {}))
    for section in ("people", "places", "preparation_names", "other_preparations_mentioned", "works_mentioned"):
        errors.extend(_validate_context_items(recipe_source, payload, section=section))

    ingredient_labels: list[str] = []
    repeated_ingredient_quantity_spans: dict[str, int] = {}
    for item in payload.get("ingredients", []):
        span = item.get("source_span", "")
        base = item.get("base_label", "")
        label = item.get("normalized_label", "")
        alternative_set_id = item.get("alternative_set_id")
        span_key = _greekish(span)
        label_key = _greekish(label)
        if span not in source_haystack:
            errors.append(f"ingredient source_span not found in lemma/text: {span}")
        if not base or not label:
            errors.append(f"ingredient missing labels: {span}")
        if alternative_set_id is not None and not isinstance(alternative_set_id, str):
            errors.append(f"ingredient alternative_set_id must be a string or null: {span}")
        if _ascii_letters(label) or _ascii_letters(base):
            errors.append(f"ingredient label contains ASCII letters: {label}")
        for root in ("ερυθρ", "ιταλικ", "ομφακ"):
            if root in span_key and root not in label_key and "χωρ" not in span_key:
                errors.append(f"ingredient normalized_label dropped explicit modifier from source_span: {label} <- {span}")
        if " ἢ " in span or " ἢ " in label:
            errors.append(f"ingredient alternatives must be split rather than collapsed: {span}")
        if " ἢ " in span and not alternative_set_id:
            errors.append(f"ingredient alternative missing alternative_set_id: {span}")
        ingredient_labels.extend([base, label, span])
        for quantity in item.get("quantities", []):
            if quantity.get("source_span") and quantity["source_span"] not in source_haystack:
                errors.append(f"ingredient quantity span not found in lemma/text: {quantity['source_span']}")
            if "ἀνὰ" in (quantity.get("source_span") or ""):
                errors.append(f"ingredient quantity span must exclude distributive ἀνὰ: {quantity['source_span']}")
            normalized_unit = quantity.get("normalized_unit")
            inferred_unit = infer_normalized_unit(
                raw_unit=quantity.get("raw_unit"),
                source_span=quantity.get("source_span"),
            )
            if normalized_unit and normalized_unit not in normalized_unit_vocabulary():
                errors.append(f"ingredient quantity normalized_unit is not in the controlled vocabulary: {normalized_unit}")
            if inferred_unit and not normalized_unit:
                errors.append(
                    f"ingredient quantity missing normalized_unit for resolvable unit {inferred_unit}: {quantity.get('source_span')}"
                )
            if inferred_unit and normalized_unit and normalized_unit != inferred_unit:
                errors.append(
                    f"ingredient quantity normalized_unit mismatch: expected {inferred_unit}, found {normalized_unit}"
                )
            if quantity.get("source_span"):
                repeated_ingredient_quantity_spans[quantity["source_span"]] = (
                    repeated_ingredient_quantity_spans.get(quantity["source_span"], 0) + 1
                )
        for qualifier in item.get("qualifiers", []):
            if qualifier.get("source_span") and qualifier["source_span"] not in source_haystack:
                errors.append(f"ingredient qualifier span not found in lemma/text: {qualifier['source_span']}")

    for item in payload.get("processes", []):
        span = item.get("source_span", "")
        label = item.get("normalized_label", "")
        span_key = _greekish(span)
        if span not in source_haystack:
            errors.append(f"process source_span not found in lemma/text: {span}")
        if not label:
            errors.append(f"process missing normalized_label: {span}")
        elif _ascii_letters(label):
            errors.append(f"process normalized_label contains ASCII letters: {label}")
        elif not _looks_like_infinitive(label):
            errors.append(f"process normalized_label is not infinitive-like: {label}")
        elif " καὶ " in label:
            errors.append(f"process normalized_label combines multiple actions: {label}")
        if item.get("target_type") == "ingredient":
            for target in item.get("target_labels", []):
                if target not in ingredient_labels:
                    errors.append(f"process target label not found in ingredients: {target}")
        for quantity in item.get("quantities", []):
            if quantity.get("source_span") and quantity["source_span"] not in source_haystack:
                errors.append(f"process quantity span not found in lemma/text: {quantity['source_span']}")
            if "ἀνὰ" in (quantity.get("source_span") or ""):
                errors.append(f"process quantity span must exclude distributive ἀνὰ: {quantity['source_span']}")
            normalized_unit = quantity.get("normalized_unit")
            inferred_unit = infer_normalized_unit(
                raw_unit=quantity.get("raw_unit"),
                source_span=quantity.get("source_span"),
            )
            if normalized_unit and normalized_unit not in normalized_unit_vocabulary():
                errors.append(f"process quantity normalized_unit is not in the controlled vocabulary: {normalized_unit}")
            if inferred_unit and not normalized_unit:
                errors.append(
                    f"process quantity missing normalized_unit for resolvable unit {inferred_unit}: {quantity.get('source_span')}"
                )
            if inferred_unit and normalized_unit and normalized_unit != inferred_unit:
                errors.append(
                    f"process quantity normalized_unit mismatch: expected {inferred_unit}, found {normalized_unit}"
                )
        for qualifier in item.get("qualifiers", []):
            if qualifier.get("source_span") and qualifier["source_span"] not in source_haystack:
                errors.append(f"process qualifier span not found in lemma/text: {qualifier['source_span']}")

    for item in payload.get("materials", []):
        span = item.get("source_span", "")
        label = item.get("normalized_label", "")
        if span not in source_haystack:
            errors.append(f"material source_span not found in lemma/text: {span}")
        if not label:
            errors.append(f"material missing normalized_label: {span}")
        elif _ascii_letters(label):
            errors.append(f"material normalized_label contains ASCII letters: {label}")
        elif not _shares_stem(span, label) and item.get("certainty") != "uncertain":
            errors.append(f"material normalized_label appears inferred rather than text-anchored: {label} <- {span}")
        for quantity in item.get("quantities", []):
            if quantity.get("source_span") and quantity["source_span"] not in source_haystack:
                errors.append(f"material quantity span not found in lemma/text: {quantity['source_span']}")
            if "ἀνὰ" in (quantity.get("source_span") or ""):
                errors.append(f"material quantity span must exclude distributive ἀνὰ: {quantity['source_span']}")
            normalized_unit = quantity.get("normalized_unit")
            inferred_unit = infer_normalized_unit(
                raw_unit=quantity.get("raw_unit"),
                source_span=quantity.get("source_span"),
            )
            if normalized_unit and normalized_unit not in normalized_unit_vocabulary():
                errors.append(f"material quantity normalized_unit is not in the controlled vocabulary: {normalized_unit}")
            if inferred_unit and not normalized_unit:
                errors.append(
                    f"material quantity missing normalized_unit for resolvable unit {inferred_unit}: {quantity.get('source_span')}"
                )
            if inferred_unit and normalized_unit and normalized_unit != inferred_unit:
                errors.append(
                    f"material quantity normalized_unit mismatch: expected {inferred_unit}, found {normalized_unit}"
                )

    for item in payload.get("uses", []):
        span = item.get("source_span", "")
        snippet = item.get("snippet", "")
        if span and span not in source_haystack:
            errors.append(f"use source_span not found in lemma/text: {span}")
        if snippet and not snippet.strip():
            errors.append("use snippet empty")

    if "ἀνὰ" in source_haystack and any(count > 1 for count in repeated_ingredient_quantity_spans.values()):
        if not _has_distributive_note(payload.get("notes", [])):
            errors.append("recipe notes must mention distributive ἀνὰ when a shared ingredient quantity is repeated")

    return errors


def _validate_preparation_patch(recipe_source: dict[str, str], payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in PREPARATION_ONLY_KEYS:
        if key not in payload:
            errors.append(f"missing top-level key {key}")
    if payload.get("recipe_id") != recipe_source["recipe_id"]:
        errors.append("recipe_id mismatch")
    errors.extend(_validate_preparation(recipe_source, payload.get("preparation") or {}))
    for section in ("preparation_names", "other_preparations_mentioned"):
        errors.extend(_validate_context_items(recipe_source, payload, section=section))
    return errors


def _quantity_issue_allowed(
    dataset_key: str,
    recipe_id: str,
    *,
    quantity_span: str,
    raw_unit: str | None,
) -> str | None:
    entries = QUANTITY_UNIT_ALLOWLIST.get(dataset_key, {}).get(recipe_id, [])
    for entry in entries:
        if entry.get("source_span") == quantity_span and entry.get("raw_unit") == (raw_unit or ""):
            return entry.get("reason", "")
    return None


def _collect_quantity_unit_issues(
    *,
    dataset_key: str,
    recipe_id: str,
    payload: dict[str, Any],
    use_allowlist: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    allowed_units = normalized_unit_vocabulary()
    failures: list[dict[str, Any]] = []
    allowlisted: list[dict[str, Any]] = []
    for section in ("ingredients", "processes", "materials"):
        for item in payload.get(section, []):
            item_span = item.get("source_span", "")
            for quantity in item.get("quantities", []):
                quantity_span = quantity.get("source_span") or ""
                raw_unit = quantity.get("raw_unit")
                normalized_unit = quantity.get("normalized_unit")
                inferred = infer_normalized_unit(raw_unit=raw_unit, source_span=quantity_span)
                if normalized_unit and normalized_unit not in allowed_units:
                    failures.append(
                        {
                            "section": section,
                            "item_source_span": item_span,
                            "quantity_source_span": quantity_span,
                            "raw_unit": raw_unit,
                            "normalized_unit": normalized_unit,
                            "issue": "invalid_normalized_unit",
                            "expected": inferred,
                        }
                    )
                    continue
                if inferred and not normalized_unit:
                    issue = {
                        "section": section,
                        "item_source_span": item_span,
                        "quantity_source_span": quantity_span,
                        "raw_unit": raw_unit,
                        "normalized_unit": normalized_unit,
                        "issue": "missing_normalized_unit",
                        "expected": inferred,
                    }
                    if use_allowlist:
                        reason = _quantity_issue_allowed(
                            dataset_key,
                            recipe_id,
                            quantity_span=quantity_span,
                            raw_unit=raw_unit,
                        )
                        if reason is not None:
                            allowlisted.append({**issue, "allowlist_reason": reason})
                            continue
                    failures.append(issue)
                    continue
                if inferred and normalized_unit and normalized_unit != inferred:
                    failures.append(
                        {
                            "section": section,
                            "item_source_span": item_span,
                            "quantity_source_span": quantity_span,
                            "raw_unit": raw_unit,
                            "normalized_unit": normalized_unit,
                            "issue": "normalized_unit_mismatch",
                            "expected": inferred,
                        }
                    )
    return failures, allowlisted


def _build_quantity_unit_validation_report(
    records: list[Any],
    payloads_by_recipe_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    failures_by_dataset: dict[str, list[dict[str, Any]]] = {}
    allowlisted_by_dataset: dict[str, list[dict[str, Any]]] = {}
    for recipe in records:
        payload = payloads_by_recipe_id[recipe.recipe_id]
        failures, allowlisted = _collect_quantity_unit_issues(
            dataset_key=recipe.dataset_key,
            recipe_id=recipe.recipe_id,
            payload=payload,
            use_allowlist=True,
        )
        if failures:
            failures_by_dataset.setdefault(recipe.dataset_key, []).append(
                {"recipe_id": recipe.recipe_id, "issues": failures}
            )
        if allowlisted:
            allowlisted_by_dataset.setdefault(recipe.dataset_key, []).append(
                {"recipe_id": recipe.recipe_id, "issues": allowlisted}
            )
    failure_count = sum(len(entry["issues"]) for entries in failures_by_dataset.values() for entry in entries)
    allowlisted_count = sum(
        len(entry["issues"]) for entries in allowlisted_by_dataset.values() for entry in entries
    )
    return {
        "summary": {
            "allowed_unit_count": len(normalized_unit_vocabulary()),
            "allowed_units": sorted(normalized_unit_vocabulary()),
            "failure_count": failure_count,
            "allowlisted_count": allowlisted_count,
        },
        "failures_by_dataset": failures_by_dataset,
        "allowlisted_by_dataset": allowlisted_by_dataset,
        "allowlist": QUANTITY_UNIT_ALLOWLIST,
    }


def _run_codex_recipe_generic(
    recipe,
    *,
    prompt_builder,
    validator,
    schema_path: Path,
    temp_output_dir: Path,
    timeout: int,
) -> tuple[bool, dict[str, Any] | None, str]:
    recipe_source = {
        "recipe_id": recipe.recipe_id,
        "lemma": recipe.lemma or recipe.recipe_id,
        "text": recipe.text,
    }
    output_path = temp_output_dir / f"{recipe.recipe_id}.json"
    if output_path.exists():
        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            output_path.unlink()
        else:
            errors = validator(recipe_source, payload)
            if not errors:
                return True, payload, "ok"
            output_path.unlink()
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "-m",
        AUTHORITY_MODEL,
        "-c",
        f'model_reasoning_effort="{AUTHORITY_REASONING}"',
        "--cd",
        str(REPO_ROOT),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
        prompt_builder(recipe_source, dataset_key=recipe.dataset_key),
    ]
    try:
        completed = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, None, "timeout"

    if completed.returncode != 0:
        stderr = (completed.stderr or completed.stdout or "").strip()
        return False, None, stderr[-1200:]
    if not output_path.exists():
        return False, None, "missing output file"

    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, None, f"invalid json: {exc}"

    errors = validator(recipe_source, payload)
    if errors:
        return False, payload, "; ".join(errors[:8])
    return True, payload, "ok"


def _run_codex_recipe(
    recipe,
    *,
    schema_path: Path,
    temp_output_dir: Path,
    timeout: int,
) -> tuple[bool, dict[str, Any] | None, str]:
    return _run_codex_recipe_generic(
        recipe,
        prompt_builder=_prompt,
        validator=_validate_record,
        schema_path=schema_path,
        temp_output_dir=temp_output_dir,
        timeout=timeout,
    )


def _run_codex_preparation_recipe(
    recipe,
    *,
    schema_path: Path,
    temp_output_dir: Path,
    timeout: int,
) -> tuple[bool, dict[str, Any] | None, str]:
    return _run_codex_recipe_generic(
        recipe,
        prompt_builder=_preparation_prompt,
        validator=_validate_preparation_patch,
        schema_path=schema_path,
        temp_output_dir=temp_output_dir,
        timeout=timeout,
    )


def _generate_corpus_structured_authority(
    dataset_key: str,
    recipes: list[Any],
    *,
    runner,
    temp_root_name: str,
    schema_path: Path,
    max_parallel: int,
    timeout: int,
) -> tuple[str, dict[str, Any], list[str]]:
    temp_output_dir = Path(tempfile.gettempdir()) / temp_root_name / dataset_key
    temp_output_dir.mkdir(parents=True, exist_ok=True)

    pending = list(recipes)
    results: dict[str, Any] = {}
    failed_messages: dict[str, str] = {}
    rounds = [max_parallel, max_parallel, min(5, max_parallel), min(3, max_parallel)]
    rounds = [value for idx, value in enumerate(rounds) if value > 0 and value not in rounds[:idx]]

    for workers in rounds:
        if not pending:
            break
        next_pending: list[Any] = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {
                executor.submit(
                    runner,
                    recipe,
                    schema_path=schema_path,
                    temp_output_dir=temp_output_dir,
                    timeout=timeout,
                ): recipe
                for recipe in pending
            }
            for future in as_completed(future_map):
                recipe = future_map[future]
                ok, payload, message = future.result()
                if ok and payload is not None:
                    results[recipe.recipe_id] = payload
                    failed_messages.pop(recipe.recipe_id, None)
                else:
                    next_pending.append(recipe)
                    failed_messages[recipe.recipe_id] = message
        pending = next_pending

    failures = [f"{recipe.recipe_id}: {failed_messages.get(recipe.recipe_id, 'failed')}" for recipe in pending]
    return dataset_key, results, failures


def generate_structured_authority(
    records: list[Any],
    *,
    max_parallel_per_corpus: int,
    timeout: int,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    ensure_dirs()
    schema_path = Path(tempfile.gettempdir()) / "recipe_structured_schema.json"
    schema_path.write_text(json.dumps(_schema(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    records_by_dataset: dict[str, list[Any]] = {}
    for dataset in DATASETS:
        records_by_dataset[dataset["key"]] = [record for record in records if record.dataset_key == dataset["key"]]

    all_results: dict[str, dict[str, Any]] = {}
    all_failures: list[str] = []
    with ThreadPoolExecutor(max_workers=len(records_by_dataset)) as executor:
        future_map = {
            executor.submit(
                _generate_corpus_structured_authority,
                dataset_key,
                recipes,
                runner=_run_codex_recipe,
                temp_root_name=STRUCTURED_TEMP_ROOT,
                schema_path=schema_path,
                max_parallel=max_parallel_per_corpus,
                timeout=timeout,
            ): dataset_key
            for dataset_key, recipes in records_by_dataset.items()
        }
        for future in as_completed(future_map):
            dataset_key, corpus_results, failures = future.result()
            all_results[dataset_key] = corpus_results
            all_failures.extend(failures)
    return all_results, all_failures


def generate_preparation_authority(
    records: list[Any],
    *,
    max_parallel_per_corpus: int,
    timeout: int,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    ensure_dirs()
    schema_path = Path(tempfile.gettempdir()) / "recipe_structured_preparation_schema.json"
    schema_path.write_text(
        json.dumps(_preparation_only_schema(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    records_by_dataset: dict[str, list[Any]] = {}
    for dataset in DATASETS:
        records_by_dataset[dataset["key"]] = [record for record in records if record.dataset_key == dataset["key"]]

    all_results: dict[str, dict[str, Any]] = {}
    all_failures: list[str] = []
    with ThreadPoolExecutor(max_workers=len(records_by_dataset)) as executor:
        future_map = {
            executor.submit(
                _generate_corpus_structured_authority,
                dataset_key,
                recipes,
                runner=_run_codex_preparation_recipe,
                temp_root_name=PREPARATION_TEMP_ROOT,
                schema_path=schema_path,
                max_parallel=max_parallel_per_corpus,
                timeout=timeout,
            ): dataset_key
            for dataset_key, recipes in records_by_dataset.items()
        }
        for future in as_completed(future_map):
            dataset_key, corpus_results, failures = future.result()
            all_results[dataset_key] = corpus_results
            all_failures.extend(failures)
    return all_results, all_failures


def load_structured_authority_from_temp(
    records: list[Any],
    *,
    temp_root_name: str = STRUCTURED_TEMP_ROOT,
    validator=_validate_record,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    temp_root = Path(tempfile.gettempdir()) / temp_root_name
    all_results: dict[str, dict[str, Any]] = {dataset["key"]: {} for dataset in DATASETS}
    all_failures: list[str] = []

    for record in records:
        output_path = temp_root / record.dataset_key / f"{record.recipe_id}.json"
        if not output_path.exists():
            all_failures.append(f"{record.recipe_id}: missing temp output")
            continue
        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            all_failures.append(f"{record.recipe_id}: invalid json: {exc}")
            continue

        recipe_source = {
            "recipe_id": record.recipe_id,
            "lemma": record.lemma or record.recipe_id,
            "text": record.text,
        }
        errors = validator(recipe_source, payload)
        if errors:
            all_failures.append(f"{record.recipe_id}: {'; '.join(errors[:8])}")
            continue

        all_results[record.dataset_key][record.recipe_id] = payload

    return all_results, all_failures


def _new_build_version() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _merge_results_into_authority_files(
    results_by_dataset: dict[str, dict[str, Any]],
    *,
    preparation_only: bool,
) -> None:
    for dataset_key, rel_path in STRUCTURED_AUTHORITY_BY_DATASET.items():
        dataset_results = results_by_dataset.get(dataset_key, {})
        if not dataset_results:
            continue
        out_path = REPO_ROOT / rel_path
        existing: dict[str, Any] = {}
        if out_path.exists():
            existing = load_structured_authority_corpus(
                out_path,
                allow_legacy=True,
                dataset_key=dataset_key,
            )["recipes"]
        metadata = default_authority_metadata(dataset_key=dataset_key, build_version=None)
        if preparation_only:
            for recipe_id, patch in dataset_results.items():
                current = dict(existing.get(recipe_id) or {})
                if not current:
                    raise KeyError(f"Cannot apply preparation-only patch; missing base authority for {recipe_id}")
                current["preparation"] = patch["preparation"]
                current["preparation_names"] = patch["preparation_names"]
                current["other_preparations_mentioned"] = patch["other_preparations_mentioned"]
                existing[recipe_id] = current
        else:
            existing.update(dataset_results)
        write_json(out_path, {"metadata": metadata, "recipes": existing})


def _stamp_authority_build_versions(build_version: str) -> None:
    for dataset_key, rel_path in STRUCTURED_AUTHORITY_BY_DATASET.items():
        out_path = REPO_ROOT / rel_path
        if not out_path.exists():
            continue
        payload = load_structured_authority_corpus(out_path, allow_legacy=False, dataset_key=dataset_key)
        metadata = dict(payload["metadata"])
        metadata["build_version"] = build_version
        write_json(out_path, {"metadata": metadata, "recipes": payload["recipes"]})


def _write_review_authority_files(results_by_dataset: dict[str, dict[str, Any]]) -> None:
    for dataset_key, rel_path in REVIEW_STRUCTURED_AUTHORITY_BY_DATASET.items():
        dataset_results = results_by_dataset.get(dataset_key, {})
        if not dataset_results:
            continue
        out_path = REPO_ROOT / rel_path
        metadata = default_authority_metadata(dataset_key=dataset_key, build_version=None)
        write_json(out_path, {"metadata": metadata, "recipes": dataset_results})


def main() -> int:
    parser = argparse.ArgumentParser(description="Build standalone normalized recipe/entity JSON records.")
    parser.add_argument(
        "--generate-structured-authority",
        action="store_true",
        help="Generate structured reviewed authority JSON from recipe lemma+text with Codex before rebuilding.",
    )
    parser.add_argument(
        "--generate-preparation-authority",
        action="store_true",
        help="Generate preparation-only authority JSON from recipe lemma+text with Codex before merging onto the existing structured authority.",
    )
    parser.add_argument(
        "--max-parallel-per-corpus",
        type=int,
        default=10,
        help="Maximum concurrent Codex extraction jobs per corpus during structured authority generation.",
    )
    parser.add_argument(
        "--codex-timeout",
        type=int,
        default=900,
        help="Per-recipe Codex timeout in seconds during structured authority generation.",
    )
    parser.add_argument(
        "--recipe-ids",
        nargs="+",
        help="Limit structured-authority generation to the given recipe ids.",
    )
    parser.add_argument(
        "--probe-only",
        action="store_true",
        help="Run structured-authority generation and report results without merging authority files or rebuilding derived outputs.",
    )
    parser.add_argument(
        "--merge-from-temp",
        action="store_true",
        help="Validate existing /tmp recipe-structured outputs and merge them into structured authority files before rebuilding.",
    )
    parser.add_argument(
        "--merge-preparation-from-temp",
        action="store_true",
        help="Validate existing /tmp preparation-only outputs and merge their preparation-only patches onto structured authority files before rebuilding.",
    )
    parser.add_argument(
        "--write-review-authority",
        action="store_true",
        help="Write review-only structured authority files (for example the Book 1 emended temp authority) instead of merging canonical outputs. Requires --probe-only.",
    )
    parser.add_argument(
        "--init-aetius-book1-emended-working-copy",
        action="store_true",
        help="Create a fresh Book 1 emended working authority copy plus a narrow-patch scaffold without touching canonical authority.",
    )
    parser.add_argument(
        "--force-working-copy-init",
        action="store_true",
        help="Overwrite the Book 1 emended working authority copy and patch scaffold when used with --init-aetius-book1-emended-working-copy.",
    )
    parser.add_argument(
        "--apply-aetius-book1-emended-patches",
        action="store_true",
        help="Apply accepted narrow Book 1 emended patches to the working authority copy only.",
    )
    args = parser.parse_args()
    if args.generate_structured_authority and args.generate_preparation_authority:
        raise ValueError("choose only one authority generation mode per run")
    if args.merge_from_temp and args.merge_preparation_from_temp:
        raise ValueError("choose only one temp merge mode per run")
    special_modes = [
        args.init_aetius_book1_emended_working_copy,
        args.apply_aetius_book1_emended_patches,
    ]
    if sum(bool(mode) for mode in special_modes) > 1:
        raise ValueError("choose only one Book 1 emended working-copy mode per run")
    if any(special_modes) and any(
        (
            args.generate_structured_authority,
            args.generate_preparation_authority,
            args.merge_from_temp,
            args.merge_preparation_from_temp,
            args.probe_only,
            args.write_review_authority,
            args.recipe_ids,
        )
    ):
        raise ValueError("Book 1 emended working-copy modes cannot be combined with authority generation or merge flags")
    if args.recipe_ids and not (
        args.generate_structured_authority
        or args.generate_preparation_authority
        or args.merge_from_temp
        or args.merge_preparation_from_temp
    ):
        raise ValueError(
            "--recipe-ids requires an authority generation or temp-merge mode"
        )
    if args.recipe_ids and (args.generate_structured_authority or args.generate_preparation_authority) and not args.probe_only:
        raise ValueError("--recipe-ids currently requires --probe-only to avoid partial canonical rebuilds")
    if args.write_review_authority and not args.probe_only:
        raise ValueError("--write-review-authority currently requires --probe-only")
    if args.force_working_copy_init and not args.init_aetius_book1_emended_working_copy:
        raise ValueError("--force-working-copy-init requires --init-aetius-book1-emended-working-copy")

    ensure_dirs()
    if args.init_aetius_book1_emended_working_copy:
        working_path, patch_path = initialize_book1_emended_working_copy(force=args.force_working_copy_init)
        print(f"Initialized {working_path.relative_to(REPO_ROOT)}")
        print(f"Initialized {patch_path.relative_to(REPO_ROOT)}")
        return 0

    if args.apply_aetius_book1_emended_patches:
        applied = apply_book1_emended_patches()
        print(
            f"Applied {len(applied)} accepted Book 1 emended patches to "
            f"{AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY.relative_to(REPO_ROOT)}"
        )
        for item in applied:
            touched = ", ".join(item["field_paths"]) or "(no field changes)"
            print(f"  - {item['recipe_id']}: {touched}")
        return 0

    records = load_recipe_records()
    selected_records = records
    if args.recipe_ids:
        wanted = set(args.recipe_ids)
        selected_records = [record for record in records if record.recipe_id in wanted]
        found = {record.recipe_id for record in selected_records}
        missing = sorted(wanted - found)
        if missing:
            raise KeyError(f"Unknown recipe ids: {', '.join(missing)}")

    if args.generate_structured_authority:
        all_results, all_failures = generate_structured_authority(
            selected_records,
            max_parallel_per_corpus=args.max_parallel_per_corpus,
            timeout=args.codex_timeout,
        )
        if all_failures:
            sample = "\n".join(f"- {line}" for line in all_failures[:20])
            raise RuntimeError(
                "Structured authority generation failed for some recipes.\n"
                f"Failure count: {len(all_failures)}\n{sample}"
            )
        if args.write_review_authority:
            _write_review_authority_files(all_results)
        if args.probe_only:
            for dataset_key, corpus_results in all_results.items():
                if corpus_results:
                    print(f"{dataset_key}: {len(corpus_results)} probe outputs")
                    for recipe_id in sorted(corpus_results):
                        payload = corpus_results[recipe_id]
                        print(
                            f"  - {recipe_id}: {len(payload.get('ingredients', []))} ingredients, "
                            f"{len(payload.get('processes', []))} processes, "
                            f"{len(payload.get('materials', []))} materials"
                        )
            return 0
        _merge_results_into_authority_files(all_results, preparation_only=False)
        reset_recipe_caches()
    elif args.generate_preparation_authority:
        all_results, all_failures = generate_preparation_authority(
            selected_records,
            max_parallel_per_corpus=args.max_parallel_per_corpus,
            timeout=args.codex_timeout,
        )
        if all_failures:
            sample = "\n".join(f"- {line}" for line in all_failures[:20])
            raise RuntimeError(
                "Preparation authority generation failed for some recipes.\n"
                f"Failure count: {len(all_failures)}\n{sample}"
            )
        if args.probe_only:
            for dataset_key, corpus_results in all_results.items():
                if corpus_results:
                    print(f"{dataset_key}: {len(corpus_results)} preparation probes")
                    for recipe_id in sorted(corpus_results):
                        payload = corpus_results[recipe_id]
                        print(
                            f"  - {recipe_id}: {len(payload.get('preparation', {}).get('qualifiers', []))} preparation qualifiers, "
                            f"{len(payload.get('preparation', {}).get('regimen_notes', []))} regimen notes, "
                            f"{len(payload.get('preparation_names', []))} aliases, "
                            f"{len(payload.get('other_preparations_mentioned', []))} preparation references"
                        )
            return 0
        _merge_results_into_authority_files(all_results, preparation_only=True)
        reset_recipe_caches()
    elif args.merge_from_temp:
        all_results, all_failures = load_structured_authority_from_temp(selected_records)
        if all_failures:
            sample = "\n".join(f"- {line}" for line in all_failures[:20])
            raise RuntimeError(
                "Structured authority temp merge failed for some recipes.\n"
                f"Failure count: {len(all_failures)}\n{sample}"
            )
        _merge_results_into_authority_files(all_results, preparation_only=False)
        reset_recipe_caches()
    elif args.merge_preparation_from_temp:
        all_results, all_failures = load_structured_authority_from_temp(
            selected_records,
            temp_root_name=PREPARATION_TEMP_ROOT,
            validator=_validate_preparation_patch,
        )
        if all_failures:
            sample = "\n".join(f"- {line}" for line in all_failures[:20])
            raise RuntimeError(
                "Preparation authority temp merge failed for some recipes.\n"
                f"Failure count: {len(all_failures)}\n{sample}"
            )
        _merge_results_into_authority_files(all_results, preparation_only=True)
        reset_recipe_caches()

    if args.probe_only:
        return 0

    build_version = _new_build_version()
    _stamp_authority_build_versions(build_version)
    reset_recipe_caches()
    index: list[dict[str, str]] = []
    index_metadata = default_authority_metadata(build_version=build_version)
    lines = [
        "# Entity Extraction Log",
        "",
        f"- Source recipe units processed: {len(records)}",
        "- Output mode: one standalone JSON file per recipe unit",
        (
            f"- Extraction authority: `reports/entity_review/structured/*.json` "
            f"(`{AUTHORITY_MODEL}`, reasoning `{AUTHORITY_REASONING}`, "
            f"entity model `{ENTITY_MODEL_VERSION}`, authority `{AUTHORITY_VERSION}`, "
            f"default prompt `{PROMPT_VERSION}`, Book 1 prompt `{prompt_version_for_dataset('aetius_book1_oils')}`, build `{build_version}`)."
        ),
        "- Canonical extraction is generated from structured GPT-5.4-high authority derived from each recipe's lemma and text.",
        "",
    ]
    payloads_by_recipe_id: dict[str, dict[str, Any]] = {}
    ordered_payloads: list[tuple[Any, dict[str, Any]]] = []
    for recipe in records:
        payload = build_recipe_payload(recipe)
        payloads_by_recipe_id[recipe.recipe_id] = payload
        ordered_payloads.append((recipe, payload))
        index.append(
            {
                "recipe_id": recipe.recipe_id,
                "recipe_urn": recipe.recipe_urn,
                "record_urn": recipe.record_urn,
                "file": str((RECIPE_ENTITY_DIR / f'{recipe.recipe_id}.json').relative_to(DERIVED_DIR.parent)),
                "host_raw_file": recipe.host_raw_file,
            }
        )
        lines.append(
            f"- `{recipe.recipe_id}`: {len(payload['ingredients'])} ingredients, "
            f"{len(payload['processes'])} processes, {len(payload['materials'])} materials, "
            f"{len(payload['people'])} people, {len(payload['places'])} places, "
            f"{len(payload['uses'])} uses, {len(payload['works_mentioned'])} works, "
            f"{len(payload['preparation_names'])} preparation names."
        )
    quantity_unit_report = _build_quantity_unit_validation_report(records, payloads_by_recipe_id)
    write_json(QUANTITY_UNIT_VALIDATION_JSON, quantity_unit_report)
    if quantity_unit_report["summary"]["failure_count"]:
        sample_lines: list[str] = []
        for dataset_key, entries in quantity_unit_report["failures_by_dataset"].items():
            for entry in entries[:5]:
                first = entry["issues"][0]
                sample_lines.append(
                    f"- {dataset_key} {entry['recipe_id']}: {first['issue']} at {first['quantity_source_span']} "
                    f"(expected {first.get('expected')}, found {first.get('normalized_unit')})"
                )
            if len(sample_lines) >= 10:
                break
        sample = "\n".join(sample_lines[:10])
        raise RuntimeError(
            "Quantity/unit validation failed.\n"
            f"Failure count: {quantity_unit_report['summary']['failure_count']}\n"
            f"See {QUANTITY_UNIT_VALIDATION_JSON.relative_to(REPO_ROOT)} for the full report.\n"
            f"{sample}"
        )
    for recipe, payload in ordered_payloads:
        out_path = RECIPE_ENTITY_DIR / f"{recipe.recipe_id}.json"
        write_json(out_path, payload)
    write_json(RECIPE_ENTITY_DIR / "index.json", {"metadata": index_metadata, "recipes": index})
    write_text(REPORTS_DIR / "entity_extraction_log.md", "\n".join(lines) + "\n")
    summary = {
        "metadata": index_metadata,
        "recipe_count": len(records),
        "index_file": str((RECIPE_ENTITY_DIR / "index.json").relative_to(DERIVED_DIR.parent)),
        "structured_authority_dir": str(STRUCTURED_AUTHORITY_DIR.relative_to(DERIVED_DIR.parent)),
    }
    write_json(DERIVED_DIR / "recipe_entities_summary.json", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
