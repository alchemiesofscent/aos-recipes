# Data-Model & Schema Revision Policy

| | |
|---|---|
| **Version** | 0.1.0 (Proposed) |
| **Date** | 2026-06-05 |
| **Author** | Sean Coughlin (coughlin@flu.cas.cz) |
| **Status** | Proposed — for discussion, not yet adopted |
| **Supersedes** | none |
| **Applies to** | `data/recipes/*.json` (recipe-entity `schema_version 1.2`) and the `quantity-gold-v2` overlay |

## Why this document exists

The `aos-recipes` corpus (193 Greek pharmaceutical recipes from Dioscorides, Aëtius, and
Paul of Aegina) has a data model that grew in layers. It is good at recording *what a recipe
says*, but not yet good enough at recording it in a **queryable, interoperable** form. A
spot-check of eight representative recipes (see [Appendix A](#appendix-a--evidence-base))
shows that the three things the project most wants to *study* — quantities/measures,
processing modifications, and textual uncertainty/variants — are inconsistently or
informally encoded. This document records **where we are** and **what we should do**, so the
revision can proceed deliberately and be versioned.

This is a planning document. It changes no data and no code. It also lays out *how* the work
should be sequenced and versioned.

### Authority and scope

`/home/seanm/github/aetius` is the **source of truth**; `aos-recipes` is the
derived, **validate-only mirror** (see [`quantity_gold.md`](quantity_gold.md)). All schema,
authority-file, and vocabulary changes proposed here are **implemented upstream in `aetius`
and mirrored here** via the export commands. This policy document itself lives in
`aos-recipes` because it is the public-facing export, but it governs both repositories.

---

## 1. Where we are

### 1.1 Current layers

| Layer | Location | What it holds |
|---|---|---|
| Canonical recipe entities | `data/recipes/*.json`, `data/recipes.json` (`schema_version 1.2`) | `ingredients[].quantities[]`, inline `processes[].qualifiers[]`, `certainty`, `alternative_set_id`, `linked_process_ids`, `source_kind`, `emendations`, `other_preparations_mentioned`, `notes` |
| Quantity-gold overlay (v2) | `data/review/quantity_gold/` | `schema.json`, `recipes/*.json` records, `vocabularies/{metrology,temporal,process_qualifiers}.json`, `projection/{recipes,rich_recipes}.json`, `quantity_ledger.csv` |
| Metrology vocab (compat) | `data/metrology/units.json` | normalized units + dimensions |
| Validators | `scripts/validate.py`, `scripts/quantity_gold.py` | structural + overlay checks (mirror = validate-only) |

### 1.2 Strengths to preserve

- The gold overlay's **record model** (`record_type`, `dimension`, `qualifier_kind`,
  `temporal_label`, `value.kind` incl. `fraction`/`range`/`approximate`, `reference` for
  anaphora) and its **first-class rejection records** with `reason_code`.
- **Provenance and versioning** on every gold record (`run_id`, `source_commit`,
  `created/updated/reviewed_by`, `content_sha256_excluding_metadata`).
- **Non-mutating projections** — canonical JSON is never rewritten by the overlay.

### 1.3 Gaps (each blocks a study question)

| # | Finding | Blocks |
|---|---|---|
| F1 | **Frequency mislabeled as manner.** krokinon 1.54 stores "πλεονάκις τῆς ἡμέρας" / "συνεχῶς" as free-text `manner`; only "ἐπὶ ἡμέρας πέντε" is `duration`. | "which require daily / N×-per-day stirring" |
| F2 | **Durations are free text**, not number+unit (`"5 days"`, `"40 ἡμέραι"`, `"overnight"`, `"a short while"`). | "which require ≥5-day maceration" |
| F3 | **Time-points/ordinals collapsed into `duration`** ("τῇ ἕκτῃ" on the 6th day, "τῇ ἑξῆς" next day, "πρωὶ" morning). | scheduling vs elapsed-time queries |
| F4 | **No action/process vocabulary.** Every process has `base_label: null`, `process_type: null`; ἀνακίνει/ἀνακινήσας are unlinked surface forms; processes aren't linked to ingredients. | "which ingredients require stirring / boiling" |
| F5 | **Stated synonyms not captured.** sousinon 1.52 "ὃ ἔνιοι λείρινον καλοῦσιν" lives only in `text`. | synonym/identity resolution |
| F6 | **Authorial variants in prose only.** sousinon's "οἱ δέ" alternative ending is a free-text note; `alternative_set_id` is `null`. | variant-aware analysis |
| F7 | **Cross-recipe inheritance unmodeled** (krokinon: "ὡς εἴρηται ἐπὶ τοῦ σουσίνου, πλήθει καὶ συσταθμίᾳ τῇ αὐτῇ"). | resolving inherited quantities/processes |
| F8 | **Two unaligned qualifier vocabularies.** canonical `qualifier_type` = {manner, duration, location, exposure, other} vs gold `qualifier_kind` = {duration, frequency, repetition, interval, sequence, condition, temperature, manner, other}. | any cross-layer query |
| F9 | **Descriptor encoding inconsistent.** "ἴσον" is a `quantity` (descriptor/`same_as`) in krokinon but a `qualifier` in sousinon; `same_as` has no referent. | proportional-quantity queries |
| F10 | **Internal list-vs-procedure quantity variants** (Aëtius 1.135: list "𐆄 ε" uncertain vs procedure "ξέστας ε" certain) recorded only in prose. | quantity reliability |
| F11 | **Staged intermediate products** (sousinon's re-pressed μύρον; repeated infusion cycles) — recipes are DAGs, modeled as flat lists. | process-structure queries |
| F12 | **Concept identity fused with modifiers** ("στέαρ ταύρειον", "κρόκος Κιλίκιος"); same plant gets different head-nouns (κρίνον vs πέταλα κρίνου). | cross-recipe ingredient identity |
| F13 | **Stages mislabeled as `location`** (Aëtius 1.132 "ἐν τῇ πρώτῃ/δευτέρᾳ/τρίτῃ ἑψήσει"). | stage-aware queries |
| F14 | **Variants handled by file-splitting without linkage** (Aëtius 1.132-2 "Ἰωάννης μυρεψός" variant; cf. 1.129/-129-2, 1.131…-131-5) — `alternative_set_id: null`, note-only. | grouping variant sets |
| F15 | **Range & indefinite values** ("ἐπὶ ἡμέρας β ἢ γ"; "ἐφ' ἱκανόν"; "τὸ ἀρκοῦν") not structured at canonical level. | dosage/duration ranges |
| F16 | **Frequency with explicit count, and anaphoric frequency** (Paul 7.20.8 "τρὶς τῆς ἡμέρας"; "κινοῦντες ὁμοίως"). | rate queries |
| F17 | **Explicit batch division & intervals** (Paul 7.20.8 "εἰς τρεῖς ἐμβολὰς"; "μετὰ γ ἡμέρας"). | multi-batch process queries |
| F18 | **Multi-product / by-product records** (Aëtius 1.132 δευτέριον from residue, ingredients flagged by note only). | product/by-product modeling |
| F19 | **Vocabulary drift / unresolved units.** Ad-hoc `qualifier_type` values appear inline (`exposure`=ἡλίου, `color`=λευκή); symbolic units (𐆄, ξ̸, γρ=gramma, 𐅻=drachme) often left `uncertain`. | governance, normalization |

**Coverage reality.** The gold pipeline has produced **1 reviewed recipe of 193**
(`dioscorides-1-25-kyphi`). The overlay still reports a `174` denominator from a run that
predates the Book 2 fats slice and the later Aëtius Book 16 split; the current corpus is
`193`. This must be reconciled on the
next full run (see [W4](#w4--execute-and-version-the-gold-pipeline)).

**Conclusion.** The recipes require revision. The canonical inline qualifiers are
un-normalized and use a narrower, partly-misapplied vocabulary than the gold overlay; the two
layers must be reconciled and the process/quantity/variant phenomena normalized.

---

## 2. What we should do

Five workstreams. Each states the problem, the proposed model, the query it enables, and
where it lands.

### W1 — Controlled-term authority layer (concept thesaurus) *(centerpiece)*

*Addresses F4, F5, F7, F12.*

Introduce **authority files** (one per domain: ingredients, actions/processes,
manner/intensity, equipment/vessels, products, qualities, heat/exposure, and a
witness/authority register). Each concept is a record with:

- a **minted stable ID**, e.g. `urn:aos:concept:ingredient:sousinon-0001`;
- `pref_label` (headword/lemma), `alt_labels` (orthographic variants),
  `synonyms` (e.g. σούσινον / λίρινον / κρίνινον — each with attestation locus + provenance),
  `broader` / `narrower` / `related`, `lang`, `notes`, `provenance`, `version`.

**Resolution chain** wired into recipes — *inflected surface form → headword/lemma →
concept*: add a `concept_id` foreign key to ingredient **and** process entities, reusing the
existing `surface_form` → `base_label` path. **Separate identity from modifiers** (F12):
quality modifiers move to qualifiers, not into `normalized_label`.

**ID recommendation.** Mint **stable opaque IDs** for concepts. Do **not** content-hash
labels: labels get corrected over time, which would churn the hash and break every link.
Reserve content hashing for *record integrity* (already done via
`content_sha256_excluding_metadata`). Surface occurrences may carry a deterministic
occurrence id for traceability.

*Enables:* "all recipes using the lily-perfume concept regardless of spelling/synonym";
"every occurrence of *stir* across the corpus".

### W2 — Process-modification model (make it studyable)

*Addresses F1, F2, F3, F4, F8, F13, F15, F16, F17, F18, F19.*

- **Reconcile the two qualifier vocabularies** into one governed set (close the canonical
  `qualifier_type` ⟷ gold `qualifier_kind` gap). Promote missing/ad-hoc kinds to first class:
  `frequency`; `exposure`/heat-source; a time-`point`/`schedule` kind distinct from
  `duration` (F3); a `stage` kind (F13). Reclassify `color` as an ingredient quality, not a
  process qualifier.
- **Decompose** a compound instruction into linked records on one process target. Worked
  example (Paul 7.20.8, "βρέξαντες ἐπὶ ε ἡμέρας κινοῦντες τρὶς τῆς ἡμέρας" = soak 5 days,
  stirring three times a day):
  - action = `stir` (concept),
  - manner = controlled intensity term (if present),
  - **frequency** = normalized rate (count 3 / per day),
  - **duration** = number 5 / temporal-unit day.
- **Normalize frequency** into the `rate` dimension, supporting explicit count-per-period
  **and** anaphoric reference ("ὁμοίως", F16) reusing the gold `reference` mechanism.
  **Normalize durations** into number + temporal-unit, with **range** and
  **indefinite/ad-libitum** value kinds (F15). **Promote manner/intensity** to first-class
  with a controlled vocabulary (today κατακόρως is rejected; καθαρίως/ἐπιμελῶς/συνεχῶς are
  free text).
- **Link process → ingredient targets** (`target.concept_id`, recipe `linked_process_ids`).
- **Model staging explicitly** (F11, F13, F17, F18): processing stages/batches with order and
  inter-stage intervals; intermediate and secondary products (δευτέριον, re-pressed μύρον) as
  nodes — recipes as DAGs, not flat lists. Add **cross-recipe inheritance** (F7) via typed
  references (`see_recipe`, `same_quantity_as`, `same_process_as`). *Staging/DAG and
  inheritance are a stretch phase if they prove heavy.*

*Enables:* "which ingredients require vigorous stirring / daily (or N×/day) stirring /
≥5-day maceration / sun-exposure / multi-batch infusion".

### W3 — Uncertainty and lightweight variant readings

*Addresses F5, F6, F9, F10, F14, and uncertainty generally. (Decision: lightweight variant
arrays, not a full TEI apparatus.)*

- **Graded uncertainty** (e.g. `certain` / `probable` / `possible` / `conjectural`) layered
  onto the current binary `certainty`.
- **`variant_readings[]`** on quantities/records/ingredients:
  `{ source_type (manuscript | recension | in_text_variant | attributed | editorial),
  siglum_or_authority, reading, normalized_value, normalized_unit, support,
  editorial_decision (lemma | variant | rejected), source_ref, note }`. This covers
  manuscript witnesses, in-text "οἱ δέ / ἔνιοι" variants (F6), attributed variants
  ("Ἰωάννης μυρεψός", F14), and internal list-vs-procedure attestations (F10). Sigla and
  named authorities resolve to the W1 register.
- **Group variant sets structurally.** Actually use `alternative_set_id`, and add a
  cross-record `variant_set` linking split sibling files (e.g. `aetius-1-132` ⟷
  `aetius-1-132-2`) that today carry only free-text notes (F14). Connect to the existing
  `source_kind: apparatus_other_recension` and `emendations` (already populated, e.g. by
  Irene Cala in Aëtius 1.135 and 1.132).
- **Standardize descriptors** (F9): one encoding for "ἴσον" / "διπλάσιον" / "τὸ ἀρκοῦν", with
  an explicit referent for `same_as`.

### W4 — Execute and version the gold pipeline

*Incorporates [`quantity_gold.md`](quantity_gold.md).*

- Restate the authority/mirror split and the validate-only posture of this repo.
- Run the full LLM/gold generation across **all 193 recipes** in `aetius`, **reconcile
  174 → 193**, then `--export-derived` to this mirror.
- Define run/version cadence and acceptance gates:
  `generated_unreviewed` → `machine_validated` → `human_reviewed` →
  `accepted_for_projection` (→ `accepted_for_canonical_update` where warranted).

### W5 — Validation and versioning

- **Extend validators** (`scripts/validate.py`, `scripts/quantity_gold.py`): `concept_id`
  resolves to an authority record; variant `siglum_or_authority` resolves to the register;
  manner/action/exposure terms are in the controlled vocab; frequency and duration are
  normalized (not free text); (existing) span anchoring and duration relocation.
- **Version everything.** Adopt SemVer across: the recipe-entity schema, the quantity-gold
  schema, each controlled vocabulary, the authority files, and this policy document. Record
  them in a single `VERSIONS` manifest tied to `run_id` + `source_commit`. Current baselines:
  recipe-entity `1.2`; quantity-gold `quantity-gold-v2`; gold artifact `2026-06-05-codex-v1`;
  export `aos-recipes-export-v1`.

---

## 3. Interoperability stance

*(Decision: bespoke JSON + controlled vocabularies.)* The contract is bespoke JSON plus
governed controlled vocabularies. The interoperability surface is **stable URNs** plus
**CTS-style line citations** (`recipe_urn`, `record_urn`, `line_citations`). An optional
future crosswalk to SKOS/TEI is explicitly **out of scope** for this revision but is not
precluded by it — the authority layer (W1) is deliberately SKOS-shaped to keep that door open.

---

## 4. Phasing and sequence

1. **Authority layer + concept IDs** (ingredients + actions) — W1.
2. **Process model**: reconciled qualifier vocab + frequency/duration normalization — W2.
3. **Variant + uncertainty model** — W3.
4. **Full gold run + export** — W4.
5. **Validators + `VERSIONS` manifest** — W5.

Cross-recipe inheritance and staging/DAG (within W2) are a **stretch phase**. Every phase is
implemented in `aetius` and mirrored to `aos-recipes`.

---

## 5. Decisions log and open questions

**Locked (2026-06-05):**

- Deliverable is this policy document only; no schema/code changes yet.
- Variant model is **lightweight variant arrays**, not a full TEI apparatus.
- Interoperability is **bespoke JSON + controlled vocabularies**.

**Open:**

- Exact graded-uncertainty scale and its mapping from the current binary `certainty`.
- Manner/intensity vocabulary granularity.
- Concept-ID minting authority and format.
- Whether to model staging/DAG and multi-product (δευτέριον / by-product) records now or in
  the stretch phase.
- How far to normalize cross-recipe quantity inheritance (resolve vs merely link).
- Whether to keep variants as split sibling files linked by `variant_set`, or merge them into
  one record with alternative branches.

---

## Appendix A — Evidence base

Findings F1–F19 were drawn from a spot-check of these records (read, unchanged):

`data/recipes/dioscorides-1-25-kyphi.json` (also the one reviewed gold recipe),
`dioscorides-1-52-sousinon.json`, `dioscorides-1-54-krokinon.json`,
`dioscorides-2-76-sampsuchized-stear.json`, `aetius-1-135.json` (Καπνιστὸν ἔλαιον),
`aetius-1-132.json` and `aetius-1-132-2.json` (salka oil + John-the-perfumer variant),
`paul-7-20-5.json` (Χαμαιμήλινον), `paul-7-20-8.json` (Σούσινον σύνθετον).

Cross-references: [`schema.md`](schema.md), [`quantity_gold.md`](quantity_gold.md),
`data/review/quantity_gold/schema.json`,
`data/review/quantity_gold/vocabularies/{metrology,temporal,process_qualifiers}.json`.
