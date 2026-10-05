# Europa Linguarum Viva

A living atlas of Europe's languages and regional voices. Interactive relief maps built from official geodata, with source-checked language content linked to CEFR levels.

**Pilot:** Austria and the federal state of Salzburg. Interface in English and German.

## What is here

| Path | Content |
|---|---|
| `index.html` | The published site (one self-contained page). |
| `src/template.html` | Page layout, styles and interaction. |
| `src/content_src.py` → `src/content/*.json`, `src/content.js` | Salzburg content cards and the source list. Every statement carries a source and a locator. |
| `src/places_sbg.json` | Recording places of the Sprachatlas Salzburg and the DiÖ places cited by Bülow (2019), with coordinate sources. |
| `src/build.mjs` → `src/geo.json` | Map geometry: Europe, Austria, the nine federal states and their districts. |
| `src/sart.py`, `src/art.py`, `src/art_at.py` → `src/art_*.webp` | Relief artwork rendered from elevation data. |
| `src/assemble.py`, `src/build_site.py` | Put everything into one page and write `index.html`. |
| `src/legal.py` → `impressum.html`, `datenschutz.html` | Legal notice and privacy page (German and English). |
| `src/fonts/`, `fonts/` | EB Garamond and IBM Plex Mono, self-hosted (no request to Google). |
| `src/tests/` | Browser tests for desktop and phone (Playwright). |

## Content rules

- Every statement is tied to a published source with an exact locator.
- Dialect forms appear only as spelled in the source; nothing is reconstructed.
- Where sources disagree, both views are shown.
- Recordings of other projects are linked, never copied.
- All cards are checked against their sources; expert review is pending and each card says so.

## Data and credits

- Elevation: DGM Österreich 10 m, CC BY 4.0 (data.gv.at).
- Boundaries of states, districts and municipalities: Statistik Austria (2021), via GeoJSON-TopoJSON-Austria by Flooh Perlot, CC BY 4.0.
- Countries: Natural Earth via world-atlas (public domain).
- Rivers, lakes and towns: Natural Earth (public domain).
- Fonts: EB Garamond and IBM Plex Mono, SIL Open Font License, via Fontsource.
- Village coordinates: GeoNames via all-the-cities (CC BY 4.0) and Wikipedia.
- Language sources: listed in `src/content/sources.json` and on the site's "Method & sources" page.

The raw elevation models and boundary files are not stored here because of their size. `src/build.mjs` and `src/sart.py` name the files they expect.

## Status

Work in progress. Content is researched and drafted with AI assistance (Claude, Anthropic) and checked against the cited sources; it has not yet been reviewed by dialectologists. Corrections are welcome.
