# Regeneration

Regenerate from the source repository:

```bash
cd /home/seancoughlin/Projects/aetius
python3 scripts/recipes/build_recipe_entities.py
python3 scripts/recipes/export_standalone_repo.py --dest /home/seancoughlin/Projects/aos-recipes --force
cd /home/seancoughlin/Projects/aos-recipes
python3 scripts/validate.py
```

The exporter reads the dataset registrations in `scripts/recipes/common.py`, so slice membership should be changed there first.

Quantity-gold overlays are maintained in `/home/seancoughlin/Projects/aetius`
and mirrored here as derived artifacts. Do not edit
`data/review/quantity_gold/` independently in this checkout.

```bash
cd /home/seancoughlin/Projects/aetius
python3 scripts/quantity_gold.py --write-artifacts --validate
python3 scripts/quantity_gold.py --export-derived /home/seancoughlin/Projects/aos-recipes
cd /home/seancoughlin/Projects/aos-recipes
python3 scripts/quantity_gold.py --validate
python3 scripts/validate.py
```

The source metrology TSV is copied from
`/home/seancoughlin/Projects/aetius/docs/weights-and-measures.tsv` to
`provenance/source/docs/weights-and-measures.tsv`. Quantity-gold controlled
vocabularies are mirrored under `data/review/quantity_gold/vocabularies/`, with
`data/metrology/units.json` retained as a compatibility path.
