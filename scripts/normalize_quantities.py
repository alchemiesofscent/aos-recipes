#!/usr/bin/env python3
"""Deterministic quantity-unit normalization for data/recipes/*.json.

Pass 2 (extended) — resolves the remaining residuals from pass 1 while keeping pass 1 idempotent.

Rules applied (in order; idempotent):
  1.  γο family    → normalized_unit "uncia"      (Greek ounce abbreviation, fused-numeral suffix allowed)
  1b. ξε family    → normalized_unit "xestes"     (analogous; fills null entries only)
  1c. λι family    → normalized_unit "litra"      (analogous; fills null entries only; splits raw_unit/raw_number per user rule λιστ.= λι + στ = 6)
  2.  Descriptors  → normalized_unit "descriptor" + descriptor_family
          comparison:    same_as, more_than (less_than reserved)
          approximation: as_much_as, a_little, many
          fractions:     fraction:half, fraction:third, fraction:fourth, part
          multipliers:   multiple:two, multiple:three
          relative_to:   παρὰ-comparison cases
          quantity_unspecified: bare πλῆθος
  3.  Durations on processes → moved to processes[i].durations[] with day/hour/day_and_night
  4.  Discrete units → kenchros / kokkos / daktylos (Greek transliteration)
  5.  Pure σταθμόν-by-weight indicators → moved to host.qualifiers[] (qualifier_type "measurement_mode"); removed from quantities[]
  6.  ἐμβολάς (infusion, per user: not a unit) → moved to host.qualifiers[] (qualifier_type "application_form")

Rewrites canonical recipes under data/recipes/, the byte-for-byte-equivalent quantity content in
provenance/source/derived/recipe_entities/*.json, and the combined data/recipes.json index.
Writes a markdown report covering rule counts and any residual unresolved entries (bare numerals,
fractional symbol 𐅵, deliberate hold-backs).
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


def nfc(s):
    """NFC-normalize a string for comparison; pass through non-strings."""
    return unicodedata.normalize("NFC", s) if isinstance(s, str) else s


def nfc_set(items):
    return {nfc(x) for x in items}


def nfc_map(d):
    return {nfc(k): v for k, v in d.items()}

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "data" / "recipes"
COMBINED_PATH = ROOT / "data" / "recipes.json"
MIRROR_DIR = ROOT / "provenance" / "source" / "derived" / "recipe_entities"
REPORT_DIR = ROOT / "provenance" / "normalization"

# ---------------------------------------------------------------------------
# Rule 1, 1b, 1c — abbreviated unit regexes (γο / ξε / λι + Greek numeral suffix)

GO_RE = re.compile(r"^γο[Ͱ-Ͽἀ-῿ʹʹ.]*\.?$")
XE_RE = re.compile(r"^ξε[Ͱ-Ͽἀ-῿ʹʹ.]*\.?$")
LI_RE = re.compile(r"^λι[Ͱ-Ͽἀ-῿ʹʹ.]*\.?$")
GO_UNRESOLVED_NOTE = "The abbreviated unit γο is unresolved."

# Greek alphabetic-numeral letter values (additive). Stigma (ϛ) and the digraph στ both = 6.
GREEK_NUM_LETTERS = {
    "α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ϛ": 6, "ζ": 7, "η": 8, "θ": 9,
    "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60, "ο": 70, "π": 80, "ϟ": 90,
    "ρ": 100, "σ": 200, "τ": 300, "υ": 400, "φ": 500, "χ": 600, "ψ": 700, "ω": 800,
}

def parse_greek_numeral(s: str):
    """Parse an additive Greek alphabetic numeral (e.g. 'στ'=6, 'κστ'=26). 'στ' = 6 as a digraph for ϛ."""
    if not s:
        return None
    s = s.strip().rstrip(".ʹ")
    total = 0
    i = 0
    while i < len(s):
        # Handle 'στ' digraph as 6
        if s[i : i + 2] == "στ":
            total += 6
            i += 2
            continue
        ch = s[i]
        if ch in GREEK_NUM_LETTERS:
            total += GREEK_NUM_LETTERS[ch]
            i += 1
        else:
            return None
    return total if total > 0 else None


# ---------------------------------------------------------------------------
# Rule 2 — descriptor taxonomy (family per literal phrase / raw_unit)

DESCRIPTOR_SPAN_FAMILY = {
    # Comparison: same_as
    "ἴσον": "same_as",
    "ἴσῳ": "same_as",
    "ἶσον ἴσῳ": "same_as",
    "τὸ ἴσον": "same_as",
    "τὸ αὐτό": "same_as",
    "ἴσον τῷ σταθμῷ": "same_as",
    "τὸν ἴσον σταθμὸν": "same_as",
    "ἴσον δὲ τῷ χυλῷ": "same_as",
    "τὸ ἴσον πλῆθος": "same_as",
    # Comparison: more_than
    "πλεῖον": "more_than",
    # Approximation: as_much_as
    "τὸ ἀρκοῦν": "as_much_as",
    "τὸ ἱκανὸν": "as_much_as",
    "τὸ ἱκανόν": "as_much_as",
    "ὅσον ἂν δόξῃ": "as_much_as",
    "τοσοῦτον": "as_much_as",
    "τοσοῦτον, ὅσον ἦν ὁ ἔμπροσθεν δοθείς": "as_much_as",
    # Approximation: a_little
    "ὀλίγου": "a_little",
    "ὀλίγα": "a_little",
    # Approximation: many
    "πολλοὺς": "many",
    # Fractions
    "μέρος ἓν ἥμισυ": "fraction:half",  # "one and a half parts"
    "τὸ τρίτον μέρος": "fraction:third",
    "τὸ ἄλλο τρίτον": "fraction:third",
    "τὸ τελευταῖον τρίτον": "fraction:third",
    "τῷ τρίτῳ τοῦ ἐλαίου": "fraction:third",
    "τὸ τέταρτον": "fraction:fourth",
    "μέρος ἕν": "part",
    # Multipliers
    "δίς": "multiple:two",
    "διπλασίονι": "multiple:two",
    "τὸ διπλοῦν": "multiple:two",
    "τρὶς": "multiple:three",
}

DESCRIPTOR_RAW_UNIT_FAMILY = {
    "πλῆθος": "quantity_unspecified",
    "μέρος": "part",
}


# ---------------------------------------------------------------------------
# Rule 3 — process duration units

DURATION_UNIT_MAP = {
    "ἡμέρας": "day",
    "ὥρας": "hour",
    "ἡμέρας καὶ νύκτας": "day_and_night",
}


# ---------------------------------------------------------------------------
# Rule 4 — discrete-count units (Greek transliteration per user)

DISCRETE_UNIT_MAP = {
    "κέγχρους": "kenchros",  # millet seed
    "κόκκους": "kokkos",     # grain
    "δάκτυλος": "daktylos",  # finger-breadth (length)
    "δάκτυλον": "daktylos",
    "δακτύλους": "daktylos",
}


# ---------------------------------------------------------------------------
# Rule 5, 6 — entries to relocate from quantities[] into qualifiers[]

WEIGHT_INDICATOR_RAW_UNITS = {"σταθμόν", "σταθμὸν", "τῷ σταθμῷ"}  # pure "by weight" — same_as cases stay as descriptors
INFUSION_RAW_UNITS = {"ἐμβολὰς", "ἐμβολάς", "ἐμβολή"}
INFUSION_SPANS = {"τρεῖς ἐμβολὰς"}


# ---------------------------------------------------------------------------
# Rule 7 — παρὰ-comparison (relative_to a reference ingredient)

PARA_RE = re.compile(r"^παρ[άὰ][άὰ]?\s*τ[ὸό]")  # tolerates the παράὰ typo seen in source data


# ---------------------------------------------------------------------------
# Rule 8 — per-recipe manual overrides for bare-numeral cases the user disambiguated.
# Each entry pins a specific (recipe_id, ingredient normalized_label, source_span) to a unit.

MANUAL_COUNT_OVERRIDES = [
    # User: plural countable ingredients given as bare numerals
    ("aetius-1-132", "κάρυον ἰνδικόν", "β"),    # 2 Indian nuts
    ("aetius-16-141", "ἰσχάδες μέλαναι", "ν."),  # 50 black figs
    ("aetius-16-142", "κάρυα ἰνδικά", "γ."),    # 3 Indian nuts
]

# User note for aetius-1-133 ἔλαιον "𐅵 κ" — keep unresolved with explanatory note.
HALF_GLYPH_NOTE = (
    "Wellmann notes a variant reading with ξεστ- here. The printed glyph 𐅵 (U+10175 GREEK ONE HALF SIGN) "
    "is unclear in the source; kept as printed pending better glyph evidence."
)


# ---------------------------------------------------------------------------

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def matches_re(value, regex) -> bool:
    return isinstance(value, str) and regex.match(value) is not None


DESCRIPTOR_SPAN_FAMILY_NFC = nfc_map(DESCRIPTOR_SPAN_FAMILY)
DESCRIPTOR_RAW_UNIT_FAMILY_NFC = nfc_map(DESCRIPTOR_RAW_UNIT_FAMILY)
DURATION_UNIT_MAP_NFC = nfc_map(DURATION_UNIT_MAP)
DISCRETE_UNIT_MAP_NFC = nfc_map(DISCRETE_UNIT_MAP)
WEIGHT_INDICATOR_RAW_UNITS_NFC = nfc_set(WEIGHT_INDICATOR_RAW_UNITS)
INFUSION_RAW_UNITS_NFC = nfc_set(INFUSION_RAW_UNITS)
INFUSION_SPANS_NFC = nfc_set(INFUSION_SPANS)


def classify(q: dict):
    """Return one of: ('resolve_uncia',), ('resolve_xestes', raw_unit, raw_number, normnum),
    ('resolve_litra', raw_unit, raw_number, normnum), ('descriptor', family), ('duration', dkey),
    ('discrete', unit), ('weight_indicator',), ('infusion',), ('relative_to',), ('correct_litra', raw_number, normnum), or None.

    Decisions look at raw_unit + source_span. Resolved entries (normalized_unit already set
    correctly) return None so the rule is a no-op (idempotent).
    """
    raw_unit_nfc = nfc(q.get("raw_unit"))
    source_span_nfc = nfc(q.get("source_span"))
    raw_unit = q.get("raw_unit")  # preserve original for actions that need the unmodified value
    source_span = q.get("source_span")
    norm = q.get("normalized_unit")

    # Rules 1 / 1b / 1c (γο, ξε, λι abbreviated units) are handled in normalize_abbrev_inplace
    # which runs before classify(); classify() handles the remaining rules.

    # Rule 3 — duration units
    if isinstance(raw_unit_nfc, str) and raw_unit_nfc in DURATION_UNIT_MAP_NFC:
        return ("duration", DURATION_UNIT_MAP_NFC[raw_unit_nfc])

    # Rule 4 — discrete units
    if isinstance(raw_unit_nfc, str) and raw_unit_nfc in DISCRETE_UNIT_MAP_NFC:
        if norm != DISCRETE_UNIT_MAP_NFC[raw_unit_nfc]:
            return ("discrete", DISCRETE_UNIT_MAP_NFC[raw_unit_nfc])

    # Rule 5 — pure weight indicator (not same_as cases, which stay as descriptors)
    if isinstance(raw_unit_nfc, str) and raw_unit_nfc in WEIGHT_INDICATOR_RAW_UNITS_NFC and source_span_nfc not in DESCRIPTOR_SPAN_FAMILY_NFC:
        return ("weight_indicator",)

    # Rule 6 — infusion
    if (isinstance(raw_unit_nfc, str) and raw_unit_nfc in INFUSION_RAW_UNITS_NFC) or source_span_nfc in INFUSION_SPANS_NFC:
        return ("infusion",)

    # Rule 7 — παρὰ-comparison
    if isinstance(raw_unit, str) and PARA_RE.match(raw_unit):
        if norm != "descriptor" or q.get("descriptor_family") != "relative_to":
            return ("relative_to",)
        return None

    # Rule 2 — descriptor with family. source_span lookup wins over raw_unit fallback (more specific).
    family = None
    if isinstance(source_span_nfc, str) and source_span_nfc in DESCRIPTOR_SPAN_FAMILY_NFC:
        family = DESCRIPTOR_SPAN_FAMILY_NFC[source_span_nfc]
    elif isinstance(raw_unit_nfc, str) and raw_unit_nfc in DESCRIPTOR_RAW_UNIT_FAMILY_NFC:
        family = DESCRIPTOR_RAW_UNIT_FAMILY_NFC[raw_unit_nfc]
    elif norm == "descriptor" and not q.get("descriptor_family"):
        # Legacy entry tagged in v1 without a family — assign best-effort fallback.
        family = "unspecified"
    if family is not None and (norm != "descriptor" or q.get("descriptor_family") != family):
        return ("descriptor", family)

    return None


_SPURIOUS_CORRECTION_RE = re.compile(
    r"Corrected by normalize_quantities\.py: raw_number '(?P<a>.+?)'→'(?P<b>.+?)', normalized_number (?P<x>\S+)→(?P<y>\S+)"
)


def cleanup_spurious_correction_notes(q: dict, tally: Counter) -> None:
    """Strip notes from a previous buggy run that 'corrected' raw_number whitespace without changing the value."""
    notes = q.get("notes") or []
    if not notes:
        return
    cleaned = []
    any_removed = False
    for n in notes:
        m = _SPURIOUS_CORRECTION_RE.search(n) if isinstance(n, str) else None
        if m and m.group("x") == m.group("y") and m.group("a").strip(" .") == m.group("b").strip(" ."):
            any_removed = True
            continue
        cleaned.append(n)
    if any_removed:
        q["notes"] = cleaned
        if isinstance(q.get("raw_number"), str):
            q["raw_number"] = q["raw_number"].strip()
        tally["cleanup_spurious_notes_removed"] += 1


_ABBREV_FAMILIES = [
    # (prefix, normalized_unit_name, tally_key_prefix)
    ("γο", "uncia", "rule1_go"),
    ("ξε", "xestes", "rule1b_xestes"),
    ("λι", "litra", "rule1c_litra"),
]


def normalize_abbrev_inplace(q: dict, tally: Counter) -> bool:
    """Idempotently normalize a γο/ξε/λι-family quantity entry.

    The canonical post-shape is:
      raw_unit = "γο" | "ξε" | "λι"
      raw_number = the Greek numeral string (no whitespace, no trailing period)
      normalized_number = parsed int
      normalized_unit = "uncia" | "xestes" | "litra"
    The original spelling is preserved verbatim in source_span (untouched).

    Returns True if any field changed.
    """
    raw_unit = q.get("raw_unit") or ""
    source_span = q.get("source_span") or ""
    matched = None
    for prefix, unit_name, key_prefix in _ABBREV_FAMILIES:
        if (raw_unit == prefix
                or (isinstance(raw_unit, str) and raw_unit.startswith(prefix) and matches_re(raw_unit, _PREFIX_RE[prefix]))
                or (raw_unit in (None, "") and isinstance(source_span, str) and matches_re(source_span, _PREFIX_RE[prefix]))):
            matched = (prefix, unit_name, key_prefix)
            break
    if not matched:
        return False
    prefix, unit_name, key_prefix = matched

    # Gather candidate numeral strings in priority order: source_span suffix > raw_unit suffix > raw_number.
    candidates: list[str] = []
    if isinstance(source_span, str) and source_span.startswith(prefix):
        candidates.append(source_span[len(prefix):].strip(" ").rstrip("."))
    if isinstance(raw_unit, str) and raw_unit.startswith(prefix) and raw_unit != prefix:
        candidates.append(raw_unit[len(prefix):].strip(" ").rstrip("."))
    if q.get("raw_number"):
        candidates.append(str(q["raw_number"]).strip(" ").rstrip("."))
    parsed_str = None
    parsed_num = None
    for cand in candidates:
        if not cand:
            continue
        n = parse_greek_numeral(cand)
        if n is not None:
            parsed_str = cand
            parsed_num = n
            break

    changed_fields = []
    old_raw_unit = q.get("raw_unit")
    old_raw_number = q.get("raw_number")
    old_norm_number = q.get("normalized_number")
    old_norm_unit = q.get("normalized_unit")

    if old_raw_unit != prefix:
        q["raw_unit"] = prefix
        changed_fields.append("raw_unit")
    if parsed_str and old_raw_number != parsed_str:
        q["raw_number"] = parsed_str
        changed_fields.append("raw_number")
    if parsed_num is not None and old_norm_number != parsed_num:
        q["normalized_number"] = parsed_num
        changed_fields.append("normalized_number")
    if old_norm_unit != unit_name:
        q["normalized_unit"] = unit_name
        changed_fields.append("normalized_unit")

    # Strip the legacy γο-unresolved note now that we've resolved the unit.
    if prefix == "γο":
        notes = q.get("notes") or []
        if GO_UNRESOLVED_NOTE in notes:
            q["notes"] = [n for n in notes if n != GO_UNRESOLVED_NOTE]
            changed_fields.append("notes")

    if not changed_fields:
        return False

    # Record an audit note only when we changed a value that was previously non-null and different
    # (i.e. a genuine correction, not a fill-in of a null), so that fills don't accumulate noise.
    real_correction = (
        (old_norm_number is not None and "normalized_number" in changed_fields and old_norm_number != parsed_num)
        or (old_raw_number not in (None, "") and "raw_number" in changed_fields and str(old_raw_number).strip(" .") != parsed_str)
    )
    if real_correction:
        note = (
            f"Corrected by normalize_quantities.py (rule {prefix}+numeral): "
            f"raw_number {old_raw_number!r}→{parsed_str!r}, "
            f"normalized_number {old_norm_number}→{parsed_num}."
        )
        notes = q.get("notes") or []
        if note not in notes:
            q["notes"] = notes + [note]
        tally[f"{key_prefix}_corrected"] += 1
    else:
        tally[f"{key_prefix}_filled"] += 1
    return True


_PREFIX_RE = {
    "γο": GO_RE,
    "ξε": XE_RE,
    "λι": LI_RE,
}


def apply_manual_overrides(record: dict, host_kind: str, host_obj: dict, q: dict, tally: Counter) -> None:
    """Apply user-specified per-recipe overrides for ambiguous bare-numeral entries."""
    recipe_id = record.get("recipe_id")
    item_label = nfc(host_obj.get("normalized_label") or "")
    span = nfc(q.get("source_span") or "")
    for r_id, label, source_span in MANUAL_COUNT_OVERRIDES:
        if recipe_id == r_id and item_label == nfc(label) and span == nfc(source_span):
            if q.get("normalized_unit") != "count":
                q["normalized_unit"] = "count"
                tally["rule8_manual_count"] += 1
            return
    # aetius-1-133 ἔλαιον "𐅵 κ": keep raw_unit/normalized_unit as-is but add the note.
    if recipe_id == "aetius-1-133" and item_label == nfc("ἔλαιον") and span == nfc("𐅵 κ"):
        notes = q.get("notes") or []
        if HALF_GLYPH_NOTE not in notes:
            q["notes"] = notes + [HALF_GLYPH_NOTE]
            tally["rule8_half_note_added"] += 1


def normalize_record(record: dict, tally: Counter, host_warnings: list) -> None:
    def process_host(host_kind: str, host_obj: dict):
        kept = []
        durations_to_move = []
        qualifiers_to_add = []
        for q in host_obj.get("quantities") or []:
            cleanup_spurious_correction_notes(q, tally)
            normalize_abbrev_inplace(q, tally)
            apply_manual_overrides(record, host_kind, host_obj, q, tally)
            decision = classify(q)
            if decision is None:
                kept.append(q)
                continue
            kind = decision[0]
            if kind == "descriptor":
                _, family = decision
                if q.get("normalized_unit") != "descriptor":
                    tally["rule2_descriptor_tagged"] += 1
                if q.get("descriptor_family") != family:
                    tally["rule2_descriptor_family_set"] += 1
                q["normalized_unit"] = "descriptor"
                q["descriptor_family"] = family
                kept.append(q)
            elif kind == "duration":
                _, dkey = decision
                if host_kind != "processes":
                    host_warnings.append(
                        f"{record.get('recipe_id')}: duration entry found on {host_kind}, leaving in place: {q.get('source_span')!r}"
                    )
                    kept.append(q)
                    continue
                q["normalized_unit"] = dkey
                durations_to_move.append(q)
                tally["rule3_durations_moved"] += 1
            elif kind == "discrete":
                _, unit = decision
                q["normalized_unit"] = unit
                tally["rule4_discrete_resolved"] += 1
                kept.append(q)
            elif kind == "weight_indicator":
                qualifiers_to_add.append({
                    "qualifier_type": "measurement_mode",
                    "source_span": q.get("source_span"),
                    "normalized_value": "by_weight",
                    "certainty": q.get("certainty") or "certain",
                    "notes": q.get("notes") or [],
                })
                tally["rule5_weight_moved"] += 1
            elif kind == "infusion":
                qualifiers_to_add.append({
                    "qualifier_type": "application_form",
                    "source_span": q.get("source_span"),
                    "normalized_value": "infusion",
                    "count": q.get("normalized_number"),
                    "certainty": q.get("certainty") or "certain",
                    "notes": q.get("notes") or [],
                })
                tally["rule6_infusion_moved"] += 1
            elif kind == "relative_to":
                q["normalized_unit"] = "descriptor"
                q["descriptor_family"] = "relative_to"
                tally["rule7_relative_to_tagged"] += 1
                kept.append(q)
            else:
                kept.append(q)

        host_obj["quantities"] = kept
        if durations_to_move:
            host_obj["durations"] = (host_obj.get("durations") or []) + durations_to_move
        if qualifiers_to_add:
            existing_quals = host_obj.get("qualifiers") or []
            # Avoid duplicates on re-runs: skip if an identical qualifier (by type+source_span) already present.
            existing_keys = {(qq.get("qualifier_type"), qq.get("source_span")) for qq in existing_quals}
            new_quals = [qq for qq in qualifiers_to_add if (qq["qualifier_type"], qq["source_span"]) not in existing_keys]
            if new_quals:
                host_obj["qualifiers"] = existing_quals + new_quals

    for ing in record.get("ingredients") or []:
        process_host("ingredients", ing)
    for proc in record.get("processes") or []:
        process_host("processes", proc)
    for mat in record.get("materials") or []:
        process_host("materials", mat)


def refresh_quantity_display(canonical: dict) -> None:
    """Recompute entity_groups.ingredients[].quantity_display when it still references unresolved γο."""
    groups = canonical.get("entity_groups") or {}
    group_ings = groups.get("ingredients") or []
    by_urn = {ing.get("ingredient_urn"): ing for ing in canonical.get("ingredients") or []}
    for g in group_ings:
        display = g.get("quantity_display", "")
        if not isinstance(display, str) or "γο" not in display:
            continue
        ing = by_urn.get(g.get("entity_urn"))
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
            normalize_record(mirror, Counter(), [])
            if json.dumps(mirror, ensure_ascii=False, sort_keys=True) != mirror_before:
                dump(mpath, mirror)
                files_touched_mirror += 1

    combined = load(COMBINED_PATH)
    combined["recipes"] = [load(p) for p in canonical_files]
    if "metadata" in combined and isinstance(combined["metadata"], dict):
        combined["metadata"]["exported_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dump(COMBINED_PATH, combined)

    # Tally residuals.
    residual = Counter()
    family_dist = Counter()
    for cpath in canonical_files:
        rec = load(cpath)
        for host in ("ingredients", "processes", "materials"):
            for item in rec.get(host) or []:
                for q in item.get("quantities") or []:
                    if q.get("normalized_unit") is None:
                        key = (q.get("raw_unit") or "<null>", q.get("source_span") or "")
                        residual[key] += 1
                    if q.get("descriptor_family"):
                        family_dist[q["descriptor_family"]] += 1

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"qty-resolve-{today}.md"
    lines = [
        f"# Quantity normalization pass — {today}",
        "",
        "Run by `scripts/normalize_quantities.py`. Deterministic post-processing; no LLM calls. Idempotent.",
        "",
        "## Rules",
        "",
        "1. **γο → uncia.** `raw_unit` or `source_span` matching `γο` + Greek numeral suffix.",
        "1b. **ξε → xestes.** Same shape, e.g. *ξεα.* = xestes·1.",
        "1c. **λι → litra.** Per user rule, *λιστ.* = λι + στ = litra·6. Where existing entries had read *ιστ* as the numeral (=16), they are corrected to *στ* (=6) with a note recording the prior value.",
        "2. **Descriptors → `normalized_unit: \"descriptor\"` + `descriptor_family`.** Families:"
        " `same_as`, `more_than`, `less_than` (reserved); `as_much_as`, `a_little`, `many`;"
        " `fraction:half`, `fraction:third`, `fraction:fourth`, `part`;"
        " `multiple:two`, `multiple:three`; `relative_to`; `quantity_unspecified`.",
        "3. **Durations** (*ἡμέρας / ὥρας / ἡμέρας καὶ νύκτας*) moved out of `processes[i].quantities` into `processes[i].durations` with `day / hour / day_and_night`.",
        "4. **Discrete units** → Greek-transliteration names: *κέγχρους* → `kenchros`, *κόκκους* → `kokkos`, *δακτύλους* → `daktylos`.",
        "5. **By-weight indicators** (*σταθμόν / σταθμὸν / τῷ σταθμῷ*) moved from `quantities[]` into `qualifiers[]` with `qualifier_type: \"measurement_mode\"`, `normalized_value: \"by_weight\"`. The *ἴσον τῷ σταθμῷ* variants stay in `quantities[]` as `descriptor_family: \"same_as\"`.",
        "6. **ἐμβολάς (infusion)** moved from `quantities[]` into `qualifiers[]` with `qualifier_type: \"application_form\"`, `normalized_value: \"infusion\"`, `count: <n>`. Per user: infusion is not a unit.",
        "",
        "## Counts",
        "",
        f"- Rule 1 γο → uncia: filled **{tally['rule1_go_filled']}**, corrected **{tally['rule1_go_corrected']}** entries.",
        f"- Rule 1b ξε → xestes: filled **{tally['rule1b_xestes_filled']}**, corrected **{tally['rule1b_xestes_corrected']}** entries.",
        f"- Rule 1c λι → litra: filled **{tally['rule1c_litra_filled']}**, corrected **{tally['rule1c_litra_corrected']}** entries.",
        f"- Rule 8 manual count overrides: **{tally['rule8_manual_count']}** entries; explanatory note added: **{tally['rule8_half_note_added']}** entries.",
        f"- Cleanup (stale whitespace-only notes removed): **{tally['cleanup_spurious_notes_removed']}** entries.",
        f"- Rule 2 descriptor tagged: **{tally['rule2_descriptor_tagged']}** entries (family newly set: **{tally['rule2_descriptor_family_set']}**).",
        f"- Rule 3 durations moved: **{tally['rule3_durations_moved']}** entries.",
        f"- Rule 4 discrete units resolved: **{tally['rule4_discrete_resolved']}** entries.",
        f"- Rule 5 by-weight moved to qualifiers: **{tally['rule5_weight_moved']}** entries.",
        f"- Rule 6 infusion moved to qualifiers: **{tally['rule6_infusion_moved']}** entries.",
        f"- Rule 7 relative-to tagged: **{tally['rule7_relative_to_tagged']}** entries.",
        f"- Canonical files rewritten: **{files_touched_canonical}**.",
        f"- Provenance mirrors rewritten: **{files_touched_mirror}**.",
        "",
        "## Descriptor family distribution (post-pass)",
        "",
    ]
    if family_dist:
        lines.append("| family | count |")
        lines.append("|--------|------:|")
        for fam, n in sorted(family_dist.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| `{fam}` | {n} |")
    else:
        lines.append("None.")
    lines.append("")
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
        lines.append("| count | raw_unit | source_span | notes |")
        lines.append("|------:|----------|-------------|-------|")
        for (ru, ss), n in sorted(residual.items(), key=lambda kv: (-kv[1], kv[0])):
            note = ""
            if ru == "<null>" and ss in {"β", "γ.", "ν."}:
                note = "bare Greek numeral, no unit context (deferred per user)"
            elif ru == "𐅵":
                note = "fractional half symbol 𐅵 (U+10175) — needs human review"
            lines.append(f"| {n} | `{ru}` | `{ss}` | {note} |")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Rule 1  γο → uncia:        filled {tally['rule1_go_filled']}, corrected {tally['rule1_go_corrected']}")
    print(f"Rule 1b ξε → xestes:       filled {tally['rule1b_xestes_filled']}, corrected {tally['rule1b_xestes_corrected']}")
    print(f"Rule 1c λι → litra:        filled {tally['rule1c_litra_filled']}, corrected {tally['rule1c_litra_corrected']}")
    print(f"Rule 8  manual count:      {tally['rule8_manual_count']}  (half-glyph note added: {tally['rule8_half_note_added']})")
    print(f"Cleanup stale notes:       {tally['cleanup_spurious_notes_removed']}")
    print(f"Rule 2  descriptor tagged: {tally['rule2_descriptor_tagged']}  (family set: {tally['rule2_descriptor_family_set']})")
    print(f"Rule 3  durations moved:   {tally['rule3_durations_moved']}")
    print(f"Rule 4  discrete resolved: {tally['rule4_discrete_resolved']}")
    print(f"Rule 5  by-weight moved:   {tally['rule5_weight_moved']}")
    print(f"Rule 6  infusion moved:    {tally['rule6_infusion_moved']}")
    print(f"Rule 7  relative-to:       {tally['rule7_relative_to_tagged']}")
    print(f"Canonical files rewritten: {files_touched_canonical}")
    print(f"Mirror files rewritten:    {files_touched_mirror}")
    print(f"Residual unresolved:       {sum(residual.values())} entries ({len(residual)} distinct)")
    print(f"Report: {report_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
