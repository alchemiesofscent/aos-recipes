#!/usr/bin/env python3
"""Deterministic quantity-unit normalization for data/recipes/*.json.

Applies three rules to existing extracted quantities:
  1. γο family  -> normalized_unit "uncia"          (Greek abbreviation for ounce)
  2. Descriptors -> normalized_unit "descriptor"     (non-numeric quantifiers)
  3. Time-on-process quantities -> processes[i].durations[]  (separate from material amounts)

Updates the canonical recipe JSONs under data/recipes/, the combined data/recipes.json
index, and the byte-for-byte-equivalent quantity content in the provenance mirrors at
provenance/source/derived/recipe_entities/*.json. Writes a markdown report of the run.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "data" / "recipes"
COMBINED_PATH = ROOT / "data" / "recipes.json"
MIRROR_DIR = ROOT / "provenance" / "source" / "derived" / "recipe_entities"
REPORT_DIR = ROOT / "provenance" / "normalization"

GO_RE = re.compile(r"^γο[Ͱ-Ͽἀ-῿ʹʹ.]*\.?$")
GO_UNRESOLVED_NOTE = "The abbreviated unit γο is unresolved."

DESCRIPTOR_SPANS = {
    "τὸ ἀρκοῦν",
    "τὸ ἴσον",
    "τὸ αὐτό",
    "τὸ ἴσον πλῆθος",
    "ὀλίγου",
    "πολλοὺς",
    "ἴσον τῷ σταθμῷ",
    "τὸν ἴσον σταθμὸν",
}
DESCRIPTOR_RAW_UNITS = {"πλῆθος", "σταθμόν", "σταθμὸν", "τῷ σταθμῷ"}

DURATION_UNIT_MAP = {
    "ἡμέρας": "day",
    "ὥρας": "hour",
    "ἡμέρας καὶ νύκτας": "day_and_night",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def is_go(raw_unit, source_span) -> bool:
    if raw_unit == "γο":
        return True
    if isinstance(raw_unit, str) and GO_RE.match(raw_unit):
        return True
    if raw_unit in (None, "") and isinstance(source_span, str) and GO_RE.match(source_span):
        return True
    return False


def is_descriptor(raw_unit, source_span) -> bool:
    if isinstance(source_span, str) and source_span in DESCRIPTOR_SPANS:
        return True
    if isinstance(raw_unit, str) and raw_unit in DESCRIPTOR_RAW_UNITS:
        return True
    return False


def duration_key(raw_unit):
    if isinstance(raw_unit, str) and raw_unit in DURATION_UNIT_MAP:
        return DURATION_UNIT_MAP[raw_unit]
    return None


def normalize_record(record: dict, tally: Counter, host_warnings: list) -> dict:
    """Mutate `record` (a recipe dict) in place; return it. Updates `tally`."""

    def apply_rules_to_quantities(host_kind, host_obj):
        """Apply rules 1 & 2 in place; return (kept, moved_durations)."""
        kept = []
        durations_to_move = []
        for q in host_obj.get("quantities") or []:
            raw_unit = q.get("raw_unit")
            source_span = q.get("source_span")
            # Rule 3 collection (must precede 1 & 2 since durations also have raw_unit=ἡμέρας etc.)
            dkey = duration_key(raw_unit)
            if dkey is not None:
                if host_kind != "process":
                    host_warnings.append(
                        f"{record.get('recipe_id')}: duration entry found on {host_kind}, leaving in place: {source_span!r}"
                    )
                    kept.append(q)
                    continue
                q["normalized_unit"] = dkey
                durations_to_move.append(q)
                tally["rule3_durations_moved"] += 1
                continue
            # Rule 1: γο -> uncia
            if is_go(raw_unit, source_span):
                if q.get("normalized_unit") != "uncia":
                    q["normalized_unit"] = "uncia"
                    tally["rule1_go_resolved"] += 1
                    notes = q.get("notes") or []
                    if GO_UNRESOLVED_NOTE in notes:
                        notes = [n for n in notes if n != GO_UNRESOLVED_NOTE]
                        q["notes"] = notes
                kept.append(q)
                continue
            # Rule 2: descriptor tagging
            if is_descriptor(raw_unit, source_span):
                if q.get("normalized_unit") != "descriptor":
                    q["normalized_unit"] = "descriptor"
                    tally["rule2_descriptor_tagged"] += 1
                kept.append(q)
                continue
            kept.append(q)
        return kept, durations_to_move

    for ing in record.get("ingredients") or []:
        kept, _ = apply_rules_to_quantities("ingredient", ing)
        ing["quantities"] = kept

    for proc in record.get("processes") or []:
        kept, moved = apply_rules_to_quantities("process", proc)
        proc["quantities"] = kept
        if moved:
            existing = proc.get("durations") or []
            proc["durations"] = existing + moved

    for mat in record.get("materials") or []:
        kept, _ = apply_rules_to_quantities("material", mat)
        mat["quantities"] = kept

    return record


def refresh_quantity_display(canonical: dict) -> None:
    """For canonical-only entity_groups.ingredients[].quantity_display, recompute when stale.

    The original display string is opaque (LLM-generated), so we only intervene when the
    display still mentions an unresolved γο form that we just resolved. Recomputed value:
    join of "<normalized_number> <normalized_unit>" for each numeric quantity, space-separated.
    Conservative: leave display untouched unless we detect it contains 'γο'.
    """
    groups = canonical.get("entity_groups") or {}
    group_ings = groups.get("ingredients") or []
    by_urn = {ing.get("ingredient_urn"): ing for ing in canonical.get("ingredients") or []}
    for g in group_ings:
        urn = g.get("entity_urn")
        display = g.get("quantity_display", "")
        if not isinstance(display, str) or "γο" not in display:
            continue
        ing = by_urn.get(urn)
        if not ing:
            continue
        parts = []
        for q in ing.get("quantities") or []:
            num = q.get("normalized_number")
            unit = q.get("normalized_unit")
            if num is not None and unit:
                parts.append(f"{num} {unit}")
        g["quantity_display"] = " · ".join(parts)


def main() -> int:
    canonical_files = sorted(CANONICAL_DIR.glob("*.json"))
    if not canonical_files:
        print("no canonical recipe files found", file=sys.stderr)
        return 1

    tally = Counter()
    host_warnings: list[str] = []
    files_touched_canonical = 0
    files_touched_mirror = 0

    for cpath in canonical_files:
        canonical = load(cpath)
        recipe_id = canonical.get("recipe_id")
        mpath = MIRROR_DIR / f"{recipe_id}.json"
        mirror = load(mpath) if mpath.exists() else None

        canonical_before = json.dumps(canonical, ensure_ascii=False, sort_keys=True)
        normalize_record(canonical, tally, host_warnings)
        refresh_quantity_display(canonical)
        if json.dumps(canonical, ensure_ascii=False, sort_keys=True) != canonical_before:
            dump(cpath, canonical)
            files_touched_canonical += 1

        if mirror is not None:
            mirror_before = json.dumps(mirror, ensure_ascii=False, sort_keys=True)
            normalize_record(mirror, Counter(), [])  # don't double-count; warnings already captured
            if json.dumps(mirror, ensure_ascii=False, sort_keys=True) != mirror_before:
                dump(mpath, mirror)
                files_touched_mirror += 1

    # Rebuild combined index from canonical files, preserving the existing top-level shape.
    combined = load(COMBINED_PATH)
    combined["recipes"] = [load(p) for p in canonical_files]
    if "metadata" in combined and isinstance(combined["metadata"], dict):
        combined["metadata"]["exported_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dump(COMBINED_PATH, combined)

    # Compute residual unresolved tally for report.
    residual = Counter()
    for cpath in canonical_files:
        rec = load(cpath)
        for host in ("ingredients", "processes", "materials"):
            for item in rec.get(host) or []:
                for q in item.get("quantities") or []:
                    if q.get("normalized_unit") is None:
                        key = (q.get("raw_unit") or "<null>", q.get("source_span") or "")
                        residual[key] += 1

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"qty-resolve-{today}.md"
    lines = [
        f"# Quantity normalization pass — {today}",
        "",
        "Run by `scripts/normalize_quantities.py`. Deterministic post-processing; no LLM calls.",
        "",
        "## Rules applied",
        "",
        "1. **γο → uncia.** Any quantity whose `raw_unit` is `γο` (or `γο`+Greek-numeral suffix, "
        "or whose `source_span` matches that shape when `raw_unit` is null) gets `normalized_unit: \"uncia\"`. "
        "The existing `normalized_number` is preserved. The note "
        "`\"The abbreviated unit γο is unresolved.\"` is removed.",
        "2. **Descriptor tagging.** Non-numeric quantifiers (exact match on `source_span` or `raw_unit`) "
        "get `normalized_unit: \"descriptor\"`. Phrases covered: "
        + ", ".join(sorted(f"`{s}`" for s in DESCRIPTOR_SPANS | DESCRIPTOR_RAW_UNITS))
        + ".",
        "3. **Durations onto processes.** Quantities with `raw_unit` in "
        + ", ".join(f"`{k}` (→ `{v}`)" for k, v in DURATION_UNIT_MAP.items())
        + " are removed from `processes[i].quantities` and appended to a new "
        "`processes[i].durations` array (with the mapped `normalized_unit`).",
        "",
        "## Counts",
        "",
        f"- Rule 1 (γο → uncia): **{tally['rule1_go_resolved']}** entries.",
        f"- Rule 2 (descriptor): **{tally['rule2_descriptor_tagged']}** entries.",
        f"- Rule 3 (durations moved): **{tally['rule3_durations_moved']}** entries.",
        f"- Canonical files rewritten: **{files_touched_canonical}**.",
        f"- Provenance mirrors rewritten: **{files_touched_mirror}**.",
        "",
    ]
    if host_warnings:
        lines.append("## Warnings")
        lines.append("")
        for w in host_warnings:
            lines.append(f"- {w}")
        lines.append("")
    lines.append("## Residual unresolved quantities")
    lines.append("")
    if not residual:
        lines.append("None.")
    else:
        lines.append("| count | raw_unit | source_span |")
        lines.append("|------:|----------|-------------|")
        for (ru, ss), n in sorted(residual.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {n} | `{ru}` | `{ss}` |")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Rule 1 γο→uncia: {tally['rule1_go_resolved']} entries")
    print(f"Rule 2 descriptor: {tally['rule2_descriptor_tagged']} entries")
    print(f"Rule 3 durations moved: {tally['rule3_durations_moved']} entries")
    print(f"Canonical files rewritten: {files_touched_canonical}")
    print(f"Mirror files rewritten: {files_touched_mirror}")
    print(f"Residual unresolved: {sum(residual.values())} entries ({len(residual)} distinct)")
    print(f"Report: {report_path.relative_to(ROOT)}")
    if host_warnings:
        print(f"Warnings: {len(host_warnings)} (see report)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
