# Ingestion contract

v1 of `aos-recipes` is the canonical input for the Claude cowork scholarly revision workflow. This file is the contract that workflow reads against.

## The ingestion unit

The ingestion unit is **one recipe at a time**: a single file under `data/recipes/<recipe_id>.json`. Each file is a complete self-contained record. There are 193 of them.

```bash
ls data/recipes/ | wc -l   # 193
```

## What every recipe file carries

| Field | Purpose |
|---|---|
| `recipe_id` | Stable across all v1 commits and any future schema revisions (e.g. `aetius-16-126-1`). |
| `recipe_urn` | `urn:aos:recipe:…` form of `recipe_id`; cite this in downstream artifacts. |
| `record_urn` | URN of the underlying recipe-entity record. |
| `dataset_key`, `work_slug` | Source-slice identifiers (one of the five slices). |
| `author`, `work`, `book`, `chapter`, `section`, `chapter_name`, `lemma` | Bibliographic location. |
| `text`, `original_text` | Normalized and as-published Greek text. |
| `text_source`, `source_kind`, `source_entry` | Provenance of the Greek text. |
| `emendations`, `emendation_count` | Recorded editorial corrections, where present. |
| `ingredients`, `processes`, `materials`, `tools`, `people`, `places`, `uses`, `preparation_names`, `other_preparations_mentioned`, `works_mentioned` | Structured entities extracted upstream. |
| `entity_groups` | Same entities grouped by semantic kind, for indexed access. |
| `canonical_file` | Repo-relative path back to this file (self-pointer for round-trip checks). |

`data/recipes.json` is the aggregated array of the same 193 records, with a top-level `metadata` block. Use the per-recipe files for ingestion and the aggregate for bulk indexing.

## Mirror under provenance

`provenance/source/derived/recipe_entities/<recipe_id>.json` mirrors each record byte-for-byte for audit. Ingest from `data/recipes/`; cite the provenance mirror only when investigating discrepancies.

## What v1 does NOT carry

The cowork workflow is responsible for producing all of the following; they are not part of v1:

- Revised translations into modern languages.
- Scholarly commentary beyond what's already in `emendations` / `notes`.
- TEI linking between recipe records and source manuscripts.
- Variant apparatus beyond what's encoded in the original `source_kind` and `emendations`.
- Resolution of the 19 schema gaps catalogued in [`schema_recommendations.md`](schema_recommendations.md) (frequency vocabulary, action authority, staging DAG, etc.).
- Concept-level identity beyond `lookup_key` in `data/ingredient_lexicon.json` (the lexicon is local enrichment, not part of the per-recipe ingestion unit).

Downstream artifacts produced by the cowork workflow should key on `recipe_id` and cite the v1 input as e.g. `aos-recipes@v1.0:data/recipes/aetius-16-126-1.json`.

## Stable identifiers

`recipe_id` and `recipe_urn` are stable. `ingredient_id` and `ingredient_urn` within a recipe are stable within v1. Schema may evolve in v2; identifiers will be preserved or accompanied by an explicit migration map.

## Versioning

Pin the v1 commit hash or the `v1.0` git tag when referencing "the v1 input of recipe X" in any downstream artifact. The release date, schema baselines, and source commit are recorded in `CITATION.cff` and `CHANGELOG.md`.
