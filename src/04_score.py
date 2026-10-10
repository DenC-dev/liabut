"""Step 2b: score automatic cognates against the ABVD expert sets on D2 (B-cubed; PROTOCOL.md section 3).

Implementation note: an ABVD form can sit in more than one expert set (partial cognacy). For B-cubed each form
needs one class, so the first expert set listed for the form is used. Forms without an expert set are not scored.
Also reports agreement between our LexStat sets and LexiRumah's own biglexstat sets on D1 (descriptive).

    python3 src/04_score.py
"""
import json
import os
from collections import defaultdict

from common import DATA, RES, read_csv, write_csv


def bcubed(pred, gold):
    """pred, gold: dict item -> label; items grouped by concept beforehand. Returns P, R over items."""
    by_p, by_g = defaultdict(set), defaultdict(set)
    for i, l in pred.items():
        by_p[l].add(i)
    for i, l in gold.items():
        by_g[l].add(i)
    P = R = 0.0
    for i in gold:
        sp, sg = by_p[pred[i]], by_g[gold[i]]
        inter = len(sp & sg)
        P += inter / len(sp)
        R += inter / len(sg)
    return P, R, len(gold)


def score(pred_rows, gold, concept_of):
    pred = {r["Form_ID"]: r["Cognateset_ID"] for r in pred_rows}
    items = [f for f in gold if f in pred]
    per = defaultdict(list)
    for f in items:
        per[concept_of[f]].append(f)
    Pt = Rt = N = 0.0
    rows = []
    for c, fs in sorted(per.items()):
        p, r, n = bcubed({f: pred[f] for f in fs}, {f: gold[f] for f in fs})
        Pt, Rt, N = Pt + p, Rt + r, N + n
        pc, rc = p / n, r / n
        rows.append(dict(Concept_ID=c, Forms=n, P=round(pc, 4), R=round(rc, 4),
                         F=round(2 * pc * rc / (pc + rc), 4) if pc + rc else 0))
    P, R = Pt / N, Rt / N
    return dict(P=round(P, 4), R=round(R, 4), F=round(2 * P * R / (P + R), 4), forms=int(N)), rows


def main():
    forms = read_csv(os.path.join(DATA, "d2", "forms.csv"))
    concept_of = {r["ID"]: r["Concept_ID"] for r in forms}
    gold = {}
    for r in read_csv(os.path.join(DATA, "d2", "cognates_expert.csv")):
        gold.setdefault(r["Form_ID"], r["Cognateset_ID"])
    out = {}
    for m in ("lexstat", "sca"):
        pred = read_csv(os.path.join(RES, "cognates", f"d2_{m}.csv"))
        tot, rows = score(pred, gold, concept_of)
        out[f"d2_{m}_vs_expert"] = tot
        write_csv(os.path.join(RES, "scores", f"bcubed_d2_{m}_by_concept.csv"), rows)

    # D1: our LexStat against LexiRumah's biglexstat (agreement only; neither is a gold standard)
    d1forms = read_csv(os.path.join(DATA, "d1", "forms.csv"))
    c1 = {r["ID"]: r["Concept_ID"] for r in d1forms}
    big = {r["Form_ID"]: r["Cognateset_ID"] for r in read_csv(os.path.join(DATA, "d1", "cognates_biglexstat.csv"))}
    for m in ("lexstat", "sca"):
        pred = read_csv(os.path.join(RES, "cognates", f"d1_{m}.csv"))
        tot, _ = score(pred, big, c1)
        out[f"d1_{m}_vs_biglexstat"] = tot
    os.makedirs(os.path.join(RES, "scores"), exist_ok=True)
    with open(os.path.join(RES, "scores", "bcubed.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
