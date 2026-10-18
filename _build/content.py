# -*- coding: utf-8 -*-
"""Inhoud van de site. Alle lopende tekst is overgenomen uit de oorspronkelijke
iWeb-site; alleen hier en daar is een spelfout hersteld. Nieuwe zinnen zijn
beperkt tot koppen en korte navigatieteksten."""

SITE_URL = "https://peter-jangootzen.github.io/atelierculemborg"
SITE_BASE = "/atelierculemborg/"  # alleen gebruikt voor 404.html

SITE = {
    "name": "Atelier Culemborg",
    "tagline": "Teken- en schilderlessen in Culemborg",
    "street": "Achter ’t Zand 87",
    "postcode": "4103 XN",
    "city": "Culemborg",
    "phone": "0345-522241",
    "phone_link": "+31345522241",
    "email": 'info@atelierculemborg.nl',
}

NAV = [
    ("Home", "index.html"),
    ("Over mij", "over-mij.html"),
]

# (slug, naam, ondertitel in het menu)
# group: "lessen" (voor wie) of "technieken" (waarmee)
COURSES = [
    dict(
        slug="kinderen",
        group="lessen",
        nav="Kinderen",
        name="Kinderen",
        h1="Teken- en schilderlessen voor kinderen",
        kicker="Les · 7 – 10 jaar",
        age="7 – 10 jaar",
        summary="Spelenderwijze komen de kinderen hier met kunst in aanraking.",
        image="kinderen-1",
        body=[
            "Spelenderwijze komen de kinderen hier met kunst in aanraking.",
            "Elke week hebben wij een bepaald thema die wij met de kinderen bespreken en gaan tekenen of schilderen. Het kan een dier, mens, landschap, een stripverhaal of iets anders zijn.",
            "Er wordt met verschillende technieken gewerkt: o.a. houtskool, aquarel, acryl, pastel.",
            "Ook wordt er op verschillende materialen gewerkt: o.a. canvasdoeken, papier en hout.",
            "De kinderen krijgen goede begeleiding, maar ook veel vrijheid voor hun eigen beeldvorming.",
            "Deze les is voor kinderen in de leeftijd 7 tot 10 jaar.",
            "Aanmelden kan het hele schooljaar door. Geen les tijdens de schoolvakantie.",
            "Expositie in de openbare bibliotheek van Culemborg in juni 2012.",
        ],
        gallery=["kinderen-2", "kinderen-3", "kinderen-4"],
        gallery_caption="Exposities in de openbare bibliotheek en het stadskantoor in Culemborg.",
        tags=["Houtskool", "Aquarel", "Acryl", "Pastel"],
    ),
    dict(
        slug="jongeren",
        group="lessen",
        nav="Jongeren",
        name="Jongeren",
        h1="Teken- en schilderlessen voor de jeugd",
        kicker="Les · 11 – 17 jaar",
        age="11 – 17 jaar",
        summary="Voor jongeren die de wereld van kleuren, vormen en verschillende technieken willen ontdekken.",
        image="jongeren-1",
        body=[
            "Deze les is voor jongeren die de wereld van kleuren, vormen en verschillende technieken willen ontdekken. Plezier en voldoening staan hier centraal.",
            "Er wordt met zeer verschillende thema’s gewerkt: o.a. dieren, mensen, landschappen, mode en stripverhalen.",
            "Jongeren krijgen goede begeleiding. Zij leren op een ongedwongen manier over kleurmenging, gebruik van lijnen, schaduw en perspectief.",
            "Deze les is voor jongens en meiden in de leeftijd van 11 tot 17 jaar.",
            "Het atelier ligt op loopafstand van NS- en busstation Culemborg.",
            "Goed bereikbaar vanuit Geldermalsen, Buurmalsen, Tricht, Houten en Utrecht!",
            "Aanmelden kan het hele schooljaar door. Geen les tijdens de schoolvakantie.",
        ],
        gallery=["jongeren-2"],
        tags=["Dieren", "Mensen", "Landschappen", "Mode", "Stripverhalen"],
    ),
    dict(
        slug="volwassenen",
        group="lessen",
        nav="Volwassenen",
        name="Volwassenen",
        h1="Teken- en schilderlessen voor volwassenen",
        kicker="Les · 18 jaar en ouder",
        age="18 jaar en ouder",
        summary="In uw eigen tempo werken aan de onderwerpen en technieken die bij u passen.",
        image="cursus-olieverf",
        body=[
            "Voor volwassenen die graag willen leren tekenen en schilderen, of die het na jaren weer willen oppakken.",
            "Er zijn vele thema’s mogelijk, bijvoorbeeld: landschappen, bloemen, stillevens, abstracte vormen, portretten van mensen en huisdieren, of modetekenen.",
            "U kiest zelf de techniek waarmee u werkt: aquarel, acryl, olieverf, pastelkrijt, inkt, houtskool of een combinatie daarvan.",
            "De begeleiding is persoonlijk: u werkt in uw eigen tempo, naar uw eigen inspiratie of naar opdracht, met aandacht voor kleurgebruik, licht en schaduw, lijnen en perspectief.",
            "Het atelier ligt op loopafstand van NS- en busstation Culemborg.",
            "Goed bereikbaar vanuit Geldermalsen, Buurmalsen, Tricht, Houten en Utrecht!",
            "Aanmelden kan het hele schooljaar door. Geen les tijdens de schoolvakantie.",
        ],
        gallery=[],
        tags=["Eigen tempo", "Eigen onderwerp", "Alle technieken"],
    ),
    dict(
        slug="individueel",
        group="lessen",
        nav="Individueel",
        name="Individueel",
        h1="Individuele teken- en schilderlessen",
        kicker="Les · in overleg",
        age="In overleg",
        summary="Les aan huis of alleen werken, in overleg afgestemd op wat bij u past.",
        image="cursus-acryl",
        body=[
            "Bent u door leeftijd of een handicap aan huis gebonden of vindt u het niet zo plezierig om in een groep te werken?",
            "Er bestaat de mogelijkheid om individuele teken- en schilderlessen te volgen.",
            "Tijdens een gesprek wordt er gekeken welke teken- en schildertechniek bij u past.",
            "U leert alles over het mengen van kleuren, toepassen van licht en schaduw, het gebruik van lijnen, perspectief en het kiezen van het juiste onderwerp. U leert bewuster kijken naar de dingen om u heen. U werkt naar uw eigen inspiratie of naar een opdracht.",
            "Tekenen en schilderen kunnen een geweldige bezigheid en een welkome invulling van uw vrije tijd worden! Lestijden en kosten van de lessen in overleg.",
        ],
        gallery=[],
        tags=["Aan huis", "Eigen tempo", "In overleg"],
    ),
    dict(
        slug="modetekenen",
        group="technieken",
        nav="Modetekenen",
        name="Modetekenen",
        h1="Modetekenen",
        kicker="Techniek · mode en ontwerpen",
        summary="Stap voor stap een model, rok, topje, broek en accessoires leren tekenen en schilderen.",
        image="modetekenen-1",
        body=[
            "Teken je graag? Vind je mode leuk? Of wil je voor jezelf iets ontwerpen?",
            "In deze les leer je stap voor stap hoe je bijvoorbeeld een model, rok, topje, broek en accessoires kunt tekenen en schilderen. Deze les is zowel voor jeugd als voor volwassenen.",
            "Je leert over compositie, kleuren en het gebruik van lijnen. Je ontwerpen worden in kleur (aquarel, acryl of inkt) en stof uitgewerkt. Er komen zowel moderne als historische ontwerpen aan bod.",
            "Het atelier ligt op loopafstand van NS- en busstation Culemborg.",
            "Goed bereikbaar vanuit Geldermalsen, Buurmalsen, Tricht, Houten en Utrecht!",
            "Aanmelden kan het hele schooljaar door. Geen les tijdens de schoolvakantie.",
        ],
        gallery=["modetekenen-2", "modetekenen-3"],
        tags=["Aquarel", "Acryl", "Inkt", "Stof"],
    ),
    dict(
        slug="tekenen",
        group="technieken",
        nav="Tekenen",
        name="Tekenen",
        h1="Tekenen",
        kicker="Techniek · potlood, houtskool en krijt",
        summary="Stap voor stap leren hoe je een dier, mens of landschap tekent.",
        image="cursus-tekenen",
        body=[
            "In deze les leer je stap voor stap hoe je dingen als een dier, mens of landschap tekent.",
            "Je leert alles over het gebruik van lijnen, proporties en het toepassen van licht en schaduw.",
            "De begeleiding tijdens de les is zeer individueel. Iedere cursist bepaalt zijn eigen tempo.",
            "Er wordt gewerkt met potlood, houtskool en krijt.",
        ],
        gallery=["cursus-tekenen-houtskool"],
        tags=["Potlood", "Houtskool", "Krijt"],
    ),
    dict(
        slug="aquarel",
        group="technieken",
        nav="Aquarel",
        name="Aquarel",
        h1="Aquarel",
        kicker="Techniek · waterverf",
        summary="Alles over aquarelverf, penselen, doseren met water en papier opspannen.",
        image="cursus-aquarel",
        body=[
            "Bent u altijd al geraakt door de transparantie, het vele licht en de grote intensiteit van een aquarel? Ontdek en beleef aquarel!",
            "U leert in deze les alles over deze techniek.",
            "U leert omgaan met aquarelverf, penselen, penseelhouding, doseren met water, aquarelpapier en papier opspannen op een raam.",
            "Er wordt uitgelegd over het licht, schaduw, kleurmenging, diepte en sfeer in uw kunstwerk.",
            "U werkt in kleine groepen in uw eigen tempo met begeleiding. U werkt naar eigen inspiratie of naar opdracht.",
        ],
        gallery=[],
        tags=["Transparantie", "Kleurmenging", "Licht en schaduw"],
    ),
    dict(
        slug="acryl",
        group="technieken",
        nav="Acryl",
        name="Acryl",
        h1="Acryl",
        kicker="Techniek · acrylverf",
        summary="Levendige kleuren en alle effecten van acrylverf, van wassing tot dekkende laag.",
        image="cursus-acryl",
        body=[
            "Bent u geïnspireerd door de vele mogelijkheden van acrylverf? Of wilt u het graag uitproberen?",
            "In deze les leert u de levendige kleuren kennen en alle effecten die u met acrylverf kunt verkrijgen. U leert stap voor stap de verschillende technieken toepassen; van transparante wassingen tot dekkende verflagen. U leert over kleurmenging, licht, schaduw, diepte en sfeer in uw schilderwerk.",
            "Acryl is ideaal om mee te experimenteren en voor het creëren van speciale effecten.",
            "U werkt naar uw eigen inspiratie of naar opdracht.",
        ],
        gallery=[],
        tags=["Wassingen", "Kleurmenging", "Speciale effecten"],
    ),
    dict(
        slug="olieverf",
        group="technieken",
        nav="Olieverf",
        name="Olieverf",
        h1="Olieverf",
        kicker="Techniek · olieverf",
        summary="De vele aspecten van olieverf: opbouw, kleurmenging, sfeer en nat-op-nat.",
        image="cursus-olieverf",
        body=[
            "In deze les schilderen met olieverf leert u de vele aspecten van deze duurzame techniek kennen.",
            "U leert over kleurmenging, het toepassen van licht en schaduw, perspectief en het verkrijgen van sfeer in uw schilderij. U komt te weten over het opbouwen met en het gebruik van lijnen in een schilderij. U kunt kiezen voor de stap-voor-stap techniek, maar ook de nat-op-nat techniek is mogelijk.",
            "U werkt naar uw eigen inspiratie of naar opdracht.",
        ],
        gallery=[],
        tags=["Stap voor stap", "Nat-op-nat", "Perspectief"],
    ),
    dict(
        slug="pastelkrijt",
        group="technieken",
        nav="Pastelkrijt",
        name="Pastelkrijt",
        h1="Pastelkrijt",
        kicker="Techniek · pastelkrijt",
        summary="Zeer levendige kleuren en het spel tussen licht en donker, laag over laag.",
        image="cursus-pastelkrijt",
        body=[
            "Hebt u ooit met pastelkrijt gewerkt? U vindt deze techniek erg leuk maar wel moeilijk of misschien bent u niet tevreden over uw eigen resultaten?",
            "Niet opgeven! In deze les leert u alles over deze geweldige, zeer kleurrijke techniek.",
            "Er zijn vele mogelijkheden. Zeer levendige kleuren, het spel tussen licht en donker, en de licht poederige structuur van pastelkrijt maken deze techniek zo uniek. Vormen komen tot leven in een bijna mystieke sfeer.",
            "In deze les leert u alles over pastelkrijt: het toepassen van licht en schaduw, perspectief, het gebruik van de lijnen, mengen van kleuren, laag-over-laag werken, herstellen van gemaakte fouten. U kunt uw eigen onderwerp kiezen.",
            "U werkt naar uw eigen inspiratie of naar opdracht.",
        ],
        gallery=[],
        tags=["Laag over laag", "Kleurmenging", "Eigen onderwerp"],
    ),
    dict(
        slug="gemengde-technieken",
        group="technieken",
        nav="Gemengde technieken",
        name="Gemengde technieken",
        h1="Gemengde technieken",
        kicker="Techniek · inkt, aquarel, acryl, Chinees en pastel",
        summary="Vele teken- en schildertechnieken in korte tijd uitproberen.",
        image="cursus-gemengde-technieken",
        lead_extra="Inkt, aquarel, acryl, Chinees en pastel",
        body=[
            "U vindt tekenen en schilderen erg leuk. U weet nog niet welke techniek u het leukste lijkt? Of wilt u de diverse technieken een keer uitproberen?",
            "In deze les komen vele teken- en schildertechnieken aan bod. In korte tijd leert u een bepaalde techniek kennen, het toepassen van licht en schaduw, mengen van kleuren, gebruik van lijnen en perspectief.",
            "U werkt naar uw eigen inspiratie of naar opdracht.",
        ],
        gallery=[],
        tags=["Inkt", "Aquarel", "Acryl", "Chinees", "Pastel"],
    ),
]

LESSEN = [c for c in COURSES if c["group"] == "lessen"]
TECHNIEKEN = [c for c in COURSES if c["group"] == "technieken"]

HOME = {
    "title": "Atelier Culemborg — teken- en schilderlessen in Culemborg",
    "description": "Teken- en schilderlessen in Culemborg: aquarel, acryl, olieverf, pastel, tekenen en modetekenen. Voor kinderen, jongeren en volwassenen.",
    "intro": "Bij Atelier Culemborg wordt met veel aandacht en onder deskundige begeleiding gekeken naar uw persoonlijke wensen. Zowel les in groepen als individuele les is mogelijk.",
    "themes": [
        "Er zijn vele thema’s mogelijk, bijvoorbeeld: landschappen, bloemen, stillevens, abstracte vormen, portretten van mensen/huisdieren en modetekenen.",
        "Er wordt met verschillende technieken gewerkt, waaronder: aquarel, acryl, olieverf, pastel, inkt, houtskool en gemengde technieken.",
        "U werkt in uw eigen tempo.",
    ],
    "travel": [
        "Het atelier ligt op loopafstand van NS- en busstation Culemborg.",
        "Goed bereikbaar vanuit Geldermalsen, Buurmalsen, Tricht, Tiel, Houten en Utrecht!",
    ],
}

ABOUT = {
    "title": "Over mij — Atelier Culemborg",
    "description": "Alicja Gootzen geeft in haar atelier in Culemborg teken- en schilderlessen aan kinderen, jeugd en volwassenen, en cultuurlessen in Buren.",
    "body": [
        "In mijn eigen atelier in Culemborg geef ik teken- en schilderlessen aan kinderen, jeugd en volwassenen. Cursisten kunnen kiezen uit verschillende thema’s: landschappen, dieren, portretten, striptekenen en modetekenen.",
        "Plezier in tekenen en schilderen, maar ook goede begeleiding staan bij mij altijd centraal.",
        "Daarnaast geef ik met heel veel plezier cultuurlessen in groepen van 3 t/m 8 op de Koningin Beatrix school in Buren. Ook heb ik voor de Wereldwinkel tevens een aantal schetsen/ontwerpen gemaakt met als thema ‘kerstfeest’. Deze zijn door een Zimbabwaanse kunstenaar gebeeldhouwd uit natuursteen en zijn nu te koop in een aantal wereldwinkels.",
    ],
    "gallery_caption": "Beelden uit natuursteen, gemaakt naar schetsen en ontwerpen voor de Wereldwinkel.",
}

EXPOS = {
    "title": "Exposities — Atelier Culemborg",
    "description": "Exposities van werk van cursisten van Atelier Culemborg in Culemborg: het oude stadhuis, de bibliotheek en de kerkzaal.",
    "intro": "Een selectie van exposities van Atelier Culemborg.",
    "sections": [
        {
            "h": "Expositie kinderen en jongeren van Atelier Culemborg, juli 2024",
            "images": ["expo-2024-1", "expo-2024-2"],
        },
        {
            "h": "Expositie van volwassenen en jongeren in het oude stadhuis in Culemborg, november 2018",
            "images": ["expo-2018-1", "expo-2018-2"],
        },
        {
            "h": "Expositie van kinderen en jongeren, november 2016",
            "images": ["expo-2016-1", "expo-2016-2"],
            "link": ("Klik hier voor meer foto’s", 'https://www.facebook.com/media/set/?set=a.319568861763276.1073741831.307081719678657&type=3'),
        },
        {
            "h": "Expositie in het oude stadhuis in Culemborg, november 2015",
            "images": ["expo-2015-1"],
        },
        {
            "h": "Exposities in de openbare bibliotheek van Culemborg, 2013",
            "images": ["expo-2013-1"],
        },
    ],
}

CONTACT = {
    "title": "Contact — Atelier Culemborg",
    "description": "Contact met Atelier Culemborg: Alicja Gootzen, Achter ’t Zand 87, 4103 XN Culemborg. Telefoon 0345-522241 of info@atelierculemborg.nl.",
}
