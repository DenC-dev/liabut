"""E31 (Addendum 9): the triplet test under unequal rates (simulated null), and its power.

Null: the E21 simulator on the ML lexical tree with its branch lengths and no borrowing; rate scale and stable factor
drawn from E21's accepted model-H runs. Power: borrowing into proto-Lakalei-Idate from Habu on a share of other
concepts. D is always the excess of (focal + third) over (Nuclear Central Timor + third).

    python3 src/36_triplet_power.py      # writes results/literature/e31_triplet_power.json
"""
import importlib
import json
import math
import os
import sys
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import RES  # noqa: E402

abc = importlib.import_module("31_borrowing_abc")
te = abc.te
LIT = os.path.join(RES, "literature")
SEED = 20261013
N_NULL, N_POW = 2000, 500
RATES = [0.0, 0.05, 0.1, 0.2, 0.3]
G = {"LI": abc.LI, "NCT": abc.NCT, "Welaun": ["west2547-welaun"], "Tetun": ["tetu1245-suai"], "Habu": ["habu1241"],
     "Kawaimina": ["waim1252", "midi1237", "naue1237"], "Galoli": ["galo1243"]}
TRIPS = [("Welaun", "NCT", "Tetun"), ("LI", "NCT", "Tetun"), ("LI", "NCT", "Habu"), ("LI", "NCT", "Kawaimina"),
         ("LI", "NCT", "Galoli")]


def dz(per):
    """per: concepts x 3 counts (AB, AC, BC). Returns D (AC vs BC excess) and jackknife Z."""
    tot = per.sum(axis=0)

    def d(v):
        s = v[1] + v[2]
        return (v[1] - v[2]) / s if s else 0.0
    D = d(tot)
    m = len(per)
    if m < 2:
        return D, None, tot
    jk = np.array([d(tot - per[i]) for i in range(m)])
    se = math.sqrt((m - 1) / m * ((jk - jk.mean()) ** 2).sum())
    return D, (D / se if se > 0 else None), tot


def per_concept(tip, A, B, C, att_idx, mask):
    rows = np.zeros((len(mask), 3))
    used = np.zeros(len(mask), dtype=bool)
    for a, b, c in product(G[A], G[B], G[C]):
        m = att_idx[a] & att_idx[b] & att_idx[c] & mask
        used |= m
        x, y, z = tip[te.tx(a)], tip[te.tx(b)], tip[te.tx(c)]
        rows[:, 0] += m & (x == y) & (x != 0) & (z != x)
        rows[:, 1] += m & (x == z) & (x != 0) & (y != x)
        rows[:, 2] += m & (y == z) & (y != 0) & (x != y)
    return rows[used]


def observed_per_concept(sets_of, attested, concepts, A, B, C, mask):
    rows = np.zeros((len(concepts), 3))
    used = np.zeros(len(concepts), dtype=bool)
    for a, b, c in product(G[A], G[B], G[C]):
        for i, k in enumerate(concepts):
            if not mask[i] or k not in attested[a] or k not in attested[b] or k not in attested[c]:
                continue
            used[i] = True
            sa, sb, sc = sets_of[(a, k)], sets_of[(b, k)], sets_of[(c, k)]
            rows[i, 0] += bool((sa & sb) - sc)
            rows[i, 1] += bool((sa & sc) - sb)
            rows[i, 2] += bool((sb & sc) - sa)
    return rows[used]


def main():
    from collections import defaultdict
    rng = np.random.default_rng(SEED)
    H, _ = abc.trees()
    info = abc.branches(H)
    stable, _ = abc.ex.stable_concepts()
    lects, rows, members, status, segs = abc.ic.classify()
    attested, sets_of = defaultdict(set), defaultdict(set)
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        if status[r["Cognateset_ID"]] == "innovation":
            sets_of[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    concepts = sorted({r["Concept_ID"] for r in rows})
    smask = np.array([c in stable for c in concepts])
    allx = {t for g in G.values() for t in g}
    att_idx = {l: np.array([c in attested[l] for c in concepts]) for l in allx}
    # accepted model-H parameters from E21
    ref = np.load(os.path.join(LIT, "e21_abc", "reference_table.npz"), allow_pickle=True)
    S, P, M, obs = ref["S"], ref["P"], ref["M"], ref["obs"]
    sd = S.std(axis=0)
    sd[sd == 0] = 1
    d = np.sqrt((((S - obs) / sd) ** 2).sum(axis=1))
    own = np.where(M == "H")[0]
    acc = own[np.argsort(d[own])[: int(0.01 * len(own))]]
    observed = {}
    for A, B, C in TRIPS:
        for st, mask in (("stable", smask), ("other", ~smask)):
            D, Z, tot = dz(observed_per_concept(sets_of, attested, concepts, A, B, C, mask))
            observed[f"({A}, {B}, {C}) {st}"] = dict(D=round(D, 3), Z=round(Z, 2) if Z else None, counts=tot.tolist())

    def sim(theta, habu_rate=0.0):
        s, r_s = theta[0], theta[1]
        tip = abc.simulate(info, "H", (s, r_s, 0.0, 0.0), concepts, smask, None, rng)
        if habu_rate > 0:
            borrow = (~smask) & (rng.random(len(concepts)) < habu_rate)
            donor = tip[te.tx("habu1241")]
            for li in G["LI"]:
                v = tip[te.tx(li)].copy()
                v[borrow] = donor[borrow]
                tip[te.tx(li)] = v
        return tip
    null = {k: [] for k in observed}
    for _ in range(N_NULL):
        tip = sim(P[rng.choice(acc)])
        for A, B, C in TRIPS:
            for st, mask in (("stable", smask), ("other", ~smask)):
                D, Z, _ = dz(per_concept(tip, A, B, C, att_idx, mask))
                null[f"({A}, {B}, {C}) {st}"].append((D, Z if Z is not None else 0.0))
    res = dict(null_replicates=N_NULL, observed=observed, null={})
    for k, v in null.items():
        Ds = np.array([x[0] for x in v])
        Zs = np.array([x[1] for x in v])
        o = observed[k]["D"]
        res["null"][k] = dict(D_null_median=round(float(np.median(Ds)), 3),
                              D_null_95=[round(float(np.percentile(Ds, 2.5)), 3), round(float(np.percentile(Ds, 97.5)), 3)],
                              p_upper=round(float(np.mean(Ds >= o)), 4),
                              p_upper_Z=round(float(np.mean(Zs >= (observed[k]["Z"] or 0))), 4),
                              share_null_Z_ge_2=round(float(np.mean(Zs >= 2)), 3))
    # post hoc (not pre-declared): a calibrated threshold, the 95th percentile of the simulated null Z
    zcut = float(np.percentile([x[1] for x in null["(LI, NCT, Habu) other"]], 95))
    power = {}
    for rate in RATES:
        det_o, det_s, overtake, cal = [], [], [], []
        for _ in range(N_POW):
            tip = sim(P[rng.choice(acc)], rate)
            Do, Zo, to = dz(per_concept(tip, "LI", "NCT", "Habu", att_idx, ~smask))
            Ds, Zs, ts = dz(per_concept(tip, "LI", "NCT", "Habu", att_idx, smask))
            det_o.append(Zo is not None and Zo >= 2)
            det_s.append(Zs is not None and Zs >= 2)
            overtake.append(to[1] >= to[0])
            cal.append(Zo is not None and Zo >= zcut)
        power[str(rate)] = dict(detect_other_Z_ge_2=round(float(np.mean(det_o)), 3),
                                detect_stable_Z_ge_2=round(float(np.mean(det_s)), 3),
                                habu_pair_at_least_tree_pair_other=round(float(np.mean(overtake)), 3),
                                post_hoc_calibrated_detect_other=round(float(np.mean(cal)), 3))
        print(rate, power[str(rate)], flush=True)
    res["power_habu_borrowing_other_concepts"] = power
    res["post_hoc_calibrated_Z_threshold"] = round(zcut, 2)
    res["validation"] = dict(false_detection_at_0=power["0.0"]["detect_other_Z_ge_2"],
                             detection_at_0_2=power["0.2"]["detect_other_Z_ge_2"],
                             passes=power["0.0"]["detect_other_Z_ge_2"] <= 0.10 and power["0.2"]["detect_other_Z_ge_2"] >= 0.5)
    json.dump(res, open(os.path.join(LIT, "e31_triplet_power.json"), "w"), indent=1)
    print(json.dumps(res["null"], indent=1))
    print(json.dumps(res["validation"]))


if __name__ == "__main__":
    main()
