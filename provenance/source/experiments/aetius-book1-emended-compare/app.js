let compareData = null;
let currentFilter = null;
let currentRecipeId = null;

const FILTER_LABELS = {
  changed_emended: "Changed Emended",
  protected_changed: "Protected Changed",
  changed_non_emended: "Changed Non-Emended",
  unchanged: "Unchanged",
};

async function init() {
  try {
    if (window.AETIUS_BOOK1_EMENDED_COMPARE_DATA) {
      compareData = window.AETIUS_BOOK1_EMENDED_COMPARE_DATA;
    } else {
      const response = await fetch("data/aetius_book1_emended_compare.json");
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      compareData = await response.json();
    }
  } catch (error) {
    const compareCard = document.getElementById("compare-card");
    compareCard.innerHTML = `
      <h2>Comparison data unavailable</h2>
      <p class="status">Build the local compare dataset and serve this folder over HTTP. Example: <code>python3 scripts/recipes/build_aetius_book1_emended_compare.py</code></p>
      <p class="status">${escapeHtml(String(error))}</p>
    `;
    return;
  }

  document.getElementById("chapter-name").textContent =
    "Only changed recipes by default · baseline experiment vs emended experiment text, canonical authority vs review-only authority";

  bindControls();
  renderSummary();
  renderFilters();
  syncCurrentSelection();
  renderRecipeList();
  renderCard();
}

function bindControls() {
  document.getElementById("show-unchanged").addEventListener("change", () => {
    if (currentFilter === "unchanged" && !document.getElementById("show-unchanged").checked) {
      currentFilter = compareData.default_filter;
    }
    renderFilters();
    syncCurrentSelection();
    renderRecipeList();
    renderCard();
  });
}

function renderSummary() {
  const summary = compareData.summary;
  const container = document.getElementById("summary");
  const items = [
    ["Total", summary.total_recipes],
    ["Changed", summary.changed_recipes],
    ["Emended", summary.changed_emended],
    ["Non-Emended", summary.changed_non_emended],
    ["Protected", summary.protected_changed],
    ["Unchanged", summary.unchanged],
  ];
  container.innerHTML = items
    .map(
      ([label, value]) => `
        <div class="summary-item">
          <div class="summary-value">${escapeHtml(String(value))}</div>
          <div class="summary-label">${escapeHtml(label)}</div>
        </div>
      `
    )
    .join("");
}

function getVisibleFilterKeys() {
  const keys = ["changed_emended", "protected_changed", "changed_non_emended"];
  if (document.getElementById("show-unchanged").checked) {
    keys.push("unchanged");
  }
  return keys;
}

function renderFilters() {
  const container = document.getElementById("filters");
  const visibleKeys = getVisibleFilterKeys();
  if (!currentFilter || !visibleKeys.includes(currentFilter)) {
    currentFilter = compareData.default_filter;
  }
  container.innerHTML = visibleKeys
    .map((key) => {
      const count = compareData.filters[key].length;
      const active = key === currentFilter ? "active" : "";
      return `
        <button class="filter-button ${active}" type="button" data-filter="${escapeAttribute(key)}">
          <span>${escapeHtml(FILTER_LABELS[key])}</span>
          <span class="filter-count">${escapeHtml(String(count))}</span>
        </button>
      `;
    })
    .join("");

  container.querySelectorAll(".filter-button").forEach((button) => {
    button.addEventListener("click", () => {
      currentFilter = button.dataset.filter;
      syncCurrentSelection();
      renderFilters();
      renderRecipeList();
      renderCard();
    });
  });
}

function getCurrentRecipeIds() {
  return compareData.filters[currentFilter] || [];
}

function syncCurrentSelection() {
  const recipeIds = getCurrentRecipeIds();
  if (!recipeIds.length) {
    currentRecipeId = null;
    return;
  }
  if (!currentRecipeId || !recipeIds.includes(currentRecipeId)) {
    currentRecipeId = recipeIds[0];
  }
}

function renderRecipeList() {
  const recipeIds = getCurrentRecipeIds();
  const container = document.getElementById("recipe-list");
  document.getElementById("recipe-counter").textContent = `${recipeIds.length} recipes`;

  if (!recipeIds.length) {
    container.innerHTML = `<p class="empty-state">No recipes in this filter.</p>`;
    return;
  }

  container.innerHTML = recipeIds
    .map((recipeId) => {
      const recipe = compareData.recipes_by_id[recipeId];
      const active = recipeId === currentRecipeId ? "active" : "";
      const chips = [
        recipe.has_overlay ? "overlay" : "non-overlay",
        recipe.protected_baseline ? "protected" : null,
        recipe.text_changed ? "text" : "authority",
      ]
        .filter(Boolean)
        .map((chip) => `<span class="recipe-chip">${escapeHtml(chip)}</span>`)
        .join("");

      return `
        <button class="recipe-link ${active}" type="button" data-recipe-id="${escapeAttribute(recipeId)}">
          <span class="recipe-link-id">${escapeHtml(recipeId)}</span>
          <span class="recipe-link-lemma">${escapeHtml(recipe.lemma)}</span>
          <span class="recipe-link-meta">${escapeHtml(recipe.chapter_name)}</span>
          <span class="recipe-link-chips">${chips}</span>
        </button>
      `;
    })
    .join("");

  container.querySelectorAll(".recipe-link").forEach((button) => {
    button.addEventListener("click", () => {
      currentRecipeId = button.dataset.recipeId;
      renderRecipeList();
      renderCard();
    });
  });
}

function renderCard() {
  const compareCard = document.getElementById("compare-card");
  if (!currentRecipeId) {
    compareCard.innerHTML = `<p class="empty-state">No recipe selected.</p>`;
    return;
  }

  const recipe = compareData.recipes_by_id[currentRecipeId];
  compareCard.innerHTML = `
    <section class="compare-header">
      <div>
        <div class="eyebrow-row">
          <span class="recipe-id">${escapeHtml(recipe.recipe_id)}</span>
          <span class="meta-chip">${escapeHtml(recipe.chapter)}.${escapeHtml(recipe.section)}</span>
          <span class="meta-chip">${escapeHtml(recipe.citation.start || "?")}-${escapeHtml(recipe.citation.end || "?")}</span>
        </div>
        <h2>${escapeHtml(recipe.lemma)}</h2>
        <p class="card-subtitle">${escapeHtml(recipe.chapter_name)}</p>
        <div class="status-row">
          <span class="status-pill ${recipe.protected_baseline ? "status-protected" : ""}">
            Protected baseline: ${escapeHtml(recipe.protected_baseline ? "yes" : "no")}
          </span>
          <span class="status-pill ${recipe.has_overlay ? "status-overlay" : ""}">
            Overlay: ${escapeHtml(recipe.has_overlay ? `${recipe.overlay.emendation_count} emendation(s)` : "none")}
          </span>
          <span class="status-pill">
            Display text: ${escapeHtml(recipe.display_text_source)}
          </span>
        </div>
        <div class="section-chip-row">
          ${recipe.changed_sections.length
            ? recipe.changed_sections.map((section) => `<span class="section-chip">${escapeHtml(section)}</span>`).join("")
            : '<span class="section-chip">text only</span>'}
        </div>
      </div>
      <button class="copy-button" type="button" id="copy-json-diff">Copy JSON Diff</button>
    </section>

    ${renderTextPanel(recipe)}
    ${renderOverlayPanel(recipe)}
    ${renderAuthorityPanel(recipe)}
  `;

  document.getElementById("copy-json-diff").addEventListener("click", async () => {
    const button = document.getElementById("copy-json-diff");
    try {
      await navigator.clipboard.writeText(JSON.stringify(recipe.copy_payload, null, 2));
      const original = button.textContent;
      button.textContent = "Copied";
      window.setTimeout(() => {
        button.textContent = original;
      }, 1400);
    } catch (error) {
      button.textContent = "Copy failed";
      window.setTimeout(() => {
        button.textContent = "Copy JSON Diff";
      }, 1400);
    }
  });
}

function renderTextPanel(recipe) {
  const unchangedMessage = recipe.text_changed
    ? ""
    : `<p class="panel-note">Running text is unchanged between baseline and emended display versions for this recipe.</p>`;

  return `
    <section class="panel">
      <div class="panel-header">
        <h3>Running Text</h3>
        <p class="panel-copy">Baseline experiment on the left, emended experiment on the right.</p>
      </div>
      ${unchangedMessage}
      <div class="two-up">
        <section class="pane">
          <div class="pane-title">Baseline</div>
          <div class="text-diff">${renderDiffChunks(recipe.text.old_chunks, "old")}</div>
        </section>
        <section class="pane">
          <div class="pane-title">Emended</div>
          <div class="text-diff">${renderDiffChunks(recipe.text.new_chunks, "new")}</div>
        </section>
      </div>
    </section>
  `;
}

function renderDiffChunks(chunks, side) {
  return chunks
    .map((chunk) => {
      let className = "diff-equal";
      if (chunk.kind === "replace") {
        className = "diff-change";
      } else if (side === "old" && chunk.kind === "delete") {
        className = "diff-remove";
      } else if (side === "new" && chunk.kind === "insert") {
        className = "diff-add";
      }
      return `<span class="${className}">${escapeHtml(chunk.text)}</span>`;
    })
    .join("");
}

function renderOverlayPanel(recipe) {
  if (!recipe.overlay.emendation_count) {
    return `
      <section class="panel">
        <div class="panel-header">
          <h3>Emendations</h3>
        </div>
        <p class="empty-state">No overlay emendations recorded for this recipe.</p>
      </section>
    `;
  }

  return `
    <section class="panel">
      <div class="panel-header">
        <h3>Emendations</h3>
      </div>
      <div class="emendation-list">
        ${recipe.overlay.emendations.map(renderEmendation).join("")}
      </div>
    </section>
  `;
}

function renderEmendation(item) {
  return `
    <article class="emendation-card">
      <div class="emendation-meta">${escapeHtml(item.locus || "")} · ${escapeHtml(item.operation || "")}</div>
      <div class="emendation-author">${escapeHtml(item.proposal_author || "")}</div>
      ${item.olivieri_text ? `<div><strong>Olivieri:</strong> ${escapeHtml(item.olivieri_text)}</div>` : ""}
      ${item.adopted_text ? `<div><strong>Adopted:</strong> ${escapeHtml(item.adopted_text)}</div>` : ""}
      ${item.note ? `<div><strong>Note:</strong> ${escapeHtml(item.note)}</div>` : ""}
    </article>
  `;
}

function renderAuthorityPanel(recipe) {
  const sections = recipe.changed_sections.map((section) => {
    const diff = recipe.authority.sections[section];
    return `
      <section class="authority-section">
        <div class="authority-section-header">
          <h4>${escapeHtml(section)}</h4>
        </div>
        ${renderAuthoritySection(section, diff)}
      </section>
    `;
  });

  return `
    <section class="panel">
      <div class="panel-header">
        <h3>Authority Diff</h3>
        <p class="panel-copy">Canonical authority on the left, review-only emended authority on the right.</p>
      </div>
      ${sections.length ? sections.join("") : '<p class="empty-state">No authority differences recorded for this recipe.</p>'}
    </section>
  `;
}

function renderAuthoritySection(section, diff) {
  if (diff.kind === "object") {
    return renderObjectDiff(diff);
  }
  if (diff.kind === "list") {
    return renderListDiff(diff);
  }
  return renderScalarDiff(diff);
}

function renderObjectDiff(diff) {
  const rows = diff.field_diffs
    .map(
      (fieldDiff) => `
        <tr>
          <th>${escapeHtml(fieldDiff.field)}</th>
          <td>${renderValue(fieldDiff.old)}</td>
          <td>${renderValue(fieldDiff.new)}</td>
        </tr>
      `
    )
    .join("");

  return `
    <div class="object-diff">
      <table class="diff-table">
        <thead>
          <tr>
            <th>Field</th>
            <th>Canonical</th>
            <th>Review-only</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function renderListDiff(diff) {
  const added = diff.added.length ? renderTagList(diff.added, "tag-add") : '<span class="tag-empty">None</span>';
  const removed = diff.removed.length ? renderTagList(diff.removed, "tag-remove") : '<span class="tag-empty">None</span>';
  return `
    <div class="two-up authority-two-up">
      <section class="pane">
        <div class="pane-title">Canonical (${escapeHtml(String(diff.old_count))})</div>
        ${renderStringList(diff.old_items)}
      </section>
      <section class="pane">
        <div class="pane-title">Review-only (${escapeHtml(String(diff.new_count))})</div>
        ${renderStringList(diff.new_items)}
      </section>
    </div>
    <div class="delta-row">
      <div>
        <div class="delta-title">Removed</div>
        ${removed}
      </div>
      <div>
        <div class="delta-title">Added</div>
        ${added}
      </div>
    </div>
  `;
}

function renderScalarDiff(diff) {
  return `
    <div class="two-up authority-two-up">
      <section class="pane">
        <div class="pane-title">Canonical</div>
        <div class="scalar-box">${renderValue(diff.old)}</div>
      </section>
      <section class="pane">
        <div class="pane-title">Review-only</div>
        <div class="scalar-box">${renderValue(diff.new)}</div>
      </section>
    </div>
  `;
}

function renderValue(value) {
  if (value === null || value === undefined) {
    return '<span class="value-empty">None</span>';
  }
  if (Array.isArray(value)) {
    return renderStringList(value);
  }
  if (typeof value === "object") {
    return `<pre class="json-block">${escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
  }
  return `<div class="value-text">${escapeHtml(String(value))}</div>`;
}

function renderStringList(items) {
  if (!items.length) {
    return '<p class="empty-state">None</p>';
  }
  return `
    <ul class="string-list">
      ${items.map((item) => `<li>${escapeHtml(String(item))}</li>`).join("")}
    </ul>
  `;
}

function renderTagList(items, className) {
  return `
    <div class="tag-list">
      ${items.map((item) => `<span class="tag ${className}">${escapeHtml(String(item))}</span>`).join("")}
    </div>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("'", "&#39;");
}

init();
