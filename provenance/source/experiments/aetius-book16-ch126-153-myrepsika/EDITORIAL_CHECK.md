# QC And Editorial Check

## Automated QC

- `python3 -m py_compile experiments/aetius-book16-ch126-153-myrepsika/extract.py`
- `python3 experiments/aetius-book16-ch126-153-myrepsika/extract.py`
- `node --check experiments/aetius-book16-ch126-153-myrepsika/app.js`
- `python3 - <<'PY' ... viewer static references ok ... PY`
- Result: `qc_report.json` returned `status: "ok"` with `44` entries across chapters `126-153`, no missing lemmas, no missing chapter names, no missing reconstructed Zervos pages or lines, no title-only entries, and all three chapter `130` `ἕψησις` subsections present.

## Editorial Review

- Verified chapter `126` against `tei/raw/tlg0718016.xml:4823-4845`: `t1-t2` are stored only as collection metadata, while `t3`, `4`, and `9` correctly title the three recipe blocks that begin at raw lines `1`, `5`, and `10`.
- Verified chapter `127` against `...:4846-4854`: the rebuild now splits the chapter into three recipes by treating the inline starts `Ἄλλο ξηρόμυρον.` and `Ἄλλο ξηρόμυρον φρυκτόν.` as separate units, with partial-line fragments preserved under the same reconstructed citations.
- Verified chapter `130` against `...:4864-4887`: the extractor keeps `ἐλαίου σάλκα σκευασία πολυτελής` as one entry with three internal subsections (`πρώτη`, `δευτέρα`, `τρίτη ἕψησις`), and then separates `ὑγρόμυρον` and `λευκόφυλλον` as sections `2` and `3`.
- Verified chapters `138` and `144` against `...:4962-4973` and `...:5042-5051`: all heading units now carry their full body text, so the prior title-only placeholders are gone.
- Verified newly recovered single-unit chapters `140`, `141`, `143`, `145`, `148`, `149`, `150`, and `152`: each now stores non-empty body text from the raw witness and contributes to the reconstructed Zervos page-line span.
- Verified later body-bearing chapters `146`, `151`, and `153`: chapter `146` still splits at the second formal title line, `151` remains a single body-bearing unit, and `153` preserves the final short recipe block.
- Confirmed that free-flowing `text` stores body prose only, while `zervos.lines` preserve the reconstructed title+body line sequence anchored at `161.7` and continued through the raw `<pb/>` breaks.
- Confirmed the viewer uses a Genitum-first local font stack (`local("Genitum")`, `local("Genitum Regular")`) with serif fallbacks because the repo does not contain a bundled Genitum font asset.
