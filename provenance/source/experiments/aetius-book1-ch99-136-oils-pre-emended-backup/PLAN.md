# Aetius Book 1 Chapters 99-136 Oils

## Prompt Copy

> extract into a json the proemium and recipes from tei/output/tlg0718.tlg001.aos-grc1.xml:913-1103, aetius book 1 chapters 99-136. create a json structure that stores the preparation name (lemma), the chapter, section, chapter name, olivieri edition pagination and lineation; one entry per preparation / text unit. produce a rudimentary carousel viewer for the json with next / back arrows that shows title, allows free flowing text (while keeping edition lineation stored), uses genitum typeface, and allows arrow key navigation as well. create folder under 'experiments', plan, document plan with prompt copy, plan, and checklist, perform qc over result, do an editorial check, then commit following user review.

## Plan

1. Parse the corrected Aëtius witness directly from `tei/output/tlg0718.tlg001.aos-grc1.xml` file lines `913-1103`.
2. Treat chapter `100` as the proemium and chapters `101-136` as the entry sequence, with one JSON entry per preparation/text unit rather than forcing a one-entry-per-chapter model.
3. Emit JSON plus a JS fallback that preserve Olivieri page/line data while exposing free-flowing text for display.
4. Build a small static carousel viewer with back/next buttons, arrow-key navigation, and a Genitum-first font stack.
5. Split inline secondary preparations where they function as distinct recipe units, notably `aetius-1-113-2`, `aetius-1-129-2`, the four later headed nard units in chapter `131`, and `aetius-1-132-2`, while preserving Olivieri lineation spans for each unit.
6. Run scripted QC, then perform an editorial pass against sampled chapters across the range.

## Checklist

- [x] Create the experiment workspace and source files.
- [x] Generate the JSON with chapter `100` as proemium.
- [x] Generate one entry per preparation/text unit for `101-136`.
- [x] Split the distinct inline preparations in chapters `113`, `129`, `131`, and `132` into separate viewer entries.
- [x] Keep Olivieri pagination and per-line lineation in the output.
- [x] Build the carousel viewer with next/back controls and arrow-key navigation.
- [x] Use a Genitum-first local font stack.
- [x] Run QC over counts, chapter coverage, and lineation completeness.
- [x] Perform an editorial check against the XML slice.
- [x] Leave the changes ready for user review before any commit.
