# Provenance

Exported from `/home/seanm/github/aetius` at source commit `b4a881a6e7d3766dc90df37d947df2b23d8e8fe1`.

Included canonical experiment slices:

- `experiments/dioscorides-book1-perfumes-resins`
- `experiments/dioscorides-book2-fats`
- `experiments/aetius-book1-ch99-136-oils`
- `experiments/aetius-book16-ch126-153-myrepsika`
- `experiments/paul-book7-ch20-perfumes`

Provenance-only folders:

- `experiments/aetius-book1-ch99-136-oils-pre-emended-backup`
- `experiments/aetius-book1-emended-compare`
- `experiments/aetius-book1-emended-working-compare`

Excluded folders and generated noise:

- `experiments/parallel-viewer`
- `experiments/.codex`
- `**/__pycache__`
- `.pytest_cache`
- `node_modules`

Exact source JSON, QC reports, selected planning docs, structured authority files, and derived recipe-entity JSON are copied under `provenance/source/`.

## Experiment Apparatus Snapshot

The canonical experiment folders also preserve their local extraction and browsing apparatus:

- `extract.py`: slice-specific extractor used to build the experiment JSON.
- `app.js`, `index.html`, and `style.css`: the lightweight local browser used during review.
- `data/aetius_book1_emendations.json`: the Aetius Book 1 emendation overlay used by the current Book 1 oils slice.

The prompt-bearing recipe authority scripts are copied under `provenance/source/scripts/recipes/`:

- `build_recipe_entities.py`
- `common.py`

These files are included as provenance snapshots, not as the primary public API for this repository. The canonical corpus contract remains the normalized files in `data/`, documented in `docs/schema.md`.
