let experimentData = null;
let index = 0;
const COPY_SUCCESS_MS = 1600;
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
    if (window.AETIUS_BOOK16_CH126_153_MYREPSIKA_DATA) {
      experimentData = window.AETIUS_BOOK16_CH126_153_MYREPSIKA_DATA;
    } else {
      const response = await fetch("data/aetius_book16_ch126_153_myrepsika.json");
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      experimentData = await response.json();
    }
  } catch (error) {
    const entry = document.getElementById("entry");
    entry.innerHTML = `
      <h2>Viewer data unavailable</h2>
      <p class="status">Serve this folder over HTTP or load the generated data script directly.</p>
      <p class="status">${escapeHtml(String(error))}</p>
    `;
    return;
  }

  renderContext();
  bindNavigation();
  renderEntry();
}

function renderContext() {
  const partTitle = document.getElementById("part-title");
  const summary = document.getElementById("collection-summary");
  const editionRange = document.getElementById("edition-range");
  const coverage = document.getElementById("coverage");
  const zervos = experimentData.work.part_title_zervos.citation;

  partTitle.textContent = experimentData.work.part_title;
  summary.textContent = "Recipes rebuilt from the raw Zervos witness for Aëtius XVI 126-153, with page-line citation reconstructed from the raw line flow.";
  editionRange.textContent = `${zervos.start}-${zervos.end}`;
  coverage.textContent = `Book ${experimentData.work.book} · ${experimentData.entries.length} units · pp. ${experimentData.work.page_span.join(", ")}`;
}

function bindNavigation() {
  document.getElementById("prev").addEventListener("click", () => move(-1));
  document.getElementById("next").addEventListener("click", () => move(1));
  document.addEventListener("keydown", (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey) {
      return;
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      move(-1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      move(1);
    }
  });
}

function move(delta) {
  if (!experimentData) {
    return;
  }
  const nextIndex = index + delta;
  if (nextIndex < 0 || nextIndex >= experimentData.entries.length) {
    return;
  }
  index = nextIndex;
  renderEntry();
}

function renderEntry() {
  const entry = experimentData.entries[index];
  const entryEl = document.getElementById("entry");
  const counter = document.getElementById("counter");
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");

  counter.textContent = `${index + 1} of ${experimentData.entries.length}`;
  prevButton.disabled = index === 0;
  nextButton.disabled = index === experimentData.entries.length - 1;

  const sectionLabel = entry.section ? ` · Section ${escapeHtml(entry.section)}` : "";
  const textBlock = entry.title_only
    ? `<p class="empty-text">No body text survives in this XML slice for this titled unit.</p>`
    : entry.subsections
      ? renderSubsections(entry.subsections)
      : `<p class="entry-text">${escapeHtml(entry.text)}</p>`;

  entryEl.innerHTML = `
    <div class="entry-topline">
      <h2>${escapeHtml(entry.lemma)}</h2>
      <div class="entry-meta">Book ${escapeHtml(entry.book)} · Chapter ${escapeHtml(entry.chapter)}${sectionLabel}</div>
    </div>
    <div class="entry-meta">${escapeHtml(entry.chapter_name)}</div>
    <div class="recipe-id">Recipe ID: ${escapeHtml(entry.derived_recipe_id || entry.id || "unlinked")}</div>
    <div class="line-range">Zervos ${escapeHtml(entry.zervos.citation.start)}-${escapeHtml(entry.zervos.citation.end)} · pp. ${escapeHtml(entry.zervos.pages.join(", "))}</div>
    ${renderCorrectionPanel(entry)}
    ${textBlock}
    ${renderEntityGroups(entry.entity_groups)}
    <details class="lineation">
      <summary>Stored edition lineation</summary>
      <div class="line-list">
        ${renderLines(entry.zervos.lines)}
      </div>
    </details>
  `;
  bindCorrectionPanel(entry, entryEl);
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

function renderSubsections(subsections) {
  return `
    <div class="subsections">
      ${subsections
        .map(
          (subsection) => `
            <section class="subsection">
              <div class="subsection-kicker">Section ${escapeHtml(subsection.section)} · Zervos ${escapeHtml(subsection.zervos.citation.start)}-${escapeHtml(subsection.zervos.citation.end)}</div>
              <h3>${escapeHtml(subsection.title)}</h3>
              <p class="entry-text">${escapeHtml(subsection.text)}</p>
            </section>
          `
        )
        .join("")}
    </div>
  `;
}

function renderLines(lines) {
  return lines
    .map(
      (line) => `
        <div class="line">
          <div class="line-label">${escapeHtml(line.page)}.${escapeHtml(line.line)}</div>
          <div>${escapeHtml(line.text)}</div>
        </div>
      `
    )
    .join("");
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
