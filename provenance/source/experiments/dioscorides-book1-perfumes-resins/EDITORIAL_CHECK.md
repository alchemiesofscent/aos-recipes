# QC And Editorial Check

## Automated QC

- `python3 -m py_compile experiments/dioscorides-book1-perfumes-resins/extract.py`
- `python3 experiments/dioscorides-book1-perfumes-resins/extract.py`
- `node --check experiments/dioscorides-book1-perfumes-resins/app.js`
- Result: `qc_report.json` returned `status: "ok"` with `1` proemium block, `52` extracted entries, one apparatus-only `ἰασμέλαιον` entry, two resin-technique entries, and no missing text, pages, or lineation.

## Editorial Review

- Verified the prompt/source mismatch: raw lines `1590-1633` are book `1`, chapter `25` (`κῦφι`) in `tei/raw/tlg0656.tlg001.1st1K-grc1.xml`, not chapter `35`.
- Confirmed `κῦφι` is stored as its own chapter entry (`book 1`, chapter `25`) at the start of the carousel rather than as the proemium.
- Confirmed the dedicated proemium now comes from the later transition at chapter `42`, section `2` (raw lines `2306-2342`), which introduces the perfume material before chapter `43`.
- Spot-checked split entries against the XML for chapter `30` (`ἔλαιον ἀγρίας ἐλαίας`, `λευκανθὲν ἔλαιον`, `σικυώνιον`), chapter `31` (olive-shoot oil), chapter `36` (`κνήκινον`), chapter `58` (`μεγάλλειον`, `ἠδύχρουν`), and chapter `59` (`μενδήσιον`).
- Confirmed the `ἰασμέλαιον` entry is derived only from the apparatus note at raw lines `3195-3205` and is marked as coming from another recension rather than the witness’s main text.
- Confirmed the resin extraction is limited to chapter `71`, sections `5-6`, which are the explicit preparation/burning techniques within the requested `3695-3934` slice.
- Confirmed `break="no"` joins are dehyphenated only in the free-flow `text` field, while the stored `wellmann.lines` list keeps the per-line segmentation used by the viewer.
- The viewer uses a Genitum-first local font stack (`local("Genitum")`, `local("Genitum Regular")`) with Gentium/Palatino fallbacks because no bundled Genitum asset is present in the repository.
