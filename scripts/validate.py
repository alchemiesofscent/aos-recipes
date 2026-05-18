#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    "dioscorides_book1_perfumes_resins": 52,
    "dioscorides_book2_fats": 18,
    "aetius_book1_oils": 43,
    "aetius_book16_myrepsika": 44,
    "paul_book7_perfumes": 35,
}
FORBIDDEN = ("parallel-viewer", "experiments/.codex", "__pycache__")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    recipes_payload = load(ROOT / "data" / "recipes.json")
    sources_payload = load(ROOT / "data" / "sources.json")
    entities_payload = load(ROOT / "data" / "entities" / "index.json")
    manifest = load(ROOT / "manifest.json")
    recipes = recipes_payload.get("recipes")
    if not isinstance(recipes, list):
        fail("data/recipes.json missing recipes list")
    if len(recipes) != 192:
        fail(f"expected 192 recipes, found {len(recipes)}")

    ids = [recipe.get("recipe_id") for recipe in recipes]
    if any(not recipe_id for recipe_id in ids):
        fail("recipe without recipe_id")
    duplicates = [recipe_id for recipe_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        fail(f"duplicate recipe IDs: {duplicates[:5]}")

    counts = Counter(recipe.get("dataset_key") for recipe in recipes)
    if dict(counts) != EXPECTED_COUNTS:
        fail(f"slice counts mismatch: {dict(counts)}")
    manifest_counts = {
        item["dataset_key"]: item["recipe_count"]
        for item in manifest.get("counts_by_slice", [])
    }
    if manifest_counts != EXPECTED_COUNTS:
        fail(f"manifest counts mismatch: {manifest_counts}")

    source_keys = {source["dataset_key"] for source in sources_payload.get("sources", [])}
    if source_keys != set(EXPECTED_COUNTS):
        fail(f"sources mismatch: {sorted(source_keys)}")

    for recipe in recipes:
        recipe_id = recipe["recipe_id"]
        if recipe.get("source_entry", {}).get("derived_recipe_id") != recipe_id:
            fail(f"bad derived_recipe_id link for {recipe_id}")
        recipe_file = ROOT / recipe.get("canonical_file", "")
        if not recipe_file.exists():
            fail(f"missing canonical recipe file for {recipe_id}: {recipe_file}")
        file_payload = load(recipe_file)
        if file_payload.get("recipe_id") != recipe_id:
            fail(f"recipe file ID mismatch for {recipe_id}")
        if recipe_id not in entities_payload.get("by_recipe", {}):
            fail(f"missing entity index coverage for {recipe_id}")
        provenance_file = ROOT / "provenance" / "source" / "derived" / "recipe_entities" / f"{recipe_id}.json"
        if not provenance_file.exists():
            fail(f"missing provenance derived record for {recipe_id}")

    text_paths = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        if any(token in rel for token in FORBIDDEN):
            fail(f"forbidden path exported: {rel}")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".js", ".html", ".css", ".py", ".txt"}:
            text_paths.append(path)
    for path in text_paths:
        body = path.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN:
            if token in body and path.name != "validate.py" and path.name != "manifest.json" and path.name != "provenance.md":
                fail(f"forbidden token {token!r} in {path.relative_to(ROOT)}")

    print("PASS: 192 recipes; expected slice counts; unique IDs; source links; entity coverage; no forbidden exports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
