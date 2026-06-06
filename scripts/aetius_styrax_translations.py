"""Literal English translations of the 30 Aetius styrax recipes.

Hand-written, applying the glossary in docs/aetius-styrax-recipes.md consistently.
Keyed by recipe_id; each value is a single string, may contain markdown line breaks.

Plural conventions used here: **uncia** stays singular for any count (matches the
data column); **litra → litrai**, **xestes → xestai**, **drachme → drachmai**,
**gramma → grammata** (Greek transliteration plurals).
"""

TRANSLATIONS: dict[str, str] = {
    "aetius-1-123": (
        "Styrax-oil is prepared thus: of finest sweet olive oil, 1 xestes; "
        "of fatty styrax, 2 uncia. Boiled together in a double-vessel (bain-marie), "
        "the virtue of the styrax is deposited into the oil. It is a little warmer than "
        "dill-oil, but exceedingly emollient, and on this account it nobly softens "
        "hardened parts of the body."
    ),
    "aetius-1-131": (
        "Preparation of Cyzicene nard-oil. I prepared this many times in Alexandria "
        "and it is very good. Unripe-olive oil, 12 Italian xestai; aspalathos, cyperus, "
        "Illyrian iris, cardamom-seed, long aristolochia, xylocassia, 12 uncia each; "
        "elenium, balsam-wood, schoenus-flower, cassia, costus, 6 uncia each; amomum, "
        "malabathron-leaf, spikenard, arnabo, styrax, balsam-fruit, 3 uncia each; "
        "balsam-juice, 3 uncia; savin, 1 uncia. It is prepared thus: strip the bark "
        "from the aspalathos, cyperus, elenium, balsam-wood, iris, and aristolochia, "
        "pound them coarsely, and soak them in hot water for 3 days; then pour in the "
        "oil and boil, stirring continuously and adding water little by little as the "
        "first lot is consumed; then, having boiled for 3 hours or more, cover the pot "
        "and leave it overnight. On the next day, lift out what has already been boiled, "
        "separate the water from the oil, then add fresh water and a little wine and "
        "boil. When it comes to a boil, add first the cardamom, then the schoenus and "
        "xylocassia (pounded), and boil for 2 hours; again leave overnight. On the third "
        "day, lift out likewise, add clean water, and boil; when it comes to a boil, "
        "sprinkle in, ground fine, in portions, the cassia, costus, and the rest — each "
        "pounded separately. Toward the very end, add the spikenard, malabathron-leaf, "
        "and the styrax broken up into fine pieces; and as soon as it melts, take the "
        "pot at once from the fire and add the balsam-juice. Stir well, stopper it, "
        "cover it thoroughly, and leave for 2 days; then take it up into a mussel-shell "
        "jar (myakion). A second batch is prepared thus: to what remains from the third "
        "boiling add 6 xestai of oil, bring it to a boil, and boil for 2 hours; then "
        "sprinkle in finest-ground cassia 2 uncia, Celtic nard 2 uncia, savin 4 drachmai, "
        "styrax 1 uncia, balsam-juice 2 uncia. Nard-oil is of warming, toning, and "
        "soothing virtue, and so most fit for a chilled and weakened stomach, and for "
        "the belly and liver afflicted with the same. It is also injected into chilled "
        "intestines, and used by women in the womb as a thoroughly approved remedy."
    ),
    "aetius-1-131-5": (
        "Preparation of nard-oil by John the perfumer. Olive oil, 6 xestai; aspalathos, "
        "4 litrai; balsam-wood, 2 litrai; costus, 3 uncia; xylocassia, 4 uncia; "
        "balsam-fruit, 6 uncia; amomum, 3 uncia; reed-grade styrax, 2 uncia; "
        "balsam-juice, 2 uncia."
    ),
    "aetius-1-132": (
        "Preparation of salka-oil. I prepared this in Alexandria and it is the very "
        "finest. Aspalathos 6 uncia, balsam-wood 9 uncia, cyperus 4 uncia, elenium "
        "6 uncia, iris 6 uncia, calamus 18 grammata, schoenus-flower 2½ uncia, fatty "
        "styrax 2 uncia, Indian nuts 2, malabathron-leaf 18 grammata, spikenard 1 uncia, "
        "clove 1½ uncia, arnabo 1½ uncia, amomum 3 uncia, cassia 2 uncia, costus 1 uncia, "
        "myrrh 1 uncia, hypnon-moss 3 uncia, xylocassia 3 uncia, olive oil 15 xestai. It "
        "is boiled in the manner described above for nard-oil: at the first boiling, "
        "balsam-wood, iris, cyperus, elenium, and xylocassia are thrown in — peeled, "
        "coarsely pounded, and pre-soaked in water for 2 or 3 days; at the second "
        "boiling, calamus, schoenus, and hypnon-moss (pre-moistened in old fragrant "
        "wine) are added; at the third, the rest. A second batch is likewise made: to "
        "what remains from the third boiling add 6 xestai of oil and boil until reduced; "
        "then add good white stakte 3 uncia, seiroma — that is, the watery fraction of "
        "balsam-juice — 6 uncia, mastic 6 uncia, reed-grade styrax 1 uncia. Women use "
        "salka-oil for anointing the head. The preparation described above is "
        "exceedingly fine."
    ),
    "aetius-1-132-2": (
        "Preparation of salka-oil by John the perfumer. Costus 12 uncia, malabathron-leaf "
        "4 uncia, cassia 6 uncia, myrrh 6 uncia, xylocaryophyllon (clove-wood) 6 uncia, "
        "balsam-fruit 6 uncia, spikenard 4 uncia, calamus 1 uncia, iris 12 uncia, fatty "
        "styrax 9 uncia, saffron 4 drachmai, olive oil 5½ xestai."
    ),
    "aetius-1-133": (
        "Preparation of malabathron-leaf oil — also called malabathrinon — the finest. "
        "Aspalathos 1½ litrai, balsam-wood 2 litrai, cyperus 1½ litrai, elenium 1½ litrai, "
        "malabathron-leaf 4 uncia, amomum 6 uncia, xylocassia 4 uncia, myrrh 3 uncia, "
        "costus 9 uncia, first-quality styrax 1 litra, casamum (that is, balsam-fruit) "
        "6 uncia, calamus 1½ litrai, spikenard 2 uncia, clove 4 uncia, seiroma — i.e. "
        "the watery residue — 6 uncia, balsam-juice 6 uncia, arnabo 6 uncia, cardamom "
        "6 uncia, iris 1 litra, olive oil 20 (unit unresolved), fragrant wine q.s. "
        "(sufficient quantity). Boil as you would the nard-oil."
    ),
    "aetius-1-135": (
        "Smoked oil. The so-called smoked oil is prepared thus: large aromatic onycha, "
        "5 uncia; male frankincense and first-quality styrax, 5 uncia; clean bdellium, "
        "5 uncia; costus, 5 uncia; good sweet olive oil, 5 xestai; hypnon-moss q.s. "
        "(sufficient quantity). Divide the costus into coarse pieces, and likewise the "
        "styrax and the bdellium; mix them together and put them into a new earthenware "
        "pot (xestion) without a handle. Then partially cover the mouth with hypnon-moss, "
        "and around the moss pack small twigs of aspalathos or some other fragrant wood, "
        "so that what is inside the pot may not fall out. Then take another handle-less "
        "earthenware vessel, long-necked, with a mouth fitting that of the pot containing "
        "the above ingredients, pour into it 5 xestai of sweet olive oil, dig a hole in "
        "the ground, and sink the oil-vessel up to its neck so that it does not heat "
        "through. Then take the pot, invert it head-downwards over the mouth of the "
        "oil-vessel, joining the two mouths together; and smear the outside of the pot "
        "all around with clay, sealing the joined mouths of both vessels, and leave it "
        "to dry. The next day, heap many coals on top of and around the pot so that it "
        "is covered on every side; kindle a fire and fan it. Once the fire has caught, "
        "let it die down, so that, as the ingredients are slowly heated, smoke passes "
        "through the pot's mouth and smokes the oil beneath them — and for this reason "
        "it is called smoked oil. Then the next day open it, take out the oil, store it "
        "in a glass vessel, and use it. Women use it when their menstrual periods are "
        "suppressed, anointing the lower belly and loins with it. It is also fitting "
        "for those not being properly cleansed in childbirth, applied likewise. It is "
        "also useful for those with a chilled chest, and beneficial against tenesmus, "
        "applied warm, taken up in a fold of wool and placed on the belly and loins."
    ),
    "aetius-16-126-1": (
        "Arnabo, amomum, spikenard — 3 uncia each. Malabathron-leaf and styrax — "
        "likewise. Saffron, cloves — 1½ uncia each. Balsam-juice — 6 uncia. Fresh "
        "roses — 26 uncia."
    ),
    "aetius-16-126-2": (
        "Cassia-leaves, saffron, styrax, arnabo, amomum, spikenard — 1½ uncia each. "
        "Cloves, 4 drachmai. Musk, 3 grammata. Balsam-juice, 1 uncia. Indian oil (or "
        "another), 3 uncia. Dry roses, 2 uncia; or fresh roses, 4 uncia."
    ),
    "aetius-16-126-3": (
        "Massouaphion, cloves, costus — 2 uncia each. Malabathron-leaves, spikenard, "
        "rose-juice — 12 grammata each. Amomum, styrax — 1 uncia each. Gum, 2 uncia. "
        "Pound and sift the dry ingredients and soak the gum; then crush the styrax in "
        "a mortar and blend it well with the dry ingredients; add the gum and form into "
        "round troches the size of a soaked chickpea. Pierce them with a needle, thread "
        "them on a strong cord, dry them, and give them to be worn around the neck."
    ),
    "aetius-16-127-1": (
        "Dry roses, 1 litra. Costus, malabathron-leaf, cloves, hypnon-moss, aromatic "
        "calamus, onycha, styrax — 2 uncia each."
    ),
    "aetius-16-127-2": (
        "Malabathron-leaves, dry roses, amomum, costus, cloves, spikenard, arnabo-juice, "
        "saffron — 1 uncia each. Hypnon-moss, styrax, balsam-juice — 4 drachmai each."
    ),
    "aetius-16-128": (
        "Samian earth, 1 litra. Styrax, malabathron-leaf, balsam-juice — 2 uncia each. "
        "Grind the styrax with the balsam-juice; pound and sift the malabathron-leaf; "
        "then blend everything well together in the mortar, mix in q.s. (sufficient "
        "quantity) of rose-juice, and use."
    ),
    "aetius-16-129": (
        "Malabathron-leaf, spikenard-juice, mastic, clove — 1 uncia and 12 grammata each. "
        "Fatty styrax, balsam-juice — 2 uncia each. Saffron, 6 grammata. Musk, 1 gramma. "
        "First-quality salka-oil, 4 uncia."
    ),
    "aetius-16-130-1": (
        "Unripe-olive oil, 20 xestai. Illyrian iris, 1 litra. Amomum, 6 uncia. "
        "Aspalathos and hypnon-moss — 1 litra each. *Second boiling.* Calamus alos, "
        "2 litrai. Cloves, malabathron-leaf, balsam-fruit — 1 litra each. Xylocassia, "
        "5 uncia. *Third boiling.* Cassia, 4 uncia. Costus, fatty styrax, saffron — "
        "1 uncia each. Myrrh, arnabo — 3 uncia each. Spikenard, 4 uncia. Boil with "
        "water. The manner of the preparation is given in Book 1, in the section on "
        "the compounding of oils, where you also have written another excellent recipe "
        "for salka-oil and for the preparation of nard-oil."
    ),
    "aetius-16-131-1": (
        "Balsam-juice, 1 litra. Styrax, amomum — 3 uncia each. Cassia, 4 uncia. Lilies, "
        "20 in number. Grind all together and use. If it should be too thick, thin it "
        "with salka-oil."
    ),
    "aetius-16-131-2": (
        "Wax, 1 litra. Cyzicene nard-oil, 3 litrai. Bruttian pitch, 5 uncia. Ladanum, "
        "1 uncia. Fatty styrax, 3 uncia. Costus, cassia — 2 uncia each. Cardamom, "
        "malabathron-leaf — 1 uncia each. Spikenard, 1 uncia (the seventh — i.e. half). "
        "Saffron, Aminaean wine — 1 uncia each. Balsam-juice, 3 uncia."
    ),
    "aetius-16-133-2": (
        "Costus, 2 uncia. Cassia, balsam-fruit, massouaphion, myrrh — 1 uncia each. "
        "Amomum, 5 uncia. Spikenard, styrax — 4 uncia each. Clove, 1½ uncia. "
        "Balsam-juice, 6 uncia. Lilies, 40 in number. Fragrant "
        "astringent wine, 12 xestai. Cappadocian salt, 2 uncia. Strip the petals from "
        "the lilies, wipe clean every saffron-colored part within them, and let them "
        "wither in the shade on a clean linen cloth for a day and a night. Then pound "
        "and sift the dry ingredients; grind the myrrh in a mortar with wine; then add "
        "all the dry ingredients and dissolve them in the wine. Break the styrax into "
        "the finest pieces with the fingers and add to them; mix together, then pour "
        "in the balsam-juice. When all is well united, throw the lily-petals into the "
        "mortar, knead with the hands, take up the ground mixture with the petals, put "
        "it in a jar (bikion) and shake. Likewise pour in the wine into the same jar "
        "and shake after. Then stopper the jar with bryon-moss or hypnon-moss, bind it "
        "up, seal it firmly, set it in the sun for 40 days, and use."
    ),
    "aetius-16-136": (
        "Honey, 1 xestes. Wine, 5 xestai. Pepper, 46 grammata. Reed-grade styrax, "
        "3 grammata. Pound and sift the pepper; dissolve the styrax in a small pot "
        "(troullion) over coals with a little honey; then grind them together well in "
        "a mortar with the pepper, dripping in a little wine bit by bit; add to the "
        "honey, and once thoroughly ground together, pour in the wine and take up. One "
        "must always remember this: if the honey is not pure, the spiced drink (propoma) "
        "made from it will not settle properly. Therefore one must skim impure honey "
        "first, for once skimmed, the propoma will settle and become clear within one day."
    ),
    "aetius-16-142": (
        "Preparation of musk-incense. Fresh roses, 6 litrai. Attic honey strained "
        "through a loose cloth, 3 litrai and 3 uncia. Malabathron-leaf, 6 uncia. "
        "Amomum, 4 uncia. Clove, 2 uncia. Spikenard, 4 uncia. Costus, 8 uncia. Onycha, "
        "1 uncia. Balsam-fruit, 4 uncia. Asaron, 2 uncia. Aloe, 1 uncia. Indian reed "
        "(sweet flag), 6 uncia. Indian nuts, 3. Sandarach, 16 grammata. Ambergris, "
        "1 uncia. Fatty styrax, 3 litrai. Mastic, 2 uncia. Saffron, 1 uncia. In place "
        "of the styrax: fatty ladanum, 1 litra. White perfumer's stakte, 1 litra (some "
        "say 5 uncia). Saffron, 1 uncia. Mastic, 3 uncia. Musk, 4 grammata. Pound and "
        "sift the dry ingredients; crush the styrax in a mortar with the ladanum, the "
        "honey, and the stakte; sprinkle in the dry ingredients, mix together, and "
        "dissolve in a small pot. Then melt the ambergris, add to them, and unite. "
        "Then grind the musk with warm water, reserving from it q.s. (sufficient "
        "quantity) for the final shaping; knead the incense in the mortar and take up "
        "the musk carefully; mix together and shape using the reserved musk."
    ),
    "aetius-16-143": (
        "Preparation of the royal incense. Reed-grade styrax, 1 litra. Aloe, 6 uncia. "
        "Ambergris, 1 uncia. Musk, 4 grammata. Some prepare it thus: reed-grade styrax, "
        "1 litra. Aloe, 4 uncia. Ambergris, 1 uncia. Musk, 4 grammata. They also add "
        "rose-juice, q.s. (sufficient quantity)."
    ),
    "aetius-16-144-1": (
        "Preparation of Theopemptus' musk-incense. Fatty styrax, 10 uncia. Clove, "
        "saffron, dry roses, malabathron-leaf, mastic — 1 uncia each. Musk, 4 ceration. "
        "But I, he says, put in musk 4 grammata, and as much balsam as suffices."
    ),
    "aetius-16-144-2": (
        "Another preparation of musk-incense. Malabathron-leaf, costus, bryon (i.e. "
        "hypnon-moss), dry roses, spikenard — 1 uncia each. Saffron, onycha, clove, "
        "amomum, cassia — 12 grammata each. Balsam-fruit, bdellium — likewise. Styrax, "
        "20 grammata. Musk, 3 grammata. Rose-honey, q.s. (sufficient quantity)."
    ),
    "aetius-16-145": (
        "Preparation of good rose-incense. Malabathron-leaf, dry roses, costus, mastic — "
        "2 uncia each. Spikenard, amomum, balsam-juice — 1½ uncia each. Saffron, "
        "myrrh — 1 uncia each. Styrax, 10 uncia. Old "
        "fragrant wine and honey, q.s. (sufficient quantity) of each."
    ),
    "aetius-16-146-1": (
        "Preparation of musk-incense burned in church. Costus, 4½ litrai. Cloves, "
        "9 litrai. Malabathron-leaves, 1½ litrai. Spikenard, the same. Casamum, "
        "14 uncia. Liquid styrax, 6 litrai. White styrax, 3 litrai. Trichinos-grade "
        "saffron, 10 uncia. Ambergris, 2 uncia. Musk, 2 uncia."
    ),
    "aetius-16-146-1-2": (
        "The Archon of the East prepares it thus: costus, 3 uncia. Spikenard, 1 uncia. "
        "Malabathron-leaves, the same. Cloves, 3½ uncia. Casamum, ½ uncia. White "
        "styrax, 2 uncia. Liquid first-quality styrax, 5 uncia. Trichinos-grade "
        "saffron, 2 grammata. Musk and ambergris, 2 grammata each."
    ),
    "aetius-16-147": (
        "Preparation of good perfumer's incense. Costus, 1½ litrai. Casamum, 1 litra. "
        "Xylocaryophylla (clove-wood), shaved malabathron-leaves, spikenard — 6 uncia "
        "each. Aspalathos-bark, dry roses — 3 uncia each. Chian mastic, bdellium — "
        "2 uncia each. Ladanum, 3 litrai. Black stakte, 6 litrai. Saffron, 6 grammata. "
        "But I, he says, instead of the black stakte put in 12 litrai of the white, "
        "and 14 litrai of styrax."
    ),
    "aetius-16-148": (
        "Preparation of contributors' incense (eranou). Costus, 19 uncia. Cloves, "
        "4 uncia. Ladanum, 1 litra. Spikenard, malabathron-leaves — 6 uncia each. "
        "White styrax, 16 uncia (with an unresolved abbreviation `λιγ.` standing "
        "between styrax and ἄσπρου in the manuscript). Saffron, 6 grammata. Musk, "
        "8 uncia. Honey, 5 uncia."
    ),
    "aetius-16-149": (
        "Incense of Lady Rōmylē. Reed-grade styrax, 2 litrai. Costus, white stakte — "
        "6 uncia each. Cloves, taron — 2 uncia each. Spikenard, 2½ uncia. Saffron, "
        "4 uncia. Ambergris, 4 drachmai. Aloe, 1 uncia. Musk, 4 grammata — or as much "
        "as you wish."
    ),
    "aetius-16-150": (
        "Rose-incense of the embolarch (market-overseer). Cassia, myrrh, bdellium, "
        "arnabo, Indian reed (sweet flag), saroua, balsam-fruit, fatty ladanum, "
        "hypnon-moss, malabathron-leaves — 3 uncia each. Cloves, large onycha, mastic — "
        "4 uncia each. Saffron, 2 uncia. Spikenard, balsam-juice — 6 uncia each. Dry "
        "roses, styrax — 1 litra each. Fresh roses, 2 litrai. Old fragrant wine and "
        "Attic honey, q.s. (sufficient quantity) of each."
    ),
    "aetius-16-151": (
        "Rose-incense of Bishop Pamphylos. Malabathron-leaf, clove, hypnon-moss, fatty "
        "ladanum — 2½ uncia each. Indian reed (sweet flag), spikenard, large onycha, "
        "bdellium, balsam-fruit, saffron, cassia — 3 uncia each. Amomum, mastic — "
        "5 uncia each. Costus, 1½ uncia. Arnabo, the same. Saroua, 1 uncia. "
        "Balsam-juice, 3 uncia. Fatty styrax, 3 litrai. Fresh roses, picked clean of "
        "their nails (sepals), 6 litrai. Mead (oinomeli), q.s. (sufficient quantity). "
        "Let the honey be first-quality, and the wine old and fragrant."
    ),
}
