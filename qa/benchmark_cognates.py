#!/usr/bin/env python3
"""Reproduce D2 cognate-clustering benchmarks against expert judgments.

Run: python qa/benchmark_cognates.py
Standard-library only. Reports the protocol's B-cubed score (first expert
label per form, including the original partial-cognacy convention) and a
separate pairwise sensitivity score that excludes Doubt=True judgments.
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


def bcubed(pred, gold):
    by_p, by_g = defaultdict(set), defaultdict(set)
    for item, label in pred.items():
        by_p[label].add(item)
    for item, label in gold.items():
        by_g[label].add(item)
    precision = recall = 0.0
    for item in gold:
        shared = len(by_p[pred[item]] & by_g[gold[item]])
        precision += shared / len(by_p[pred[item]])
        recall += shared / len(by_g[gold[item]])
    n = len(gold)
    p, r = precision / n, recall / n
    return {"forms": n, "precision": p, "recall": r,
            "f1": 2 * p * r / (p + r) if p + r else 0.0}


def pairwise(method, automatic, expert, concept_by_form):
    groups = defaultdict(list)
    for form_id in expert:
        if form_id in automatic and form_id in concept_by_form:
            groups[concept_by_form[form_id]].append(form_id)
    tp = fp = fn = tn = 0
    for ids in groups.values():
        for left, right in combinations(ids, 2):
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
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return {
        "method": method, "forms_scored": sum(map(len, groups.values())),
        "concepts_scored": len(groups), "form_pairs_scored": tp + fp + fn + tn,
        "true_positive_pairs": tp, "false_positive_pairs": fp,
        "false_negative_pairs": fn, "true_negative_pairs": tn,
        "precision": round(p, 6), "recall": round(r, 6),
        "f1": round(2 * p * r / (p + r), 6) if p + r else 0.0,
    }


def main():
    forms = read(ROOT / "data/d2/forms.csv")
    expert_rows = read(ROOT / "data/d2/cognates_expert.csv")
    concept_by_form = {row["ID"]: row["Concept_ID"] for row in forms}

    # Match src/04_score.py and PROTOCOL.md: first listed expert set is the
    # reference class for B-cubed, including forms with partial judgments.
    expert_first = {}
    expert_confident = defaultdict(set)
    doubtful_rows = 0
    for row in expert_rows:
        expert_first.setdefault(row["Form_ID"], row["Cognateset_ID"])
        if row.get("Doubt", "").strip().lower() == "true":
            doubtful_rows += 1
        else:
            expert_confident[row["Form_ID"]].add(row["Cognateset_ID"])

    if not expert_first or not set(expert_first).issubset(concept_by_form):
        raise SystemExit("Expert cognate reference is empty or contains unknown form IDs.")

    results = []
    for method in ("lexstat", "sca"):
        rows = read(ROOT / f"results/cognates/d2_{method}.csv")
        automatic = {row["Form_ID"]: row["Cognateset_ID"] for row in rows}
        if len(automatic) != len(rows):
            raise SystemExit(f"{method}: duplicate Form_ID in automatic output.")
        if not set(expert_first).issubset(automatic):
            raise SystemExit(f"{method}: expert-coded forms lack automatic assignments.")

        # B-cubed is computed concept-by-concept, matching the project's
        # existing protocol implementation and its committed score tables.
        by_concept = defaultdict(list)
        for form_id in expert_first:
            by_concept[concept_by_form[form_id]].append(form_id)
        total_p = total_r = 0.0
        n_total = 0
        for ids in by_concept.values():
            local = bcubed(
                {i: automatic[i] for i in ids},
                {i: expert_first[i] for i in ids},
            )
            total_p += local["precision"] * local["forms"]
            total_r += local["recall"] * local["forms"]
            n_total += local["forms"]
        p, r = total_p / n_total, total_r / n_total
        b3 = {"forms": n_total, "concepts": len(by_concept),
              "precision": round(p, 4), "recall": round(r, 4),
              "f1": round(2 * p * r / (p + r), 4)}
        results.append({
            "method": method,
            "protocol_b_cubed": b3,
            "pairwise_sensitivity_excluding_doubtful_rows": pairwise(
                method, automatic, expert_confident, concept_by_form
            ),
        })

    report = {
        "title": "D2 automatic cognate clustering against expert judgments",
        "reference": "data/d2/cognates_expert.csv",
        "automatic_outputs": ["results/cognates/d2_lexstat.csv", "results/cognates/d2_sca.csv"],
        "doubtful_expert_rows": doubtful_rows,
        "protocol_b_cubed_rule": (
            "first expert cognate-set label per form; forms without expert labels excluded; "
            "B-cubed calculated within concept"
        ),
        "secondary_pairwise_rule": (
            "unordered pairs within concept; only confident expert rows retained; "
            "pair positive if any confident expert cognate-set label is shared"
        ),
        "results": results,
        "limitations": [
            "The expert coding is a reference standard for this benchmark, not an independent adjudication.",
            "Pairwise observations are dependent because each form occurs in multiple pairs.",
            "No threshold tuning or held-out validation is performed.",
            "Cognate agreement does not measure semantic correctness, borrowing detection, or phylogenetic accuracy.",
        ],
    }
    output = ROOT / "qa/cognate_benchmark.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for result in results:
        b = result["protocol_b_cubed"]
        print(f'{result["method"]} B-cubed: forms={b["forms"]}, '
              f'P={b["precision"]:.4f}, R={b["recall"]:.4f}, F1={b["f1"]:.4f}')
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
