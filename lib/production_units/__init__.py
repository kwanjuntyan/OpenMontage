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

__all__ = [
    "ProductionUnitError",
    "build_scene_plan_units",
    "merge_scene_plan_units",
    "run_scene_plan_compare",
]
