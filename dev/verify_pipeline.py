import json
import os
import sys
from pathlib import Path

root = (
    Path(__file__).resolve().parents[1]
    / "ecoscope-workflows-multi-source-workflow-workflow"
)
sys.path.insert(0, str(root))
os.environ["ECOSCOPE_WORKFLOWS_RESULTS"] = "/tmp/multi-source-v0.3.0-smoke-results"
Path(os.environ["ECOSCOPE_WORKFLOWS_RESULTS"]).mkdir(exist_ok=True)
from ecoscope_workflows_multi_source_workflow_workflow.dispatch import dispatch
from jsonschema import Draft202012Validator, FormatChecker

zone = {
    "label": "America/Vancouver",
    "tzCode": "America/Vancouver",
    "name": "America/Vancouver",
    "utc": "-07:00",
}
params = {
    "workflow_details": {
        "name": "Multi-source smoke test",
        "description": "Separate maps and grouping",
    },
    "event_source": {"data_source": {"name": "mock_events"}},
    "event_time_range": {
        "since": "2026-08-31T17:00:00-07:00",
        "until": "2026-10-13T16:59:00-07:00",
        "timezone": zone,
    },
    "event_types": {"event_types": ["fire", "integrated"]},
    "event_groupers": {"groupers": [{"index_name": "event_type"}]},
    "patrol_source": {"data_source": {"name": "mock_patrols"}},
    "patrol_time_range": {
        "since": "2024-05-31T17:00:00-07:00",
        "until": "2024-06-30T16:59:00-07:00",
        "timezone": zone,
    },
    "patrol_types": {"patrol_types": ["ltm", "distance", "census"]},
    "patrol_groupers": {"groupers": [{"index_name": "patrol_type"}]},
}
schema = json.loads(
    (root / "ecoscope_workflows_multi_source_workflow_workflow/params.json").read_text()
)
Draft202012Validator(schema, format_checker=FormatChecker()).validate(params)
print(
    "PASS: full submitted parameters accept multiple types and independent sections.",
    flush=True,
)
result = dispatch("sequential", True, params)
if result.error:
    print(result.error)
    print(result.trace)
    raise SystemExit(1)
output = result.model_dump(mode="json")["result"]
assert output["filters"]["schema"]["properties"]
assert output["views"]
assert all(len(widgets) == 2 for widgets in output["views"].values())
Path("/tmp/multi-source-v0.3.0-smoke-results/result.json").write_text(
    json.dumps(output)
)
print(
    "PASS: complete pipeline with mock external IO produced two maps and grouped views."
)
params["event_groupers"]["groupers"] = []
params["patrol_groupers"]["groupers"] = []
result = dispatch("sequential", True, params)
assert not result.error, (result.error, result.trace)
output = result.model_dump(mode="json")["result"]
assert output["filters"]["schema"]["properties"]
assert len(output["views"]) == 1
assert len(next(iter(output["views"].values()))) == 2
print(
    "PASS: leaving both grouping sections empty still produces the standard All filters and two maps."
)
