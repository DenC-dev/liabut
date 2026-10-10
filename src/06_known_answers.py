"""Step 4: distances, trees, known-answer checks, Mantel test and the gate (PROTOCOL.md sections 5 and 6).

Configurations: dataset (D1, D2) x cognates (D1: lexstat, sca, biglexstat; D2: expert, lexstat, sca)
x data variant (primary, all, contact [D1], tetun) x tree (UPGMA, NJ). The gate uses only
D1/D2 primary + LexStat + UPGMA, the D2 expert-vs-LexStat B-cubed score and the Mantel test.

    python3 src/06_known_answers.py
"""
import json
import os

import numpy as np

from common import (DATA, REF, RES, SEED, bootstrap_support, cognate_tensors, distance, nj, nj_newick, read_csv,
                    recovered_rooted, recovered_unrooted, upgma_clusters, upgma_newick, write_csv)

MIN_CONCEPTS = 100
MIN_PAIR = 50
REPS = 1000


def cognate_rows(ds, method):
    forms = {r["ID"]: r for r in read_csv(os.path.join(DATA, ds, "forms.csv"))}
    if method == "expert":
        src = read_csv(os.path.join(DATA, "d2", "cognates_expert.csv"))
    elif method == "biglexstat":
        src = read_csv(os.path.join(DATA, "d1", "cognates_biglexstat.csv"))
    else:
        src = read_csv(os.path.join(RES, "cognates", f"{ds}_{method}.csv"))
    rows = []
    for r in src:
        f = forms.get(r["Form_ID"])
        if f:
            rows.append(dict(Form_ID=r["Form_ID"], Lect_ID=f["Lect_ID"], Concept_ID=f["Concept_ID"],
                             Cognateset_ID=r["Cognateset_ID"]))
    return rows


def apply_variant(rows, flags, variant, contact_sets_lexstat):
    out = []
    for r in rows:
        fl = flags[r["Form_ID"]]
        if variant != "all" and (fl["L1_expert"] == "True" or fl["L3_indonesian"] == "True"
                                 or fl["L4_portuguese"] == "True"):
            continue
        if variant == "contact" and fl["L2_contact"] == "True":
            continue
        if variant == "tetun" and fl["L5_tetun"] == "True":
            continue
        out.append(r)
    return out


def main():
    ka = [r for r in read_csv(os.path.join(REF, "known_answers.csv"))]
    flags = {ds: {r["Form_ID"]: r for r in read_csv(os.path.join(RES, "loans", f"{ds}_flags.csv"))}
             for ds in ("d1", "d2")}
    names = {ds: {r["ID"]: r["Name"] for r in read_csv(os.path.join(DATA, ds, "lects.csv"))} for ds in ("d1", "d2")}

    configs = []
    for ds, methods, variants in (("d1", ("lexstat", "sca", "biglexstat"), ("primary", "all", "contact", "tetun")),
                                  ("d2", ("expert", "lexstat", "sca"), ("primary", "all", "tetun"))):
        for m in methods:
            for v in variants:
                configs.append((ds, m, v))

    results, mats, dropped_log, sparse_log = [], {}, {}, {}
    for ds, m, v in configs:
        rows = apply_variant(cognate_rows(ds, m), flags[ds], v, None)
        lects_all = [r["ID"] for r in read_csv(os.path.join(DATA, ds, "lects.csv"))]
        concepts = sorted({r["Concept_ID"] for r in rows})
        per_lect = {l: len({r["Concept_ID"] for r in rows if r["Lect_ID"] == l}) for l in lects_all}
        lects = [l for l in lects_all if per_lect[l] >= MIN_CONCEPTS]
        dropped_log[f"{ds}-{m}-{v}"] = {l: per_lect[l] for l in lects_all if l not in lects}
        S, A = cognate_tensors(rows, lects, concepts)
        d, shared = distance(S, A)
        sparse = [(lects[i], lects[j], int(shared[i, j])) for i in range(len(lects)) for j in range(i + 1, len(lects))
                  if shared[i, j] < MIN_PAIR]
        sparse_log[f"{ds}-{m}-{v}"] = len(sparse)
        mats[(ds, m, v)] = (lects, d)

        tag = f"{ds}_{m}_{v}"
        os.makedirs(os.path.join(RES, "distances"), exist_ok=True)
        with open(os.path.join(RES, "distances", f"{tag}.csv"), "w") as fh:
            fh.write("Lect," + ",".join(lects) + "\n")
            for i, l in enumerate(lects):
                fh.write(l + "," + ",".join(f"{x:.4f}" for x in d[i]) + "\n")
        labels = [f"{l}_{names[ds].get(l, l)}".replace(" ", "_").replace(",", "").replace("'", "")
                  .replace("(", "").replace(")", "").replace(":", "") for l in lects]
        os.makedirs(os.path.join(RES, "trees"), exist_ok=True)
        open(os.path.join(RES, "trees", f"{tag}_upgma.nwk"), "w").write(upgma_newick(d, labels) + "\n")
        open(os.path.join(RES, "trees", f"{tag}_nj.nwk"), "w").write(nj_newick(d, labels) + "\n")

        idx = {l: i for i, l in enumerate(lects)}
        checks = [k for k in ka if k["Dataset"] == ds.upper()]
        groups, usable = [], []
        for k in checks:
            mem = [idx[x] for x in k["Members"].split() if x in idx]
            missing = [x for x in k["Members"].split() if x not in idx]
            usable.append((k, mem, missing))
            groups.append(mem)
        clusters, _ = upgma_clusters(d)
        splits, _, _ = nj(d)
        boot_u = bootstrap_support(S, A, groups, REPS, SEED, "upgma")
        boot_n = bootstrap_support(S, A, groups, REPS, SEED, "nj")
        for (k, mem, missing), bu, bn in zip(usable, boot_u, boot_n):
            ok = len(mem) >= 2
            results.append(dict(
                Dataset=ds.upper(), Cognates=m, Variant=v, Check=k["ID"], Tier=k["Tier"], Name=k["Name"],
                Members_Present=len(mem), Members_Missing=" ".join(missing),
                UPGMA=bool(ok and recovered_rooted(clusters, mem)),
                NJ=bool(ok and recovered_unrooted(splits, mem, len(lects))),
                UPGMA_Bootstrap=round(float(bu), 3), NJ_Bootstrap=round(float(bn), 3),
                Lects=len(lects), Concepts=len(concepts)))
        print(tag, f"{len(lects)} lects", f"{len(concepts)} concepts",
              sum(r["UPGMA"] for r in results[-len(checks):]), "/", len(checks), "UPGMA;",
              sum(r["NJ"] for r in results[-len(checks):]), "/", len(checks), "NJ", flush=True)

    write_csv(os.path.join(RES, "known_answers.csv"), results)

    # Mantel: D1 LexStat primary vs D2 expert primary over matched lects
    l1, d1 = mats[("d1", "lexstat", "primary")]
    l2, d2 = mats[("d2", "expert", "primary")]
    pairs = [(r["ABVD_ID"], r["LexiRumah_ID"]) for r in read_csv(os.path.join(REF, "lect_map.csv"))
             if r["ABVD_ID"] in l2 and r["LexiRumah_ID"] in l1]
    i1 = [l1.index(b) for _, b in pairs]
    i2 = [l2.index(a) for a, _ in pairs]
    A1, A2 = d1[np.ix_(i1, i1)], d2[np.ix_(i2, i2)]
    iu = np.triu_indices(len(pairs), 1)
    x, y = A1[iu], A2[iu]
    ok = ~(np.isnan(x) | np.isnan(y))
    r_obs = float(np.corrcoef(x[ok], y[ok])[0, 1])
    rng = np.random.default_rng(SEED)
    ge = 0
    for _ in range(9999):
        p = rng.permutation(len(pairs))
        yp = A2[np.ix_(p, p)][iu]
        okp = ~(np.isnan(x) | np.isnan(yp))
        ge += np.corrcoef(x[okp], yp[okp])[0, 1] >= r_obs
    p_mantel = (ge + 1) / 10000

    bc = json.load(open(os.path.join(RES, "scores", "bcubed.json")))
    sel = lambda ds: [r for r in results if r["Dataset"] == ds and r["Cognates"] == "lexstat" and r["Variant"] == "primary"]
    g1 = sum(r["UPGMA"] for r in sel("D1")) / len(sel("D1"))
    g2 = sum(r["UPGMA"] for r in sel("D2")) / len(sel("D2"))
    f = bc["d2_lexstat_vs_expert"]["F"]
    gate = dict(
        G1=dict(rule="D1 known-answer clades recovered >= 80% (LexStat, primary, UPGMA)", value=round(g1, 3),
                passed=g1 >= 0.8, failed_checks=[r["Check"] for r in sel("D1") if not r["UPGMA"]]),
        G2=dict(rule="D2 known-answer clades recovered >= 80% (LexStat, primary, UPGMA)", value=round(g2, 3),
                passed=g2 >= 0.8, failed_checks=[r["Check"] for r in sel("D2") if not r["UPGMA"]]),
        G3=dict(rule="B-cubed F >= 0.75, D2 LexStat vs expert", value=f, passed=f >= 0.75),
        G4=dict(rule="Mantel r >= 0.70 and p < 0.01, D1 LexStat vs D2 expert distances", value=round(r_obs, 3),
                p=p_mantel, matched_lects=len(pairs), passed=bool(r_obs >= 0.7 and p_mantel < 0.01)),
    )
    gate["passed"] = all(g["passed"] for g in gate.values())
    gate["notes"] = dict(lects_dropped_below_100_concepts=dropped_log, pairs_below_50_shared_concepts=sparse_log)
    with open(os.path.join(RES, "gate.json"), "w") as fh:
        json.dump(gate, fh, indent=1)
    print(json.dumps({k: v for k, v in gate.items() if k != "notes"}, indent=1))


if __name__ == "__main__":
    main()
