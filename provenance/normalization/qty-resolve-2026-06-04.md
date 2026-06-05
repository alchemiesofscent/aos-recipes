# Quantity normalization pass — 2026-06-04

Run by `scripts/normalize_quantities.py`. Deterministic post-processing; no LLM calls. Idempotent.

## Rules

1. **γο → uncia.** `raw_unit` or `source_span` matching `γο` + Greek numeral suffix.
1b. **ξε → xestes.** Same shape, e.g. *ξεα.* = xestes·1.
1c. **λι → litra.** Per user rule, *λιστ.* = λι + στ = litra·6. Where existing entries had read *ιστ* as the numeral (=16), they are corrected to *στ* (=6) with a note recording the prior value.
2. **Descriptors → `normalized_unit: "descriptor"` + `descriptor_family`.** Families: `same_as`, `more_than`, `less_than` (reserved); `as_much_as`, `a_little`, `many`; `fraction:half`, `fraction:third`, `fraction:fourth`, `part`; `multiple:two`, `multiple:three`; `relative_to`; `quantity_unspecified`.
3. **Durations** (*ἡμέρας / ὥρας / ἡμέρας καὶ νύκτας*) moved out of `processes[i].quantities` into `processes[i].durations` with `day / hour / day_and_night`.
4. **Discrete units** → Greek-transliteration names: *κέγχρους* → `kenchros`, *κόκκους* → `kokkos`, *δακτύλους* → `daktylos`.
5. **By-weight indicators** (*σταθμόν / σταθμὸν / τῷ σταθμῷ*) moved from `quantities[]` into `qualifiers[]` with `qualifier_type: "measurement_mode"`, `normalized_value: "by_weight"`. The *ἴσον τῷ σταθμῷ* variants stay in `quantities[]` as `descriptor_family: "same_as"`.
6. **ἐμβολάς (infusion)** moved from `quantities[]` into `qualifiers[]` with `qualifier_type: "application_form"`, `normalized_value: "infusion"`, `count: <n>`. Per user: infusion is not a unit.

## Counts

- Rule 1 γο → uncia: filled **87**, corrected **28** entries.
- Rule 1b ξε → xestes: filled **1**, corrected **1** entries.
- Rule 1c λι → litra: filled **69**, corrected **11** entries.
- Rule 8 manual count overrides: **3** entries; explanatory note added: **1** entries.
- Cleanup (stale whitespace-only notes removed): **0** entries.
- Rule 2 descriptor tagged: **51** entries (family newly set: **51**).
- Rule 3 durations moved: **8** entries.
- Rule 4 discrete units resolved: **4** entries.
- Rule 5 by-weight moved to qualifiers: **0** entries.
- Rule 6 infusion moved to qualifiers: **1** entries.
- Rule 7 relative-to tagged: **1** entries.
- Canonical files rewritten: **79**.
- Provenance mirrors rewritten: **75**.

## Descriptor family distribution (post-pass)

| family | count |
|--------|------:|
| `as_much_as` | 19 |
| `same_as` | 14 |
| `fraction:third` | 4 |
| `a_little` | 3 |
| `multiple:two` | 3 |
| `many` | 2 |
| `fraction:fourth` | 1 |
| `fraction:half` | 1 |
| `more_than` | 1 |
| `multiple:three` | 1 |
| `part` | 1 |
| `quantity_unspecified` | 1 |
| `relative_to` | 1 |

## Residual unresolved quantities

| count | raw_unit | source_span | notes |
|------:|----------|-------------|-------|
| 1 | `𐅵` | `𐅵 κ` | fractional half symbol 𐅵 (U+10175) — needs human review |
