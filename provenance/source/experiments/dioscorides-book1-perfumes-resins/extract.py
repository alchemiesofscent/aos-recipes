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
SOURCE_XML = REPO_ROOT / "tei/raw/tlg0656.tlg001.1st1K-grc1.xml"
OUTPUT_JSON = ROOT / "data/dioscorides_book1_perfumes_resins.json"
OUTPUT_JS = ROOT / "data/dioscorides_book1_perfumes_resins.js"
QC_REPORT = ROOT / "qc_report.json"

CHAPTER_NAMES = {
    "25": "κῦφι",
    "30": "ἔλαιον πρὸς τὴν ἐν ὑγιείᾳ χρῆσιν",
    "31": "ἐλαιόμελι",
    "32": "κίκινον ἔλαιον",
    "33": "ἀμυγδάλινον ἔλαιον",
    "34": "βαλάνινον",
    "35": "ὑοσκυάμινον",
    "36": "διὰ τοῦ κνιδίου κόκκου",
    "37": "ῥαφάνινον",
    "38": "σινάπινον",
    "39": "μυρσίνινον",
    "40": "δάφνινον",
    "41": "σχίνινον",
    "42": "μαστίχινον",
    "43": "ῥόδινον",
    "44": "ἐλατῖνον",
    "45": "μηλῖνον",
    "46": "οἰνάνθινον",
    "47": "τηλῖνον",
    "48": "σαμψουχῖνον",
    "49": "ὠκιμῖνον",
    "50": "ἁβροτόνινον",
    "51": "ἀνηθίνον",
    "52": "σουσῖνον",
    "53": "ναρκίσσινον",
    "54": "κρόκινον",
    "55": "κυπρῖνον",
    "56": "ἴρινον",
    "57": "γλεύκινον",
    "58": "ἀμαράκινον",
    "59": "μετώπιον",
    "60": "στακτή",
    "61": "κιναμώμινον",
    "62": "νάρδινον",
    "63": "μαλαβάθρινον",
    "71": "ῥητίνη",
}

SLICE_KYPHI = {"start": 1590, "end": 1633}
SLICE_PROEMIUM = {"start": 2306, "end": 2342}
SLICE_PERFUMES = {"start": 1855, "end": 3167}
SLICE_IASMELAION = {"start": 3195, "end": 3205}
SLICE_RESINS = {"start": 3695, "end": 3934}

PROEMIUM_SPECS = [
    {
        "id": "dioscorides-1-myra-proemium",
        "book": "1",
        "chapter": "42",
        "section": "2",
        "entry_kind": "proemium",
        "source_kind": "main_text",
        "lemma": "μύρα",
        "chapter_name": "μύρα",
        "refs": [("section", "42", "2")],
        "source_lines": SLICE_PROEMIUM,
    },
]

ENTRY_SPECS = [
    {
        "id": "dioscorides-1-25-kyphi",
        "book": "1",
        "chapter": "25",
        "section": "1-2",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κῦφι",
        "chapter_name": CHAPTER_NAMES["25"],
        "refs": [("section", "25", "1"), ("section", "25", "2")],
        "source_lines": SLICE_KYPHI,
    },
    {
        "id": "dioscorides-1-30-omphakinon",
        "book": "1",
        "chapter": "30",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ὀμφάκινον",
        "chapter_name": CHAPTER_NAMES["30"],
        "refs": [("section", "30", "1"), ("section", "30", "2")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-30-3-agrias-elaias",
        "book": "1",
        "chapter": "30",
        "section": "3",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἔλαιον ἀγρίας ἐλαίας",
        "chapter_name": CHAPTER_NAMES["30"],
        "refs": [("section_paragraph", "30", "3", 0)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-30-whitened-oil",
        "book": "1",
        "chapter": "30",
        "section": "3-4",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "λευκανθὲν ἔλαιον",
        "chapter_name": CHAPTER_NAMES["30"],
        "refs": [("section_paragraph", "30", "3", 1), ("section", "30", "4")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-30-5-sikyonion",
        "book": "1",
        "chapter": "30",
        "section": "5",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σικυώνιον",
        "chapter_name": CHAPTER_NAMES["30"],
        "refs": [("section", "30", "5")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-31-elaiomeli",
        "book": "1",
        "chapter": "31",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἐλαιόμελι",
        "chapter_name": CHAPTER_NAMES["31"],
        "refs": [("chapter_paragraph", "31", 0)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-31-thalloi-oil",
        "book": "1",
        "chapter": "31",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἔλαιον ἐκ θαλλῶν ἐλαίας",
        "chapter_name": CHAPTER_NAMES["31"],
        "refs": [("chapter_paragraph", "31", 1)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-32-kikinon",
        "book": "1",
        "chapter": "32",
        "section": "1",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κίκινον",
        "chapter_name": CHAPTER_NAMES["32"],
        "refs": [("section", "32", "1")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-32-2-kikinon-aigyption",
        "book": "1",
        "chapter": "32",
        "section": "2",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κίκινον αἰγυπτίων",
        "chapter_name": CHAPTER_NAMES["32"],
        "refs": [("section", "32", "2")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-33-amygdalinon",
        "book": "1",
        "chapter": "33",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἀμυγδάλινον",
        "chapter_name": CHAPTER_NAMES["33"],
        "refs": [("chapter", "33")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-34-balaninon",
        "book": "1",
        "chapter": "34",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "βαλάνινον",
        "chapter_name": CHAPTER_NAMES["34"],
        "refs": [("chapter_paragraph", "34", 0)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-34-sesaminon-karyinon",
        "book": "1",
        "chapter": "34",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σησάμινον καὶ καρύϊνον",
        "chapter_name": CHAPTER_NAMES["34"],
        "refs": [("chapter_paragraph", "34", 1)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-35-hyoskyaminon",
        "book": "1",
        "chapter": "35",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ὑοσκυάμινον",
        "chapter_name": CHAPTER_NAMES["35"],
        "refs": [("chapter", "35")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-36-knidion",
        "book": "1",
        "chapter": "36",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "διὰ τοῦ κνιδίου κόκκου",
        "chapter_name": CHAPTER_NAMES["36"],
        "refs": [("chapter_paragraph", "36", 0)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-36-knekikon",
        "book": "1",
        "chapter": "36",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κνήκινον",
        "chapter_name": CHAPTER_NAMES["36"],
        "refs": [("chapter_paragraph", "36", 1)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-37-raphaninon",
        "book": "1",
        "chapter": "37",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ῥαφάνινον",
        "chapter_name": CHAPTER_NAMES["37"],
        "refs": [("chapter_paragraph", "37", 0)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-37-melanthinon",
        "book": "1",
        "chapter": "37",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μελάνθινον",
        "chapter_name": CHAPTER_NAMES["37"],
        "refs": [("chapter_paragraph", "37", 1)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-38-sinapinon",
        "book": "1",
        "chapter": "38",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σινάπινον",
        "chapter_name": CHAPTER_NAMES["38"],
        "refs": [("chapter", "38")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-39-myrsininon",
        "book": "1",
        "chapter": "39",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μυρσίνινον",
        "chapter_name": CHAPTER_NAMES["39"],
        "refs": [("chapter", "39")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-40-daphninon",
        "book": "1",
        "chapter": "40",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "δάφνινον",
        "chapter_name": CHAPTER_NAMES["40"],
        "refs": [("chapter", "40")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-41-schininon",
        "book": "1",
        "chapter": "41",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σχίνινον",
        "chapter_name": CHAPTER_NAMES["41"],
        "refs": [("chapter", "41")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-42-mastichinon",
        "book": "1",
        "chapter": "42",
        "section": "1",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μαστίχινον",
        "chapter_name": CHAPTER_NAMES["42"],
        "refs": [("section", "42", "1")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-43-rhodinon",
        "book": "1",
        "chapter": "43",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ῥόδινον",
        "chapter_name": CHAPTER_NAMES["43"],
        "refs": [("chapter", "43")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-44-elatinon",
        "book": "1",
        "chapter": "44",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἐλατῖνον",
        "chapter_name": CHAPTER_NAMES["44"],
        "refs": [("chapter", "44")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-45-melinon",
        "book": "1",
        "chapter": "45",
        "section": "1",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μηλῖνον",
        "chapter_name": CHAPTER_NAMES["45"],
        "refs": [("section", "45", "1")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-45-2-melinon-allos",
        "book": "1",
        "chapter": "45",
        "section": "2",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μηλῖνον ἄλλως",
        "chapter_name": CHAPTER_NAMES["45"],
        "refs": [("section", "45", "2")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-46-oinanthinon",
        "book": "1",
        "chapter": "46",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "οἰνάνθινον",
        "chapter_name": CHAPTER_NAMES["46"],
        "refs": [("chapter", "46")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-47-telinon",
        "book": "1",
        "chapter": "47",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "τηλῖνον",
        "chapter_name": CHAPTER_NAMES["47"],
        "refs": [("chapter", "47")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-48-sampsouchinon",
        "book": "1",
        "chapter": "48",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σαμψουχῖνον",
        "chapter_name": CHAPTER_NAMES["48"],
        "refs": [("chapter", "48")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-49-okiminon",
        "book": "1",
        "chapter": "49",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ὠκιμῖνον",
        "chapter_name": CHAPTER_NAMES["49"],
        "refs": [("chapter", "49")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-50-habrotoninon",
        "book": "1",
        "chapter": "50",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἁβροτόνινον",
        "chapter_name": CHAPTER_NAMES["50"],
        "refs": [("chapter", "50")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-51-anethinon",
        "book": "1",
        "chapter": "51",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἀνηθίνον",
        "chapter_name": CHAPTER_NAMES["51"],
        "refs": [("chapter", "51")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-52-sousinon",
        "book": "1",
        "chapter": "52",
        "section": "1-4",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σουσῖνον",
        "chapter_name": CHAPTER_NAMES["52"],
        "refs": [("section", "52", "1"), ("section", "52", "2"), ("section", "52", "3"), ("section", "52", "4")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-52-5-sousinon-haploun",
        "book": "1",
        "chapter": "52",
        "section": "5",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "σουσῖνον ἁπλοῦν",
        "chapter_name": CHAPTER_NAMES["52"],
        "refs": [("section", "52", "5")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-53-narkissinon",
        "book": "1",
        "chapter": "53",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ναρκίσσινον",
        "chapter_name": CHAPTER_NAMES["53"],
        "refs": [("chapter", "53")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-54-krokinon",
        "book": "1",
        "chapter": "54",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κρόκινον",
        "chapter_name": CHAPTER_NAMES["54"],
        "refs": [("chapter", "54")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-55-kyprinon",
        "book": "1",
        "chapter": "55",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κυπρῖνον",
        "chapter_name": CHAPTER_NAMES["55"],
        "refs": [("chapter", "55")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-56-irinon",
        "book": "1",
        "chapter": "56",
        "section": "1,3-4",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἴρινον",
        "chapter_name": CHAPTER_NAMES["56"],
        "refs": [("section", "56", "1"), ("section", "56", "3"), ("section", "56", "4")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-56-2-irinon-allos",
        "book": "1",
        "chapter": "56",
        "section": "2",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἴρινον ἄλλως",
        "chapter_name": CHAPTER_NAMES["56"],
        "refs": [("section", "56", "2")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-57-gleukinon",
        "book": "1",
        "chapter": "57",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "γλεύκινον",
        "chapter_name": CHAPTER_NAMES["57"],
        "refs": [("chapter", "57")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-58-amarakinon",
        "book": "1",
        "chapter": "58",
        "section": "1-2",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἀμαράκινον",
        "chapter_name": CHAPTER_NAMES["58"],
        "refs": [("section", "58", "1"), ("section", "58", "2")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-58-3-megalleion",
        "book": "1",
        "chapter": "58",
        "section": "3",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μεγάλλειον",
        "chapter_name": CHAPTER_NAMES["58"],
        "refs": [("section_paragraph", "58", "3", 0)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-58-3-hedychroun",
        "book": "1",
        "chapter": "58",
        "section": "3",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "ἠδύχρουν",
        "chapter_name": CHAPTER_NAMES["58"],
        "refs": [("section_paragraph", "58", "3", 1)],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-59-metopion",
        "book": "1",
        "chapter": "59",
        "section": "1-2",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μετώπιον",
        "chapter_name": CHAPTER_NAMES["59"],
        "refs": [("section", "59", "1"), ("section", "59", "2")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-59-3-mendesion",
        "book": "1",
        "chapter": "59",
        "section": "3",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μενδήσιον",
        "chapter_name": CHAPTER_NAMES["59"],
        "refs": [("section", "59", "3")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-60-stakte",
        "book": "1",
        "chapter": "60",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "στακτή",
        "chapter_name": CHAPTER_NAMES["60"],
        "refs": [("chapter", "60")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-61-kinamominon",
        "book": "1",
        "chapter": "61",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "κιναμώμινον",
        "chapter_name": CHAPTER_NAMES["61"],
        "refs": [("chapter", "61")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-62-nardinon",
        "book": "1",
        "chapter": "62",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "νάρδινον",
        "chapter_name": CHAPTER_NAMES["62"],
        "refs": [("chapter", "62")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-63-malabathrinon",
        "book": "1",
        "chapter": "63",
        "entry_kind": "recipe",
        "source_kind": "main_text",
        "lemma": "μαλαβάθρινον",
        "chapter_name": CHAPTER_NAMES["63"],
        "refs": [("chapter", "63")],
        "source_lines": SLICE_PERFUMES,
    },
    {
        "id": "dioscorides-1-63-iasmelaion",
        "book": "1",
        "chapter": "63",
        "entry_kind": "recipe",
        "source_kind": "apparatus_other_recension",
        "lemma": "ἰασμέλαιον",
        "chapter_name": CHAPTER_NAMES["63"],
        "section": "apparatus",
        "source_lines": SLICE_IASMELAION,
        "caveat": "Preserved only in the apparatus as an addition from another recension; not part of the main-text flow of this witness.",
        "apparatus_anchor": {"page": "57", "line": "5"},
    },
    {
        "id": "dioscorides-1-71-5-burned-resin-with-water",
        "book": "1",
        "chapter": "71",
        "section": "5",
        "entry_kind": "technique",
        "source_kind": "main_text",
        "lemma": "ῥητίνη κεκαυμένη μετὰ ὕδατος",
        "chapter_name": CHAPTER_NAMES["71"],
        "refs": [("section", "71", "5")],
        "source_lines": SLICE_RESINS,
    },
    {
        "id": "dioscorides-1-71-6-burned-resin-without-water",
        "book": "1",
        "chapter": "71",
        "section": "6",
        "entry_kind": "technique",
        "source_kind": "main_text",
        "lemma": "ῥητίνη κεκαυμένη δίχα ὕδατος",
        "chapter_name": CHAPTER_NAMES["71"],
        "refs": [("section", "71", "6")],
        "source_lines": SLICE_RESINS,
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
    for div in chapter.findall("tei:div[@type='textpart'][@subtype='section']", NS):
        if div.get("n") == section_n:
            return div
    raise RuntimeError(f"Section {section_n} not found in chapter {chapter.get('n')}.")


def find_paragraph(parent: ET.Element, index: int) -> ET.Element:
    paragraphs = parent.findall("tei:p", NS)
    if index < 0 or index >= len(paragraphs):
        raise RuntimeError(f"Paragraph {index} not found under {tag_name(parent)} {parent.get('n')}.")
    return paragraphs[index]


def resolve_targets(book: ET.Element, refs: list[tuple]) -> list[ET.Element]:
    targets: list[ET.Element] = []
    for ref in refs:
        kind = ref[0]
        if kind == "chapter":
            targets.append(find_book_chapter(book, ref[1]))
        elif kind == "chapter_paragraph":
            chapter = find_book_chapter(book, ref[1])
            targets.append(find_paragraph(chapter, ref[2]))
        elif kind == "section":
            chapter = find_book_chapter(book, ref[1])
            targets.append(find_section(chapter, ref[2]))
        elif kind == "section_paragraph":
            chapter = find_book_chapter(book, ref[1])
            section = find_section(chapter, ref[2])
            targets.append(find_paragraph(section, ref[3]))
        else:
            raise RuntimeError(f"Unknown ref kind: {kind}")
    return targets


def collect_fragments(book: ET.Element) -> list[dict[str, object]]:
    fragments: list[dict[str, object]] = []
    state = {"current_page": None, "current_line": None, "break_no": False}

    def append_text(text: str | None, ancestors: tuple[int, ...]) -> None:
        if not text:
            return
        cleaned = WHITESPACE_RE.sub(" ", text)
        if not cleaned.strip() or state["current_line"] is None or state["current_page"] is None:
            return
        fragments.append(
            {
                "page": str(state["current_page"]),
                "line": str(state["current_line"]),
                "break_no": bool(state["break_no"]),
                "text": cleaned.strip(),
                "ancestors": ancestors,
            }
        )

    def walk(node: ET.Element, ancestors: tuple[int, ...]) -> None:
        name = tag_name(node)
        if name == "note" or name == "del":
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
            if child_name == "note" or child_name == "del":
                append_text(child.tail, current_ancestors)
                continue
            walk(child, current_ancestors)
            append_text(child.tail, current_ancestors)

    walk(book, tuple())
    return fragments


def build_lines(fragments: list[dict[str, object]], target_ids: set[int]) -> list[dict[str, object]]:
    grouped: OrderedDict[tuple[str, str], dict[str, object]] = OrderedDict()
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

    lines: list[dict[str, object]] = []
    for key, item in grouped.items():
        text = normalize_space(" ".join(item.pop("parts")))
        if not text:
            continue
        item["text"] = text
        item["citation"] = f"{item['page']}.{item['line']}"
        lines.append(item)
    return lines


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
        "start": {"page": str(start["page"]), "line": str(start["line"])},
        "end": {"page": str(end["page"]), "line": str(end["line"])},
        "citation": {"start": f"{start['page']}.{start['line']}", "end": f"{end['page']}.{end['line']}"},
        "page_spans": list(spans.values()),
        "lines": lines,
    }


def build_entry_from_spec(spec: dict[str, object], fragments: list[dict[str, object]], book: ET.Element) -> dict[str, object]:
    targets = resolve_targets(book, spec["refs"])
    target_ids = {id(target) for target in targets}
    lines = build_lines(fragments, target_ids)
    if not lines:
        raise RuntimeError(f"No lineation found for {spec['id']}")
    payload = {
        "id": spec["id"],
        "entry_kind": spec["entry_kind"],
        "source_kind": spec["source_kind"],
        "lemma": spec["lemma"],
        "book": spec["book"],
        "chapter": spec["chapter"],
        "section": spec.get("section"),
        "chapter_name": spec["chapter_name"],
        "text": join_flow_text(lines),
        "source_lines": spec["source_lines"],
        "caveat": spec.get("caveat"),
        "wellmann": build_lineation(lines),
    }
    return payload


def extract_iasmelaion_note(root: ET.Element) -> str:
    for note in root.findall(".//tei:note[@type='footnote']", NS):
        text = normalize_space(" ".join(note.itertext()))
        if "ἰασμέλαιον" not in text:
            continue
        marker = "περὶ ἰασμίνου·"
        if marker not in text:
            raise RuntimeError("Found ἰασμέλαιον note but could not locate the recital marker.")
        excerpt = text.split(marker, 1)[1]
        return normalize_space(excerpt)
    raise RuntimeError("Could not find the ἰασμέλαιον apparatus note.")


def build_apparatus_entry(spec: dict[str, object], text: str) -> dict[str, object]:
    anchor = spec["apparatus_anchor"]
    page = str(anchor["page"])
    line = str(anchor["line"])
    lines = [{"page": page, "line": line, "break_no": False, "text": text, "citation": f"{page}.{line}"}]
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
        "source_lines": spec["source_lines"],
        "caveat": spec.get("caveat"),
        "wellmann": build_lineation(lines),
    }


def build_output() -> dict[str, object]:
    root = ET.parse(SOURCE_XML).getroot()
    book = find_book(root, "1")
    fragments = collect_fragments(book)
    apparatus_text = extract_iasmelaion_note(root)

    proemium = [build_entry_from_spec(spec, fragments, book) for spec in PROEMIUM_SPECS]
    entries: list[dict[str, object]] = []
    for spec in ENTRY_SPECS:
        if spec["source_kind"] == "apparatus_other_recension":
            entries.append(build_apparatus_entry(spec, apparatus_text))
        else:
            entries.append(build_entry_from_spec(spec, fragments, book))
    entries = attach_viewer_entity_groups(entries)

    pages: list[str] = []
    for item in proemium + entries:
        for page in item["wellmann"]["pages"]:
            if page not in pages:
                pages.append(page)
    pages.sort(key=lambda value: int(value))

    return {
        "source": {
            "xml_file": str(SOURCE_XML.relative_to(REPO_ROOT)),
            "edition": "Wellmann",
            "requested_slices": [
                {"label": "kyphi", **SLICE_KYPHI},
                {"label": "proemium", **SLICE_PROEMIUM},
                {"label": "perfumes_main", **SLICE_PERFUMES},
                {"label": "iasmelaion_apparatus", **SLICE_IASMELAION},
                {"label": "resin_techniques", **SLICE_RESINS},
            ],
            "notes": [
                "Raw lines 1590-1633 are book 1 chapter 25 in this witness, although the prompt referred to chapter 35.",
                "The perfume proemium is taken from the later transition at chapter 42 section 2 (raw lines 2306-2342), not from the chapter 25 κῦφι entry.",
                "The ἰασμέλαιον entry is preserved only in the apparatus as an addition from another recension.",
            ],
        },
        "work": {
            "author": "Dioscorides",
            "work": "De materia medica",
            "book": "1",
            "chapter_span": ["25", "30-63", "71"],
            "page_span": pages,
        },
        "proemium": proemium,
        "entries": entries,
    }


def build_qc_report(data: dict[str, object]) -> dict[str, object]:
    entries = data["entries"]
    expected_ids = [spec["id"] for spec in ENTRY_SPECS]
    actual_ids = [entry["id"] for entry in entries]
    missing_ids = [entry_id for entry_id in expected_ids if entry_id not in actual_ids]
    duplicate_ids = sorted({entry_id for entry_id in actual_ids if actual_ids.count(entry_id) > 1})
    missing_text = [entry["id"] for entry in entries if not entry["text"]]
    missing_pages = [entry["id"] for entry in entries if not entry["wellmann"]["pages"]]
    missing_lines = [entry["id"] for entry in entries if not entry["wellmann"]["lines"]]
    non_lowercase_lemmas = [entry["id"] for entry in entries if entry["lemma"] != str(entry["lemma"]).lower()]
    apparatus_entries = [entry["id"] for entry in entries if entry["source_kind"] == "apparatus_other_recension"]
    technique_entries = [entry["id"] for entry in entries if entry["entry_kind"] == "technique"]
    non_monotonic_citations = [
        entry["id"]
        for entry in entries
        if tuple(int(part) for part in entry["wellmann"]["citation"]["start"].split("."))
        > tuple(int(part) for part in entry["wellmann"]["citation"]["end"].split("."))
    ]

    return {
        "proemium_count": len(data["proemium"]),
        "expected_proemium_count": len(PROEMIUM_SPECS),
        "entry_count": len(entries),
        "expected_entry_count": len(ENTRY_SPECS),
        "expected_ids": expected_ids,
        "actual_ids": actual_ids,
        "first_entry_id": actual_ids[0] if actual_ids else None,
        "missing_ids": missing_ids,
        "duplicate_ids": duplicate_ids,
        "missing_text": missing_text,
        "missing_pages": missing_pages,
        "missing_lines": missing_lines,
        "non_lowercase_lemmas": non_lowercase_lemmas,
        "non_monotonic_citations": non_monotonic_citations,
        "apparatus_entries": apparatus_entries,
        "technique_entries": technique_entries,
        "page_span": data["work"]["page_span"],
        "status": "ok"
        if len(data["proemium"]) == len(PROEMIUM_SPECS)
        and len(entries) == len(ENTRY_SPECS)
        and actual_ids[:1] == ["dioscorides-1-25-kyphi"]
        and not any(
            [
                missing_ids,
                duplicate_ids,
                missing_text,
                missing_pages,
                missing_lines,
                non_lowercase_lemmas,
                non_monotonic_citations,
            ]
        )
        and apparatus_entries == ["dioscorides-1-63-iasmelaion"]
        and technique_entries == [
            "dioscorides-1-71-5-burned-resin-with-water",
            "dioscorides-1-71-6-burned-resin-without-water",
        ]
        else "needs_review",
    }


def main() -> None:
    data = build_output()
    qc = build_qc_report(data)
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT_JSON.write_text(json_text + "\n", encoding="utf-8")
    OUTPUT_JS.write_text(f"window.DIOSCORIDES_BOOK1_DATA = {json_text};\n", encoding="utf-8")
    QC_REPORT.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_JS.relative_to(REPO_ROOT)}")
    print(f"Wrote {QC_REPORT.relative_to(REPO_ROOT)}")
    print(f"Entries: {qc['entry_count']}")
    print(f"QC status: {qc['status']}")


if __name__ == "__main__":
    main()
