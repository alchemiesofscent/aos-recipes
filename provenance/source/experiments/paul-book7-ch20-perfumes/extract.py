from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.recipes.common import attach_viewer_entity_groups

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_NS = "{http://www.w3.org/XML/1998/namespace}"
WHITESPACE_RE = re.compile(r"\s+")
HYPHEN_CHARS = ("-", "‐", "‑", "‒", "–", "—", "﹘", "﹣", "－")

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE_XML = REPO_ROOT / "tei/output/tlg0715.tlg001.aos-grc1.cmg9_2.xml"
OUTPUT_JSON = ROOT / "data/paul_book7_ch20_perfumes.json"
OUTPUT_JS = ROOT / "data/paul_book7_ch20_perfumes.js"
QC_REPORT = ROOT / "qc_report.json"


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def tag_name(node: ET.Element) -> str:
    return node.tag.rsplit("}", 1)[-1]


def parse_page_from_xml_id(xml_id: str | None) -> str | None:
    if not xml_id:
        return None
    match = re.search(r"heib-(\d+)-(\d+)(?:-\d+)?$", xml_id)
    if not match:
        return None
    return f"{match.group(1)}.{match.group(2)}"


def strip_trailing_punctuation(text: str) -> str:
    return text.rstrip(" .·;")


def join_flow_text(lines: list[dict[str, object]]) -> str:
    chunks: list[str] = []
    for line in lines:
        text = normalize_space(str(line["text"]))
        if not text:
            continue
        if chunks and bool(line["break_no"]):
            if chunks[-1].endswith(HYPHEN_CHARS):
                chunks[-1] = chunks[-1][:-1]
            chunks[-1] += text
        else:
            chunks.append(text)
    return " ".join(chunks)


def build_lineation(lines: list[dict[str, object]]) -> dict[str, object]:
    pages: list[str] = []
    spans: OrderedDict[str, dict[str, str]] = OrderedDict()
    for line in lines:
        page = str(line["page"])
        if page not in pages:
            pages.append(page)
        if page not in spans:
            spans[page] = {"page": page, "start_line": str(line["line"]), "end_line": str(line["line"])}
        spans[page]["end_line"] = str(line["line"])

    start = lines[0]
    end = lines[-1]
    return {
        "pages": pages,
        "start": {"page": str(start["page"]), "line": str(start["line"]), "xml_id": str(start["xml_id"])},
        "end": {"page": str(end["page"]), "line": str(end["line"]), "xml_id": str(end["xml_id"])},
        "citation": {
            "start": f"{start['page']}.{start['line']}",
            "end": f"{end['page']}.{end['line']}",
        },
        "page_spans": list(spans.values()),
        "lines": lines,
    }


def collect_lines(nodes: list[ET.Element], starting_page: str | None) -> tuple[list[dict[str, object]], str | None]:
    state = {
        "current_page": starting_page,
        "current_line": None,
        "lines": [],
    }

    def flush_line() -> None:
        current = state["current_line"]
        if not current:
            return
        text = normalize_space("".join(current.pop("parts")))
        if text:
            current["text"] = text
            current["citation"] = f"{current['page']}.{current['line']}"
            state["lines"].append(current)
        state["current_line"] = None

    def append_text(text: str | None) -> None:
        if not text:
            return
        if not state["current_line"]:
            return
        cleaned = WHITESPACE_RE.sub(" ", text)
        if cleaned.strip():
            state["current_line"]["parts"].append(cleaned)

    def walk(node: ET.Element) -> None:
        append_text(node.text)
        for child in node:
            name = tag_name(child)
            if name == "pb":
                pb_page = child.get("n")
                if pb_page:
                    state["current_page"] = pb_page
            elif name == "lb":
                flush_line()
                lb_page = parse_page_from_xml_id(child.get(f"{XML_NS}id")) or state["current_page"]
                if lb_page:
                    state["current_page"] = lb_page
                state["current_line"] = {
                    "page": state["current_page"],
                    "line": child.get("n"),
                    "xml_id": child.get(f"{XML_NS}id"),
                    "break_no": child.get("break") == "no",
                    "parts": [],
                }
            else:
                walk(child)
            append_text(child.tail)

    for node in nodes:
        walk(node)
    flush_line()
    return state["lines"], state["current_page"]


def extract_section(section: ET.Element, chapter_name: str, current_page: str | None) -> tuple[dict[str, object], str | None]:
    head = section.find("tei:head", NS)
    body_nodes = [child for child in section if tag_name(child) != "head"]

    head_lines, current_page = collect_lines([head], current_page) if head is not None else ([], current_page)
    body_lines, current_page = collect_lines(body_nodes, current_page)
    section_lines = head_lines + body_lines

    section_n = section.get("n")
    base = section.get(f"{XML_NS}base", "")
    head_text = join_flow_text(head_lines)
    body_text = join_flow_text(body_lines)
    full_text = join_flow_text(section_lines)

    payload = {
        "section": section_n,
        "cts": base.rsplit(":", 1)[-1] if base else None,
        "chapter": "20",
        "book": "7",
        "chapter_name": chapter_name,
        "title": head_text,
        "lemma": strip_trailing_punctuation(head_text) if head_text else None,
        "text": body_text if body_text else full_text,
        "heiberg": build_lineation(section_lines),
    }
    return payload, current_page


def load_target_chapter() -> ET.Element:
    tree = ET.parse(SOURCE_XML)
    root = tree.getroot()
    for chapter in root.findall(".//tei:div[@subtype='chapter']", NS):
        base = chapter.get(f"{XML_NS}base", "")
        if chapter.get("n") == "20" and base.endswith(":7"):
            return chapter
    raise RuntimeError("Could not find Paul of Aegina 7.20 in the source XML.")


def build_output() -> dict[str, object]:
    chapter = load_target_chapter()
    sections = chapter.findall("tei:div", NS)
    current_page: str | None = None

    title_section = next(section for section in sections if section.get("n") == "t")
    title_payload, current_page = extract_section(title_section, "", current_page)
    chapter_name = title_payload["text"]

    proemium: list[dict[str, object]] = []
    perfumes: list[dict[str, object]] = []

    for section in sections:
        n = section.get("n")
        if n == "t":
            continue
        payload, current_page = extract_section(section, chapter_name, current_page)
        if n in {"1", "2", "3"}:
            proemium.append(payload)
        else:
            payload["id"] = f"paul-7-20-{n}"
            perfumes.append(payload)
    perfumes = attach_viewer_entity_groups(perfumes)

    pages = []
    for item in proemium + perfumes:
        for page in item["heiberg"]["pages"]:
            if page not in pages:
                pages.append(page)

    return {
        "source": {
            "xml_file": str(SOURCE_XML.relative_to(REPO_ROOT)),
            "xml_line_range": {"start": 7136, "end": 7481},
            "edition": "Heiberg",
        },
        "work": {
            "author": "Paul of Aegina",
            "work": "Medical Epitome",
            "book": "7",
            "chapter": "20",
            "cts": "urn:cts:greekLit:tlg0715.tlg001.aos-grc1:7.20",
            "chapter_name": chapter_name,
            "page_span": pages,
        },
        "proemium": proemium,
        "perfumes": perfumes,
    }


def build_qc_report(data: dict[str, object]) -> dict[str, object]:
    perfumes = data["perfumes"]
    expected_sections = [str(number) for number in range(4, 39)]
    actual_sections = [entry["section"] for entry in perfumes]
    missing_sections = [section for section in expected_sections if section not in actual_sections]
    entries_missing_text = [entry["section"] for entry in perfumes if not entry["text"]]
    entries_missing_lines = [entry["section"] for entry in perfumes if not entry["heiberg"]["lines"]]
    entries_missing_pages = [entry["section"] for entry in perfumes if not entry["heiberg"]["pages"]]

    return {
        "chapter": "7.20",
        "chapter_name": data["work"]["chapter_name"],
        "proemium_sections": [entry["section"] for entry in data["proemium"]],
        "perfume_count": len(perfumes),
        "expected_perfume_count": 35,
        "expected_sections": expected_sections,
        "actual_sections": actual_sections,
        "missing_sections": missing_sections,
        "entries_missing_text": entries_missing_text,
        "entries_missing_lines": entries_missing_lines,
        "entries_missing_pages": entries_missing_pages,
        "page_span": data["work"]["page_span"],
        "status": "ok"
        if not any([missing_sections, entries_missing_text, entries_missing_lines, entries_missing_pages])
        and len(perfumes) == 35
        else "needs_review",
    }


def main() -> None:
    data = build_output()
    qc = build_qc_report(data)
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT_JSON.write_text(json_text + "\n", encoding="utf-8")
    OUTPUT_JS.write_text(f"window.PAUL_BOOK7_CH20_DATA = {json_text};\n", encoding="utf-8")
    QC_REPORT.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_JS.relative_to(REPO_ROOT)}")
    print(f"Wrote {QC_REPORT.relative_to(REPO_ROOT)}")
    print(f"Perfumes: {qc['perfume_count']}")
    print(f"QC status: {qc['status']}")


if __name__ == "__main__":
    main()
