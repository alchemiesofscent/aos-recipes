const state = { recipes: [], sources: [], selected: null };

const sourceFilter = document.querySelector("#sourceFilter");
const searchInput = document.querySelector("#searchInput");
const recipeList = document.querySelector("#recipeList");
const detail = document.querySelector("#detail");
const counts = document.querySelector("#counts");

function labelFor(recipe) {
  return recipe.lemma || recipe.chapter_name || recipe.recipe_id;
}

function sourceName(key) {
  const source = state.sources.find((item) => item.dataset_key === key);
  return source ? source.display_name : key;
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

function renderList() {
  const recipes = filteredRecipes();
  recipeList.innerHTML = "";
  for (const recipe of recipes) {
    const button = document.createElement("button");
    button.className = "recipe-button" + (state.selected?.recipe_id === recipe.recipe_id ? " active" : "");
    button.innerHTML = `<strong>${labelFor(recipe)}</strong><span>${sourceName(recipe.dataset_key)} · ${recipe.recipe_id}</span>`;
    button.addEventListener("click", () => {
      state.selected = recipe;
      renderList();
      renderDetail();
    });
    recipeList.append(button);
  }
  counts.textContent = `${recipes.length} shown · ${state.recipes.length} recipes`;
  if (!state.selected && recipes.length) {
    state.selected = recipes[0];
    renderList();
    renderDetail();
  }
}

function chipItems(items) {
  return (items || [])
    .map((item) => item.normalized_label || item.base_label || item.surface_form || item.source_span)
    .filter(Boolean)
    .slice(0, 80)
    .map((text) => `<span class="chip">${text}</span>`)
    .join("");
}

function renderDetail() {
  const recipe = state.selected;
  if (!recipe) {
    detail.innerHTML = "";
    return;
  }
  detail.innerHTML = `
    <h2>${labelFor(recipe)}</h2>
    <div class="meta">${sourceName(recipe.dataset_key)} · ${recipe.recipe_id} · ${recipe.recipe_urn}</div>
    <div class="greek">${recipe.text || ""}</div>
    <div class="section"><h3>Ingredients</h3><div class="chips">${chipItems(recipe.ingredients)}</div></div>
    <div class="section"><h3>Processes</h3><div class="chips">${chipItems(recipe.processes)}</div></div>
    <div class="section"><h3>Places And People</h3><div class="chips">${chipItems([...(recipe.places || []), ...(recipe.people || [])])}</div></div>
  `;
}

async function init() {
  const [recipePayload, sourcePayload] = await Promise.all([
    fetch("../data/recipes.json").then((response) => response.json()),
    fetch("../data/sources.json").then((response) => response.json()),
  ]);
  state.recipes = recipePayload.recipes;
  state.sources = sourcePayload.sources;
  sourceFilter.innerHTML = `<option value="all">All sources</option>` + state.sources
    .map((source) => `<option value="${source.dataset_key}">${source.display_name}</option>`)
    .join("");
  sourceFilter.addEventListener("change", () => {
    state.selected = null;
    renderList();
  });
  searchInput.addEventListener("input", () => {
    state.selected = null;
    renderList();
  });
  renderList();
}

init().catch((error) => {
  detail.textContent = error.message;
});
