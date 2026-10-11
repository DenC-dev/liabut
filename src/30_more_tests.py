"""Addendum 8: E20 (which member of Lakalei-Idate carries each signal), E22 (historical glottometry),
E24 (triplet tests on other disputed branches).

    python3 src/30_more_tests.py e20|e22|e24|all
"""
import csv
import importlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from itertools import product

import numpy as np
from scipy.stats import binomtest

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, read_csv  # noqa: E402

ic = importlib.import_module("28_innovations_contact")
ex = importlib.import_module("10_exploratory")
bayes = importlib.import_module("09_bayes")
LIT = os.path.join(RES, "literature")


def setup():
    stable, _ = ex.stable_concepts()
    lects, rows, members, status, segs = ic.classify()
    attested = defaultdict(set)
    sets_of = defaultdict(set)
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        if status[r["Cognateset_ID"]] == "innovation":
            sets_of[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    inn = {s: {r["Lect_ID"] for r in rs} for s, rs in members.items() if status[s] == "innovation"}
    concept_of = {s: rs[0]["Concept_ID"] for s, rs in members.items()}
    return dict(stable=stable, lects=lects, rows=rows, members=members, status=status, segs=segs,
                attested=attested, sets_of=sets_of, inn=inn, concept_of=concept_of)


def grp(lects, lid):
    return ic.GROUP_OF.get(lects[lid]["Group"], "other") if lid not in ic.LI else "LI"


# ------------------------------------------------------------------ E20
def e20(S, idate="idat1237"):
    lects, att = S["lects"], S["attested"]
    lak = "laka1255"
    types = {"Central Timor": "CT", "Habu": "Habu", "Tetun": "Tetun", "Kawaimina": "Kawaimina"}
    eastern = {"Tetun", "Habu", "Kawaimina"}
    out = {}
    for label, g in types.items():
        counts = {stratum: Counter() for stratum in ("all", "stable", "other")}
        examples = []
        for s, ls in S["inn"].items():
            c = S["concept_of"][s]
            if c not in att[idate] or c not in att[lak]:
                continue
            groups = {grp(lects, l) for l in ls if l not in ic.LI}
            if g not in groups:
                continue
            rivals = ({"CT"} | eastern) - {g}
            if groups & rivals:
                continue
            i, k = idate in ls, lak in ls
            if not (i or k):
                continue
            cls = "both" if i and k else "Lakalei only" if k else "Idate only"
            for stratum in ("all", "stable" if c in S["stable"] else "other"):
                counts[stratum][cls] += 1
            examples.append(dict(type=label, concept=c, pattern=cls,
                                 forms="; ".join(f"{lects[r['Lect_ID']]['Name']}: {''.join(S['segs'][r['Form_ID']])}"
                                                 for r in S["members"][s] if r["Lect_ID"] in (idate, lak) or
                                                 grp(lects, r["Lect_ID"]) == g)[:300]))
        res = {}
        for stratum, cnt in counts.items():
            lo, io = cnt["Lakalei only"], cnt["Idate only"]
            p = binomtest(lo, lo + io, 0.5).pvalue if lo + io else None
            res[stratum] = dict(both=cnt["both"], lakalei_only=lo, idate_only=io,
                                binomial_p=round(p, 4) if p is not None else None)
        out[label] = res
        with open(os.path.join(LIT, f"e20_examples_{idate}{ic.SUF}.csv"), "a" if label != "Central Timor" else "w",
                  newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["type", "concept", "pattern", "forms"])
            if label == "Central Timor":
                w.writeheader()
            w.writerows(examples)
    return out


def run_e20(S):
    res = dict(primary_idat1237=e20(S, "idat1237"), sensitivity_idat1237_cribas=e20(S, "idat1237-cribas"))
    km = {}
    for li in ("idat1237", "idat1237-cribas", "laka1255"):
        km[li] = {o: round(ic.km(S["lects"][li], S["lects"][o])) for o in
                  ("mamb1306-Slete", "kema1243-kaila", "tuku1254", "habu1241", "tetu1245-suai", "galo1243")}
    res["distances_km"] = km
    json.dump(res, open(os.path.join(LIT, f"e20_split_test{ic.SUF}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


# ------------------------------------------------------------------ E22
NAMED = {
    "Lakalei-Idate": ["idat1237-cribas", "laka1255"],
    "Nuclear Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254"],
    "Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun"],
    "Lakalei-Idate + Nuclear Central Timor (Ramelaic)": ["mamb1306-Slete", "kema1243-kaila", "tuku1254",
                                                         "idat1237-cribas", "laka1255"],
    "Lakalei-Idate + Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun",
                                      "idat1237-cribas", "laka1255"],
    "Eastern Timor": ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"],
    "Lakalei-Idate + Eastern Timor": ["idat1237-cribas", "laka1255", "tetu1245-suai", "habu1241", "waim1252",
                                      "midi1237", "naue1237"],
    "Lakalei-Idate + Habu": ["idat1237-cribas", "laka1255", "habu1241"],
    "Tetun + Habu": ["tetu1245-suai", "habu1241"],
    "Habu + Kawaimina": ["habu1241", "waim1252", "midi1237", "naue1237"],
    "Kawaimina": ["waim1252", "midi1237", "naue1237"],
    "Waima'a + Naueti": ["waim1252", "naue1237"],
    "Wetar-Atauro (with Galoli)": ["galo1243", "dadu1237", "ilma1240", "kaha1239"],
    "Wetar": ["ilma1240", "kaha1239"],
    "Rote-Meto": ["koto1251", "term1237", "dela1252"],
    "Helong + Meto": ["funa1237", "koto1251"],
}


def run_e22(S):
    lects = S["lects"]
    taxa = [t for t in bayes.BAYES_TAXA if t not in bayes.OUTGROUP]
    flores = {l for l, info in lects.items() if info["Group"] == "Flores-Lembata"}
    items = []   # (taxon set, attested set)
    for s, ls in S["inn"].items():
        if ls & flores:
            continue
        c = S["concept_of"][s]
        T = frozenset(t for t in taxa if t in ls)
        if len(T) < 2:
            continue
        items.append((T, frozenset(t for t in taxa if c in S["attested"][t]), "lexical"))
    sc = {r["Taxon"]: r for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                           "innovation_matrix_24_hull.csv"))}
    chars = ["p_lenited", "ng_velar", "ng_n", "j_rhotic", "j_l", "R_zero", "b_lenited", "d_liquid", "b_h_initial",
             "k_lost_initial", "k_lost_medial"]
    for ch in chars:
        T = frozenset(t for t in taxa if sc[t][ch] == "1")
        A = frozenset(t for t in taxa if sc[t][ch] in ("0", "1"))
        if 2 <= len(T) < len(A):
            items.append((T, A, "sound"))

    def score(G):
        G = frozenset(G)
        eps = p = q = 0
        for T, A, _ in items:
            if not G <= A:
                continue
            if T == G:
                eps += 1
            if G <= T:
                p += 1
            elif T & G and T - G and G - T:
                q += 1
        k = p / (p + q) if p + q else 0.0
        return dict(epsilon=eps, p=p, q=q, kappa=round(k, 3), sigma=round(eps * k, 2))
    cands = {T for T, _, _ in items}
    scored = sorted(((score(G), G) for G in cands), key=lambda x: -x[0]["sigma"])
    names = {frozenset(v): k for k, v in NAMED.items()}
    top = [dict(group=names.get(G, " + ".join(sorted(G))), size=len(G), **sc_) for sc_, G in scored[:15]]
    named = {k: score(v) for k, v in NAMED.items()}
    res = dict(innovations=len(items), lexical=sum(1 for i in items if i[2] == "lexical"),
               sound=sum(1 for i in items if i[2] == "sound"), top15_by_sigma=top, named=named)
    json.dump(res, open(os.path.join(LIT, f"e22_glottometry{ic.SUF}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


# ------------------------------------------------------------------ E24
G24 = {"Habu": ["habu1241"], "Tetun": ["tetu1245-suai"], "Kawaimina": ["waim1252", "midi1237", "naue1237"],
       "Waima'a": ["waim1252"], "Naueti": ["naue1237"], "Midiki": ["midi1237"], "Galoli": ["galo1243"],
       "Wetar": ["ilma1240", "kaha1239"], "Dadu'a": ["dadu1237"], "Helong": ["funa1237"], "Meto": ["koto1251"],
       "Rote": ["term1237", "dela1252"], "Welaun": ["west2547-welaun"],
       "NCT": ["mamb1306-Slete", "kema1243-kaila", "tuku1254"]}
T24 = [("Welaun", "NCT", "Tetun"), ("Habu", "Tetun", "Kawaimina"), ("Waima'a", "Naueti", "Midiki"),
       ("Galoli", "Wetar", "Dadu'a"), ("Galoli", "Wetar", "Tetun"), ("Helong", "Meto", "Rote")]


def triplet(S, A, B, C, groups):
    out = {}
    for stratum in ("all", "stable", "other"):
        per = defaultdict(lambda: np.zeros(3))
        for a, b, c in product(groups[A], groups[B], groups[C]):
            for k in S["attested"][a] & S["attested"][b] & S["attested"][c]:
                if stratum == "stable" and k not in S["stable"] or stratum == "other" and k in S["stable"]:
                    continue
                sa, sb, sc = S["sets_of"][(a, k)], S["sets_of"][(b, k)], S["sets_of"][(c, k)]
                v = per[k]
                v[0] += bool((sa & sb) - sc)
                v[1] += bool((sa & sc) - sb)
                v[2] += bool((sb & sc) - sa)
        M = np.array(list(per.values())) if per else np.zeros((0, 3))
        tot = M.sum(axis=0)
        names = [f"{A}+{B}", f"{A}+{C}", f"{B}+{C}"]
        t = int(np.argmax(tot))
        mi = [i for i in range(3) if i != t]

        def d(v):
            s = v[mi[0]] + v[mi[1]]
            return (v[mi[0]] - v[mi[1]]) / s if s else 0.0
        D = d(tot)
        m = len(M)
        jk = np.array([d(tot - M[i]) for i in range(m)]) if m > 1 else np.array([0.0])
        se = math.sqrt((m - 1) / m * ((jk - jk.mean()) ** 2).sum()) if m > 1 else float("nan")
        out[stratum] = dict(concepts=m, counts={n: int(x) for n, x in zip(names, tot)}, tree_pair=names[t],
                            D=dict(pair_excess=f"{names[mi[0]]} vs {names[mi[1]]}", value=round(D, 3),
                                   se=round(se, 3), Z=round(D / se, 2) if se and se > 0 else None))
    return out


def run_e24(S):
    res = {f"({A}, {B}, {C})": triplet(S, A, B, C, G24) for A, B, C in T24}
    json.dump(res, open(os.path.join(LIT, f"e24_other_branches{ic.SUF}.json"), "w"), indent=1, ensure_ascii=False)
    for k, v in res.items():
        print(k, json.dumps(v, ensure_ascii=False))


if __name__ == "__main__":
    S = setup()
    cmd = sys.argv[1]
    if cmd in ("e20", "all"):
        run_e20(S)
    if cmd in ("e22", "all"):
        run_e22(S)
    if cmd in ("e24", "all"):
        run_e24(S)
