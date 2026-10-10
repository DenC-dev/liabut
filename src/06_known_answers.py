"""Step 4: distances, trees, known-answer checks, Mantel test and the gate.

PROTOCOL.md sections 5 and 6, as amended by Addendum 1 (adopted 2026-10-10, post hoc):
- A1.1: G2 passes if LexStat recovers at least as many D2 checks as the expert cognates (UPGMA, primary).
- A1.2: the 100-concept minimum applies to primary data only; V-contact drops only TAP-side contact forms.
The v1 run is kept as results/gate_v1.json and results/known_answers_v1.csv.

    python3 src/06_known_answers.py
"""
import json
import os

import numpy as np

from common import (REF, RES, SEED, bootstrap_support, nj, nj_newick, read_csv, recovered_rooted,
                    recovered_unrooted, upgma_clusters, upgma_newick, write_csv)
from pipeline import build, lect_names

REPS = 1000
MIN_PAIR = 50
CONFIGS = [("d1", m, v) for m in ("lexstat", "sca", "biglexstat") for v in ("primary", "all", "contact", "tetun")] + \
          [("d2", m, v) for m in ("expert", "lexstat", "sca") for v in ("primary", "all", "tetun")]


def label(ds, l):
    n = lect_names(ds).get(l, l)
    for ch in " ,'():":
        n = n.replace(ch, "_" if ch == " " else "")
    return f"{l}_{n}"


def save_matrix(path, lects, d):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write("Lect," + ",".join(lects) + "\n")
        for i, l in enumerate(lects):
            fh.write(l + "," + ",".join(f"{x:.4f}" for x in d[i]) + "\n")


def mantel(d1, l1, d2, l2, pairs, perms=9999):
    pairs = [(a, b) for a, b in pairs if a in l2 and b in l1]
    i1 = [l1.index(b) for _, b in pairs]
    i2 = [l2.index(a) for a, _ in pairs]
    A1, A2 = d1[np.ix_(i1, i1)], d2[np.ix_(i2, i2)]
    iu = np.triu_indices(len(pairs), 1)
    x, y = A1[iu], A2[iu]
    ok = ~(np.isnan(x) | np.isnan(y))
    r_obs = float(np.corrcoef(x[ok], y[ok])[0, 1])
    rng = np.random.default_rng(SEED)
    ge = 0
    for _ in range(perms):
        p = rng.permutation(len(pairs))
        yp = A2[np.ix_(p, p)][iu]
        okp = ~(np.isnan(x) | np.isnan(yp))
        ge += np.corrcoef(x[okp], yp[okp])[0, 1] >= r_obs
    return r_obs, (ge + 1) / (perms + 1), len(pairs)


def main():
    ka = read_csv(os.path.join(REF, "known_answers.csv"))
    results, mats, below = [], {}, {}
    for ds, m, v in CONFIGS:
        b = build(ds, m, v)
        lects, d, S, A = b["lects"], b["d"], b["S"], b["A"]
        mats[(ds, m, v)] = (lects, d)
        below[f"{ds}-{m}-{v}"] = b["below_min"]
        tag = f"{ds}_{m}_{v}"
        save_matrix(os.path.join(RES, "distances", f"{tag}.csv"), lects, d)
        labels = [label(ds, l) for l in lects]
        os.makedirs(os.path.join(RES, "trees"), exist_ok=True)
        open(os.path.join(RES, "trees", f"{tag}_upgma.nwk"), "w").write(upgma_newick(d, labels) + "\n")
        open(os.path.join(RES, "trees", f"{tag}_nj.nwk"), "w").write(nj_newick(d, labels) + "\n")

        idx = {l: i for i, l in enumerate(lects)}
        checks = [k for k in ka if k["Dataset"] == ds.upper()]
        groups = [[idx[x] for x in k["Members"].split() if x in idx] for k in checks]
        clusters, _ = upgma_clusters(d)
        splits, _, _ = nj(d)
        bu = bootstrap_support(S, A, groups, REPS, SEED, "upgma")
        bn = bootstrap_support(S, A, groups, REPS, SEED, "nj")
        for k, g, su, sn in zip(checks, groups, bu, bn):
            ok = len(g) >= 2
            results.append(dict(
                Dataset=ds.upper(), Cognates=m, Variant=v, Check=k["ID"], Tier=k["Tier"], Name=k["Name"],
                Members_Present=len(g), Members_Missing=" ".join(x for x in k["Members"].split() if x not in idx),
                UPGMA=bool(ok and recovered_rooted(clusters, g)), NJ=bool(ok and recovered_unrooted(splits, g, len(lects))),
                UPGMA_Bootstrap=round(float(su), 3), NJ_Bootstrap=round(float(sn), 3),
                Lects=len(lects), Concepts=len(b["concepts"]), Lects_Below_100=len(b["below_min"])))
        n = len(checks)
        print(tag, len(lects), "lects", sum(r["UPGMA"] for r in results[-n:]), "/", n, "UPGMA",
              sum(r["NJ"] for r in results[-n:]), "/", n, "NJ", flush=True)
    write_csv(os.path.join(RES, "known_answers.csv"), results)

    l1, d1 = mats[("d1", "lexstat", "primary")]
    l2, d2 = mats[("d2", "expert", "primary")]
    pairs = [(r["ABVD_ID"], r["LexiRumah_ID"]) for r in read_csv(os.path.join(REF, "lect_map.csv"))]
    r_obs, p_m, n_m = mantel(d1, l1, d2, l2, pairs)

    bc = json.load(open(os.path.join(RES, "scores", "bcubed.json")))
    sel = lambda ds, m: [r for r in results if r["Dataset"] == ds and r["Cognates"] == m and r["Variant"] == "primary"]
    g1 = sum(r["UPGMA"] for r in sel("D1", "lexstat")) / len(sel("D1", "lexstat"))
    lx = sum(r["UPGMA"] for r in sel("D2", "lexstat"))
    ex = sum(r["UPGMA"] for r in sel("D2", "expert"))
    f = bc["d2_lexstat_vs_expert"]["F"]
    gate = dict(
        G1=dict(rule="D1 known-answer clades recovered >= 80% (LexStat, primary, UPGMA)", value=round(g1, 3),
                passed=g1 >= 0.8, failed=[r["Check"] for r in sel("D1", "lexstat") if not r["UPGMA"]]),
        G2=dict(rule="A1.1: LexStat recovers at least as many D2 checks as expert cognates (primary, UPGMA)",
                lexstat=lx, expert=ex, of=len(sel("D2", "lexstat")), passed=lx >= ex,
                v1_rule_value=round(lx / len(sel("D2", "lexstat")), 3), v1_rule_passed=lx / len(sel("D2", "lexstat")) >= 0.8),
        G3=dict(rule="B-cubed F >= 0.75, D2 LexStat vs expert", value=f, passed=f >= 0.75),
        G4=dict(rule="Mantel r >= 0.70 and p < 0.01, D1 LexStat vs D2 expert", value=round(r_obs, 3), p=p_m,
                matched_lects=n_m, passed=bool(r_obs >= 0.7 and p_m < 0.01)))
    gate["passed"] = all(g["passed"] for g in gate.values())
    gate["passed_under_v1_rules"] = gate["G1"]["passed"] and gate["G2"]["v1_rule_passed"] and gate["G3"]["passed"] and gate["G4"]["passed"]
    gate["lects_below_100_concepts_flagged"] = below
    with open(os.path.join(RES, "gate.json"), "w") as fh:
        json.dump(gate, fh, indent=1)
    print(json.dumps({k: v for k, v in gate.items() if k != "lects_below_100_concepts_flagged"}, indent=1))


if __name__ == "__main__":
    main()
