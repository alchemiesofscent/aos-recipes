# Regeneration

Ownership, the source/mirror boundary, and the rationale for the staged-export pattern below are documented in [`repo_policy.md`](repo_policy.md). This file is the operational command sequence.

## Recipe Export

```bash
cd /home/seanm/github/aetius
python3 scripts/recipes/build_recipe_entities.py
python3 scripts/recipes/export_standalone_repo.py --dest /tmp/aos-recipes-export --force --no-git-init

cd /home/seanm/github/aos-recipes
mkdir -p data/review data/entities provenance/source
rsync -a --delete /tmp/aos-recipes-export/data/recipes/ data/recipes/
rsync -a --delete /tmp/aos-recipes-export/data/entities/ data/entities/
rsync -a --delete /tmp/aos-recipes-export/provenance/source/ provenance/source/
cp /tmp/aos-recipes-export/data/recipes.json data/recipes.json
cp /tmp/aos-recipes-export/data/context_units.json data/context_units.json
cp /tmp/aos-recipes-export/data/sources.json data/sources.json
cp /tmp/aos-recipes-export/manifest.json manifest.json
cp /tmp/aos-recipes-export/data/review/measure_unit_audit.jsonl data/review/measure_unit_audit.jsonl

python3 scripts/normalize_quantities.py
python3 scripts/extract_ingredient_lexicon.py
python3 scripts/cooccurrence.py
python3 scripts/validate.py
python3 scripts/extract_ingredient_lexicon.py --check
python3 scripts/cooccurrence.py --check
```

The exporter reads the dataset registrations in `scripts/recipes/common.py`, so slice membership should be changed there first.

Use `python3 scripts/extract_ingredient_lexicon.py --check --strict` before downstream LSJ joining. Strict mode fails while any emitted row remains marked `needs_review`.

Do not copy staged `docs/`, `site/`, or `scripts/` into the live checkout. Those
paths are maintained in `aos-recipes`. After a source export, review
`docs/provenance.md` and update its source commit or slice list if needed.

## Quantity Gold

The quantity-gold mirror is maintained in `/home/seanm/github/aetius` and exported here as derived artifacts. Do not edit `data/review/quantity_gold/` independently in this checkout. v1 carries one accepted record (`dioscorides-1-25-kyphi`); per-recipe revision continues in the Claude cowork scholarly workflow rather than as a bulk upstream campaign. See [`quantity_gold.md`](quantity_gold.md) for artifact layout and validation, and [`schema_recommendations.md`](schema_recommendations.md) for the forward-looking schema design.

The source metrology TSV is copied from `/home/seanm/github/aetius/docs/weights-and-measures.tsv` to `provenance/source/docs/weights-and-measures.tsv`. Quantity-gold controlled vocabularies are mirrored under `data/review/quantity_gold/vocabularies/`, with `data/metrology/units.json` retained as a compatibility path.
