# Private ontology query index

Markdown nodes and `ontology/catalog.json` remain authoritative. Neo4j Community
stores a rebuildable, revisioned projection of concept IDs, metadata, aliases,
and typed relationships. Article bodies, Korean companions, diagrams, lessons,
and private study notes are **not** moved into Neo4j. SQLite retains study notes.

## Server integration

Set `PRINCIPIA_NEO4J_URL=http://127.0.0.1:17474` on the private Principia server.
Only loopback HTTP origins are accepted; this deployment disables Bolt and binds
HTTP to 127.0.0.1. Do not expose the unauthenticated database through Tailscale
Serve or a public proxy. Only the private app exposes these read endpoints:

- `GET /api/ontology`: validate the source, refresh a stale projection, return its digest/counts.
- `GET /api/ontology/prerequisites/<id>`: same freshness check, then traverse only
  `REQUIRES`; includes the target. This is an ancestry set, not a personalized
  ordered roadmap. The browser orders learning and prunes learned ancestry.

Source changes are picked up on the next query. An index outage returns 503 on
these endpoints without disabling the graph, browser roadmaps, or SQLite notes.
`/api/health` reports configuration, not database liveness; use `/api/ontology`
for a live index check. GitHub Pages uses the identical validated projection
exported at build time, and never connects to the private database.

```sh
uv run python -m principia_app.neo4j sync
uv run python -m principia_app.neo4j status
uv run python -m principia_app.neo4j prerequisites flash-attention
```

Snapshots use content-derived keys; repeated sync is idempotent and the current
pointer changes in the same transaction as the data. Old snapshots are retained,
so raw counts across all snapshots exceed the current concept count. Filter by
the `PrincipiaProjection {id:'current'}` digest when querying directly. No automatic
snapshot deletion is configured.

## Local service

The verified installation uses Neo4j Community 5.26.30 and Temurin Java
21.0.12.1, each verified against its publisher SHA-256. Installation resides at
`~/.local/share/principia-neo4j/`; launchd label is
`com.sunguklim.principia-neo4j`. It runs at login, restarts on failure, uses a
512 MB maximum heap and 128 MB page cache, and disables usage reporting.
Logs reside at `~/.local/state/principia/neo4j{,-error}.log`.

To stop or restart this per-user service:

```sh
launchctl bootout gui/$(id -u)/com.sunguklim.principia-neo4j
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.sunguklim.principia-neo4j.plist
```

The main app service is separate. Disabling its `PRINCIPIA_NEO4J_URL` setting
restores graph-only mode without deleting source files or study history.

Compatibility: [Neo4j system requirements](https://neo4j.com/docs/operations-manual/current/installation/requirements/).
