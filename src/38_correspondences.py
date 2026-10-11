"""E33 (Addendum 9): regular correspondences as a loan test.

For a lect pair, every shared LexStat set is aligned (LingPy SCA, global) and scored by its identity share: the share
of aligned positions (gaps included) where the two segments are identical, ignoring length, stress and other marks.
Recent loans should sit closer to identity than the pair's inherited baseline (its shared retentions).

    python3 src/38_correspondences.py      # writes results/literature/e33_correspondences.json and e33_sets.csv
"""
import importlib
import json
import os
import sys
import unicodedata
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, RES, read_csv, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

a9 = importlib.import_module("34_addendum9")
ex = importlib.import_module("10_exploratory")
clf = importlib.import_module("35_classifier")
LIT = os.path.join(RES, "literature")
PAIRS = [("laka1255", "mamb1306-Slete"), ("idat1237-cribas", "mamb1306-Slete"), ("idat1237-cribas", "habu1241"),
         ("laka1255", "habu1241"), ("laka1255", "tetu1245-suai"), ("idat1237-cribas", "tetu1245-suai")]
MARKS = "ːˑˈˌ'ʰʷʲⁿ̃"


def base(seg):
    s = unicodedata.normalize("NFD", seg)
    s = "".join(ch for ch in s if not unicodedata.combining(ch) and ch not in MARKS)
    return s or seg


def identity(a, b):
    from lingpy.align.pairwise import Pairwise
    p = Pairwise(" ".join(a), " ".join(b))
    p.align(method="global")
    x, y, _ = p.alignments[0]
    same = sum(1 for u, v in zip(x, y) if u != "-" and v != "-" and base(u) == base(v))
    return same / len(x) if len(x) else 0.0


def mwu_greater(x, y):
    from scipy.stats import mannwhitneyu
    if len(x) < 2 or len(y) < 2:
        return None
    return float(mannwhitneyu(x, y, alternative="greater").pvalue)


def main():
    stable, _ = ex.stable_concepts()
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"]
            for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    rows = variant_rows("d1", "lexstat", "primary")
    rules = {"R0": a9.R0, "R2": json.load(open(os.path.join(LIT, "e30_classifier.json")))["chosen"]}
    stat = {k: a9.statuses(rows, r)[0] for k, r in rules.items()}
    by_set = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_set[r["Cognateset_ID"]][r["Lect_ID"]].append(r)
    res, table = {}, []
    for A, B in PAIRS:
        groups = {rule: defaultdict(list) for rule in rules}
        for sid, by in by_set.items():
            if A not in by or B not in by or sid not in stat["R0"]:
                continue
            fa, fb = by[A][0], by[B][0]
            idn = identity(segs[fa["Form_ID"]], segs[fb["Form_ID"]])
            stratum = "stable" if fa["Concept_ID"] in stable else "other"
            for rule in rules:
                groups[rule][(stat[rule][sid], stratum)].append(idn)
            table.append(dict(Pair=f"{A}|{B}", Cognateset_ID=sid, Concept=fa["Concept_ID"], Stratum=stratum,
                              Status_R0=stat["R0"][sid], Status_R2=stat["R2"][sid],
                              Form_A="".join(segs[fa["Form_ID"]]), Form_B="".join(segs[fb["Form_ID"]]),
                              Identity=round(idn, 3)))
        out = {}
        for rule, g in groups.items():
            ret = g[("retention", "stable")] + g[("retention", "other")]
            out[rule] = dict(
                n={f"{s}/{t}": len(v) for (s, t), v in g.items()},
                mean_identity={f"{s}/{t}": round(float(np.mean(v)), 3) for (s, t), v in g.items() if v},
                retentions_mean=round(float(np.mean(ret)), 3) if ret else None,
                p_innov_other_gt_innov_stable=mwu_greater(g[("innovation", "other")], g[("innovation", "stable")]),
                p_innov_gt_ret=mwu_greater(g[("innovation", "stable")] + g[("innovation", "other")], ret),
                p_innov_stable_gt_ret=mwu_greater(g[("innovation", "stable")], ret))
        res[f"{A}|{B}"] = out
    P = {}
    for rule in rules:
        lm, im, ih = res["laka1255|mamb1306-Slete"][rule], res["idat1237-cribas|mamb1306-Slete"][rule], \
            res["idat1237-cribas|habu1241"][rule]
        tests = {"P6 Lakalei-Mambae: other > stable innovations": lm["p_innov_other_gt_innov_stable"],
                 "P7 Idate-Habu: innovations > retentions": ih["p_innov_gt_ret"],
                 "P8a Lakalei-Mambae: stable innovations > retentions (predicted not)": lm["p_innov_stable_gt_ret"],
                 "P8b Idate-Mambae: stable innovations > retentions (predicted not)": im["p_innov_stable_gt_ret"]}
        names = list(tests)
        ps = [tests[n] if tests[n] is not None else 1.0 for n in names]
        hol = a9.holm(ps)
        P[rule] = {n: dict(p=None if tests[n] is None else round(tests[n], 4), holm=round(h, 4)) for n, h in zip(names, hol)}
        P[rule]["P6 holds"] = hol[0] < 0.05
        P[rule]["P7 holds"] = hol[1] < 0.05
        P[rule]["P8 holds"] = ps[2] >= 0.05 and ps[3] >= 0.05
    res["predictions"] = P
    json.dump(res, open(os.path.join(LIT, "e33_correspondences.json"), "w"), indent=1, ensure_ascii=False)
    write_csv(os.path.join(LIT, "e33_sets.csv"), table)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
