# Atelier Culemborg — website

Statische website van Atelier Culemborg (teken- en schilderlessen in Culemborg).
Geen WordPress, geen PHP, geen database: alleen HTML, één stylesheet, één klein
JavaScript-bestand en geoptimaliseerde afbeeldingen.

## Structuur

```
index.html                  home
cursussen.html              overzicht van alle cursussen
kinderen.html               ↓ de tien cursuspagina's
jongeren.html
modetekenen.html
tekenen.html
aquarel.html
acryl.html
olieverf.html
pastelkrijt.html
gemengde-technieken.html
individueel.html
over-mij.html
exposities.html
contact.html
404.html

assets/css/style.css        alle vormgeving
assets/js/site.js           menu, submenu, lightbox (geen dependencies)
assets/fonts/               3 zelf-gehoste woff2-bestanden (Cormorant Garamond + Inter)
assets/img/                 webp-afbeeldingen + manifest.json

Atelier_Culemborg/*.html    doorverwijzingen vanaf de oude iWeb-URL's
_build/                     generator (content.py, build.py, images.py)
```

## Lokaal bekijken

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## Aanpassen

De tekst staat in `_build/content.py`. Na een wijziging:

```bash
python3 _build/build.py      # schrijft alle HTML opnieuw
```

`_build/build.py` genereert ook `sitemap.xml`, `robots.txt`, `favicon.svg` en de
doorverwijspagina's in `Atelier_Culemborg/`. Pas je het adres of de contactgegevens
aan, dan hoef je dat alleen in `content.py` (bovenin, bij `SITE`) te doen.

## Afbeeldingen

`_build/images.py` maakt uit de originele foto's geoptimaliseerde WebP-bestanden
(van 5,2 MB naar 1,3 MB) en een `manifest.json` met breedte, hoogte en alt-tekst.
Het script verwacht de oude iWeb-export; zonder die export is het niet nodig —
nieuwe foto's kun je ook met de hand als `.webp` in `assets/img/` zetten en in
`content.py` opnemen.

## Publiceren

De site draait op GitHub Pages (branch `main`, map `/`). Na een push is de site
binnen een minuut bijgewerkt op <https://peter-jangootzen.github.io/atelierculemborg/>.

### Eigen domein

`atelierculemborg.nl` staat nog op de oude hosting. Bij het overstappen:

1. `CNAME` met daarin `atelierculemborg.nl` in de root van deze repository zetten
   (of het domein invullen bij *Settings → Pages → Custom domain*).
2. In `_build/content.py` `SITE_URL` en `SITE_BASE` aanpassen en opnieuw builden,
   zodat canonical-URL's, sitemap en de 404-pagina kloppen.
3. DNS bij de provider omzetten naar GitHub Pages (A-records voor het apex-domein,
   `CNAME` voor `www`).
4. De oude bestanden op de Plesk-server kunnen daarna blijven staan of worden
   verwijderd; de oude URL's (`/Atelier_Culemborg/Home.html`) verwijzen in deze
   repository al door naar de nieuwe pagina's.

## Wat er veranderd is ten opzichte van de iWeb-site

- Vaste 700-pixelbreedte en absolute posities vervangen door responsieve layout.
- Eén navigatiemenu met een submenu voor de cursussen, ook bruikbaar op de telefoon.
- Eigen lettertypen (Cormorant Garamond en Inter), zelf gehost — geen Google Fonts.
- Afbeeldingen als WebP, met `width`/`height` en lazy loading.
- SEO: unieke titels en omschrijvingen, canonicals, Open Graph, `sitemap.xml`,
  `robots.txt`, gestructureerde data (ArtSchool, Course, BreadcrumbList).
- Toegankelijkheid: één `h1` per pagina, alt-teksten, skip-link, zichtbare
  focusstijlen, toetsenbordbediening voor menu en lightbox, `prefers-reduced-motion`.
- Lichtbox voor de expositiefoto's; oude URL's blijven werken via doorverwijzingen.
