#!/usr/bin/env python3
"""Dependency-free integrity checks for Liabut's committed D1 corpus and estimates.

Run from any working directory: python qa/check_release.py
This checks release consistency, not whether the linguistic interpretations
or model assumptions are correct.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def unique(records: list[dict[str, str]], field: str, label: str) -> None:
    values = [r.get(field, "") for r in records]
    if any(not value for value in values):
        raise AssertionError(f"{label}: blank {field}")
    if len(values) != len(set(values)):
        raise AssertionError(f"{label}: duplicate {field}")


def main() -> int:
    lects = rows("data/d1/lects.csv")
    concepts = rows("data/d1/concepts.csv")
    forms = rows("data/d1/forms.csv")
    estimates = rows("results/principal_estimates.csv")

    unique(lects, "ID", "D1 lects")
    unique(concepts, "ID", "D1 concepts")
    unique(forms, "ID", "D1 forms")

    assert len(lects) == 70, f"expected 70 D1 lects, got {len(lects)}"
    assert len(concepts) == 152, f"expected 152 D1 concepts, got {len(concepts)}"
    assert len(forms) == 10555, f"expected 10,555 D1 forms, got {len(forms)}"
    assert estimates, "principal_estimates.csv is empty"

    lect_ids = {r["ID"] for r in lects}
    concept_ids = {r["ID"] for r in concepts}
    for form in forms:
        assert form["Lect_ID"] in lect_ids, (
            f"form {form['ID']} has unknown lect {form['Lect_ID']}"
        )
        assert form["Concept_ID"] in concept_ids, (
            f"form {form['ID']} has unknown concept {form['Concept_ID']}"
        )
        assert form["Value"], f"form {form['ID']} has no source value"
        assert form["Source"], f"form {form['ID']} has no source citation"

    missing = []
    for estimate in estimates:
        source = estimate.get("File", "")
        if source and not (ROOT / source).is_file():
            missing.append(source)
    if missing:
        raise AssertionError("principal estimates cite missing files: " + ", ".join(sorted(set(missing))))

    print("Liabut release QA: PASS")
    print(f"  {len(lects)} lects; {len(concepts)} concepts; {len(forms)} source forms")
    print(f"  {len(estimates)} principal estimates; all cited source files exist")
    print("  unique IDs and D1 lect/concept references verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print(f"Liabut release QA: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
