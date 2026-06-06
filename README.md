# AOS Recipes

This standalone corpus exports 193 QC-complete Greek recipe records from the Aetius TEI pipeline.

The primary artifacts are JSON data and documentation. The `site/` folder is a no-build browser for quick inspection.

## Data

- `data/recipes.json`: complete normalized recipe records.
- `data/recipes/*.json`: one complete record per recipe.
- `data/context_units.json`: proemia and contextual non-recipe units.
- `data/entities/index.json`: grouped entity occurrence index.
- `data/ingredient_lexicon.tsv`: deduplicated ingredient lookup table with article, nominative singular, genitive singular, and LSJ headword join key.
- `data/ingredient_lexicon.json`: ingredient lookup table plus source occurrence evidence and normalized-label variants.
- `data/sources.json`: source slice metadata.
- `data/review/quantity_gold/`: mirrored quantity-gold authority artifacts from
  `/home/seanm/github/aetius`. Current coverage uses the 193-recipe corpus;
  older archived runs may still record the former 174-record artifact-run
  denominator.
- `manifest.json`: export metadata, source commit, included paths, excluded paths, and counts.

## Sources

| Source | Dataset key | Recipes | Source JSON |
|---|---:|---:|---|
| Aëtius Book 16 myrepsika | `aetius_book16_myrepsika` | 45 | `experiments/aetius-book16-ch126-153-myrepsika/data/aetius_book16_ch126_153_myrepsika.json` |
| Aëtius Book 1 oils | `aetius_book1_oils` | 43 | `experiments/aetius-book1-ch99-136-oils/data/aetius_book1_ch99_136_oils.json` |
| Dioscorides Book 1 perfumes and resins | `dioscorides_book1_perfumes_resins` | 52 | `experiments/dioscorides-book1-perfumes-resins/data/dioscorides_book1_perfumes_resins.json` |
| Dioscorides Book 2 fats | `dioscorides_book2_fats` | 18 | `experiments/dioscorides-book2-fats/data/dioscorides_book2_fats.json` |
| Paul 7.20 perfumes | `paul_book7_perfumes` | 35 | `experiments/paul-book7-ch20-perfumes/data/paul_book7_ch20_perfumes.json` |

## Browse

Live: <https://alchemiesofscent.github.io/aos-recipes/>.

Or serve locally from the repo root:

```bash
python3 -m http.server 8000
```

Then open `http://127.0.0.1:8000/site/`.

## Validate

```bash
python3 scripts/validate.py
python3 scripts/extract_ingredient_lexicon.py --check
```

Quantity-gold mirror validation only:

```bash
python3 scripts/quantity_gold.py --validate
```

## Further reading

The full documentation is indexed by audience in [`docs/README.md`](docs/README.md). For the v1.0 freeze policy, the Definition of Done, and the release checklist, see [`docs/release_v1.md`](docs/release_v1.md).
