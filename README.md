# Multi-Source Workflow

A test workflow with two independent EarthRanger source/type selections and two
maps, derived from wildlife-dynamics/dsc-analysis using standard Ecoscope tasks.

1. Import this repository folder into Ecoscope Desktop.
2. Choose a time range containing data.
3. Under **Patrols**, choose an EarthRanger data source and any patrol types to include. Leave empty for all types.
4. Under **Events**, choose an EarthRanger data source and any event types to include. Leave empty for all types.
   The two sources may be different, or the same.
5. Run the workflow to see **Patrols Map** and **Events Map**.

The patrol map shows tracks from completed patrols. The event map shows events
with point geometry. An empty lookup is distinct from a successful lookup with
no matching data in the selected time range; an empty dataset produces an empty
map widget. Patrols must contain enough valid GPS observations to form tracks.

Changing the patrol source should refresh and clear only its patrol type.
Changing the event source should refresh and clear only its event type. The other
section and the time range should retain their values.

The workflow ID is `multi_source_workflow`.

## Recompile

```sh
pixi run --locked bash dev/recompile.sh
```

The generated package remains in `ecoscope-workflows-multi-source-workflow-workflow/`.
No Google Earth Engine connection, transect IDs, or custom task extensions are
needed by this version.
