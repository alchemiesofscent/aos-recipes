#!/usr/bin/env python3
"""Extract all Aetius recipes that use styrax (στύραξ) as an ingredient.

Produces docs/aetius-styrax-recipes.md with a Greek block + structured ingredient
list per recipe. English translations are left as placeholders for hand-writing.

Re-running this script is safe for the Greek/ingredient blocks — but it will
overwrite any hand-written translations. After translations are added, edit the
markdown directly; do not re-run unless the data has changed.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPES_DIR = ROOT / "data" / "recipes"
OUT = ROOT / "docs" / "aetius-styrax-recipes.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aetius_styrax_translations import TRANSLATIONS  # noqa: E402

# Both upsilon-with-tonos (03CD) and upsilon-with-oxia (1F7B) variants occur in the data;
# normalize to NFC before checking.
STYRAX_NEEDLES = tuple(
    unicodedata.normalize("NFC", n) for n in ("στύρα", "Στύρα", "Στυρά", "στυρά")
)
EDITION_NAMES = {"olivieri": "Olivieri", "zervos": "Zervos"}
TRANSLATION_PLACEHOLDER = "> _[translation pending]_"


def has_styrax_ingredient(recipe: dict) -> bool:
    for ing in recipe.get("ingredients", []):
        blob = unicodedata.normalize(
            "NFC",
            (ing.get("normalized_label") or "") + (ing.get("surface_form") or ""),
        )
        if any(n in blob for n in STYRAX_NEEDLES):
            return True
    return False


def format_quantity(q: dict) -> str:
    num = q.get("normalized_number")
    unit = q.get("normalized_unit")
    fam = q.get("descriptor_family")
    if unit == "descriptor":
        if fam == "as_much_as":
            return "q.s. (sufficient quantity)"
        if fam == "same_as":
            return "same as preceding"
        if fam:
            return f"descriptor: {fam}"
        return "descriptor"
    if num is not None and unit:
        return f"{num} {unit}"
    if num is not None and unit is None:
        return f"{num} (unit unresolved)"
    if num is None and unit:
        return unit
    return "(no amount specified)"


def is_distributive(quantities: list) -> bool:
    for q in quantities:
        for note in q.get("notes", []) or []:
            n = note.lower()
            if "distributive" in n or "ἀνὰ" in note or "ἀνά" in note:
                return True
    return False


def format_ingredient_quantity(quantities: list) -> str:
    if not quantities:
        return "(no amount specified)"
    parts = [format_quantity(q) for q in quantities]
    rendered = " or ".join(parts)
    if is_distributive(quantities):
        rendered += " each"
    return rendered


def render_citation(recipe: dict) -> str:
    cit = recipe.get("citation", {}) or {}
    edition = EDITION_NAMES.get(cit.get("edition_key"), cit.get("edition_key", "?"))
    inner = cit.get("citation", {}) or {}
    start, end = inner.get("start", "?"), inner.get("end", "?")
    if start == end:
        return f"{edition} {start}"
    return f"{edition} {start} – {end}"


def sort_key(recipe: dict):
    book = int(recipe.get("book", "0") or 0)
    rid = recipe.get("recipe_id", "")
    parts = rid.split("-")
    chapter = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
    tail = tuple(int(part) if part.isdigit() else 0 for part in parts[3:])
    return (book, chapter, *tail)


def render_recipe(recipe: dict) -> str:
    rid = recipe["recipe_id"]
    lemma = recipe.get("lemma") or recipe.get("chapter_name") or ""
    citation = render_citation(recipe)
    text = (recipe.get("text") or "").strip()

    lines: list[str] = []
    lines.append(f"### `{rid}` — {lemma}")
    lines.append("")
    lines.append(f"**Citation:** {citation}")
    lines.append("")
    lines.append("**Greek:**")
    lines.append("")
    lines.append("> " + text)
    lines.append("")
    lines.append("**Translation:**")
    lines.append("")
    translation = TRANSLATIONS.get(rid)
    if translation:
        lines.append("> " + translation)
    else:
        lines.append(TRANSLATION_PLACEHOLDER)
    lines.append("")
    lines.append("**Ingredients:**")
    lines.append("")
    for idx, ing in enumerate(recipe.get("ingredients", []), 1):
        label = ing.get("normalized_label") or ing.get("surface_form") or "?"
        qty = format_ingredient_quantity(ing.get("quantities", []) or [])
        cert = ing.get("certainty")
        suffix = " _(uncertain)_" if cert == "uncertain" else ""
        lines.append(f"{idx}. **{label}** — {qty}{suffix}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    recipes = []
    for path in sorted(RECIPES_DIR.glob("aetius-*.json")):
        with path.open(encoding="utf-8") as fh:
            recipe = json.load(fh)
        if has_styrax_ingredient(recipe):
            recipes.append(recipe)
    recipes.sort(key=sort_key)

    book1 = [r for r in recipes if r.get("book") == "1"]
    book16 = [r for r in recipes if r.get("book") == "16"]

    out: list[str] = []
    out.append("# Aetius of Amida — Recipes Containing Styrax")
    out.append("")
    out.append(
        "Every recipe in the Aetius corpus that calls for styrax (στύραξ) as an ingredient, "
        "rendered with the original Greek, a literal English translation, and an enumerated "
        "ingredient list with normalized quantities."
    )
    out.append("")
    out.append(
        f"**Scope:** {len(recipes)} recipes — {len(book1)} from Book 1 (oils, ed. Olivieri) and "
        f"{len(book16)} from Book 16 (myrepsika — perfumes and incenses, ed. Zervos). "
        "Generated from `data/recipes/aetius-*.json` via "
        "`scripts/extract_styrax_recipes.py`; translations are hand-written and not auto-regenerated."
    )
    out.append("")
    out.append("## Translation conventions")
    out.append("")
    out.append("Ingredients are rendered using a fixed glossary so that the same Greek lemma "
               "appears as the same English term across all recipes:")
    out.append("")
    out.append("| Greek | English |")
    out.append("| --- | --- |")
    out.append("| στύραξ | styrax |")
    out.append("| στύραξ λιπαρός | fatty styrax |")
    out.append("| στύραξ καλαμίτης | reed-grade styrax (styrax calamites) |")
    out.append("| στύραξ πρωτεῖος | first-quality styrax |")
    out.append("| στύραξ χυμάτιος | liquid styrax |")
    out.append("| στύραξ ἄσπρος | white styrax |")
    out.append("| ναρδόσταχυς | spikenard |")
    out.append("| φύλλον | malabathron-leaf |")
    out.append("| ἄμωμον | amomum |")
    out.append("| κρόκος | saffron |")
    out.append("| καρυόφυλλον / καρυόφυλλα | clove(s) |")
    out.append("| καρποβάλσαμον | balsam-fruit |")
    out.append("| ὀποβάλσαμον | balsam-juice |")
    out.append("| ξυλοβάλσαμον | balsam-wood |")
    out.append("| κόστος | costus |")
    out.append("| ὄνυξ | onycha |")
    out.append("| ἄσαρον | asaron |")
    out.append("| ἀλόη | aloe |")
    out.append("| μαστίχη | mastic |")
    out.append("| λάδανον | ladanum |")
    out.append("| μόσχος | musk |")
    out.append("| ἄμβαρ | ambergris |")
    out.append("| ῥόδα χλωρά | fresh roses |")
    out.append("| ἔλαιον | olive oil |")
    out.append("| γλυκὺ ἔλαιον | sweet olive oil |")
    out.append("| μέλι (ἀττικόν) | (Attic) honey |")
    out.append("| οἶνος εὐώδης | fragrant wine |")
    out.append("| χυλὸς ῥόδων | rose-juice |")
    out.append("| κάλαμος ἰνδικός | Indian reed (sweet flag) |")
    out.append("| κάρυα ἰνδικά | Indian nuts |")
    out.append("| σανδαράχη | sandarach |")
    out.append("| ἀρναβώ | arnabo |")
    out.append("")
    out.append(
        "Units are kept in their Latin/Greek metrological forms (`uncia`, `litra`, `xestes`, "
        "`drachme`, `gramma`, `scripula`, `ceration`, `count`). Distributive ἀνά is rendered "
        "as a trailing **each**. `q.s.` = *quantum sufficit*, the standard pharmacist's "
        "rendering of τὸ ἀρκοῦν / τὸ ἱκανόν. Ingredients flagged `(uncertain)` reflect a "
        "low-confidence reading in the upstream entity-review pass."
    )
    out.append("")
    out.append(
        "**A note on fractional numerals.** The compressed Byzantine numeral `αζʹ` (and "
        "its kin `βζʹ`, `γζʹ`, …) follows the pharmacological half-marker convention: "
        "a unit-digit followed by `ζʹ` reads as *digit + ½* — so `γοαζʹ = 1½ uncia`, "
        "`γοβζʹ = 2½ uncia`, and so on. This is distinct from the additive numeral "
        "reading (e.g. `ιζʹ = 17`) because additive 8 would canonically be written as "
        "the single letter `η`; the redundant `αζ` form *is* the half-marker signal. "
        "The reading is confirmed in-text at 16-139, where the scribe writes "
        "`ξεαζʹ. ἤτοι ξέστ. α καὶ ἥμισ.` (\"1½ xestes, i.e. one xestes and a half\"). "
        "This convention is applied by `scripts/normalize_quantities.py` "
        "(`parse_half_suffix_numeral`)."
    )
    out.append("")
    out.append("## Book 1 — Oils (ed. Olivieri)")
    out.append("")
    for r in book1:
        out.append(render_recipe(r))
    out.append("## Book 16 — Perfumes and incenses (ed. Zervos)")
    out.append("")
    for r in book16:
        out.append(render_recipe(r))

    out.append("## Appendix: Styrax-variant index")
    out.append("")
    out.append("| Recipe | Styrax form(s) called for |")
    out.append("| --- | --- |")
    for r in recipes:
        forms = []
        for ing in r.get("ingredients", []):
            lab = ing.get("normalized_label") or ""
            lab_nfc = unicodedata.normalize("NFC", lab)
            if any(n in lab_nfc for n in STYRAX_NEEDLES):
                if lab not in forms:
                    forms.append(lab)
        out.append(f"| `{r['recipe_id']}` | {', '.join(forms)} |")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT} — {len(recipes)} recipes ({len(book1)} Book 1, {len(book16)} Book 16)")


if __name__ == "__main__":
    main()
