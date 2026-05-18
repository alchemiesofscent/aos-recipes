let chapterData = null;
let index = 0;
const COPY_SUCCESS_MS = 1600;
const ENTITY_GROUP_LABELS = [
  ["labels", "Preparation Labels"],
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
    if (window.DIOSCORIDES_BOOK2_FATS_DATA) {
      chapterData = window.DIOSCORIDES_BOOK2_FATS_DATA;
    } else {
      const response = await fetch("data/dioscorides_book2_fats.json");
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      chapterData = await response.json();
    }
  } catch (error) {
    const entry = document.getElementById("entry");
    entry.innerHTML = `
      <h2>Viewer data unavailable</h2>
      <p class="status">Open the generated data script directly or serve this folder over HTTP. Example: <code>python3 -m http.server</code></p>
      <p class="status">${escapeHtml(String(error))}</p>
    `;
    return;
  }

  document.getElementById("chapter-name").textContent =
    "Core fats from Dioscorides Book 2, split into distinct preparations and techniques with Wellmann lineation preserved.";
  renderSourceNotes();
  renderScope();
  bindNavigation();
  renderEntry();
}

function renderSourceNotes() {
  const container = document.getElementById("source-notes");
  container.innerHTML = chapterData.source.notes
    .map((note) => `<p class="source-note">${escapeHtml(note)}</p>`)
    .join("");
}

function renderScope() {
  const container = document.getElementById("scope");
  container.innerHTML = chapterData.entries
    .map(
      (entry) => `
        <section class="proemium-block">
          <div class="proemium-meta">Chapter ${escapeHtml(entry.chapter)} · Wellmann ${escapeHtml(entry.wellmann.citation.start)}-${escapeHtml(entry.wellmann.citation.end)}</div>
          <h3>${escapeHtml(entry.lemma)}</h3>
          <p class="proemium-text">${escapeHtml(entry.entry_kind)} · Section ${escapeHtml(entry.section || "")}</p>
        </section>
      `
    )
    .join("");
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

function renderEntry() {
  const entry = chapterData.entries[index];
  const entryEl = document.getElementById("entry");
  const counter = document.getElementById("counter");
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");

  counter.textContent = `${index + 1} of ${chapterData.entries.length}`;
  prevButton.disabled = index === 0;
  nextButton.disabled = index === chapterData.entries.length - 1;

  const section = entry.section ? ` · Section ${escapeHtml(entry.section)}` : "";
  const caveat = entry.caveat
    ? `<div class="caveat">${escapeHtml(entry.caveat)}</div>`
    : "";

  entryEl.innerHTML = `
    <div class="entry-topline">
      <h2>${escapeHtml(entry.lemma)}</h2>
      <div class="entry-meta">Book ${escapeHtml(entry.book)} · Chapter ${escapeHtml(entry.chapter)}${section}</div>
    </div>
    <div class="entry-meta">${escapeHtml(entry.chapter_name)} · ${escapeHtml(entry.entry_kind)} · ${escapeHtml(entry.source_kind)}</div>
    <div class="recipe-id">Recipe ID: ${escapeHtml(entry.derived_recipe_id || entry.id || "unlinked")}</div>
    <div class="line-range">Wellmann ${escapeHtml(entry.wellmann.citation.start)}-${escapeHtml(entry.wellmann.citation.end)} · pp. ${escapeHtml(entry.wellmann.pages.join(", "))}</div>
    ${caveat}
    ${renderCorrectionPanel(entry)}
    <p class="entry-text">${renderTextWithMarkers(entry)}</p>
    ${renderEntityGroups(entry.entity_groups)}
    <details class="lineation">
      <summary>Stored edition lineation</summary>
      <div class="line-list">
        ${entry.wellmann.lines
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

function renderTextWithMarkers(entry) {
  const text = String(entry.text || "");
  const markersByOffset = new Map();
  for (const marker of entry.section_markers || []) {
    const offset = Math.max(0, Math.min(text.length, Number(marker.offset || 0)));
    if (!markersByOffset.has(offset)) {
      markersByOffset.set(offset, []);
    }
    markersByOffset.get(offset).push(marker);
  }

  const offsets = Array.from(markersByOffset.keys()).sort((a, b) => a - b);
  let cursor = 0;
  let html = "";
  for (const offset of offsets) {
    if (offset > cursor) {
      html += escapeHtml(text.slice(cursor, offset));
    }
    html += markersByOffset.get(offset).map(renderSectionMarker).join("");
    cursor = offset;
  }
  html += escapeHtml(text.slice(cursor));
  return html;
}

function renderSectionMarker(marker) {
  const title = `Book ${marker.chapter}, section ${marker.section}`;
  return `<span class="section-marker" title="${escapeAttribute(title)}">${escapeHtml(marker.label || "")}</span>`;
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

function renderCorrectionPanel(entry) {
  return `
    <section class="correction-panel">
      <div class="correction-panel-header">
        <div>
          <h3 class="correction-panel-title">Correction Capture</h3>
          <p class="correction-panel-copy">Check affected items, describe the issue once, then copy JSON for this recipe.</p>
        </div>
        <button type="button" class="copy-correction">Copy JSON Correction</button>
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
    </section>
  `;
}

function renderEntityItem(groupKey, item, itemIndex) {
  const normalized = item.normalized_label && item.normalized_label !== item.surface_form
    ? `<span class="entity-normalized">Normalized: ${escapeHtml(item.normalized_label)}</span>`
    : "";
  const quantity = item.quantity_display
    ? `<span class="entity-normalized">Quantity: ${escapeHtml(item.quantity_display)}</span>`
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
          ${quantity}
        </span>
      </label>
    </li>
  `;
}

function bindCorrectionPanel(entry, entryEl) {
  const copyButton = entryEl.querySelector(".copy-correction");
  const status = entryEl.querySelector(".correction-status");
  if (!copyButton || !status) {
    return;
  }
  copyButton.addEventListener("click", async () => {
    try {
      if (!navigator.clipboard || typeof navigator.clipboard.writeText !== "function") {
        throw new Error("Clipboard API unavailable in this browser context.");
      }
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
  const selectedTargets = Array.from(entryEl.querySelectorAll(".correction-target:checked")).map((input) => {
    const target = {
      group: input.dataset.group || "",
      index: input.dataset.index ? Number(input.dataset.index) : null,
      surface_form: input.dataset.surfaceForm || "",
    };
    if (input.dataset.normalizedLabel) {
      target.normalized_label = input.dataset.normalizedLabel;
    }
    return target;
  });

  return {
    recipe_id: entry.derived_recipe_id || entry.id || "",
    lemma: entry.lemma || "",
    book: String(entry.book ?? ""),
    chapter: String(entry.chapter ?? ""),
    section: String(entry.section ?? ""),
    chapter_name: entry.chapter_name || "",
    selected_targets: selectedTargets,
    text_span: entryEl.querySelector('[name="text_span"]')?.value || "",
    current_issue: entryEl.querySelector('[name="current_issue"]')?.value || "",
    desired_correction: entryEl.querySelector('[name="desired_correction"]')?.value || "",
    notes_pattern: entryEl.querySelector('[name="notes_pattern"]')?.value || "",
    editor_label: entryEl.querySelector('[name="editor_label"]')?.value || "",
  };
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
