#!/usr/bin/env python3
"""Summarize the committed Liabut cognate-coding sensitivity experiment."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/literature/e15_coding_robustness.json"
OUT = ROOT / "qa/classification_sensitivity.json"


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    methods = ("lexstat", "lexstat035", "lexstat075", "sca", "biglexstat")
    focal = "Lakalei-Idate + Central Timor (with Welaun)"
    alternative = "Lakalei-Idate + Eastern Timor"
    rows = []
    for method in methods:
        if method not in source:
            raise SystemExit(f"Missing sensitivity coding: {method}")
        support = source[method]["support"]
        if focal not in support or alternative not in support:
            raise SystemExit(f"Missing focal clade support for {method}")
        rows.append({
            "coding": method,
            "characters": source[method]["characters"],
            "lakalei_idate_plus_central_timor_bootstrap": support[focal],
            "lakalei_idate_plus_eastern_timor_bootstrap": support[alternative],
            "abvd_expert_distance_fit_mantel_r": source.get(
                "diagnostic_fit_to_ABVD_experts", {}
            ).get(method, {}).get("mantel_r"),
        })

    values = [r["lakalei_idate_plus_central_timor_bootstrap"] for r in rows]
    report = {
        "title": "Liabut sensitivity of focal Lakalei–Idaté placement to cognate coding",
        "source": "results/literature/e15_coding_robustness.json",
        "results": rows,
        "summary": {
            "focal_clade_support_min": min(values),
            "focal_clade_support_max": max(values),
            "focal_clade_support_primary_lexstat": next(
                r["lakalei_idate_plus_central_timor_bootstrap"]
                for r in rows if r["coding"] == "lexstat"
            ),
            "alternative_eastern_timor_clade_support_all_codings": all(
                r["lakalei_idate_plus_eastern_timor_bootstrap"] == 0 for r in rows
            ),
        },
        "interpretation": [
            "Support for Lakalei–Idaté with Central Timor changes substantially across cognate codings and thresholds.",
            "The primary LexStat result is 65%, below the project's 70% clade-support criterion.",
            "No tested coding supports the alternative Lakalei–Idaté plus Eastern Timor clade.",
            "This is a sensitivity summary of existing analyses, not a new tree inference or proof that either classification is correct.",
        ],
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
