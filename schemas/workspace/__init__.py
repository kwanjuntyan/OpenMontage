"""Versioned Director Workspace contract loading and validation.

This package contains wire schemas only.  It does not read projects, resolve
authority, register HTTP routes, or mutate production state.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_DIR = Path(__file__).parent
WORKSPACE_V1_SCHEMA = SCHEMA_DIR / "workspace_projection_v1.schema.json"


def load_workspace_v1_schema() -> dict[str, Any]:
    """Return an isolated copy of the Workspace v1 schema bundle."""

    return json.loads(WORKSPACE_V1_SCHEMA.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _workspace_v1_validator_cached(
    definition: str = "workspace_projection",
) -> Draft202012Validator:
    """Compile one immutable v1 validator once per process/definition.

    The bundle intentionally uses only local references so fixtures and future
    consumers do not need network access or a second schema registry.
    """

    schema = load_workspace_v1_schema()
    definitions = schema.get("$defs", {})
    if definition not in definitions:
        raise KeyError(f"unknown Workspace v1 definition: {definition}")
    schema["$ref"] = f"#/$defs/{definition}"
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def workspace_v1_validator(
    definition: str = "workspace_projection",
) -> Draft202012Validator:
    """Return the cached compiled validator for a public v1 definition.

    Validation remains exactly the same; caching avoids reparsing and
    rechecking the immutable tracked schema for every projection request.
    """
    return _workspace_v1_validator_cached(definition)


def validate_workspace_v1(value: Any, definition: str = "workspace_projection") -> None:
    """Validate one JSON-shaped Workspace v1 value or raise ValidationError."""

    workspace_v1_validator(definition).validate(deepcopy(value))


__all__ = [
    "WORKSPACE_V1_SCHEMA",
    "load_workspace_v1_schema",
    "validate_workspace_v1",
    "workspace_v1_validator",
]
