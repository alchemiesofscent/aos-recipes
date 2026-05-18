from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.recipes.common import VIEWER_ENTITY_GROUPS, attach_viewer_entity_groups

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
WHITESPACE_RE = re.compile(r"\s+")
BARE_NUMERAL_RE = re.compile(r"(?<![\w])\d{1,3}(?![\w])")
HYPHEN_CHARS = ("-", "‐", "‑", "‒", "–", "—", "﹘", "﹣", "－")
SENTENCE_BOUNDARY_RE = re.compile(r"[.;··]")

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE_XML = REPO_ROOT / "tei/raw/tlg0656.tlg001.1st1K-grc1.xml"
OUTPUT_JSON = ROOT / "data/dioscorides_book2_fats.json"
OUTPUT_JS = ROOT / "data/dioscorides_book2_fats.js"
QC_REPORT = ROOT / "qc_report.json"

ENTRY_SPECS: list[dict[str, Any]] = [
    {
        "id": "dioscorides-2-72-boutyron",
        "book": "2",
        "chapter": "72",
        "section": "1-2",
        "lemma": "βούτυρον",
        "chapter_name": "βούτυρον",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [("section", "72", "1"), ("section", "72", "2")],
    },
    {
        "id": "dioscorides-2-72-boutyron-lignys",
        "book": "2",
        "chapter": "72",
        "section": "3",
        "lemma": "λιγνὺς ἐκ βουτύρου",
        "chapter_name": "βούτυρον",
        "entry_kind": "technique",
        "source_kind": "main_text",
        "refs": [("section", "72", "3")],
    },
    {
        "id": "dioscorides-2-74-oisypos",
        "book": "2",
        "chapter": "74",
        "section": "1-2, 4",
        "lemma": "οἴσυπος",
        "chapter_name": "οἴσυπος",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [("section", "74", "1"), ("section", "74", "2"), ("section", "74", "4")],
    },
    {
        "id": "dioscorides-2-74-oisypos-boiled",
        "book": "2",
        "chapter": "74",
        "section": "3",
        "lemma": "οἴσυπος ἑψητός",
        "chapter_name": "οἴσυπος",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [("section", "74", "3")],
    },
    {
        "id": "dioscorides-2-74-oisypos-burned-lignys",
        "book": "2",
        "chapter": "74",
        "section": "5",
        "lemma": "οἴσυπος κεκαυμένος καὶ λιγνύς",
        "chapter_name": "οἴσυπος",
        "entry_kind": "technique",
        "source_kind": "main_text",
        "refs": [("section", "74", "5")],
    },
    {
        "id": "dioscorides-2-76-goose-chicken-stear",
        "book": "2",
        "chapter": "76",
        "section": "1-2",
        "lemma": "στέαρ χήνειον καὶ ὀρνίθειον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section", "76", "1"),
            ("section_span", "76", "2", None, "ἐστι δὲ καὶ ἄλλος τρόπος"),
        ],
    },
    {
        "id": "dioscorides-2-76-rendered-stear-with-salt",
        "book": "2",
        "chapter": "76",
        "section": "2",
        "lemma": "στέαρ τεθεραπευμένον μετὰ ἁλός",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section_span", "76", "2", "ἐστι δὲ καὶ ἄλλος τρόπος", "ὔειον δὲ καὶ ἄρκειον"),
        ],
    },
    {
        "id": "dioscorides-2-76-pig-bear-stear",
        "book": "2",
        "chapter": "76",
        "section": "2-3",
        "lemma": "στέαρ ὔειον καὶ ἄρκειον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section_span", "76", "2", "ὔειον δὲ καὶ ἄρκειον", None),
            ("section", "76", "3"),
        ],
    },
    {
        "id": "dioscorides-2-76-goat-sheep-deer-stear",
        "book": "2",
        "chapter": "76",
        "section": "4-5",
        "lemma": "στέαρ τράγειον καὶ προβάτειον καὶ ἐλάφειον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section", "76", "4"),
            ("section_span", "76", "5", None, "καὶ τοῦ βοείου"),
        ],
    },
    {
        "id": "dioscorides-2-76-ox-stear",
        "book": "2",
        "chapter": "76",
        "section": "5-6",
        "lemma": "στέαρ βόειον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section_span", "76", "5", "καὶ τοῦ βοείου", None),
            ("section_span", "76", "6", None, "τὸ δὲ ταύρειον"),
        ],
    },
    {
        "id": "dioscorides-2-76-bull-stear",
        "book": "2",
        "chapter": "76",
        "section": "6-8",
        "lemma": "στέαρ ταύρειον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section_span", "76", "6", "τὸ δὲ ταύρειον", None),
            ("section", "76", "7"),
            ("section_span", "76", "8", None, "ἀρωματιστέο"),
        ],
    },
    {
        "id": "dioscorides-2-76-aromatized-calf-bull-deer-stear",
        "book": "2",
        "chapter": "76",
        "section": "8-10",
        "lemma": "στέαρ μόσχειον καὶ ταύρειον καὶ ἐλάφειον ἀρωματιστόν",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section_span", "76", "8", "ἀρωματιστέο", None),
            ("section", "76", "9"),
            ("section_span", "76", "10", None, "προστύφεται"),
        ],
    },
    {
        "id": "dioscorides-2-76-aromatic-pretreatment-basic",
        "book": "2",
        "chapter": "76",
        "section": "10",
        "lemma": "πρόστυψις στεάτων πρὸς ἀρώματα",
        "chapter_name": "στέαρ",
        "entry_kind": "technique",
        "source_kind": "main_text",
        "refs": [("section_span", "76", "10", "προστύφεται", None)],
    },
    {
        "id": "dioscorides-2-76-aromatic-pretreatment-lotus",
        "book": "2",
        "chapter": "76",
        "section": "11-12",
        "lemma": "πρόστυψις στεάτων διὰ λωτίνου καρποῦ",
        "chapter_name": "στέαρ",
        "entry_kind": "technique",
        "source_kind": "main_text",
        "refs": [("section", "76", "11"), ("section", "76", "12")],
    },
    {
        "id": "dioscorides-2-76-aromatized-bird-goose-stear",
        "book": "2",
        "chapter": "76",
        "section": "13-14",
        "lemma": "στέαρ ὀρνίθειον καὶ χήνειον ἀρωματιστόν",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section", "76", "13"),
            ("section_span", "76", "14", None, "σαμψουχίζεται"),
        ],
    },
    {
        "id": "dioscorides-2-76-sampsuchized-stear",
        "book": "2",
        "chapter": "76",
        "section": "14-15",
        "lemma": "στέαρ σαμψουχιζόμενον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [
            ("section_span", "76", "14", "σαμψουχίζεται", None),
            ("section", "76", "15"),
        ],
    },
    {
        "id": "dioscorides-2-76-preserved-untreated-stear",
        "book": "2",
        "chapter": "76",
        "section": "16",
        "lemma": "στέαρ ἀθεράπευτον ἄσηπτον",
        "chapter_name": "στέαρ",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "refs": [("section", "76", "16")],
    },
    {
        "id": "dioscorides-2-76-stear-properties-catalogue",
        "book": "2",
        "chapter": "76",
        "section": "17-19",
        "lemma": "δυνάμεις στεάτων",
        "chapter_name": "στέαρ",
        "entry_kind": "properties_catalogue",
        "source_kind": "main_text",
        "refs": [("section", "76", "17"), ("section", "76", "18"), ("section", "76", "19")],
    },
]


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def tag_name(node: ET.Element) -> str:
    return node.tag.rsplit("}", 1)[-1]


def find_book(root: ET.Element, book_n: str) -> ET.Element:
    for div in root.findall(".//tei:div[@type='textpart'][@subtype='book']", NS):
        if div.get("n") == book_n:
            return div
    raise RuntimeError(f"Book {book_n} not found.")


def find_book_chapter(book: ET.Element, chapter_n: str) -> ET.Element:
    for div in book.findall(".//tei:div[@type='textpart'][@subtype='chapter']", NS):
        if div.get("n") == chapter_n:
            return div
    raise RuntimeError(f"Book chapter {chapter_n} not found.")


def find_section(chapter: ET.Element, section_n: str) -> ET.Element:
    for div in chapter.findall("tei:div[@type='textpart']", NS):
        if div.get("n") == section_n:
            return div
    raise RuntimeError(f"Section {section_n} not found in chapter {chapter.get('n')}.")


def collect_fragments(book: ET.Element) -> list[dict[str, Any]]:
    fragments: list[dict[str, Any]] = []
    state: dict[str, str | bool | None] = {
        "current_page": None,
        "current_line": None,
        "break_no": False,
    }

    def append_text(text: str | None, ancestors: tuple[int, ...]) -> None:
        if not text:
            return
        cleaned = normalize_space(text)
        if not cleaned or state["current_line"] is None or state["current_page"] is None:
            return
        fragments.append(
            {
                "page": str(state["current_page"]),
                "line": str(state["current_line"]),
                "break_no": bool(state["break_no"]),
                "text": cleaned,
                "ancestors": ancestors,
            }
        )

    def walk(node: ET.Element, ancestors: tuple[int, ...]) -> None:
        name = tag_name(node)
        if name in {"note", "del"}:
            return
        if name == "pb":
            page = node.get("n")
            if page:
                state["current_page"] = page
                state["current_line"] = "1"
                state["break_no"] = False
            return
        if name == "lb":
            line = node.get("n")
            if line:
                state["current_line"] = line
                state["break_no"] = node.get("break") == "no"
            return

        current_ancestors = ancestors + (id(node),)
        append_text(node.text, current_ancestors)
        for child in node:
            child_name = tag_name(child)
            if child_name in {"note", "del"}:
                append_text(child.tail, current_ancestors)
                continue
            walk(child, current_ancestors)
            append_text(child.tail, current_ancestors)

    walk(book, tuple())
    return fragments


def build_lines(fragments: list[dict[str, Any]], target_ids: set[int]) -> list[dict[str, Any]]:
    grouped: OrderedDict[tuple[str, str], dict[str, Any]] = OrderedDict()
    for fragment in fragments:
        if not target_ids.intersection(fragment["ancestors"]):
            continue
        key = (str(fragment["page"]), str(fragment["line"]))
        if key not in grouped:
            grouped[key] = {
                "page": str(fragment["page"]),
                "line": str(fragment["line"]),
                "break_no": bool(fragment["break_no"]),
                "parts": [],
            }
        grouped[key]["parts"].append(str(fragment["text"]))

    lines: list[dict[str, Any]] = []
    for item in grouped.values():
        raw_text = normalize_space(" ".join(item.pop("parts")))
        if not raw_text:
            continue
        item["raw_text"] = raw_text
        item["text"] = clean_structural_numerals(raw_text)
        item["citation"] = f"{item['page']}.{item['line']}"
        lines.append(item)
    return lines


def join_flow_text(lines: list[dict[str, Any]], *, raw: bool = False) -> str:
    chunks: list[str] = []
    key = "raw_text" if raw else "text"
    for line in lines:
        text = normalize_space(str(line[key]))
        if not text:
            continue
        if chunks and bool(line["break_no"]):
            if chunks[-1].endswith(HYPHEN_CHARS):
                chunks[-1] = chunks[-1][:-1]
            chunks[-1] += text
        else:
            chunks.append(text)
    return " ".join(chunks)


def clean_structural_numerals(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start, end = match.span()
        before = text[max(0, start - 4) : start]
        after = text[end : min(len(text), end + 1)]
        if re.search(r"\([IVXLCDM]+\s*$", before) and after == ")":
            return match.group(0)
        return " "

    cleaned = BARE_NUMERAL_RE.sub(replace, text)
    cleaned = re.sub(r"\s+([,.;··:])", r"\1", cleaned)
    return normalize_space(cleaned)


def slice_between(text: str, start_phrase: str | None, end_phrase: str | None) -> str:
    start = 0
    end = len(text)
    if start_phrase:
        start = text.find(start_phrase)
        if start == -1:
            raise RuntimeError(f"Could not find start phrase: {start_phrase}")
    if end_phrase:
        end = text.find(end_phrase, start)
        if end == -1:
            raise RuntimeError(f"Could not find end phrase: {end_phrase}")
    return normalize_space(text[start:end])


def line_overlaps_text(line: dict[str, Any], sliced_raw_text: str) -> bool:
    raw_line = str(line["raw_text"])
    cleaned_line = str(line["text"])
    return raw_line in sliced_raw_text or cleaned_line in clean_structural_numerals(sliced_raw_text)


def resolve_ref(book: ET.Element, fragments: list[dict[str, Any]], ref: tuple[Any, ...]) -> dict[str, Any]:
    kind = ref[0]
    if kind not in {"section", "section_span"}:
        raise RuntimeError(f"Unknown ref kind: {kind}")
    chapter_n, section_n = str(ref[1]), str(ref[2])
    section = find_section(find_book_chapter(book, chapter_n), section_n)
    lines = build_lines(fragments, {id(section)})
    if not lines:
        raise RuntimeError(f"No lineation found for chapter {chapter_n} section {section_n}")

    raw_text = join_flow_text(lines, raw=True)
    if kind == "section_span":
        raw_text = slice_between(raw_text, ref[3], ref[4])
        matching_lines = [line for line in lines if line_overlaps_text(line, raw_text)]
        lines = matching_lines or lines
    text = clean_structural_numerals(raw_text)
    return {
        "chapter": chapter_n,
        "section": section_n,
        "raw_text": raw_text,
        "text": text,
        "lines": lines,
    }


def snap_marker_offset(text: str, offset: int) -> int:
    candidates = [0]
    candidates.extend(match.end() for match in SENTENCE_BOUNDARY_RE.finditer(text))
    candidates.append(len(text))
    return min(candidates, key=lambda candidate: (abs(candidate - offset), candidate))


def build_section_markers(segments: list[dict[str, Any]], combined_text: str) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    offset = 0
    seen: set[tuple[str, str]] = set()
    for segment in segments:
        key = (segment["chapter"], segment["section"])
        if key in seen:
            offset += len(segment["text"]) + 1
            continue
        seen.add(key)
        raw = segment["raw_text"]
        token_match = re.search(rf"(?<![\w]){re.escape(segment['section'])}(?![\w])", raw)
        raw_token = token_match.group(0) if token_match else None
        marker_offset = snap_marker_offset(combined_text, offset)
        markers.append(
            {
                "chapter": segment["chapter"],
                "section": segment["section"],
                "label": f"§{segment['section']}",
                "raw_token": raw_token,
                "offset": marker_offset,
            }
        )
        offset += len(segment["text"]) + 1
    return markers


def build_lineation(lines: list[dict[str, Any]]) -> dict[str, Any]:
    pages: list[str] = []
    spans: OrderedDict[str, dict[str, str]] = OrderedDict()
    cleaned_lines: list[dict[str, Any]] = []
    for line in lines:
        line = dict(line)
        page = str(line["page"])
        if page not in pages:
            pages.append(page)
        if page not in spans:
            spans[page] = {"page": page, "start_line": str(line["line"]), "end_line": str(line["line"])}
        spans[page]["end_line"] = str(line["line"])
        cleaned_lines.append(line)

    start = cleaned_lines[0]
    end = cleaned_lines[-1]
    return {
        "pages": pages,
        "start": {"page": str(start["page"]), "line": str(start["line"])},
        "end": {"page": str(end["page"]), "line": str(end["line"])},
        "citation": {"start": f"{start['page']}.{start['line']}", "end": f"{end['page']}.{end['line']}"},
        "page_spans": list(spans.values()),
        "lines": cleaned_lines,
    }


def dedupe_lines(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for line in lines:
        key = (str(line["page"]), str(line["line"]), str(line["raw_text"]))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(line)
    return deduped


def build_entry(spec: dict[str, Any], fragments: list[dict[str, Any]], book: ET.Element) -> dict[str, Any]:
    segments = [resolve_ref(book, fragments, ref) for ref in spec["refs"]]
    raw_text = normalize_space(" ".join(segment["raw_text"] for segment in segments))
    text = normalize_space(" ".join(segment["text"] for segment in segments))
    lines = dedupe_lines([line for segment in segments for line in segment["lines"]])
    if not text or not lines:
        raise RuntimeError(f"No text or lineation found for {spec['id']}")
    wellmann = build_lineation(lines)
    return {
        "id": spec["id"],
        "entry_kind": spec["entry_kind"],
        "source_kind": spec["source_kind"],
        "lemma": spec["lemma"],
        "book": spec["book"],
        "chapter": spec["chapter"],
        "section": spec.get("section"),
        "chapter_name": spec["chapter_name"],
        "text": text,
        "raw_text": raw_text,
        "section_markers": build_section_markers(segments, text),
        "source_lines": {
            "start": wellmann["citation"]["start"],
            "end": wellmann["citation"]["end"],
        },
        "wellmann": wellmann,
    }


def attach_empty_entity_groups(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for entry in entries:
        entry["derived_recipe_id"] = entry["id"]
        entry["entity_groups"] = {group: [] for group in VIEWER_ENTITY_GROUPS}
    return entries


def build_output(*, skip_entities: bool) -> dict[str, Any]:
    root = ET.parse(SOURCE_XML).getroot()
    book = find_book(root, "2")
    fragments = collect_fragments(book)

    entries = [build_entry(spec, fragments, book) for spec in ENTRY_SPECS]
    entries = attach_empty_entity_groups(entries) if skip_entities else attach_viewer_entity_groups(entries)

    pages: list[str] = []
    for entry in entries:
        for page in entry["wellmann"]["pages"]:
            if page not in pages:
                pages.append(page)
    pages.sort(key=lambda value: int(value))

    return {
        "source": {
            "xml_file": str(SOURCE_XML.relative_to(REPO_ROOT)),
            "edition": "Wellmann",
            "requested_slices": [
                {
                    "label": spec["lemma"],
                    "book": spec["book"],
                    "chapter": spec["chapter"],
                    "section": spec.get("section"),
                    "recipe_id": spec["id"],
                }
                for spec in ENTRY_SPECS
            ],
            "notes": [
                "Book 2 fats slice split into logical preparation and technique units from chapters 72, 74, and 76.",
                "Bare Arabic numerals in the raw witness are treated as structural or note noise and removed from display text, except parenthetical cross-references such as (I 68).",
                "Section markers are stored separately and displayed near sentence boundaries as heuristic navigation aids.",
            ],
        },
        "work": {
            "author": "Dioscorides",
            "work": "De materia medica",
            "book": "2",
            "chapter_span": ["72", "74", "76"],
            "page_span": pages,
        },
        "proemium": [],
        "entries": entries,
    }


def build_qc_report(data: dict[str, Any], *, skip_entities: bool) -> dict[str, Any]:
    entries = data["entries"]
    expected_ids = [spec["id"] for spec in ENTRY_SPECS]
    actual_ids = [entry["id"] for entry in entries]
    missing_ids = [entry_id for entry_id in expected_ids if entry_id not in actual_ids]
    duplicate_ids = sorted({entry_id for entry_id in actual_ids if actual_ids.count(entry_id) > 1})
    missing_text = [entry["id"] for entry in entries if not entry["text"]]
    missing_raw_text = [entry["id"] for entry in entries if not entry["raw_text"]]
    missing_pages = [entry["id"] for entry in entries if not entry["wellmann"]["pages"]]
    missing_lines = [entry["id"] for entry in entries if not entry["wellmann"]["lines"]]
    missing_markers = [entry["id"] for entry in entries if not entry["section_markers"]]
    bare_numerals = [
        entry["id"]
        for entry in entries
        if BARE_NUMERAL_RE.search(re.sub(r"\([IVXLCDM]+\s+\d{1,3}\)", "", entry["text"]))
    ]
    missing_entities = [
        entry["id"]
        for entry in entries
        if not skip_entities and not any(entry.get("entity_groups", {}).get(group) for group in VIEWER_ENTITY_GROUPS)
    ]
    non_monotonic_citations = [
        entry["id"]
        for entry in entries
        if tuple(int(part) for part in entry["wellmann"]["citation"]["start"].split("."))
        > tuple(int(part) for part in entry["wellmann"]["citation"]["end"].split("."))
    ]
    status = "ok"
    if any(
        [
            missing_ids,
            duplicate_ids,
            missing_text,
            missing_raw_text,
            missing_pages,
            missing_lines,
            missing_markers,
            bare_numerals,
            non_monotonic_citations,
        ]
    ):
        status = "needs_review"
    if len(entries) != len(ENTRY_SPECS):
        status = "needs_review"
    if not skip_entities and missing_entities:
        status = "needs_review"

    return {
        "entry_count": len(entries),
        "expected_entry_count": len(ENTRY_SPECS),
        "expected_ids": expected_ids,
        "actual_ids": actual_ids,
        "missing_ids": missing_ids,
        "duplicate_ids": duplicate_ids,
        "missing_text": missing_text,
        "missing_raw_text": missing_raw_text,
        "missing_pages": missing_pages,
        "missing_lines": missing_lines,
        "missing_markers": missing_markers,
        "bare_numerals": bare_numerals,
        "missing_entities": missing_entities,
        "non_monotonic_citations": non_monotonic_citations,
        "page_span": data["work"]["page_span"],
        "skip_entities": skip_entities,
        "status": status,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Dioscorides Book 2 fats experiment data.")
    parser.add_argument(
        "--skip-entities",
        action="store_true",
        help="Write base viewer data without requiring derived recipe entity records.",
    )
    args = parser.parse_args()

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    data = build_output(skip_entities=args.skip_entities)
    qc = build_qc_report(data, skip_entities=args.skip_entities)
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT_JSON.write_text(json_text + "\n", encoding="utf-8")
    OUTPUT_JS.write_text(f"window.DIOSCORIDES_BOOK2_FATS_DATA = {json_text};\n", encoding="utf-8")
    QC_REPORT.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_JS.relative_to(REPO_ROOT)}")
    print(f"Wrote {QC_REPORT.relative_to(REPO_ROOT)}")
    print(f"Entries: {qc['entry_count']}")
    print(f"QC status: {qc['status']}")


if __name__ == "__main__":
    main()
