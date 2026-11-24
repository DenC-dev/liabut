#!/usr/bin/env python3
"""Compare automatic D2 cognate clusters with expert-coded cognate judgments.

Run from any directory: python qa/benchmark_cognates.py
Uses only the Python standard library. The unit scored is a pair of forms
within the same concept. Expert rows marked Doubt=True are excluded; if an
expert assigns multiple confident cognate sets to a form, any shared set
makes the pair a positive reference pair.
"""
import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def score(method, automatic, expert, concept_by_form):
    groups = defaultdict(list)
    for form_id in expert:
        if form_id in automatic and form_id in concept_by_form:
            groups[concept_by_form[form_id]].append(form_id)

    tp = fp = fn = tn = 0
    for form_ids in groups.values():
        for left, right in combinations(form_ids, 2):
            reference = bool(expert[left] & expert[right])
            predicted = automatic[left] == automatic[right]
            if reference and predicted:
                tp += 1
            elif predicted:
                fp += 1
            elif reference:
                fn += 1
            else:
                tn += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "method": method,
        "forms_scored": sum(map(len, groups.values())),
        "concepts_scored": len(groups),
        "form_pairs_scored": tp + fp + fn + tn,
        "true_positive_pairs": tp,
        "false_positive_pairs": fp,
        "false_negative_pairs": fn,
        "true_negative_pairs": tn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
    }


def main():
    forms = read(ROOT / "data/d2/forms.csv")
    expert_rows = read(ROOT / "data/d2/cognates_expert.csv")
    concept_by_form = {row["ID"]: row["Concept_ID"] for row in forms}

    expert = defaultdict(set)
    doubtful_rows = 0
    for row in expert_rows:
        if row.get("Doubt", "").strip().lower() == "true":
            doubtful_rows += 1
            continue
        expert[row["Form_ID"]].add(row["Cognateset_ID"])

    if not expert:
        raise SystemExit("No confident expert cognate judgments found.")
    if not set(expert).issubset(concept_by_form):
        raise SystemExit("Expert cognate file contains form IDs absent from D2 forms.")

    reports = []
    for method in ("lexstat", "sca"):
        rows = read(ROOT / f"results/cognates/d2_{method}.csv")
        automatic = {row["Form_ID"]: row["Cognateset_ID"] for row in rows}
        if len(automatic) != len(rows):
            raise SystemExit(f"{method}: duplicate Form_ID in automatic output.")
        missing = set(expert) - set(automatic)
        if missing:
            raise SystemExit(f"{method}: {len(missing)} expert-coded forms lack automatic assignments.")
        reports.append(score(method, automatic, expert, concept_by_form))

    report = {
        "title": "D2 automatic cognate clustering against expert judgments",
        "reference": "data/d2/cognates_expert.csv",
        "automatic_outputs": [
            "results/cognates/d2_lexstat.csv",
            "results/cognates/d2_sca.csv",
        ],
        "reference_forms_with_confident_judgments": len(expert),
        "doubtful_reference_rows_excluded": doubtful_rows,
        "scoring": {
            "unit": "unordered form pairs within the same concept",
            "positive_rule": "the two forms share at least one confident expert cognate-set label",
            "automatic_rule": "the two forms have the same automatically assigned cognate-set ID",
            "multiple_expert_labels": "retained as a set; any shared label is positive",
            "scope": "only forms with confident expert labels are scored",
        },
        "results": reports,
        "limitations": [
            "Pairwise observations are dependent because each form occurs in multiple pairs.",
            "This is agreement with this expert-coded reference, not an independent gold standard.",
            "The benchmark does not measure semantic correctness, borrowing detection, or phylogenetic accuracy.",
            "No threshold tuning or held-out validation is performed here.",
        ],
    }
    output = ROOT / "qa/cognate_benchmark.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for result in reports:
        print(
            f'{result["method"]}: forms={result["forms_scored"]}, '
            f'pairs={result["form_pairs_scored"]}, '
            f'P={result["precision"]:.3f}, R={result["recall"]:.3f}, '
            f'F1={result["f1"]:.3f}'
        )
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
