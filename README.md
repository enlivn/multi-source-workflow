# Multi-Source Workflow

Two independent EarthRanger analyses using the standard Events and Patrols workflow tasks.

The configuration form contains workflow name/description followed by:

1. Events — Data Source
2. Events — Time Range
3. Events — Event Types
4. Events — Group Data
5. Patrols — Data Source
6. Patrols — Time Range
7. Patrols — Patrol Types
8. Patrols — Group Data

Both type selectors support multiple selections. Leave a type selector empty to include all types.
Each side has its own timezone, dates, source, and category/time/spatial grouping.

The results show the Events Map above the Patrols Map, both full width. The events
map and patrol trajectory map reuse the standard workflow's grouped GeoArrow map
pipeline, including spatial lookup, timezone conversion, and map tooltips.

The template ID remains `multi_source_workflow`. Update the existing template in
Desktop to use this version. Existing workflow configurations keep their old schema;
create a new workflow to use the new independent sections.

## Recompile

```sh
pixi run --locked bash dev/recompile.sh
```

The compiler generates the normal task pipelines. `dev/finalize.py` preserves the
separate event/patrol category lists and installs the small dashboard composition
helper. This helper combines the two standard dashboards' views, prefixing their
filter names so, for example, choosing a month for Events does not change Patrols.
All data retrieval, processing, grouping, and map rendering use standard tasks.

Build the cloud `environment.tar` for `linux-64` with Compose's
`scripts/custom-workflows/templates.py prepare` in the retained approval container.
