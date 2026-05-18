from __future__ import annotations

import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import OrderedDict, defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.recipes.common import attach_viewer_entity_groups

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_NS = "{http://www.w3.org/XML/1998/namespace}"
WHITESPACE_RE = re.compile(r"\s+")
HYPHEN_CHARS = ("-", "‐", "‑", "‒", "–", "—", "﹘", "﹣", "－")
RANGE_HEADER_RE = re.compile(r"^\[?(?P<start>\d+\.\d+)(?:-(?:(?P<end_page>\d+)\.)?(?P<end_line>\d+))?\]$")
NOTE_LINE_RE = re.compile(
    r"^\[?(?P<start>\d+\.\d+)(?:-(?:(?P<end_page>\d+)\.)?(?P<end_line>\d+))?\]\s*(?P<rest>.*)$"
)
HEADING_RE = re.compile(r"^\([^)]+\)\s*(?P<body>.+)$")
INLINE_PAGE_MARKER_RE = re.compile(r"\[(?:p\.?\d+|\d+)\]")
REVISED_NUMERAL_MARK_RE = re.compile(r"(?<=[α-ωϛϙϲς])(?:΄|ʹ|ʹ)")
REVISED_NUMERAL_SIGMA_RE = re.compile(r"\b([α-ωϛϙ]+)ϲ\b")
REVISED_XESTES_RE = re.compile(r"ξ̸ε\s+([α-ωϛϙϲς]+)\b")
REVISED_SIGNED_NUMERAL_RE = re.compile(r"(?<!\S)([ΓΧ<])\s*([α-ωϛϙϲς]+)\b")
ARABIC_DIGITS_AFTER_WORD_RE = re.compile(r"(?<=[^\W\d_])\d+(?=(?:\s|[.,;··:)])|$)")
ARABIC_STANDALONE_DIGITS_RE = re.compile(r"(?:(?<=^)|(?<=\s)|(?<=[(]))\d+(?=(?:\s|[.,;··:)])|$)")
SPACE_BEFORE_PUNCTUATION_RE = re.compile(r"\s+([.,;··:)])")

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE_XML = REPO_ROOT / "tei/output/tlg0718.tlg001.aos-grc1.xml"
REVISED_NOTES = REPO_ROOT / "experiments/revised-aetius-1-99-136.txt"
OUTPUT_JSON = ROOT / "data/aetius_book1_ch99_136_oils.json"
OUTPUT_JS = ROOT / "data/aetius_book1_ch99_136_oils.js"
EMENDATION_JSON = ROOT / "data/aetius_book1_emendations.json"
QC_REPORT = ROOT / "qc_report.json"

PROEMIUM_CHAPTER = "100"
ENTRY_START = 101
ENTRY_END = 136

TITLE_MARKERS = (
    " σκευάζεται",
    " γίγνεται",
    " δύναμιν ἔχει",
    " τὰ αὐτὰ δρᾷ",
    " συντίθεται",
    " μαλακτικ",
    " ἐκ τοῦ",
    " ἐν Αἰγύπτῳ",
    " ἁρμόδια",
    " καλούμενον",
)

AETIUS_BOOK1_ENTRY_SPLITS: dict[str, list[dict[str, object]]] = {
    "aetius-1-113": [
        {
            "recipe_id": "aetius-1-113",
            "section": "113",
            "text": "Ἔλαιον ῥόδινον, κηρωτὴ ἡ ψύχουσα. Ῥόδινον σκευάζεται οὕτως· ῥόδων ἐρυθρῶν ἐξωνυχισμένων καὶ ἐψυγμένων ἡμέραν καὶ νύκτα 𐆄 γ, ἐλαίου ὀμφακίνου ξέστης ἰταλικὸς εἷς, ἐμβάλλοντα δὲ τὰ ῥόδα περισφίγγειν χρὴ τὸ στόμα τοῦ βίκου ἔσωθεν μὲν ὀθονίῳ, ἔξωθεν δὲ δέρματι διὰ τοὺς γιγνομένους ὄμβρους αἰφνίδιον καὶ ἡλιοῦν ἡμέρας κ καὶ οὕτως σειρώσαντα ἀποτίθεσθαι τοὺς βίκους ἐπὶ σανίδων ἐν οἴκοις εὐκράτοις. τινὲς δὲ ἕτερά τινα προσεμβάλλουσι τοῖς ῥόδοις. ἀρίστη δέ ἐστιν ἡ διὰ τῶν ῥόδων μόνων καὶ ἐλαίου σκευασία. τινὲς δὲ οὐχ ἡλιοῦσιν, ἀλλ' ἀποκρημνοῦσι τὸν βίκον εἰς φρέαρ ὕδατος ψυχροῦ ἡμέρας μ. ἁρμόζει δὲ κεφαλῇ θερμανθείσῃ καὶ ξηρανθείσῃ ἢ ἐξ ἡλιώσεως ἢ ἐκ πυρετῶν ἤ τινος ἄλλης τοιαύτης προφάσεως. ὑγραίνει γὰρ καὶ παρηγορεῖ καὶ ὕπνον ἐπάγει. καὶ πινόμενον δὲ τὸ κάλλιστον ῥόδινον σὺν ὕδατι ψυχρῷ ἢ θερμῷ ἐπὶ τῶν δακνομένων τὸν στόμαχον ἐκ χολῆς δριμείας ἢ ἐλμίνθων ἢ ἀσκαρίδων μεγάλας παρέχει ὠφελείας. ἐπὶ δὲ ἐλμίνθων καὶ μάλιστα ἐπὶ παίδων κρεῖττον ποιεῖ μιγνύμενον ἑψήματι τῷ ἀπ' οἴνου τριτουμένου σκευαζομένῳ καὶ πινόμενον· ἐκτινάσσει γὰρ αὐτὰς τάχιστα. ἐνίεται δὲ καὶ κώλῳ δακνομένῳ διὰ τὰς εἰρημένας προφάσεις.",
            "citation": {"start": "58.1", "end": "59.7"},
            "notes": ["Rose-oil preparation split from the explicitly introduced cooling cerate aetius-1-113-2."],
        },
        {
            "recipe_id": "aetius-1-113-2",
            "section": "113.2",
            "lemma": "κηρωτὴ ἡ ψύχουσα",
            "text": "κηρωτὴ ἡ ψύχουσα. καὶ ἐπὶ σπλάγχνων δὲ ἐν πυρετοῖς ἐκθερμαινομένων ἁρμοδία ἡ κηρωτὴ δι' αὐτοῦ σκευαζομένη καὶ πλυνομένη δι' ὕδατος ψυχροῦ, καὶ πλειστάκις ἀλλασσομένου τοῦ ὕδατος ἐν θέρει καὶ ἐπιρραπτομένης τῆς κηρωτῆς τοῖς σπλάγχνοις. σκεύαζε δὲ οὕτως τὴν κηρωτήν· κηροῦ 𐆄 ϛ ῥοδίνου 𐆄 δ. τῆκε τὸν κηρὸν μετ' ὀλίγου ῥοδίνου ἐπὶ διπλώματος καὶ ἐπίχεε εἰς ὕδωρ ψυχροῦν καὶ ψυγέντα ἄρας τῆκε πάλιν καὶ ἐπίχεε καὶ μάλασσε ταῖς χερσὶν ἀποπλύνων τὸν κηρὸν τῷ ὕδατι καὶ πάλιν τὸ τρίτον τῆκε καὶ ἐπιχέας πλῦνε, εἶτα ἐπιβάλλων τὸ λοιπὸν τοῦ ῥοδίνου τῆκε καὶ ἄρας κινῶν ψῦχε καὶ ἐπίχεε ἐν θυίᾳ καὶ λείου ἐπιστάζων ὕδωρ ὅσον ἐπιδέχεται καὶ ἀνελόμενος ἀπόθου εἰς ψυχρὸν ὕδωρ ἀλλάσσων. εἰ δὲ ἀντὶ τοῦ ὕδατος ὄξος μίξῃς τῇ κηρωτῇ ἐπιρραίνων ἐν τῷ λειοῦσθαι αὐτὸ ἐν τῇ θυίᾳ, ἀγαθὸν φάρμακον ἐργάσῃ πρὸς ἐρυσιπέλατα καὶ ἕρπητας καὶ ἄνθρακας. κεῖται καλῶς ἡ κηρωτὴ ἐν τῷ Ϟα κεφαλαίῳ τοῦ ε λόγου.",
            "citation": {"start": "58.13", "end": "58.25"},
            "notes": ["Cooling cerate split from aetius-1-113 as a second preparation block."],
        },
    ],
    "aetius-1-129": [
        {
            "recipe_id": "aetius-1-129",
            "section": "129",
            "text": "Κύπρινον· ἐλαίου ξ̸εκε, κυπέρου ἑλενίου ἴρεως ἀνὰ λίτραν α, σαμψύχου ὑσσώπου ἀνὰ 𐆄 γ, λύγου σπέρματος 𐆄 γ, ἐλελισφάκου 𐆄 γ κύπρου ἄνθους λίτραν α. ἕψεται δὲ καὶ τοῦτο δυσὶν ἑψήσεσι. τὰ μὲν γὰρ ἄλλα πάντα εἴδη οἴνῳ ῥανθέντα εὐώδει πρὸ μιᾶς ἡμέρας εἶτα ἐμβληθέντα τῷ ἐλαίῳ ἕψεται ὥρας ϛ, τῇ δὲ ἑξῆς σειρωθέντος τοῦ ἐλαίου καὶ λαβόντος ἕτερον ὕδωρ καθαρόν, ὡς τὸ τρίτον εἶναι τοῦ χαλκείου, ἐμβάλλεται τὸ ἄνθος τῆς κύπρου. ἐμβλητέον δὲ αὐτὸ μετὰ τῶν ἁπαλῶν κλωναρίων ἄκοπον. εἰ δὲ ξηρὸν εἴη προκόπτειν καὶ οὕτως ἕψεται ὥραν μίαν. θερμαίνει δὲ τὸ κύπρινον οὐκ ἀγεννῶς. ἐστὶ δὲ καὶ λεπτομερὲς καὶ ὑστέραις ἄγαν χρήσιμον, ταῖς κατεψυγμέναις μᾶλλον, καὶ γὰρ λεπτύνει τοὺς ἐν ταύταις παχεῖς χυμούς.",
            "citation": {"start": "64.5", "end": "64.15"},
            "notes": ["Primary kyprinon formulation split from the fresh-herb variant aetius-1-129-2."],
        },
        {
            "recipe_id": "aetius-1-129-2",
            "section": "129.2",
            "text": "ὅταν δὲ εὐπορῶμεν τῶν βοτανῶν χλωρῶν, οὕτως σκευάζομεν τὸ κύπρινον· ἐλαίου ξ̸ειε, κυπέρων ἑλενίου ἴρεως ἀνὰ 𐆄 ϛ σαμψύχου ὑσσώπου ἐλελισφάκου ἀνὰ 𐆄 β ἄγνου χλωρῶν φύλλων 𐆄 β κιτροφύλλων χλωρῶν 𐆄 ζ χαμαιλιβάνου χλωροῦ 𐆄 δ δάφνης φύλλων χλωρῶν 𐆄 ε κύπρου ἄνθους 𐆄 β βαλσάμου ὀποῦ 𐆄 ϛʹ.",
            "citation": {"start": "64.15", "end": "64.20"},
            "notes": ["Fresh-herb kyprinon formulation split from aetius-1-129."],
        },
    ],
    "aetius-1-131": [
        {
            "recipe_id": "aetius-1-131",
            "section": "131",
            "text": "Νάρδου Κυζικηνῆς σκευασία. Ἐσκεύασα ταύτην ἐν Ἀλεξανδρείᾳ πλειστάκις καί ἐστι πάνυ καλή· ἐλαίου ὀμφακίζοντος ξ̸ειβ ἰταλικοί, ἀσπαλάθου κυπέρων ἴρεως ἰλλυρικῆς καρδαμώμου σπέρμα ἀριστολοχίας μακρᾶς ξυλοκασίας ἀνὰ 𐆄 ιβ ἑλενίου ξυλοβαλσάμου σχοίνου ἄνθους κασίας κόστου ἀνὰ 𐆄 ϛʹ ἀμώμου φύλλου ναρδοστάχυος ἀνὰ 𐆄 β στύρακος καρποβαλσάμου ἀνὰ 𐆄 γʹ ὀποβαλσάμου 𐆄 γʹ βράθυος 𐆄 α. σκευάζεται δὲ οὕτως· ἀσπάλαθον κύπερον ἑλένιον ξυλοβάλσαμον ἶριν ἀριστολοχίαν ἀποφλοιώσας κόψας ἁδρομερῶς βρέχε ἡμέρας γ ὕδατι θερμῷ, ἔπειτα ἐπιβάλλων τὸ ἔλαιον ἕψε κινῶν συνεχῶς ἐπιβάλλων ὕδωρ κατὰ βραχὺ πρὸς ὃ τὸ πρῶτον ἀναλίσκεται, εἶτα ἑψήσας ἐπὶ ὥρας γ ἢ καὶ πλέον σκεπάσας ἔα διανυκτερεῦσαι· τῇ δὲ ἑξῆς ἀνασπάσας τὰ ἤδη ἑψηθέντα καὶ ἀποχωρίσας τοῦ ἐλαίου τὸ ὕδωρ, εἶτ' ἐπιβαλὼν ἕτερον ὕδωρ καὶ οἴνου βραχὺ ἕψε. ὅταν δὲ ἀναζέσῃ, ἐπίβαλλε πρῶτον καρδάμωμον εἶτα σχοῖνον ξυλοκασίαν κεκομμένα καὶ ἕψε ἐπὶ ὥρας β καὶ πάλιν ἔα διανυκτερεῦσαι. τῇ δὲ τρίτῃ ἀνασπάσας ὁμοίως καὶ ὕδωρ καθαρὸν ἐπιβαλὼν ἕψε καὶ ὅταν ἀναζέσῃ ἐπίπασσε λεῖα κατὰ μέρος κασίαν κόστον καὶ τὰ λοιπά, ἕκαστον κατ' ἰδίαν κοπέν. περὶ τὰ τελευταῖα δὲ νάρδου στάχυ καὶ φύλλον καὶ τὸν στύρακα εἰς λεπτὰ μόρια διαμερισθέντα, καὶ τακέντος αὐτοῦ ἆρον εὐθέως ἀπὸ τοῦ πυρὸς καὶ ἐπίβαλλε τὸ ὀποβάλσαμον καὶ ἀνακινήσας ἱκανῶς καὶ πωμάσας καὶ σκεπάσας καλῶς ἔα ἡμέρας β καὶ οὕτως μυακίῳ ἀναλάμβανε. τὸ δὲ δευτέριον σκευάζεται οὕτως· τοῖς καταλειφθεῖσιν ἐκ τῆς τρίτης ἑψήσεως ἐπίβαλλε ἐλαίου ξ̸ ϛʹ καὶ ἀναζέσας ἕψε ὥρας β, εἶτα ἐπίπασσε κασίας λειοτάτης 𐆄 β νάρδου κελτικῆς 𐆄 β βράθυος 𐅻 δ στύρακος 𐆄 α ὀποβαλσάμου 𐆄 β. ἐστὶ δὲ ἡ νάρδος δυνάμεως θερμαντικῆς τονωτικῆς παρηγορικῆς, στομάχῳ τοίνυν ἐψυγμένῳ καὶ ἀτόνῳ καὶ γαστρὶ καὶ ἥπατι τὰ αὐτὰ πεπονθόσιν ἐπιτηδειοτάτη. ἐνίεται καὶ ἐπὶ τῶν ψυγέντων τὰ ἔντερα καὶ ἐπὶ γυναικῶν τῇ μήτρα χρῶ ὡς πάνυ δοκίμῳ.",
            "citation": {"start": "65.4", "end": "66.4"},
            "notes": ["Primary Kyzikene nard preparation split from the later headed nard variants in chapter 131."],
        },
        {
            "recipe_id": "aetius-1-131-2",
            "section": "131.2",
            "lemma": "Προέψησις τῆς νάρδου",
            "text": "Προέψησις τῆς νάρδου. Οἴνου παλαιοῦ λι ι δενδρολιβάνου φύλλων λι α ῥάσδου λι γ καλαμοκρίνου λι γ βρουλλοκυπέρου λι δ, ταῦτα πάντα βάλλε ἐν τῇ προεψήσει. ὁ δὲ βρασμὸς αὐτοῦ ὥρας ιβ ἵνα κενωθῇ εἰς καθαρὸν ἀγγεῖον καὶ σπογγισθῇ τὸ κακάβιν καὶ πάλιν βάλλῃς οἴνου λι ιε καὶ ἐκεῖνο τὸ ἔλαιον ἐπάνω.",
            "citation": {"start": "66.5", "end": "66.9"},
            "notes": ["Pre-boiling stage split from aetius-1-131 as its own headed unit."],
        },
        {
            "recipe_id": "aetius-1-131-3",
            "section": "131.3",
            "lemma": "Νάρδου σκευασία",
            "text": "Νάρδου σκευασία. Νάρδος σκευαζομένη ἐν τῇ ἐκκλησίᾳ. στάχους λι κιναμώμου λι καρυοφύλλων λι ἀμώμου λι σχινάνθων λι καλάμου ἀρωματικοῦ λι ξυλαλόης λι καρύων μυριστικῶν λι καχρύου λι ξανθοκαρύων λι μάκερ λι γαλαγγὰ λι βαλσάμου λι καρποβαλσάμου λι ξυλοβαλσάμου λι μυροβαλάνου λι φύλλου ἰνδικοῦ λι κασίας λι ξηροκαρυοφύλλου λι πεπέρεως μακροῦ λι πεπέρεως λευκοῦ λι πεπέρεως κοινοῦ λι ἄσαρ χαλδαικοῦ λι κελτικοῦ λι θυμιάματος λι σμύρνης τρωγλίτιδος λι κόστου λι μόσχου λι ἄμπαρ λι γομφίτου λαδάνου λι τερεβίνθης λι οἴνου εὐώδους τὸ ἀρκοῦν.",
            "citation": {"start": "66.10", "end": "66.18"},
            "notes": ["Church-prepared nard formulation split from aetius-1-131."],
        },
        {
            "recipe_id": "aetius-1-131-4",
            "section": "131.4",
            "lemma": "Ἑτέρα σκευασία νάρδου",
            "text": "Ἑτέρα σκευασία νάρδου. Ἐν τῇ προεψήσει οἴνου παλαιοῦ λι ιε δενδρολιβάνου φύλλων λι α μυρσίνης φύλλων λι α ῥάσδου λι γ καλαμοκρίνου λι β βρουλλοκυπέρου λι δ· ταῦτα πάντα βάλλε ἐν τῇ προεψήσει ἵνα βράσωσιν ὥρας ιβ καὶ κενωθῇ εἰς καθαρὸν ἀγγεῖον καὶ σπογγισθῇ τὸ κακάβιν καὶ πάλιν βάλλῃς οἴνου λι ιε καὶ ἐκεῖνο τὸ ἔλαιον ἐπάνω. τὸ δὲ τριψίδιον ἔστω κιναμώμου ἀληθινοῦ λι γ γαλαγγὰν 𐆄 ϛ καρυοφύλλων 𐆄 δ στάχους 𐆄 γ ξανθοκαρύων 𐆄 γ λάδανον καθαρὸν 𐆄 γ τερεβίνθης 𐆄 ιη ξυλαλόης 𐆄 β κόστου 𐆄 δ ἀσάρου βουκελλαρίου λι δ θυμιάματος βασιλικοῦ 𐆄 γ. ταῦτα κόψας καὶ σείσας καὶ ἑνώσας μετὰ τοῦ ἐλαίου τῆς προεψήσεως, ἕψησον κατὰ πεῖραν, ἵνα μήτε καῦσις γένηται, μήτε πάλιν ἐνδεεστέρα ἡ ἕψησις.",
            "citation": {"start": "66.19", "end": "66.29"},
            "notes": ["Second nard formulation split from aetius-1-131."],
        },
        {
            "recipe_id": "aetius-1-131-5",
            "section": "131.5",
            "lemma": "Ναρδίνου σκευασία Ἰωάννου μυρεψοῦ",
            "text": "Ναρδίνου σκευασία Ἰωάννου μυρεψοῦ. Ἐλαίου ξ̸εϛ ἀσπαλάθου λίτραι δ ξυλοβαλσάμου λίτραι β κόστου 𐆄 γʹ ξυλοκασίας 𐆄 δ καρποβαλσάμου 𐆄 γʹ ἀμώμου 𐆄 γʹ στύρακος καλαμίτου 𐆄 β ὀποβαλσάμου 𐆄 β.",
            "citation": {"start": "66.30", "end": "66.33"},
            "notes": ["John-the-perfumer nard formulation split from aetius-1-131."],
        },
    ],
    "aetius-1-132": [
        {
            "recipe_id": "aetius-1-132",
            "section": "132",
            "text": "Ἐλαίου σαλκᾶ σκευασία. Ἐσκεύασα ταύτην ἐν Ἀλεξανδρείᾳ καί ἐστι πάνυ καλλίστη· ἀσπαλάθου 𐆄 ϛʹ ξυλοβαλσάμου 𐆄 θ κυπέρων 𐆄 δ ἑλενίου 𐆄 ϛʹ ἴρεως 𐆄 ϛʹ καλάμου γρ ιη σχοίνου ἄνθους 𐆄 βς στύρακος λιπαροῦ 𐆄 β κάρυα ἰνδικὰ β φύλλου γρ ιη ναρδοστάχυος 𐆄 α καρυοφύλλου 𐆄 ας ἀρνάβω 𐆄 ας ἀμώμου 𐆄 γʹ κασίας 𐆄 β κόστου 𐆄 α σμύρνης 𐆄 α ὕπνου 𐆄 γ ξυλοκασίας 𐆄 γ ἐλαίου ξ̸ει. ἕψεται δὲ τῷ προειρημένῳ τρόπῳ ἐπὶ τῆς νάρδου· ἐν τῇ πρώτῃ ἑψήσει ἐμβαλλομένων ξυλοβαλσάμου ἴρεως κυπέρου ἑλενίου ξυλοκασίας ἀποφλοισθέντων καὶ ἁδρομερῶς κοπέντων καὶ προβραχέντων ὕδατι ἐπὶ ἡμέρας β ἢ γ, ἐν δὲ τῇ δευτέρᾳ ἑψήσει ἐμβάλλεται κάλαμος σχοῖνος ὕπνον προνοτισθέντα οἴνῳ παλαιῷ εὐώδει, ἐν δὲ τῇ τρίτῃ τὰ λοιπά. γίγνεται δὲ καὶ δευτέριον οὕτως· τοῖς καταλειφθεῖσιν ἀπὸ τῆς τρίτης ἑψήσεως ἐπιβάλλονται ἐλαίου ξέσται ϛʹ καὶ ἕψεται ἐφ' ἱκανόν· εἶτα ἐπιβάλλονται στακτῆς καλῆς λευκῆς 𐆄 γʹ σειρώματος τουτέστι τὸ ὕδωρ τοῦ ὀποβαλσάμου 𐆄 ϛ μαστίχης 𐆄 ϛʹ στύρακος καλοῦ 𐆄 α. χρῶνται δὲ τῷ σαλκᾷ αἱ γυναῖκες τὰς κεφαλὰς ἀλείφουσαι. ἐστὶ δὲ ἡ εἰρημένη σκευασία πάνυ καλλίστη.",
            "citation": {"start": "67.1", "end": "67.17"},
            "notes": ["Primary salka-oil formulation split from the John-the-perfumer variant aetius-1-132-2."],
        },
        {
            "recipe_id": "aetius-1-132-2",
            "section": "132.2",
            "text": "Ἐλαίου σαλκᾶ σκευασία Ἰωάννου μυρεψοῦ. Κόστου 𐆄 ιβ φύλλου 𐆄 δ κασίας 𐆄 ϛʹ ζιγγιβέρεως 𐆄 ϛʹ ξυλοκαρυοφύλλου 𐆄 ϛʹ καρποβαλσάμου 𐆄 ϛʹ νάρδου στάχους 𐆄 δ καλάμου 𐆄 α ἴρεως 𐆄 ιβ στύρακος λιπαροῦ 𐆄 θ κρόκου 𐅻 δ ἐλαίου ξ̸ε ϛʹ.",
            "citation": {"start": "67.17", "end": "67.20"},
            "notes": ["John-the-perfumer salka-oil variant split from aetius-1-132."],
        },
    ],
}

REVISED_HEADING_RECIPE_IDS = (
    ("∆άφνινον", "aetius-1-108"),
    ("Οἰνάνθινον", "aetius-1-111"),
    ("Μήλινον", "aetius-1-112"),
    ("Ἔλαιον ῥόδινον", "aetius-1-113"),
    ("Κρίνινον", "aetius-1-116"),
    ("Ναρκίσσινον", "aetius-1-118"),
    ("Ἰασμή", "aetius-1-120"),
    ("Μυρσινάτον", "aetius-1-121"),
    ("Σικυώνιον", "aetius-1-124"),
    ("Μεγάλειον", "aetius-1-127"),
    ("Ἀμαράκινον", "aetius-1-128"),
    ("Κύπρινον", "aetius-1-129"),
    ("Νάρδου Κυζικηνῆς", "aetius-1-131"),
    ("Ἐλαίου σαλκᾶ", "aetius-1-132"),
    ("Φυλλίνου ἤτοι μαλαβαθρίνου", "aetius-1-133"),
    ("Καπνιστὸν ἔλαιον", "aetius-1-135"),
)

SPLIT_TEXT_TRANSFORMS = {
    "aetius-1-113": (
        (", κηρωτὴ ἡ ψύχουσα. Ῥόδινον", ""),
    ),
    "aetius-1-113-2": (
        ("ἐπιρραπτομένης", "ἐπιρριπτομένης"),
    ),
    "aetius-1-129-2": (
        ("κύπρου ἄνθους 𐆄 β βαλσάμου", "κύπρου ἄνθους 𐆄 ι βαλσάμου"),
    ),
    "aetius-1-131": (
        ("ἀμώμου φύλλου ναρδοστάχυος ἀνὰ 𐆄 β στύρακος", "ἀμώμου φύλλου ναρδοστάχυος ἀρναβῶ στύρακος"),
        ("δευτέριον", "δεύτερον"),
    ),
    "aetius-1-131-5": (
        ("καρποβαλσάμου 𐆄 γʹ", "καρποβαλσάμου 𐆄 ϛʹ"),
    ),
    "aetius-1-132": (
        ("στύρακος καλοῦ", "στύρακος καλαμίτου"),
    ),
    "aetius-1-132-2": (
        ("ζιγγιβέρεως", "σμύρνης"),
    ),
}


def citation_key(citation: str) -> tuple[int, int]:
    page, line = citation.split(".", 1)
    return int(page), int(line)


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def strip_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def normalize_match_key(text: str) -> str:
    return normalize_space(strip_diacritics(text).replace("ς", "σ").lower())


def tag_name(node: ET.Element) -> str:
    return node.tag.rsplit("}", 1)[-1]


def parse_page_from_xml_id(xml_id: str | None) -> str | None:
    if not xml_id:
        return None
    match = re.search(r"oliv-(\d+)(?:-\d+)?$", xml_id)
    if not match:
        return None
    return match.group(1)


def strip_trailing_punctuation(text: str) -> str:
    return text.rstrip(" .·;·:")


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


def slice_lines_by_citation(
    lines: list[dict[str, object]],
    *,
    start: str,
    end: str,
) -> list[dict[str, object]]:
    start_key = citation_key(start)
    end_key = citation_key(end)
    selected = [
        line
        for line in lines
        if start_key <= (int(str(line["page"])), int(str(line["line"]))) <= end_key
    ]
    if not selected:
        raise RuntimeError(f"Unable to recover lineation slice for citation {start}-{end}.")
    return selected


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
        if not text or not state["current_line"]:
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


def derive_title(text: str, chapter_number: str) -> str:
    flow = normalize_space(text)
    if flow.startswith("Ἔλαιον τὸ ἐκ"):
        return "Ἔλαιον"

    opening = flow[:160]
    punctuation_positions = [opening.find(mark) for mark in (".", "·", ":", ";")]
    punctuation_positions = [position for position in punctuation_positions if position > 0]
    first_punctuation = min(punctuation_positions) if punctuation_positions else None

    marker_positions = [(opening.find(marker), marker) for marker in TITLE_MARKERS if opening.find(marker) > 0]
    first_marker = min(marker_positions, default=None)

    if first_punctuation is not None and first_punctuation <= 35 and (
        first_marker is None or first_punctuation < first_marker[0]
    ):
        return strip_trailing_punctuation(opening[:first_punctuation])

    if first_marker is not None and first_marker[0] <= 100:
        return strip_trailing_punctuation(opening[: first_marker[0]])

    if first_punctuation is not None and first_punctuation <= 120:
        return strip_trailing_punctuation(opening[:first_punctuation])

    words = flow.split()
    fallback = " ".join(words[: min(len(words), 8)])
    if not fallback:
        raise RuntimeError(f"Could not derive a title for chapter {chapter_number}.")
    return strip_trailing_punctuation(fallback)


def parse_citation_token(token: str) -> tuple[str, str]:
    clean = token.strip().strip("[]")
    start, _, end = clean.partition("-")
    if not end:
        return start, start
    start_page, _ = start.split(".", 1)
    if "." not in end:
        return start, f"{start_page}.{end}"
    return start, end


def split_inline_note_fragments(citation_token: str, text: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(?=\[?\d+\.\d+(?:-(?:(?:\d+)\.)?\d+)?\])")
    pieces = [piece.strip() for piece in pattern.split(text) if piece.strip()]
    fragments: list[tuple[str, str]] = []
    for idx, piece in enumerate(pieces):
        match = NOTE_LINE_RE.match(piece)
        if match:
            end_line = match.group("end_line")
            token = f"[{match.group('start')}-{match.group('end_page') + '.' if match.group('end_page') else ''}{end_line}]" if end_line else f"[{match.group('start')}]"
            fragments.append((token, match.group("rest").strip()))
        elif idx == 0:
            fragments.append((citation_token, piece))
    return fragments


def parse_emendation_statement(citation_token: str, statement: str) -> dict[str, object] | None:
    normalized = normalize_space(statement.rstrip("."))
    if not any(keyword in normalized for keyword in (" replaces ", " omitted ", " added ", "rejecting Cala's suggestion")):
        return None

    start_citation, end_citation = parse_citation_token(citation_token)
    locus = f"[{citation_token.strip().strip('[]')}]"
    proposal_author = "Irene Cala"
    decision = "accepted"
    operation = None
    olivieri_text = None
    adopted_text = None
    note = None

    reject_match = re.match(r"rejecting Cala's suggestion of (.+?) for (.+)$", normalized)
    if reject_match:
        operation = "reject_suggestion"
        proposal_author = "Irene Cala"
        decision = "rejected"
        olivieri_text = reject_match.group(2)
        adopted_text = reject_match.group(2)
        note = f"Rejected suggestion: {reject_match.group(1)}"
    else:
        replace_match = re.match(r"(.+?) replaces (.+?)(?: (after .+|before .+|in .+|suggested by .+))?$", normalized)
        omit_match = re.match(r"(.+?) omitted (after .+|between .+)$", normalized)
        add_match = re.match(r"(.+?) added (after .+|before .+)$", normalized)
        if replace_match:
            operation = "replace"
            adopted_text = replace_match.group(1)
            olivieri_text = replace_match.group(2)
            note = replace_match.group(3)
            if note and "suggested by Coughlin" in note:
                proposal_author = "Sean Coughlin"
        elif omit_match:
            operation = "omit"
            olivieri_text = omit_match.group(1)
            adopted_text = None
            note = omit_match.group(2)
        elif add_match:
            operation = "add"
            adopted_text = add_match.group(1)
            olivieri_text = None
            note = add_match.group(2)
        else:
            return None

    return {
        "locus": locus,
        "start_citation": start_citation,
        "end_citation": end_citation,
        "operation": operation,
        "olivieri_text": olivieri_text,
        "adopted_text": adopted_text,
        "proposal_author": proposal_author,
        "decision": decision,
        "note": normalize_space(note) if note else normalized,
    }


def parse_revised_emendations() -> list[dict[str, object]]:
    lines = REVISED_NOTES.read_text(encoding="utf-8").splitlines()
    notes: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        match = NOTE_LINE_RE.match(stripped)
        if not match:
            index += 1
            continue
        rest = match.group("rest").strip()
        if not rest:
            index += 1
            continue
        continuation: list[str] = []
        look_ahead = index + 1
        while look_ahead < len(lines):
            next_stripped = lines[look_ahead].strip()
            if not next_stripped or NOTE_LINE_RE.match(next_stripped) or HEADING_RE.match(next_stripped):
                break
            continuation.append(next_stripped)
            look_ahead += 1
        combined = normalize_space(" ".join([rest, *continuation]))
        end_line = match.group("end_line")
        citation_token = f"[{match.group('start')}-{match.group('end_page') + '.' if match.group('end_page') else ''}{end_line}]" if end_line else f"[{match.group('start')}]"
        for token, fragment in split_inline_note_fragments(citation_token, combined):
            note = parse_emendation_statement(token, fragment)
            if note:
                notes.append(note)
        index = look_ahead if continuation else index + 1
    return notes


def join_editorial_lines(lines: list[str]) -> str:
    chunks: list[str] = []
    for line in lines:
        text = normalize_space(INLINE_PAGE_MARKER_RE.sub("", line))
        if not text:
            continue
        if chunks and chunks[-1].endswith(HYPHEN_CHARS):
            chunks[-1] = chunks[-1][:-1] + text
        else:
            chunks.append(text)
    return normalize_space(" ".join(chunks))


def resolve_revised_block_recipe_id(heading_body: str) -> str:
    for prefix, recipe_id in REVISED_HEADING_RECIPE_IDS:
        if heading_body.startswith(prefix):
            return recipe_id
    raise KeyError(f"Unmapped revised heading: {heading_body}")


def parse_revised_blocks() -> dict[str, str]:
    blocks: dict[str, list[str]] = {}
    current_recipe_id: str | None = None
    current_lines: list[str] = []
    skipping_note = False

    def flush() -> None:
        nonlocal current_recipe_id, current_lines
        if current_recipe_id and current_lines:
            blocks[current_recipe_id] = current_lines[:]
        current_recipe_id = None
        current_lines = []

    for raw_line in REVISED_NOTES.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            flush()
            current_recipe_id = resolve_revised_block_recipe_id(heading_match.group("body"))
            current_lines = [heading_match.group("body")]
            skipping_note = False
            continue
        if current_recipe_id is None:
            continue
        if not stripped:
            skipping_note = False
            continue
        if stripped.isdigit() or RANGE_HEADER_RE.match(stripped):
            continue
        note_match = NOTE_LINE_RE.match(stripped)
        if note_match:
            if note_match.group("rest").strip():
                skipping_note = True
            continue
        if skipping_note:
            continue
        current_lines.append(stripped)
    flush()
    return {recipe_id: join_editorial_lines(lines) for recipe_id, lines in blocks.items()}


def transform_split_text(recipe_id: str, text: str) -> str:
    updated = text
    for old, new in SPLIT_TEXT_TRANSFORMS.get(recipe_id, ()):
        if old not in updated:
            raise RuntimeError(f"Missing expected split-text segment for {recipe_id}: {old}")
        updated = updated.replace(old, new, 1)
    return updated


def normalize_revised_quantity_display(text: str) -> str:
    updated = text
    updated = REVISED_NUMERAL_MARK_RE.sub("", updated)
    updated = REVISED_NUMERAL_SIGMA_RE.sub(lambda match: f"{match.group(1)}ς", updated)
    updated = REVISED_XESTES_RE.sub(lambda match: f"ξ̸ε {match.group(1)}", updated)

    def replace_signed_numeral(match: re.Match[str]) -> str:
        sign = match.group(1)
        numeral = match.group(2)
        replacement = {
            "Γ": "𐆄",
            "Χ": "Χ",
            "<": "𐅻",
        }[sign]
        return f"{replacement} {numeral}"

    updated = REVISED_SIGNED_NUMERAL_RE.sub(replace_signed_numeral, updated)
    updated = ARABIC_DIGITS_AFTER_WORD_RE.sub("", updated)
    updated = ARABIC_STANDALONE_DIGITS_RE.sub("", updated)
    updated = SPACE_BEFORE_PUNCTUATION_RE.sub(r"\1", updated)
    return normalize_space(updated)


def extract_chapter(chapter: ET.Element, current_page: str | None) -> tuple[dict[str, object], str | None]:
    chapter_lines, current_page = collect_lines(list(chapter), current_page)
    flow_text = join_flow_text(chapter_lines)
    chapter_number = chapter.get("n", "")
    chapter_name = derive_title(flow_text, chapter_number)

    payload = {
        "id": f"aetius-1-{chapter_number}",
        "book": "1",
        "chapter": chapter_number,
        "section": chapter_number,
        "cts": chapter.get(f"{XML_NS}base"),
        "lemma": chapter_name,
        "chapter_name": chapter_name,
        "text": flow_text,
        "olivieri": build_lineation(chapter_lines),
    }
    return payload, current_page


def expand_entry_payloads(entry: dict[str, object]) -> list[dict[str, object]]:
    recipe_id = str(entry["id"])
    split_specs = AETIUS_BOOK1_ENTRY_SPLITS.get(recipe_id)
    if not split_specs:
        return [entry]

    chapter_lines = list(entry["olivieri"]["lines"])
    expanded: list[dict[str, object]] = []
    for spec in split_specs:
        split_entry = {
            "id": spec["recipe_id"],
            "book": entry["book"],
            "chapter": entry["chapter"],
            "cts": entry["cts"],
            "lemma": spec.get("lemma", entry["lemma"]),
            "chapter_name": spec.get("chapter_name", entry["chapter_name"]),
            "text": spec.get("text", entry["text"]),
            "olivieri": build_lineation(
                slice_lines_by_citation(
                    chapter_lines,
                    start=spec["citation"]["start"],
                    end=spec["citation"]["end"],
                )
            ),
        }
        section = spec.get("section", entry.get("section"))
        if section is not None:
            split_entry["section"] = section
        if spec.get("notes"):
            split_entry["notes"] = list(spec["notes"])
        expanded.append(split_entry)
    return expanded


def load_target_chapters() -> list[ET.Element]:
    tree = ET.parse(SOURCE_XML)
    root = tree.getroot()
    chapters: list[ET.Element] = []
    for chapter in root.findall(".//tei:div[@subtype='chapter']", NS):
        number = chapter.get("n")
        if not number or not number.isdigit():
            continue
        if int(PROEMIUM_CHAPTER) <= int(number) <= ENTRY_END:
            chapters.append(chapter)
    return chapters


def span_length(citation: dict[str, str]) -> int:
    start_page, start_line = citation_key(citation["start"])
    end_page, end_line = citation_key(citation["end"])
    return (end_page - start_page) * 100 + (end_line - start_line)


def note_overlaps_entry(note: dict[str, object], entry: dict[str, object]) -> bool:
    note_start = citation_key(str(note["start_citation"]))
    note_end = citation_key(str(note["end_citation"]))
    entry_start = citation_key(str(entry["olivieri"]["citation"]["start"]))
    entry_end = citation_key(str(entry["olivieri"]["citation"]["end"]))
    return note_start <= entry_end and note_end >= entry_start


def assign_emendations_to_entries(
    entries: list[dict[str, object]],
    notes: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    by_recipe: dict[str, list[dict[str, object]]] = defaultdict(list)
    for note in notes:
        candidates = [entry for entry in entries if note_overlaps_entry(note, entry)]
        if not candidates:
            continue
        chosen = min(candidates, key=lambda entry: span_length(entry["olivieri"]["citation"]))
        by_recipe[str(chosen["id"])].append(note)
    for recipe_id in by_recipe:
        by_recipe[recipe_id].sort(key=lambda item: citation_key(str(item["start_citation"])))
    return by_recipe


def finalize_entry(
    entry: dict[str, object],
    *,
    revised_blocks: dict[str, str],
    emendations_by_recipe: dict[str, list[dict[str, object]]],
) -> dict[str, object]:
    recipe_id = str(entry["id"])
    original_text = normalize_space(str(entry["text"]))
    emended_text = original_text
    recipe_emendations = [dict(item) for item in emendations_by_recipe.get(recipe_id, [])]
    has_accepted_change = any(item["decision"] == "accepted" for item in recipe_emendations)
    if recipe_id in revised_blocks and recipe_id not in SPLIT_TEXT_TRANSFORMS and has_accepted_change:
        emended_text = normalize_revised_quantity_display(revised_blocks[recipe_id])
    elif recipe_id in SPLIT_TEXT_TRANSFORMS:
        emended_text = transform_split_text(recipe_id, original_text)

    entry["original_text"] = original_text
    entry["text"] = emended_text
    entry["text_source"] = "emended" if emended_text != original_text else "olivieri"
    entry["emendations"] = recipe_emendations
    entry["emendation_count"] = len(entry["emendations"])
    return entry


def build_emendation_overlay(entries: list[dict[str, object]]) -> dict[str, object]:
    recipes: dict[str, dict[str, object]] = {}
    for entry in entries:
        if entry["emendation_count"] == 0 and entry["text_source"] == "olivieri":
            continue
        recipes[str(entry["id"])] = {
            "emended_text": entry["text"],
            "text_source": entry["text_source"],
            "emendations": entry["emendations"],
            "emendation_count": entry["emendation_count"],
        }
    return {
        "source_file": str(REVISED_NOTES.relative_to(REPO_ROOT)),
        "edition": "Olivieri",
        "recipes": recipes,
    }


SPLIT_PARENT_IDS = set(AETIUS_BOOK1_ENTRY_SPLITS)
SPLIT_ENTRY_IDS = {
    spec["recipe_id"]
    for recipe_id, split_specs in AETIUS_BOOK1_ENTRY_SPLITS.items()
    if recipe_id.startswith("aetius-1-")
    and recipe_id.count("-") == 2
    and split_specs
    and ENTRY_START <= int(recipe_id.rsplit("-", 1)[-1]) <= ENTRY_END
    for spec in split_specs
}
EXPECTED_ENTRY_COUNT = (ENTRY_END - ENTRY_START + 1) + sum(
    len(split_specs) - 1
    for recipe_id, split_specs in AETIUS_BOOK1_ENTRY_SPLITS.items()
    if recipe_id.startswith("aetius-1-")
    and recipe_id.count("-") == 2
    and split_specs
    and ENTRY_START <= int(recipe_id.rsplit("-", 1)[-1]) <= ENTRY_END
)


def build_output() -> tuple[dict[str, object], dict[str, object]]:
    chapters = load_target_chapters()
    chapter_numbers = [chapter.get("n") for chapter in chapters]
    expected_numbers = [str(number) for number in range(int(PROEMIUM_CHAPTER), ENTRY_END + 1)]
    if chapter_numbers != expected_numbers:
        raise RuntimeError(f"Unexpected chapter sequence: {chapter_numbers}")

    current_page: str | None = None
    proemium: list[dict[str, object]] = []
    entries: list[dict[str, object]] = []

    for chapter in chapters:
        payload, current_page = extract_chapter(chapter, current_page)
        if payload["chapter"] == PROEMIUM_CHAPTER:
            proemium.append(payload)
        else:
            entries.extend(expand_entry_payloads(payload))

    revised_blocks = parse_revised_blocks()
    revised_notes = parse_revised_emendations()
    emendations_by_recipe = assign_emendations_to_entries(entries, revised_notes)
    entries = [
        finalize_entry(
            entry,
            revised_blocks=revised_blocks,
            emendations_by_recipe=emendations_by_recipe,
        )
        for entry in entries
    ]

    try:
        entries = attach_viewer_entity_groups(entries)
    except KeyError:
        for entry in entries:
            entry["derived_recipe_id"] = entry["id"]
            entry["entity_groups"] = {
                "labels": [],
                "ingredients": [],
                "processes": [],
                "tools": [],
                "other_preparations_mentioned": [],
                "people": [],
                "places": [],
                "works_mentioned": [],
                "preparation_names": [],
            }

    pages: list[str] = []
    for item in proemium + entries:
        for page in item["olivieri"]["pages"]:
            if page not in pages:
                pages.append(page)

    data = {
        "source": {
            "xml_file": str(SOURCE_XML.relative_to(REPO_ROOT)),
            "revised_notes_file": str(REVISED_NOTES.relative_to(REPO_ROOT)),
            "xml_line_range": {"start": 913, "end": 1103},
            "requested_chapter_range": {"start": "99", "end": "136"},
            "effective_chapter_range": {"proemium": "100", "entries_start": "101", "entries_end": "136"},
            "edition": "Olivieri",
            "display_text": "emended where revised notes adopt a change; otherwise Olivieri",
        },
        "work": {
            "author": "Aëtius of Amida",
            "work": "Libri medicinales",
            "book": "1",
            "chapter_range": {"proemium": "100", "entries_start": "101", "entries_end": "136"},
            "cts": "urn:cts:greekLit:tlg0718.tlg001.aos-grc1:1.100-136",
            "chapter_name": proemium[0]["chapter_name"],
            "page_span": pages,
        },
        "proemium": proemium,
        "entries": entries,
    }
    overlay = build_emendation_overlay(entries)
    return data, overlay


def build_qc_report(data: dict[str, object], overlay: dict[str, object]) -> dict[str, object]:
    entries = data["entries"]
    actual_entry_ids = [entry["id"] for entry in entries]
    expected_chapters = [str(number) for number in range(ENTRY_START, ENTRY_END + 1)]
    actual_chapters = [entry["chapter"] for entry in entries]
    missing_chapters = [chapter for chapter in expected_chapters if chapter not in actual_chapters]

    return {
        "book": "1",
        "proemium_chapters": [entry["chapter"] for entry in data["proemium"]],
        "entry_count": len(entries),
        "expected_entry_count": EXPECTED_ENTRY_COUNT,
        "expected_chapters": expected_chapters,
        "actual_chapters": actual_chapters,
        "missing_chapters": missing_chapters,
        "split_entry_ids": sorted(entry_id for entry_id in actual_entry_ids if entry_id in SPLIT_ENTRY_IDS),
        "entries_missing_lemma": [entry["chapter"] for entry in entries if not entry["lemma"]],
        "entries_missing_text": [entry["chapter"] for entry in entries if not entry["text"]],
        "entries_missing_lines": [entry["chapter"] for entry in entries if not entry["olivieri"]["lines"]],
        "entries_missing_pages": [entry["chapter"] for entry in entries if not entry["olivieri"]["pages"]],
        "entries_missing_original_text": [entry["chapter"] for entry in entries if not entry.get("original_text")],
        "entries_with_emended_text": [entry["id"] for entry in entries if entry["text_source"] == "emended"],
        "entries_with_editorial_notes_only": [
            entry["id"]
            for entry in entries
            if entry["text_source"] == "olivieri" and entry["emendation_count"] > 0
        ],
        "overlay_recipe_count": len(overlay["recipes"]),
        "page_span": data["work"]["page_span"],
        "status": "ok"
        if data["proemium"]
        and [entry["chapter"] for entry in data["proemium"]] == [PROEMIUM_CHAPTER]
        and len(entries) == EXPECTED_ENTRY_COUNT
        and not missing_chapters
        and set(SPLIT_ENTRY_IDS).issubset(actual_entry_ids)
        and not any(
            [
                [entry["chapter"] for entry in entries if not entry["lemma"]],
                [entry["chapter"] for entry in entries if not entry["text"]],
                [entry["chapter"] for entry in entries if not entry["olivieri"]["lines"]],
                [entry["chapter"] for entry in entries if not entry["olivieri"]["pages"]],
                [entry["chapter"] for entry in entries if not entry.get("original_text")],
            ]
        )
        else "needs_review",
    }


def main() -> None:
    data, overlay = build_output()
    qc = build_qc_report(data, overlay)
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT_JSON.write_text(json_text + "\n", encoding="utf-8")
    OUTPUT_JS.write_text(f"window.AETIUS_BOOK1_CH99_136_DATA = {json_text};\n", encoding="utf-8")
    EMENDATION_JSON.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QC_REPORT.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_JS.relative_to(REPO_ROOT)}")
    print(f"Wrote {EMENDATION_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {QC_REPORT.relative_to(REPO_ROOT)}")
    print(f"Entries: {qc['entry_count']}")
    print(f"Emended entries: {len(qc['entries_with_emended_text'])}")
    print(f"QC status: {qc['status']}")


if __name__ == "__main__":
    main()
