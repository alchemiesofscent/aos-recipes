let compareData = null;
let currentFilter = null;
let currentRecipeId = null;

const FILTER_LABELS = {
  pending: "Pending",
  accepted: "Accepted",
  rejected: "Rejected",
  changed: "Changed",
  unchanged: "Unchanged",
};

async function init() {
  try {
    if (window.AETIUS_BOOK1_EMENDED_WORKING_COMPARE_DATA) {
      compareData = window.AETIUS_BOOK1_EMENDED_WORKING_COMPARE_DATA;
    } else {
      const response = await fetch("data/aetius_book1_emended_working_compare.json");
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      compareData = await response.json();
    }
  } catch (error) {
    document.getElementById("compare-card").innerHTML = `
      <h2>Patch comparison data unavailable</h2>
      <p class="status">Build the local patch-review dataset and serve this folder over HTTP. Example: <code>python3 scripts/recipes/build_aetius_book1_emended_working_compare.py</code></p>
      <p class="status">${escapeHtml(String(error))}</p>
    `;
    return;
  }

  document.getElementById("chapter-name").textContent =
    "Canonical Book 1 authority on the left, working-copy patch flow on the right";

  renderSummary();
  renderFilters();
  syncCurrentSelection();
  renderRecipeList();
  renderCard();
}

function renderSummary() {
  const summary = compareData.summary;
  const container = document.getElementById("summary");
  const items = [
    ["Patch Recipes", summary.total_patch_recipes],
    ["Pending", summary.pending],
    ["Accepted", summary.accepted],
    ["Rejected", summary.rejected],
    ["Changed", summary.changed],
    ["Unchanged", summary.unchanged],
  ];
  container.innerHTML = items.map(([label, value]) => `
    <div class="summary-item">
      <div class="summary-value">${escapeHtml(String(value))}</div>
      <div class="summary-label">${escapeHtml(label)}</div>
    </div>
  `).join("");
}

function renderFilters() {
  const container = document.getElementById("filters");
  const keys = Object.keys(compareData.filters);
  if (!currentFilter || !keys.includes(currentFilter)) {
    currentFilter = compareData.default_filter;
  }
  container.innerHTML = keys.map((key) => `
    <button class="filter-button ${key === currentFilter ? "active" : ""}" type="button" data-filter="${escapeAttribute(key)}">
      <span>${escapeHtml(FILTER_LABELS[key])}</span>
      <span class="filter-count">${escapeHtml(String(compareData.filters[key].length))}</span>
    </button>
  `).join("");
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
  currentRecipeId = recipeIds.includes(currentRecipeId) ? currentRecipeId : (recipeIds[0] || null);
}

function renderRecipeList() {
  const recipeIds = getCurrentRecipeIds();
  document.getElementById("recipe-counter").textContent = `${recipeIds.length} recipes`;
  const container = document.getElementById("recipe-list");
  if (!recipeIds.length) {
    container.innerHTML = `<p class="empty-state">No recipes in this filter.</p>`;
    return;
  }
  container.innerHTML = recipeIds.map((recipeId) => {
    const recipe = compareData.recipes_by_id[recipeId];
    const active = recipeId === currentRecipeId ? "active" : "";
    const chips = [
      recipe.review_status,
      recipe.change_scope,
      recipe.changed ? "changed" : "unchanged",
    ].map((chip) => `<span class="recipe-chip">${escapeHtml(chip)}</span>`).join("");
    return `
      <button class="recipe-link ${active}" type="button" data-recipe-id="${escapeAttribute(recipeId)}">
        <span class="recipe-link-id">${escapeHtml(recipeId)}</span>
        <span class="recipe-link-lemma">${escapeHtml(recipe.lemma)}</span>
        <span class="recipe-link-meta">${escapeHtml(recipe.chapter_name)}</span>
        <span class="recipe-link-chips">${chips}</span>
      </button>
    `;
  }).join("");
  container.querySelectorAll(".recipe-link").forEach((button) => {
    button.addEventListener("click", () => {
      currentRecipeId = button.dataset.recipeId;
      renderRecipeList();
      renderCard();
    });
  });
}

function renderCard() {
  const container = document.getElementById("compare-card");
  if (!currentRecipeId) {
    container.innerHTML = `<p class="empty-state">No recipe selected.</p>`;
    return;
  }
  const recipe = compareData.recipes_by_id[currentRecipeId];
  container.innerHTML = `
    <section class="compare-header">
      <div>
        <div class="eyebrow-row">
          <span class="recipe-id">${escapeHtml(recipe.recipe_id)}</span>
          <span class="meta-chip">${escapeHtml(recipe.chapter)}.${escapeHtml(recipe.section)}</span>
        </div>
        <h2>${escapeHtml(recipe.lemma)}</h2>
        <p class="card-subtitle">${escapeHtml(recipe.chapter_name)}</p>
        <div class="status-row">
          <span class="status-pill status-${escapeAttribute(recipe.review_status)}">Review: ${escapeHtml(recipe.review_status)}</span>
          <span class="status-pill">Scope: ${escapeHtml(recipe.change_scope)}</span>
          <span class="status-pill">Changed sections: ${escapeHtml(recipe.changed_sections.length ? recipe.changed_sections.join(", ") : "none")}</span>
        </div>
      </div>
      <button class="copy-button" type="button" id="copy-json-diff">Copy Patch JSON</button>
    </section>

    ${renderPatchPanel(recipe)}
    ${renderAuthorityPanel(recipe)}
  `;

  document.getElementById("copy-json-diff").addEventListener("click", async () => {
    const button = document.getElementById("copy-json-diff");
    try {
      await navigator.clipboard.writeText(JSON.stringify(recipe.copy_payload, null, 2));
      const original = button.textContent;
      button.textContent = "Copied";
      window.setTimeout(() => { button.textContent = original; }, 1200);
    } catch (_error) {
      button.textContent = "Copy failed";
      window.setTimeout(() => { button.textContent = "Copy Patch JSON"; }, 1200);
    }
  });
}

function renderPatchPanel(recipe) {
  return `
    <section class="panel">
      <div class="panel-header">
        <h3>Patch Review</h3>
        <p class="panel-copy">This is the explicit patch record from the working-copy flow.</p>
      </div>
      <div class="status-row">
        ${recipe.emendation_refs.map((ref) => `<span class="tag">${escapeHtml(ref.locus || ref.start_citation || "?")} · ${escapeHtml(ref.operation || "op")}</span>`).join("") || '<span class="tag-empty">No emendation refs</span>'}
      </div>
      <p class="panel-note">${escapeHtml(recipe.reason || "No reason entered yet.")}</p>
      <div class="field-list">
        ${recipe.fields.length ? recipe.fields.map(renderFieldItem).join("") : '<p class="empty-state">No field operations recorded yet.</p>'}
      </div>
    </section>
  `;
}

function renderFieldItem(field) {
  return `
    <article class="field-item">
      <div class="field-op">${escapeHtml(field.op || "op")}</div>
      <div class="mono">${escapeHtml(field.path || "(no path)")}</div>
      ${field.match ? `<div class="panel-note">match: <code>${escapeHtml(JSON.stringify(field.match))}</code></div>` : ""}
      ${field.after_match ? `<div class="panel-note">after_match: <code>${escapeHtml(JSON.stringify(field.after_match))}</code></div>` : ""}
      ${Object.prototype.hasOwnProperty.call(field, "old_value") ? `<div class="panel-note">old_value: <code>${escapeHtml(JSON.stringify(field.old_value))}</code></div>` : ""}
      ${Object.prototype.hasOwnProperty.call(field, "new_value") ? `<div class="panel-note">new_value: <code>${escapeHtml(JSON.stringify(field.new_value))}</code></div>` : ""}
      ${Object.prototype.hasOwnProperty.call(field, "value") ? `<div class="panel-note">value: <code>${escapeHtml(JSON.stringify(field.value))}</code></div>` : ""}
    </article>
  `;
}

function renderAuthorityPanel(recipe) {
  if (!recipe.changed_sections.length) {
    return `
      <section class="panel">
        <div class="panel-header">
          <h3>Authority Diff</h3>
          <p class="panel-copy">Canonical and working-copy authority are still identical for this recipe.</p>
        </div>
      </section>
    `;
  }
  const sections = recipe.changed_sections.map((section) => renderAuthoritySection(section, recipe.authority.sections[section])).join("");
  return `
    <section class="panel">
      <div class="panel-header">
        <h3>Authority Diff</h3>
        <p class="panel-copy">Canonical authority on the left, working-copy authority on the right.</p>
      </div>
      ${sections}
    </section>
  `;
}

function renderAuthoritySection(section, diff) {
  return `
    <section class="delta-block">
      <div class="delta-row">
        <h4 class="delta-title">${escapeHtml(section)}</h4>
      </div>
      ${renderDiffContent(diff)}
    </section>
  `;
}

function renderDiffContent(diff) {
  if (diff.kind === "object") {
    return `
      <div class="split-grid">
        <section class="pane">
          <div class="mini-title">Canonical</div>
          <pre class="mono">${escapeHtml(JSON.stringify(diff.old_summary, null, 2))}</pre>
        </section>
        <section class="pane">
          <div class="mini-title">Working Copy</div>
          <pre class="mono">${escapeHtml(JSON.stringify(diff.new_summary, null, 2))}</pre>
        </section>
      </div>
    `;
  }
  if (diff.kind === "list") {
    return `
      <div class="split-grid">
        <section class="pane">
          <div class="mini-title">Canonical</div>
          <pre class="mono">${escapeHtml(JSON.stringify(diff.old_items, null, 2))}</pre>
        </section>
        <section class="pane">
          <div class="mini-title">Working Copy</div>
          <pre class="mono">${escapeHtml(JSON.stringify(diff.new_items, null, 2))}</pre>
        </section>
      </div>
    `;
  }
  return `
    <div class="split-grid">
      <section class="pane">
        <div class="mini-title">Canonical</div>
        <pre class="mono">${escapeHtml(JSON.stringify(diff.old, null, 2))}</pre>
      </section>
      <section class="pane">
        <div class="mini-title">Working Copy</div>
        <pre class="mono">${escapeHtml(JSON.stringify(diff.new, null, 2))}</pre>
      </section>
    </div>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

init();
