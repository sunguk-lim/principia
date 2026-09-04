# Web application architecture

Principia has one knowledge source and one frontend build.

## Source of truth

`nodes/*.md` is canonical. `brain.py` and `web/render.py` own graph parsing and projection. The web
build imports those functions and emits `web/dist/data/graph.json`; it does not parse a second graph
format or scrape the legacy HTML.

## Shared frontend

`webapp/` is a React + TypeScript application rendered with Cytoscape.js. `npm run build` produces
`web/dist`, including the graph dataset, node figures, application assets, PWA manifest, and the
legacy graph fallback.

GitHub Pages uploads `web/dist` directly. FastAPI mounts that exact directory, so both surfaces use
the same renderer and data contract.

## Private state

The frontend uses a storage adapter. On the local server, `/api/status` persists progress and notes
in SQLite. On GitHub Pages, where no private API exists, the same interface falls back to browser
local storage. Private state never enters the generated graph dataset or static deployment.
