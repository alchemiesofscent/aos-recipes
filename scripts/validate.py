#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True

from quantity_gold import validate_repository_overlay

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    "dioscorides_book1_perfumes_resins": 52,
    "dioscorides_book2_fats": 18,
    "aetius_book1_oils": 43,
    "aetius_book16_myrepsika": 45,
    "paul_book7_perfumes": 35,
}
FORBIDDEN = ("parallel-viewer", "experiments/.codex", "__pycache__")
CONCRETE_PROCESS_RAW_UNIT_HINTS = (
    "𐆄",
    "οὐγγ",
    "κοτύλ",
    "κυάθ",
    "λίτρ",
    "ξέστ",
    "ξέστ",
    "xestes",
    "cotyle",
    "cyathos",
    "litra",
    "uncia",
)


def quantity_haystack(payload: dict) -> str:
    return " ".join(value for value in (payload.get("text"), payload.get("original_text")) if value)


def quantity_source_anchored(payload: dict, quantity: dict) -> bool:
    source_span = quantity.get("source_span") or ""
    return bool(source_span) and source_span in quantity_haystack(payload)


def concrete_process_quantity(quantity: dict) -> bool:
    normalized_unit = quantity.get("normalized_unit")
    if normalized_unit and normalized_unit != "descriptor":
        return True
    raw = " ".join(
        value
        for value in (quantity.get("raw_unit"), quantity.get("source_span"))
        if value
    )
    return any(hint in raw for hint in CONCRETE_PROCESS_RAW_UNIT_HINTS)


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
    if len(recipes) != 193:
        fail(f"expected 193 recipes, found {len(recipes)}")

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

    for required_path in (
        ROOT / "data" / "metrology" / "units.json",
        ROOT / "provenance" / "source" / "docs" / "weights-and-measures.tsv",
        ROOT / "data" / "review" / "quantity_gold" / "schema.json",
    ):
        if not required_path.exists():
            fail(f"missing required quantity authority support file: {required_path.relative_to(ROOT)}")

    ABBREV_UNIT_PREFIX = {"γο": "uncia", "ξε": "xestes", "λι": "litra"}
    DESCRIPTOR_SPANS = {
        "τὸ ἀρκοῦν", "τὸ ἴσον", "τὸ αὐτό", "τὸ ἴσον πλῆθος",
        "ὀλίγου", "πολλοὺς", "ἴσον τῷ σταθμῷ", "τὸν ἴσον σταθμὸν",
        "τὸ ἱκανὸν", "τὸ ἱκανόν", "ὅσον ἂν δόξῃ", "ὀλίγα", "ἴσον δὲ τῷ χυλῷ",
        "ἴσον", "ἴσῳ", "ἶσον ἴσῳ", "πλεῖον", "τοσοῦτον", "δίς", "τρὶς",
        "διπλασίονι", "τὸ διπλοῦν", "τὸ τέταρτον", "τὸ τρίτον μέρος",
        "τὸ ἄλλο τρίτον", "τὸ τελευταῖον τρίτον", "τῷ τρίτῳ τοῦ ἐλαίου",
        "μέρος ἕν", "μέρος ἓν ἥμισυ", "τοσοῦτον, ὅσον ἦν ὁ ἔμπροσθεν δοθείς",
    }
    DESCRIPTOR_RAW_UNITS = {"πλῆθος", "μέρος"}
    WEIGHT_INDICATOR_RAW_UNITS = {"σταθμόν", "σταθμὸν", "τῷ σταθμῷ"}
    INFUSION_RAW_UNITS = {"ἐμβολὰς", "ἐμβολάς", "ἐμβολή"}
    DISCRETE_UNITS = {"κέγχρους": "kenchros", "κόκκους": "kokkos", "δακτύλους": "daktylos", "δάκτυλος": "daktylos", "δάκτυλον": "daktylos"}
    DURATION_UNITS = {"ἡμέρας", "ὥρας", "ἡμέρας καὶ νύκτας"}

    def check_quantity_invariants(file_payload, recipe_id):
        for host in ("ingredients", "processes", "materials"):
            for item in file_payload.get(host) or []:
                for q in item.get("quantities") or []:
                    raw_unit = q.get("raw_unit") or ""
                    source_span = q.get("source_span") or ""
                    norm = q.get("normalized_unit")
                    if not quantity_source_anchored(file_payload, q):
                        fail(f"{recipe_id}: quantity source_span not found in text/original_text: {q}")
                    if host == "processes" and item.get("target_type") == "ingredient" and concrete_process_quantity(q):
                        fail(f"{recipe_id}: ingredient-targeted process quantity should be on ingredient: {q}")
                    for prefix, expected_unit in ABBREV_UNIT_PREFIX.items():
                        if raw_unit.startswith(prefix) and norm != expected_unit:
                            fail(f"{recipe_id}: {prefix}-prefixed unit not normalized to {expected_unit}: {q}")
                    if (source_span in DESCRIPTOR_SPANS or raw_unit in DESCRIPTOR_RAW_UNITS) and norm != "descriptor":
                        fail(f"{recipe_id}: descriptor quantifier not tagged: {q}")
                    if norm == "descriptor" and not q.get("descriptor_family"):
                        fail(f"{recipe_id}: descriptor entry missing descriptor_family: {q}")
                    if raw_unit in DURATION_UNITS and host == "processes":
                        fail(f"{recipe_id}: duration entry still in processes.quantities (should be in durations): {q}")
                    if raw_unit in WEIGHT_INDICATOR_RAW_UNITS and source_span not in DESCRIPTOR_SPANS:
                        fail(f"{recipe_id}: by-weight indicator still in quantities (should be in qualifiers): {q}")
                    if raw_unit in INFUSION_RAW_UNITS:
                        fail(f"{recipe_id}: infusion still in quantities (should be in qualifiers): {q}")
                    if raw_unit in DISCRETE_UNITS and norm != DISCRETE_UNITS[raw_unit]:
                        fail(f"{recipe_id}: discrete unit {raw_unit!r} not normalized to {DISCRETE_UNITS[raw_unit]!r}: {q}")

    def check_mirror_parity(file_payload, mirror_payload, recipe_id):
        def quantity_view(payload):
            view = {}
            for host in ("ingredients", "processes", "materials"):
                view[host] = []
                for item in payload.get(host) or []:
                    key = item.get(f"{host[:-1]}_urn") or item.get(f"{host[:-1]}_id")
                    view[host].append({
                        "key": key,
                        "quantities": item.get("quantities") or [],
                        "durations": item.get("durations") or [],
                    })
            return view
        if quantity_view(file_payload) != quantity_view(mirror_payload):
            fail(f"{recipe_id}: provenance mirror has different quantities/durations from canonical")

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
        check_quantity_invariants(file_payload, recipe_id)
        check_mirror_parity(file_payload, load(provenance_file), recipe_id)

    quantity_gold_errors = validate_repository_overlay(
        require_complete=False,
        require_canonical_coverage=False,
    )
    if quantity_gold_errors:
        fail(f"quantity-gold overlay validation failed: {quantity_gold_errors[0]}")

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

    print("PASS: 193 recipes; expected slice counts; unique IDs; source links; entity coverage; no forbidden exports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
