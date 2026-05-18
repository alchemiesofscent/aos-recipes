# QC And Editorial Check

## Automated QC

- `python3 -m py_compile experiments/aetius-book1-ch99-136-oils/extract.py`
- `python3 experiments/aetius-book1-ch99-136-oils/extract.py`
- Result: `qc_report.json` returned `status: "ok"` with chapter `100` as the sole proemium block, `36` entry chapters (`101-136`), no missing chapters, and no missing lemmas, text, pages, or lineation.

## Editorial Review

- Verified the corrected witness is `tei/output/tlg0718.tlg001.aos-grc1.xml` and that file lines `913-1103` span chapters `99-136`.
- Applied the user’s clarified scope: chapter `100` is the proemium and chapters `101-136` are stored as one entry each, including advisory chapters such as `134` and `136`.
- Spot-checked chapters `101`, `108`, `113`, `117`, `124`, `128`, `131`, `134`, and `135` against the XML to confirm lemma extraction, page transitions, and Olivieri start/end citations.
- Confirmed `break="no"` joins are dehyphenated only in the free-flowing `text` field, while the stored `olivieri.lines` list preserves the edition’s line-by-line segmentation.
- The viewer uses a Genitum-first local font stack (`local("Genitum")`, `local("Genitum Regular")`) with Gentium/Palatino fallbacks because no bundled Genitum font asset is present in the repository.
