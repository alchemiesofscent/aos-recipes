# AOS Recipes Repo Policy

| | |
|---|---|
| **Version** | 0.1.0 |
| **Date** | 2026-06-05 |
| **Status** | Active operational policy |
| **Applies to** | `/home/seanm/github/aos-recipes` and its export relationship with `/home/seanm/github/aetius` |

## Role

`aos-recipes` is a published standalone dataset repo with local enrichment. It is
not a pure mirror of `aetius`, and it is not the source authority for recipe
extraction.

`aetius` owns source authority: structured recipe authority, recipe-entity
building, measure-audit application, quantity-gold generation, and source
metrology.

`aos-recipes` owns public consumption: exported JSON, validation, local
post-export enrichment, public documentation, topical reports, and the static
browser.

## Ownership

| Path or layer | Owner | Edit rule |
|---|---|---|
| `data/recipes.json`, `data/recipes/*.json`, `data/context_units.json`, `data/entities/`, `data/sources.json`, `manifest.json` | Generated from `aetius` | Update by staged export and allowlisted sync only. |
| `provenance/source/**` | Generated from `aetius` | Do not hand-edit; it is a source snapshot used for audit and validation. |
| `data/review/measure_unit_audit.jsonl` | Source-reviewed in `aetius` | Update upstream, then mirror with the recipe export. |
| `data/review/quantity_gold/**`, `data/metrology/units.json` | Generated from `aetius` quantity-gold workflow | Do not edit in this checkout; export from `aetius`. |
| `/home/seanm/github/aetius/data/review/normalization_campaigns/**` | Source-side campaign artifacts | Keep source packets, LLM candidates, and accepted decision ledgers upstream; publish summaries here in `docs/`. |
| `data/ingredient_lexicon.tsv`, `data/ingredient_lexicon.json` | Generated locally in `aos-recipes` | Regenerate from `data/recipes.json`. |
| `provenance/normalization/**` | Generated locally in `aos-recipes` | Regenerate with local normalization/check scripts. |
| `scripts/validate.py`, `scripts/extract_ingredient_lexicon.py`, `scripts/quantity_gold.py` | Maintained in `aos-recipes` | Keep mirror-facing validation and enrichment behavior here. |
| `site/**` | Maintained in `aos-recipes` | Public browser surface; do not overwrite from source export. |
| `docs/**` | Maintained in `aos-recipes` | Public export documentation and reports; do not overwrite from source export. |

## Regeneration Boundary

Never run the `aetius` standalone exporter directly with `--force` against the
live `aos-recipes` checkout. The exporter clears the destination and rewrites a
smaller generated repo surface, which can delete mirror-owned docs, scripts, and
site files.

Regenerate by exporting to a temporary directory first, then sync only the
source-owned generated layers listed in this policy. See
[`regeneration.md`](regeneration.md) for the command sequence.

## Transitional Normalization

`scripts/normalize_quantities.py` is a transitional post-export compatibility
step. New quantity authority should be reviewed in `aetius` or the
quantity-gold workflow first. Deterministic normalization rules should be
derived from accepted review decisions, not used as a substitute for contextual
review.

The schema-policy normalization campaign is governed by
[`normalization_campaign.md`](normalization_campaign.md). Its LLM candidates and
decision ledgers live upstream in `aetius`; this repo validates and documents the
mirrored results.

## Versioning

Changes to this policy use SemVer:

- Patch: clarify wording or commands without changing ownership.
- Minor: add or move ownership of a path/layer.
- Major: change the source/mirror authority boundary.
