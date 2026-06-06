# Release v1.0 — Canonical Snapshot for Scholarly Ingestion

Status: ready to tag. Last reviewed: 2026-06-06.

## Role of v1

v1 is the **canonical snapshot of the 193 recipes** that gets ingested, one at a time, into the Claude cowork scholarly revision workflow. The scholarly work — revised text, translation, commentary, TEI linking — happens *outside* this repository and produces its own per-recipe artifacts.

v1 is **not** the revised scholarly edition. It is:

- The fixed input the cowork skill reads.
- The reference point downstream artifacts cite as "v1 of recipe X".
- The historical record of the corpus as extracted from `aetius` at source commit `4fde3ddef7203eccf1f13f9e9a9c60ca002b1651`.

## Freeze policy

- Scope is locked at **193 recipes** from five slices (Dioscorides bk1 perfumes & resins (52), Dioscorides bk2 fats (18), Aëtius bk1 oils (43), Aëtius bk16 myrepsika (45), Paul 7.20 perfumes (35)). No new sources before v2.
- Recipe IDs, URNs, schema (`schema_version 1.2`), and the quantity-gold-v2 overlay shape are fixed. Future schema changes are recommendations only; see [`schema_recommendations.md`](schema_recommendations.md).
- Bug-fix re-runs of deterministic local scripts (lexicon, cooccurrence, normalization) are allowed only if they reproduce byte-identical output for the existing corpus.
- The one accepted quantity-gold record (`dioscorides-1-25-kyphi`) is part of v1 as-is. The remaining 192 recipes have no quantity-gold record in v1; they will be revised individually in the cowork workflow.

## Definition of Done

### Required for v1.0 tag

- [x] `python3 scripts/validate.py` exits 0.
- [x] `python3 scripts/extract_ingredient_lexicon.py --check` exits 0.
- [x] `python3 scripts/cooccurrence.py --check` exits 0.
- [x] `python3 scripts/quantity_gold.py --validate` exits 0.
- [x] Documentation consolidated: no redundant files; [`README.md`](README.md) indexes every other doc; stale governance docs archived under [`archive/`](archive/).
- [x] All markdown internal links resolve (mechanical link-checker passes; see Verification below).
- [x] Per-recipe ingestion contract documented in [`ingestion.md`](ingestion.md).
- [x] `release_v1.md` (this file) is linked from the top-level `README.md`.
- [x] `CITATION.cff` present (license: CC-BY-4.0 placeholder — confirm or change before tagging; release date will be updated to actual tag date if it differs from 2026-06-06).
- [x] `CHANGELOG.md` present with a v1.0 entry summarising the snapshot.

### Release mechanics

- [ ] All boxes above ticked.
- [ ] PR merged to `main`.
- [ ] v1.0 git tag created on the merge commit and pushed.
- [ ] GitHub release notes drafted from `CHANGELOG.md`.

### Out of scope for v1

The following are **not** v1 requirements; they belong to the scholarly cowork workflow or to a future v2:

- Revised translations, commentary, or TEI-linked editions of any recipe.
- Quantity-gold review of recipes beyond `dioscorides-1-25-kyphi`.
- Resolution of the 19 schema gaps (F1–F19) documented in [`schema_recommendations.md`](schema_recommendations.md).
- The 69 lexicon entries marked `needs_review` (the lexicon is local enrichment; the cowork workflow does not consume it).

## Verification

Mechanical link checker — every relative markdown link inside `README.md` and `docs/**/*.md` must point to a file that exists:

```bash
python3 - <<'PY'
import re, pathlib
root = pathlib.Path('.')
md_link = re.compile(r'\]\((?!https?://|#)([^)]+)\)')
broken = 0
for md in list(root.glob('*.md')) + list(root.rglob('docs/**/*.md')):
    base = md.parent
    for m in md_link.finditer(md.read_text(encoding='utf-8')):
        target = (base / m.group(1).split('#', 1)[0]).resolve()
        if not target.exists():
            print(f'BROKEN: {md} -> {m.group(1)}')
            broken += 1
print(f'broken: {broken}')
PY
```

## Sign-off log

| Date | Item | Reviewer | Notes |
|---|---|---|---|
| 2026-06-06 | Freeze policy adopted; checklist published | (owner) | v1.0-preparation PR opened |
| 2026-06-06 | Repo-local DoD boxes ticked | (owner) | All four validators green; link checker clean |
| 2026-06-06 | v1.0 reframed for scholarly ingestion | (owner) | Upstream gold-review campaign superseded by Claude cowork per-recipe workflow; schema_policy and normalization_campaign archived; schema_recommendations.md captures forward-looking design |
| 2026-06-06 | CITATION.cff and CHANGELOG.md present; link checker clean | (owner) | All "Required for v1.0 tag" boxes ticked; ready for review and merge |
