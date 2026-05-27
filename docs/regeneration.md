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
