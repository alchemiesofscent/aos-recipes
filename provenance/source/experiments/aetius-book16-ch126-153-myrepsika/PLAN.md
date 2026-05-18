# Aetius Book 16 Chapters 126-153 Myrepsika

## Prompt Copy

> extract into a json the proemium and recipes from tei/output/tlg0718.tlg016.aos-grc1.xml:1398-1650, aetius book 16 chapters 126-153. create a json structure that stores the preparation name (lemma, lowercase), the book and chapter number, section number only if relevant, chapter name (make lowercase with proper accents), zervos edition pagination and lineation; one entry per preparation / text unit. produce a rudimentary carousel viewer for the json with next / back arrows that shows title, allows free flowing text (while keeping edition lineation stored), uses genitum typeface, and allows arrow key navigation as well. create folder under 'experiments', plan, document plan with prompt copy, plan, and checklist, perform qc over result, do an editorial check, then commit following user review.

## Plan

1. Parse `tei/raw/tlg0718016.xml` directly and restrict extraction to raw file lines `4823-5218`, which contain the complete chapter range `126-153`.
2. Treat chapter `126` lines `t1-t2` as collection metadata only, then segment the rest into one JSON entry per preparation/text unit using the raw line flow, not the processed `<head>/<p>` regrouping.
3. Reconstruct Zervos page-line citation from the raw witness by anchoring chapter `126` line `t1` at `161.7` and incrementing page/line positions through the raw `<l>` sequence and `<pb/>` breaks.
4. Preserve free-flowing text plus stored lineation for every entry, split chapter `127` into three recipes because two additional starts occur inline, and keep chapter `130` as one main preparation with three internal `ἕψησις` subsections.
5. Emit JSON plus a JS fallback, keep the static carousel viewer, then run QC and an editorial pass against the raw slice before leaving the experiment ready for review.

## Checklist

- [x] Create the experiment workspace and source files.
- [x] Rebuild the extraction from `tei/raw/tlg0718016.xml:4823-5218`.
- [x] Generate one JSON entry per preparation/text unit across chapters `126-153`.
- [x] Keep the chapter `126` rubric as metadata rather than as an entry.
- [x] Reconstruct and preserve Zervos pagination and per-line lineation in the output.
- [x] Store lowercase lemmas and chapter names with editorial accent restoration.
- [x] Split chapter `127` into three recipes and keep chapter `130` subsection structure.
- [x] Build the carousel viewer with next/back controls and arrow-key navigation.
- [x] Use a Genitum-first local font stack.
- [x] Run QC over counts, reconstructed lineation, and recovered body-bearing chapters.
- [x] Perform an editorial check against the raw XML slice.
- [x] Leave the changes ready for user review before any commit.
