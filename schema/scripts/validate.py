#!/usr/bin/env python3
"""Check the store's JSON files against their schemas.

    python3 schema/scripts/validate.py            # the examples in schema/examples
    python3 schema/scripts/validate.py FILE...    # named files; the schema is picked by file name

Needs the `jsonschema` package. Exit status 1 when any file fails.
"""
import json
import os
import sys

from jsonschema import Draft202012Validator, FormatChecker

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.dirname(HERE)


def schema_for(path):
    name = os.path.basename(path)
    if name.endswith(".manifest.json") or name == "manifest.json":
        return "manifest.schema.json"
    if name == "index.json":
        return "index.schema.json"
    if name == "app.json" or name.endswith(".app.json"):
        return "app.schema.json"
    raise SystemExit(f"no schema for {path}")


def main(paths):
    if not paths:
        ex = os.path.join(SCHEMA_DIR, "examples")
        paths = [os.path.join(ex, f) for f in sorted(os.listdir(ex)) if f.endswith(".json")]
    failed = 0
    for path in paths:
        with open(os.path.join(SCHEMA_DIR, schema_for(path)), encoding="utf-8") as f:
            validator = Draft202012Validator(json.load(f), format_checker=FormatChecker())
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for e in errors[:5]:
                where = "/".join(str(p) for p in e.path) or "(root)"
                print(f"  {where}: {e.message[:160]}")
        else:
            print(f"ok   {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
