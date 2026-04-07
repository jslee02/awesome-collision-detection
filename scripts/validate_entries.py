#!/usr/bin/env python3
"""Validate all data/*.yaml files against schema/entry.schema.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, cast

import jsonschema
import yaml

Entry = dict[str, Any]


def load_schema(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return cast(dict[str, Any], json.load(f))


def load_yaml(path: Path) -> list[Entry]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if data is None:
            return []
        if not isinstance(data, list):
            raise ValueError(f"{path.name} must contain a top-level YAML list")
        return cast(list[Entry], data)


def validate() -> bool:
    root = Path(__file__).resolve().parent.parent
    schema = load_schema(root / "schema" / "entry.schema.json")
    data_dir = root / "data"
    yaml_files = sorted(data_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"WARNING: No YAML files in {data_dir}")
        return True

    all_valid = True
    total = 0
    errors = 0
    for yaml_path in yaml_files:
        try:
            entries = load_yaml(yaml_path)
        except Exception as e:
            print(f"ERROR: Failed to load {yaml_path.name}: {e}", file=sys.stderr)
            all_valid = False
            continue

        for index, entry in enumerate(entries):
            total += 1
            if not isinstance(entry, dict):
                print(f"ERROR: {yaml_path.name}[{index}]: not a dict", file=sys.stderr)
                errors += 1
                all_valid = False
                continue

            raw_name = entry.get("name")
            name = raw_name if isinstance(raw_name, str) else f"[entry {index}]"
            try:
                jsonschema.validate(
                    instance=entry,
                    schema=schema,
                    format_checker=jsonschema.FormatChecker(),
                )
            except jsonschema.ValidationError as e:
                print(f"ERROR: {yaml_path.name}[{name}]: {e.message}", file=sys.stderr)
                errors += 1
                all_valid = False
            except jsonschema.SchemaError as e:
                print(f"ERROR: Schema error in {yaml_path.name}: {e.message}", file=sys.stderr)
                errors += 1
                all_valid = False

    if all_valid:
        print(f"✓ All {total} entries validated successfully")
    else:
        print(
            f"✗ Validation failed: {errors} error(s) in {total} entries",
            file=sys.stderr,
        )
    return all_valid


if __name__ == "__main__":
    raise SystemExit(0 if validate() else 1)
