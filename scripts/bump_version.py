#!/usr/bin/env python3
"""
bump_version.py

Increments the patch version (0.0.1) in Mods/TweaksAndStuff/modinfo.json.
Prints the new version to stdout.

Usage: python scripts/bump_version.py <path-to-modinfo.json>
If no path is provided, it defaults to Mods/TweaksAndStuff/modinfo.json
"""
import json
import sys
from pathlib import Path


def bump_version(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if "version" not in data:
        raise KeyError("'version' key not found in JSON file")

    old = data["version"]
    parts = old.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"Version '{old}' is not in semver x.y.z numeric format")

    major, minor, patch = map(int, parts)
    patch += 1
    new = f"{major}.{minor}.{patch}"
    data["version"] = new

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return new


def main(argv):
    p = Path(argv[1]) if len(argv) > 1 else Path("Mods/TweaksAndStuff/modinfo.json")
    try:
        new_version = bump_version(p)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print(new_version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
