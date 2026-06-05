# Quantity Gold Mirror

This repo is the derived/export mirror for quantity-gold artifacts. The source
authority is `/home/seancoughlin/Projects/aetius`.

## Rules

- Do not edit `data/review/quantity_gold/` independently in this checkout.
- Generate candidates, validate records, write ledgers, build projections, and
  archive stable artifacts in `/home/seancoughlin/Projects/aetius`.
- Export approved source artifacts into this repo with the source command:

```bash
cd /home/seancoughlin/Projects/aetius
python3 scripts/quantity_gold.py --write-artifacts --validate
python3 scripts/quantity_gold.py --export-derived /home/seancoughlin/Projects/aos-recipes
```

## Mirrored Files

- `data/review/quantity_gold/recipes/<recipe_id>.json`: source-approved
  quantity-gold records.
- `data/review/quantity_gold/quantity_ledger.csv`: flat review ledger.
- `data/review/quantity_gold/summary.md`: source summary.
- `data/review/quantity_gold/projection/recipes.json`: compatibility
  projection into the existing `quantities[]` shape.
- `data/review/quantity_gold/projection/rich_recipes.json`: rich projection that
  preserves process qualifiers, temporal records, and rejections.
- `data/review/quantity_gold/runs/<run_id>/`: mirror run snapshots.
- `data/review/quantity_gold/archive/<run_id>/`: archived overwritten mirror
  predecessors.

## Current Regression Record

The current reviewed record is `dioscorides-1-25-kyphi`.

- `ἡμίξεστον` projects to `1/2 xestes`.
- `ἡμέραν μίαν` is preserved as a one-day process duration qualifier.
- Four non-measure spans are represented as first-class rejection records.
- Canonical `data/recipes/*.json` is unchanged by projection.

## Coverage Count Note

This repo validates 192 standalone recipe records:

- Dioscorides Book 1 perfumes and resins: 52
- Dioscorides Book 2 fats: 18
- Aetius Book 1 oils: 43
- Aetius Book 16 myrepsika: 44
- Paul 7.20 perfumes: 35

The mirrored quantity-gold artifacts may report `corpus_recipe_count: 174`.
That value is copied from the artifact run that built the current reviewed
overlay before the Book 2 fats slice was present in the local source workflow.
It is not the current standalone export denominator.

The current `aetius` source recipe-entity index and this standalone mirror both
now contain 192 recipes, including `dioscorides_book2_fats`. The current LLM/gold
process has still not run across all 192 recipes; the reviewed gold layer
contains one accepted recipe record, `dioscorides-1-25-kyphi`.

Until the quantity-gold artifacts are rebuilt and exported from the current
`aetius` source tree, read `1 / 174` as artifact-run coverage and `192` as the
current source/export corpus size.

## Validate

```bash
python3 scripts/quantity_gold.py --validate
python3 scripts/validate.py
```

`scripts/quantity_gold.py` in this mirror refuses generation and projection
commands. Use the source repo for those operations.
