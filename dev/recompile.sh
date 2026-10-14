#!/bin/bash
set -euo pipefail

pixi run --manifest-path pixi.toml --locked dot -c
pixi run --manifest-path pixi.toml --locked wt-compiler compile \
    --spec spec.yaml --clobber \
    --pkg-name-prefix ecoscope-workflows \
    --results-env-var ECOSCOPE_WORKFLOWS_RESULTS "$@"
pixi run --manifest-path pixi.toml --locked python dev/finalize.py
