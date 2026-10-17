#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genereert de statische site van Atelier Culemborg.

    python3 _build/build.py

Schrijft HTML, sitemap.xml en robots.txt in de root van de repository.
De oude iWeb-URL's (Atelier_Culemborg/*.html) blijven bestaan als
doorverwijspagina's, zodat bestaande links en zoekresultaten blijven werken.
"""
from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path

from content import (ABOUT, CONTACT, COURSES, EXPOS, HOME, NAV, SITE,
                     SITE_BASE, SITE_URL)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "assets" / "img" / "manifest.json").read_text())


# --------------------------------------------------------------------------
# hulpjes
# --------------------------------------------------------------------------

def e(text: str) -> str:
    """HTML-escape, maar laat typografische tekens met rust."""
    return html.escape(text, quote=False)


def attr(text: str) -> str:
    return html.escape(text, quote=True)


def image(slug: str, sizes: str | None = None, cls: str = "", eager: bool = False,
          widths: str | None = None) -> str:
    item = MANIFEST[slug]
    alt = attr(item["alt"])
    loading = "eager" if eager else "lazy"
    common = f'class="{cls}" ' if cls else ""
    if "only" in item["variants"]:
        name = item["variants"]["only"]
        w, h = item["only_w"], item["only_h"]
        return (f'<img src="assets/img/{name}" width="{w}" height="{h}" alt="{alt}" '
                f'{common}loading="{loading}" decoding="async">')
    sm, lg = item["variants"]["sm"], item["variants"]["lg"]
    src = sm
    srcset = (f'assets/img/{sm} {item["sm_w"]}w, assets/img/{lg} {item["lg_w"]}w')
    sizes = sizes or "(max-width: 760px) 100vw, 50vw"
    return (f'<img src="assets/img/{src}" srcset="{srcset}" sizes="{attr(sizes)}" '
            f'width="{item["sm_w"]}" height="{item["sm_h"]}" alt="{alt}" {common}'
            f'loading="{loading}" decoding="async">')


def meta_desc(text: str, limit: int = 156) -> str:
    """Kort een omschrijving netjes af op een woordgrens."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit - 1].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def natural(slug: str) -> int:
    """Breedte waarop een afbeelding scherp blijft (plus de lijst eromheen)."""
    return MANIFEST[slug]["w"] + 26


def url(path: str) -> str:
    return f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"


def jsonld(data: dict) -> str:
    return ('<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
            + "</script>")


def head(page: dict, path: str, extra_ld: list[dict] | None = None,
         og_type: str = "website") -> str:
    title = page["title"]
    desc = meta_desc(page["description"])
    canonical = url(path)
    ld = extra_ld or []
    ld_html = "\n".join(jsonld(d) for d in ld)
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta name="author" content="Atelier Culemborg">
<meta name="theme-color" content="#131116">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url('assets/img/og-atelier-culemborg.jpg')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Atelier Culemborg — teken- en schilderlessen in Culemborg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/cormorant-garamond.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add("js");</script>
<script src="assets/js/site.js" defer></script>
{ld_html}
</head>"""


def header(current: str) -> str:
    def link(label, href):
        cur = ' aria-current="page"' if current == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'

    courses_items = "\n".join(
        f'<li><a href="{c["slug"]}.html">{e(c["nav"])}'
        f'<span class="age">{e(c["age"])}</span></a></li>' for c in COURSES)
    courses_current = "page" if current == "cursussen.html" or any(
        current == f'{c["slug"]}.html' for c in COURSES) else ""

    return f"""<body>
<a class="skip-link" href="#main">Direct naar de inhoud</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="index.html">
      <svg width="30" height="30" viewBox="0 0 30 30" aria-hidden="true" focusable="false">
        <circle cx="15" cy="15" r="14" fill="none" stroke="currentColor" stroke-opacity=".3"/>
        <path d="M9.5 20.5 15 8.6l5.5 11.9" fill="none" stroke="#cba8d9" stroke-width="1.2" stroke-linecap="round"/>
        <path d="M11.8 16.6h6.4" stroke="#cba8d9" stroke-width="1.2" stroke-linecap="round"/>
      </svg>
      <span>Atelier Culemborg<small>Teken- en schilderlessen</small></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu openen">
      <span></span>
    </button>
    <nav class="nav" id="site-nav" aria-label="Hoofdmenu">
      {link("Home", "index.html")}
      {link("Over mij", "over-mij.html")}
      <div class="nav__group" data-open="false">
        <button type="button" aria-expanded="false" aria-controls="submenu-cursussen"{' class="is-current"' if courses_current else ''}>
          Cursussen <i class="chev" aria-hidden="true"></i>
        </button>
        <ul class="nav__menu" id="submenu-cursussen">
          <li><a href="cursussen.html"{" aria-current=\"page\"" if current == "cursussen.html" else ""}>Alle cursussen<span class="age">Overzicht</span></a></li>
          {courses_items}
        </ul>
      </div>
      {link("Exposities", "exposities.html")}
      <a href="contact.html" class="nav__cta"{" aria-current=\"page\"" if current == "contact.html" else ""}>Contact</a>
    </nav>
  </div>
</header>
<main id="main">"""


def footer() -> str:
    courses_links = "\n".join(
        f'<li><a href="{c["slug"]}.html">{e(c["nav"])}</a></li>' for c in COURSES[:6])
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p class="footer-brand">Atelier Culemborg</p>
        <p>Teken- en schildercursussen voor kinderen, jongeren en volwassenen,
        in een eigen atelier op loopafstand van station Culemborg.</p>
      </div>
      <div>
        <h2>Cursussen</h2>
        <ul>{courses_links}</ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li>Alicja Gootzen</li>
          <li>{SITE['street']}<br>{SITE['postcode']} {SITE['city']}</li>
          <li><a href="tel:{SITE['phone_link']}">{SITE['phone']}</a></li>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span data-year>{date.today().year}</span> Atelier Culemborg</p>
      <p><a href="contact.html">Contact</a> · <a href="exposities.html">Exposities</a> · <a href="cursussen.html">Cursussen</a></p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def card(course: dict, kicker: str | None = None) -> str:
    kicker = kicker or course["age"]
    return f"""<a class="card reveal" href="{course['slug']}.html">
  <div class="card__media">{image(course["image"], sizes="(max-width: 760px) 100vw, 33vw")}</div>
  <div class="card__body">
    <span class="card__kicker">{e(kicker)}</span>
    <span class="card__title">{e(course['name'])}</span>
    <p class="card__text">{e(course['summary'])}</p>
  </div>
</a>"""


def gallery(slugs: list[str], caption: str = "", natural: bool = False,
            tall: bool = False) -> str:
    if not slugs:
        return ""
    if natural:
        cls = "gallery gallery--natural"
    elif tall:
        cls = "gallery gallery--tall"
    elif len(slugs) == 1:
        cls = "gallery gallery--single"
    elif len(slugs) == 2:
        cls = "gallery gallery--pair"
    else:
        cls = "gallery"
    items = "\n".join(
        f'<button class="gallery__item" type="button" '
        f'data-full="assets/img/{MANIFEST[s]["variants"].get("lg") or MANIFEST[s]["variants"]["only"]}" '
        f'data-alt="{attr(MANIFEST[s]["alt"])}" '
        f'aria-label="Vergroot: {attr(MANIFEST[s]["alt"])}">'
        f'{image(s, sizes="(max-width: 760px) 50vw, 25vw")}</button>' for s in slugs)
    cap = f'<p class="muted" style="font-size:.85rem;margin-top:.9rem">{e(caption)}</p>' if caption else ""
    return f'<div class="{cls}">\n{items}\n</div>{cap}'


def lightbox() -> str:
    return """<dialog class="lightbox" id="lightbox" aria-label="Afbeelding vergroten">
  <div class="lightbox__inner">
    <button class="lightbox__close" type="button" aria-label="Sluiten">✕</button>
    <button class="lightbox__prev" type="button" aria-label="Vorige afbeelding">‹</button>
    <img alt="">
    <button class="lightbox__next" type="button" aria-label="Volgende afbeelding">›</button>
    <p class="lightbox__caption"></p>
  </div>
</dialog>"""


def crumbs(items: list[tuple[str, str | None]]) -> str:
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<a href="{href}">{e(label)}</a>')
        else:
            parts.append(f'<span aria-current="page">{e(label)}</span>')
    return '<nav class="crumbs" aria-label="Kruimelpad">' + ' <span aria-hidden="true">/</span> '.join(parts) + "</nav>"


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url(path)}
            for i, (name, path) in enumerate(items)
        ],
    }


ORG_LD = {
    "@context": "https://schema.org",
    "@type": ["ArtSchool", "LocalBusiness"],
    "@id": SITE_URL + "/#organisatie",
    "name": SITE["name"],
    "description": HOME["description"],
    "url": url(""),
    "logo": url("assets/img/logo-atelier-culemborg.webp"),
    "image": url("assets/img/og-atelier-culemborg.jpg"),
    "telephone": SITE["phone"],
    "email": SITE["email"],
    "priceRange": "In overleg",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": SITE["street"],
        "postalCode": SITE["postcode"],
        "addressLocality": SITE["city"],
        "addressRegion": "Gelderland",
        "addressCountry": "NL",
    },
    "areaServed": ["Culemborg", "Geldermalsen", "Tricht", "Tiel", "Houten", "Utrecht"],
    "founder": {"@type": "Person", "name": "Alicja Gootzen"},
}

WEBSITE_LD = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": SITE["name"],
    "url": url(""),
    "inLanguage": "nl-NL",
    "publisher": {"@id": SITE_URL + "/#organisatie"},
}


# --------------------------------------------------------------------------
# pagina's
# --------------------------------------------------------------------------

def build_home() -> str:
    cards = "\n".join(card(c) for c in COURSES[:6])
    facts = f"""
      <ul class="facts">
        <li><b>Adres</b><span>{SITE['street']}, {SITE['postcode']} {SITE['city']}</span></li>
        <li><b>Telefoon</b><span><a href="tel:{SITE['phone_link']}">{SITE['phone']}</a></span></li>
        <li><b>E-mail</b><span><a href="mailto:{SITE['email']}">{SITE['email']}</a></span></li>
      </ul>"""

    themes = "".join(f"<p>{e(p)}</p>" for p in HOME["themes"])
    travel = "".join(f"<p>{e(p)}</p>" for p in HOME["travel"])

    return head(HOME, "", [ORG_LD, WEBSITE_LD]) + header("index.html") + f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <p class="eyebrow">Atelier in Culemborg</p>
      <h1>Welkom bij<br> Atelier Culemborg</h1>
      <p class="lead">{e(HOME['intro'])}</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="cursussen.html">Bekijk de cursussen <span class="arrow" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="contact.html">Neem contact op</a>
      </div>
    </div>
    <figure class="hero__figure">
      <div class="hero__plate">{image("logo-atelier-culemborg", eager=True)}</div>
      <figcaption class="hero__caption">Teken- en schilderlessen, met aandacht voor ieder mens</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Het atelier</p>
      <h2>Thema’s en technieken</h2>
      <div class="prose">{themes}</div>
      <p style="margin-top:1.4rem"><a class="btn btn--ghost" href="over-mij.html">Meer over het atelier</a></p>
    </div>
    <figure class="figure-mat split__media" style="max-width:360px">
      {image("kunstwerk-waterlelies", sizes="(max-width: 980px) 100vw, 40vw")}
    </figure>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <p class="eyebrow">Cursussen</p>
    <h2>Kies een techniek</h2>
    <p class="lead" style="max-width:52ch;margin-bottom:2.5rem">Van tekenen en aquarel tot olieverf en modetekenen:
    voor kinderen, jongeren en volwassenen.</p>
    <div class="grid grid--3">
      {cards}
    </div>
    <p style="margin-top:2.5rem"><a class="btn btn--ghost" href="cursussen.html">Alle cursussen <span class="arrow" aria-hidden="true">→</span></a></p>
  </div>
</section>

<section class="section">
  <div class="wrap split split--reverse">
    <div>
      <p class="eyebrow">Over mij</p>
      <h2>Persoonlijke begeleiding</h2>
      <div class="prose"><p>{e(ABOUT['body'][0])}</p><p>{e(ABOUT['body'][1])}</p></div>
      <p style="margin-top:1.4rem"><a class="btn btn--ghost" href="over-mij.html">Lees verder</a></p>
    </div>
    <figure class="figure-mat split__media" style="max-width:{natural("portret-alicja-gootzen")}px">
      {image("portret-alicja-gootzen", sizes="(max-width: 980px) 60vw, 300px")}
      <figcaption>Alicja Gootzen, Atelier Culemborg</figcaption>
    </figure>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Exposities</p>
      <h2>Exposities van Atelier Culemborg</h2>
      <div class="prose"><p>Werk van cursisten was de afgelopen jaren te zien in het oude stadhuis,
      de openbare bibliotheek en de kerkzaal in Culemborg.</p></div>
      <p style="margin-top:1.6rem"><a class="btn btn--primary" href="exposities.html">Bekijk de exposities <span class="arrow" aria-hidden="true">→</span></a></p>
    </div>
    <div class="media-pair">
      <a href="exposities.html" aria-label="Expositie 2024">{image("expo-2024-1", sizes="(max-width: 980px) 50vw, 25vw")}</a>
      <a href="exposities.html" aria-label="Expositie 2018">{image("expo-2018-1", sizes="(max-width: 980px) 50vw, 25vw")}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Contact</p>
      <h2>Goed bereikbaar</h2>
      <div class="prose">{travel}</div>
      {facts}
    </div>
    <div class="contact-card">
      <h3 style="margin-bottom:1.2rem">Aanmelden of een vraag?</h3>
      <p class="muted" style="font-size:.95rem">Bel of mail gerust voor lestijden, kosten en beschikbaarheid.
      Een kennismaking in het atelier is mogelijk.</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--primary" href="tel:{SITE['phone_link']}">Bel {SITE['phone']}</a>
        <a class="btn btn--ghost" href="mailto:{SITE['email']}">Mail het atelier</a>
      </div>
    </div>
  </div>
</section>
""" + footer()


def build_courses_overview() -> str:
    page = {
        "title": "Cursussen — Atelier Culemborg",
        "description": "Alle teken- en schildercursussen van Atelier Culemborg: kinderen, jongeren, modetekenen, tekenen, aquarel, acryl, olieverf, pastelkrijt, gemengde technieken en individuele les.",
    }
    cards = "\n".join(card(c) for c in COURSES)
    ld = breadcrumb_ld([("Home", ""), ("Cursussen", "cursussen.html")])
    return head(page, "cursussen.html", [ld]) + header("cursussen.html") + f"""
<section class="page-head">
  <div class="wrap">
    {crumbs([("Home", "index.html"), ("Cursussen", None)])}
    <p class="eyebrow">Aanbod</p>
    <h1>Cursussen in het atelier</h1>
    <p class="lead" style="max-width:56ch">Van tekenen en aquarel tot olieverf en modetekenen: tien cursussen
    in Culemborg, voor kinderen, jongeren en volwassenen.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--3">
      {cards}
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Niet zeker welke cursus past?</h2>
        <p class="muted">Vertel wat u leuk lijkt, dan kijken we samen verder.</p>
      </div>
      <a class="btn btn--primary" href="contact.html">Neem contact op</a>
    </div>
  </div>
</section>
""" + footer()


def build_course(c: dict, idx: int) -> str:
    others = [COURSES[(idx + n) % len(COURSES)] for n in (1, 2, 3)]
    body = c["body"]
    lead = body[0]
    rest = "".join(f"<p>{e(p)}</p>" for p in body[1:])
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in c.get("tags", []))
    tags_html = f'<div class="tag-row">{tags}</div>' if tags else ""
    extra_lead = f'<p class="eyebrow" style="margin-top:1rem">{e(c["lead_extra"])}</p>' if c.get("lead_extra") else ""

    page = {
        "title": f"{c['name']} — cursus bij Atelier Culemborg",
        "description": meta_desc(f"{c['summary']} Cursus {c['name']} in Culemborg."),
    }
    ld = [
        breadcrumb_ld([("Home", ""), ("Cursussen", "cursussen.html"), (c["name"], f"{c['slug']}.html")]),
        {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": c["name"],
            "description": " ".join(body)[:300],
            "inLanguage": "nl-NL",
            "provider": {"@id": SITE_URL + "/#organisatie"},
            "hasCourseInstance": {
                "@type": "CourseInstance",
                "courseMode": "onsite",
                "location": {"@id": SITE_URL + "/#organisatie"},
            },
        },
    ]
    gallery_html = gallery(c.get("gallery", []), c.get("gallery_caption", ""))
    related = "\n".join(card(o) for o in others)

    return head(page, f"{c['slug']}.html", ld, og_type="article") + header(f"{c['slug']}.html") + f"""
<section class="page-head">
  <div class="wrap">
    {crumbs([("Home", "index.html"), ("Cursussen", "cursussen.html"), (c["name"], None)])}
    <p class="eyebrow">{e(c['kicker'])}</p>
    <h1>{e(c['h1'])}</h1>
    <p class="lead" style="max-width:52ch">{e(lead)}</p>
    {extra_lead}
  </div>
</section>

<div class="wrap course">
  <div class="prose">
    {rest}
    {tags_html}
  </div>
  <figure class="figure-mat course__figure" style="max-width:{natural(c["image"])}px">
    {image(c["image"], sizes="(max-width: 980px) 100vw, 40vw")}
  </figure>
</div>

{f'<section class="section section--tight"><div class="wrap">' + gallery_html + '</div></section>' if gallery_html else ''}

<section class="section section--tight">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Interesse in {e(c['name'].lower())}?</h2>
        <p class="muted">Neem contact op voor meer informatie of om u aan te melden.</p>
      </div>
      <div class="btn-row" style="margin:0">
        <a class="btn btn--primary" href="contact.html">Naar contact</a>
        <a class="btn btn--ghost" href="tel:{SITE['phone_link']}">{SITE['phone']}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Ook mogelijk</p>
    <h2>Andere cursussen</h2>
    <div class="grid grid--3" style="margin-top:2rem">
      {related}
    </div>
  </div>
</section>
""" + footer()


def build_about() -> str:
    page = ABOUT
    body = "".join(f"<p>{e(p)}</p>" for p in ABOUT["body"])
    ld = breadcrumb_ld([("Home", ""), ("Over mij", "over-mij.html")])
    return head(page, "over-mij.html", ld, og_type="profile") + header("over-mij.html") + f"""
<section class="page-head">
  <div class="wrap">
    {crumbs([("Home", "index.html"), ("Over mij", None)])}
    <p class="eyebrow">Het atelier</p>
    <h1>Over mij</h1>
  </div>
</section>

<div class="wrap course">
  <div class="prose">
    {body}
    <p style="margin-top:2rem"><a class="btn btn--ghost" href="contact.html">Kom eens langs</a></p>
  </div>
  <figure class="figure-mat course__figure" style="max-width:{natural("portret-alicja-gootzen")}px">
    {image("portret-alicja-gootzen", sizes="(max-width: 980px) 70vw, 330px")}
    <figcaption>Alicja Gootzen</figcaption>
  </figure>
</div>

<section class="section section--tint">
  <div class="wrap">
    <p class="eyebrow">Natuursteen</p>
    <h2>Beelden voor de Wereldwinkel</h2>
    <p class="lead" style="max-width:56ch">Schetsen en ontwerpen met het thema ‘kerstfeest’,
    gebeeldhouwd uit natuursteen door een Zimbabwaanse kunstenaar.</p>
    {gallery(["natuursteen-1", "natuursteen-2", "natuursteen-3", "natuursteen-4"], ABOUT["gallery_caption"], tall=True)}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Kennismaken in het atelier?</h2>
        <p class="muted">U bent welkom om eens sfeer te komen proeven.</p>
      </div>
      <a class="btn btn--primary" href="contact.html">Naar contact</a>
    </div>
  </div>
</section>
{lightbox()}
""" + footer()


def build_exposities() -> str:
    page = EXPOS
    blocks = []
    for sec in EXPOS["sections"]:
        link = ""
        if sec.get("link"):
            label, href = sec["link"]
            link = f'<p style="margin-top:1rem"><a class="btn btn--ghost" href="{attr(href)}" target="_blank" rel="noopener">{e(label)} <span class="arrow" aria-hidden="true">→</span></a></p>'
        blocks.append(f"""<section class="expo">
  <h2>{e(sec['h'])}</h2>
  {gallery(sec['images'])}
  {link}
</section>""")
    ld = breadcrumb_ld([("Home", ""), ("Exposities", "exposities.html")])
    return head(page, "exposities.html", ld) + header("exposities.html") + f"""
<section class="page-head">
  <div class="wrap">
    {crumbs([("Home", "index.html"), ("Exposities", None)])}
    <p class="eyebrow">Werken van cursisten</p>
    <h1>Exposities</h1>
    <p class="lead" style="max-width:56ch">{e(EXPOS['intro'])}</p>
  </div>
</section>

<div class="wrap">
{''.join(blocks)}
</div>

<section class="section section--tight">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Zelf aan de slag?</h2>
        <p class="muted">Bekijk het aanbod of neem contact op voor meer informatie.</p>
      </div>
      <div class="btn-row" style="margin:0">
        <a class="btn btn--primary" href="cursussen.html">Alle cursussen</a>
        <a class="btn btn--ghost" href="contact.html">Contact</a>
      </div>
    </div>
  </div>
</section>
{lightbox()}
""" + footer()


def build_contact() -> str:
    page = CONTACT
    ld = [
        breadcrumb_ld([("Home", ""), ("Contact", "contact.html")]),
        {**ORG_LD, "@context": "https://schema.org"},
    ]
    return head(page, "contact.html", ld) + header("contact.html") + f"""
<section class="page-head">
  <div class="wrap">
    {crumbs([("Home", "index.html"), ("Contact", None)])}
    <p class="eyebrow">Aanmelden of langskomen</p>
    <h1>Contact</h1>
    <p class="lead" style="max-width:50ch">Bel, mail of kom langs in het atelier.
    Een kennismaking is altijd mogelijk.</p>
  </div>
</section>

<div class="wrap contact-grid">
  <div class="contact-card">
    <dl>
      <dt>Naam</dt><dd>Alicja Gootzen</dd>
      <dt>Adres</dt><dd><address>{SITE['street']}<br>{SITE['postcode']} {SITE['city']}</address></dd>
      <dt>Telefoon</dt><dd><a href="tel:{SITE['phone_link']}">{SITE['phone']}</a></dd>
      <dt>E-mail</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd>
    </dl>
    <div class="btn-row">
      <a class="btn btn--primary" href="tel:{SITE['phone_link']}">Bellen</a>
      <a class="btn btn--ghost" href="mailto:{SITE['email']}">Mailen</a>
    </div>
    <p style="margin-top:1.5rem">
      <a class="muted" style="font-size:.85rem" href="https://www.openstreetmap.org/search?query=Achter+%27t+Zand+87+Culemborg" target="_blank" rel="noopener">Bekijk de locatie op OpenStreetMap →</a>
    </p>
  </div>
  <figure class="figure-mat" style="max-width:{natural("portret-alicja-gootzen")}px">
    {image("portret-alicja-gootzen", sizes="(max-width: 980px) 70vw, 340px")}
    <figcaption>Alicja Gootzen, Atelier Culemborg</figcaption>
  </figure>
</div>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Bereikbaarheid</h2>
        <div class="prose">
          <p>{e(HOME['travel'][0])}</p>
          <p>{e(HOME['travel'][1])}</p>
        </div>
      </div>
      <div class="contact-card">
        <h3 style="margin-bottom:.8rem">Op afspraak</h3>
        <p class="muted" style="font-size:.95rem">Lestijden en kosten van de lessen in overleg.
        Ook individuele les aan huis of alleen werken is mogelijk.</p>
        <p style="margin-top:1rem"><a href="individueel.html">Lees over individuele les →</a></p>
      </div>
    </div>
  </div>
</section>
""" + footer()


def build_404() -> str:
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pagina niet gevonden — Atelier Culemborg</title>
<meta name="robots" content="noindex,follow">
<link rel="icon" href="{SITE_BASE}favicon.svg" type="image/svg+xml">
<style>
  html{{background:#131116;color:#efeaf2;font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
  body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:2rem}}
  main{{max-width:34rem;text-align:center}}
  h1{{font:300 clamp(2rem,6vw,3rem)/1.1 Georgia,"Times New Roman",serif;margin:0 0 .8rem;color:#fff}}
  p{{color:#a79fb0;margin:0 0 1.8rem}}
  a{{display:inline-block;background:#cba8d9;color:#23182b;text-decoration:none;padding:.9rem 1.6rem;border-radius:999px;font-weight:500}}
</style>
</head>
<body>
<main>
  <h1>Deze pagina bestaat niet</h1>
  <p>Misschien is de link verouderd. Ga terug naar de startpagina van Atelier Culemborg.</p>
  <a href="{SITE_BASE}">Naar Atelier Culemborg</a>
</main>
</body>
</html>
"""


def build_redirects() -> None:
    mapping = {
        "Home": "index.html",
        "Over_mij": "over-mij.html",
        "Kinderen": "kinderen.html",
        "Jongeren": "jongeren.html",
        "Modetekenen": "modetekenen.html",
        "Tekenen": "tekenen.html",
        "Aquarel": "aquarel.html",
        "Acryl": "acryl.html",
        "Olieverf": "olieverf.html",
        "Pastelkrijt": "pastelkrijt.html",
        "Gemengde_Technieken": "gemengde-technieken.html",
        "Individueel": "individueel.html",
        "Exposities": "exposities.html",
        "Contact": "contact.html",
    }
    out = ROOT / "Atelier_Culemborg"
    out.mkdir(exist_ok=True)
    for old, new in mapping.items():
        (out / f"{old}.html").write_text(f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title>Verplaatst — Atelier Culemborg</title>
<link rel="canonical" href="../{new}">
<meta http-equiv="refresh" content="0; url=../{new}">
<meta name="robots" content="noindex,follow">
</head>
<body>
<p>Deze pagina is verplaatst naar <a href="../{new}">Atelier Culemborg</a>.</p>
</body>
</html>
""", encoding="utf-8")
    # oude map met iWeb-assets opruimen
    for item in out.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        elif item.suffix in {".css", ".js", ".jpg", ".png", ".xml"}:
            item.unlink()


def build_sitemap() -> None:
    pages = [("", "1.0"), ("cursussen.html", "0.9"), ("over-mij.html", "0.8"),
             ("exposities.html", "0.7"), ("contact.html", "0.8")]
    pages += [(f"{c['slug']}.html", "0.8") for c in COURSES]
    today = date.today().isoformat()
    body = "\n".join(
        f"""  <url>
    <loc>{url(p)}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{pr}</priority>
  </url>""" for p, pr in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")


def build_favicon() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#231a2b"/>
  <path d="M17 46 32 16l15 30" fill="none" stroke="#cba8d9" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M22.5 37h19" stroke="#cba8d9" stroke-width="3.2" stroke-linecap="round"/>
</svg>
"""
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    (ROOT / "cursussen.html").write_text(build_courses_overview(), encoding="utf-8")
    for i, c in enumerate(COURSES):
        (ROOT / f"{c['slug']}.html").write_text(build_course(c, i), encoding="utf-8")
    (ROOT / "over-mij.html").write_text(build_about(), encoding="utf-8")
    (ROOT / "exposities.html").write_text(build_exposities(), encoding="utf-8")
    (ROOT / "contact.html").write_text(build_contact(), encoding="utf-8")
    (ROOT / "404.html").write_text(build_404(), encoding="utf-8")
    build_redirects()
    build_sitemap()
    build_favicon()
    print("site gebouwd:", len(list(ROOT.glob('*.html'))), "pagina's")


if __name__ == "__main__":
    main()
