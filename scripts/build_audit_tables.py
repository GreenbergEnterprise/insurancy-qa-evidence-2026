#!/usr/bin/env python3
"""Build compact CSV evidence tables from an Insurancy production audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path


OUTPUT = Path(__file__).resolve().parents[1]
DATA = OUTPUT / "data"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    first_pass = json.loads((DATA / "production-crawl.json").read_text())
    complete_path = DATA / "production-audit.json"
    if not complete_path.exists():
        complete_path = DATA / "production-crawl-final.json"
    if not complete_path.exists():
        complete_path = DATA / "production-crawl-complete.json"
    internal = json.loads(
        (complete_path if complete_path.exists() else DATA / "production-crawl-full.json").read_text()
    )

    external_rows: list[dict[str, object]] = []
    for failure in first_pass["external_failures_or_blocks"]:
        if failure["status"] != 404:
            continue
        for source in failure["sources"]:
            external_rows.append(
                {
                    "status": 404,
                    "source_page": source["source"],
                    "anchor_text": source["text"],
                    "broken_target": failure["target"],
                }
            )
    write_csv(
        DATA / "external-404-links.csv",
        ["status", "source_page", "anchor_text", "broken_target"],
        sorted(
            external_rows,
            key=lambda row: (str(row["source_page"]), str(row["broken_target"])),
        ),
    )

    write_csv(
        DATA / "internal-broken-links.csv",
        ["status", "source", "text", "target", "error"],
        [
            {
                "status": row["status"],
                "source": row["source"],
                "text": row["text"],
                "target": row["target"],
                "error": row["error"],
            }
            for row in internal["broken_internal_links"]
        ],
    )

    smoke = json.loads((DATA / "rate-funnel-smoke.json").read_text())
    write_csv(
        DATA / "rate-funnel-smoke.csv",
        [
            "requested",
            "final_url",
            "title",
            "first_heading",
            "elapsed_ms",
            "error",
        ],
        [
            {
                "requested": row["requested"],
                "final_url": row.get("finalUrl", ""),
                "title": row.get("title", ""),
                "first_heading": (row.get("headings") or [""])[0],
                "elapsed_ms": row.get("elapsedMs", ""),
                "error": row.get("error") or "",
            }
            for row in smoke
        ],
    )

    print(
        json.dumps(
            {
                "external_404_link_instances": len(external_rows),
                "internal_broken_link_instances": len(
                    internal["broken_internal_links"]
                ),
                "rate_routes_smoke_tested": len(smoke),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
