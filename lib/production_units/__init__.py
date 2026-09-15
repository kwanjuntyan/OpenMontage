"""Opt-in Production Unit helpers.

The package is intentionally inert unless a caller explicitly selects a
Production Unit mode. Importing it must not alter the legacy pipeline.
"""

from .scene_plan_merge import (
    ProductionUnitError,
    build_scene_plan_units,
    merge_scene_plan_units,
    run_scene_plan_compare,
)
from .script_merge import build_script_units, merge_script_units, run_script_units
from .clp_merge import build_clp_candidate_units, merge_clp_candidates, run_clp_units
from .assets import (
    AssetBatchIntegrationError,
    bind_batch_result,
    build_asset_units,
    compile_asset_batch_request,
    run_asset_units,
)

__all__ = [
    "ProductionUnitError",
    "build_scene_plan_units",
    "merge_scene_plan_units",
    "run_scene_plan_compare",
    "build_script_units",
    "merge_script_units",
    "run_script_units",
    "build_clp_candidate_units",
    "merge_clp_candidates",
    "run_clp_units",
    "AssetBatchIntegrationError",
    "bind_batch_result",
    "build_asset_units",
    "compile_asset_batch_request",
    "run_asset_units",
]
