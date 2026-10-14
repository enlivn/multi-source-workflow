"""Compose the two standard dashboards without sharing their grouping selections."""

import json
from copy import deepcopy
from itertools import product


def combine_dashboards(events, patrols):
    dashboards = [
        ("Events", events.model_dump(mode="json")),
        ("Patrols", patrols.model_dump(mode="json")),
    ]
    filters = {"schema": {"type": "object", "properties": {}, "uiSchema": {}}}
    side_views = []
    for side, dashboard in dashboards:
        schema = (dashboard.get("filters") or {}).get("schema", {})
        for key, field in schema.get("properties", {}).items():
            name = f"{side}: {key}"
            field = deepcopy(field)
            field["title"] = f"{side} — {field.get('title', key)}"
            filters["schema"]["properties"][name] = field
            ui = deepcopy(schema.get("uiSchema", {}).get(key, {}))
            ui["ui:title"] = field["title"]
            filters["schema"]["uiSchema"][name] = ui
        side_views.append(
            [
                (
                    {
                        f"{side}: {key}": value
                        for key, value in json.loads(view).items()
                    },
                    widgets,
                )
                for view, widgets in dashboard["views"].items()
            ]
        )
    if len(side_views[0]) * len(side_views[1]) > 10000:
        raise ValueError(
            "Too many event/patrol group combinations. Choose fewer grouping fields or shorter time ranges."
        )
    views = {}
    # Each combination selects one existing event view and one existing patrol view.
    # Prefixes keep identical groupers (e.g. Month) independent between the maps.
    for event_view, patrol_view in product(*side_views):
        selections = event_view[0] | patrol_view[0]
        widgets = deepcopy(event_view[1] + patrol_view[1])
        for index, widget in enumerate(widgets):
            widget["id"] = index
        views[json.dumps(selections, sort_keys=True)] = widgets
    metadata = deepcopy(dashboards[0][1]["metadata"])
    metadata["time_range"] = " | ".join(
        f"{side}: {dashboard['metadata']['time_range']}"
        for side, dashboard in dashboards
    )
    metadata["time_zone"] = " | ".join(
        f"{side}: {dashboard['metadata']['time_zone']}"
        for side, dashboard in dashboards
    )
    return {
        "filters": filters if filters["schema"]["properties"] else None,
        "views": views,
        "metadata": metadata,
        "layout": [],
    }
