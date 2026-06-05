#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.recipes.common import (  # noqa: E402
    MEASURE_RELATIONS,
    REPO_ROOT,
    STRUCTURED_AUTHORITY_DIR,
    normalize_space,
    write_json,
)


DEFAULT_LEDGER = REPO_ROOT / "data" / "review" / "measure_unit_audit.jsonl"
ENTITY_KINDS = {"ingredients", "processes", "materials"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply reviewed quantity relationship metadata to structured authority.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--check", action="store_true", help="Validate the ledger without writing authority files.")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_ledger(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row["_line_no"] = line_no
        rows.append(row)
    return rows


def authority_files() -> dict[str, Path]:
    by_recipe: dict[str, Path] = {}
    for path in sorted(STRUCTURED_AUTHORITY_DIR.glob("*.json")):
        payload = load_json(path)
        recipes = payload.get("recipes") or {}
        for recipe_id in recipes:
            by_recipe[recipe_id] = path
    return by_recipe


def resolve_entity(recipe: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    kind = row.get("entity_kind")
    if kind not in ENTITY_KINDS:
        raise ValueError(f"line {row['_line_no']}: unsupported entity_kind {kind!r}")
    items = recipe.get(kind) or []
    index = row.get("entity_index_hint")
    if not isinstance(index, int) or index < 1 or index > len(items):
        raise ValueError(f"line {row['_line_no']}: entity_index_hint out of range")
    entity = items[index - 1]
    expected_span = normalize_space(row.get("entity_span") or "")
    actual_span = normalize_space(entity.get("source_span") or "")
    if expected_span and actual_span != expected_span:
        raise ValueError(
            f"line {row['_line_no']}: entity span mismatch for {row.get('recipe_id')}: "
            f"expected {expected_span!r}, found {actual_span!r}"
        )
    return entity


def indexed_quantities(entity: dict[str, Any], row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    quantities = entity.get("quantities") or []
    by_span: dict[str, dict[str, Any]] = {}
    for quantity in quantities:
        span = normalize_space(quantity.get("source_span") or "")
        if span in by_span:
            raise ValueError(f"line {row['_line_no']}: duplicate quantity span {span!r}")
        by_span[span] = quantity
    expected = [normalize_space(value) for value in row.get("quantity_spans") or []]
    missing = [span for span in expected if span not in by_span]
    if missing:
        raise ValueError(f"line {row['_line_no']}: missing quantity spans {missing!r}")
    return by_span


def apply_row(authority_payloads: dict[Path, dict[str, Any]], by_recipe: dict[str, Path], row: dict[str, Any]) -> int:
    recipe_id = row.get("recipe_id")
    path = by_recipe.get(recipe_id)
    if path is None:
        raise KeyError(f"line {row['_line_no']}: unknown recipe_id {recipe_id!r}")
    recipe = authority_payloads[path]["recipes"][recipe_id]
    entity = resolve_entity(recipe, row)
    quantities_by_span = indexed_quantities(entity, row)

    patch = row.get("proposed_patch") or {}
    groups = patch.get("groups") or []
    if not groups:
        raise ValueError(f"line {row['_line_no']}: proposed_patch.groups is required")

    touched = 0
    for group in groups:
        relation = group.get("measure_relation") or row.get("decision")
        if relation not in MEASURE_RELATIONS:
            raise ValueError(f"line {row['_line_no']}: unsupported measure_relation {relation!r}")
        group_key = group.get("measure_group_id") or group.get("group") or f"line-{row['_line_no']}"
        if not isinstance(group_key, str) or not group_key.strip():
            raise ValueError(f"line {row['_line_no']}: blank measure group")
        if not group_key.startswith(f"{recipe_id}:"):
            group_key = (
                f"{recipe_id}:{row['entity_kind']}:{row['entity_index_hint']}:measure:{normalize_space(group_key)}"
            )
        for span in group.get("quantity_spans") or []:
            normalized_span = normalize_space(span)
            quantity = quantities_by_span.get(normalized_span)
            if quantity is None:
                raise ValueError(f"line {row['_line_no']}: quantity span not present: {span!r}")
            quantity["measure_group_id"] = group_key
            quantity["measure_relation"] = relation
            touched += 1
    return touched


def main() -> int:
    args = parse_args()
    rows = load_ledger(args.ledger)
    by_recipe = authority_files()
    paths = {by_recipe[row["recipe_id"]] for row in rows}
    authority_payloads = {path: load_json(path) for path in paths}

    touched = 0
    for row in rows:
        touched += apply_row(authority_payloads, by_recipe, row)

    if not args.check:
        for path, payload in sorted(authority_payloads.items()):
            write_json(path, payload)

    print(f"{'Checked' if args.check else 'Applied'} {len(rows)} audit rows; touched {touched} quantities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
