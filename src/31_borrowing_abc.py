"""E21 (Addendum 8): how much borrowing would each placement of Lakalei-Idate need? Approximate Bayesian computation.

Model H: the ML lexical tree (Lakalei-Idate sister to Central Timor) + borrowing into Lakalei-Idate from Eastern Timor.
Model G: the ML tree under the constraint (Lakalei-Idate + Eastern Timor) + borrowing into Lakalei-Idate from Nuclear
         Central Timor. (Implemented as an IQ-TREE constrained ML tree, which is how "regrafted as sister to Eastern
         Timor" is realised: Eastern Timor is not a clade in the unconstrained tree, so there is no single branch to
         graft onto.)
Summary statistics: the 18 E18 triplet counts (LI, NCT, X), X = Tetun, Habu, Kawaimina, stable and other concepts.

    python3 src/31_borrowing_abc.py
"""
import importlib
import json
import os
import subprocess
import sys
from collections import defaultdict
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import RES  # noqa: E402

ic = importlib.import_module("28_innovations_contact")
ex = importlib.import_module("10_exploratory")
te = importlib.import_module("20_total_evidence")
LIT = os.path.join(RES, "literature")
WORK = os.path.join(LIT, "e21_abc")
IQ = os.environ.get("IQTREE", "iqtree2")
N_SIM = int(os.environ.get("ABC_N", "20000"))
SEED = 20261011

LI = ["idat1237-cribas", "laka1255"]
NCT = ["mamb1306-Slete", "kema1243-kaila", "tuku1254"]
X = {"Tetun": ["tetu1245-suai"], "Habu": ["habu1241"], "Kawaimina": ["waim1252", "midi1237", "naue1237"]}
EAST = [t for v in X.values() for t in v]


def trees():
    from Bio import Phylo
    os.makedirs(WORK, exist_ok=True)
    cons = os.path.join(WORK, "constraint_LI_ET.nwk")
    others = [t for t in te.TAXON_GLOTTO if t not in LI + EAST]
    open(cons, "w").write("((" + ",".join(te.tx(t) for t in LI + EAST) + ")," + ",".join(te.tx(t) for t in others) + ");\n")
    lex = os.path.join(RES, "total_evidence", "lex.phy")
    if not os.path.exists(os.path.join(WORK, "G.treefile")):
        subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-s", lex, "-m", "GTR2+FO+G4",
                        "-g", cons, "-pre", os.path.join(WORK, "G")], check=True)
    H = Phylo.read(os.path.join(RES, "total_evidence", "lex_only.treefile"), "newick")
    G = Phylo.read(os.path.join(WORK, "G.treefile"), "newick")
    for t in (H, G):
        t.root_with_outgroup(te.tx("lama1277-lewoi"))
    return H, G


def branches(tree):
    """Pre-order list of (child_index, parent_index, length); tips named."""
    nodes = list(tree.find_clades(order="preorder"))
    idx = {id(n): i for i, n in enumerate(nodes)}
    parent = {}
    for n in nodes:
        for c in n.clades:
            parent[id(c)] = id(n)
    out = [(idx[id(n)], idx[parent[id(n)]], n.branch_length or 0.0) for n in nodes[1:]]
    tips = {n.name: idx[id(n)] for n in nodes if n.is_terminal()}
    return len(nodes), out, tips


def observed_and_masks():
    stable, _ = ex.stable_concepts()
    lects, rows, members, status, segs = ic.classify()
    attested = defaultdict(set)
    sets_of = defaultdict(set)
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        if status[r["Cognateset_ID"]] == "innovation":
            sets_of[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    concepts = sorted({r["Concept_ID"] for r in rows})
    obs = stats_from(lambda l, k: sets_of[(l, k)], lambda l: attested[l], concepts, stable)
    return concepts, stable, attested, obs


def stats_from(classes, att, concepts, stable):
    """18 counts: for X in Tetun, Habu, Kawaimina; stratum stable, other; pairs LI+NCT, LI+X, NCT+X."""
    out = []
    for xname, xs in X.items():
        for stratum in ("stable", "other"):
            n = np.zeros(3)
            for a, b, c in product(LI, NCT, xs):
                for k in att(a) & att(b) & att(c):
                    if (k in stable) != (stratum == "stable"):
                        continue
                    sa, sb, sc = classes(a, k), classes(b, k), classes(c, k)
                    n[0] += bool((sa & sb) - sc)
                    n[1] += bool((sa & sc) - sb)
                    n[2] += bool((sb & sc) - sa)
            out.extend(n.tolist())
    return np.array(out)


def simulate(tree_info, model, theta, concepts, stable_mask, att_mask, rng):
    nnodes, br, tips = tree_info
    s, r_s, b_s, b_o = theta
    K = len(concepts)
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
    tipstate = {t: state[i] for t, i in tips.items()}
    donors = EAST if model == "H" else NCT
    p = np.where(stable_mask, b_s, b_o)
    borrow = rng.random(K) < p
    pick = rng.integers(0, len(donors), K)
    don = np.array([tipstate[te.tx(donors[j])][k] for k, j in enumerate(pick)])
    for li in LI:
        v = tipstate[te.tx(li)].copy()
        v[borrow] = don[borrow]
        tipstate[te.tx(li)] = v
    return tipstate


def sim_stats(tipstate, concepts, att_idx, stable_mask):
    out = []
    for xname, xs in X.items():
        for stratum in (True, False):
            n = np.zeros(3)
            for a, b, c in product(LI, NCT, xs):
                m = att_idx[a] & att_idx[b] & att_idx[c] & (stable_mask == stratum)
                A, B, C = tipstate[te.tx(a)][m], tipstate[te.tx(b)][m], tipstate[te.tx(c)][m]
                n[0] += np.sum((A == B) & (A != 0) & (C != A))
                n[1] += np.sum((A == C) & (A != 0) & (B != A))
                n[2] += np.sum((B == C) & (B != 0) & (A != B))
            out.extend(n.tolist())
    return np.array(out)


def main():
    rng = np.random.default_rng(SEED)
    H, G = trees()
    info = {"H": branches(H), "G": branches(G)}
    concepts, stable, attested, obs = observed_and_masks()
    stable_mask = np.array([c in stable for c in concepts])
    att_idx = {l: np.array([c in attested[l] for c in concepts]) for l in LI + NCT + EAST}
    params, stats, models = [], [], []
    for model in ("H", "G"):
        for _ in range(N_SIM):
            theta = (rng.uniform(1, 12), rng.uniform(0.2, 1), rng.uniform(0, 0.6), rng.uniform(0, 0.6))
            ts = simulate(info[model], model, theta, concepts, stable_mask, None, rng)
            stats.append(sim_stats(ts, concepts, att_idx, stable_mask))
            params.append(theta)
            models.append(model)
    S = np.array(stats)
    P = np.array(params)
    M = np.array(models)
    sd = S.std(axis=0)
    sd[sd == 0] = 1
    d = np.sqrt((((S - obs) / sd) ** 2).sum(axis=1))
    keep = np.argsort(d)[: int(0.01 * len(d))]
    res = dict(observed=obs.tolist(), simulations_per_model=N_SIM, accepted=len(keep),
               model_posterior={m: round(float(np.mean(M[keep] == m)), 3) for m in ("H", "G")},
               distance_accepted_max=round(float(d[keep].max()), 3))
    names = ["rate_scale", "stable_rate_factor", "b_stable", "b_other"]
    for m in ("H", "G"):
        km = keep[M[keep] == m]
        own = np.where(M == m)[0]
        own_keep = own[np.argsort(d[own])[: int(0.01 * len(own))]]
        res[f"model_{m}"] = dict(
            accepted_in_pooled=len(km), best_distance=round(float(d[own].min()), 3),
            median_distance_top1pct=round(float(np.median(d[own_keep])), 3),
            posterior_within_model_top1pct={n: dict(median=round(float(np.median(P[own_keep, i])), 3),
                                                    q05=round(float(np.percentile(P[own_keep, i], 5)), 3),
                                                    q95=round(float(np.percentile(P[own_keep, i], 95)), 3))
                                            for i, n in enumerate(names)},
            share_b_stable_over_0_2=round(float(np.mean(P[own_keep, 2] > 0.2)), 3))
    # Diagnostic, added after the first run and not pre-declared: can this ABC tell the models apart at all?
    # 200 simulations per model are used as pseudo-observed data against the rest of the reference table.
    np.savez_compressed(os.path.join(WORK, "reference_table.npz"), S=S, P=P, M=M, obs=obs)
    cv = {}
    for m in ("H", "G"):
        idx = rng.choice(np.where(M == m)[0], 200, replace=False)
        post = []
        for i in idx:
            dd = np.sqrt((((S - S[i]) / sd) ** 2).sum(axis=1))
            dd[i] = np.inf
            k = np.argsort(dd)[: int(0.01 * len(dd))]
            post.append(np.mean(M[k] == m))
        post = np.array(post)
        cv[m] = dict(mean_posterior_of_true_model=round(float(post.mean()), 3),
                     share_correct_over_0_5=round(float(np.mean(post > 0.5)), 3))
    res["diagnostic_cross_validation"] = cv
    json.dump(res, open(os.path.join(LIT, "e21_borrowing_abc.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
