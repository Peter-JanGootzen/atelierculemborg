# atelierculemborg.nl

Statische website van Atelier Culemborg, bedoeld voor hosting via GitHub Pages.

## Structuur

- `index.html` — verwijst door naar de homepagina
- `Atelier_Culemborg/` — de volledige site (iWeb-export: HTML, CSS, JS, afbeeldingen)

Er is geen server-side code: geen WordPress, geen PHP, geen database.

## Lokaal bekijken

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## Publiceren

Zet in de GitHub-repository *Settings → Pages* de bron op branch `main`, map `/ (root)`.
Voor het eigen domein `atelierculemborg.nl` hoort daarbij een `CNAME`-bestand in de root
(of hetzelfde invullen bij *Custom domain*), plus DNS-records naar GitHub Pages.
