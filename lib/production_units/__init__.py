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
from .edit_merge import build_edit_units, merge_edit_units, run_edit_units
from .render import (
    build_assembly_command,
    build_unit_render_commands,
    make_assembly_receipt,
    make_unit_render_receipt,
    run_render_units,
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
    "build_edit_units",
    "merge_edit_units",
    "run_edit_units",
    "build_unit_render_commands",
    "make_unit_render_receipt",
    "build_assembly_command",
    "make_assembly_receipt",
    "run_render_units",
]
