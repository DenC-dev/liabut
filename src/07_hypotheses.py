"""Step 5: lexical support for every hypothesis clade (PROTOCOL.md section 7, Addendum 2 A2.2).

For each configuration (dataset x cognates x variant, plus Austronesian-only D1 trees), each hypothesis clade is
checked on UPGMA and NJ trees after pruning its `Prune` lects, with 1,000 concept-bootstrap replicates.
A clade is "lexically supported" if bootstrap >= 70% under UPGMA and NJ on D1 LexStat primary, V-contact and V-tetun.

    python3 src/07_hypotheses.py
"""
import os

import numpy as np

from common import REF, RES, SEED, bootstrap_support, distance, nj, read_csv, recovered_rooted, recovered_unrooted, \
    upgma_clusters, write_csv
from pipeline import build, roles

REPS = 1000
THRESH = 0.70
# D2 lects that have no LexiRumah twin take the membership of a close stand-in (same subgroup in every hypothesis)
D2_STANDIN = {"70": "luan1264", "1366": "tetu1245-suai", "486": "lama1277-lewoi"}


def hypotheses():
    h = read_csv(os.path.join(REF, "hypotheses.csv")) + read_csv(os.path.join(REF, "hypotheses_addendum2.csv"))
    return [dict(ID=r["ID"], Source=r["Source"], Name=r["Name"], Members=set(r["Members"].split()),
                 Prune=set(r["Prune"].split()), Contrast=r["Contrast"]) for r in h]


def d2_alias():
    m = {r["ABVD_ID"]: r["LexiRumah_ID"] for r in read_csv(os.path.join(REF, "lect_map.csv"))}
    m.update(D2_STANDIN)
    return m


def evaluate(b, hyps, alias=None):
    """b: output of pipeline.build. Returns rows with recovery and bootstrap support per hypothesis."""
    lects = b["lects"]
    key = [alias.get(l, None) if alias else l for l in lects]
    out = []
    by_prune = {}
    for h in hyps:
        by_prune.setdefault(frozenset(h["Prune"]), []).append(h)
    for prune, hs in by_prune.items():
        keep = [i for i, k in enumerate(key) if k not in prune]
        S, A = b["S"][:, keep][:, :, keep], b["A"][:, keep][:, :, keep]
        d, _ = distance(S, A)
        kk = [key[i] for i in keep]
        groups, info = [], []
        for h in hs:
            g = [j for j, k in enumerate(kk) if k in h["Members"]]
            groups.append(g)
            info.append((h, len(g), len([m for m in h["Members"] if m not in prune])))
        cl, _ = upgma_clusters(d)
        sp, _, _ = nj(d)
        bu = bootstrap_support(S, A, groups, REPS, SEED, "upgma")
        bn = bootstrap_support(S, A, groups, REPS, SEED, "nj")
        for (h, n_present, n_def), g, su, sn in zip(info, groups, bu, bn):
            testable = len(g) >= 2 and len(g) < len(kk) - 1
            out.append(dict(Hypothesis=h["ID"], Name=h["Name"], Source=h["Source"], Contrast=h["Contrast"],
                            Members_Present=n_present, Lects_In_Tree=len(kk), Testable=testable,
                            UPGMA=bool(testable and recovered_rooted(cl, g)),
                            NJ=bool(testable and recovered_unrooted(sp, g, len(kk))),
                            UPGMA_Bootstrap=round(float(su), 3) if testable else None,
                            NJ_Bootstrap=round(float(sn), 3) if testable else None))
    return out


def main():
    hyps = hypotheses()
    rows = []
    configs = [("d1", m, v, None) for m in ("lexstat", "sca", "biglexstat") for v in ("primary", "all", "contact", "tetun")]
    configs += [("d1", "lexstat", v, "an_only") for v in ("primary", "contact", "tetun")]
    configs += [("d2", m, v, None) for m in ("expert", "lexstat", "sca") for v in ("primary", "all", "tetun")]
    role = roles()
    for ds, m, v, opt in configs:
        b = build(ds, m, v)
        if opt == "an_only":
            keep = [i for i, l in enumerate(b["lects"]) if role.get(l) != "TAP"]
            b = dict(b, lects=[b["lects"][i] for i in keep], S=b["S"][:, keep][:, :, keep], A=b["A"][:, keep][:, :, keep])
        res = evaluate(b, hyps, d2_alias() if ds == "d2" else None)
        for r in res:
            r.update(Dataset=ds.upper(), Cognates=m, Variant=v + ("+AN-only" if opt else ""))
        rows += res
        print(ds, m, v, opt or "", "done", flush=True)
    cols = ["Dataset", "Cognates", "Variant", "Hypothesis", "Name", "Source", "Contrast", "Members_Present",
            "Lects_In_Tree", "Testable", "UPGMA", "NJ", "UPGMA_Bootstrap", "NJ_Bootstrap"]
    write_csv(os.path.join(RES, "hypotheses", "clade_support.csv"), rows, cols)

    # the pre-registered 70% rule, D1 LexStat
    summ = []
    for h in hyps:
        get = lambda var: next((r for r in rows if r["Dataset"] == "D1" and r["Cognates"] == "lexstat"
                                and r["Variant"] == var and r["Hypothesis"] == h["ID"]), None)
        p, c, t, a = get("primary"), get("contact"), get("tetun"), get("primary+AN-only")
        ok = lambda r: r is not None and r["Testable"] and r["UPGMA_Bootstrap"] >= THRESH and r["NJ_Bootstrap"] >= THRESH
        summ.append(dict(Hypothesis=h["ID"], Name=h["Name"], Source=h["Source"], Contrast=h["Contrast"],
                         Primary_UPGMA=p["UPGMA_Bootstrap"], Primary_NJ=p["NJ_Bootstrap"],
                         Contact_UPGMA=c["UPGMA_Bootstrap"], Contact_NJ=c["NJ_Bootstrap"],
                         Tetun_UPGMA=t["UPGMA_Bootstrap"], Tetun_NJ=t["NJ_Bootstrap"],
                         ANonly_UPGMA=a["UPGMA_Bootstrap"], ANonly_NJ=a["NJ_Bootstrap"],
                         Lexically_Supported=ok(p) and ok(c) and ok(t)))
    write_csv(os.path.join(RES, "hypotheses", "summary_d1_lexstat.csv"), summ)
    for s in summ:
        print(f"{s['Hypothesis']:9s} {s['Name'][:38]:38s} P {s['Primary_UPGMA']}/{s['Primary_NJ']}  "
              f"C {s['Contact_UPGMA']}/{s['Contact_NJ']}  T {s['Tetun_UPGMA']}/{s['Tetun_NJ']}  "
              f"AN {s['ANonly_UPGMA']}/{s['ANonly_NJ']}  -> {'SUPPORTED' if s['Lexically_Supported'] else 'no'}")


if __name__ == "__main__":
    main()
