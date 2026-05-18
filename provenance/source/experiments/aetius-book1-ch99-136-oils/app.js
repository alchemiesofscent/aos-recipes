let chapterData = null;
let index = 0;
const COPY_SUCCESS_MS = 1600;
const CORRECTION_DRAFT_STORAGE_PREFIX = "aetius-book1-correction-draft";
const NUMERAL_CONTEXT_RE = /([𐆄Χ𐅻]\s*|ξ̸ε\s+|(?:λίτρα(?:ι|ς|ν)?|λίτρα(?:ι|ς|ν)?|γρ|ἡμέρας|ἡμέρας|ἡμέραν|ἡμέραν|ὥρας|ὥραν|νύκτα|νύκτα|ξέστ(?:ης|ην|αι|ας|ῃ|ῳ)?|ξέστ(?:ης|ην|αι|ας|ῃ|ῳ)?|ἰταλικ(?:ὸς|ὸν|οῦ|οί))\s+)([α-ωϛϙς]{1,3})(?=$|[\s.,;··:])/gu;
const ENTITY_GROUP_LABELS = [
  ["ingredients", "Ingredients"],
  ["processes", "Processes"],
  ["tools", "Tools"],
  ["other_preparations_mentioned", "Other Preparations Mentioned"],
  ["preparation_names", "Preparation Names"],
  ["people", "People"],
  ["places", "Places"],
  ["works_mentioned", "Works Mentioned"],
];

async function init() {
  try {
    const response = await fetch("data/aetius_book1_ch99_136_oils.json", {
      cache: "no-store",
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    chapterData = await response.json();
  } catch (error) {
    const entry = document.getElementById("entry");
    entry.innerHTML = `
      <h2>Viewer data unavailable</h2>
      <p class="status">Open the generated data script directly or serve this folder over HTTP. Example: <code>python3 -m http.server</code></p>
      <p class="status">${escapeHtml(String(error))}</p>
    `;
    return;
  }

  document.getElementById("chapter-name").textContent = `Chapters 100-136 with emended display text and preserved Olivieri lineation · proemium title: ${chapterData.proemium[0].chapter_name}`;
  renderProemium();
  bindNavigation();
  renderEntry();
}

function bindNavigation() {
  document.getElementById("prev").addEventListener("click", () => move(-1));
  document.getElementById("next").addEventListener("click", () => move(1));
  document.addEventListener("keydown", (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey) {
      return;
    }
    if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
      event.preventDefault();
      move(-1);
    }
    if (event.key === "ArrowRight" || event.key === "ArrowDown") {
      event.preventDefault();
      move(1);
    }
  });
}

function move(delta) {
  if (!chapterData) {
    return;
  }
  const nextIndex = index + delta;
  if (nextIndex < 0 || nextIndex >= chapterData.entries.length) {
    return;
  }
  index = nextIndex;
  renderEntry();
}

function renderProemium() {
  const container = document.getElementById("proemium");
  container.innerHTML = chapterData.proemium
    .map(
      (section) => `
        <section class="proemium-block">
          <div class="proemium-meta">Chapter ${escapeHtml(section.chapter)} · Olivieri ${escapeHtml(section.olivieri.citation.start)}-${escapeHtml(section.olivieri.citation.end)}</div>
          <h3>${escapeHtml(section.chapter_name)}</h3>
          <p class="proemium-text">${escapeHtml(section.text)}</p>
        </section>
      `
    )
    .join("");
}

function renderEntry() {
  const entry = chapterData.entries[index];
  const correctionDraft = loadCorrectionDraft(entry);
  const entryEl = document.getElementById("entry");
  const counter = document.getElementById("counter");
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");

  counter.textContent = `${index + 1} of ${chapterData.entries.length}`;
  prevButton.disabled = index === 0;
  nextButton.disabled = index === chapterData.entries.length - 1;

  entryEl.innerHTML = `
    <div class="entry-topline">
      <h2>${escapeHtml(entry.lemma)}</h2>
      <div class="entry-meta">Book ${escapeHtml(entry.book)} · Chapter ${escapeHtml(entry.chapter)} · Section ${escapeHtml(entry.section)}</div>
    </div>
    <div class="entry-meta">${escapeHtml(entry.chapter_name)}</div>
    <div class="recipe-id">Recipe ID: ${escapeHtml(entry.derived_recipe_id || entry.id || "unlinked")}</div>
    <div class="line-range">Olivieri ${escapeHtml(entry.olivieri.citation.start)}-${escapeHtml(entry.olivieri.citation.end)} · pp. ${escapeHtml(entry.olivieri.pages.join(", "))}</div>
    <div class="display-status">${escapeHtml(renderDisplayStatus(entry))}</div>
    <p class="entry-text">${formatDisplayText(entry.text)}</p>
    ${renderEmendations(entry)}
    ${renderCorrectionPanel(entry, correctionDraft)}
    ${renderEntityGroups(entry.entity_groups)}
    <details class="lineation">
      <summary>Stored edition lineation</summary>
      <div class="line-list">
        ${entry.olivieri.lines
          .map(
            (line) => `
              <div class="line">
                <div class="line-label">${escapeHtml(line.page)}.${escapeHtml(line.line)}</div>
                <div>${escapeHtml(line.text)}</div>
              </div>
            `
          )
          .join("")}
      </div>
    </details>
  `;
  bindCorrectionPanel(entry, entryEl);
}

function formatDisplayText(text) {
  return escapeHtml(text).replace(
    NUMERAL_CONTEXT_RE,
    (_, prefix, numeral) => `${prefix}${numeral}ʹ`,
  );
}

function renderDisplayStatus(entry) {
  if (entry.text_source === "emended") {
    return "Display text: emended from Olivieri";
  }
  return "Display text: Olivieri";
}

function renderEmendations(entry) {
  if (!entry.emendation_count) {
    return "";
  }
  return `
    <details class="emendations">
      <summary>Emendations (${entry.emendation_count})</summary>
      <ul class="emendation-list">
        ${entry.emendations.map(renderEmendationItem).join("")}
      </ul>
    </details>
  `;
}

function renderEmendationItem(item) {
  const status = item.decision === "rejected" ? "rejected suggestion" : item.operation;
  const olivieri = item.olivieri_text
    ? `<div class="emendation-text"><strong>Olivieri:</strong> ${escapeHtml(item.olivieri_text)}</div>`
    : "";
  const adopted = item.adopted_text
    ? `<div class="emendation-text"><strong>Adopted:</strong> ${escapeHtml(item.adopted_text)}</div>`
    : "";
  const note = item.note
    ? `<div class="emendation-text"><strong>Note:</strong> ${escapeHtml(item.note)}</div>`
    : "";
  return `
    <li class="emendation-item">
      <div class="emendation-meta">${escapeHtml(item.locus)} · ${escapeHtml(status)} · ${escapeHtml(item.proposal_author)}</div>
      ${olivieri}
      ${adopted}
      ${note}
    </li>
  `;
}

function renderEntityGroups(entityGroups = {}) {
  const sections = ENTITY_GROUP_LABELS.map(([key, label]) => {
    const items = Array.isArray(entityGroups[key]) ? entityGroups[key] : [];
    if (!items.length) {
      return "";
    }
    return `
      <section class="entity-group">
        <h3 class="entity-group-heading">${escapeHtml(label)}</h3>
        <ul class="entity-list">
          ${items.map((item, itemIndex) => renderEntityItem(key, item, itemIndex)).join("")}
        </ul>
      </section>
    `;
  })
    .filter(Boolean)
    .join("");

  return `
    <section class="entity-block">
      <h3 class="entity-block-title">Derived Recipe Contents</h3>
      ${sections || '<p class="entity-empty">No derived ingredients, processes, or related entities recorded for this entry.</p>'}
    </section>
  `;
}

function renderCorrectionPanel(entry, draft = null) {
  const isOpen = correctionPanelStartsOpen(draft);
  return `
    <details class="correction-panel"${isOpen ? " open" : ""}>
      <summary class="correction-panel-summary">
        <span class="correction-panel-summary-text">
          <span class="correction-panel-title">Correction Capture</span>
          <span class="correction-panel-copy">Per-recipe draft saved in this browser.</span>
        </span>
      </summary>
      <div class="correction-panel-body">
        <div class="correction-panel-header">
          <p class="correction-panel-copy">Check affected items, describe the issue once, then copy JSON for this recipe.</p>
          <div class="correction-actions">
            <button type="button" class="clear-correction">Clear Saved Draft</button>
            <button type="button" class="copy-correction">Copy JSON Correction</button>
          </div>
        </div>
        <label class="correction-select correction-select-meta">
          <input
            class="correction-target"
            type="checkbox"
            data-group="preparation"
            data-surface-form="${escapeAttribute(entry.lemma || "")}"
            data-normalized-label="${escapeAttribute(entry.chapter_name || entry.lemma || "")}"
          />
          <span class="correction-target-meta">Preparation/title/meta issue</span>
        </label>
        <div class="correction-fields">
          <label class="correction-field">
            <span>text_span</span>
            <textarea name="text_span" rows="2"></textarea>
          </label>
          <label class="correction-field">
            <span>current_issue</span>
            <textarea name="current_issue" rows="3"></textarea>
          </label>
          <label class="correction-field">
            <span>desired_correction</span>
            <textarea name="desired_correction" rows="3"></textarea>
          </label>
          <label class="correction-field">
            <span>notes_pattern</span>
            <textarea name="notes_pattern" rows="2"></textarea>
          </label>
          <label class="correction-field">
            <span>editor_label</span>
            <input name="editor_label" type="text" value="" />
          </label>
        </div>
        <div class="correction-status" aria-live="polite"></div>
      </div>
    </details>
  `;
}

function renderEntityItem(groupKey, item, itemIndex) {
  const normalized = item.normalized_label && item.normalized_label !== item.surface_form
    ? `<span class="entity-normalized">Normalized: ${escapeHtml(item.normalized_label)}</span>`
    : "";
  const quantityDisplay = groupKey === "ingredients" && item.quantity_display
    ? `<span class="entity-quantity">Greek quantity: ${formatDisplayText(item.quantity_display)}</span>`
    : "";
  return `
    <li class="entity-item">
      <label class="entity-select">
        <input
          class="correction-target entity-check"
          type="checkbox"
          data-group="${escapeAttribute(groupKey)}"
          data-index="${itemIndex}"
          data-surface-form="${escapeAttribute(item.surface_form || "")}"
          data-normalized-label="${escapeAttribute(item.normalized_label || "")}"
        />
        <span class="entity-body">
          <span class="entity-surface">${escapeHtml(item.surface_form)}</span>
          ${normalized}
          ${quantityDisplay}
        </span>
      </label>
    </li>
  `;
}

function bindCorrectionPanel(entry, entryEl) {
  const panel = entryEl.querySelector(".correction-panel");
  const copyButton = entryEl.querySelector(".copy-correction");
  const clearButton = entryEl.querySelector(".clear-correction");
  const status = entryEl.querySelector(".correction-status");
  if (!panel || !copyButton || !clearButton || !status) {
    return;
  }
  restoreCorrectionDraft(entry, entryEl);

  const persist = () => persistCorrectionDraft(entry, entryEl);
  panel.addEventListener("toggle", persist);
  entryEl.querySelectorAll(".correction-target").forEach((input) => {
    input.addEventListener("change", persist);
  });
  entryEl.querySelectorAll(".correction-field input, .correction-field textarea").forEach((field) => {
    field.addEventListener("input", persist);
    field.addEventListener("change", persist);
  });

  clearButton.addEventListener("click", () => {
    clearCorrectionDraft(entry);
    resetCorrectionPanel(entryEl);
    status.textContent = `Cleared saved draft for ${getCorrectionRecipeId(entry)}.`;
  });

  copyButton.addEventListener("click", async () => {
    try {
      if (!navigator.clipboard || typeof navigator.clipboard.writeText !== "function") {
        throw new Error("Clipboard API unavailable in this browser context.");
      }
      persist();
      const payload = buildCorrectionPayload(entry, entryEl);
      await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
      status.textContent = `Copied correction payload for ${entry.derived_recipe_id || entry.id || entry.lemma}.`;
      const originalLabel = copyButton.textContent;
      copyButton.textContent = "Copied";
      window.setTimeout(() => {
        if (copyButton.isConnected) {
          copyButton.textContent = originalLabel;
        }
      }, COPY_SUCCESS_MS);
    } catch (error) {
      status.textContent = `Copy failed: ${String(error)}`;
    }
  });
}

function buildCorrectionPayload(entry, entryEl) {
  const draft = collectCorrectionDraft(entry, entryEl);

  return {
    recipe_id: entry.derived_recipe_id || entry.id || "",
    lemma: entry.lemma || "",
    book: String(entry.book ?? ""),
    chapter: String(entry.chapter ?? ""),
    section: String(entry.section ?? ""),
    chapter_name: entry.chapter_name || "",
    selected_targets: draft.selected_targets,
    text_span: draft.text_span,
    current_issue: draft.current_issue,
    desired_correction: draft.desired_correction,
    notes_pattern: draft.notes_pattern,
    editor_label: draft.editor_label,
  };
}

function getCorrectionRecipeId(entry) {
  return entry.derived_recipe_id || entry.id || "";
}

function correctionDraftStorageKey(entry) {
  return `${CORRECTION_DRAFT_STORAGE_PREFIX}:${getCorrectionRecipeId(entry)}`;
}

function readCorrectionDraft(entry) {
  try {
    const stored = window.localStorage.getItem(correctionDraftStorageKey(entry));
    if (!stored) {
      return null;
    }
    const parsed = JSON.parse(stored);
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch (_error) {
    return null;
  }
}

function loadCorrectionDraft(entry) {
  return readCorrectionDraft(entry);
}

function writeCorrectionDraft(entry, draft) {
  try {
    window.localStorage.setItem(correctionDraftStorageKey(entry), JSON.stringify(draft));
  } catch (_error) {
    // Ignore localStorage failures and leave the viewer usable.
  }
}

function clearCorrectionDraft(entry) {
  try {
    window.localStorage.removeItem(correctionDraftStorageKey(entry));
  } catch (_error) {
    // Ignore localStorage failures and leave the viewer usable.
  }
}

function targetDescriptorFromInput(input) {
  const target = {
    group: input.dataset.group || "",
    index: input.dataset.index ? Number(input.dataset.index) : null,
    surface_form: input.dataset.surfaceForm || "",
  };
  if (input.dataset.normalizedLabel) {
    target.normalized_label = input.dataset.normalizedLabel;
  }
  return target;
}

function targetSignature(target) {
  return [
    target.group || "",
    target.index == null ? "" : String(target.index),
    target.surface_form || "",
    target.normalized_label || "",
  ].join("::");
}

function collectCorrectionDraft(entry, entryEl) {
  return {
    selected_targets: Array.from(entryEl.querySelectorAll(".correction-target:checked")).map(targetDescriptorFromInput),
    text_span: entryEl.querySelector('[name="text_span"]')?.value || "",
    current_issue: entryEl.querySelector('[name="current_issue"]')?.value || "",
    desired_correction: entryEl.querySelector('[name="desired_correction"]')?.value || "",
    notes_pattern: entryEl.querySelector('[name="notes_pattern"]')?.value || "",
    editor_label: entryEl.querySelector('[name="editor_label"]')?.value || "",
    is_open: Boolean(entryEl.querySelector(".correction-panel")?.open),
  };
}

function correctionDraftHasContent(draft) {
  if (!draft) {
    return false;
  }
  return Boolean(
    (draft.selected_targets && draft.selected_targets.length)
      || draft.text_span
      || draft.current_issue
      || draft.desired_correction
      || draft.notes_pattern
      || draft.editor_label,
  );
}

function correctionPanelStartsOpen(draft) {
  return Boolean(draft?.is_open || correctionDraftHasContent(draft));
}

function restoreCorrectionDraft(entry, entryEl) {
  const draft = loadCorrectionDraft(entry);
  if (!draft) {
    return;
  }
  const selected = new Set((draft.selected_targets || []).map(targetSignature));
  entryEl.querySelectorAll(".correction-target").forEach((input) => {
    input.checked = selected.has(targetSignature(targetDescriptorFromInput(input)));
  });
  const fields = ["text_span", "current_issue", "desired_correction", "notes_pattern", "editor_label"];
  fields.forEach((fieldName) => {
    const field = entryEl.querySelector(`[name="${fieldName}"]`);
    if (field && typeof draft[fieldName] === "string") {
      field.value = draft[fieldName];
    }
  });
  const panel = entryEl.querySelector(".correction-panel");
  if (panel) {
    panel.open = correctionPanelStartsOpen(draft);
  }
}

function persistCorrectionDraft(entry, entryEl) {
  const draft = collectCorrectionDraft(entry, entryEl);
  if (!draft.is_open && !correctionDraftHasContent(draft)) {
    clearCorrectionDraft(entry);
    return;
  }
  writeCorrectionDraft(entry, draft);
}

function resetCorrectionPanel(entryEl) {
  entryEl.querySelectorAll(".correction-target").forEach((input) => {
    input.checked = false;
  });
  entryEl.querySelectorAll(".correction-field input, .correction-field textarea").forEach((field) => {
    field.value = "";
  });
  const panel = entryEl.querySelector(".correction-panel");
  if (panel) {
    panel.open = false;
  }
}

function escapeHtml(value) {
  const node = document.createElement("div");
  node.textContent = value;
  return node.innerHTML;
}

function escapeAttribute(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

document.addEventListener("DOMContentLoaded", init);
