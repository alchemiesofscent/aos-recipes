const state = {
  recipes: [],
  sources: [],
  selected: null,
  filtered: [],
};

const sourceFilter = document.querySelector("#sourceFilter");
const searchInput = document.querySelector("#searchInput");
const searchClear = document.querySelector("#searchClear");
const recipeList = document.querySelector("#recipeList");
const detail = document.querySelector("#detail");
const counts = document.querySelector("#counts");
const themeToggle = document.querySelector("#themeToggle");

const THEME_CYCLE = ["auto", "light", "dark"];

function labelFor(recipe) {
  return recipe.lemma || recipe.chapter_name || recipe.recipe_id;
}

function sourceName(key) {
  const source = state.sources.find((item) => item.dataset_key === key);
  return source ? source.display_name : key;
}

function escapeHtml(value) {
  if (value === null || value === undefined) return "";
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function filteredRecipes() {
  const source = sourceFilter.value;
  const query = searchInput.value.trim().toLocaleLowerCase();
  return state.recipes.filter((recipe) => {
    const sourceMatch = source === "all" || recipe.dataset_key === source;
    const haystack = [recipe.recipe_id, recipe.lemma, recipe.chapter_name, recipe.text]
      .filter(Boolean)
      .join(" ")
      .toLocaleLowerCase();
    return sourceMatch && (!query || haystack.includes(query));
  });
}

function selectRecipe(recipe, { updateHash = true, scrollIntoView = false } = {}) {
  state.selected = recipe;
  if (updateHash && recipe) {
    const next = "#" + recipe.recipe_id;
    if (location.hash !== next) {
      history.replaceState(null, "", next);
    }
  }
  renderList();
  renderDetail();
  if (scrollIntoView && recipe) {
    const active = recipeList.querySelector(".recipe-button.active");
    if (active) active.scrollIntoView({ block: "nearest" });
  }
}

function renderList() {
  state.filtered = filteredRecipes();
  recipeList.innerHTML = "";
  for (const recipe of state.filtered) {
    const isActive = state.selected?.recipe_id === recipe.recipe_id;
    const button = document.createElement("button");
    button.className = "recipe-button" + (isActive ? " active" : "");
    button.setAttribute("role", "option");
    button.setAttribute("aria-selected", isActive ? "true" : "false");
    button.tabIndex = isActive ? 0 : -1;
    button.dataset.recipeId = recipe.recipe_id;
    button.innerHTML = `<strong>${escapeHtml(labelFor(recipe))}</strong><span>${escapeHtml(sourceName(recipe.dataset_key))} · ${escapeHtml(recipe.recipe_id)}</span>`;
    button.addEventListener("click", () => {
      selectRecipe(recipe);
    });
    recipeList.append(button);
  }
  counts.textContent = `${state.filtered.length} shown · ${state.recipes.length} recipes`;
  if (searchClear) searchClear.hidden = searchInput.value.length === 0;
}

function chipItems(items) {
  return (items || [])
    .map((item) => item.normalized_label || item.base_label || item.surface_form || item.source_span)
    .filter(Boolean)
    .slice(0, 80)
    .map((text) => `<span class="chip">${escapeHtml(text)}</span>`)
    .join("");
}

const DESCRIPTOR_FAMILY_LABELS = {
  same_as: "the same",
  more_than: "more than",
  less_than: "less than",
  as_much_as: "as much as needed",
  a_little: "a little",
  many: "many",
  "fraction:half": "½",
  "fraction:third": "⅓",
  "fraction:fourth": "¼",
  part: "part(s)",
  "multiple:two": "double",
  "multiple:three": "triple",
  relative_to: "relative to (preceding)",
  quantity_unspecified: "(unspecified)",
  unspecified: "—",
};

function unitDisplayName(unit) {
  if (!unit) return "";
  if (unit === "descriptor") return "";
  return unit;
}

function descriptorFamilyLabel(family) {
  if (!family) return "";
  return DESCRIPTOR_FAMILY_LABELS[family] || family;
}

function entityLabel(item) {
  return item.normalized_label || item.base_label || item.surface_form || item.source_span || "";
}

function formatQuantity(q) {
  if (!q) return { qty: "", unit: "", source: "" };
  const isDescriptor = q.normalized_unit === "descriptor";
  const num = q.normalized_number;
  let qty = "";
  if (num !== null && num !== undefined && num !== "") qty = String(num);
  if (isDescriptor) qty = qty || "";
  if (q.certainty === "uncertain" && qty) {
    qty = `${qty}<sup class="uncertainty-mark" title="Uncertain reading">?</sup>`;
  }
  const unit = isDescriptor ? descriptorFamilyLabel(q.descriptor_family) : unitDisplayName(q.normalized_unit);
  const source = q.source_span || "";
  return { qty, unit, source };
}

function formattedQuantityInline(q) {
  const f = formatQuantity(q);
  const left = [f.qty, f.unit].filter(Boolean).join(" ");
  if (f.source && f.source !== left) return `${left} (${f.source})`.trim();
  return left;
}

function quantityGroups(qs) {
  const groups = [];
  const byId = new Map();
  qs.forEach((q, index) => {
    const id = q.measure_group_id || `__quantity_${index}`;
    if (!byId.has(id)) {
      const group = { id, items: [] };
      byId.set(id, group);
      groups.push(group);
    }
    byId.get(id).items.push(q);
  });
  return groups;
}

function groupRelation(group) {
  const relations = group.items.map((q) => q.measure_relation || "standalone");
  return relations.find((relation) => relation !== "standalone") || relations[0] || "standalone";
}

function quantityMainText(q) {
  const f = formatQuantity(q);
  return [f.qty, f.unit].filter(Boolean).join(" ") || f.source || "";
}

function formatQuantityGroup(group) {
  const relation = groupRelation(group);
  const items = group.items;
  const primary = items[0];
  const f = primary ? formatQuantity(primary) : { qty: "", unit: "", source: "" };
  const variants = [];

  if (relation === "compound_component") {
    return {
      qty: items.map(quantityMainText).filter(Boolean).join(" "),
      unit: "",
      source: items.map((q) => q.source_span || "").filter(Boolean).join(" + "),
      variants,
    };
  }

  if (relation === "equivalent_notation") {
    return {
      qty: f.qty,
      unit: f.unit,
      source: items.map((q) => q.source_span || "").filter(Boolean).join(" = ") || f.source,
      variants,
    };
  }

  if (relation === "variant_quantity") {
    variants.push(...items.slice(1).map(formattedQuantityInline).filter(Boolean));
  }

  return {
    qty: f.qty,
    unit: f.unit,
    source: f.source,
    variants,
  };
}

function formatQuantityCells(qs) {
  const groups = quantityGroups(qs).map(formatQuantityGroup);
  if (!groups.length) return { qty: "", unit: "", source: "", variants: [] };
  const variants = groups.flatMap((group) => group.variants);
  if (groups.length === 1) {
    return { ...groups[0], variants };
  }
  return {
    qty: groups.map((group) => [group.qty, group.unit].filter(Boolean).join(" ")).filter(Boolean).join(" · "),
    unit: "",
    source: groups.map((group) => group.source).filter(Boolean).join(" · "),
    variants,
  };
}

function renderEntityTable(items, { label = "Ingredient", showDuration = false } = {}) {
  if (!items || !items.length) return "";
  const headerCols = [label, "Qty", "Unit", "Source"];
  if (showDuration) headerCols.push("Duration");
  const headRow = headerCols.map((c) => `<th>${escapeHtml(c)}</th>`).join("");

  const rows = items.map((item) => {
    const name = entityLabel(item);
    const qs = Array.isArray(item.quantities) ? item.quantities : [];
    const f = formatQuantityCells(qs);
    let variantHtml = "";
    if (f.variants.length) {
      variantHtml = `<small class="qty-variant">alt: ${escapeHtml(f.variants.join(" · "))}</small>`;
    }
    const cells = [
      `<td class="col-name">${escapeHtml(name)}</td>`,
      `<td class="col-qty">${f.qty}</td>`,
      `<td class="col-unit">${escapeHtml(f.unit)}</td>`,
      `<td class="col-source">${escapeHtml(f.source)}${variantHtml}</td>`,
    ];
    if (showDuration) {
      const durations = Array.isArray(item.durations) ? item.durations : [];
      const durText = durations.map(formattedQuantityInline).filter(Boolean).join(" · ");
      cells.push(`<td class="col-duration">${escapeHtml(durText)}</td>`);
    }
    return `<tr>${cells.join("")}</tr>`;
  }).join("");

  return `<table class="entity-table"><thead><tr>${headRow}</tr></thead><tbody>${rows}</tbody></table>`;
}

function entitySection(title, html) {
  return `<div class="section${html ? "" : " empty"}"><h3>${escapeHtml(title)}</h3>${html}</div>`;
}

function chipSection(title, html) {
  return `<div class="section${html ? "" : " empty"}"><h3>${escapeHtml(title)}</h3><div class="chips">${html}</div></div>`;
}

function citationPagesText(citation) {
  if (!citation) return "";
  const pages = Array.isArray(citation.pages) ? citation.pages.filter(Boolean) : [];
  if (pages.length === 0) return "";
  if (pages.length === 1) return `p. ${pages[0]}`;
  return `pp. ${pages[0]}–${pages[pages.length - 1]}`;
}

function locatorText(recipe) {
  const parts = [];
  if (recipe.book) parts.push(`Book ${recipe.book}`);
  if (recipe.chapter) parts.push(`ch. ${recipe.chapter}`);
  if (recipe.section && recipe.section !== recipe.chapter) parts.push(`§${recipe.section}`);
  return parts.join(", ");
}

function metaRow(label, valueHtml) {
  if (!valueHtml) return "";
  return `<dt>${escapeHtml(label)}</dt><dd>${valueHtml}</dd>`;
}

function renderDetail() {
  const recipe = state.selected;
  if (!recipe) {
    detail.innerHTML = "";
    return;
  }
  const authorWork = [recipe.author, recipe.work].filter(Boolean).join(" — ");
  const locator = locatorText(recipe);
  const pages = citationPagesText(recipe.citation);
  const ingredientsHtml = renderEntityTable(recipe.ingredients, { label: "Ingredient" });
  const materialsHtml = renderEntityTable(recipe.materials, { label: "Material" });
  const processesHtml = renderEntityTable(recipe.processes, { label: "Process", showDuration: true });
  const placesPeopleChips = chipItems([...(recipe.places || []), ...(recipe.people || [])]);
  const usesChips = chipItems(recipe.uses);
  const sectionsHtml = [
    entitySection("Ingredients", ingredientsHtml),
    entitySection("Materials", materialsHtml),
    entitySection("Processes", processesHtml),
    chipSection("Places and people", placesPeopleChips),
    chipSection("Uses", usesChips),
  ].join("");

  detail.innerHTML = `
    <header class="detail-header">
      <h2>${escapeHtml(labelFor(recipe))}</h2>
      <dl class="detail-meta">
        ${metaRow("Source", escapeHtml(sourceName(recipe.dataset_key)))}
        ${metaRow("Author", escapeHtml(authorWork))}
        ${metaRow("Locator", escapeHtml(locator))}
        ${metaRow("Pages", escapeHtml(pages))}
        ${metaRow("Recipe ID", escapeHtml(recipe.recipe_id))}
        ${metaRow("URN", `<code>${escapeHtml(recipe.recipe_urn || "")}</code>`)}
      </dl>
    </header>
    <div class="detail-inner">
      <div class="greek">${escapeHtml(recipe.text || "")}</div>
      ${sectionsHtml}
    </div>
  `;
  detail.scrollTop = 0;
}

function moveSelection(direction) {
  if (!state.filtered.length) return;
  const currentIndex = state.selected
    ? state.filtered.findIndex((r) => r.recipe_id === state.selected.recipe_id)
    : -1;
  let nextIndex;
  if (currentIndex === -1) {
    nextIndex = direction > 0 ? 0 : state.filtered.length - 1;
  } else {
    nextIndex = currentIndex + direction;
    if (nextIndex < 0) nextIndex = 0;
    if (nextIndex >= state.filtered.length) nextIndex = state.filtered.length - 1;
  }
  selectRecipe(state.filtered[nextIndex], { scrollIntoView: true });
}

function isTypingTarget(el) {
  if (!el) return false;
  const tag = el.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
  if (el.isContentEditable) return true;
  return false;
}

function attachKeyboardNav() {
  document.addEventListener("keydown", (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;

    if (event.key === "/" && !isTypingTarget(event.target)) {
      event.preventDefault();
      searchInput.focus();
      searchInput.select();
      return;
    }

    if (event.key === "Escape" && event.target === searchInput) {
      if (searchInput.value.length > 0) {
        searchInput.value = "";
        onSearchChange();
      } else {
        searchInput.blur();
      }
      return;
    }

    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      if (event.target === sourceFilter) return;
      event.preventDefault();
      moveSelection(event.key === "ArrowDown" ? 1 : -1);
    }
  });
}

let searchDebounce;
function onSearchChange() {
  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(() => {
    state.selected = null;
    renderList();
    if (!state.selected && state.filtered.length) {
      selectRecipe(state.filtered[0]);
    } else if (!state.filtered.length) {
      renderDetail();
    }
  }, 120);
  if (searchClear) searchClear.hidden = searchInput.value.length === 0;
}

function applyTheme(theme) {
  const root = document.documentElement;
  if (theme === "auto") {
    root.removeAttribute("data-theme");
  } else {
    root.setAttribute("data-theme", theme);
  }
  if (themeToggle) {
    themeToggle.textContent = `Theme: ${theme}`;
    themeToggle.title = `Theme: ${theme} (click to cycle)`;
  }
}

function initTheme() {
  const saved = localStorage.getItem("aos.theme");
  const theme = THEME_CYCLE.includes(saved) ? saved : "auto";
  applyTheme(theme);
  if (!themeToggle) return;
  themeToggle.addEventListener("click", () => {
    const current = localStorage.getItem("aos.theme") || "auto";
    const idx = THEME_CYCLE.indexOf(current);
    const next = THEME_CYCLE[(idx + 1) % THEME_CYCLE.length];
    localStorage.setItem("aos.theme", next);
    applyTheme(next);
  });
}

function recipeFromHash() {
  const id = location.hash.slice(1);
  if (!id) return null;
  return state.recipes.find((r) => r.recipe_id === id) || null;
}

async function fetchDataJson(name) {
  // Works for both layouts:
  //   - GitHub Pages deploy (data/ sibling of index.html): "data/<name>"
  //   - Local repo-root serving (open /site/, data is one level up): "../data/<name>"
  const candidates = ["data/" + name, "../data/" + name];
  let lastError;
  for (const url of candidates) {
    try {
      const response = await fetch(url);
      if (!response.ok) { lastError = new Error(`${url} → ${response.status}`); continue; }
      const text = await response.text();
      try { return JSON.parse(text); } catch (e) { lastError = new Error(`${url} returned non-JSON`); continue; }
    } catch (e) { lastError = e; }
  }
  throw lastError || new Error(`could not load ${name}`);
}

async function init() {
  initTheme();

  const [recipePayload, sourcePayload] = await Promise.all([
    fetchDataJson("recipes.json"),
    fetchDataJson("sources.json"),
  ]);
  state.recipes = recipePayload.recipes;
  state.sources = sourcePayload.sources;

  sourceFilter.innerHTML = `<option value="all">All sources</option>` + state.sources
    .map((source) => `<option value="${escapeHtml(source.dataset_key)}">${escapeHtml(source.display_name)}</option>`)
    .join("");

  sourceFilter.addEventListener("change", () => {
    state.selected = null;
    renderList();
    if (state.filtered.length) {
      selectRecipe(state.filtered[0]);
    } else {
      renderDetail();
    }
  });

  searchInput.addEventListener("input", onSearchChange);

  if (searchClear) {
    searchClear.addEventListener("click", () => {
      searchInput.value = "";
      onSearchChange();
      searchInput.focus();
    });
  }

  window.addEventListener("hashchange", () => {
    const target = recipeFromHash();
    if (target && target.recipe_id !== state.selected?.recipe_id) {
      selectRecipe(target, { updateHash: false, scrollIntoView: true });
    }
  });

  attachKeyboardNav();

  const initial = recipeFromHash();
  if (initial) {
    state.selected = initial;
    renderList();
    renderDetail();
    const active = recipeList.querySelector(".recipe-button.active");
    if (active) active.scrollIntoView({ block: "center" });
  } else {
    renderList();
    if (state.filtered.length) {
      selectRecipe(state.filtered[0]);
    }
  }
}

init().catch((error) => {
  detail.textContent = error.message;
});
