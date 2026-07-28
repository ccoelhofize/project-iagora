# SPDX-License-Identifier: EUPL-1.2

"""Deterministic validation for the JSON Schema subset used by the POC."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


class ContractViolation(ValueError):
    """Raised when an instance does not satisfy its executable contract."""


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ContractViolation(f"Unsupported schema type: {expected}")


def _validate_format(value: str, format_name: str, path: str) -> None:
    try:
        if format_name == "date":
            date.fromisoformat(value)
        elif format_name == "date-time":
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        elif format_name == "uri":
            parsed = urlparse(value)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("absolute URI required")
        else:
            raise ContractViolation(f"Unsupported schema format: {format_name}")
    except ValueError as exc:
        raise ContractViolation(f"{path}: invalid {format_name}: {value!r}") from exc


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    """Validate an instance against the explicit schema keywords used here."""

    if "const" in schema and instance != schema["const"]:
        raise ContractViolation(f"{path}: expected constant {schema['const']!r}")

    if "enum" in schema and instance not in schema["enum"]:
        raise ContractViolation(f"{path}: {instance!r} is not in {schema['enum']!r}")

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not any(_matches_type(instance, expected) for expected in expected_types):
            raise ContractViolation(f"{path}: expected type {expected_types}, got {type(instance).__name__}")

    if instance is None:
        return

    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in instance]
        if missing:
            raise ContractViolation(f"{path}: missing required fields {missing}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unexpected = sorted(set(instance) - set(properties))
            if unexpected:
                raise ContractViolation(f"{path}: unexpected fields {unexpected}")
        for key, child_schema in properties.items():
            if key in instance:
                validate(instance[key], child_schema, f"{path}.{key}")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ContractViolation(f"{path}: requires at least {schema['minItems']} items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in instance]
            if len(serialized) != len(set(serialized)):
                raise ContractViolation(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(instance):
                validate(item, item_schema, f"{path}[{index}]")

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise ContractViolation(f"{path}: value is shorter than {schema['minLength']}")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, instance) is None:
            raise ContractViolation(f"{path}: value does not match {pattern!r}")
        format_name = schema.get("format")
        if format_name:
            _validate_format(instance, format_name, path)

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise ContractViolation(f"{path}: value is below {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            raise ContractViolation(f"{path}: value is above {schema['maximum']}")


def validate_files(instance_path: Path, schema_path: Path) -> Any:
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    validate(instance, schema)
    return instance
