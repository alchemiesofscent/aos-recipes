# Regeneration

`aos-recipes` is a standalone dataset repo with local enrichment. Follow
[`repo_policy.md`](repo_policy.md): export from `aetius` to a staging directory,
then sync only source-owned generated layers into this checkout.

Do not run the source exporter directly with `--force` against the live
`aos-recipes` checkout. It clears the destination and can delete mirror-owned
docs, scripts, and site files.

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
python3 scripts/validate.py
python3 scripts/extract_ingredient_lexicon.py --check
```

The exporter reads the dataset registrations in `scripts/recipes/common.py`, so slice membership should be changed there first.

Use `python3 scripts/extract_ingredient_lexicon.py --check --strict` before downstream LSJ joining. Strict mode fails while any emitted row remains marked `needs_review`.

Do not copy staged `docs/`, `site/`, or `scripts/` into the live checkout. Those
paths are maintained in `aos-recipes`. After a source export, review
`docs/provenance.md` and update its source commit or slice list if needed.

## Quantity Gold

Quantity-gold overlays are maintained in `/home/seanm/github/aetius`
and mirrored here as derived artifacts. Do not edit
`data/review/quantity_gold/` independently in this checkout.

For the schema-policy normalization campaign, prepare and run LLM candidate
packets upstream before any accepted gold export:

```bash
cd /home/seanm/github/aetius
python3 scripts/quantity_gold.py --prepare-campaign --campaign-run-id schema-policy-v0.1.0-20260605
python3 scripts/quantity_gold.py --generate --campaign-run-id schema-policy-v0.1.0-20260605
python3 scripts/quantity_gold.py --validate-campaign schema-policy-v0.1.0-20260605 --require-complete
```

Generated candidates are not accepted gold. Promote only reviewed decisions into
stable `data/review/quantity_gold/recipes/*.json`, then rebuild and export:

```bash
cd /home/seanm/github/aetius
python3 scripts/quantity_gold.py --validate --require-complete
python3 scripts/quantity_gold.py --write-artifacts
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
