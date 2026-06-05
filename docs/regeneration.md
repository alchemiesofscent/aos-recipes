# Regeneration

Regenerate from the source repository:

```bash
cd /home/seanm/github/aetius
python3 scripts/recipes/build_recipe_entities.py
python3 scripts/recipes/export_standalone_repo.py --dest /home/seanm/github/aos-recipes --force
cd /home/seanm/github/aos-recipes
python3 scripts/extract_ingredient_lexicon.py
python3 scripts/validate.py
python3 scripts/extract_ingredient_lexicon.py --check
```

The exporter reads the dataset registrations in `scripts/recipes/common.py`, so slice membership should be changed there first.

Use `python3 scripts/extract_ingredient_lexicon.py --check --strict` before downstream LSJ joining. Strict mode fails while any emitted row remains marked `needs_review`.

Quantity-gold overlays are maintained in `/home/seanm/github/aetius`
and mirrored here as derived artifacts. Do not edit
`data/review/quantity_gold/` independently in this checkout.

```bash
cd /home/seanm/github/aetius
python3 scripts/quantity_gold.py --write-artifacts --validate
python3 scripts/quantity_gold.py --export-derived /home/seanm/github/aos-recipes
cd /home/seanm/github/aos-recipes
python3 scripts/quantity_gold.py --validate
python3 scripts/validate.py
```

The source metrology TSV is copied from
`/home/seanm/github/aetius/docs/weights-and-measures.tsv` to
`provenance/source/docs/weights-and-measures.tsv`. Quantity-gold controlled
vocabularies are mirrored under `data/review/quantity_gold/vocabularies/`, with
`data/metrology/units.json` retained as a compatibility path.
