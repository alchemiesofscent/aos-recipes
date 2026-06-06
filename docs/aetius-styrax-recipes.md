# Aetius of Amida — Recipes Containing Styrax

Every recipe in the Aetius corpus that calls for styrax (στύραξ) as an ingredient, rendered with the original Greek, a literal English translation, and an enumerated ingredient list with normalized quantities.

**Scope:** 31 recipes — 7 from Book 1 (oils, ed. Olivieri) and 24 from Book 16 (myrepsika — perfumes and incenses, ed. Zervos). Generated from `data/recipes/aetius-*.json` via `scripts/extract_styrax_recipes.py`; translations are hand-written and not auto-regenerated.

## Translation conventions

Ingredients are rendered using a fixed glossary so that the same Greek lemma appears as the same English term across all recipes:

| Greek | English |
| --- | --- |
| στύραξ | styrax |
| στύραξ λιπαρός | fatty styrax |
| στύραξ καλαμίτης | reed-grade styrax (styrax calamites) |
| στύραξ πρωτεῖος | first-quality styrax |
| στύραξ χυμάτιος | liquid styrax |
| στύραξ ἄσπρος | white styrax |
| ναρδόσταχυς | spikenard |
| φύλλον | malabathron-leaf |
| ἄμωμον | amomum |
| κρόκος | saffron |
| καρυόφυλλον / καρυόφυλλα | clove(s) |
| καρποβάλσαμον | balsam-fruit |
| ὀποβάλσαμον | balsam-juice |
| ξυλοβάλσαμον | balsam-wood |
| κόστος | costus |
| ὄνυξ | onycha |
| ἄσαρον | asaron |
| ἀλόη | aloe |
| μαστίχη | mastic |
| λάδανον | ladanum |
| μόσχος | musk |
| ἄμβαρ | ambergris |
| ῥόδα χλωρά | fresh roses |
| ἔλαιον | olive oil |
| γλυκὺ ἔλαιον | sweet olive oil |
| μέλι (ἀττικόν) | (Attic) honey |
| οἶνος εὐώδης | fragrant wine |
| χυλὸς ῥόδων | rose-juice |
| κάλαμος ἰνδικός | Indian reed (sweet flag) |
| κάρυα ἰνδικά | Indian nuts |
| σανδαράχη | sandarach |
| ἀρναβώ | arnabo |

Units are kept in their Latin/Greek metrological forms (`uncia`, `litra`, `xestes`, `drachme`, `gramma`, `scripula`, `ceration`, `count`). Distributive ἀνά is rendered as a trailing **each**. `q.s.` = *quantum sufficit*, the standard pharmacist's rendering of τὸ ἀρκοῦν / τὸ ἱκανόν. Ingredients flagged `(uncertain)` reflect a low-confidence reading in the upstream entity-review pass.

**A note on fractional numerals.** The compressed Byzantine numeral `αζʹ` (and its kin `βζʹ`, `γζʹ`, …) follows the pharmacological half-marker convention: a unit-digit followed by `ζʹ` reads as *digit + ½* — so `γοαζʹ = 1½ uncia`, `γοβζʹ = 2½ uncia`, and so on. This is distinct from the additive numeral reading (e.g. `ιζʹ = 17`) because additive 8 would canonically be written as the single letter `η`; the redundant `αζ` form *is* the half-marker signal. The reading is confirmed in-text at 16-139, where the scribe writes `ξεαζʹ. ἤτοι ξέστ. α καὶ ἥμισ.` ("1½ xestes, i.e. one xestes and a half"). This convention is applied by `scripts/normalize_quantities.py` (`parse_half_suffix_numeral`).

## Book 1 — Oils (ed. Olivieri)

### `aetius-1-123` — Στυράκινον

**Citation:** Olivieri 62.19 – 62.23

**Greek:**

> Στυράκινον σκευάζεται οὕτως· γλυκέος ἐλαίου καλλίστου ξ̸εʹ εἷς, στύρακος λιπαροῦ 𐆄 β. ἑψηθέντα δὲ ἐν διπλώματι ἐναποτίθεται τῷ ἐλαίῳ τὴν τοῦ στύρακος δύναμιν. θερμότερον δέ ἐστιν ἐπ' ὀλίγον τοῦτο τοῦ ἀνηθίνου, μαλακτικὸν δέ ἐστι σφόδρα καὶ διὰ τοῦτο ἁπαλύνει τὰ ἐσκληρυσμένα τῶν σωμάτων γενναίως.

**Translation:**

> Styrax-oil is prepared thus: of finest sweet olive oil, 1 xestes; of fatty styrax, 2 uncia. Boiled together in a double-vessel (bain-marie), the virtue of the styrax is deposited into the oil. It is a little warmer than dill-oil, but exceedingly emollient, and on this account it nobly softens hardened parts of the body.

**Ingredients:**

1. **γλυκὺ ἔλαιον** — 1 xestes
2. **στύραξ λιπαρός** — 2 uncia

### `aetius-1-131` — Νάρδου Κυζικηνῆς σκευασία

**Citation:** Olivieri 65.4 – 66.4

**Greek:**

> Νάρδου Κυζικηνῆς σκευασία. Ἐσκεύασα ταύτην ἐν Ἀλεξανδρείᾳ πλειστάκις καί ἐστι πάνυ καλή· ἐλαίου ὀμφακίζοντος ξ̸ειβ ἰταλικοί, ἀσπαλάθου κυπέρων ἴρεως ἰλλυρικῆς καρδαμώμου σπέρμα ἀριστολοχίας μακρᾶς ξυλοκασίας ἀνὰ 𐆄 ιβ ἑλενίου ξυλοβαλσάμου σχοίνου ἄνθους κασίας κόστου ἀνὰ 𐆄 ϛʹ ἀμώμου φύλλου ναρδοστάχυος ἀρναβῶ στύρακος καρποβαλσάμου ἀνὰ 𐆄 γʹ ὀποβαλσάμου 𐆄 γʹ βράθυος 𐆄 α. σκευάζεται δὲ οὕτως· ἀσπάλαθον κύπερον ἑλένιον ξυλοβάλσαμον ἶριν ἀριστολοχίαν ἀποφλοιώσας κόψας ἁδρομερῶς βρέχε ἡμέρας γ ὕδατι θερμῷ, ἔπειτα ἐπιβάλλων τὸ ἔλαιον ἕψε κινῶν συνεχῶς ἐπιβάλλων ὕδωρ κατὰ βραχὺ πρὸς ὃ τὸ πρῶτον ἀναλίσκεται, εἶτα ἑψήσας ἐπὶ ὥρας γ ἢ καὶ πλέον σκεπάσας ἔα διανυκτερεῦσαι· τῇ δὲ ἑξῆς ἀνασπάσας τὰ ἤδη ἑψηθέντα καὶ ἀποχωρίσας τοῦ ἐλαίου τὸ ὕδωρ, εἶτ' ἐπιβαλὼν ἕτερον ὕδωρ καὶ οἴνου βραχὺ ἕψε. ὅταν δὲ ἀναζέσῃ, ἐπίβαλλε πρῶτον καρδάμωμον εἶτα σχοῖνον ξυλοκασίαν κεκομμένα καὶ ἕψε ἐπὶ ὥρας β καὶ πάλιν ἔα διανυκτερεῦσαι. τῇ δὲ τρίτῃ ἀνασπάσας ὁμοίως καὶ ὕδωρ καθαρὸν ἐπιβαλὼν ἕψε καὶ ὅταν ἀναζέσῃ ἐπίπασσε λεῖα κατὰ μέρος κασίαν κόστον καὶ τὰ λοιπά, ἕκαστον κατ' ἰδίαν κοπέν. περὶ τὰ τελευταῖα δὲ νάρδου στάχυ καὶ φύλλον καὶ τὸν στύρακα εἰς λεπτὰ μόρια διαμερισθέντα, καὶ τακέντος αὐτοῦ ἆρον εὐθέως ἀπὸ τοῦ πυρὸς καὶ ἐπίβαλλε τὸ ὀποβάλσαμον καὶ ἀνακινήσας ἱκανῶς καὶ πωμάσας καὶ σκεπάσας καλῶς ἔα ἡμέρας β καὶ οὕτως μυακίῳ ἀναλάμβανε. τὸ δὲ δεύτερον σκευάζεται οὕτως· τοῖς καταλειφθεῖσιν ἐκ τῆς τρίτης ἑψήσεως ἐπίβαλλε ἐλαίου ξ̸ ϛʹ καὶ ἀναζέσας ἕψε ὥρας β, εἶτα ἐπίπασσε κασίας λειοτάτης 𐆄 β νάρδου κελτικῆς 𐆄 β βράθυος 𐅻 δ στύρακος 𐆄 α ὀποβαλσάμου 𐆄 β. ἐστὶ δὲ ἡ νάρδος δυνάμεως θερμαντικῆς τονωτικῆς παρηγορικῆς, στομάχῳ τοίνυν ἐψυγμένῳ καὶ ἀτόνῳ καὶ γαστρὶ καὶ ἥπατι τὰ αὐτὰ πεπονθόσιν ἐπιτηδειοτάτη. ἐνίεται καὶ ἐπὶ τῶν ψυγέντων τὰ ἔντερα καὶ ἐπὶ γυναικῶν τῇ μήτρα χρῶ ὡς πάνυ δοκίμῳ.

**Translation:**

> Preparation of Cyzicene nard-oil. I prepared this many times in Alexandria and it is very good. Unripe-olive oil, 12 Italian xestai; aspalathos, cyperus, Illyrian iris, cardamom-seed, long aristolochia, xylocassia, 12 uncia each; elenium, balsam-wood, schoenus-flower, cassia, costus, 6 uncia each; amomum, malabathron-leaf, spikenard, arnabo, styrax, balsam-fruit, 3 uncia each; balsam-juice, 3 uncia; savin, 1 uncia. It is prepared thus: strip the bark from the aspalathos, cyperus, elenium, balsam-wood, iris, and aristolochia, pound them coarsely, and soak them in hot water for 3 days; then pour in the oil and boil, stirring continuously and adding water little by little as the first lot is consumed; then, having boiled for 3 hours or more, cover the pot and leave it overnight. On the next day, lift out what has already been boiled, separate the water from the oil, then add fresh water and a little wine and boil. When it comes to a boil, add first the cardamom, then the schoenus and xylocassia (pounded), and boil for 2 hours; again leave overnight. On the third day, lift out likewise, add clean water, and boil; when it comes to a boil, sprinkle in, ground fine, in portions, the cassia, costus, and the rest — each pounded separately. Toward the very end, add the spikenard, malabathron-leaf, and the styrax broken up into fine pieces; and as soon as it melts, take the pot at once from the fire and add the balsam-juice. Stir well, stopper it, cover it thoroughly, and leave for 2 days; then take it up into a mussel-shell jar (myakion). A second batch is prepared thus: to what remains from the third boiling add 6 xestai of oil, bring it to a boil, and boil for 2 hours; then sprinkle in finest-ground cassia 2 uncia, Celtic nard 2 uncia, savin 4 drachmai, styrax 1 uncia, balsam-juice 2 uncia. Nard-oil is of warming, toning, and soothing virtue, and so most fit for a chilled and weakened stomach, and for the belly and liver afflicted with the same. It is also injected into chilled intestines, and used by women in the womb as a thoroughly approved remedy.

**Ingredients:**

1. **ἔλαιον ὀμφάκινον** — xestes
2. **ἀσπάλαθος** — 12 uncia
3. **κύπειρος** — 12 uncia
4. **ἶρις ἰλλυρική** — 12 uncia
5. **σπέρμα καρδαμώμου** — 12 uncia
6. **ἀριστολοχία μακρά** — 12 uncia
7. **ξυλοκασία** — 12 uncia
8. **ἑλένιον** — 6 uncia
9. **ξυλοβάλσαμον** — 6 uncia
10. **σχοίνου ἄνθος** — 6 uncia
11. **κασία** — 6 uncia
12. **κόστος** — 6 uncia
13. **ἄμωμον** — 2 uncia
14. **φύλλον** — 2 uncia _(uncertain)_
15. **ναρδοστάχυς** — 2 uncia
16. **ἀρναβώ** — 3 uncia _(uncertain)_
17. **στύραξ** — 3 uncia
18. **καρποβάλσαμον** — 3 uncia
19. **ὀποβάλσαμον** — 3 uncia
20. **βράθυ** — 1 uncia
21. **ὕδωρ** — (no amount specified)
22. **ὕδωρ** — (no amount specified)
23. **οἶνος** — (no amount specified)
24. **ὕδωρ** — (no amount specified)
25. **ἔλαιον** — xestes
26. **κασία** — 2 uncia
27. **νάρδος κελτική** — 2 uncia
28. **βράθυ** — drachme
29. **στύραξ** — 1 uncia
30. **ὀποβάλσαμον** — 2 uncia

### `aetius-1-131-5` — Ναρδίνου σκευασία Ἰωάννου μυρεψοῦ

**Citation:** Olivieri 66.30 – 66.33

**Greek:**

> Ναρδίνου σκευασία Ἰωάννου μυρεψοῦ. Ἐλαίου ξ̸εϛ ἀσπαλάθου λίτραι δ ξυλοβαλσάμου λίτραι β κόστου 𐆄 γʹ ξυλοκασίας 𐆄 δ καρποβαλσάμου 𐆄 ϛʹ ἀμώμου 𐆄 γʹ στύρακος καλαμίτου 𐆄 β ὀποβαλσάμου 𐆄 β.

**Translation:**

> Preparation of nard-oil by John the perfumer. Olive oil, 6 xestai; aspalathos, 4 litrai; balsam-wood, 2 litrai; costus, 3 uncia; xylocassia, 4 uncia; balsam-fruit, 6 uncia; amomum, 3 uncia; reed-grade styrax, 2 uncia; balsam-juice, 2 uncia.

**Ingredients:**

1. **ἔλαιον** — xestes
2. **ἀσπάλαθος** — 4 litra
3. **ξυλοβάλσαμον** — 2 litra
4. **κόστος** — 3 uncia
5. **ξυλοκασία** — 4 uncia
6. **καρποβάλσαμον** — 3 uncia
7. **ἄμωμον** — 3 uncia
8. **στύραξ καλαμίτης** — 2 uncia
9. **ὀποβάλσαμον** — 2 uncia

### `aetius-1-132` — Ἐλαίου σαλκᾶ σκευασία

**Citation:** Olivieri 67.1 – 67.17

**Greek:**

> Ἐλαίου σαλκᾶ σκευασία. Ἐσκεύασα ταύτην ἐν Ἀλεξανδρείᾳ καί ἐστι πάνυ καλλίστη· ἀσπαλάθου 𐆄 ϛʹ ξυλοβαλσάμου 𐆄 θ κυπέρων 𐆄 δ ἑλενίου 𐆄 ϛʹ ἴρεως 𐆄 ϛʹ καλάμου γρ ιη σχοίνου ἄνθους 𐆄 βς στύρακος λιπαροῦ 𐆄 β κάρυα ἰνδικὰ β φύλλου γρ ιη ναρδοστάχυος 𐆄 α καρυοφύλλου 𐆄 ας ἀρνάβω 𐆄 ας ἀμώμου 𐆄 γʹ κασίας 𐆄 β κόστου 𐆄 α σμύρνης 𐆄 α ὕπνου 𐆄 γ ξυλοκασίας 𐆄 γ ἐλαίου ξ̸ει. ἕψεται δὲ τῷ προειρημένῳ τρόπῳ ἐπὶ τῆς νάρδου· ἐν τῇ πρώτῃ ἑψήσει ἐμβαλλομένων ξυλοβαλσάμου ἴρεως κυπέρου ἑλενίου ξυλοκασίας ἀποφλοισθέντων καὶ ἁδρομερῶς κοπέντων καὶ προβραχέντων ὕδατι ἐπὶ ἡμέρας β ἢ γ, ἐν δὲ τῇ δευτέρᾳ ἑψήσει ἐμβάλλεται κάλαμος σχοῖνος ὕπνον προνοτισθέντα οἴνῳ παλαιῷ εὐώδει, ἐν δὲ τῇ τρίτῃ τὰ λοιπά. γίγνεται δὲ καὶ δευτέριον οὕτως· τοῖς καταλειφθεῖσιν ἀπὸ τῆς τρίτης ἑψήσεως ἐπιβάλλονται ἐλαίου ξέσται ϛʹ καὶ ἕψεται ἐφ' ἱκανόν· εἶτα ἐπιβάλλονται στακτῆς καλῆς λευκῆς 𐆄 γʹ σειρώματος τουτέστι τὸ ὕδωρ τοῦ ὀποβαλσάμου 𐆄 ϛ μαστίχης 𐆄 ϛʹ στύρακος καλαμίτου 𐆄 α. χρῶνται δὲ τῷ σαλκᾷ αἱ γυναῖκες τὰς κεφαλὰς ἀλείφουσαι. ἐστὶ δὲ ἡ εἰρημένη σκευασία πάνυ καλλίστη.

**Translation:**

> Preparation of salka-oil. I prepared this in Alexandria and it is the very finest. Aspalathos 6 uncia, balsam-wood 9 uncia, cyperus 4 uncia, elenium 6 uncia, iris 6 uncia, calamus 18 grammata, schoenus-flower 2½ uncia, fatty styrax 2 uncia, Indian nuts 2, malabathron-leaf 18 grammata, spikenard 1 uncia, clove 1½ uncia, arnabo 1½ uncia, amomum 3 uncia, cassia 2 uncia, costus 1 uncia, myrrh 1 uncia, hypnon-moss 3 uncia, xylocassia 3 uncia, olive oil 15 xestai. It is boiled in the manner described above for nard-oil: at the first boiling, balsam-wood, iris, cyperus, elenium, and xylocassia are thrown in — peeled, coarsely pounded, and pre-soaked in water for 2 or 3 days; at the second boiling, calamus, schoenus, and hypnon-moss (pre-moistened in old fragrant wine) are added; at the third, the rest. A second batch is likewise made: to what remains from the third boiling add 6 xestai of oil and boil until reduced; then add good white stakte 3 uncia, seiroma — that is, the watery fraction of balsam-juice — 6 uncia, mastic 6 uncia, reed-grade styrax 1 uncia. Women use salka-oil for anointing the head. The preparation described above is exceedingly fine.

**Ingredients:**

1. **ἀσπάλαθος** — 6 uncia
2. **ξυλοβάλσαμον** — 9 uncia
3. **κύπερος** — 4 uncia
4. **ἑλένιον** — 6 uncia
5. **ἴρις** — 6 uncia
6. **κάλαμος** — 18 gramma
7. **σχοίνου ἄνθος** — 2.5 uncia
8. **στύραξ λιπαρός** — 2 uncia
9. **κάρυον ἰνδικόν** — 2 count
10. **φύλλον** — 18 gramma
11. **ναρδοστάχυς** — 1 uncia
12. **καρυόφυλλον** — 1.5 uncia
13. **ἀρνάβω** — 1.5 uncia _(uncertain)_
14. **ἄμωμον** — 3 uncia
15. **κασία** — 2 uncia
16. **κόστος** — 1 uncia
17. **σμύρνα** — 1 uncia
18. **ὕπνος** — 3 uncia
19. **ξυλοκασία** — 3 uncia
20. **ἔλαιον** — 15 xestes
21. **ἔλαιον** — 6 xestes
22. **στακτὴ λευκή** — 3 uncia
23. **ὕδωρ τοῦ ὀποβαλσάμου** — 6 uncia
24. **μαστίχη** — 6 uncia
25. **στύραξ** — 1 uncia

### `aetius-1-132-2` — Ἐλαίου σαλκᾶ σκευασία

**Citation:** Olivieri 67.17 – 67.20

**Greek:**

> Ἐλαίου σαλκᾶ σκευασία Ἰωάννου μυρεψοῦ. Κόστου 𐆄 ιβ φύλλου 𐆄 δ κασίας 𐆄 ϛʹ σμύρνης 𐆄 ϛʹ ξυλοκαρυοφύλλου 𐆄 ϛʹ καρποβαλσάμου 𐆄 ϛʹ νάρδου στάχους 𐆄 δ καλάμου 𐆄 α ἴρεως 𐆄 ιβ στύρακος λιπαροῦ 𐆄 θ κρόκου 𐅻 δ ἐλαίου ξ̸ε ϛʹ.

**Translation:**

> Preparation of salka-oil by John the perfumer. Costus 12 uncia, malabathron-leaf 4 uncia, cassia 6 uncia, myrrh 6 uncia, xylocaryophyllon (clove-wood) 6 uncia, balsam-fruit 6 uncia, spikenard 4 uncia, calamus 1 uncia, iris 12 uncia, fatty styrax 9 uncia, saffron 4 drachmai, olive oil 5½ xestai.

**Ingredients:**

1. **κόστος** — 12 uncia
2. **φύλλον** — 4 uncia
3. **κασία** — 6 uncia
4. **σμύρνα** — 6 uncia
5. **ξυλοκαρυόφυλλον** — 6 uncia
6. **καρποβάλσαμον** — 6 uncia
7. **νάρδου στάχυς** — 4 uncia
8. **κάλαμος** — 1 uncia
9. **ἴρις** — 12 uncia
10. **στύραξ λιπαρός** — 9 uncia
11. **κρόκος** — 𐅻 δ drachme
12. **ἔλαιον** — 6 xestes

### `aetius-1-133` — Φυλλίνου ἤτοι μαλαβαθρίνου σκευασία καλλίστη

**Citation:** Olivieri 67.21 – 68.3

**Greek:**

> Φυλλίνου ἤτοι μαλαβαθρίνου σκευασία καλλίστη. Ἀσπαλάθου λίτρα ας ξυλοβαλσάμου λίτραι β κυπέρων λίτρα ας ἑλενίου λίτρα ας φύλλου 𐆄 δ ἀμώμου 𐆄 ϛ. ξυλοκασίας 𐆄 δ σμύρνης 𐆄 γ κόστου 𐆄 θ στύρακος πρωτείου λίτρα α κασάμου ἤτοι καρποβαλσάμου 𐆄 ϛʹ καλάμου λίτρα ας νάρδου στάχυος 𐆄 β καρυοφύλλου 𐆄 δʹ σειρώματος ὅ ἐστι κάθισμα ὑδατῶδες ὀποβαλσάμου 𐆄 ϛʹ ἀρνάβω 𐆄 ϛʹ καρδαμώμου 𐆄 ϛʹ ἴρεως λίτρα α ἐλαίου 𐅵 κ οἴνου εὐώδους τὸ ἀρκοῦν· ἕψε ὡς τὴν νάρδον.

**Translation:**

> Preparation of malabathron-leaf oil — also called malabathrinon — the finest. Aspalathos 1½ litrai, balsam-wood 2 litrai, cyperus 1½ litrai, elenium 1½ litrai, malabathron-leaf 4 uncia, amomum 6 uncia, xylocassia 4 uncia, myrrh 3 uncia, costus 9 uncia, first-quality styrax 1 litra, casamum (that is, balsam-fruit) 6 uncia, calamus 1½ litrai, spikenard 2 uncia, clove 4 uncia, seiroma — i.e. the watery residue — 6 uncia, balsam-juice 6 uncia, arnabo 6 uncia, cardamom 6 uncia, iris 1 litra, olive oil 20 (unit unresolved), fragrant wine q.s. (sufficient quantity). Boil as you would the nard-oil.

**Ingredients:**

1. **ἀσπάλαθος** — 1.5 litra
2. **ξυλοβάλσαμον** — 2 litra
3. **κύπειρος** — 1.5 litra
4. **ἑλένιον** — 1.5 litra
5. **φύλλον** — 4 uncia
6. **ἄμωμον** — 6 uncia
7. **ξυλοκασία** — 4 uncia
8. **σμύρνη** — 3 uncia
9. **κόστος** — 9 uncia
10. **στύραξ πρωτεῖος** — 1 litra
11. **κάσαμον ἤτοι καρποβάλσαμον** — 6 uncia
12. **κάλαμος** — 1.5 litra
13. **στάχυς νάρδου** — 2 uncia
14. **καρυόφυλλον** — 4 uncia
15. **σειρῶμα ὀποβαλσάμου** — 6 uncia
16. **ἀρνάβω** — 6 uncia _(uncertain)_
17. **καρδάμωμον** — 6 uncia
18. **ἶρις** — 1 litra
19. **ἔλαιον** — 20 (unit unresolved)
20. **οἶνος εὐώδης** — q.s. (sufficient quantity)

### `aetius-1-135` — Καπνιστὸν ἔλαιον

**Citation:** Olivieri 68.15 – 69.12

**Greek:**

> Καπνιστὸν ἔλαιον. Τὸ δὲ λεγόμενον καπνιστὸν ἔλαιον σκευάζεται οὕτως· ὀνύχων ἀρωματικῶν μεγάλων 𐆄 ε λιβάνου ἄρρενος στύρακος πρωτείου 𐆄 ε βδελλίου καθαροῦ 𐆄 ε κόστου 𐆄 ε ἐλαίου γλυκέος καλοῦ ξ̸ε ε ὕπνου τὸ ἀρκοῦν· τὸν <δὲ> κόστον εἰς ἁδρομερῆ μόρια διαμερίσας, καὶ τὸν στύρακα ὁμοίως καὶ τὸ βδέλλιον, εἶτ’ ἀναμίξας, ἅμα ἔμβαλε ἐν ξεστίῳ καινῷ ὀστρακίνῳ μὴ ἔχοντι ὠτίον· εἶτα σκεπάσας ποσῷ τὸ στόμιον ὕπνῳ καὶ ἔξωθεν τοῦ ὕπνου ξυλάρια ἀσπαλάθου ἤ τινος τῶν εὐωδῶν περιφράξας, ὥστε μὴ ἐκπεσεῖν τὰ ἐν τῷ ξεστίῳ, εἶτα ἕτερον ὀστράκινον ἀγγεῖον ἄωτον λαβὼν μακροτράχηλον στόμιον ἔχον ἁρμόδιον τῷ στομίῳ τῷ περιέχοντι τὰ εἰρημένα εἴδη, καὶ ἐμβαλὼν ἐν αὐτῷ ἐλαίου γλυκέος ξέστας ε καὶ ὀρύξας τὴν γῆν, χῶσον μέχρι τοῦ τραχήλου τὸ ἔχον τὸ ἔλαιον ἵνα μὴ πυρωθῇ, εἶτα ἐπικέφαλα λαβὼν τὸ ξεστίον καὶ ἁρμόσας αὐτὸ τῷ στομίῳ τοῦ ἔχοντος τὸ ἔλαιον, χρίε ἔξωθεν τὸ ξεστίον πηλῷ ὅλον κύκλῳ καὶ τὰ στόματα ἀμφοτέρων τὰ ἀλλήλοις ἡρμοσμένα καὶ ἐάσας ξηρανθῆναι, τῇ ἑξῆς κάρβωνας πολλοὺς ἐπιθεὶς καὶ σκεπάσας αὐτοῖς πάντοθεν τὸ ξεστίον, ἄναψον πῦρ καὶ ῥίπιζε. ἀναφθέντος δὲ τοῦ πυρός, ἔα αὐτὸ μαραίνεσθαι, ἵνα κατὰ βραχὺ πυρούμενα διὰ τοῦ στόματος τοῦ ξεστίου τὰ εἴδη καπνίσῃ τὸ ὑποκείμενον αὐτοῖς ἔλαιον· τούτου γὰρ χάριν καπνιστὸν ὀνομάζεται· εἶτα τῇ ἑξῆς ἀνοίξας ἀνελοῦ τὸ ἔλαιον καὶ φύλαττε ἐν ὑελίνῳ ἀγγείῳ καὶ χρῶ. τούτῳ χρῶνται αἱ γυναῖκες ἐφ’ ὧν ἐπίσχηται τὰ καταμήνια, χρίουσαι αὐτῷ τὸ ἦτρον καὶ τὴν ὀσφύν. ἁρμόδιον δέ ἐστι κἀπὶ τῶν μὴ κατὰ λόγον ἐν τοῖς τοκετοῖς καθαιρομένων ὁμοίως χριόμενον. χρήσιμον δὲ καὶ τοῖς τὸν θώρακα ἐψυγμένοις καὶ τεινεσμῶν ἐνοχλούντων ὠφέλιμον θερμὸν πτύγματι ἐρίου ἀναλαμβανόμενον καὶ ἐπιτιθέμενον ἤτρῳ καὶ ὀσφύι.

**Translation:**

> Smoked oil. The so-called smoked oil is prepared thus: large aromatic onycha, 5 uncia; male frankincense and first-quality styrax, 5 uncia; clean bdellium, 5 uncia; costus, 5 uncia; good sweet olive oil, 5 xestai; hypnon-moss q.s. (sufficient quantity). Divide the costus into coarse pieces, and likewise the styrax and the bdellium; mix them together and put them into a new earthenware pot (xestion) without a handle. Then partially cover the mouth with hypnon-moss, and around the moss pack small twigs of aspalathos or some other fragrant wood, so that what is inside the pot may not fall out. Then take another handle-less earthenware vessel, long-necked, with a mouth fitting that of the pot containing the above ingredients, pour into it 5 xestai of sweet olive oil, dig a hole in the ground, and sink the oil-vessel up to its neck so that it does not heat through. Then take the pot, invert it head-downwards over the mouth of the oil-vessel, joining the two mouths together; and smear the outside of the pot all around with clay, sealing the joined mouths of both vessels, and leave it to dry. The next day, heap many coals on top of and around the pot so that it is covered on every side; kindle a fire and fan it. Once the fire has caught, let it die down, so that, as the ingredients are slowly heated, smoke passes through the pot's mouth and smokes the oil beneath them — and for this reason it is called smoked oil. Then the next day open it, take out the oil, store it in a glass vessel, and use it. Women use it when their menstrual periods are suppressed, anointing the lower belly and loins with it. It is also fitting for those not being properly cleansed in childbirth, applied likewise. It is also useful for those with a chilled chest, and beneficial against tenesmus, applied warm, taken up in a fold of wool and placed on the belly and loins.

**Ingredients:**

1. **ὄνυχες ἀρωματικοὶ μεγάλοι** — 5 uncia
2. **λίβανος ἄρρην** — (no amount specified)
3. **στύραξ πρωτεῖος** — 5 uncia
4. **βδέλλιον καθαρόν** — 5 uncia
5. **κόστος** — 5 uncia
6. **ἔλαιον γλυκὺ καλόν** — 5 xestes

## Book 16 — Perfumes and incenses (ed. Zervos)

### `aetius-16-126-1` — ξηρόφρυκτον ὃ καλοῦσι βερεθρίας

**Citation:** Zervos 161.9 – 161.12

**Greek:**

> Ἀρναβῶ, ἀμώμου, ναρδοστάχυος ἀνὰ γογ. φύλλου στύρακος ὁμοίως. κρόκου, καρυοφύλλων ἀνὰ γοαζʹ. ὀποβαλσάμου γοστ. ῥόδων χλωρῶν γοκστ ἤτοι οὐγ. κστ.

**Translation:**

> Arnabo, amomum, spikenard — 3 uncia each. Malabathron-leaf and styrax — likewise. Saffron, cloves — 1½ uncia each. Balsam-juice — 6 uncia. Fresh roses — 26 uncia.

**Ingredients:**

1. **ἀρναβώ** — 3 uncia each _(uncertain)_
2. **ἄμωμον** — 3 uncia each
3. **ναρδόσταχυς** — 3 uncia each
4. **φύλλον** — (no amount specified)
5. **στύραξ** — (no amount specified)
6. **κρόκος** — 1.5 uncia each
7. **καρυόφυλλα** — 1.5 uncia each
8. **ὀποβάλσαμον** — 6 uncia
9. **ῥόδα χλωρά** — 26 uncia or 26 uncia

### `aetius-16-126-2` — ἄλλο μοσχάτον

**Citation:** Zervos 161.13 – 161.17

**Greek:**

> Φύλλων κασίας, κρόκου, στύρακος, ἀρναβῶ, ἀμώμου, ναρδοστάχυος ἀνὰ γοαζʹ. καρυοφύλλων δραχ. δ. μόσχου γράμματα γ. ὀποβαλσάμου γοα· ἐλαίου ἰνδικοῦ ἢ ἑτέρου γογ. ῥόδων ξηρῶν γοβ ἢ χλωρῶν γοδ.

**Translation:**

> Cassia-leaves, saffron, styrax, arnabo, amomum, spikenard — 1½ uncia each. Cloves, 4 drachmai. Musk, 3 grammata. Balsam-juice, 1 uncia. Indian oil (or another), 3 uncia. Dry roses, 2 uncia; or fresh roses, 4 uncia.

**Ingredients:**

1. **φύλλα κασίας** — 1.5 uncia
2. **κρόκος** — 1.5 uncia
3. **στύραξ** — 1.5 uncia
4. **ἀρναβώ** — 1.5 uncia _(uncertain)_
5. **ἄμωμον** — 1.5 uncia
6. **ναρδόσταχυς** — 1.5 uncia
7. **καρυόφυλλον** — 4 drachme
8. **μόσχος** — 3 gramma
9. **ὀποβάλσαμον** — 1 uncia
10. **ἔλαιον ἰνδικόν** — 3 uncia
11. **ἔλαιον ἕτερον** — 3 uncia _(uncertain)_
12. **ῥόδα ξηρά** — 2 uncia
13. **ῥόδα χλωρά** — 4 uncia _(uncertain)_

### `aetius-16-126-3` — σκευασία ἀραβικῶν ἢ λαιῶν

**Citation:** Zervos 161.18 – 161.26

**Greek:**

> Μασσουαφίου, καρυοφύλλων, κόστου, ἀνὰ γοβ. φύλλων ναρδοστάχυος, ῥόδων χυλοῦ, ἀνὰ γράμματα ιβ. ἀμώμου, στύρακος, ἀνὰ γοα. κόμμεως γοβ. κόψας καὶ σήσας τὰ ξηρὰ καὶ βρέξας τὸ κόμμι, ἔπειτα ὁλμοκοπήσας τὸν στύρακα καὶ ἑνώσας αὐτῷ τὰ ξηρὰ καλῶς, ἐπίβαλλε τὸ κόμμι καὶ ἀναλάμβανε τροχίσκους στρογγύλους ἔχοντας μέγεθος ἐρεβίνθου βεβρεγμένου, καὶ βελόνῃ διατρήσας καὶ διάρας σπαρτίῳ ἰσχυρῷ ξήραινε, καὶ δίδου φορεῖν περὶ τὸν τράχηλον.

**Translation:**

> Massouaphion, cloves, costus — 2 uncia each. Malabathron-leaves, spikenard, rose-juice — 12 grammata each. Amomum, styrax — 1 uncia each. Gum, 2 uncia. Pound and sift the dry ingredients and soak the gum; then crush the styrax in a mortar and blend it well with the dry ingredients; add the gum and form into round troches the size of a soaked chickpea. Pierce them with a needle, thread them on a strong cord, dry them, and give them to be worn around the neck.

**Ingredients:**

1. **μασσουάφιον** — 2 uncia each _(uncertain)_
2. **καρυόφυλλον** — 2 uncia each
3. **κόστος** — 2 uncia each
4. **φύλλα ναρδοστάχυος** — 12 gramma each
5. **χυλὸς ῥόδων** — 12 gramma each
6. **ἄμωμον** — 1 uncia each
7. **στύραξ** — 1 uncia each
8. **κόμμι** — 2 uncia

### `aetius-16-127-1` — ῥοδάτον ξηρόμυρον

**Citation:** Zervos 162.1 – 162.3

**Greek:**

> Ῥόδων ξηρῶν λίτρ. α. κόστου, φύλλου, καρυοφύλλων, ὕπνου, καλάμου ἀρωματικοῦ, ὀνύχων, στύρακος ἀνὰ γοβ.

**Translation:**

> Dry roses, 1 litra. Costus, malabathron-leaf, cloves, hypnon-moss, aromatic calamus, onycha, styrax — 2 uncia each.

**Ingredients:**

1. **ῥόδα ξηρά** — 1 litra
2. **κόστος** — 2 uncia each
3. **φύλλον** — 2 uncia each
4. **καρυόφυλλον** — 2 uncia each
5. **ὕπνος** — 2 uncia each
6. **κάλαμος ἀρωματικός** — 2 uncia each
7. **ὄνυξ** — 2 uncia each
8. **στύραξ** — 2 uncia each

### `aetius-16-127-2` — ἄλλο ξηρόμυρον

**Citation:** Zervos 162.3 – 162.6

**Greek:**

> Φύλλων ῥόδων ξηρῶν, ἀμώμου, κόστου, καρυοφύλλων, ναρδοστάχυος, χυλοῦ ἀρναβῶ, κρόκου, ἀνὰ γοα. ὕπνου, στύρακος, ὀποβαλσάμου ἀνὰ δραχ. δ.

**Translation:**

> Malabathron-leaves, dry roses, amomum, costus, cloves, spikenard, arnabo-juice, saffron — 1 uncia each. Hypnon-moss, styrax, balsam-juice — 4 drachmai each.

**Ingredients:**

1. **ξηρὰ φύλλα ῥόδων** — 1 uncia
2. **ἄμωμον** — 1 uncia
3. **κόστος** — 1 uncia
4. **καρυόφυλλα** — 1 uncia
5. **ναρδοστάχυς** — 1 uncia
6. **χυλὸς ἀρναβῶ** — 1 uncia
7. **κρόκος** — 1 uncia
8. **ὕπνος** — 4 drachme
9. **στύραξ** — 4 drachme
10. **ὀποβάλσαμον** — 4 drachme

### `aetius-16-128` — ἄλλο ξηρόμυρον τὸ καλούμενον λευκόφυλλον, ᾧ χρῶνται εἰς τοὺς τραχήλους καὶ ἐπὶ τὰς μασχάλας

**Citation:** Zervos 162.8 – 162.13

**Greek:**

> Γῆς σαμίας λίτ. α. στύρακος, φύλλου, ὀποβαλσάμου, ἀνὰ γοβ. τὸν στύρακα λείου μετὰ τοῦ ὀποβαλσάμου, τὸ δὲ φύλλον κόψας καὶ σήσας, εἶτα ἑνώσας πάντα ἐν τῇ θυίᾳ καλῶς, μίξον αὐτῷ χυλοῦ ῥόδων τὸ ἀρκοῦν καὶ χρῶ.

**Translation:**

> Samian earth, 1 litra. Styrax, malabathron-leaf, balsam-juice — 2 uncia each. Grind the styrax with the balsam-juice; pound and sift the malabathron-leaf; then blend everything well together in the mortar, mix in q.s. (sufficient quantity) of rose-juice, and use.

**Ingredients:**

1. **γῆ Σαμία** — 1 litra
2. **στύραξ** — 2 uncia
3. **φύλλον** — 2 uncia
4. **ὀποβάλσαμον** — 2 uncia
5. **χυλὸς ῥόδων** — q.s. (sufficient quantity)

### `aetius-16-129` — ὑγρομύρου σκευασία ᾧ χρῶνται εἰς τὰ ὦτα γυναῖκες

**Citation:** Zervos 162.14 – 162.17

**Greek:**

> Φύλλου, ναρδοστάχυος χυλοῦ, μαστίχης, καρυοφύλλου ἀνὰ γοα γράμματα ιβ. στύρακος λιπαροῦ, ὀποβαλσάμου ἀνὰ γοβ. κρόκου γράμματα στ. μόσχου γράμμα α. ἐλαίου σαλκᾶ πρωτείου γοδ.

**Translation:**

> Malabathron-leaf, spikenard-juice, mastic, clove — 1 uncia and 12 grammata each. Fatty styrax, balsam-juice — 2 uncia each. Saffron, 6 grammata. Musk, 1 gramma. First-quality salka-oil, 4 uncia.

**Ingredients:**

1. **φύλλον** — 1 uncia or 12 gramma
2. **χυλὸς ναρδοστάχυος** — 1 uncia or 12 gramma
3. **μαστίχη** — 1 uncia or 12 gramma
4. **καρυόφυλλον** — 1 uncia or 12 gramma
5. **στύραξ λιπαρός** — 2 uncia
6. **ὀποβάλσαμον** — 2 uncia
7. **κρόκος** — 6 gramma
8. **μόσχος** — 1 gramma
9. **ἔλαιον σαλκᾶ πρωτεῖον** — 4 uncia _(uncertain)_

### `aetius-16-130-1` — ἐλαίου σάλκα σκευασία πολυτελής

**Citation:** Zervos 162.18 – 163.6

**Greek:**

> Ἐλαίου ὀμφακίνου ξστκ ἤτοι ξέστ. κ. ἴρεως ἰλλυρικῆς λίτ. α. ἀμώμου γοστ ἤτοι οὐγ. στ. ἀσπαλάθου, ὕπνου ἀνὰ λίτ. α. δευτέρα ἕψησις. Καλάμου ἅλου λίτ. β. καρυοφύλλων, φύλλου, καρποβαλσάμου, ἀνὰ λίτ. α. ξυλοκασίας γοε. τρίτη ἕψησις. Κασίας γοδ. κόστου, στύρακος λιπαροῦ, κρόκου, ἀνὰ γοα. σμύρνης, ἀρναβῶ, ἀνὰ γογ. ναρδοστάχυος γοδ. ὕδατι ἕψε. ὁ δὲ τρόπος τῆς σκευασίας εἴρηται ἐν τῷ α λόγῳ περὶ τῆς τῶν ἐλαίων συνθέσεως, ἔνθα ἔχεις γεγραμμένην ἑτέραν γραφὴν καλλίστην ἐλαίου σαλκᾶ καὶ νάρδου μύρου σκευασίαν.

**Translation:**

> Unripe-olive oil, 20 xestai. Illyrian iris, 1 litra. Amomum, 6 uncia. Aspalathos and hypnon-moss — 1 litra each. *Second boiling.* Calamus alos, 2 litrai. Cloves, malabathron-leaf, balsam-fruit — 1 litra each. Xylocassia, 5 uncia. *Third boiling.* Cassia, 4 uncia. Costus, fatty styrax, saffron — 1 uncia each. Myrrh, arnabo — 3 uncia each. Spikenard, 4 uncia. Boil with water. The manner of the preparation is given in Book 1, in the section on the compounding of oils, where you also have written another excellent recipe for salka-oil and for the preparation of nard-oil.

**Ingredients:**

1. **ἔλαιον ὀμφάκινον** — 20 xestes or 20 xestes
2. **ἶρις Ἰλλυρική** — 1 litra
3. **ἄμωμον** — 6 uncia or 6 uncia
4. **ἀσπάλαθος** — 1 litra each
5. **ὕπνον** — 1 litra each _(uncertain)_
6. **κάλαμος ἅλος** — 2 litra _(uncertain)_
7. **καρυόφυλλον** — 1 litra each
8. **φύλλον** — 1 litra each
9. **καρποβάλσαμον** — 1 litra each
10. **ξυλοκασία** — 5 uncia
11. **κασία** — 4 uncia
12. **κόστος** — 1 uncia each
13. **στύραξ λιπαρός** — 1 uncia each
14. **κρόκος** — 1 uncia each
15. **σμύρνα** — 3 uncia each
16. **ἀρναβώ** — 3 uncia each _(uncertain)_
17. **ναρδόσταχυς** — 4 uncia

### `aetius-16-131-1` — φουλιάτου σκευασία

**Citation:** Zervos 163.17 – 163.20

**Greek:**

> Ὀποβαλσάμου λίτ. α. στύρακος, ἀμώμου ἀνὰ γογ. κασίας γοδ. κρίνα τὸν ἀριθμὸν κ. λέαινε ἅμα καὶ χρῶ. εἰ δὲ παχύτερον εἴη, ἔκλυε αὐτὸ μύρῳ σαλκᾶ.

**Translation:**

> Balsam-juice, 1 litra. Styrax, amomum — 3 uncia each. Cassia, 4 uncia. Lilies, 20 in number. Grind all together and use. If it should be too thick, thin it with salka-oil.

**Ingredients:**

1. **ὀποβάλσαμον** — 1 litra
2. **στύραξ** — 3 uncia
3. **ἄμωμον** — 3 uncia
4. **κασία** — 4 uncia
5. **κρίνα** — 20 count

### `aetius-16-131-2` — ἄλλη γραφὴ φουλιάτου

**Citation:** Zervos 163.21 – 163.25

**Greek:**

> Κηροῦ λιτ. α. νάρδου κυζικηνικοῦ λίτ. γ. πίσσης βρυτίας γοε. λαδάνου γοα. στύρακος λιπαροῦ γογ. κόστου, κασίας ἀνὰ γοβ. καρδαμώμου, φύλλου ἀνὰ γοα. ναρδοστάχυος γοα. τὸ ζʹ. ἤτοι τὸ ἥμισ. κρόκου, οἴνου ἀμιναίου ἀνὰ γοα. ὀποβαλσάμου γογ.

**Translation:**

> Wax, 1 litra. Cyzicene nard-oil, 3 litrai. Bruttian pitch, 5 uncia. Ladanum, 1 uncia. Fatty styrax, 3 uncia. Costus, cassia — 2 uncia each. Cardamom, malabathron-leaf — 1 uncia each. Spikenard, 1 uncia (the seventh — i.e. half). Saffron, Aminaean wine — 1 uncia each. Balsam-juice, 3 uncia.

**Ingredients:**

1. **κηρός** — 300 litra
2. **νάρδος κυζικηνική** — 3 litra
3. **πίσσα βρυτία** — 5 uncia
4. **λάδανον** — 1 uncia
5. **στύραξ λιπαρός** — 3 uncia
6. **κόστος** — 2 uncia each
7. **κασία** — 2 uncia each
8. **καρδάμωμον** — 1 uncia each
9. **φύλλον** — 1 uncia each
10. **ναρδοστάχυς** — 1 uncia
11. **κρόκος** — 1 uncia each
12. **οἶνος ἀμιναῖος** — 1 uncia each
13. **ὀποβάλσαμον** — 3 uncia

### `aetius-16-133-2` — ἑτέρα οἰνανθαρίου σκευασία

**Citation:** Zervos 164.20 – 165.12

**Greek:**

> Κόστου γοβ. κασίας, καρποβαλσάμου, μασσουαφίου, σμύρνης ἀνὰ γοα. ἀμώμου γοε. ναρδοστάχυος, στύρακος, ἀνὰ γοδ. καρυοφύλλου γοαζʹ. ὀποβαλσάμου γοστ. κρίνα τὸν ἀριθμὸν μ. οἴνου εὐώδους στύφοντος ξστιβ ἤτοι ξέστ. ιβ. ἁλῶν καππαδοκικῶν γοβ. Τὰ κρίνα ἀποφυλλίσας καὶ ἐκμάξας καθαρῶς ἅπαν τὸ ἐν αὐτοῖς κροκῶδες, ψύχε ἐν σκιᾷ ἐν σινδόνι καθαρᾷ ἡμέραν καὶ νύκτα, ὥστε μαρανθῆναι· εἶτα κόψας καὶ σήσας τὰ ξηρὰ, καὶ λεάνας τὴν σμύρναν μετ' οἴνου ἐν θυίᾳ, εἶτα ἐπιβαλὼν καὶ τὰ ξηρὰ πάντα καὶ διαλύσας τῷ οἴνῳ, τὸν δὲ στύρακα εἰς λεπτότατα τοῖς δακτύλοις διαμερίσας ἐπίβαλλε αὐτοῖς, καὶ ἑνώσας αὐτὰ ἐπίχεε τῷ ὀποβαλσάμῳ. ἑνωθέντων δὲ ἱκανῶς, τὰ φύλλα τῶν κρίνων ἐμβαλὼν ἐν τῇ θυίᾳ καὶ ἀναφυρῶν ταῖς χερσὶν, ἀναλάμβανε τοῖς κρίνοις τὰ λειωθέντα, καὶ ἐμβαλὼν ἐν βικίῳ ἀνατάρασσε, καὶ τὸν οἶνον ὁμοίως ἐν αὐτῷ τῷ βικίῳ ἐμβαλὼν ὕστερον ἀνατάρασσε· καὶ οὕτως πωμάσας βρύῳ ἢ ὕπνῳ, καὶ ἐπιδήσας καὶ χρίσας ἀςφαλῶς, τίθει ἐν ἡλίῳ ἡμέρας μ καὶ χρῶ.

**Translation:**

> Costus, 2 uncia. Cassia, balsam-fruit, massouaphion, myrrh — 1 uncia each. Amomum, 5 uncia. Spikenard, styrax — 4 uncia each. Clove, 1½ uncia. Balsam-juice, 6 uncia. Lilies, 40 in number. Fragrant astringent wine, 12 xestai. Cappadocian salt, 2 uncia. Strip the petals from the lilies, wipe clean every saffron-colored part within them, and let them wither in the shade on a clean linen cloth for a day and a night. Then pound and sift the dry ingredients; grind the myrrh in a mortar with wine; then add all the dry ingredients and dissolve them in the wine. Break the styrax into the finest pieces with the fingers and add to them; mix together, then pour in the balsam-juice. When all is well united, throw the lily-petals into the mortar, knead with the hands, take up the ground mixture with the petals, put it in a jar (bikion) and shake. Likewise pour in the wine into the same jar and shake after. Then stopper the jar with bryon-moss or hypnon-moss, bind it up, seal it firmly, set it in the sun for 40 days, and use.

**Ingredients:**

1. **κόστος** — 2 uncia
2. **κασία** — 1 uncia each
3. **καρποβάλσαμον** — 1 uncia each
4. **μασσουάφιον** — 1 uncia each
5. **σμύρνα** — 1 uncia each
6. **ἄμωμον** — 5 uncia
7. **ναρδοστάχυς** — 4 uncia each
8. **στύραξ** — 4 uncia each
9. **καρυόφυλλον** — 1.5 uncia
10. **ὀποβάλσαμον** — 6 uncia
11. **κρίνον** — 40 count
12. **οἶνος εὐώδης στύφων** — 12 xestes
13. **ἅλες καππαδοκικοί** — 2 uncia

### `aetius-16-136` — κονδίτου καθαρτικοῦ σκευασία ἐπὶ τῶν φλεγματικῶν, χρῶ δὲ τούτῳ ἐν χειμῶνι

**Citation:** Zervos 166.8 – 166.19

**Greek:**

> Μέλιτος ξστα ἤτοι ξέστ. α. οἴνου ξεε ἤτοι ξέστ. ε. πεπέρεως γράμματα μστ. στύρακος καλαμίτου γράμματα γ. τὸ πέπερι κόψας καὶ σήσας, τὸν δὲ στύρακα διαλύσας ἐν τρουλλίῳ μετ' ὀλίγου μέλιτος ἐπ' ἀνθράκων, εἶτα λειώσας αὐτὰ ἐν θυίᾳ μετὰ τοῦ πεπέρεως ἱκανῶς οἶνον ὀλίγον κατὰ βραχὺ ἐπιστάζων, ἐπίβαλλε τῷ μέλιτι, καὶ συλλεάνας ἐπίβαλλε τὸν οἶνον καὶ ἀναλάμβανε. Μεμνῆσθαι δὲ τούτου ἀεὶ χρή· ὅτι εἰ μὴ ἔστι καθαρὸν τὸ μέλι, οὐ καθίσταται καλῶς τὸ ἐξ αὐτοῦ σκευαζόμενον πρόπομα, ὅθεν χρὴ προεπαφρίζειν τὸ μὴ καθαρὸν μέλι· καθίσταται γὰρ εἰ ἐπαφρισθῇ, ἐν μιᾷ ἡμέρᾳ τὸ πρόπομα καὶ καθαρὸν γίνεται.

**Translation:**

> Honey, 1 xestes. Wine, 5 xestai. Pepper, 46 grammata. Reed-grade styrax, 3 grammata. Pound and sift the pepper; dissolve the styrax in a small pot (troullion) over coals with a little honey; then grind them together well in a mortar with the pepper, dripping in a little wine bit by bit; add to the honey, and once thoroughly ground together, pour in the wine and take up. One must always remember this: if the honey is not pure, the spiced drink (propoma) made from it will not settle properly. Therefore one must skim impure honey first, for once skimmed, the propoma will settle and become clear within one day.

**Ingredients:**

1. **μέλι** — 1 xestes
2. **οἶνος** — 5 xestes
3. **πέπερι** — 46 gramma
4. **στύραξ καλαμίτης** — 3 gramma

### `aetius-16-142` — θυμιάματος μοσχάτου σκευασία

**Citation:** Zervos 168.10 – 169.2

**Greek:**

> Ῥόδων χλωρῶν λιστ. ἤτοι λίτρ. στ. μέλιτος ἀττικοῦ διυλιςμένου διὰ ῥάκους ἀραιοῦ λιγ. γογ. ἤτοι λίτρ. γ καὶ οὐγ. γ. φύλλου γοστ ἤτοι οὐγ. στ. ἀμώμου γοδ ἤτοι οὐγ. δ. καρυοφύλλου γοβ ἤτοι οὐγ. β. ναρδοστάχυος γοδ ἤτοι οὐγ. δ. κόστου γοη ἤτοι οὐγ. η. ὀνύχων γοα, ἤτοι οὐγ. α. καρποβαλσάμου γοδ, ἤτοι οὐγ. δ. ἀσάρου γοβ, ἤτοι οὐγ. β. ἀλόης γοα, ἤτοι οὐγ. α. καλάμου ἰνδικοῦ γοστ, ἤτοι οὐγ. στ. κάρυα ἰνδικὰ γ. σανδαράχης γράμματα ιστ. ἄμβαρος γοα, ἤτοι οὐγ. α. στύρακος λιπαροῦ λιγ, ἤτοι λίτρ. γ. μαστίχης γοβ, ἤτοι οὐγ. β. κρόκου γοα. ἀντὶ δὲ τοῦ στύρακος, λαδάνου λιπαροῦ λίτρ. α. στακτῆς λευκῆς μυρεψικῆς λίτρ. α. τινὲς δὲ γοε ἤτοι οὐγ. ε. κρόκου γοα. μαστίχης γογ. μόσχου γράμματα δ. κόψας καὶ σήσας τὰ ξηρὰ, ὁλμοκοπήσας δὲ καὶ τὸν στύρακα μετὰ τοῦ λαδάνου καὶ τοῦ μέλιτος καὶ τῆς στακτῆς, ἐπίπασσε τὰ ξηρὰ καὶ ἑνώσας λύε ἐν τρουλλίῳ, εἶτα τῆκε τὸ ἄμβαρ καὶ ἐπιβαλὼν αὐτοῖς ἕνωσον. εἶτα λειώσας τὸν μόσχον ὕδατι θερμῷ, καὶ φυλάξας ἐξ αὐτοῦ τὸ ἀρκοῦν εἰς τὴν ἀνάπλασιν, μάλασσε τὸ θυμίαμα ἐν τῇ θυίᾳ καὶ ἀναλάμβανε ἀκριβῶς τὸν μόσχον, καὶ ἑνώσας ἀνάπλασσε τῷ φυλαχθέντι μόσχῳ.

**Translation:**

> Preparation of musk-incense. Fresh roses, 6 litrai. Attic honey strained through a loose cloth, 3 litrai and 3 uncia. Malabathron-leaf, 6 uncia. Amomum, 4 uncia. Clove, 2 uncia. Spikenard, 4 uncia. Costus, 8 uncia. Onycha, 1 uncia. Balsam-fruit, 4 uncia. Asaron, 2 uncia. Aloe, 1 uncia. Indian reed (sweet flag), 6 uncia. Indian nuts, 3. Sandarach, 16 grammata. Ambergris, 1 uncia. Fatty styrax, 3 litrai. Mastic, 2 uncia. Saffron, 1 uncia. In place of the styrax: fatty ladanum, 1 litra. White perfumer's stakte, 1 litra (some say 5 uncia). Saffron, 1 uncia. Mastic, 3 uncia. Musk, 4 grammata. Pound and sift the dry ingredients; crush the styrax in a mortar with the ladanum, the honey, and the stakte; sprinkle in the dry ingredients, mix together, and dissolve in a small pot. Then melt the ambergris, add to them, and unite. Then grind the musk with warm water, reserving from it q.s. (sufficient quantity) for the final shaping; knead the incense in the mortar and take up the musk carefully; mix together and shape using the reserved musk.

**Ingredients:**

1. **ῥόδα χλωρά** — 6 litra
2. **μέλι ἀττικόν** — 3 litra or 3 uncia
3. **φύλλον** — 6 uncia
4. **ἄμωμον** — 4 uncia
5. **καρυόφυλλον** — 2 uncia
6. **ναρδοστάχυς** — 4 uncia
7. **κόστος** — 8 uncia
8. **ὄνυξ** — 1 uncia
9. **καρποβάλσαμον** — 4 uncia
10. **ἄσαρον** — 2 uncia
11. **ἀλόη** — 1 uncia
12. **κάλαμος ἰνδικός** — 6 uncia
13. **κάρυα ἰνδικά** — 3 count
14. **σανδαράχη** — 16 gramma
15. **ἄμβαρ** — 1 uncia
16. **στύραξ λιπαρός** — 3 litra
17. **μαστίχη** — 2 uncia
18. **κρόκος** — 1 uncia
19. **λάδανον λιπαρόν** — 1 litra
20. **στακτὴ λευκὴ μυρεψική** — 1 litra or 5 uncia
21. **κρόκος** — 1 uncia
22. **μαστίχη** — 3 uncia
23. **μόσχος** — 4 gramma

### `aetius-16-143` — θυμιάματος τοῦ βασιλικοῦ σκευασία

**Citation:** Zervos 169.3 – 169.7

**Greek:**

> Στύρακος καλαμίτου λίτρ. α. ἀλόης γοστ. ἄμβαρος γοα. μόσχου γράμματα δ. τινὲς δὲ τοῦτο οὕτω σκευάζουσι· στύρακος καλαμίτου λίτρ. α. ἀλόης γοδ. ἄμβαρος γοα. μόσχου γράμματα δ. προστιθέασι δὲ καὶ χυλοῦ ῥόδων τὸ ἀρκοῦν.

**Translation:**

> Preparation of the royal incense. Reed-grade styrax, 1 litra. Aloe, 6 uncia. Ambergris, 1 uncia. Musk, 4 grammata. Some prepare it thus: reed-grade styrax, 1 litra. Aloe, 4 uncia. Ambergris, 1 uncia. Musk, 4 grammata. They also add rose-juice, q.s. (sufficient quantity).

**Ingredients:**

1. **στύραξ καλαμίτης** — 1 litra
2. **ἀλόη** — 6 uncia
3. **ἄμβαρος** — 1 uncia
4. **μόσχος** — 4 gramma
5. **στύραξ καλαμίτης** — 1 litra
6. **ἀλόη** — 4 uncia
7. **ἄμβαρος** — 1 uncia
8. **μόσχος** — 4 gramma
9. **χυλὸς ῥόδων** — q.s. (sufficient quantity)

### `aetius-16-144-1` — θυμιάματος μοσχάτου Θεοπέμπτου σκευασία

**Citation:** Zervos 169.8 – 169.11

**Greek:**

> Στύρακος λιπαροῦ γοι. καρυοφύλλου, κρόκου, ῥόδων ξηρῶν, φύλλου, μαστίχης, ἀνὰ γοα. μόσχου κεράτια δ. Ἐγὼ δὲ φησὶ, μόσχου γράμματα δ καὶ βαλσάμου τὸ ἱκανὸν ἐνέβαλλον.

**Translation:**

> Preparation of Theopemptus' musk-incense. Fatty styrax, 10 uncia. Clove, saffron, dry roses, malabathron-leaf, mastic — 1 uncia each. Musk, 4 ceration. But I, he says, put in musk 4 grammata, and as much balsam as suffices.

**Ingredients:**

1. **στύραξ λιπαρός** — 10 uncia
2. **καρυόφυλλον** — 1 uncia each
3. **κρόκος** — 1 uncia each
4. **ῥόδα ξηρά** — 1 uncia each
5. **φύλλον** — 1 uncia each
6. **μαστίχη** — 1 uncia each
7. **μόσχος** — 4 ceration
8. **μόσχος** — 4 gramma
9. **βάλσαμον** — q.s. (sufficient quantity)

### `aetius-16-144-2` — ἄλλου θυμιάματος μοσχάτου σκευασία

**Citation:** Zervos 169.12 – 169.16

**Greek:**

> Φύλλου, κόστου, βρύου ἤτοι ὕπνου, ῥόδων ξηρῶν, ναρδοστάχυος, ἀνὰ γοα. κρόκου, ὀνύχων, καρυοφύλλου, ἀμώμου, κασίας ἀνὰ γράμματα ιβ. καρποβαλσάμου, βδελλίου ἀνὰ ὁμοίως. στύρακος γράμματα κ. μόσχου γράμματα γ. ῥοδομέλιτος τὸ ἱκανόν.

**Translation:**

> Another preparation of musk-incense. Malabathron-leaf, costus, bryon (i.e. hypnon-moss), dry roses, spikenard — 1 uncia each. Saffron, onycha, clove, amomum, cassia — 12 grammata each. Balsam-fruit, bdellium — likewise. Styrax, 20 grammata. Musk, 3 grammata. Rose-honey, q.s. (sufficient quantity).

**Ingredients:**

1. **φύλλον** — 1 uncia
2. **κόστος** — 1 uncia
3. **βρύον** — 1 uncia
4. **ὕπνος** — 1 uncia
5. **ῥόδα ξηρά** — 1 uncia
6. **ναρδόσταχυς** — 1 uncia
7. **κρόκος** — 12 gramma
8. **ὄνυξ** — 12 gramma
9. **καρυόφυλλον** — 12 gramma
10. **ἄμωμον** — 12 gramma
11. **κασία** — 12 gramma
12. **καρποβάλσαμον** — 12 gramma
13. **βδέλλιον** — 12 gramma
14. **στύραξ** — 20 gramma
15. **μόσχος** — 3 gramma
16. **ῥοδομέλιτον** — q.s. (sufficient quantity)

### `aetius-16-145` — θυμιάματος καλοῦ ῥοδάτου σκευασία

**Citation:** Zervos 169.17 – 169.20

**Greek:**

> Φύλλου, ῥόδων ξηρῶν, κόστου, μαστίχης ἀνὰ γοβ. ναρδοστάχυος, ἀμώμου, ὀποβαλσάμου, ἀνὰ γοαζʹ. κρόκου. σμύρνης ἀνὰ γοα. στύρακος γοι. οἴνου εὐώδους παλαιοῦ καὶ μέλιτος τὸ ἀρκοῦν.

**Translation:**

> Preparation of good rose-incense. Malabathron-leaf, dry roses, costus, mastic — 2 uncia each. Spikenard, amomum, balsam-juice — 1½ uncia each. Saffron, myrrh — 1 uncia each. Styrax, 10 uncia. Old fragrant wine and honey, q.s. (sufficient quantity) of each.

**Ingredients:**

1. **φύλλον** — 2 uncia
2. **ῥόδα ξηρά** — 2 uncia
3. **κόστος** — 2 uncia
4. **μαστίχη** — 2 uncia
5. **ναρδοστάχυς** — 1.5 uncia
6. **ἄμωμον** — 1.5 uncia
7. **ὀποβάλσαμον** — 1.5 uncia
8. **κρόκος** — 1 uncia
9. **σμύρνα** — 1 uncia
10. **στύραξ** — 10 uncia
11. **οἶνος εὐώδης παλαιός** — q.s. (sufficient quantity)
12. **μέλι** — q.s. (sufficient quantity)

### `aetius-16-146-1` — μοσχάτου ἐν τῇ ἐκκλησίᾳ καπνιζομένου σκευασία

**Citation:** Zervos 169.21 – 170.7

**Greek:**

> Κόστου λίτρ. δ ἤτοι δ. καὶ ἡμίσ. καρυοφύλλων λίτρ. θ. φύλλων λίτ. α καὶ ἡμίσ. ναρδοστάχυος τὸ αὐτό. κασάμου γοιδ ἤτοι οὐγ. ιδ. στύρακος χυματίου λίτρ. στ. ἄσπρου λιτρ. γ. κρόκου τριχίνου γοι. ἄμβαρος γοβ. μόσχου γοβ.

**Translation:**

> Preparation of musk-incense burned in church. Costus, 4½ litrai. Cloves, 9 litrai. Malabathron-leaves, 1½ litrai. Spikenard, the same. Casamum, 14 uncia. Liquid styrax, 6 litrai. White styrax, 3 litrai. Trichinos-grade saffron, 10 uncia. Ambergris, 2 uncia. Musk, 2 uncia.

**Ingredients:**

1. **κόστος** — 4 litra or 4.5 litra
2. **καρυόφυλλον** — 9 litra
3. **φύλλον** — 1.5 litra
4. **ναρδόσταχυς** — same as preceding
5. **κάσαμον** — 14 uncia or 14 uncia
6. **στύραξ χυμάτιος** — 6 litra _(uncertain)_
7. **ἄσπρον** — 400 litra _(uncertain)_
8. **κρόκος τριχῖνος** — 10 uncia
9. **ἄμβαρος** — 2 uncia
10. **μόσχος** — 2 uncia

### `aetius-16-146-1-2` — μοσχάτου ἐν τῇ ἐκκλησίᾳ καπνιζομένου σκευασία

**Citation:** Zervos 169.21 – 170.7

**Greek:**

> ὁ ἄρχων δὲ τῆς Ἀνατολῆς σκευάζει οὕτως. κόστου γογ. ναρδοστάχυος γοα. φύλλων τὸ αὐτό. καρυοφύλλων γογζʹ. ἤτοι οὐγ. γ καὶ ἡμίσ. κασάμου γοζʹ. ἤτοι οὐγ. ἡμίσ. ἄσπρου γοβ. στύρακος γοβ. χυματίου πρωτείου γοε. κρόκου τριχίνου γράμματα β. μόσχου, ἄμβαρος ἀνὰ γράμματα β.

**Translation:**

> The Archon of the East prepares it thus: costus, 3 uncia. Spikenard, 1 uncia. Malabathron-leaves, the same. Cloves, 3½ uncia. Casamum, ½ uncia. White styrax, 2 uncia. Liquid first-quality styrax, 5 uncia. Trichinos-grade saffron, 2 grammata. Musk and ambergris, 2 grammata each.

**Ingredients:**

1. **κόστος** — 3 uncia
2. **ναρδόσταχυς** — 1 uncia
3. **φύλλον** — same as preceding
4. **καρυόφυλλον** — 3.5 uncia or 3.5 uncia
5. **κάσαμον** — uncia or 0.5 uncia
6. **ἄσπρον** — 2 uncia _(uncertain)_
7. **στύραξ** — 2 uncia
8. **χυμάτιον πρωτεῖον** — 5 uncia _(uncertain)_
9. **κρόκος τριχῖνος** — 2 gramma
10. **μόσχος** — 2 gramma each
11. **ἄμβαρος** — 2 gramma each

### `aetius-16-147` — θυμιάματος μυρεψικοῦ καλοῦ σκευασία

**Citation:** Zervos 170.15 – 170.20

**Greek:**

> Κόστου λιαζʹ. κασάμου λια. ξυλοκαρυοφύλλων, σκύλματος φύλλων, ναρδοστάχυος ἀνὰ γοστ. φλοιοῦ ἀσπαλάθου, ῥόδων ξηρῶν ἀνὰ γογ. μαστίχης χίας, βδελλίου ἀνὰ γοβ. λαδάνου λιγ. μελαίνης στακτῆς λιστ. κρόκου γράμματα στ. Ἐγὼ δὲ φησὶν, ἀντὶ τῆς μελαίνης στακτῆς ἔβαλλον τῆς λευκῆς λιβ. καὶ στύρακος λιδ.

**Translation:**

> Preparation of good perfumer's incense. Costus, 1½ litrai. Casamum, 1 litra. Xylocaryophylla (clove-wood), shaved malabathron-leaves, spikenard — 6 uncia each. Aspalathos-bark, dry roses — 3 uncia each. Chian mastic, bdellium — 2 uncia each. Ladanum, 3 litrai. Black stakte, 6 litrai. Saffron, 6 grammata. But I, he says, instead of the black stakte put in 12 litrai of the white, and 14 litrai of styrax.

**Ingredients:**

1. **κόστος** — 1.5 litra
2. **κάσαμον** — 1 litra
3. **ξυλοκαρυόφυλλον** — 6 uncia
4. **φύλλα σκύλματος** — 6 uncia
5. **ναρδόσταχυς** — 6 uncia
6. **φλοιὸς ἀσπαλάθου** — 3 uncia
7. **ξηρὰ ῥόδα** — 3 uncia
8. **μαστίχη χία** — 2 uncia
9. **βδέλλιον** — 2 uncia
10. **λάδανον** — 3 litra
11. **μελαίνη στακτή** — 6 litra
12. **κρόκος** — 6 gramma
13. **λευκὴ στακτή** — 2 litra _(uncertain)_
14. **στύραξ** — 4 litra

### `aetius-16-148` — θυμιάματος ἐράνου σκευασία

**Citation:** Zervos 171.1 – 171.4

**Greek:**

> Κόστου γοιθ. καρυοφύλλων γοδ. λαδάνου λια. ναρδοστάχυος, φύλλων ἀνὰ γοστ. στύρακος λιγ. ἄσπρου γοιστ. κρόκου γράμματα στ. μόσχου γοη. μέλιτος γοε.

**Translation:**

> Preparation of contributors' incense (eranou). Costus, 19 uncia. Cloves, 4 uncia. Ladanum, 1 litra. Spikenard, malabathron-leaves — 6 uncia each. White styrax, 16 uncia (with an unresolved abbreviation `λιγ.` standing between styrax and ἄσπρου in the manuscript). Saffron, 6 grammata. Musk, 8 uncia. Honey, 5 uncia.

**Ingredients:**

1. **κόστος** — 19 uncia
2. **καρυόφυλλον** — 4 uncia
3. **λάδανον** — 1 litra
4. **ναρδόσταχυς** — 6 uncia each
5. **φύλλον** — 6 uncia each
6. **στύραξ ἄσπρος** — 16 uncia _(uncertain)_
7. **κρόκος** — 6 gramma
8. **μόσχος** — 8 uncia
9. **μέλι** — 5 uncia

### `aetius-16-149` — θυμίαμα τῆς κυρίας Ῥωμύλου

**Citation:** Zervos 171.5 – 171.8

**Greek:**

> Στύρακος καλαμίτου λιβ. κόστου, στακτῆς λευκῆς, ἀνὰ γοστ. καρυοφύλλων, τάρου ἀνὰ γοβ. ναρδοστάχυος γοβζʹ. κρόκου γοδ. ἄμβαρος δραχ. δ. ἀλούα γοα. μόσχου γράμματα δ. ἢ ὅσον βούλει.

**Translation:**

> Incense of Lady Rōmylē. Reed-grade styrax, 2 litrai. Costus, white stakte — 6 uncia each. Cloves, taron — 2 uncia each. Spikenard, 2½ uncia. Saffron, 4 uncia. Ambergris, 4 drachmai. Aloe, 1 uncia. Musk, 4 grammata — or as much as you wish.

**Ingredients:**

1. **στύραξ καλαμίτης** — 2 litra
2. **κόστος** — 6 uncia
3. **στακτή λευκή** — 6 uncia
4. **καρυόφυλλον** — 2 uncia
5. **τάρον** — 2 uncia _(uncertain)_
6. **ναρδόσταχυς** — 2.5 uncia
7. **κρόκος** — 4 uncia
8. **ἄμβαρος** — 4 drachme
9. **ἀλούα** — 1 uncia
10. **μόσχος** — 4 gramma

### `aetius-16-150` — θυμίαμα ῥοδάτον τοῦ ἐμβολάρχου

**Citation:** Zervos 171.9 – 171.15

**Greek:**

> Κασίας, σμύρνης, βδελλίου, ἀρναβῶ, καλάμου ἰνδικοῦ, σαρούα, καρποβαλσάμου, λαδάνου λιπαροῦ, ὕπνου, φύλλων, ἀνὰ γογ. καρυοφύλλων, ὀνύχων μεγάλων, μαστίχης, ἀνὰ γοδ. κρόκου γοβ. ναρδοστάχυος, ὀποβαλσάμου, ἀνὰ γοστ. ῥόδων ξηρῶν, στύρακος, ἀνὰ λια. ῥόδων χλωρῶν λιβ. οἴνου παλαιοῦ εὐώδους καὶ μέλιτος ἀττικοῦ τὸ ἀρκοῦν.

**Translation:**

> Rose-incense of the embolarch (market-overseer). Cassia, myrrh, bdellium, arnabo, Indian reed (sweet flag), saroua, balsam-fruit, fatty ladanum, hypnon-moss, malabathron-leaves — 3 uncia each. Cloves, large onycha, mastic — 4 uncia each. Saffron, 2 uncia. Spikenard, balsam-juice — 6 uncia each. Dry roses, styrax — 1 litra each. Fresh roses, 2 litrai. Old fragrant wine and Attic honey, q.s. (sufficient quantity) of each.

**Ingredients:**

1. **κασία** — 3 uncia
2. **σμύρνα** — 3 uncia
3. **βδέλλιον** — 3 uncia
4. **ἀρναβώ** — 3 uncia
5. **κάλαμος ἰνδικός** — 3 uncia
6. **σαρούα** — 3 uncia
7. **καρποβάλσαμον** — 3 uncia
8. **λάδανον λιπαρόν** — 3 uncia
9. **ὕπνος** — 3 uncia
10. **φύλλον** — 3 uncia
11. **καρυόφυλλον** — 4 uncia
12. **ὄνυξ μέγας** — 4 uncia
13. **μαστίχη** — 4 uncia
14. **κρόκος** — 2 uncia
15. **ναρδόσταχυς** — 6 uncia
16. **ὀποβάλσαμον** — 6 uncia
17. **ῥόδον ξηρόν** — 1 litra
18. **στύραξ** — 1 litra
19. **ῥόδον χλωρόν** — 2 litra
20. **οἶνος παλαιὸς εὐώδης** — q.s. (sufficient quantity)
21. **μέλι ἀττικόν** — q.s. (sufficient quantity)

### `aetius-16-151` — θυμίαμα ῥοδάτον ἐπισκόπου Παμφύλου

**Citation:** Zervos 171.16 – 171.23

**Greek:**

> Φύλλου, καρυοφύλλου, ὕπνου, λαδάνου λιπαροῦ ἀνὰ γοβζʹ. καλάμου ἰνδικοῦ, ναρδοστάχυος, ὀνύχων μεγάλων, βδελλίου, καρποβαλσάμου, κρόκου, κασίας, ἀνὰ γογ. ἀμώμου, μαστίχης ἀνὰ γοε. κόστου γοαζʹ. ἀρναβῶ τὸ αὐτό. σαρούα γοα. ὀποβαλσάμου γογ. στύρακος λιπαροῦ λιγ. ῥόδων νεαρῶν ἐξωνυχισμένων λιστ. οἰνομέλιτος τὸ ἀρκοῦν. ἔστω δὲ τὸ μέλι πρωτεῖον, καὶ ὁ οἶνος παλαιὸς καὶ εὐώδης.

**Translation:**

> Rose-incense of Bishop Pamphylos. Malabathron-leaf, clove, hypnon-moss, fatty ladanum — 2½ uncia each. Indian reed (sweet flag), spikenard, large onycha, bdellium, balsam-fruit, saffron, cassia — 3 uncia each. Amomum, mastic — 5 uncia each. Costus, 1½ uncia. Arnabo, the same. Saroua, 1 uncia. Balsam-juice, 3 uncia. Fatty styrax, 3 litrai. Fresh roses, picked clean of their nails (sepals), 6 litrai. Mead (oinomeli), q.s. (sufficient quantity). Let the honey be first-quality, and the wine old and fragrant.

**Ingredients:**

1. **φύλλον** — 2.5 uncia
2. **καρυόφυλλον** — 2.5 uncia
3. **ὕπνος** — 2.5 uncia
4. **λάδανον λιπαρόν** — 2.5 uncia
5. **κάλαμος ἰνδικός** — 3 uncia
6. **ναρδόσταχυς** — 3 uncia
7. **ὄνυξ μέγας** — 3 uncia
8. **βδέλλιον** — 3 uncia
9. **καρποβάλσαμον** — 3 uncia
10. **κρόκος** — 3 uncia
11. **κασία** — 3 uncia
12. **ἄμωμον** — 5 uncia
13. **μαστίχη** — 5 uncia
14. **κόστος** — 1.5 uncia
15. **ἀρναβώ** — same as preceding _(uncertain)_
16. **σαρούα** — 1 uncia _(uncertain)_
17. **ὀποβάλσαμον** — 3 uncia
18. **στύραξ λιπαρός** — 3 litra
19. **ῥόδα νεαρά** — 6 litra
20. **μέλι** — (no amount specified)
21. **οἶνος** — (no amount specified)

## Appendix: Styrax-variant index

| Recipe | Styrax form(s) called for |
| --- | --- |
| `aetius-1-123` | στύραξ λιπαρός |
| `aetius-1-131` | στύραξ |
| `aetius-1-131-5` | στύραξ καλαμίτης |
| `aetius-1-132` | στύραξ λιπαρός, στύραξ |
| `aetius-1-132-2` | στύραξ λιπαρός |
| `aetius-1-133` | στύραξ πρωτεῖος |
| `aetius-1-135` | στύραξ πρωτεῖος |
| `aetius-16-126-1` | στύραξ |
| `aetius-16-126-2` | στύραξ |
| `aetius-16-126-3` | στύραξ |
| `aetius-16-127-1` | στύραξ |
| `aetius-16-127-2` | στύραξ |
| `aetius-16-128` | στύραξ |
| `aetius-16-129` | στύραξ λιπαρός |
| `aetius-16-130-1` | στύραξ λιπαρός |
| `aetius-16-131-1` | στύραξ |
| `aetius-16-131-2` | στύραξ λιπαρός |
| `aetius-16-133-2` | στύραξ |
| `aetius-16-136` | στύραξ καλαμίτης |
| `aetius-16-142` | στύραξ λιπαρός |
| `aetius-16-143` | στύραξ καλαμίτης |
| `aetius-16-144-1` | στύραξ λιπαρός |
| `aetius-16-144-2` | στύραξ |
| `aetius-16-145` | στύραξ |
| `aetius-16-146-1` | στύραξ χυμάτιος |
| `aetius-16-146-1-2` | στύραξ |
| `aetius-16-147` | στύραξ |
| `aetius-16-148` | στύραξ ἄσπρος |
| `aetius-16-149` | στύραξ καλαμίτης |
| `aetius-16-150` | στύραξ |
| `aetius-16-151` | στύραξ λιπαρός |
