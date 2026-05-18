# Quantity normalization pass — 2026-05-18

Run by `scripts/normalize_quantities.py`. Deterministic post-processing; no LLM calls.

## Rules applied

1. **γο → uncia.** Any quantity whose `raw_unit` is `γο` (or `γο`+Greek-numeral suffix, or whose `source_span` matches that shape when `raw_unit` is null) gets `normalized_unit: "uncia"`. The existing `normalized_number` is preserved. The note `"The abbreviated unit γο is unresolved."` is removed.
2. **Descriptor tagging.** Non-numeric quantifiers (exact match on `source_span` or `raw_unit`) get `normalized_unit: "descriptor"`. Phrases covered: `πλῆθος`, `πολλοὺς`, `σταθμόν`, `σταθμὸν`, `τὸ αὐτό`, `τὸ ἀρκοῦν`, `τὸ ἴσον πλῆθος`, `τὸ ἴσον`, `τὸν ἴσον σταθμὸν`, `τῷ σταθμῷ`, `ἴσον τῷ σταθμῷ`, `ὀλίγου`.
3. **Durations onto processes.** Quantities with `raw_unit` in `ἡμέρας` (→ `day`), `ὥρας` (→ `hour`), `ἡμέρας καὶ νύκτας` (→ `day_and_night`) are removed from `processes[i].quantities` and appended to a new `processes[i].durations` array (with the mapped `normalized_unit`).

## Counts

- Rule 1 (γο → uncia): **0** entries.
- Rule 2 (descriptor): **0** entries.
- Rule 3 (durations moved): **0** entries.
- Canonical files rewritten: **0**.
- Provenance mirrors rewritten: **0**.

## Residual unresolved quantities

| count | raw_unit | source_span |
|------:|----------|-------------|
| 1 | `<null>` | `β` |
| 1 | `<null>` | `γ.` |
| 1 | `<null>` | `δίς` |
| 1 | `<null>` | `διπλασίονι` |
| 1 | `<null>` | `λιστ.` |
| 1 | `<null>` | `ν.` |
| 1 | `<null>` | `ξεα.` |
| 1 | `<null>` | `πλεῖον` |
| 1 | `<null>` | `τοσοῦτον` |
| 1 | `<null>` | `τοσοῦτον, ὅσον ἦν ὁ ἔμπροσθεν δοθείς` |
| 1 | `<null>` | `τρὶς` |
| 1 | `<null>` | `τὸ διπλοῦν` |
| 1 | `<null>` | `τὸ τελευταῖον τρίτον` |
| 1 | `<null>` | `τὸ τέταρτον` |
| 1 | `<null>` | `τὸ ἄλλο τρίτον` |
| 1 | `<null>` | `τὸ ἱκανόν` |
| 1 | `<null>` | `τὸ ἱκανὸν` |
| 1 | `<null>` | `τῷ τρίτῳ τοῦ ἐλαίου` |
| 1 | `<null>` | `ἴσον δὲ τῷ χυλῷ` |
| 1 | `<null>` | `ἴσῳ` |
| 1 | `<null>` | `ἶσον ἴσῳ` |
| 1 | `<null>` | `ὀλίγα` |
| 1 | `<null>` | `ὅσον ἂν δόξῃ` |
| 1 | `δακτύλους` | `δακτύλους ὀκτώ` |
| 1 | `κέγχρους` | `κέγχρους γ.` |
| 1 | `κόκκους` | `κόκκους μ` |
| 1 | `κόκκους` | `κόκκους μ.` |
| 1 | `μέρος` | `μέρος ἓν ἥμισυ` |
| 1 | `μέρος` | `μέρος ἕν` |
| 1 | `μέρος` | `τὸ τρίτον μέρος` |
| 1 | `παράὰ τὸ κινάμωμον` | `τετραπλασίονος παράὰ τὸ κινάμωμον` |
| 1 | `ἐμβολὰς` | `τρεῖς ἐμβολὰς` |
| 1 | `ἡμέρας` | `ἐπὶ ἡμέρας δέκα` |
| 1 | `ἡμέρας` | `ἡμέρας μ.` |
| 1 | `𐅵` | `𐅵 κ` |
