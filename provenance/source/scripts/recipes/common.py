from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DERIVED_DIR = REPO_ROOT / "derived"
RECIPE_ENTITY_DIR = DERIVED_DIR / "recipe_entities"
REPORTS_DIR = REPO_ROOT / "reports"
SCHEMA_DIR = REPO_ROOT / "schema"
RAW_DIR = REPO_ROOT / "tei" / "raw"
STRUCTURED_AUTHORITY_DIR = REPORTS_DIR / "entity_review" / "structured"
WEIGHTS_AND_MEASURES_TSV = REPO_ROOT / "docs" / "weights-and-measures.tsv"
AETIUS_BOOK1_EXPERIMENT_DIR = REPO_ROOT / "experiments" / "aetius-book1-ch99-136-oils"
AETIUS_BOOK1_PRE_EMENDED_BACKUP_DIR = (
    REPO_ROOT / "experiments" / "aetius-book1-ch99-136-oils-pre-emended-backup"
)

AUTHORITY_MODEL = "gpt-5.4"
AUTHORITY_REASONING = "high"
ENTITY_MODEL_VERSION = "1.2"
AUTHORITY_VERSION = "2026-04-13-qty-alt-v1"
PROMPT_VERSION = "qty-alt-pass-v1"
PROMPT_VERSION_BY_DATASET = {
    "aetius_book1_oils": "qty-alt-pass-v2-book1-emended",
}
AUTHORITY_METADATA_KEYS = (
    "entity_model_version",
    "authority_version",
    "prompt_version",
    "build_version",
)

VIEWER_ENTITY_GROUPS = (
    "labels",
    "ingredients",
    "processes",
    "tools",
    "other_preparations_mentioned",
    "people",
    "places",
    "works_mentioned",
    "preparation_names",
)

MEASURE_RELATIONS = {
    "standalone",
    "compound_component",
    "equivalent_notation",
    "variant_quantity",
}


def prompt_version_for_dataset(dataset_key: str | None) -> str:
    if not dataset_key:
        return PROMPT_VERSION
    return PROMPT_VERSION_BY_DATASET.get(dataset_key, PROMPT_VERSION)


DATASETS: list[dict[str, Any]] = [
    {
        "key": "dioscorides_book1_perfumes_resins",
        "path": REPO_ROOT
        / "experiments"
        / "dioscorides-book1-perfumes-resins"
        / "data"
        / "dioscorides_book1_perfumes_resins.json",
        "host_raw_file": "tei/raw/tlg0656.tlg001.1st1K-grc1.xml",
        "work_slug": "diosc.b1.recipes",
        "entries_key": "entries",
        "recipe_kind": "recipe",
    },
    {
        "key": "dioscorides_book2_fats",
        "path": REPO_ROOT
        / "experiments"
        / "dioscorides-book2-fats"
        / "data"
        / "dioscorides_book2_fats.json",
        "host_raw_file": "tei/raw/tlg0656.tlg001.1st1K-grc1.xml",
        "work_slug": "diosc.b2.fats",
        "entries_key": "entries",
        "recipe_kind": "recipe",
    },
    {
        "key": "aetius_book1_oils",
        "path": AETIUS_BOOK1_EXPERIMENT_DIR / "data" / "aetius_book1_ch99_136_oils.json",
        "host_raw_file": "tei/raw/tlg0718001.xml",
        "work_slug": "aetius.b1.oils",
        "entries_key": "entries",
        "recipe_kind": "recipe",
    },
    {
        "key": "aetius_book16_myrepsika",
        "path": REPO_ROOT
        / "experiments"
        / "aetius-book16-ch126-153-myrepsika"
        / "data"
        / "aetius_book16_ch126_153_myrepsika.json",
        "host_raw_file": "tei/raw/tlg0718016.xml",
        "work_slug": "aetius.b16.myrepsika",
        "entries_key": "entries",
        "recipe_kind": "recipe",
    },
    {
        "key": "paul_book7_perfumes",
        "path": REPO_ROOT
        / "experiments"
        / "paul-book7-ch20-perfumes"
        / "data"
        / "paul_book7_ch20_perfumes.json",
        "host_raw_file": "tei/raw/tlg0715001.xml",
        "work_slug": "paul.b7.perfumes",
        "entries_key": "perfumes",
        "recipe_kind": "recipe",
    },
]

RECIPE_RECORD_SPLITS: dict[str, list[dict[str, Any]]] = {
    "aetius-16-146-1": [
        {
            "recipe_id": "aetius-16-146-1",
            "text": (
                "Κόστου λίτρ. δ ἤτοι δ. καὶ ἡμίσ. καρυοφύλλων λίτρ. θ. "
                "φύλλων λίτ. α καὶ ἡμίσ. ναρδοστάχυος τὸ αὐτό. κασάμου γοιδ "
                "ἤτοι οὐγ. ιδ. στύρακος χυματίου λίτρ. στ. ἄσπρου λιτρ. γ. "
                "κρόκου τριχίνου γοι. ἄμβαρος γοβ. μόσχου γοβ."
            ),
            "notes": [
                "First formulation of Book 16, ch. 146, §1; the second formulation is split as aetius-16-146-1-2."
            ],
        },
        {
            "recipe_id": "aetius-16-146-1-2",
            "text": (
                "ὁ ἄρχων δὲ τῆς Ἀνατολῆς σκευάζει οὕτως. κόστου γογ. "
                "ναρδοστάχυος γοα. φύλλων τὸ αὐτό. καρυοφύλλων γογζʹ. "
                "ἤτοι οὐγ. γ καὶ ἡμίσ. κασάμου γοζʹ. ἤτοι οὐγ. ἡμίσ. "
                "ἄσπρου γοβ. στύρακος γοβ. χυματίου πρωτείου γοε. "
                "κρόκου τριχίνου γράμματα β. μόσχου, ἄμβαρος ἀνὰ γράμματα β."
            ),
            "notes": [
                "Second formulation of Book 16, ch. 146, §1, introduced by ὁ ἄρχων δὲ τῆς Ἀνατολῆς σκευάζει οὕτως."
            ],
        },
    ]
}


AUTHORITY_LEDGER_BY_DATASET = {
    "dioscorides_book1_perfumes_resins": "reports/entity_review/pass3_gpt54/dioscorides.md",
    "dioscorides_book2_fats": "reports/entity_review/pass3_gpt54/dioscorides.md",
    "aetius_book1_oils": "reports/entity_review/pass3_gpt54/aetius_book1.md",
    "aetius_book16_myrepsika": "reports/entity_review/pass3_gpt54/aetius_book16.md",
    "paul_book7_perfumes": "reports/entity_review/pass3_gpt54/paul.md",
}


STRUCTURED_AUTHORITY_BY_DATASET = {
    "dioscorides_book1_perfumes_resins": "reports/entity_review/structured/dioscorides.json",
    "dioscorides_book2_fats": "reports/entity_review/structured/dioscorides.json",
    "aetius_book1_oils": "reports/entity_review/structured/aetius_book1.json",
    "aetius_book16_myrepsika": "reports/entity_review/structured/aetius_book16.json",
    "paul_book7_perfumes": "reports/entity_review/structured/paul.json",
}

AETIUS_BOOK1_CANONICAL_AUTHORITY = REPO_ROOT / STRUCTURED_AUTHORITY_BY_DATASET["aetius_book1_oils"]
AETIUS_BOOK1_EMENDED_PATCH_DIR = REPO_ROOT / "data" / "review"
AETIUS_BOOK1_EMENDED_WORKING_AUTHORITY = AETIUS_BOOK1_EMENDED_PATCH_DIR / "aetius_book1_emended_working.json"
AETIUS_BOOK1_EMENDED_PATCHES = AETIUS_BOOK1_EMENDED_PATCH_DIR / "aetius_book1_emended_patches.json"
AETIUS_BOOK1_EMENDATION_OVERLAY = AETIUS_BOOK1_EXPERIMENT_DIR / "data" / "aetius_book1_emendations.json"


LEDGER_FIELD_TO_GROUP = {
    "label": "labels",
    "ingredients": "ingredients",
    "processes": "processes",
    "tools": "tools",
    "other_preparations_mentioned": "other_preparations_mentioned",
    "people": "people",
    "places": "places",
    "works_mentioned": "works_mentioned",
    "preparation_names": "preparation_names",
}


SURFACE_NORMALIZED_RE = re.compile(r"surface `([^`]+)`(?:\s*\|\s*normalized `([^`]+)`)?")
HEADER_RE = re.compile(r"^##\s+(\S+)\s+\|\s+(.+)$")
FIELD_RE = re.compile(r"^- `?([^`:]+)`?:\s*(.*)$")
MILESTONE_RE = re.compile(
    r'<milestone unit="recipe" xml:id="([^"]+)" ana="([^"]+)" corresp="([^"]+)"\s*/>'
)
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
MEASURE_CANONICAL_NAME_OVERRIDES = {
    "oungia": "uncia",
}


def strip_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def greek_ascii_slug(text: str) -> str:
    translit = strip_diacritics(text.lower()).replace("ς", "σ")
    table = str.maketrans(
        {
            "α": "a",
            "β": "b",
            "γ": "g",
            "δ": "d",
            "ε": "e",
            "ζ": "z",
            "η": "e",
            "θ": "th",
            "ι": "i",
            "κ": "k",
            "λ": "l",
            "μ": "m",
            "ν": "n",
            "ξ": "x",
            "ο": "o",
            "π": "p",
            "ρ": "r",
            "σ": "s",
            "τ": "t",
            "υ": "y",
            "φ": "ph",
            "χ": "ch",
            "ψ": "ps",
            "ω": "o",
            " ": "-",
        }
    )
    ascii_text = translit.translate(table)
    ascii_text = re.sub(r"[^a-z0-9-]+", "-", ascii_text)
    ascii_text = re.sub(r"-{2,}", "-", ascii_text).strip("-")
    return ascii_text or "item"


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def normalize_unit_token(text: str | None) -> str:
    if not text:
        return ""
    return normalize_space(strip_diacritics(text).replace("ς", "σ").lower())


@lru_cache(maxsize=1)
def load_weight_measure_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with WEIGHTS_AND_MEASURES_TSV.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for raw_row in reader:
            row = {key: normalize_space(value or "") for key, value in raw_row.items()}
            if row.get("Name"):
                row["canonical_name"] = MEASURE_CANONICAL_NAME_OVERRIDES.get(row["Name"], row["Name"])
                row["measure_key"] = normalize_unit_token(row.get("Measure"))
                row["symbol_key"] = normalize_unit_token(row.get("Symbol"))
                rows.append(row)
    return rows


@lru_cache(maxsize=1)
def normalized_unit_vocabulary() -> frozenset[str]:
    names = {row["canonical_name"] for row in load_weight_measure_rows() if row.get("canonical_name")}
    names.add("count")
    return frozenset(sorted(names))


def normalized_unit_prompt_list() -> str:
    return ", ".join(sorted(normalized_unit_vocabulary()))


def infer_normalized_unit(*, raw_unit: str | None, source_span: str | None) -> str | None:
    raw_original = raw_unit or ""
    span_original = source_span or ""
    raw = normalize_unit_token(raw_unit)
    span = normalize_unit_token(source_span)
    haystacks = tuple(token for token in (raw, span) if token)

    if "ἀριθμ" in span or "αριθμ" in span:
        return "count"
    if not raw and span.isdigit():
        return "count"
    if any("𐆄" in token for token in haystacks) or any(
        token.startswith("ουγ") or token.startswith("γο") for token in haystacks
    ):
        return "uncia"
    if any("𐅻" in token for token in haystacks) or any(token.startswith("δραχμ") for token in haystacks):
        return "drachme"
    if any("𐆈" in token for token in haystacks) or any(token.startswith("γρ") or "γραμμα" in token for token in haystacks):
        return "gramma"
    if any(token.startswith("ουγγ") or token.startswith("ουγχ") for token in haystacks):
        return "uncia"
    if "ξ̸" in raw_original or "ξ̸" in span_original:
        return "xestes"
    if any("𐆅" in token for token in haystacks) or any(
        "ξ̸" in token or "ξεστ" in token or token.startswith("ξστ") or token.startswith("ξστα") or token.startswith("ξε")
        for token in haystacks
    ):
        return "xestes"
    if any("𐆃" in token for token in haystacks) or any(
        token.startswith("λιτ") or token.startswith("λι")
        for token in (raw,)
        if token
    ):
        return "litra"
    if any("𐆁" in token for token in haystacks) or any(token.startswith("μετρητ") for token in haystacks):
        return "metretes"
    if raw == "χ" or any(token.startswith("χου") or token.startswith("χοε") for token in haystacks):
        return "chous"
    for row in load_weight_measure_rows():
        canonical = row["canonical_name"]
        symbol_key = row["symbol_key"]
        measure_key = row["measure_key"]
        if symbol_key and any(symbol_key in token for token in haystacks):
            return canonical
        if measure_key:
            prefix = measure_key[:4]
            if prefix and any(token.startswith(prefix) for token in haystacks):
                return canonical
    return None


def canonicalize_normalized_unit(
    normalized_unit: str | None,
    *,
    raw_unit: str | None,
    source_span: str | None,
) -> str | None:
    inferred_from_source = infer_normalized_unit(raw_unit=raw_unit, source_span=source_span)
    if normalized_unit:
        clean = normalize_space(normalized_unit)
        for allowed in normalized_unit_vocabulary():
            if normalize_unit_token(allowed) == normalize_unit_token(clean):
                return inferred_from_source or allowed
        inferred_from_normalized = infer_normalized_unit(raw_unit=clean, source_span=clean)
        if inferred_from_normalized:
            return inferred_from_source or inferred_from_normalized
        if inferred_from_source:
            return inferred_from_source
        return None
    return inferred_from_source


def normalize_quantity_record(quantity: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(quantity)
    had_normalized_unit = "normalized_unit" in normalized
    canonical_unit = canonicalize_normalized_unit(
        normalized.get("normalized_unit"),
        raw_unit=normalized.get("raw_unit"),
        source_span=normalized.get("source_span"),
    )
    if canonical_unit is not None or had_normalized_unit:
        normalized["normalized_unit"] = canonical_unit
    return normalized


def _assign_measure_relationship_metadata(recipe: RecipeRecord, sections: dict[str, Any]) -> None:
    for host in ("ingredients", "processes", "materials"):
        for entity_index, item in enumerate(sections.get(host, []) or [], start=1):
            quantities = item.get("quantities") or []
            for quantity_index, quantity in enumerate(quantities, start=1):
                relation = quantity.get("measure_relation") or "standalone"
                if relation not in MEASURE_RELATIONS:
                    raise ValueError(
                        f"{recipe.recipe_id}: unsupported measure_relation {relation!r} "
                        f"on {host}[{entity_index}].quantities[{quantity_index}]"
                    )
                quantity["measure_relation"] = relation
                if not quantity.get("measure_group_id"):
                    quantity["measure_group_id"] = (
                        f"{recipe.recipe_id}:{host}:{entity_index}:measure:{quantity_index}"
                    )


def normalize_witness_text(text: str) -> str:
    without_tags = TAG_RE.sub(" ", text)
    return normalize_space(without_tags)


def sentence_prefix(text: str, words: int = 8) -> str:
    clean = normalize_space(re.sub(r"^\d+\s*", "", text))
    parts = clean.split()
    return " ".join(parts[:words]).strip()


@dataclass(frozen=True)
class RecipeRecord:
    dataset_key: str
    source_json: str
    host_raw_file: str
    work_slug: str
    recipe_id: str
    recipe_urn: str
    record_urn: str
    author: str
    work: str
    book: str | None
    chapter: str | None
    section: str | None
    chapter_name: str | None
    lemma: str | None
    text: str
    original_text: str | None
    text_source: str | None
    emendations: list[dict[str, Any]]
    emendation_count: int
    source_kind: str | None
    entry_kind: str | None
    citation: dict[str, Any]
    notes: list[str]

    def to_json(self) -> dict[str, Any]:
        return {
            "dataset_key": self.dataset_key,
            "source_json": self.source_json,
            "host_raw_file": self.host_raw_file,
            "work_slug": self.work_slug,
            "recipe_id": self.recipe_id,
            "recipe_urn": self.recipe_urn,
            "record_urn": self.record_urn,
            "author": self.author,
            "work": self.work,
            "book": self.book,
            "chapter": self.chapter,
            "section": self.section,
            "chapter_name": self.chapter_name,
            "lemma": self.lemma,
            "text": self.text,
            "original_text": self.original_text,
            "text_source": self.text_source,
            "emendations": self.emendations,
            "emendation_count": self.emendation_count,
            "source_kind": self.source_kind,
            "entry_kind": self.entry_kind,
            "citation": self.citation,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class AuthorityEntity:
    group: str
    surface_form: str
    normalized_label: str


@dataclass
class AuthorityRecipe:
    dataset_key: str
    recipe_id: str
    authority_lemma: str
    groups: dict[str, list[AuthorityEntity]]
    notes: list[str]
    authority_source: str


@dataclass(frozen=True)
class StructuredAuthorityRecipe:
    dataset_key: str
    recipe_id: str
    authority_source: str
    metadata: dict[str, Any]
    data: dict[str, Any]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def default_authority_metadata(
    *,
    dataset_key: str | None = None,
    build_version: str | None = None,
) -> dict[str, Any]:
    return {
        "entity_model_version": ENTITY_MODEL_VERSION,
        "authority_version": AUTHORITY_VERSION,
        "prompt_version": prompt_version_for_dataset(dataset_key),
        "build_version": build_version,
    }


def normalize_authority_metadata(metadata: dict[str, Any], *, source: str) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise ValueError(f"Structured authority metadata must be an object in {source}")
    normalized: dict[str, Any] = {}
    for key in AUTHORITY_METADATA_KEYS:
        if key not in metadata:
            raise ValueError(f"Structured authority metadata missing `{key}` in {source}")
        value = metadata[key]
        if key == "build_version":
            if value is not None and not isinstance(value, str):
                raise ValueError(f"Structured authority metadata `{key}` must be a string or null in {source}")
        elif not isinstance(value, str) or not value.strip():
            raise ValueError(f"Structured authority metadata `{key}` must be a non-empty string in {source}")
        normalized[key] = value
    return normalized


def load_structured_authority_corpus(
    path: Path,
    *,
    allow_legacy: bool = False,
    dataset_key: str | None = None,
) -> dict[str, Any]:
    payload = load_json(path)
    if "metadata" in payload or "recipes" in payload:
        metadata = normalize_authority_metadata(payload.get("metadata"), source=str(path.relative_to(REPO_ROOT)))
        recipes = payload.get("recipes")
        if not isinstance(recipes, dict):
            raise ValueError(
                f"Structured authority `recipes` must be an object in {path.relative_to(REPO_ROOT)}"
            )
        return {"metadata": metadata, "recipes": recipes}
    if allow_legacy:
        return {"metadata": default_authority_metadata(dataset_key=dataset_key, build_version=None), "recipes": payload}
    raise ValueError(
        f"Structured authority file {path.relative_to(REPO_ROOT)} is missing required `metadata` and `recipes` wrapper"
    )


@lru_cache(maxsize=1)
def load_recipe_entity_file_map() -> dict[str, Path]:
    index_payload = load_json(RECIPE_ENTITY_DIR / "index.json")
    if isinstance(index_payload, list):
        index = index_payload
    else:
        index = index_payload.get("recipes", [])
    return {item["recipe_id"]: REPO_ROOT / item["file"] for item in index}


def _viewer_quantity_display(quantity: dict[str, Any]) -> str:
    source_span = normalize_space(str(quantity.get("source_span") or ""))
    if source_span:
        return source_span
    raw_unit = normalize_space(str(quantity.get("raw_unit") or ""))
    raw_number = normalize_space(str(quantity.get("raw_number") or ""))
    return " ".join(part for part in (raw_unit, raw_number) if part).strip()


def _compact_projection(payload: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {group: [] for group in VIEWER_ENTITY_GROUPS}

    preparation = payload.get("preparation")
    if preparation:
        grouped["labels"].append(
            {
                "entity_urn": preparation["preparation_urn"],
                "surface_form": preparation["surface_form"],
                "normalized_label": preparation["normalized_label"],
            }
        )

    for item in payload.get("ingredients", []):
        quantity_display = " · ".join(
            display for display in (_viewer_quantity_display(quantity) for quantity in item.get("quantities", [])) if display
        )
        grouped["ingredients"].append(
            {
                "entity_urn": item["ingredient_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
                "quantity_display": quantity_display,
            }
        )
    for item in payload.get("processes", []):
        grouped["processes"].append(
            {
                "entity_urn": item["process_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("materials", []):
        grouped["tools"].append(
            {
                "entity_urn": item["material_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("other_preparations_mentioned", []):
        grouped["other_preparations_mentioned"].append(
            {
                "entity_urn": item["reference_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("people", []):
        grouped["people"].append(
            {
                "entity_urn": item["person_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("places", []):
        grouped["places"].append(
            {
                "entity_urn": item["place_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("works_mentioned", []):
        grouped["works_mentioned"].append(
            {
                "entity_urn": item["work_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("preparation_names", []):
        grouped["preparation_names"].append(
            {
                "entity_urn": item["preparation_name_urn"],
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    return grouped


@lru_cache(maxsize=1)
def load_compact_recipe_entity_groups() -> dict[str, dict[str, list[dict[str, str]]]]:
    grouped: dict[str, dict[str, list[dict[str, str]]]] = {}
    for recipe_id, path in load_recipe_entity_file_map().items():
        payload = load_json(path)
        grouped[recipe_id] = _compact_projection(payload)
    return grouped


def attach_viewer_entity_groups(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = load_compact_recipe_entity_groups()
    attached: list[dict[str, Any]] = []

    for entry in entries:
        recipe_id = entry.get("id")
        if not recipe_id:
            raise KeyError("Experiment entry is missing required `id` for derived recipe lookup")
        if recipe_id not in grouped:
            raise KeyError(f"Missing derived recipe entity record for {recipe_id}")
        entry["derived_recipe_id"] = recipe_id
        entry["entity_groups"] = {
            group: [dict(item) for item in grouped[recipe_id][group]]
            for group in VIEWER_ENTITY_GROUPS
        }
        attached.append(entry)

    return attached


def _extract_citation(entry: dict[str, Any]) -> dict[str, Any]:
    for key in ("wellmann", "olivieri", "zervos", "heiberg"):
        if key in entry:
            citation = dict(entry[key])
            citation["edition_key"] = key
            return citation
    return {}


def _fallback_recipe_id(dataset_key: str, entry: dict[str, Any]) -> str:
    base = "-".join(
        part
        for part in (
            dataset_key,
            str(entry.get("book") or ""),
            str(entry.get("chapter") or ""),
            str(entry.get("section") or ""),
            greek_ascii_slug(entry.get("lemma") or "recipe"),
        )
        if part
    )
    return base


def _split_recipe_records(recipe: RecipeRecord) -> list[RecipeRecord]:
    split_specs = RECIPE_RECORD_SPLITS.get(recipe.recipe_id)
    if not split_specs:
        return [recipe]

    split_records: list[RecipeRecord] = []
    for spec in split_specs:
        recipe_id = spec["recipe_id"]
        split_records.append(
            replace(
                recipe,
                recipe_id=recipe_id,
                recipe_urn=f"urn:aos:recipe:{recipe_id}",
                record_urn=f"urn:aos:recipe-record:{recipe_id}",
                section=spec.get("section", recipe.section),
                chapter_name=spec.get("chapter_name", recipe.chapter_name),
                lemma=spec.get("lemma", recipe.lemma),
                text=normalize_space(spec["text"]),
                original_text=recipe.original_text,
                text_source=recipe.text_source,
                emendations=[dict(item) for item in recipe.emendations],
                emendation_count=recipe.emendation_count,
                citation=dict(spec.get("citation", recipe.citation)),
                notes=[*recipe.notes, *spec.get("notes", [])],
            )
        )
    return split_records


def load_recipe_records() -> list[RecipeRecord]:
    records: list[RecipeRecord] = []
    for dataset in DATASETS:
        payload = load_json(dataset["path"])
        entries = payload.get(dataset["entries_key"], [])
        for entry in entries:
            recipe_id = entry.get("id") or _fallback_recipe_id(dataset["key"], entry)
            recipe_urn = f"urn:aos:recipe:{recipe_id}"
            record_urn = f"urn:aos:recipe-record:{recipe_id}"
            notes: list[str] = []
            if payload["source"].get("notes"):
                notes.extend(payload["source"]["notes"])
            caveat = entry.get("caveat")
            if caveat:
                notes.append(caveat)
            if entry.get("source_kind") == "apparatus":
                notes.append("Apparatus-derived recipe unit; do not force main-text TEI boundary.")
            section = entry.get("section")
            if section is not None:
                section = str(section)
            base_record = RecipeRecord(
                    dataset_key=dataset["key"],
                    source_json=str(dataset["path"].relative_to(REPO_ROOT)),
                    host_raw_file=dataset["host_raw_file"],
                    work_slug=dataset["work_slug"],
                    recipe_id=recipe_id,
                    recipe_urn=recipe_urn,
                    record_urn=record_urn,
                    author=payload["work"]["author"],
                    work=payload["work"]["work"],
                    book=str(entry.get("book") or payload["work"].get("book") or ""),
                    chapter=str(entry.get("chapter") or payload["work"].get("chapter") or ""),
                    section=section,
                    chapter_name=entry.get("chapter_name") or payload["work"].get("chapter_name"),
                    lemma=entry.get("lemma"),
                    text=normalize_space(entry.get("text", "")),
                    original_text=normalize_space(entry.get("original_text", "")) or None,
                    text_source=entry.get("text_source"),
                    emendations=[dict(item) for item in entry.get("emendations", [])],
                    emendation_count=int(entry.get("emendation_count", 0) or 0),
                    source_kind=entry.get("source_kind"),
                    entry_kind=entry.get("entry_kind") or dataset.get("recipe_kind"),
                    citation=_extract_citation(entry),
                    notes=notes,
                )
            records.extend(_split_recipe_records(base_record))
    return records


@lru_cache(maxsize=1)
def load_recipe_record_map() -> dict[str, RecipeRecord]:
    return {record.recipe_id: record for record in load_recipe_records()}


def _clean_entity_text(text: str) -> str:
    cleaned = normalize_space(text.replace("→", "->").replace("`", ""))
    cleaned = cleaned.rstrip(" .;:")
    return cleaned


def _parse_entity_value(value: str) -> list[AuthorityEntity]:
    value = value.strip()
    if not value or "none attested" in value.lower():
        return []

    parsed: list[AuthorityEntity] = []
    for surface, normalized in SURFACE_NORMALIZED_RE.findall(value):
        surface_clean = _clean_entity_text(surface)
        normalized_clean = _clean_entity_text(normalized or surface)
        parsed.append(
            AuthorityEntity(
                group="",
                surface_form=surface_clean,
                normalized_label=normalized_clean,
            )
        )
    if parsed:
        return parsed

    for part in [chunk.strip() for chunk in value.split(";") if chunk.strip()]:
        if "->" in part:
            surface, normalized = part.split("->", 1)
        elif "→" in part:
            surface, normalized = part.split("→", 1)
        else:
            surface = normalized = part
        surface_clean = _clean_entity_text(surface)
        normalized_clean = _clean_entity_text(normalized)
        if not surface_clean:
            continue
        parsed.append(
            AuthorityEntity(
                group="",
                surface_form=surface_clean,
                normalized_label=normalized_clean or surface_clean,
            )
        )
    return parsed


def _new_authority_groups() -> dict[str, list[AuthorityEntity]]:
    return {group: [] for group in set(LEDGER_FIELD_TO_GROUP.values())}


def parse_review_ledger(path: Path, dataset_key: str) -> dict[str, AuthorityRecipe]:
    recipes: dict[str, AuthorityRecipe] = {}
    current: AuthorityRecipe | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        header_match = HEADER_RE.match(line)
        if header_match:
            recipe_id = header_match.group(1).strip()
            lemma = normalize_space(header_match.group(2))
            current = AuthorityRecipe(
                dataset_key=dataset_key,
                recipe_id=recipe_id,
                authority_lemma=lemma,
                groups=_new_authority_groups(),
                notes=[],
                authority_source=str(path.relative_to(REPO_ROOT)),
            )
            recipes[recipe_id] = current
            continue
        if not current:
            continue
        field_match = FIELD_RE.match(line)
        if not field_match:
            continue
        field = normalize_space(field_match.group(1))
        value = field_match.group(2).strip()
        if field == "notes":
            current.notes.append(value)
            continue
        group = LEDGER_FIELD_TO_GROUP.get(field)
        if not group:
            continue
        entities = _parse_entity_value(value)
        current.groups[group] = [
            AuthorityEntity(group=group, surface_form=item.surface_form, normalized_label=item.normalized_label)
            for item in entities
        ]

    return recipes


@lru_cache(maxsize=1)
def load_authority_recipe_map() -> dict[str, AuthorityRecipe]:
    authority: dict[str, AuthorityRecipe] = {}
    for dataset_key, rel_path in AUTHORITY_LEDGER_BY_DATASET.items():
        parsed = parse_review_ledger(REPO_ROOT / rel_path, dataset_key)
        authority.update(parsed)
    return authority


@lru_cache(maxsize=1)
def load_structured_authority_recipe_map() -> dict[str, StructuredAuthorityRecipe]:
    structured: dict[str, StructuredAuthorityRecipe] = {}
    for dataset_key, rel_path in STRUCTURED_AUTHORITY_BY_DATASET.items():
        path = REPO_ROOT / rel_path
        if not path.exists():
            continue
        payload = load_structured_authority_corpus(path, dataset_key=dataset_key)
        for recipe_id, data in payload["recipes"].items():
            structured[recipe_id] = StructuredAuthorityRecipe(
                dataset_key=dataset_key,
                recipe_id=recipe_id,
                authority_source=str(path.relative_to(REPO_ROOT)),
                metadata=dict(payload["metadata"]),
                data=data,
            )
    return structured


@lru_cache(maxsize=1)
def load_structured_authority_dataset_map() -> dict[str, dict[str, Any]]:
    datasets: dict[str, dict[str, Any]] = {}
    for dataset_key, rel_path in STRUCTURED_AUTHORITY_BY_DATASET.items():
        path = REPO_ROOT / rel_path
        if path.exists():
            datasets[dataset_key] = load_structured_authority_corpus(path, dataset_key=dataset_key)
    return datasets


def _host_locator(recipe: RecipeRecord) -> dict[str, Any]:
    return {
        "book": recipe.book,
        "chapter": recipe.chapter,
        "section": recipe.section,
        "citation": recipe.citation.get("citation"),
    }


def _copy_notes(notes: list[str] | None) -> list[str]:
    return [normalize_space(note) for note in notes or [] if normalize_space(note)]


def _make_record_id(recipe: RecipeRecord, prefix: str, slug: str) -> str:
    return f"{recipe.recipe_id}:{prefix}:{slug}"


def _make_urn(label: str, record_id: str) -> str:
    return f"urn:aos:{label}:{record_id}"


def make_quantity(
    *,
    source_span: str,
    raw_number: str | None = None,
    normalized_number: int | float | str | None = None,
    raw_unit: str | None = None,
    normalized_unit: str | None = None,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return normalize_quantity_record(
        {
        "source_span": normalize_space(source_span),
        "raw_number": raw_number,
        "normalized_number": normalized_number,
        "raw_unit": raw_unit,
        "normalized_unit": normalized_unit,
        "certainty": certainty,
        "notes": _copy_notes(notes),
        }
    )


def make_qualifier(
    *,
    qualifier_type: str,
    source_span: str,
    normalized_value: str | None = None,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "qualifier_type": qualifier_type,
        "source_span": normalize_space(source_span),
        "normalized_value": normalize_space(normalized_value) if normalized_value else None,
        "certainty": certainty,
        "notes": _copy_notes(notes),
    }


def make_regimen_note(
    *,
    source_span: str,
    normalized_note: str,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "source_span": normalize_space(source_span),
        "normalized_note": normalize_space(normalized_note),
        "certainty": certainty,
        "notes": _copy_notes(notes),
    }


def make_preparation(
    recipe: RecipeRecord,
    source_span: str,
    normalized_label: str,
    *,
    qualifiers: list[dict[str, Any]] | None = None,
    regimen_notes: list[dict[str, Any]] | None = None,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    record_id = _make_record_id(recipe, "preparation", greek_ascii_slug(normalized_label))
    return {
        "preparation_id": record_id,
        "preparation_urn": _make_urn("recipe-preparation", record_id),
        "source_span": normalize_space(source_span),
        "surface_form": normalize_space(source_span),
        "normalized_label": normalize_space(normalized_label),
        "qualifiers": [dict(item) for item in qualifiers or []],
        "regimen_notes": [
            make_regimen_note(
                source_span=item.get("source_span") or item.get("normalized_note") or "regimen note",
                normalized_note=item.get("normalized_note") or item.get("source_span") or "regimen note",
                certainty=item.get("certainty", "certain"),
                notes=item.get("notes"),
            )
            for item in regimen_notes or []
        ],
        "certainty": certainty,
        "notes": _copy_notes(notes),
        "host_locator": _host_locator(recipe),
    }


def make_ingredient(
    recipe: RecipeRecord,
    *,
    slug: str,
    source_span: str,
    base_label: str,
    normalized_label: str | None = None,
    alternative_set_id: str | None = None,
    certainty: str = "certain",
    linked_process_ids: list[str] | None = None,
    quantities: list[dict[str, Any]] | None = None,
    qualifiers: list[dict[str, Any]] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    record_id = _make_record_id(recipe, "ingredient", slug)
    return {
        "ingredient_id": record_id,
        "ingredient_urn": _make_urn("recipe-ingredient", record_id),
        "source_span": normalize_space(source_span),
        "surface_form": normalize_space(source_span),
        "base_label": normalize_space(base_label),
        "normalized_label": normalize_space(normalized_label or base_label),
        "alternative_set_id": normalize_space(alternative_set_id) if alternative_set_id else None,
        "certainty": certainty,
        "linked_process_ids": list(linked_process_ids or []),
        "quantities": list(quantities or []),
        "qualifiers": list(qualifiers or []),
        "notes": _copy_notes(notes),
        "host_locator": _host_locator(recipe),
    }


def make_process(
    recipe: RecipeRecord,
    *,
    slug: str,
    source_span: str,
    normalized_label: str,
    target_type: str = "recipe",
    target_ids: list[str] | None = None,
    quantities: list[dict[str, Any]] | None = None,
    qualifiers: list[dict[str, Any]] | None = None,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    record_id = _make_record_id(recipe, "process", slug)
    return {
        "process_id": record_id,
        "process_urn": _make_urn("recipe-process", record_id),
        "source_span": normalize_space(source_span),
        "surface_form": normalize_space(source_span),
        "normalized_label": normalize_space(normalized_label),
        "target_type": target_type,
        "target_ids": list(target_ids or []),
        "quantities": list(quantities or []),
        "qualifiers": list(qualifiers or []),
        "certainty": certainty,
        "notes": _copy_notes(notes),
        "host_locator": _host_locator(recipe),
    }


def make_material(
    recipe: RecipeRecord,
    *,
    slug: str,
    source_span: str,
    normalized_label: str,
    role: str,
    certainty: str = "certain",
    quantities: list[dict[str, Any]] | None = None,
    qualifiers: list[dict[str, Any]] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    record_id = _make_record_id(recipe, "material", slug)
    return {
        "material_id": record_id,
        "material_urn": _make_urn("recipe-material", record_id),
        "source_span": normalize_space(source_span),
        "surface_form": normalize_space(source_span),
        "normalized_label": normalize_space(normalized_label),
        "role": role,
        "certainty": certainty,
        "quantities": list(quantities or []),
        "qualifiers": list(qualifiers or []),
        "notes": _copy_notes(notes),
        "host_locator": _host_locator(recipe),
    }


def make_context_record(
    recipe: RecipeRecord,
    *,
    kind: str,
    slug: str,
    source_span: str,
    normalized_label: str,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    record_id = _make_record_id(recipe, kind, slug)
    return {
        f"{kind}_id": record_id,
        f"{kind}_urn": _make_urn(f"recipe-{kind}", record_id),
        "source_span": normalize_space(source_span),
        "surface_form": normalize_space(source_span),
        "normalized_label": normalize_space(normalized_label),
        "certainty": certainty,
        "notes": _copy_notes(notes),
        "host_locator": _host_locator(recipe),
    }


def make_use(
    recipe: RecipeRecord,
    *,
    slug: str,
    category: str,
    source_span: str,
    snippet: str,
    certainty: str = "certain",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    record_id = _make_record_id(recipe, "use", slug)
    return {
        "use_id": record_id,
        "use_urn": _make_urn("recipe-use", record_id),
        "category": category,
        "source_span": normalize_space(source_span),
        "snippet": normalize_space(snippet),
        "certainty": certainty,
        "notes": _copy_notes(notes),
        "host_locator": _host_locator(recipe),
    }


STRUCTURED_REVIEW_OVERRIDES: dict[str, dict[str, Any]] = {
    "aetius-16-134-2": {
        "ingredients": [
            {
                "slug": "rhoda",
                "source_span": "Ῥόδων ἐξωνυχισμένων καὶ προμαρανθέντων ἐπὶ σινδόνος ἡμέραν καὶ νύκτα",
                "base_label": "ῥόδον",
                "normalized_label": "ῥόδον",
                "linked_process_slugs": ["exonychizo", "promaraino", "probrecho"],
                "quantities": [
                    {
                        "source_span": "λίτ. α.",
                        "raw_number": "α",
                        "normalized_number": 1,
                        "raw_unit": "λίτ.",
                        "normalized_unit": "litra",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "meli",
                "source_span": "μέλιτος καλοῦ",
                "base_label": "μέλι",
                "normalized_label": "μέλι",
                "quantities": [
                    {
                        "source_span": "ξστα ἤτοι ξέστ. α.",
                        "raw_number": "α",
                        "normalized_number": 1,
                        "raw_unit": "ξέστ.",
                        "normalized_unit": "xestes",
                        "certainty": "certain",
                        "notes": ["Witness gives an explicit xestes equivalence."],
                    }
                ],
            },
            {
                "slug": "oinos-palaios",
                "source_span": "οἴνου παλαιοῦ",
                "base_label": "οἶνος",
                "normalized_label": "οἶνος παλαιός",
                "quantities": [
                    {
                        "source_span": "ξστε ἤτοι ξέστ. ε.",
                        "raw_number": "ε",
                        "normalized_number": 5,
                        "raw_unit": "ξέστ.",
                        "normalized_unit": "xestes",
                        "certainty": "certain",
                        "notes": ["Passage gives the equivalence explicitly."],
                    }
                ],
            },
            {
                "slug": "nardostachys",
                "source_span": "ναρδοστάχυος",
                "base_label": "ναρδόσταχυς",
                "normalized_label": "ναρδόσταχυς",
                "quantities": [
                    {
                        "source_span": "γράμματα β.",
                        "raw_number": "β",
                        "normalized_number": 2,
                        "raw_unit": "γράμματα",
                        "normalized_unit": "gramma",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "phyllon-e-kasia",
                "source_span": "φύλλου ἢ κασίας",
                "base_label": "φύλλον ἢ κασία",
                "normalized_label": "φύλλον ἢ κασία",
                "certainty": "uncertain",
                "quantities": [
                    {
                        "source_span": "γράμμα α.",
                        "raw_number": "α",
                        "normalized_number": 1,
                        "raw_unit": "γράμμα",
                        "normalized_unit": "gramma",
                        "certainty": "certain",
                    }
                ],
                "notes": ["Witness gives an alternative material rather than a single fixed ingredient."],
            },
        ],
        "processes": [
            {
                "slug": "exonychizo",
                "source_span": "ἐξωνυχισμένων",
                "normalized_label": "ἐξωνυχίζω",
                "target_type": "ingredient",
                "target_slugs": ["rhoda"],
            },
            {
                "slug": "promaraino",
                "source_span": "προμαρανθέντων",
                "normalized_label": "προμαραίνω",
                "target_type": "ingredient",
                "target_slugs": ["rhoda"],
                "qualifiers": [
                    {
                        "qualifier_type": "location",
                        "source_span": "ἐπὶ σινδόνος",
                        "normalized_value": "ἐπὶ σινδόνος",
                        "certainty": "certain",
                    },
                    {
                        "qualifier_type": "duration",
                        "source_span": "ἡμέραν καὶ νύκτα",
                        "normalized_value": "one day and night",
                        "certainty": "certain",
                    },
                ],
            },
            {
                "slug": "probrecho",
                "source_span": "Προβρέχων",
                "normalized_label": "προβρέχω",
                "target_type": "ingredient",
                "target_slugs": ["rhoda"],
                "qualifiers": [
                    {
                        "qualifier_type": "other",
                        "source_span": "τῷ οἴνῳ",
                        "normalized_value": "with wine",
                        "certainty": "certain",
                    },
                    {
                        "qualifier_type": "duration",
                        "source_span": "ἐπὶ ἡμέρας ιε",
                        "normalized_value": "15 days",
                        "certainty": "certain",
                    },
                ],
            },
            {
                "slug": "tithemi",
                "source_span": "τίθει",
                "normalized_label": "τίθημι",
                "target_type": "recipe",
                "qualifiers": [
                    {
                        "qualifier_type": "exposure",
                        "source_span": "ἐν ἡλίῳ καθ' ἑκάστην",
                        "normalized_value": "sun exposure each day",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "dietheo",
                "source_span": "διηθήσας",
                "normalized_label": "διηθέω",
            },
            {
                "slug": "proleioo",
                "source_span": "προλειώσας",
                "normalized_label": "προλειόω",
            },
            {
                "slug": "epiballo",
                "source_span": "ἐπιβαλὼν",
                "normalized_label": "ἐπιβάλλω",
            },
            {
                "slug": "sylleioo",
                "source_span": "συλλειώσας",
                "normalized_label": "συλλειόω",
            },
            {
                "slug": "mignymi",
                "source_span": "μίγνυε",
                "normalized_label": "μίγνυμι",
            },
        ],
        "materials": [
            {
                "slug": "sindon",
                "source_span": "σινδόνος",
                "normalized_label": "σινδών",
                "role": "apparatus",
            },
            {
                "slug": "thyia",
                "source_span": "θυίᾳ",
                "normalized_label": "θυία",
                "role": "tool",
            },
            {
                "slug": "keramion",
                "source_span": "κεράμιον",
                "normalized_label": "κεράμιον",
                "role": "apparatus",
            },
        ],
        "notes": [
            "Embedded GPT-5.4-high override restores participial process splitting, linked qualifiers, and direct ingredient quantities."
        ],
    },
    "aetius-1-135": {
        "ingredients": [
            {
                "slug": "onyx-aromatikos",
                "source_span": "ὀνύχων ἀρωματικῶν μεγάλων",
                "base_label": "ὄνυξ ἀρωματικός",
                "normalized_label": "ὄνυξ ἀρωματικός",
                "quantities": [
                    {
                        "source_span": "𐆄 ε",
                        "raw_number": "ε",
                        "normalized_number": 5,
                        "raw_unit": "𐆄",
                        "normalized_unit": "uncia",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "styrax-proteios",
                "source_span": "στύρακος πρωτείου",
                "base_label": "στύραξ",
                "normalized_label": "στύραξ πρωτεῖος",
                "quantities": [
                    {
                        "source_span": "𐆄 ε",
                        "raw_number": "ε",
                        "normalized_number": 5,
                        "raw_unit": "𐆄",
                        "normalized_unit": "uncia",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "bdellion",
                "source_span": "βδελλίου καθαροῦ",
                "base_label": "βδέλλιον",
                "normalized_label": "βδέλλιον",
                "quantities": [
                    {
                        "source_span": "𐆄 ε",
                        "raw_number": "ε",
                        "normalized_number": 5,
                        "raw_unit": "𐆄",
                        "normalized_unit": "uncia",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "kostos",
                "source_span": "κόστου",
                "base_label": "κόστος",
                "normalized_label": "κόστος",
                "quantities": [
                    {
                        "source_span": "𐆄 εʹ",
                        "raw_number": "εʹ",
                        "normalized_number": 5,
                        "raw_unit": "𐆄",
                        "normalized_unit": "uncia",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "elaion-glyky",
                "source_span": "ἐλαίου γλυκέος καλοῦ",
                "base_label": "ἔλαιον γλυκύ",
                "normalized_label": "ἔλαιον γλυκύ",
                "quantities": [
                    {
                        "source_span": "ξ̸εε",
                        "raw_number": "ξ̸εε",
                        "normalized_number": None,
                        "raw_unit": None,
                        "normalized_unit": None,
                        "certainty": "uncertain",
                        "notes": ["Witness quantity is preserved raw because the compound abbreviation is not normalized safely here."],
                    }
                ],
            },
        ],
        "processes": [
            {"slug": "skeuazo", "source_span": "σκευάζεται", "normalized_label": "σκευάζω"},
            {"slug": "diamerizo", "source_span": "διαμερίσας", "normalized_label": "διαμερίζω"},
            {"slug": "anamignymi", "source_span": "ἀναμίξας", "normalized_label": "ἀναμίγνυμι"},
            {"slug": "emballo", "source_span": "ἔμβαλε", "normalized_label": "ἐμβάλλω"},
            {"slug": "skepazo", "source_span": "σκεπάσας", "normalized_label": "σκεπάζω"},
            {"slug": "periphrasso", "source_span": "περιφράξας", "normalized_label": "περιφράσσω"},
            {"slug": "orysso", "source_span": "ὀρύξας", "normalized_label": "ὀρύσσω"},
            {"slug": "chonnyo", "source_span": "χῶσον", "normalized_label": "χώννυμι"},
            {"slug": "armozo", "source_span": "ἁρμόσας", "normalized_label": "ἁρμόζω"},
            {"slug": "chrio", "source_span": "χρίε", "normalized_label": "χρίω"},
            {"slug": "anapto", "source_span": "ἄναψον", "normalized_label": "ἀνάπτω"},
            {"slug": "ripizo", "source_span": "ῥίπιζε", "normalized_label": "ῥιπίζω"},
            {
                "slug": "kapnizo",
                "source_span": "καπνίσῃ",
                "normalized_label": "καπνίζω",
                "qualifiers": [
                    {
                        "qualifier_type": "other",
                        "source_span": "τὸ ὑποκείμενον αὐτοῖς ἔλαιον",
                        "normalized_value": "the oil beneath the aromatics",
                        "certainty": "certain",
                    }
                ],
            },
            {"slug": "anoigo", "source_span": "ἀνοίξας", "normalized_label": "ἀνοίγω"},
            {"slug": "anaireo", "source_span": "ἀνελοῦ", "normalized_label": "ἀναιρέω"},
            {"slug": "phylasso", "source_span": "φύλαττε", "normalized_label": "φυλάσσω"},
        ],
        "materials": [
            {
                "slug": "xestion-ostrakinon",
                "source_span": "ξεστίῳ καινῷ ὀστρακίνῳ",
                "normalized_label": "ξεστίον ὀστράκινον",
                "role": "apparatus",
            },
            {
                "slug": "hypnos-sealant",
                "source_span": "ὕπνῳ",
                "normalized_label": "ὕπνος",
                "role": "adjunct_material",
                "certainty": "uncertain",
                "notes": ["Witness names ὕπνος as a sealing medium here; role retained conservatively without over-normalizing."],
            },
            {
                "slug": "xylaria-aspalathou",
                "source_span": "ξυλάρια ἀσπαλάθου ἢ τινος τῶν εὐωδῶν",
                "normalized_label": "ξυλάρια ἀσπαλάθου ἢ τινος τῶν εὐωδῶν",
                "role": "fuel",
                "certainty": "uncertain",
                "notes": ["Structured GPT-5.4-high override keeps the aromatic wood span instead of dropping it; exact role could be fuel or aromatic adjunct."],
            },
            {
                "slug": "aggeion-ostrakinon",
                "source_span": "ὀστράκινον ἀγγεῖον",
                "normalized_label": "ὀστράκινον ἀγγεῖον",
                "role": "apparatus",
            },
            {
                "slug": "karbones",
                "source_span": "κάρβωνας πολλούς",
                "normalized_label": "κάρβων",
                "role": "fuel",
            },
            {
                "slug": "yalinon-aggeion",
                "source_span": "ὑαλίνῳ ἀγγείῳ",
                "normalized_label": "ὑάλινον ἀγγεῖον",
                "role": "apparatus",
            },
        ],
        "people": [
            {
                "slug": "gynaikes",
                "source_span": "γυναῖκες",
                "normalized_label": "γυνή",
            }
        ],
        "uses": [
            {
                "slug": "menses-application",
                "category": "medical",
                "source_span": "τούτῳ χρῶνται αἱ γυναῖκες ἐφ' ὧν ἐπίσχηται τὰ καταμήνια, χρίουσαι αὐτῷ τὸ ἦτρον καὶ τὴν ὀσφύν",
                "snippet": "Women use it when the menses are blocked, applying it to the lower abdomen and loins.",
            },
            {
                "slug": "thorax-warming",
                "category": "medical",
                "source_span": "χρήσιμον δὲ καὶ τοῖς τὸν θώρακα ἐψυγμένοις καὶ τεινεσμῶν ἐνοχλούντων",
                "snippet": "Also used for a chilled chest and related distress.",
            },
        ],
        "notes": [
            "Embedded GPT-5.4-high override restores omitted aromatic-wood and fuel/apparatus materials and moves explicit application language into uses."
        ],
    },
    "paul-7-20-4": {
        "ingredients": [
            {
                "slug": "rhoda",
                "source_span": "Ῥόδων ἐρυθρῶν ὠνυχισμένων καὶ διεψυγμένων",
                "base_label": "ῥόδον",
                "normalized_label": "ῥόδον",
                "linked_process_slugs": ["onychizo", "diepsycho"],
                "qualifiers": [
                    {
                        "qualifier_type": "color",
                        "source_span": "ἐρυθρῶν",
                        "normalized_value": "red",
                        "certainty": "certain",
                    }
                ],
                "quantities": [
                    {
                        "source_span": "𐆄 γ",
                        "raw_number": "γ",
                        "normalized_number": 3,
                        "raw_unit": "𐆄",
                        "normalized_unit": "uncia",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "elaion-omphakinon",
                "source_span": "ἐλαίου ὀμφακίνου",
                "base_label": "ἔλαιον ὀμφάκινον",
                "normalized_label": "ἔλαιον ὀμφάκινον",
                "quantities": [
                    {
                        "source_span": "ξ̸ Ἰταλικὸν α",
                        "raw_number": "α",
                        "normalized_number": None,
                        "raw_unit": "ξ̸ Ἰταλικόν",
                        "normalized_unit": None,
                        "certainty": "uncertain",
                        "notes": ["Italian xestes notation is preserved raw here rather than normalized unsafely."],
                    }
                ],
            },
        ],
        "processes": [
            {
                "slug": "onychizo",
                "source_span": "ὠνυχισμένων",
                "normalized_label": "ὀνυχίζω",
                "target_type": "ingredient",
                "target_slugs": ["rhoda"],
            },
            {
                "slug": "diepsycho",
                "source_span": "διεψυγμένων",
                "normalized_label": "διαψύχω",
                "target_type": "ingredient",
                "target_slugs": ["rhoda"],
                "qualifiers": [
                    {
                        "qualifier_type": "duration",
                        "source_span": "νυχθήμερον α",
                        "normalized_value": "one day-night",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "perisphiggo",
                "source_span": "περισφίγξας",
                "normalized_label": "περισφίγγω",
                "target_type": "recipe",
            },
            {
                "slug": "apotithemi",
                "source_span": "ἀποτίθεσο",
                "normalized_label": "ἀποτίθημι",
                "target_type": "recipe",
                "qualifiers": [
                    {
                        "qualifier_type": "exposure",
                        "source_span": "ἡλίου",
                        "normalized_value": "sun",
                        "certainty": "certain",
                    },
                    {
                        "qualifier_type": "location",
                        "source_span": "ἐν ὑπαίθρῳ",
                        "normalized_value": "outdoors",
                        "certainty": "certain",
                    },
                    {
                        "qualifier_type": "duration",
                        "source_span": "ἐπὶ μ ἡμέρας",
                        "normalized_value": "40 days",
                        "certainty": "certain",
                    },
                ],
            },
            {
                "slug": "kathizo",
                "source_span": "καθίασιν",
                "normalized_label": "καθίζω",
                "target_type": "recipe",
                "qualifiers": [
                    {
                        "qualifier_type": "location",
                        "source_span": "εἰς φρέαρ",
                        "normalized_value": "into a well",
                        "certainty": "certain",
                    },
                    {
                        "qualifier_type": "duration",
                        "source_span": "τὰς μ ἡμέρας",
                        "normalized_value": "40 days",
                        "certainty": "certain",
                    },
                ],
            },
            {
                "slug": "katorytto",
                "source_span": "κατορύττουσιν",
                "normalized_label": "κατορύττω",
                "target_type": "recipe",
                "qualifiers": [
                    {
                        "qualifier_type": "location",
                        "source_span": "ἐπὶ τῆς γῆς",
                        "normalized_value": "in the ground",
                        "certainty": "certain",
                    }
                ],
            },
        ],
        "materials": [
            {
                "slug": "bikos",
                "source_span": "τὸν βῖκον",
                "normalized_label": "βῖκος",
                "role": "apparatus",
            }
        ],
        "notes": [
            "Embedded GPT-5.4-high override keeps durations and exposure/location context out of flat process labels."
        ],
    },
    "aetius-16-128": {
        "uses": [
            {
                "slug": "neck-armpits",
                "category": "cosmetic",
                "source_span": "ᾧ χρῶνται εἰς τοὺς τραχήλους καὶ ἐπὶ τὰς μασχάλας",
                "snippet": "Applied to the neck and armpits.",
            }
        ],
        "notes": ["Embedded GPT-5.4-high override keeps the application clause as an explicit cosmetic use."],
    },
    "aetius-16-146-1": {
        "processes": [
            {
                "slug": "kapnizo",
                "source_span": "καπνιζομένου",
                "normalized_label": "καπνίζω",
                "target_type": "recipe",
                "qualifiers": [
                    {
                        "qualifier_type": "location",
                        "source_span": "ἐν τῇ ἐκκλησίᾳ",
                        "normalized_value": "in church",
                        "certainty": "certain",
                    }
                ],
            },
            {
                "slug": "prostithemi",
                "source_span": "προστιθέασι",
                "normalized_label": "προστίθημι",
            },
        ],
        "uses": [
            {
                "slug": "church-incense",
                "category": "ritual",
                "source_span": "μοσχάτου ἐν τῇ ἐκκλησίᾳ καπνιζομένου",
                "snippet": "Used as perfumed incense in church.",
            }
        ],
        "notes": ["Embedded GPT-5.4-high override makes the church-smoking context an explicit ritual use plus process qualifier."],
    },
    "paul-7-20-23": {
        "ingredients": [
            {
                "slug": "agrioy-sikyoy-rhiza",
                "source_span": "τῆς ῥίζης τοῦ ἀγρίου σικύου",
                "base_label": "ῥίζα ἀγρίου σικύου",
                "normalized_label": "ῥίζα ἀγρίου σικύου",
                "linked_process_slugs": ["diapsycho"],
            },
            {
                "slug": "elaion-italikon",
                "source_span": "τὸν Ἰταλικὸν τοῦ ἐλαίου",
                "base_label": "ἔλαιον",
                "normalized_label": "ἔλαιον Ἰταλικόν",
                "quantities": [
                    {
                        "source_span": "ξ̸",
                        "raw_number": "ξ̸",
                        "normalized_number": None,
                        "raw_unit": None,
                        "normalized_unit": None,
                        "certainty": "uncertain",
                    }
                ],
            },
        ],
        "processes": [
            {
                "slug": "diapsycho",
                "source_span": "διαψυγείσης",
                "normalized_label": "διαψύχω",
                "target_type": "ingredient",
                "target_slugs": ["agrioy-sikyoy-rhiza"],
            },
            {
                "slug": "emballo",
                "source_span": "ἐμβαλλομένων",
                "normalized_label": "ἐμβάλλω",
                "target_type": "recipe",
            },
            {
                "slug": "hepso",
                "source_span": "ἑψομένης",
                "normalized_label": "ἕψω",
                "target_type": "recipe",
            },
        ],
        "materials": [
            {
                "slug": "diploma",
                "source_span": "διπλώματι",
                "normalized_label": "δίπλωμα",
                "role": "apparatus",
            }
        ],
        "notes": ["Embedded GPT-5.4-high override keeps the prepared cucumber-root phrase as an ingredient mention linked to its own participial process."],
    },
}


def _reference_records(
    recipe: RecipeRecord,
    *,
    kind: str,
    items: list[AuthorityEntity],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        slug = f"{greek_ascii_slug(item.normalized_label)}-{idx}"
        records.append(
            make_context_record(
                recipe,
                kind=kind,
                slug=slug,
                source_span=item.surface_form,
                normalized_label=item.normalized_label,
            )
        )
    return records


def _reference_records_from_specs(
    recipe: RecipeRecord,
    *,
    kind: str,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        label = item.get("normalized_label") or item.get("source_span") or kind
        slug = f"{greek_ascii_slug(label)}-{idx}"
        records.append(
            make_context_record(
                recipe,
                kind=kind,
                slug=slug,
                source_span=item.get("source_span") or label,
                normalized_label=label,
                certainty=item.get("certainty", "certain"),
                notes=item.get("notes"),
            )
        )
    return records


def _ingredient_label_keys(item: dict[str, Any]) -> set[str]:
    return {
        normalize_space(value)
        for value in (
            item.get("base_label"),
            item.get("normalized_label"),
            item.get("source_span"),
            item.get("surface_form"),
        )
        if value
    }


def _build_structured_sections(recipe: RecipeRecord, spec: dict[str, Any]) -> dict[str, Any]:
    prep_spec = dict(spec.get("preparation") or {})
    prep_source = prep_spec.get("source_span") or recipe.lemma or recipe.recipe_id
    prep_label = prep_spec.get("normalized_label") or recipe.lemma or recipe.recipe_id

    ingredients: list[dict[str, Any]] = []
    processes: list[dict[str, Any]] = []
    materials: list[dict[str, Any]] = []

    ingredient_label_map: dict[str, list[str]] = defaultdict(list)
    process_label_map: dict[str, list[str]] = defaultdict(list)

    for idx, item in enumerate(spec.get("ingredients", []), start=1):
        label = item.get("normalized_label") or item.get("base_label") or item.get("source_span") or f"ingredient-{idx}"
        record = make_ingredient(
            recipe,
            slug=f"{greek_ascii_slug(label)}-{idx}",
            source_span=item.get("source_span") or label,
            base_label=item.get("base_label") or label,
            normalized_label=item.get("normalized_label") or label,
            alternative_set_id=item.get("alternative_set_id"),
            certainty=item.get("certainty", "certain"),
            quantities=[normalize_quantity_record(dict(value)) for value in item.get("quantities", [])],
            qualifiers=[dict(value) for value in item.get("qualifiers", [])],
            notes=item.get("notes"),
        )
        record["_pending_process_labels"] = [normalize_space(value) for value in item.get("linked_process_labels", [])]
        for key in _ingredient_label_keys(record):
            ingredient_label_map[key].append(record["ingredient_id"])
        ingredients.append(record)

    for idx, item in enumerate(spec.get("processes", []), start=1):
        label = item.get("normalized_label") or item.get("source_span") or f"process-{idx}"
        record = make_process(
            recipe,
            slug=f"{greek_ascii_slug(label)}-{idx}",
            source_span=item.get("source_span") or label,
            normalized_label=label,
            target_type=item.get("target_type", "recipe"),
            quantities=[normalize_quantity_record(dict(value)) for value in item.get("quantities", [])],
            qualifiers=[dict(value) for value in item.get("qualifiers", [])],
            certainty=item.get("certainty", "certain"),
            notes=item.get("notes"),
        )
        process_label_map[normalize_space(label)].append(record["process_id"])
        record["_pending_target_labels"] = [normalize_space(value) for value in item.get("target_labels", [])]
        processes.append(record)

    for record in ingredients:
        pending = record.pop("_pending_process_labels", [])
        linked_ids: list[str] = []
        for label in pending:
            linked_ids.extend(process_label_map.get(label, []))
        record["linked_process_ids"] = linked_ids

    for record in processes:
        pending = record.pop("_pending_target_labels", [])
        if record["target_type"] == "ingredient":
            target_ids: list[str] = []
            for label in pending:
                target_ids.extend(ingredient_label_map.get(label, []))
            record["target_ids"] = target_ids
        else:
            record["target_ids"] = []

    for idx, item in enumerate(spec.get("materials", []), start=1):
        label = item.get("normalized_label") or item.get("source_span") or f"material-{idx}"
        materials.append(
            make_material(
                recipe,
                slug=f"{greek_ascii_slug(label)}-{idx}",
                source_span=item.get("source_span") or label,
                normalized_label=label,
                role=item.get("role", "uncertain_material"),
                certainty=item.get("certainty", "certain"),
                quantities=[normalize_quantity_record(dict(value)) for value in item.get("quantities", [])],
                qualifiers=[dict(value) for value in item.get("qualifiers", [])],
                notes=item.get("notes"),
            )
        )

    return {
        "preparation": make_preparation(
            recipe,
            prep_source,
            prep_label,
            qualifiers=[dict(value) for value in prep_spec.get("qualifiers", [])],
            regimen_notes=[dict(value) for value in prep_spec.get("regimen_notes", [])],
            certainty=prep_spec.get("certainty", "certain"),
            notes=prep_spec.get("notes"),
        ),
        "ingredients": ingredients,
        "processes": processes,
        "materials": materials,
        "people": _reference_records_from_specs(recipe, kind="person", items=spec.get("people", [])),
        "places": _reference_records_from_specs(recipe, kind="place", items=spec.get("places", [])),
        "uses": [
            make_use(
                recipe,
                slug=f"{greek_ascii_slug(item.get('source_span') or item.get('snippet') or f'use-{idx}')}-{idx}",
                category=item.get("category", "other"),
                source_span=item.get("source_span") or item.get("snippet") or "use",
                snippet=item.get("snippet") or item.get("source_span") or "use",
                certainty=item.get("certainty", "certain"),
                notes=item.get("notes"),
            )
            for idx, item in enumerate(spec.get("uses", []), start=1)
        ],
        "preparation_names": _reference_records_from_specs(
            recipe, kind="preparation_name", items=spec.get("preparation_names", [])
        ),
        "other_preparations_mentioned": _reference_records_from_specs(
            recipe, kind="reference", items=spec.get("other_preparations_mentioned", [])
        ),
        "works_mentioned": _reference_records_from_specs(
            recipe, kind="work", items=spec.get("works_mentioned", [])
        ),
    }


def _default_structured_sections(recipe: RecipeRecord, authority: AuthorityRecipe) -> dict[str, Any]:
    label_items = authority.groups.get("labels", [])
    label_source = label_items[0].surface_form if label_items else (recipe.lemma or authority.authority_lemma)
    label_norm = label_items[0].normalized_label if label_items else (recipe.lemma or authority.authority_lemma)

    ingredients = [
        make_ingredient(
            recipe,
            slug=f"{greek_ascii_slug(item.normalized_label)}-{idx}",
            source_span=item.surface_form,
            base_label=item.normalized_label,
            normalized_label=item.normalized_label,
        )
        for idx, item in enumerate(authority.groups.get("ingredients", []), start=1)
    ]
    processes = [
        make_process(
            recipe,
            slug=f"{greek_ascii_slug(item.normalized_label)}-{idx}",
            source_span=item.surface_form,
            normalized_label=item.normalized_label,
        )
        for idx, item in enumerate(authority.groups.get("processes", []), start=1)
    ]
    materials = [
        make_material(
            recipe,
            slug=f"{greek_ascii_slug(item.normalized_label)}-{idx}",
            source_span=item.surface_form,
            normalized_label=item.normalized_label,
            role="tool",
        )
        for idx, item in enumerate(authority.groups.get("tools", []), start=1)
    ]

    return {
        "preparation": make_preparation(recipe, label_source, label_norm),
        "ingredients": ingredients,
        "processes": processes,
        "materials": materials,
        "people": _reference_records(recipe, kind="person", items=authority.groups.get("people", [])),
        "places": _reference_records(recipe, kind="place", items=authority.groups.get("places", [])),
        "uses": [],
        "preparation_names": _reference_records(
            recipe, kind="preparation_name", items=authority.groups.get("preparation_names", [])
        ),
        "other_preparations_mentioned": _reference_records(
            recipe,
            kind="reference",
            items=authority.groups.get("other_preparations_mentioned", []),
        ),
        "works_mentioned": _reference_records(
            recipe, kind="work", items=authority.groups.get("works_mentioned", [])
        ),
    }


def _build_override_sections(recipe: RecipeRecord, override: dict[str, Any]) -> dict[str, Any]:
    built: dict[str, Any] = {}

    ingredient_lookup: dict[str, str] = {}
    process_lookup: dict[str, str] = {}
    ingredients: list[dict[str, Any]] = []
    processes: list[dict[str, Any]] = []
    materials: list[dict[str, Any]] = []
    people: list[dict[str, Any]] = []
    places: list[dict[str, Any]] = []
    uses: list[dict[str, Any]] = []

    for spec in override.get("ingredients", []):
        record = make_ingredient(
            recipe,
            slug=spec["slug"],
            source_span=spec["source_span"],
            base_label=spec["base_label"],
            normalized_label=spec.get("normalized_label"),
            alternative_set_id=spec.get("alternative_set_id"),
            certainty=spec.get("certainty", "certain"),
            quantities=[normalize_quantity_record(dict(item)) for item in spec.get("quantities", [])],
            qualifiers=[dict(item) for item in spec.get("qualifiers", [])],
            notes=spec.get("notes"),
        )
        ingredient_lookup[spec["slug"]] = record["ingredient_id"]
        record["_pending_linked_process_slugs"] = list(spec.get("linked_process_slugs", []))
        ingredients.append(record)

    for spec in override.get("processes", []):
        record = make_process(
            recipe,
            slug=spec["slug"],
            source_span=spec["source_span"],
            normalized_label=spec["normalized_label"],
            target_type=spec.get("target_type", "recipe"),
            quantities=[normalize_quantity_record(dict(item)) for item in spec.get("quantities", [])],
            qualifiers=[dict(item) for item in spec.get("qualifiers", [])],
            certainty=spec.get("certainty", "certain"),
            notes=spec.get("notes"),
        )
        process_lookup[spec["slug"]] = record["process_id"]
        record["_pending_target_slugs"] = list(spec.get("target_slugs", []))
        processes.append(record)

    for record in ingredients:
        pending = record.pop("_pending_linked_process_slugs", [])
        record["linked_process_ids"] = [process_lookup[slug] for slug in pending if slug in process_lookup]

    for record in processes:
        pending = record.pop("_pending_target_slugs", [])
        if record["target_type"] == "ingredient":
            record["target_ids"] = [ingredient_lookup[slug] for slug in pending if slug in ingredient_lookup]
        else:
            record["target_ids"] = []

    for spec in override.get("materials", []):
        materials.append(
            make_material(
                recipe,
                slug=spec["slug"],
                source_span=spec["source_span"],
                normalized_label=spec["normalized_label"],
                role=spec["role"],
                certainty=spec.get("certainty", "certain"),
                quantities=[normalize_quantity_record(dict(item)) for item in spec.get("quantities", [])],
                qualifiers=[dict(item) for item in spec.get("qualifiers", [])],
                notes=spec.get("notes"),
            )
        )
    for spec in override.get("people", []):
        people.append(
            make_context_record(
                recipe,
                kind="person",
                slug=spec["slug"],
                source_span=spec["source_span"],
                normalized_label=spec["normalized_label"],
                certainty=spec.get("certainty", "certain"),
                notes=spec.get("notes"),
            )
        )
    for spec in override.get("places", []):
        places.append(
            make_context_record(
                recipe,
                kind="place",
                slug=spec["slug"],
                source_span=spec["source_span"],
                normalized_label=spec["normalized_label"],
                certainty=spec.get("certainty", "certain"),
                notes=spec.get("notes"),
            )
        )
    for spec in override.get("uses", []):
        uses.append(
            make_use(
                recipe,
                slug=spec["slug"],
                category=spec["category"],
                source_span=spec["source_span"],
                snippet=spec["snippet"],
                certainty=spec.get("certainty", "certain"),
                notes=spec.get("notes"),
            )
        )

    if "ingredients" in override:
        built["ingredients"] = ingredients
    if "processes" in override:
        built["processes"] = processes
    if "materials" in override:
        built["materials"] = materials
    if "people" in override:
        built["people"] = people
    if "places" in override:
        built["places"] = places
    if "uses" in override:
        built["uses"] = uses
    return built


def _flatten_entities(payload: dict[str, Any]) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    preparation = payload.get("preparation")
    if preparation:
        entities.append(
            {
                "entity_urn": preparation["preparation_urn"],
                "entity_type": "label",
                "surface_form": preparation["surface_form"],
                "normalized_label": preparation["normalized_label"],
            }
        )
    for item in payload.get("ingredients", []):
        entities.append(
            {
                "entity_urn": item["ingredient_urn"],
                "entity_type": "ingredient",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("processes", []):
        entities.append(
            {
                "entity_urn": item["process_urn"],
                "entity_type": "process",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("materials", []):
        entities.append(
            {
                "entity_urn": item["material_urn"],
                "entity_type": "material",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("people", []):
        entities.append(
            {
                "entity_urn": item["person_urn"],
                "entity_type": "person",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("places", []):
        entities.append(
            {
                "entity_urn": item["place_urn"],
                "entity_type": "place",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("preparation_names", []):
        entities.append(
            {
                "entity_urn": item["preparation_name_urn"],
                "entity_type": "preparation_name",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("other_preparations_mentioned", []):
        entities.append(
            {
                "entity_urn": item["reference_urn"],
                "entity_type": "preparation_reference",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    for item in payload.get("works_mentioned", []):
        entities.append(
            {
                "entity_urn": item["work_urn"],
                "entity_type": "work",
                "surface_form": item["surface_form"],
                "normalized_label": item["normalized_label"],
            }
        )
    return entities


def build_review_provenance(
    recipe: RecipeRecord,
    *,
    authority_source: str,
    authority_lemma: str | None = None,
    authority_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metadata = authority_metadata or default_authority_metadata(build_version=None)
    return {
        "authority_source": authority_source,
        "authority_recipe_id": recipe.recipe_id,
        "authority_lemma": authority_lemma or (recipe.lemma or recipe.recipe_id),
        "model": AUTHORITY_MODEL,
        "reasoning_effort": AUTHORITY_REASONING,
        "dataset_key": recipe.dataset_key,
        "entity_model_version": metadata["entity_model_version"],
        "authority_version": metadata["authority_version"],
        "prompt_version": metadata["prompt_version"],
        "build_version": metadata["build_version"],
    }


def build_recipe_payload(recipe: RecipeRecord) -> dict[str, Any]:
    structured = load_structured_authority_recipe_map().get(recipe.recipe_id)
    if structured is None:
        raise KeyError(f"Missing structured authority record for {recipe.recipe_id}")

    structured_data = dict(structured.data)
    review_provenance = build_review_provenance(
        recipe,
        authority_source=structured.authority_source,
        authority_lemma=structured_data.get("preparation", {}).get("normalized_label") or recipe.lemma,
        authority_metadata=structured.metadata,
    )
    build_metadata = {
        "builder": "scripts/recipes/build_recipe_entities.py",
        "built_at": structured.metadata["build_version"],
        "source_structured_authority": structured.authority_source,
        "authority_model": AUTHORITY_MODEL,
        "authority_reasoning_effort": AUTHORITY_REASONING,
        "dataset_key": recipe.dataset_key,
        "entity_model_version": structured.metadata["entity_model_version"],
        "authority_version": structured.metadata["authority_version"],
        "prompt_version": structured.metadata["prompt_version"],
        "build_version": structured.metadata["build_version"],
    }
    sections = _build_structured_sections(recipe, structured_data)
    _assign_measure_relationship_metadata(recipe, sections)
    recipe_notes = list(recipe.notes)
    recipe_notes.extend(_copy_notes(structured_data.get("notes")))

    payload = {
        **recipe.to_json(),
        "alignment_status": "pending",
        "alignment_confidence": "pending",
        "alignment_evidence": None,
        "review_status": "reviewed_structured_authority",
        "review_provenance": review_provenance,
        "schema_version": structured.metadata["entity_model_version"],
        "build_metadata": build_metadata,
        "recipe_text_excerpt": sentence_prefix(recipe.text, words=20),
        "preparation": sections["preparation"],
        "ingredients": sections["ingredients"],
        "processes": sections["processes"],
        "materials": sections["materials"],
        "people": sections["people"],
        "places": sections["places"],
        "uses": sections["uses"],
        "preparation_names": sections["preparation_names"],
        "other_preparations_mentioned": sections["other_preparations_mentioned"],
        "works_mentioned": sections["works_mentioned"],
        "notes": recipe_notes,
    }
    payload["entities"] = _flatten_entities(payload)
    return payload


def collect_milestones(text: str) -> list[tuple[str, str, str]]:
    return MILESTONE_RE.findall(text)


def recipe_span_from_milestone(text: str, recipe_id: str) -> str | None:
    xml_id = f'xml:id="rcp-{recipe_id}"'
    idx = text.find(xml_id)
    if idx == -1:
        return None
    start = text.rfind("<milestone", 0, idx)
    if start == -1:
        return None
    next_idx = text.find('<milestone unit="recipe"', idx + len(xml_id))
    end = len(text) if next_idx == -1 else next_idx
    return text[start:end]


def milestone_context(text: str, recipe_id: str, width: int = 180) -> str | None:
    xml_id = f'xml:id="rcp-{recipe_id}"'
    idx = text.find(xml_id)
    if idx == -1:
        return None
    start = max(0, idx - width)
    end = min(len(text), idx + width)
    snippet = text[start:end]
    return normalize_witness_text(snippet)


def ensure_dirs() -> None:
    RECIPE_ENTITY_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    STRUCTURED_AUTHORITY_DIR.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def reset_recipe_caches() -> None:
    load_recipe_entity_file_map.cache_clear()
    load_compact_recipe_entity_groups.cache_clear()
    load_authority_recipe_map.cache_clear()
    load_structured_authority_recipe_map.cache_clear()
    load_structured_authority_dataset_map.cache_clear()
