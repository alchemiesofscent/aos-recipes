# Quantity Gold Summary

- Schema version: `quantity-gold-v2`
- Artifact version: `2026-06-05-codex-v1`
- Run ID: `20260605T071436Z-codex`
- Source repo: `/home/seancoughlin/Projects/aetius`
- Source commit: `1632f26bab10aca3eaa698c086b54d0167440f20`
- Gold records: 1 / 174
- Accepted projection records: 11
- Process qualifier records: 1
- Rejection records: 4

## Current State

- `dioscorides-1-25-kyphi` is the currently reviewed source gold record.
- The reviewed `ἡμίξεστον` record is a fraction: numerator `1`, denominator `2`, display `1/2`, normalized unit `xestes`.
- `ἡμέραν μίαν` is modeled as a one-day `process_qualifier` with qualifier kind `duration`.
- Four non-measure spans are retained as first-class `rejection` records.
- Canonical recipe JSON is not rewritten by this workflow.

## Projection

- `projection/recipes.json` is the compatibility projection.
- `projection/rich_recipes.json` preserves process qualifiers and rejection records.
- Canonical updates require a separate reviewed canonical-update command; none is implemented here.
