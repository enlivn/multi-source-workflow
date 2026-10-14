"""Apply the template's independent category lists and dashboard composition."""

import json
import shutil
from copy import deepcopy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
release = root / "ecoscope-workflows-multi-source-workflow-workflow"
package = release / "ecoscope_workflows_multi_source_workflow_workflow"
(release / "VERSION.yaml").write_text("{MAJ: 0, MIN: 3, PATCH: 0}\n")
categories = json.loads((root / "dev/grouper_categories.json").read_text())
rjsf_path = package / "rjsf.json"
rjsf = json.loads(rjsf_path.read_text())
for side, choices in categories.items():
    definition = deepcopy(rjsf["$defs"]["ValueGrouper"])
    definition["properties"]["index_name"]["oneOf"] = choices
    definition["properties"]["index_name"].pop("enum", None)
    name = side.title() + "ValueGrouper"
    rjsf["$defs"][name] = definition
    section = rjsf["properties"][
        ("event" if side == "events" else "patrol") + "_groupers"
    ]
    section = json.loads(
        json.dumps(section).replace("#/$defs/ValueGrouper", "#/$defs/" + name)
    )
    rjsf["properties"][("event" if side == "events" else "patrol") + "_groupers"] = (
        section
    )
rjsf_path.write_text(json.dumps(rjsf, indent=2) + "\n")
shutil.copyfile(root / "dev/combine_dashboards.py", package / "combine_dashboards.py")
for dag in (package / "dags").glob("run_*.py"):
    text = dag.read_text()
    if "from ..combine_dashboards import combine_dashboards" not in text:
        text = "from ..combine_dashboards import combine_dashboards\n" + text
    text = text.replace(
        "    return patrols_dashboard\n",
        "    return combine_dashboards(events_dashboard, patrols_dashboard)\n",
    )
    assert "return combine_dashboards(events_dashboard, patrols_dashboard)" in text
    dag.write_text(text)
expected = [
    "workflow_details",
    "event_source",
    "event_time_range",
    "event_types",
    "event_groupers",
    "patrol_source",
    "patrol_time_range",
    "patrol_types",
    "patrol_groupers",
]
assert list(rjsf["properties"]) == expected, list(rjsf["properties"])
print(
    "Verified metadata plus eight sections, independent category lists, and dashboard composition."
)
