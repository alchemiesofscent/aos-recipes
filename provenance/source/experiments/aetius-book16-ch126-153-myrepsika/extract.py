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
WHITESPACE_RE = re.compile(r"\s+")
HYPHEN_CHARS = ("-", "‐", "‑", "‒", "–", "—", "﹘", "﹣", "－")

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE_XML = REPO_ROOT / "tei/raw/tlg0718016.xml"
OUTPUT_JSON = ROOT / "data/aetius_book16_ch126_153_myrepsika.json"
OUTPUT_JS = ROOT / "data/aetius_book16_ch126_153_myrepsika.js"
QC_REPORT = ROOT / "qc_report.json"

CTS_BASE = "urn:cts:greekLit:tlg0718.tlg016.aos-grc1"
START_PAGE = 161
START_LINE = 7

PART_TITLE = "σκευασίαι μύρων, μοσχάτων, κονδίτων, οἰνανθαρίων, θυμιαμάτων καὶ ἑτέρων τινῶν μυρεψικῶν"
PART_TITLE_SELECTORS = ["t1", "t2"]
EXPECTED_ENTRY_COUNT = 44
EXPECTED_CHAPTERS = [str(number) for number in range(126, 154)]
EXPECTED_TITLE_ONLY_IDS: list[str] = []
EXPECTED_MULTI_UNIT_COUNTS = {"127": 3, "130": 3, "131": 3, "133": 2, "134": 2, "137": 3, "138": 3, "144": 2, "146": 2}
RECOVERED_BODY_CHAPTERS = ["127", "128", "129", "132", "135", "136", "138", "140", "141", "143", "144", "145", "148", "149", "150", "152"]

CHAPTER_SPECS = {
    126: {
        "chapter_name": "ξηρόφρυκτον ὃ καλοῦσι βερεθρίας · ἄλλο μοσχάτον · σκευασία ἀραβικῶν ἢ λαιῶν",
        "part_title_selectors": PART_TITLE_SELECTORS,
        "unit_specs": [
            {"lemma": "ξηρόφρυκτον ὃ καλοῦσι βερεθρίας", "title_selectors": ["t3"], "body_ranges": [{"start": "1", "end": "3"}]},
            {"lemma": "ἄλλο μοσχάτον", "title_selectors": ["4"], "body_ranges": [{"start": "5", "end": "8"}]},
            {"lemma": "σκευασία ἀραβικῶν ἢ λαιῶν", "title_selectors": ["9"], "body_ranges": [{"start": "10", "end": "17"}]},
        ],
    },
    127: {
        "chapter_name": "ῥοδάτον ξηρόμυρον · ἄλλο ξηρόμυρον · ἄλλο ξηρόμυρον φρυκτόν",
        "unit_specs": [
            {
                "lemma": "ῥοδάτον ξηρόμυρον",
                "title_selectors": ["t"],
                "body_ranges": [{"start": "1", "end": "2", "end_before": "Ἄλλο ξηρόμυρον."}],
            },
            {
                "lemma": "ἄλλο ξηρόμυρον",
                "title_selectors": [{"line": "2", "match": "Ἄλλο ξηρόμυρον."}],
                "body_ranges": [{"start": "2", "start_after": "Ἄλλο ξηρόμυρον.", "end": "5", "end_before": "Ἄλλο ξηρόμυρον φρυκτόν."}],
            },
            {
                "lemma": "ἄλλο ξηρόμυρον φρυκτόν",
                "title_selectors": [{"line": "5", "match": "Ἄλλο ξηρόμυρον φρυκτόν."}],
                "body_ranges": [{"start": "5", "start_after": "Ἄλλο ξηρόμυρον φρυκτόν.", "end": "6"}],
            },
        ],
    },
    128: {
        "chapter_name": "ἄλλο ξηρόμυρον τὸ καλούμενον λευκόφυλλον, ᾧ χρῶνται εἰς τοὺς τραχήλους καὶ ἐπὶ τὰς μασχάλας",
        "unit_specs": [
            {
                "lemma": "ἄλλο ξηρόμυρον τὸ καλούμενον λευκόφυλλον, ᾧ χρῶνται εἰς τοὺς τραχήλους καὶ ἐπὶ τὰς μασχάλας",
                "title_selectors": ["t1", "t2"],
                "body_ranges": [{"start": "1", "end": "4"}],
            }
        ],
    },
    129: {
        "chapter_name": "ὑγρομύρου σκευασία ᾧ χρῶνται εἰς τὰ ὦτα γυναῖκες",
        "unit_specs": [{"lemma": "ὑγρομύρου σκευασία ᾧ χρῶνται εἰς τὰ ὦτα γυναῖκες", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]}],
    },
    130: {
        "chapter_name": "ἐλαίου σάλκα σκευασία πολυτελής · πρώτη ἕψησις · δευτέρα ἕψησις · τρίτη ἕψησις · ὑγρομύρου σκευασία · λευκοφύλλου σκευασία ἤτοι ξηρομύρου λευκοῦ",
        "unit_specs": [
            {
                "lemma": "ἐλαίου σάλκα σκευασία πολυτελής",
                "title_selectors": ["t", "1", "4", "7"],
                "body_ranges": [{"start": "2", "end": "12"}],
                "subsection_specs": [
                    {"title": "πρώτη ἕψησις", "title_selectors": ["1"], "body_ranges": [{"start": "2", "end": "3"}]},
                    {"title": "δευτέρα ἕψησις", "title_selectors": ["4"], "body_ranges": [{"start": "5", "end": "6"}]},
                    {"title": "τρίτη ἕψησις", "title_selectors": ["7"], "body_ranges": [{"start": "8", "end": "12"}]},
                ],
            },
            {"lemma": "ὑγρομύρου σκευασία", "title_selectors": ["13"], "body_ranges": [{"start": "14", "end": "18"}]},
            {"lemma": "λευκοφύλλου σκευασία ἤτοι ξηρομύρου λευκοῦ", "title_selectors": ["19"], "body_ranges": [{"start": "20", "end": "22"}]},
        ],
    },
    131: {
        "chapter_name": "φουλιάτου σκευασία · ἄλλη γραφὴ φουλιάτου · ἐκ τῶν Ὠρειβασίου φουλιάτου σκευασία",
        "unit_specs": [
            {"lemma": "φουλιάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]},
            {"lemma": "ἄλλη γραφὴ φουλιάτου", "title_selectors": ["4"], "body_ranges": [{"start": "5", "end": "8"}]},
            {"lemma": "ἐκ τῶν Ὠρειβασίου φουλιάτου σκευασία", "title_selectors": ["9"], "body_ranges": [{"start": "10", "end": "17"}]},
        ],
    },
    132: {
        "chapter_name": "σπεκάτου σκευασία",
        "unit_specs": [{"lemma": "σπεκάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "4"}]}],
    },
    133: {
        "chapter_name": "οἰνανθαρίου σκευασία · ἑτέρα οἰνανθαρίου σκευασία",
        "unit_specs": [
            {"lemma": "οἰνανθαρίου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "4"}]},
            {"lemma": "ἑτέρα οἰνανθαρίου σκευασία", "title_selectors": ["5"], "body_ranges": [{"start": "6", "end": "21"}]},
        ],
    },
    134: {
        "chapter_name": "ἀψινθάτου ἤτοι ῥοδαψινθάτου ὑγιεινοῦ σκευασία καλλίστη · ῥοδάτου ὑγιεινοῦ σκευασία",
        "unit_specs": [
            {
                "lemma": "ἀψινθάτου ἤτοι ῥοδαψινθάτου ὑγιεινοῦ σκευασία καλλίστη",
                "title_selectors": ["t1", "t2"],
                "body_ranges": [{"start": "1", "end": "4"}],
            },
            {"lemma": "ῥοδάτου ὑγιεινοῦ σκευασία", "title_selectors": ["5"], "body_ranges": [{"start": "6", "end": "12"}]},
        ],
    },
    135: {
        "chapter_name": "ῥοδάτου σκευασία",
        "unit_specs": [{"lemma": "ῥοδάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "6"}]}],
    },
    136: {
        "chapter_name": "κονδίτου καθαρτικοῦ σκευασία ἐπὶ τῶν φλεγματικῶν, χρῶ δὲ τούτῳ ἐν χειμῶνι",
        "unit_specs": [
            {
                "lemma": "κονδίτου καθαρτικοῦ σκευασία ἐπὶ τῶν φλεγματικῶν, χρῶ δὲ τούτῳ ἐν χειμῶνι",
                "title_selectors": ["t1", "t2"],
                "body_ranges": [{"start": "1", "end": "10"}],
            }
        ],
    },
    137: {
        "chapter_name": "ἀψινθάτου σκευασία · σεσελίτου σκευασία · ἀνισάτου σκευασία",
        "unit_specs": [
            {"lemma": "ἀψινθάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]},
            {"lemma": "σεσελίτου σκευασία", "title_selectors": ["4"], "body_ranges": [{"start": "5", "end": "6"}]},
            {"lemma": "ἀνισάτου σκευασία", "title_selectors": ["7"], "body_ranges": [{"start": "8", "end": "9"}]},
        ],
    },
    138: {
        "chapter_name": "μαστιχάτου κυμινάτου σκευασία · κιτράτου σκευασία · ἀπιάτου σκευασία",
        "unit_specs": [
            {"lemma": "μαστιχάτου κυμινάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "2"}]},
            {"lemma": "κιτράτου σκευασία", "title_selectors": ["3"], "body_ranges": [{"start": "4", "end": "6"}]},
            {"lemma": "ἀπιάτου σκευασία", "title_selectors": ["7"], "body_ranges": [{"start": "8", "end": "10"}]},
        ],
    },
    139: {
        "chapter_name": "ῥοδομήλου σκευασία",
        "unit_specs": [{"lemma": "ῥοδομήλου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "7"}]}],
    },
    140: {
        "chapter_name": "μουστακίων σκευασία",
        "unit_specs": [{"lemma": "μουστακίων σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "4"}]}],
    },
    141: {
        "chapter_name": "γάρου νηστικοῦ σκευασία",
        "unit_specs": [{"lemma": "γάρου νηστικοῦ σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]}],
    },
    142: {
        "chapter_name": "θυμιάματος μοσχάτου σκευασία",
        "unit_specs": [{"lemma": "θυμιάματος μοσχάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "18"}]}],
    },
    143: {
        "chapter_name": "θυμιάματος τοῦ βασιλικοῦ σκευασία",
        "unit_specs": [{"lemma": "θυμιάματος τοῦ βασιλικοῦ σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "4"}]}],
    },
    144: {
        "chapter_name": "θυμιάματος μοσχάτου Θεοπέμπτου σκευασία · ἄλλου θυμιάματος μοσχάτου σκευασία",
        "unit_specs": [
            {"lemma": "θυμιάματος μοσχάτου Θεοπέμπτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]},
            {"lemma": "ἄλλου θυμιάματος μοσχάτου σκευασία", "title_selectors": ["4"], "body_ranges": [{"start": "5", "end": "8"}]},
        ],
    },
    145: {
        "chapter_name": "θυμιάματος καλοῦ ῥοδάτου σκευασία",
        "unit_specs": [{"lemma": "θυμιάματος καλοῦ ῥοδάτου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]}],
    },
    146: {
        "chapter_name": "μοσχάτου ἐν τῇ ἐκκλησίᾳ καπνιζομένου σκευασία · θυμιάματος μυρεψικοῦ σκευασία",
        "unit_specs": [
            {"lemma": "μοσχάτου ἐν τῇ ἐκκλησίᾳ καπνιζομένου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "9"}]},
            {"lemma": "θυμιάματος μυρεψικοῦ σκευασία", "title_selectors": ["10"], "body_ranges": [{"start": "11", "end": "16"}]},
        ],
    },
    147: {
        "chapter_name": "θυμιάματος μυρεψικοῦ καλοῦ σκευασία",
        "unit_specs": [{"lemma": "θυμιάματος μυρεψικοῦ καλοῦ σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "5"}]}],
    },
    148: {
        "chapter_name": "θυμιάματος ἐράνου σκευασία",
        "unit_specs": [{"lemma": "θυμιάματος ἐράνου σκευασία", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]}],
    },
    149: {
        "chapter_name": "θυμίαμα τῆς κυρίας Ῥωμύλου",
        "unit_specs": [{"lemma": "θυμίαμα τῆς κυρίας Ῥωμύλου", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "3"}]}],
    },
    150: {
        "chapter_name": "θυμίαμα ῥοδάτον τοῦ ἐμβολάρχου",
        "unit_specs": [{"lemma": "θυμίαμα ῥοδάτον τοῦ ἐμβολάρχου", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "6"}]}],
    },
    151: {
        "chapter_name": "θυμίαμα ῥοδάτον ἐπισκόπου Παμφύλου",
        "unit_specs": [{"lemma": "θυμίαμα ῥοδάτον ἐπισκόπου Παμφύλου", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "7"}]}],
    },
    152: {
        "chapter_name": "θυμίαμα μυρεψικὸν ἡ φυκοτύχη",
        "unit_specs": [{"lemma": "θυμίαμα μυρεψικὸν ἡ φυκοτύχη", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "6"}]}],
    },
    153: {
        "chapter_name": "νεκροῦ σμύρνησις",
        "unit_specs": [{"lemma": "νεκροῦ σμύρνησις", "title_selectors": ["t"], "body_ranges": [{"start": "1", "end": "2"}]}],
    },
}


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def clone_line(line: dict[str, object], text: str | None = None) -> dict[str, object]:
    cloned = {key: value for key, value in line.items() if key not in {"raw_n", "has_label"}}
    if text is not None:
        cloned["text"] = text
    return cloned


def join_flow_text(lines: list[dict[str, object]]) -> str:
    chunks: list[str] = []
    for line in lines:
        text = normalize_space(str(line["text"]))
        if not text:
            continue
        if chunks and chunks[-1].endswith(HYPHEN_CHARS):
            chunks[-1] = chunks[-1][:-1] + text
        else:
            chunks.append(text)
    return " ".join(chunks)


def build_lineation(lines: list[dict[str, object]]) -> dict[str, object]:
    if not lines:
        raise RuntimeError("Cannot build lineation from an empty line set.")

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
        "citation": {"start": f"{start['page']}.{start['line']}", "end": f"{end['page']}.{end['line']}"},
        "page_spans": list(spans.values()),
        "lines": lines,
    }


def load_raw_chapters() -> dict[int, dict[str, object]]:
    tree = ET.parse(SOURCE_XML)
    root = tree.getroot()

    chapters: dict[int, dict[str, object]] = {}
    page = START_PAGE
    line_number = START_LINE

    chapter_elements = root.findall(".//tei:div[@type='Chapter']", NS)
    target_elements = [chapter for chapter in chapter_elements if chapter.get("n", "").isdigit() and 126 <= int(chapter.get("n", "0")) <= 153]
    expected_numbers = list(range(126, 154))
    actual_numbers = [int(chapter.get("n", "0")) for chapter in target_elements]
    if actual_numbers != expected_numbers:
        raise RuntimeError(f"Unexpected raw chapter sequence: {actual_numbers}")

    for chapter in target_elements:
        chapter_number = int(chapter.get("n", "0"))
        chapter_lines: list[dict[str, object]] = []
        order: list[str] = []

        for raw_line in chapter.findall("tei:l", NS):
            key = raw_line.get("n")
            if key is None:
                raise RuntimeError(f"Chapter {chapter_number} has a line without @n.")
            text = normalize_space("".join(raw_line.itertext()))
            if not text:
                raise RuntimeError(f"Chapter {chapter_number} line {key} is empty.")
            line = {
                "raw_n": key,
                "page": str(page),
                "line": str(line_number),
                "xml_id": f"zerv-{page}-{line_number}",
                "citation": f"{page}.{line_number}",
                "text": text,
                "has_label": raw_line.find("tei:label", NS) is not None,
            }
            chapter_lines.append(line)
            order.append(key)

            if raw_line.find(".//tei:pb", NS) is not None:
                page += 1
                line_number = 1
            else:
                line_number += 1

        chapters[chapter_number] = {
            "chapter": str(chapter_number),
            "cts": f"{CTS_BASE}:{chapter_number}",
            "lines": chapter_lines,
            "order": order,
            "line_map": {line["raw_n"]: line for line in chapter_lines},
        }

    return chapters


def select_line_fragment(line: dict[str, object], *, match: str | None = None, after: str | None = None, before: str | None = None) -> dict[str, object] | None:
    text = str(line["text"])

    if match is not None:
        if match not in text:
            raise RuntimeError(f"Missing title match '{match}' in line {line['citation']}: {text}")
        text = match
    else:
        if after is not None:
            if after not in text:
                raise RuntimeError(f"Missing start-after token '{after}' in line {line['citation']}: {text}")
            text = text.split(after, 1)[1]
        if before is not None:
            if before not in text:
                raise RuntimeError(f"Missing end-before token '{before}' in line {line['citation']}: {text}")
            text = text.split(before, 1)[0]

    text = normalize_space(text)
    if not text:
        return None
    return clone_line(line, text=text)


def select_title_fragments(chapter: dict[str, object], selectors: list[object]) -> list[dict[str, object]]:
    fragments: list[dict[str, object]] = []
    line_map = chapter["line_map"]
    for selector in selectors:
        if isinstance(selector, str):
            fragment = select_line_fragment(line_map[selector])
        else:
            fragment = select_line_fragment(
                line_map[selector["line"]],
                match=selector.get("match"),
                after=selector.get("after"),
                before=selector.get("before"),
            )
        if fragment is not None:
            fragments.append(fragment)
    return fragments


def select_body_fragments(chapter: dict[str, object], ranges: list[dict[str, str]]) -> list[dict[str, object]]:
    fragments: list[dict[str, object]] = []
    order = chapter["order"]
    line_map = chapter["line_map"]
    for range_spec in ranges:
        start_index = order.index(range_spec["start"])
        end_index = order.index(range_spec["end"])
        if end_index < start_index:
            raise RuntimeError(f"Invalid range in chapter {chapter['chapter']}: {range_spec}")

        for index in range(start_index, end_index + 1):
            line = line_map[order[index]]
            fragment = select_line_fragment(
                line,
                after=range_spec.get("start_after") if index == start_index else None,
                before=range_spec.get("end_before") if index == end_index else None,
            )
            if fragment is not None:
                fragments.append(fragment)
    return fragments


def make_entry_id(chapter: int, section: str | None) -> str:
    return f"aetius-16-{chapter}" if section is None else f"aetius-16-{chapter}-{section}"


def build_subsections(chapter: dict[str, object], subsection_specs: list[dict[str, object]]) -> list[dict[str, object]]:
    subsections: list[dict[str, object]] = []
    for position, subsection_spec in enumerate(subsection_specs, start=1):
        title_lines = select_title_fragments(chapter, subsection_spec["title_selectors"])
        body_lines = select_body_fragments(chapter, subsection_spec["body_ranges"])
        subsections.append(
            {
                "section": str(position),
                "title": subsection_spec["title"],
                "text": join_flow_text(body_lines),
                "zervos": build_lineation(title_lines + body_lines),
            }
        )
    return subsections


def extract_chapter_entries(chapter: dict[str, object]) -> tuple[dict[str, object], list[dict[str, object]]]:
    chapter_number = int(chapter["chapter"])
    chapter_spec = CHAPTER_SPECS[chapter_number]

    if chapter_number == 126:
        metadata = {
            "part_title": PART_TITLE,
            "part_title_zervos": build_lineation(select_title_fragments(chapter, chapter_spec["part_title_selectors"])),
            "chapter_name": chapter_spec["chapter_name"],
        }
    else:
        metadata = {"chapter_name": chapter_spec["chapter_name"]}

    unit_specs = chapter_spec["unit_specs"]
    requires_sections = len(unit_specs) > 1
    entries: list[dict[str, object]] = []

    for position, unit_spec in enumerate(unit_specs, start=1):
        title_lines = select_title_fragments(chapter, unit_spec["title_selectors"])
        body_lines = select_body_fragments(chapter, unit_spec["body_ranges"])
        unit_lines = title_lines + body_lines

        if not title_lines or not body_lines:
            raise RuntimeError(f"Chapter {chapter_number} unit {position} is missing title or body content.")

        section = str(position) if requires_sections else None
        entry = {
            "id": make_entry_id(chapter_number, section),
            "book": "16",
            "chapter": str(chapter_number),
            "cts": chapter["cts"],
            "lemma": unit_spec["lemma"],
            "chapter_name": chapter_spec["chapter_name"],
            "text": join_flow_text(body_lines),
            "zervos": build_lineation(unit_lines),
        }
        if section is not None:
            entry["section"] = section
        if "subsection_specs" in unit_spec:
            entry["subsections"] = build_subsections(chapter, unit_spec["subsection_specs"])
        entries.append(entry)

    return metadata, entries


def build_output() -> dict[str, object]:
    chapters = load_raw_chapters()
    entries: list[dict[str, object]] = []
    work_metadata: dict[str, object] | None = None

    for chapter_number in range(126, 154):
        chapter_metadata, chapter_entries = extract_chapter_entries(chapters[chapter_number])
        if chapter_number == 126:
            work_metadata = chapter_metadata
        entries.extend(chapter_entries)

    if work_metadata is None:
        raise RuntimeError("Chapter 126 metadata was not extracted.")
    entries = attach_viewer_entity_groups(entries)

    page_span: list[str] = []
    for entry in entries:
        for page in entry["zervos"]["pages"]:
            if page not in page_span:
                page_span.append(page)

    return {
        "source": {
            "xml_file": str(SOURCE_XML.relative_to(REPO_ROOT)),
            "xml_line_range": {"start": 4823, "end": 5218},
            "requested_chapter_range": {"start": "126", "end": "153"},
            "edition": "Zervos",
            "citation_basis": "Reconstructed from raw line flow anchored at Zervos 161.7.",
        },
        "work": {
            "author": "Aëtius of Amida",
            "work": "Libri medicinales",
            "book": "16",
            "cts": f"{CTS_BASE}:16.126-153",
            "part_title": work_metadata["part_title"],
            "part_title_zervos": work_metadata["part_title_zervos"],
            "page_span": page_span,
        },
        "entries": entries,
    }


def build_qc_report(data: dict[str, object]) -> dict[str, object]:
    entries = data["entries"]
    actual_title_only_ids = sorted(entry["id"] for entry in entries if entry.get("title_only"))
    actual_chapters = sorted({entry["chapter"] for entry in entries}, key=int)
    chapter_130 = [entry for entry in entries if entry["id"] == "aetius-16-130-1"]
    chapter_counts: OrderedDict[str, int] = OrderedDict()
    for entry in entries:
        chapter_counts.setdefault(entry["chapter"], 0)
        chapter_counts[entry["chapter"]] += 1

    report = {
        "book": "16",
        "entry_count": len(entries),
        "expected_entry_count": EXPECTED_ENTRY_COUNT,
        "expected_chapters": EXPECTED_CHAPTERS,
        "actual_chapters": actual_chapters,
        "missing_chapters": [chapter for chapter in EXPECTED_CHAPTERS if chapter not in actual_chapters],
        "expected_title_only_ids": EXPECTED_TITLE_ONLY_IDS,
        "actual_title_only_ids": actual_title_only_ids,
        "missing_title_only_ids": [entry_id for entry_id in EXPECTED_TITLE_ONLY_IDS if entry_id not in actual_title_only_ids],
        "entries_missing_lemma": [entry["id"] for entry in entries if not entry.get("lemma")],
        "entries_missing_chapter_name": [entry["id"] for entry in entries if not entry.get("chapter_name")],
        "entries_missing_text": [entry["id"] for entry in entries if not entry.get("text")],
        "entries_missing_lines": [entry["id"] for entry in entries if not entry["zervos"]["lines"]],
        "entries_missing_pages": [entry["id"] for entry in entries if not entry["zervos"]["pages"]],
        "entries_with_sections": [entry["id"] for entry in entries if "section" in entry],
        "chapter_counts": chapter_counts,
        "chapter_130_subsection_count": len(chapter_130[0]["subsections"]) if chapter_130 else 0,
        "page_span": data["work"]["page_span"],
        "recovered_body_chapters": RECOVERED_BODY_CHAPTERS,
        "recovered_body_chapters_missing_text": [
            chapter
            for chapter in RECOVERED_BODY_CHAPTERS
            if any(not entry["text"] for entry in entries if entry["chapter"] == chapter)
        ],
    }

    multi_unit_mismatches = {}
    for chapter, expected_count in EXPECTED_MULTI_UNIT_COUNTS.items():
        actual = chapter_counts.get(chapter, 0)
        if actual != expected_count:
            multi_unit_mismatches[chapter] = {"expected": expected_count, "actual": actual}
    report["multi_unit_mismatches"] = multi_unit_mismatches

    subsection_missing = []
    if chapter_130:
        for subsection in chapter_130[0]["subsections"]:
            if not subsection["text"] or not subsection["zervos"]["lines"]:
                subsection_missing.append(subsection["section"])
    report["chapter_130_missing_subsections"] = subsection_missing

    problems = [
        report["entry_count"] != report["expected_entry_count"],
        bool(report["missing_chapters"]),
        report["actual_title_only_ids"] != report["expected_title_only_ids"],
        bool(report["entries_missing_lemma"]),
        bool(report["entries_missing_chapter_name"]),
        bool(report["entries_missing_text"]),
        bool(report["entries_missing_lines"]),
        bool(report["entries_missing_pages"]),
        report["chapter_130_subsection_count"] != 3,
        bool(report["chapter_130_missing_subsections"]),
        bool(report["recovered_body_chapters_missing_text"]),
        bool(report["multi_unit_mismatches"]),
    ]
    report["status"] = "ok" if not any(problems) else "fail"
    return report


def main() -> None:
    data = build_output()
    report = build_qc_report(data)
    if report["status"] != "ok":
        raise RuntimeError(json.dumps(report, ensure_ascii=False, indent=2))

    OUTPUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_JS.write_text(
        "window.AETIUS_BOOK16_CH126_153_MYREPSIKA_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    QC_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
