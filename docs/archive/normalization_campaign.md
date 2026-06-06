# Recipe Normalization Campaign

| | |
|---|---|
| **Version** | 0.1.0 |
| **Date** | 2026-06-05 |
| **Status** | Active campaign plan |
| **Policy basis** | [`schema_policy.md`](schema_policy.md) |
| **Repo boundary** | [`repo_policy.md`](../repo_policy.md) |

## Goal

Normalize all 193 recipes for cross-recipe consistency and interoperability
without replacing Greek contextual judgment with deterministic parsing. The
campaign produces reviewable LLM candidate records, explicit decision ledgers,
and a complete quantity-gold run before any accepted changes are projected or
exported.

## Authority

`aetius` owns the source run: recipe packets, LLM candidate outputs, accepted
decision ledgers, quantity-gold records, and exports. This repo publishes the
policy, validates mirrored artifacts, regenerates local enrichments, and keeps
the static browser aligned with reviewed outputs.

The campaign ID is `schema-policy-v0.1.0-20260605`. The source run directory is
`/home/seanm/github/aetius/data/review/normalization_campaigns/runs/<run_id>/`.

## Review Contract

- LLM candidates start as `generated_unreviewed`.
- Decision rows must include Greek evidence, source span, target span, decision
  type, confidence, proposed patch, and rationale.
- Accepted canonical or projected changes must have an accepted source-side
  ledger row.
- Deterministic scripts may enumerate, validate, project, and export accepted
  decisions. They may not invent interpretive quantity, timing, variant, or
  concept decisions.
- True variants are separated from equivalent notation, aliases, compound
  measures, contextual repeated amounts, and extraction errors.

## Gold Run Gate

The campaign is not complete until the source quantity-gold validator passes
with complete coverage:

```bash
cd /home/seanm/github/aetius
python3 scripts/quantity_gold.py --validate --require-complete
```

After source export, this mirror must pass:

```bash
cd /home/seanm/github/aos-recipes
python3 scripts/validate.py
python3 scripts/extract_ingredient_lexicon.py --check
python3 scripts/quantity_gold.py --validate
```

## Reporting

The final campaign report should record baseline commits, run ID, policy
version, model and prompt version, corpus coverage, accepted/rejected/ambiguous
decision counts, unresolved issues, source export commit, mirror commit, and
manual browser spot checks.
