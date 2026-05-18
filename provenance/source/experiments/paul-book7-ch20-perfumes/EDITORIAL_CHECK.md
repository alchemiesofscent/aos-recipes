# QC And Editorial Check

## Automated QC

- `python3 -m py_compile experiments/paul-book7-ch20-perfumes/extract.py`
- `python3 experiments/paul-book7-ch20-perfumes/extract.py`
- Result: `qc_report.json` returned `status: "ok"` with 35 perfume entries, no missing sections, no missing text, no missing lineation, and a chapter page span of Heiberg `2.380` through `2.391`.

## Editorial Review

- Verified the chapter title and proemium sections 1-3 were extracted separately from the perfume entries.
- Spot-checked sections 4, 7, 9, 16, 25, 27, 33, and 38 against the XML to confirm lemma wording, page transitions, and the start/end line citations.
- Confirmed `break="no"` joins are dehyphenated in the free-flowing body text while the stored line-by-line record keeps the edition segmentation intact.
- Kept section-head qualifiers in the lemma field when they distinguish recipe variants, for example `Ἄλλη γραφὴ κυπρίνου` and `Ἄλλο Σικυώνιον δραστικώτερον`.
- The viewer uses a Genitum-first local font stack (`local("Genitum")`, `local("Genitum Regular")`) with Gentium/Palatino fallbacks because no bundled Genitum font asset is present in the repository.
