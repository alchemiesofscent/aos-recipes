# Regeneration

Regenerate from the source repository:

```bash
cd /home/seanm/github/aetius
python3 scripts/recipes/build_recipe_entities.py
python3 scripts/recipes/export_standalone_repo.py --dest /home/seanm/github/aos-recipes --force
cd /home/seanm/github/aos-recipes
python3 scripts/validate.py
```

The exporter reads the dataset registrations in `scripts/recipes/common.py`, so slice membership should be changed there first.

The copied files under `provenance/source/scripts/recipes/` and each canonical `provenance/source/experiments/<slice>/` directory are historical snapshots of the source-side extraction apparatus. Regenerate them from `/home/seanm/github/aetius` when refreshing the exported provenance bundle.
