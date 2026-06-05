# QC

The canonical export is expected to contain 193 recipes:

- Dioscorides Book 1 perfumes and resins: 52
- Dioscorides Book 2 fats: 18
- Aëtius Book 1 oils: 43
- Aëtius Book 16 myrepsika: 45
- Paul 7.20 perfumes: 35

Quantity-gold artifacts mirrored from `aetius` may still report a 174-record
artifact-run denominator. The current `aetius` source recipe-entity index and
this standalone export are both 193 recipes, including Dioscorides Book 2 fats
and the split Aëtius Book 16 record.
Refresh quantity-gold artifacts from the current source tree before treating the
artifact denominator as current corpus coverage.

Run `python3 scripts/validate.py` after regeneration. The validator checks schema shape, unique IDs, per-slice counts, `derived_recipe_id` links, entity-file coverage, and forbidden exported paths/content.
