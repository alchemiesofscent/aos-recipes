# Schema

The corpus contract is intentionally small.

- `data/recipes.json` is an object with `metadata` and `recipes`.
- Each recipe has the original derived recipe-entity record fields, plus `canonical_file`, `source_entry`, and `entity_groups`.
- `data/recipes/*.json` contains the same complete record as the matching item in `data/recipes.json`.
- `data/context_units.json` contains non-recipe source units such as proemia.
- `data/entities/index.json` groups entity occurrences by semantic group and by recipe.
- `data/sources.json` records dataset-level source, work, and provenance metadata.

Recipe IDs and URNs are preserved from the source repository. No opaque-ID migration is performed in this export.
