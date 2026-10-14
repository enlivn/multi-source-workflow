import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location(
    "compose", Path(__file__).parents[1] / "combine_dashboards.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def dashboard(side, values):
    return Mock(
        model_dump=Mock(
            return_value={
                "filters": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "month": {
                                "type": "string",
                                "title": "Month",
                                "default": values[0],
                            }
                        },
                        "uiSchema": {"month": {"ui:title": "Month"}},
                    }
                },
                "views": {
                    json.dumps({"month": value}): [
                        {"id": 0, "title": side, "data": side + value}
                    ]
                    for value in values
                },
                "metadata": {
                    "title": "Independent maps",
                    "description": "",
                    "time_range": side + " dates",
                    "time_zone": "America/Vancouver",
                },
                "layout": [],
            }
        )
    )


class TestComposition(unittest.TestCase):
    def test_two_maps_keep_independent_filters_and_views(self):
        result = module.combine_dashboards(
            dashboard("Events", ["September", "October"]),
            dashboard("Patrols", ["June", "July"]),
        )
        self.assertEqual(len(result["views"]), 4)
        self.assertEqual(
            set(result["filters"]["schema"]["properties"]),
            {"Events: month", "Patrols: month"},
        )
        for key, widgets in result["views"].items():
            selection = json.loads(key)
            self.assertEqual([w["id"] for w in widgets], [0, 1])
            self.assertEqual(widgets[0]["data"], "Events" + selection["Events: month"])
            self.assertEqual(
                widgets[1]["data"], "Patrols" + selection["Patrols: month"]
            )
        self.assertIn("Events: Events dates", result["metadata"]["time_range"])
        self.assertIn("Patrols: Patrols dates", result["metadata"]["time_range"])

    def test_default_all_grouping_still_has_two_maps(self):
        result = module.combine_dashboards(
            dashboard("Events", ["True"]), dashboard("Patrols", ["True"])
        )
        self.assertEqual(len(result["views"]), 1)
        self.assertEqual(len(next(iter(result["views"].values()))), 2)


if __name__ == "__main__":
    unittest.main()
