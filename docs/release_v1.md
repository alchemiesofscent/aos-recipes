# Release v1.0 — Definition of Done & Checklist

Status: scope frozen; awaiting upstream gold-standard revision. Last reviewed: 2026-06-06.

## Freeze policy

**v1.0 cannot ship until every one of the 193 recipes has been revised according to the gold-standard schema policy** ([`schema_policy.md`](schema_policy.md) workstreams W1–W5) AND every quantity has been reviewed and accepted into the quantity-gold layer (193/193, currently 1/193). This is a hard release gate, not an aspiration.

What "frozen" means now, as of the v1.0-preparation PR:

- Scope is locked at 193 recipes from five slices (Dioscorides bk1 perfumes & resins, Dioscorides bk2 fats, Aëtius bk1 oils, Aëtius bk16 myrepsika, Paul 7.20 perfumes). No new sources before v2.0.
- Repo structure, scripts, and the local enrichment pipeline are locked. Bug-fix re-runs of deterministic scripts (lexicon, cooccurrence, normalization) are allowed.
- Documentation is consolidated and stable; the audience-grouped index is [`README.md`](README.md).
- The upstream gold-standard schema-policy revision campaign is the only path to v1.0 release.

## Definition of Done

### Upstream-blocking — the critical path

Work owned by `/home/seanm/github/aetius`. Nothing here can be ticked until the upstream campaign progresses.

- [ ] **Schema-policy revision (W1–W5 of [`schema_policy.md`](schema_policy.md) §5) applied to all 193 recipes.** Per-recipe attestation logged in the upstream campaign run directory (`/home/seanm/github/aetius/data/review/normalization_campaigns/runs/schema-policy-v0.1.0-20260605/`).
- [ ] **Quantity-gold review complete: 193/193 recipes reviewed and accepted upstream** (currently 1/193 — only `dioscorides-1-25-kyphi`).
- [ ] `python3 scripts/quantity_gold.py --validate --require-complete` passes **upstream** in `aetius`.
- [ ] Residual unresolved quantity `𐅵 κ` ([`../provenance/normalization/qty-resolve-2026-06-05.md`](../provenance/normalization/qty-resolve-2026-06-05.md), lines 50–55) resolved.
- [ ] Re-export from `aetius` to `aos-recipes` using the documented staged-rsync workflow ([`regeneration.md`](regeneration.md)); 193 recipes confirmed; entity index regenerated; quantity-gold artifacts mirrored.
- [ ] After re-export, `python3 scripts/quantity_gold.py --validate --require-complete` passes **here** in `aos-recipes`.

### Repo-local — should be green at the end of the v1.0-preparation PR

Achievable inside `aos-recipes`. These are local-validator passes and structural cleanup.

- [x] `python3 scripts/validate.py` exits 0.
- [x] `python3 scripts/extract_ingredient_lexicon.py --check` exits 0.
- [x] `python3 scripts/cooccurrence.py --check` exits 0.
- [x] `python3 scripts/quantity_gold.py --validate` exits 0 (non-strict; full strict mode is upstream-blocking above).
- [x] Documentation consolidated: no redundant files; [`README.md`](README.md) indexes every other doc.
- [x] All markdown internal links resolve (mechanical link-checker passes; see Verification below).
- [x] `release_v1.md` (this file) is linked from the top-level `README.md`.

### Repo-local follow-ups — allowed before or after the gold campaign

These don't block v1.0 in isolation but they sharpen the release.

- [ ] `python3 scripts/extract_ingredient_lexicon.py --check --strict` exits 0 (no `needs_review` rows remain — currently 69/262). Strict pass is required before downstream LSJ joining, which is part of the upstream W1 authority-layer workstream; ticking this proves the lexicon is ready to receive the gold ingredient IDs.
- [ ] `CHANGELOG.md` present with a v1.0-rc entry summarising the freeze.
- [ ] `CITATION.cff` present.

### Release mechanics — final, after all of the above

- [ ] All boxes above ticked or explicitly waived with reviewer sign-off in the log below.
- [ ] v1.0 PR opened, reviewed, merged to `main`.
- [ ] v1.0 git tag created on the merge commit and pushed.
- [ ] GitHub release notes drafted (from `CHANGELOG.md` if present, otherwise from the merged PR descriptions since v1.0 preparation).

## Verification

A mechanical link checker, used during the v1.0-preparation PR to validate the "all markdown internal links resolve" box:

```bash
python3 - <<'PY'
import re, pathlib
root = pathlib.Path('.')
md_link = re.compile(r'\]\((?!https?://|#)([^)]+)\)')
for md in list(root.glob('*.md')) + list((root / 'docs').glob('*.md')):
    base = md.parent
    for m in md_link.finditer(md.read_text(encoding='utf-8')):
        target = (base / m.group(1).split('#', 1)[0]).resolve()
        if not target.exists():
            print(f'BROKEN: {md} -> {m.group(1)}')
PY
```

## Status mirror to upstream

The Upstream-blocking section above is mirrored from [`normalization_campaign.md`](normalization_campaign.md) (campaign id `schema-policy-v0.1.0-20260605`) and [`schema_policy.md`](schema_policy.md) (W1–W5). When the upstream campaign run directory reports completion, copy the run-id and accepted-count here and tick the box.

## Sign-off log

| Date | Item | Reviewer | Notes |
|---|---|---|---|
| 2026-06-06 | Freeze policy adopted; checklist published | (owner) | v1.0-preparation PR opened |
| 2026-06-06 | Repo-local DoD boxes ticked | (owner) | All four validators green; link checker clean |
