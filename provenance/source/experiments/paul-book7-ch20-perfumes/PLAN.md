# Paul Book 7 Chapter 20 Perfumes

## Prompt Copy

> extract into a json the proemium and recipes from tei/output/tlg0715.tlg001.aos-grc1.cmg9_2.xml:7136-7481 paul book 7 chapter 20. create a json structure that stores the preparation name (lemma), the chapter, section, chapter name, heiberg edition pagination and lineation; one entry per perfume. produce a rudimentary carousel viewer for the json with next / back arrows that shows title, allows free flowing text (while keeping edition lineation stored), uses genitum typeface, and allows arrow key navigation as well. create folder under 'experiments', plan, document plan with prompt copy, plan, and checklist, perform qc over result, do an editorial check, then commit following user review.

## Plan

1. Parse the chapter directly from the TEI and isolate the chapter title, proemium sections 1-3, and perfume sections 4-38.
2. Emit a JSON artifact with chapter metadata, a structured proemium block, and one perfume entry per section, keeping both free-flowing text and exact Heiberg page/line records.
3. Build a small static viewer that reads the JSON, shows the chapter proemium, and pages through perfume entries with button and keyboard navigation.
4. Run extractor/QC checks, then complete an editorial pass against the source for lemma wording, section boundaries, pagination, and line joins.

## Checklist

- [x] Create the experiment workspace and source files.
- [x] Generate the JSON with proemium plus one perfume entry per recipe section.
- [x] Keep Heiberg pagination and per-line lineation in the output.
- [x] Build the carousel viewer with back/next controls and arrow key navigation.
- [x] Use a Genitum-first font stack in the viewer.
- [x] Run QC over counts, section coverage, and page/line spans.
- [x] Perform an editorial check against the XML slice.
- [x] Leave changes ready for user review before any commit.
