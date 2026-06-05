# Quantity Gold Mirror

This directory contains exported quantity-gold artifacts. The source authority is
`/home/seancoughlin/Projects/aetius`; this checkout is a derived mirror.
Do not edit these artifacts independently.

Primary generated files:

- `recipes/<recipe_id>.json`: per-recipe quantity-gold authority record.
- `quantity_ledger.csv`: flat ledger of accepted and rejected records.
- `summary.md`: source summary and regression notes.
- `projection/recipes.json`: non-mutating compatibility projection into the current `quantities[]` shape.
- `projection/rich_recipes.json`: rich projection preserving process qualifiers, temporal records, and rejections.
- `runs/<run_id>/`: timestamped mirror snapshots.
- `archive/<run_id>/`: archived predecessors overwritten by export.

Coverage note: the current mirrored quantity-gold artifacts may say
`corpus_recipe_count: 174` because that denominator comes from the artifact run
that built the reviewed overlay before Book 2 fats was present in the local
source workflow. The current `aetius` source recipe-entity index and this
standalone `aos-recipes` export are both 192 recipes, including the 18-record
`dioscorides_book2_fats` slice. Rebuild and export quantity-gold artifacts from
the current source tree to refresh the artifact denominator.

Validate mirrored records with:

```bash
python3 scripts/quantity_gold.py --validate
```

Regenerate or project in the source repo:

```bash
cd /home/seancoughlin/Projects/aetius
python3 scripts/quantity_gold.py --write-artifacts --validate
python3 scripts/quantity_gold.py --export-derived /home/seancoughlin/Projects/aos-recipes
```

Canonical `data/recipes/*.json` is not rewritten by this mirror. Existing
`quantities[]` remains a compatibility target; rich gold records are not forced
into that shape.
