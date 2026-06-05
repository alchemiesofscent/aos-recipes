# Cardamom Processing in AOS Recipes

Created: 2026-06-05  
Created by: codex  
Corpus: `data/recipes.json` and `data/recipes/*.json` in `/home/seanm/github/aos-recipes`

## Scope

This report extracts every current corpus recipe whose Greek text or structured
ingredient data contains cardamom forms (`καρδαμ*`, including
`καρδάμωμον`, `καρδαμώμου`, and `καρδαμώμῳ`). Provenance duplicates under
`provenance/source/` are excluded.

Result: 16 recipe records:

- 15 structured ingredient uses of cardamom.
- 1 text-only therapeutic co-use mention: Dioscorides 1.61.

Translations below are working translations of the cited Greek excerpts.

## Processing Type Summary

| Type | Recipe records | Processing pattern |
|---|---:|---|
| Water-treated cardamom in staged oil extraction | 4 | Cardamom is chopped or soaked/wetted in water, then oil is poured over it or it is cooked with oil. |
| Wine-soaked dry aromatics | 4 | Cardamom belongs to a dry aromatic set soaked in wine, then cooked, mixed, or used in an `ἐμβολή`. |
| Heated addition / co-boiling with aromatics | 2 | Cardamom is added during a boiling sequence or coarsely chopped with aromatics and boiled with wine/fat. |
| Substitute or variant aromatic | 1 | Cardamom substitutes for calamus and is co-soaked in a variant procedure. |
| Generic compounding or ingredient list only | 4 | Cardamom is listed as a component, but no cardamom-specific handling is given in this recipe record. |
| Therapeutic co-use, not a recipe ingredient | 1 | Cardamom is named as a companion in application, not as part of the perfume formula. |

## Type 1: Water-Treated Cardamom In Staged Oil Extraction

### Dioscorides 1.52, `dioscorides-1-52-sousinon`

Citation: Dioscorides, *De materia medica* 1.52.1-4; Wellmann 47.15-49.1.  
Recipe: σουσῖνον.  
Cardamom quantity: first 3 litrai + 6 unciae; later 10 holkai of chopped cardamom.

Greek text:

> εἶτα ἀπηθήσας τὸ ἔλαιον ἀπόχει κατὰ καρδαμώμου κεκομμένου καὶ βεβρεγμένου ὕδατι ὀμερίῳ λιτρῶν τριῶν οὐγγιῶν ἓξ καὶ ἐάσας βραχῆναι ἀπόθλιβε.
>
> ... πάλιν ἐπίχει τοῦ ήρωματισμένου ἐλαίου τὸ ἴσον πλῆθος τῷ προτέρῳ καὶ καρδαμώμου κεκομμένου συνέμβαλε ὁλκὰς δέκα, καὶ ἀνακινήσας χρησίμως ταῖς χερσὶ καὶ ἐπισχὼν μικρὸν ἐξίπου ...
>
> ... προσεπεμβάλλων καὶ τὸ καρδάμωμον ... καρδάμωμον παραμίσγων ... προσεμβάλλων καὶ τὸ καρδάμωμον ...

Translation:

> Then, after straining the oil, pour it over cardamom that has been chopped and wetted with rain-water, three litrai and six unciae; let it soak and press it out.
>
> Then pour again into the basin the same amount as before of the aromatized oil, and add ten holkai of chopped cardamom; stir it well with the hands, let it stand a little, and press it out.
>
> On the repeated passes, add the cardamom again; when repeating the procedure with fresh lilies, mix in cardamom and again add cardamom.

Notes:

- This is the most intensive cardamom handling in the corpus.
- Cardamom is first chopped and wetted with rain-water, then receives hot/aromatized oil.
- It is also added repeatedly during later lily extractions, suggesting cardamom functions as a persistent aromatic driver across multiple pressings.

### Dioscorides 1.55, `dioscorides-1-55-kyprinon`

Citation: Dioscorides, *De materia medica* 1.55; Wellmann 50.20-51.20.  
Recipe: κυπρῖνον.  
Cardamom quantity: 3 litrai + 9 unciae.

Greek text:

> ... καρδαμώμου λίτρας τρεῖς οὐγγίας ἐννέα ...
>
> ὅταν δὲ καὶ μετὰ τούτου ζέσῃ, καθελὼν ἀπήθησον τοῦ χαλκοῦ τὸ ἔλαιον καὶ κατάχει κατὰ τοῦ καρδαμώμου κεκομμένου καὶ πεφυραμένου τῷ λοιπῷ ὕδατι καὶ κίνει σπάθη, ἕως ἂν ψυγῇ, μὴ διαλείπων.

Translation:

> ... three litrai and nine unciae of cardamom ...
>
> When it has boiled also with this, take the oil down from the bronze vessel, strain it, and pour it over the cardamom, which has been chopped and kneaded with the remaining water; stir with a spatula until it cools, without stopping.

Notes:

- Cardamom is not boiled with the first aromatic charge. The oil is strained off and poured over separately prepared cardamom.
- Processing verbs: chopped (`κεκομμένου`), kneaded/wetted with water (`πεφυραμένου τῷ λοιπῷ ὕδατι`), stirred continuously while cooling.

### Paul 7.20.8, `paul-7-20-8`

Citation: Paul of Aegina, *Medical Epitome* 7.20.8; Heiberg 2.383.7-2.383.21.  
Recipe: Σούσινον σύνθετον.  
Cardamom quantity: 3 litrai.

Greek text:

> Ἐλαίου ξ̸ γ, καλάμου ἀρωματικοῦ λι. ε, σμύρνης 𐆄 ε, καρδαμώμου λι. γ ...
>
> εἰς τρεῖς ἐμβολὰς διαιρετέον τὴν ὅλην σκευήν ... δεύτερον δὲ τὸ καρδάμωμον ὕδατι ἀποβρέξαντες τρεῖς ἡμέρας κινοῦντες ὁμοίως συνεψήσομεν πάλιν μετὰ τοῦ ἐλαίου ἐπὶ α ὥραν ...

Translation:

> Three sextarii of oil, five litrai of aromatic calamus, five unciae of myrrh, three litrai of cardamom ...
>
> The whole preparation is to be divided into three infusions ... second, soak the cardamom in water for three days, stirring it in the same way, and again boil it together with the oil for one hour ...

Notes:

- Cardamom is the second `ἐμβολή`.
- The processing is explicit: water soaking for three days, repeated stirring, then one hour of cooking with oil.

### Paul 7.20.30, `paul-7-20-30`

Citation: Paul of Aegina, *Medical Epitome* 7.20.30; Heiberg 2.388.11-2.388.20.  
Recipe: Κρόκινον, with another crocomagma process.  
Cardamom quantity: 7 unciae.

Greek text:

> Ἐλαίου ὀμφακίζοντος εὐώδους λι. α, καλάμου ἀρωματικοῦ λι. ε, σμύρνης τρωγλίτιδος 𐆄 ε, καρδαμώμου 𐆄 ζ, κρόκου Κίλικος 𐆄 ϛ·
>
> τῆς μὲν πρώτης ἐμβολῆς ὁ κάλαμος ἔστω καὶ ἡ σμύρνα οἴνῳ λεῖα προαποβραχέντα γ ἡμέρας ... τῆς δὲ δευτέρας τὸ καρδάμωμον ὕδατι πρὸ μιᾶς ἀποβραχέν, τῆς τρίτης δὲ ὁ κρόκος οἴνῳ.

Translation:

> One litra of fragrant omphacizing oil, five litrai of aromatic calamus, five unciae of Troglodytic myrrh, seven unciae of cardamom, six unciae of Cilician saffron.
>
> For the first infusion, let the calamus and myrrh be smoothed with wine and soaked beforehand for three days ... for the second, the cardamom is to have been soaked in water one day before; for the third, the saffron in wine.

Notes:

- Cardamom is a distinct second infusion.
- The text explicitly gives a water pre-soak of one day. It does not spell out the subsequent cooking of the cardamom as fully as Paul 7.20.8, but the `ἐμβολή` structure places it in the staged extraction sequence.

## Type 2: Wine-Soaked Dry Aromatics

### Paul 7.20.22, `paul-7-20-22`

Citation: Paul of Aegina, *Medical Epitome* 7.20.22; Heiberg 2.386.5-2.386.11.  
Recipe: Μαστίχινον ποικιλώτερον.  
Cardamom quantity: 7 litrai.

Greek text:

> Ἐλαίου ξ̸ ν, ἑλενίου λι. ε, ξυλοβαλσάμου λι. ι, σχοίνου ἄνθους λι. ε, καρδαμώμου λι. ζ ... οἴνου εὐώδους ξ̸ ε, ὕδατος ξ̸ ι· καταβραχέντα τῷ οἴνῳ τὰ ξηρὰ πρὸ τρίτης ἡμέρας μίγνυται τῷ ἐλαίῳ καὶ τῷ ὕδατι καὶ ἕψεται ὥρας ϛ ...

Translation:

> Fifty sextarii of oil, five litrai of elecampane, ten litrai of xylobalsam, five litrai of schoinos flower, seven litrai of cardamom ... five sextarii of fragrant wine, ten sextarii of water. The dry ingredients, having been soaked in the wine before the third day, are mixed with the oil and water and boiled for six hours ...

Notes:

- Cardamom belongs to `τὰ ξηρά`, the dry aromatic set.
- Processing type: wine soak, then mixing with oil and water, then six hours of boiling.

### Paul 7.20.34, `paul-7-20-34`

Citation: Paul of Aegina, *Medical Epitome* 7.20.34; Heiberg 2.390.6-2.390.20.  
Recipe: Γλεύκινον.  
Cardamom quantity: 4 unciae.

Greek text:

> βʹ ἐμβολή· Κελτικῆς 𐆄 δ, κασάμου 𐆄 β, κυπέρου, κασσίας, ναρδοστάχυος, ἀσάρου, ἀμώμου, κόστου, σαμψύχου ἀνὰ 𐆄 γ, καλάμου ἀρωματικοῦ, καρυοφύλλου, φύλλου ἀνὰ 𐆄 β, καρδαμώμου 𐆄 δ· βρέχε οἴνῳ εὐώδει.
>
> ... σκεύαζε, καθάπερ καὶ τὸ δι' ὄμφακος, πλὴν τοῦ κηροῦ. ἐνταῦθα δὲ ζ ἡμέρας δεῖ τὰ εἴδη τῶν β ἐμβολῶν ἀποβρέχεσθαι.

Translation:

> Second infusion: four unciae of Celtic nard, two unciae of cassamum, and cyperus, cassia, nard-spike, asarum, amomum, costus, and sampsuchon at three unciae each; aromatic calamus, clove, and leaf at two unciae each; cardamom at four unciae. Soak in fragrant wine.
>
> Prepare it just as the omphax recipe, except for the wax. Here the materials of the two infusions must be soaked for seven days.

Notes:

- Cardamom is in the second infusion and is explicitly wine-soaked.
- The final process note makes the soaking period seven days for the two infusion sets.

### Paul 7.20.35, `paul-7-20-35`

Citation: Paul of Aegina, *Medical Epitome* 7.20.35; Heiberg 2.390.21-2.391.7.  
Recipe: Νάρδος Κυζικηνή.  
Cardamom quantity: 6 unciae by distributive `ἀνὰ`.

Greek text:

> αʹ ἐμβολή· ἐλαίου πρωτείου ξ̸ ι, ἀσπαλάθου, κυπέρων, ἑλενίου ἴρεως, ξυλοβαλσάμου, ἀριστολοχίας, καρδαμώμου, σχοίνου ἄνθους ἀνὰ 𐆄 ϛ ... βρέχε ταῦτα εἰς οἴνου εὐώδους ξ̸ δ.

Translation:

> First infusion: ten sextarii of first-quality oil; aspalathos, cyperus, elecampane iris, xylobalsam, aristolochia, cardamom, and schoinos flower, each six unciae ... Soak these in four sextarii of fragrant wine.

Notes:

- Cardamom is part of the first infusion's dry aromatic group.
- The explicit handling is wine soaking; the recipe then says to prepare it as already described.

### Paul 7.20.16, `paul-7-20-16`

Citation: Paul of Aegina, *Medical Epitome* 7.20.16; Heiberg 2.385.1-2.385.11.  
Recipe: Ἀμυγδάλινον, ὃ καὶ μετώπιον.  
Cardamom quantity: 1 litra.

Greek text:

> ... ἐλαίου ὀμφακίνου ξ̸ κ, ἀμυγδάλων πικρῶν λι. β, καρδαμώμου λι. α, σχοίνου ἄνθους, καλάμου ἀρωματικοῦ, καρποβαλσάμου ἀνὰ λι. α ... οἴνου εὐώδους εἰς τὸ ἐμβρέξαι τὰ ξηρὰ ξ̸ δ ...
>
> τὴν ῥητίνην καὶ τὴν χαλβάνην λειωθείσας μετὰ μέρους τοῦ ἐλαίου λύσαντες ἐμβαλοῦμεν τοῖς ἄλλοις ἑψηθεῖσιν καὶ τότε τὸ μέλι, μιχθέντα δὲ ἀκριβῶς ἅπαντα καθελόντες, ἕως ἔτι χλιαρόν ἐστι, σειροῦμεν ...

Translation:

> ... twenty sextarii of omphacine oil, two litrai of bitter almonds, one litra of cardamom, and one litra each of schoinos flower, aromatic calamus, and balsam-fruit ... four sextarii of fragrant wine for soaking the dry ingredients ...
>
> Grind the resin and galbanum, dissolve them with part of the oil, and add them to the other ingredients that have been boiled; then add the honey. When everything has been mixed thoroughly, take it down and strain it while it is still warm ...

Notes:

- Cardamom is one of the dry ingredients wetted with fragrant wine.
- The structured process data links it to the cooked remainder (`τοῖς ἄλλοις ἑψηθεῖσιν`) and the final thorough mixing.

## Type 3: Heated Addition Or Co-Boiling With Aromatics

### Aëtius 1.131, `aetius-1-131`

Citation: Aëtius of Amida, *Libri medicinales* 1.131; Olivieri 65.4-66.4.  
Recipe: Νάρδου Κυζικηνῆς σκευασία.  
Cardamom quantity: cardamom seed, 12 unciae by distributive `ἀνὰ`.

Greek text:

> ... ἀσπαλάθου κυπέρων ἴρεως ἰλλυρικῆς καρδαμώμου σπέρμα ἀριστολοχίας μακρᾶς ξυλοκασίας ἀνὰ 𐆄 ιβ ...
>
> ... εἶτ' ἐπιβαλὼν ἕτερον ὕδωρ καὶ οἴνου βραχὺ ἕψε. ὅταν δὲ ἀναζέσῃ, ἐπίβαλλε πρῶτον καρδάμωμον εἶτα σχοῖνον ξυλοκασίαν κεκομμένα καὶ ἕψε ἐπὶ ὥρας β καὶ πάλιν ἔα διανυκτερεῦσαι.

Translation:

> ... aspalathos, cyperus, Illyrian iris, cardamom seed, long aristolochia, and xylocassia, each twelve unciae ...
>
> Then add other water and a little wine and boil. When it boils up, add the cardamom first, then the schoinos and chopped xylocassia; boil for two hours and again let it stand overnight.

Notes:

- Cardamom is staged: it is added first after a renewed water/wine boil.
- The text then boils the mixture for two hours and leaves it overnight.
- The chopping adjective is clearest for the following schoinos/xylocassia group, not necessarily for cardamom.

### Dioscorides 2.76.8-10, `dioscorides-2-76-aromatized-calf-bull-deer-stear`

Citation: Dioscorides, *De materia medica* 2.76.8-10; Wellmann 154.5-154.15.  
Recipe: aromatized calf, bull, and deer fat.  
Cardamom quantity: 1 uncia by distributive `ἀνὰ`.

Greek text:

> ... μεῖξον δὲ καὶ καρδαμώμου καὶ νάρδου καὶ κασσίας καὶ κιναμώμου ἀνὰ οὐγγίαν μίαν — πάντα δὲ ἔστω ὁλοσχερέστερον κεκομμένα — εἶτα ἐπιδούς οἶνον εὐώδη ἀπέρεισαι ἐπ ἀνθράκων πεπωμασμένον τὸ ἀγγεῖον καὶ σύζεσον τρίς, ἄρας τε ἀπὸ τοῦ πυρὸς ἔασον ἐννυκτερεῦσαι αὐτό· τῇ δ᾿ ἐχομένῃ ἀπόχεε τὸν οἶνον καὶ ἄλλον ἐπιδοὺς τοῦ αὐτοῦ γένους σύζεσον ὁμοίως ἔτι τρὶς ...

Translation:

> Mix in also cardamom, nard, cassia, and cinnamon, one uncia each; all of them should be rather coarsely chopped. Then add fragrant wine, set the lidded vessel on coals, and boil it together three times. Remove it from the fire and let it stand overnight. On the next day pour off the wine, add another wine of the same kind, and boil again in the same way three more times ...

Notes:

- Cardamom is coarsely chopped with the aromatic set.
- It is processed in a sealed wine-and-fat aromatization cycle: repeated co-boiling, overnight standing, wine replacement, and renewed boiling.

## Type 4: Substitute Or Variant Aromatic

### Dioscorides 1.47, `dioscorides-1-47-telinon`

Citation: Dioscorides, *De materia medica* 1.47; Wellmann 45.1-45.15.  
Recipe: τηλῖνον.  
Cardamom quantity: none specified.

Greek text:

> οἱ δὲ ἀντὶ μὲν τοῦ καλάμου καρδάμωμον, ἀντὶ δὲ τῆς κυπέρου ξυλοβάλσαμον συναποβρέχουσιν. οἱ δὲ προστύφουσι τὸ ἔλαιον τούτοις καὶ μετὰ ταῦτα τὴν τῆλιν ἀποβρέχοντες ἐξιποῦσιν.

Translation:

> Some, instead of calamus, co-soak cardamom, and instead of cyperus, xylobalsam. Others first treat the oil with these, and after that soak the fenugreek and press it out.

Notes:

- This is a variant procedure, not the main formula.
- Cardamom replaces calamus and is co-soaked with the substitute aromatic set.

## Type 5: Generic Compounding Or Ingredient List Only

### Aëtius 1.125, `aetius-1-125`

Citation: Aëtius of Amida, *Libri medicinales* 1.125; Olivieri 63.3-63.9.  
Recipe: Μετώπιον.  
Cardamom quantity: none specified.

Greek text:

> σκευάζεται δὲ δι' ἐλαίου ὀμφακίνου καὶ ἀμυγδάλων πικρῶν καὶ καρδαμώμου καὶ σχίνου καὶ καλάμου καὶ μέλιτος καὶ οἴνου καὶ καρποβαλσάμου καὶ χαλβάνης καὶ ῥητίνης.

Translation:

> It is prepared with omphacine oil, bitter almonds, cardamom, schoinos, calamus, honey, wine, balsam-fruit, galbanum, and resin.

Notes:

- Cardamom is part of the metopion ingredient set.
- No cardamom-specific operation is given in this Aëtius summary.

### Dioscorides 1.59, `dioscorides-1-59-metopion`

Citation: Dioscorides, *De materia medica* 1.59.1-2; Wellmann 54.10-55.5.  
Recipe: μετώπιον.  
Cardamom quantity: none specified.

Greek text:

> διʼ ἀμυγδάλων δὲ πικρῶν καὶ ἐλαίου ὀμφακίνου καὶ καρδαμώμου καὶ σχοίνου καὶ καλάμου καὶ μέλιτος καὶ οἴνου καὶ σμύρνης καὶ βαλσάμου καρποῦ καὶ χαλβάνης καὶ ῥητίνης συντίθεται. δόκιμον δέ ἐστι τὸ βαρύοσμον καὶ λιπαρόν, ἐμφαῖνον μᾶλλον τοῦ καρδαμώμου καὶ τῆς σμύρνης ἤπερ τῆς χαλβάνης.

Translation:

> It is compounded with bitter almonds, omphacine oil, cardamom, schoinos, calamus, honey, wine, myrrh, balsam-fruit, galbanum, and resin. The approved kind is heavy-smelling and oily, showing more of cardamom and myrrh than of galbanum.

Notes:

- No mechanical handling is specified here.
- Cardamom is important sensorially: the approved metopion should smell more of cardamom and myrrh than of galbanum.

### Aëtius 1.133, `aetius-1-133`

Citation: Aëtius of Amida, *Libri medicinales* 1.133; Olivieri 67.21-68.3.  
Recipe: Φυλλίνου ἤτοι μαλαβαθρίνου σκευασία καλλίστη.  
Cardamom quantity: 6 unciae.

Greek text:

> ... ὀποβαλσάμου 𐆄 ϛʹ ἀρνάβω 𐆄 ϛʹ καρδαμώμου 𐆄 ϛʹ ἴρεως λίτρα α ἐλαίου 𐅵 κ οἴνου εὐώδους τὸ ἀρκοῦν· ἕψε ὡς τὴν νάρδον.

Translation:

> ... six unciae of opobalsam, six unciae of arnabo, six unciae of cardamom, one litra of iris, twenty units of oil, and enough fragrant wine. Boil it as for the nard.

Notes:

- The record gives only a delegated process: `boil as for the nard`.
- Because the recipe points to the nard method, it likely depends on the preceding nard workflow, but this cardamom record itself does not spell out a separate treatment.

### Aëtius 16.131.2, `aetius-16-131-2`

Citation: Aëtius of Amida, *Libri medicinales* 16.131.2; Zervos 163.21-163.25.  
Recipe: ἄλλη γραφὴ φουλιάτου.  
Cardamom quantity: 1 uncia by distributive `ἀνὰ`.

Greek text:

> Κηροῦ λιτ. α. νάρδου κυζικηνικοῦ λίτ. γ. πίσσης βρυτίας γοε. λαδάνου γοα. στύρακος λιπαροῦ γογ. κόστου, κασίας ἀνὰ γοβ. καρδαμώμου, φύλλου ἀνὰ γοα. ναρδοστάχυος γοα. τὸ ζʹ. ἤτοι τὸ ἥμισ. κρόκου, οἴνου ἀμιναίου ἀνὰ γοα. ὀποβαλσάμου γογ.

Translation:

> One litra of wax, three litrai of Cyzicene nard, five unciae of Brytian pitch, one uncia of ladanum, three unciae of fatty storax, costus and cassia two unciae each, cardamom and leaf one uncia each, nard-spike one uncia, the seventh part, that is, the half; saffron and Aminaean wine one uncia each, opobalsam three unciae.

Notes:

- This is an ingredient formula only.
- The record notes uncertainty over the transmitted phrase `τὸ ζʹ. ἤτοι τὸ ἥμισ.` after nard-spike.

## Type 6: Therapeutic Co-Use, Not A Recipe Ingredient

### Dioscorides 1.61, `dioscorides-1-61-kinamominon`

Citation: Dioscorides, *De materia medica* 1.61; Wellmann 55.15-56.15.  
Recipe: κιναμώμινον.  
Cardamom quantity: none specified.

Greek text:

> ποιεῖ καὶ τρὸς σύριγγας καὶ σῆ πας ἐναργῶς καὶ πρὸς ὑδροκήλας καὶ ἄνθρακας καὶ γαγγραίνας σὺν καρδαμώμῳ, πρός τε ῥίγη τὰ περιοδικὰ καὶ πρὸς τρόμους καὶ τοὺς ὑπὸ τῶν ἰοβόλων θηρίων δακνομένους ἐν συγχρίσματι ...

Translation:

> It also works clearly for fistulas and putrefactions, and for hydroceles, carbuncles, and gangrenes when used with cardamom; also for periodic chills and tremors, and for those bitten by venomous animals, in an anointing mixture ...

Notes:

- Cardamom is not a structured ingredient of the cinnamon-oil formula in this record.
- It is a therapeutic co-use: the finished product is applied `with cardamom` for certain indications.

## Overall Notes

- Cardamom is most actively processed in lily oil and cyprinum recipes: it is chopped, wetted or kneaded with water, contacted with strained oil, stirred, pressed, and reintroduced through repeated extractions.
- In Paul's perfume recipes, cardamom commonly belongs to an `ἐμβολή` stage. It is either soaked in water as a distinct cardamom stage or grouped with dry aromatics soaked in fragrant wine.
- In metopion-type recipes, cardamom is often listed as a component and may define the desired odor profile, but the surviving recipe text may not specify a cardamom-specific process.
- One Dioscorides record names cardamom only as a medicinal companion in use, not as a recipe component.
