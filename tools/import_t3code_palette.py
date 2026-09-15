#!/usr/bin/env python3
"""Import the Iris palette from t3code's TypeScript source.

The imported JSON is intentionally kept in the repository so generated
IntelliJ theme assets can be audited against the upstream palette.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

UPSTREAM_URL = (
    "https://github.com/pingdotgg/t3code/blob/main/"
    "packages/shared/src/themePalettes.ts"
)


def extract_object(text: str, marker: str, end_marker: str) -> dict[str, str]:
    start = text.index(marker) + len(marker)
    end = text.index(end_marker, start)
    block = text[start:end]
    values = dict(re.findall(r'^\s+(\w+):\s*"(oklch\([^"\n]+\))",?$', block, re.MULTILINE))
    if len(values) != 57:
        raise SystemExit(f"Expected 57 palette roles in {marker!r}; found {len(values)}")
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="themePalettes.ts from t3code")
    parser.add_argument("output", type=Path, help="destination JSON file")
    parser.add_argument("--commit", default="main", help="upstream commit or ref")
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    iris_start = text.index("export const IRIS_THEME")
    iris = text[iris_start:]
    light = extract_object(iris, "colors: {", "  },\n  variants:")
    dark = extract_object(iris, "dark: {", "    },\n  },\n  sidebarArtwork")

    pinned_source_url = UPSTREAM_URL.replace("/blob/main/", f"/blob/{args.commit}/")
    payload = {
        "id": "iris",
        "label": "Iris",
        "source": {
            "repository": "https://github.com/pingdotgg/t3code",
            "file": pinned_source_url,
            "commit": args.commit,
            "license": "MIT",
        },
        "light": light,
        "dark": dark,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(light)} light and {len(dark)} dark Iris roles")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
