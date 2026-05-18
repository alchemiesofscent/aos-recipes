# Aetius Book 1 Chapters 99-136 Oils (Stable Emended Source)

## Prompt Copy

> extract into a json the proemium and recipes from tei/output/tlg0718.tlg001.aos-grc1.xml:913-1103, aetius book 1 chapters 99-136. create a json structure that stores the preparation name (lemma), the chapter, section, chapter name, olivieri edition pagination and lineation; one entry per preparation / text unit. produce a rudimentary carousel viewer for the json with next / back arrows that shows title, allows free flowing text (while keeping edition lineation stored), uses genitum typeface, and allows arrow key navigation as well. create folder under 'experiments', plan, document plan with prompt copy, plan, and checklist, perform qc over result, do an editorial check, then commit following user review.

## Current State

- This folder is now the live Aëtius Book 1 source slice.
- The pre-emended rollback copy now lives at `experiments/aetius-book1-ch99-136-oils-pre-emended-backup/`.
- The experiment keeps the emended running text, original Olivieri text, emendation overlay metadata, and the protected Book 1 split behavior.
- The viewer shows the emended display text by default while preserving Olivieri page/line data.

## Checklist

- [x] Fold the emended working experiment back into the stable Book 1 slice.
- [x] Generate the JSON with chapter `100` as proemium.
- [x] Generate one entry per preparation/text unit for `101-136`.
- [x] Preserve the current split preparations in chapters `113`, `129`, `131`, and `132`.
- [x] Emit `text`, `original_text`, `text_source`, `emendations`, and `emendation_count` per entry.
- [x] Generate machine-readable emendation metadata from `experiments/revised-aetius-1-99-136.txt`.
- [x] Keep Olivieri pagination and per-line lineation in the output.
- [x] Update the copied viewer to show emended display text and compact emendation details.
- [x] Run QC over counts, chapter coverage, split IDs, and emended-text coverage.
- [ ] Wire the Book 1-only prompt/authority regeneration path and review-only authority diff.
