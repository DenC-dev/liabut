"""E32 (Addendum 9): a fuller borrowing model for Lakalei-Idate, with ABC random forests and predictive checks.

Both placements (H: the ML lexical tree, Lakalei-Idate sister to Central Timor; G: the E21 tree constrained to
Lakalei-Idate + Eastern Timor) get the same bidirectional borrowing into proto-Lakalei-Idate: from Nuclear Central
Timor (b_c stable, b_c other) and from the Eastern Timor lects (b_e stable, b_e other). 36 summary statistics.

    RETENTION_RULE=chosen python3 src/37_abc2.py      # about 30-40 minutes
Writes results/literature/e32_abc2.json and e32_abc2/reference_table.npz.
"""
import importlib
import json
import os
import sys
from collections import defaultdict
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import RES  # noqa: E402

abc = importlib.import_module("31_borrowing_abc")
ic = abc.ic
te = abc.te
ex = abc.ex
LIT = os.path.join(RES, "literature")
WORK = os.path.join(LIT, "e32_abc2")
N_SIM = int(os.environ.get("ABC_N", "20000"))
N_PP = int(os.environ.get("ABC_PP", "500"))
SEED = 20261012

LI = abc.LI                      # idat1237-cribas, laka1255
IDATE, LAKALEI = ["idat1237-cribas"], ["laka1255"]
NCT = abc.NCT
X = abc.X                        # Tetun, Habu, Kawaimina
EAST = abc.EAST
TETUN, HABU = X["Tetun"], X["Habu"]
TRIPLETS = ([(LI, NCT, X[k]) for k in ("Tetun", "Habu", "Kawaimina")] + [(LI, TETUN, HABU)] +
            [(IDATE, NCT, HABU), (LAKALEI, NCT, HABU)])
STAT_NAMES = []
for (a, b, c), lab in zip(TRIPLETS, ["LI,NCT,Tetun", "LI,NCT,Habu", "LI,NCT,Kawaimina", "LI,Tetun,Habu",
                                     "Idate,NCT,Habu", "Lakalei,NCT,Habu"]):
    for stratum in ("stable", "other"):
        for pair in ("AB", "AC", "BC"):
            STAT_NAMES.append(f"{lab}|{stratum}|{pair}")


def observed():
    stable, _ = ex.stable_concepts()
    lects, rows, members, status, segs = ic.classify()
    attested = defaultdict(set)
    sets_of = defaultdict(set)
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        if status[r["Cognateset_ID"]] == "innovation":
            sets_of[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    concepts = sorted({r["Concept_ID"] for r in rows})
    out = []
    for A, B, C in TRIPLETS:
        for stratum in ("stable", "other"):
            n = np.zeros(3)
            for a, b, c in product(A, B, C):
                for k in attested[a] & attested[b] & attested[c]:
                    if (k in stable) != (stratum == "stable"):
                        continue
                    sa, sb, sc = sets_of[(a, k)], sets_of[(b, k)], sets_of[(c, k)]
                    n[0] += bool((sa & sb) - sc)
                    n[1] += bool((sa & sc) - sb)
                    n[2] += bool((sb & sc) - sa)
            out.extend(n.tolist())
    return concepts, stable, attested, np.array(out)


def simulate(info, theta, stable_mask, rng):
    nnodes, br, tips = info
    s, r_s, bc_s, bc_o, be_s, be_o = theta
    K = len(stable_mask)
    g = rng.gamma(1.0, 1.0, K) * np.where(stable_mask, r_s, 1.0)
    state = np.zeros((nnodes, K), dtype=np.int64)
    nxt = 1
    for child, par, L in br:
        ev = rng.poisson(s * g * L) > 0
        st = state[par].copy()
        m = int(ev.sum())
        if m:
            st[ev] = np.arange(nxt, nxt + m)
            nxt += m
        state[child] = st
    tip = {t: state[i] for t, i in tips.items()}
    pc = np.where(stable_mask, bc_s, bc_o)
    pe = np.where(stable_mask, be_s, be_o)
    u = rng.random(K)
    central = u < pc
    eastern = (~central) & (rng.random(K) < pe)
    dc = np.array([tip[te.tx(NCT[j])][k] for k, j in enumerate(rng.integers(0, len(NCT), K))])
    de = np.array([tip[te.tx(EAST[j])][k] for k, j in enumerate(rng.integers(0, len(EAST), K))])
    for li in LI:
        v = tip[te.tx(li)].copy()
        v[central] = dc[central]
        v[eastern] = de[eastern]
        tip[te.tx(li)] = v
    return tip


def stats(tip, att_idx, stable_mask):
    out = []
    for A, B, C in TRIPLETS:
        for stratum in (True, False):
            n = np.zeros(3)
            for a, b, c in product(A, B, C):
                m = att_idx[a] & att_idx[b] & att_idx[c] & (stable_mask == stratum)
                x, y, z = tip[te.tx(a)][m], tip[te.tx(b)][m], tip[te.tx(c)][m]
                n[0] += np.sum((x == y) & (x != 0) & (z != x))
                n[1] += np.sum((x == z) & (x != 0) & (y != x))
                n[2] += np.sum((y == z) & (y != 0) & (x != y))
            out.extend(n.tolist())
    return np.array(out)


def prior(rng):
    return (rng.uniform(1, 12), rng.uniform(0.2, 1), rng.uniform(0, 0.6), rng.uniform(0, 0.6),
            rng.uniform(0, 0.6), rng.uniform(0, 0.6))


def main():
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    os.makedirs(WORK, exist_ok=True)
    rng = np.random.default_rng(SEED)
    H, G = abc.trees()
    info = {"H": abc.branches(H), "G": abc.branches(G)}
    concepts, stable, attested, obs = observed()
    stable_mask = np.array([c in stable for c in concepts])
    lects = set(LI + NCT + EAST)
    att_idx = {l: np.array([c in attested[l] for c in concepts]) for l in lects}
    P, S, M = [], [], []
    for model in ("H", "G"):
        for i in range(N_SIM):
            th = prior(rng)
            S.append(stats(simulate(info[model], th, stable_mask, rng), att_idx, stable_mask))
            P.append(th)
            M.append(model)
            if i % 5000 == 0:
                print(model, i, flush=True)
    S, P, M = np.array(S), np.array(P), np.array(M)
    np.savez_compressed(os.path.join(WORK, "reference_table.npz"), S=S, P=P, M=M, obs=obs)
    y = (M == "G").astype(int)
    # ABC random forest model choice (Pudlo et al. 2016)
    rf = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=1, n_jobs=1, min_samples_leaf=1)
    rf.fit(S, y)
    votes = rf.predict_proba(obs.reshape(1, -1))[0]
    choice = "G" if votes[1] > votes[0] else "H"
    oob = rf.oob_decision_function_.argmax(axis=1)
    err = (oob != y).astype(float)
    reg = RandomForestRegressor(n_estimators=500, random_state=2, n_jobs=1, min_samples_leaf=5)
    reg.fit(S, err)
    p_err = float(reg.predict(obs.reshape(1, -1))[0])
    imp = sorted(zip(STAT_NAMES, rf.feature_importances_), key=lambda x: -x[1])[:10]
    # rejection ABC
    sd = S.std(axis=0)
    sd[sd == 0] = 1
    d = np.sqrt((((S - obs) / sd) ** 2).sum(axis=1))
    keep = np.argsort(d)[: int(0.01 * len(d))]
    names = ["rate_scale", "stable_rate_factor", "b_central_stable", "b_central_other", "b_east_stable",
             "b_east_other"]
    res = dict(observed=dict(zip(STAT_NAMES, obs.tolist())), simulations_per_model=N_SIM,
               rf=dict(votes_H=round(float(votes[0]), 3), votes_G=round(float(votes[1]), 3), chosen=choice,
                       posterior_of_chosen=round(1 - p_err, 3), oob_prior_error=round(float(err.mean()), 3),
                       top_statistics=[(n, round(float(v), 4)) for n, v in imp]),
               rejection=dict(model_posterior={m: round(float(np.mean(M[keep] == m)), 3) for m in ("H", "G")},
                              accepted=len(keep)))
    pp = {}
    for m in ("H", "G"):
        own = np.where(M == m)[0]
        ok = own[np.argsort(d[own])[: int(0.01 * len(own))]]
        res[f"model_{m}"] = dict(
            best_distance=round(float(d[own].min()), 3),
            posterior={n: dict(median=round(float(np.median(P[ok, i])), 3),
                               q05=round(float(np.percentile(P[ok, i], 5)), 3),
                               q95=round(float(np.percentile(P[ok, i], 95)), 3)) for i, n in enumerate(names)},
            share_central_stable_over_0_2=round(float(np.mean(P[ok, 2] > 0.2)), 3))
        sims = []
        for j in rng.choice(ok, N_PP, replace=True):
            sims.append(stats(simulate(info[m], P[j], stable_mask, rng), att_idx, stable_mask))
        sims = np.array(sims)
        lo = (sims <= obs).mean(axis=0)
        hi = (sims >= obs).mean(axis=0)
        pv = np.minimum(1, 2 * np.minimum(lo, hi))
        fails = [(STAT_NAMES[i], round(float(obs[i]), 1), round(float(np.median(sims[:, i])), 1), round(float(pv[i]), 3))
                 for i in range(len(obs)) if pv[i] < 0.05]
        pp[m] = dict(n_failed=len(fails), failed=fails)
    res["posterior_predictive"] = pp
    json.dump(res, open(os.path.join(LIT, "e32_abc2.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
