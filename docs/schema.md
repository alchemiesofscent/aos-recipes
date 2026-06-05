# Schema

The corpus contract is intentionally small.

- `data/recipes.json` is an object with `metadata` and `recipes`.
- Each recipe has the original derived recipe-entity record fields, plus `canonical_file`, `source_entry`, and `entity_groups`.
- `data/recipes/*.json` contains the same complete record as the matching item in `data/recipes.json`.
- `data/context_units.json` contains non-recipe source units such as proemia.
- `data/entities/index.json` groups entity occurrences by semantic group and by recipe.
- `data/sources.json` records dataset-level source, work, and provenance metadata.
- `data/metrology/units.json` is a compatibility copy of the source controlled
  unit vocabulary used by the quantity-gold overlay.
- `data/review/quantity_gold/` stores mirrored quantity-gold authority records,
  ledgers, summaries, vocabularies, run snapshots, archives, and projections
  exported from `/home/seancoughlin/Projects/aetius`.
- `data/review/quantity_gold/projection/recipes.json` is the compatibility
  projection into the existing `quantities[]` shape.
- `data/review/quantity_gold/projection/rich_recipes.json` preserves richer
  process qualifiers, temporal records, and rejection records.

Recipe IDs and URNs are preserved from the source repository. No opaque-ID migration is performed in this export.
