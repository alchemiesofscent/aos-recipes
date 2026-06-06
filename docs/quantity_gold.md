# Quantity Gold Mirror

The quantity-gold layer is a separate authority overlay for measures, durations, and process qualifiers, distinct from the canonical `data/recipes/*.json`. v1 mirrors the source authority at `/home/seanm/github/aetius`.

**The v1 snapshot includes one accepted gold record (`dioscorides-1-25-kyphi`).** Further per-recipe revision happens in the Claude cowork scholarly workflow, not in this repo; see [`schema_recommendations.md`](schema_recommendations.md) R4.

## Rules

- Do not edit `data/review/quantity_gold/` independently in this checkout. The mirror is validate-only.
- All authoritative changes happen in `/home/seanm/github/aetius` and are exported here.

## Mirrored files

- `data/review/quantity_gold/recipes/<recipe_id>.json` — source-approved quantity-gold records (currently one: `dioscorides-1-25-kyphi.json`).
- `data/review/quantity_gold/schema.json` — `quantity-gold-v2` schema.
- `data/review/quantity_gold/vocabularies/{metrology,temporal,process_qualifiers}.json` — controlled vocabularies.
- `data/review/quantity_gold/quantity_ledger.csv` — flat review ledger.
- `data/review/quantity_gold/summary.md` — source summary.
- `data/review/quantity_gold/projection/recipes.json` — compatibility projection into the existing `quantities[]` shape.
- `data/review/quantity_gold/projection/rich_recipes.json` — rich projection that preserves process qualifiers, temporal records, and rejections.
- `data/review/quantity_gold/runs/<run_id>/` — mirror run snapshots.
- `data/review/quantity_gold/archive/<run_id>/` — archived overwritten mirror predecessors.

## Current accepted record

`dioscorides-1-25-kyphi`:

- `ἡμίξεστον` projects to `1/2 xestes`.
- `ἡμέραν μίαν` is preserved as a one-day process duration qualifier.
- Four non-measure spans are represented as first-class rejection records.
- Canonical `data/recipes/dioscorides-1-25-kyphi.json` is unchanged by projection.

## Coverage

v1 validates 193 standalone recipe records (52 + 18 + 43 + 45 + 35). The current mirrored quantity-gold index reports `corpus_recipe_count: 193`. Older archived artifacts may still report `174`; that value is copied from an earlier artifact run and is not the current standalone export denominator.

## Validate

```bash
python3 scripts/quantity_gold.py --validate
python3 scripts/validate.py
```

`scripts/quantity_gold.py` in this mirror refuses generation and projection commands by design; use the source repo for those operations if a future v2 revisits the mirror layer.
