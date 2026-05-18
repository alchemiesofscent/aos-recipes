# Dioscorides Book 2 Fats Experiment

## Goal

Publish a static viewer for the core fat preparations in Dioscorides Book 2:
chapters 72, 74, and 76, split into distinct preparation and technique cards.

## Source

- TEI witness: `tei/raw/tlg0656.tlg001.1st1K-grc1.xml`
- Edition: Wellmann
- Viewer data: `data/dioscorides_book2_fats.json`
- Browser bootstrap: `data/dioscorides_book2_fats.js`

## Extraction Policy

- One viewer card is emitted per logical preparation, technique, or property catalogue unit.
- Greek text is taken from the raw witness and omits notes and deleted text.
- Bare Arabic numerals from the raw witness are removed from the Greek text flow, except parenthetical cross-references such as `(I 68)`.
- Section markers are stored separately as `section_markers` and displayed as badges near sentence boundaries.
- Wellmann page and line boundaries are preserved in `wellmann.lines`.
- Recipe IDs are stable:
  - `dioscorides-2-72-boutyron`
  - `dioscorides-2-72-boutyron-lignys`
  - `dioscorides-2-74-oisypos`
  - `dioscorides-2-74-oisypos-boiled`
  - `dioscorides-2-74-oisypos-burned-lignys`
  - `dioscorides-2-76-*`
- Derived entity groups are attached from `derived/recipe_entities/*.json`.

## Commands

```bash
python3 experiments/dioscorides-book2-fats/extract.py --skip-entities
python3 scripts/recipes/build_recipe_entities.py --generate-structured-authority --recipe-ids <split-book2-fat-ids> --probe-only
python3 scripts/recipes/build_recipe_entities.py --merge-from-temp --recipe-ids <split-book2-fat-ids>
python3 scripts/recipes/build_recipe_entities.py
python3 experiments/dioscorides-book2-fats/extract.py
```

## QC

```bash
python3 -m py_compile experiments/dioscorides-book2-fats/extract.py scripts/recipes/common.py
node --check experiments/dioscorides-book2-fats/app.js
node --check experiments/app.js
```
