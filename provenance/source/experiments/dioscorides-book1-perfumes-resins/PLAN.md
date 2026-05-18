# Dioscorides Book 1 Perfumes And Resins

## Prompt Copy

> examine experiments and plan the following. extract into a json the proemium and recipes from tei/raw/tlg0656.tlg001.1st1K-grc1.xml:1590-1633 Dioscorides book 1 chapter 35 wellmann, then 1855-3167, 3195-3205 for perfume recipes, including iasmelaion with caveat that it's in other recension. extract resin preparation technique from 3695-3934. create a json structure that stores the preparation name (lemma, lowercase), the book and chapter number, section number only if relevant, chapter name (make lowercase with proper accents), wellmann edition pagination and lineation; one entry per preparation / text unit. produce a rudimentary carousel viewer for the json with next / back arrows that shows title, allows free flowing text (while keeping edition lineation stored), uses genitum typeface, and allows arrow key navigation as well. create folder under 'experiments', plan, document plan with prompt copy, plan, and checklist, perform qc over result, do an editorial check, then commit following user review.

## Plan

1. Parse the raw Wellmann witness directly from `tei/raw/tlg0656.tlg001.1st1K-grc1.xml` and keep the requested raw slices explicit in the output metadata.
2. Treat raw lines `1590-1633` as a normal chapter entry for `κῦφι` (`book 1`, chapter `25`), because that is the chapter number in this witness even though the prompt called it chapter `35`.
3. Use the later transition at raw lines `2306-2342` (chapter `42`, section `2`) as the dedicated perfume proemium for the viewer and JSON.
4. Build a manual extraction spec for the perfume/oil span (`1855-3167`) so clear alternate methods and named variants become separate entries without flattening every explanatory section into its own card.
5. Store `ἰασμέλαιον` as a standalone caveated entry from the apparatus (`3195-3205`), anchored to the surrounding Wellmann citation rather than pretending it belongs to the main-text flow.
6. Restrict the resin output from `3695-3934` to the explicit preparation techniques in chapter `71`, sections `5-6`.
7. Emit JSON plus a JS fallback, then build a small static carousel viewer with back/next buttons, arrow-key navigation, free-flowing text, and a collapsible stored-lineation panel.
8. Run extractor/QC checks and complete an editorial pass over the chapter-numbering caveat, revised proemium, apparatus note, split entries, and resin techniques before leaving the work ready for review.

## Checklist

- [x] Create the experiment workspace and source files.
- [x] Generate the JSON with `κῦφι` as its own chapter entry and the later perfume-transition text as the dedicated proemium.
- [x] Generate one entry per preparation/text unit across the requested perfume and resin ranges.
- [x] Keep Wellmann pagination and per-line lineation in the output.
- [x] Include `ἰασμέλαιον` as an apparatus-derived caveated entry.
- [x] Build the carousel viewer with next/back controls and arrow-key navigation.
- [x] Use a Genitum-first local font stack.
- [x] Run QC over counts, required entries, and lineation completeness.
- [x] Perform an editorial check against the raw XML slices.
- [x] Leave the changes ready for user review before any commit.
