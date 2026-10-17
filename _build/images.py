#!/usr/bin/env python3
"""Generate optimized WebP assets for the Atelier Culemborg site.

Source images come from the original iWeb site (../_source/Atelier_Culemborg).
Output: assets/img/<slug>[-<width>].webp + assets/img/manifest.json
"""
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path(os.environ.get("ATELIER_SOURCE", "/workspace/_atelier-source/Atelier_Culemborg"))
OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# slug, source file, alt text (Dutch)
IMAGES = [
    ("logo-atelier-culemborg", "Home_files/shapeimage_2[1].jpg",
     "Logo van Atelier Culemborg: penselen met verf boven de handgeschreven naam"),
    ("portret-alicja-gootzen", "Contact_files/shapeimage_2.png",
     "Alicja Gootzen, kunstenares van Atelier Culemborg"),
    ("kunstwerk-waterlelies", "Home_files/home_kunstwerk_nieuw.jpg",
     "Aquarel met waterlelies en bloemen in blauwe, groene en paarse tinten"),

    ("cursus-aquarel", "Aquarel_files/P8150003.jpg",
     "Aquarel van zonnebloemen in gele en blauwe tinten"),
    ("cursus-acryl", "Acryl_files/P8140007.jpg",
     "Acrylschilderij van zonnebloemen op een ezel, met verftubes en palet"),
    ("cursus-olieverf", "Olieverf_files/P8150007.jpg",
     "Olieverfschilderij van zonnebloemen in warme gele tinten"),
    ("cursus-gemengde-technieken", "Gemengde_Technieken_files/P8150008.jpg",
     "Ingelijst werk in gemengde techniek met een vogel"),
    ("cursus-pastelkrijt", "Pastelkrijt_files/Foto's tekenles nieuwe site - 17.jpg",
     "Pasteltekening van een landschap met een kerktoren tussen bomen"),
    ("cursus-tekenen", "Tekenen_files/DSCN2101.jpg",
     "Houtskooltekening van een leeuwenkop"),
    ("cursus-tekenen-houtskool", "Tekenen_files/shapeimage_2.png",
     "Houtskooltekening van een meisje dat viool speelt"),

    ("modetekenen-1", "Modetekenen_files/Foto's tekenles nieuwe site - 05.jpg",
     "Modetekening van een figuur met hoed en gestreepte jas"),
    ("modetekenen-2", "Modetekenen_files/Foto's tekenles nieuwe site - 08.jpg",
     "Modetekening op een groene achtergrond met ruitpatroon"),
    ("modetekenen-3", "Modetekenen_files/Foto's tekenles nieuwe site - 09.jpg",
     "Modetekening in zwart-wit met een rood ruitpatroon"),

    ("jongeren-1", "Jongeren_files/Foto's tekenles nieuwe site - 16.jpg",
     "Schilderij van een witte zwaan in pasteltinten"),
    ("jongeren-2", "Jongeren_files/Foto's tekenles nieuwe site - 18.jpg",
     "Portretschilderij van een leeuw"),

    ("kinderen-1", "Kinderen_files/Foto's tekenles nieuwe site - 12.jpg",
     "Kindertekeningen in een vitrinekast"),
    ("kinderen-2", "Kinderen_files/shapeimage_2.png",
     "Vitrine met werk van de kindertekencursus"),
    ("kinderen-3", "Kinderen_files/DSCN1390.jpg",
     "Expositie met tekeningen in de openbare bibliotheek van Culemborg"),
    ("kinderen-4", "Kinderen_files/Knipsel 1.jpg",
     "Meisje aan het tekenen aan tafel"),

    ("natuursteen-1", "Over_mij_files/DSCN2370.jpg",
     "Beeld van twee olifanten, gebeeldhouwd uit natuursteen"),
    ("natuursteen-2", "Over_mij_files/DSCN2381.jpg",
     "Beeld van vogels op een sokkel, gebeeldhouwd uit natuursteen"),
    ("natuursteen-3", "Over_mij_files/DSCN2388.jpg",
     "Beeld van twee figuren met kronen, gebeeldhouwd uit natuursteen"),
    ("natuursteen-4", "Over_mij_files/DSCN2390.jpg",
     "Beeld van twee gevleugelde figuren, gebeeldhouwd uit natuursteen"),

    ("expo-2024-1", "Exposities_files/IMG_20240706_164152_1.jpg",
     "Ezel met kinderwerk tijdens de expositie in 2024"),
    ("expo-2024-2", "Exposities_files/IMG_20240706_164246.jpg",
     "Werk van cursisten op tafels in een kerkzaal, expositie 2024"),
    ("expo-2018-1", "Exposities_files/IMG_20181013_124846.jpg",
     "Bezoekers bekijken schilderijen in het oude stadhuis, expositie 2018"),
    ("expo-2018-2", "Exposities_files/IMG_20181013_132823.jpg",
     "Gang van het oude stadhuis met schilderijen, expositie 2018"),
    ("expo-2016-1", "Exposities_files/14720392_319569408429888_4616033394399933871_n.jpg",
     "Bezoekers bij tekeningen en schilderijen, expositie 2016"),
    ("expo-2016-2", "Exposities_files/14925283_319569575096538_5281680739288038596_n.jpg",
     "Ingang van de expositieruimte met affiche en ballonnen, 2016"),
    ("expo-2015-1", "Exposities_files/41DSC01309.jpg",
     "Schilderijen in een historische zaal, expositie 2015"),
    ("expo-2013-1", "Exposities_files/IMG_2411.jpg",
     "Schilderij aan de wand in de openbare bibliotheek, 2013"),
]

MAX_LG = 1500
MAX_SM = 720


def save(img, path, quality=82):
    img.save(path, "WEBP", quality=quality, method=6)


def main():
    manifest = {}
    for slug, rel, alt in IMAGES:
        src = SRC / rel
        if not src.exists():
            sys.exit(f"missing source: {src}")
        im = Image.open(src)
        im = im.convert("RGB")
        w, h = im.size
        entry = {"alt": alt, "source": rel, "w": w, "h": h, "variants": {}}

        if w > MAX_SM + 80:
            lg = im.copy()
            if w > MAX_LG:
                lg = lg.resize((MAX_LG, round(h * MAX_LG / w)), Image.LANCZOS)
            p = OUT / f"{slug}-{lg.width}.webp"
            save(lg, p, 84)
            entry["variants"]["lg"] = p.name
            entry["lg_w"], entry["lg_h"] = lg.size

            sm = im.copy()
            sm = sm.resize((MAX_SM, round(h * MAX_SM / w)), Image.LANCZOS)
            p = OUT / f"{slug}-{sm.width}.webp"
            save(sm, p, 80)
            entry["variants"]["sm"] = p.name
            entry["sm_w"], entry["sm_h"] = sm.size
        else:
            p = OUT / f"{slug}.webp"
            save(im, p, 84)
            entry["variants"]["only"] = p.name
            entry["only_w"], entry["only_h"] = im.size

        manifest[slug] = entry
        print(f"{slug:30s} {w}x{h}  " + " ".join(f"{k}:{v}" for k, v in entry["variants"].items()))

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")

    # ---- social preview (1200x630) ----
    og = Image.new("RGB", (1200, 630), (20, 18, 22))
    logo = Image.open(SRC / "Home_files/shapeimage_2[1].jpg").convert("RGB")
    logo = logo.resize((760, round(logo.height * 760 / logo.width)), Image.LANCZOS)
    og.paste(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2 - 30))
    d = ImageDraw.Draw(og)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    except OSError:
        f = ImageFont.load_default()
    txt = "Teken- en schilderlessen in Culemborg"
    tw = d.textlength(txt, font=f)
    d.text(((1200 - tw) / 2, 500), txt, font=f, fill=(180, 168, 190))
    og.save(OUT / "og-atelier-culemborg.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    print("og image written")

    # ---- apple touch icon ----
    ic = Image.new("RGB", (180, 180), (58, 44, 66))
    d = ImageDraw.Draw(ic)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 84)
    except OSError:
        f = ImageFont.load_default()
    tw = d.textlength("AC", font=f)
    d.text(((180 - tw) / 2, 40), "AC", font=f, fill=(243, 237, 246))
    ic.save(OUT / "apple-touch-icon.png", optimize=True)
    print("icon written")


if __name__ == "__main__":
    main()
