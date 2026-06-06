# Changelog

## [Unreleased]

## [1.0.0] — 2026-06-07

Initial public release. v1.0 is the canonical snapshot of 193 Greek pharmaceutical recipes from Dioscorides, Aëtius, and Paul of Aegina, designed for one-at-a-time ingestion into the Claude cowork scholarly revision workflow. See [`docs/release_v1.md`](docs/release_v1.md) for the freeze policy and [`docs/ingestion.md`](docs/ingestion.md) for the contract downstream workflows consume.

### Included

- 193 normalized recipe records in `data/recipes/` (52 Dioscorides bk1 + 18 Dioscorides bk2 + 43 Aëtius bk1 + 45 Aëtius bk16 + 35 Paul 7.20).
- Aggregated corpus in `data/recipes.json`.
- Entity occurrence index in `data/entities/index.json`.
- Ingredient lexicon: 262 canonical entries, 1,370 occurrences (`data/ingredient_lexicon.{tsv,json}`).
- Apriori frequent ingredient co-occurrence analysis (k=1 through k=10) in `data/analysis/cooccurrence/`.
- Quantity-gold-v2 mirror layer in `data/review/quantity_gold/`, with one accepted record (`dioscorides-1-25-kyphi`).
- Provenance snapshots in `provenance/source/`.
- Static browser at `site/`.
- Schema and regeneration documentation; forward-looking schema recommendations in `docs/schema_recommendations.md`; archived governance docs in `docs/archive/`.

### Known limitations

See `docs/schema_recommendations.md` for the 19 schema gaps (F1–F19) identified during v1 development. These are forward-looking recommendations for the scholarly revision workflow; they are not bugs in v1.

The ingredient lexicon contains 69 entries marked `needs_review` (LSJ-headword verification pending). The lexicon is local enrichment and not part of the per-recipe ingestion unit, so this does not block v1.

### Provenance

- Source repository: `/home/seanm/github/aetius` at commit `4fde3ddef7203eccf1f13f9e9a9c60ca002b1651`.
- Quantity-gold artifact version: `2026-06-05-codex-v1`.
- Recipe-entity schema version: `1.2`.
