#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controle van de gebouwde site: links, afbeeldingen, koppen, meta.

    python3 _build/check.py

Geeft per probleem één regel en een exitcode 1 als er iets mis is.
"""
from __future__ import annotations

import glob
import html.parser
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "_build", "assets"}
problems: list[str] = []
titles: dict[str, list[str]] = {}


class Page(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.lang = None
        self.ids: list[str] = []
        self.links: list[str] = []
        self.images: list[dict] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang")
        if d.get("id"):
            self.ids.append(d["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag == "img":
            self.images.append(d)


def main() -> int:
    pages = sorted(p for p in ROOT.glob("*.html"))
    for path in pages:
        name = path.name
        src = path.read_text(encoding="utf-8")
        p = Page()
        p.feed(src)

        title = re.search(r"<title>(.*?)</title>", src, re.S)
        if not title:
            problems.append(f"{name}: geen <title>")
        else:
            titles.setdefault(title.group(1), []).append(name)

        desc = re.search(r'<meta name="description" content="([^"]*)"', src)
        if name != "404.html":
            if not desc:
                problems.append(f"{name}: geen meta description")
            elif len(desc.group(1)) > 160:
                problems.append(f"{name}: description {len(desc.group(1))} tekens")

        if p.lang != "nl":
            problems.append(f"{name}: lang={p.lang!r}")
        if p.h1 != 1:
            problems.append(f"{name}: {p.h1} × h1")

        dupes = {i for i in p.ids if p.ids.count(i) > 1}
        if dupes:
            problems.append(f"{name}: dubbele id {sorted(dupes)}")

        for href in p.links:
            if href.startswith(("http", "mailto:", "tel:", "#", "/")):
                continue
            target = (path.parent / href.split("#")[0]).resolve()
            if not target.exists():
                problems.append(f"{name}: dode link {href}")

        for img in p.images:
            src_ = img.get("src")
            if src_ and not (path.parent / src_).exists():
                problems.append(f"{name}: ontbrekende afbeelding {src_}")
            if src_ and img.get("alt") is None:
                problems.append(f"{name}: afbeelding zonder alt ({src_})")
            if src_ and (not img.get("width") or not img.get("height")):
                problems.append(f"{name}: afbeelding zonder width/height ({src_})")
            for part in (img.get("srcset") or "").split(","):
                candidate = part.strip().split(" ")[0]
                if candidate and not (path.parent / candidate).exists():
                    problems.append(f"{name}: srcset mist {candidate}")

    for t, files in titles.items():
        if len(files) > 1:
            problems.append(f"dubbele titel {t!r}: {', '.join(files)}")

    print("\n".join(problems) if problems else f"OK — {len(pages)} pagina's gecontroleerd")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
