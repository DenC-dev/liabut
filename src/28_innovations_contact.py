"""Addendum 7: separating inheritance from contact.

E17  shared lexical innovations (cognate sets that replaced the PMP word), with a geography control
E18  triplet site-pattern test for contact (lexical analogue of ABBA-BABA), with a Welaun known-answer check

    python3 src/28_innovations_contact.py
Writes results/literature/e17_*.{json,csv}, e18_triplets.json and derived/innovations/cognate_set_status.csv.
"""
import importlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, UP, ned, read_csv, sca_string, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

ra = importlib.import_module("19_reflex_atlas")
ex = importlib.import_module("10_exploratory")
clf = importlib.import_module("35_classifier")
RULE = clf.chosen_rule()   # R0 unless RETENTION_RULE=chosen (E30)
SUF = "" if RULE["kind"] == "R0" else "_" + RULE["kind"].lower()
LIT = os.path.join(RES, "literature")
DER = os.path.join(REPO, "derived", "innovations")

LI = ["idat1237", "idat1237-cribas", "laka1255"]
GROUP_OF = {"Mambae": "CT", "Kemak": "CT", "Tokodede": "CT", "Welaun": "CT", "Tetun": "Tetun", "Habu": "Habu",
            "Kawaimina": "Kawaimina", "Galoli": "Galoli", "Idate": "LI", "Lakalei": "LI"}
# E18 taxa (step-7 representatives)
T = {"LI": ["idat1237-cribas", "laka1255"], "NCT": ["mamb1306-Slete", "kema1243-kaila", "tuku1254"],
     "Welaun": ["west2547-welaun"], "Tetun": ["tetu1245-suai"], "Habu": ["habu1241"],
     "Kawaimina": ["waim1252", "midi1237", "naue1237"], "Galoli": ["galo1243"]}
TRIPLETS = [("Welaun", "NCT", "Tetun"),                      # known-answer check
            ("LI", "NCT", "Tetun"), ("LI", "NCT", "Habu"), ("LI", "NCT", "Kawaimina"), ("LI", "NCT", "Galoli"),
            ("LI", "Tetun", "Habu")]


def pmp_forms():
    abvd = os.path.join(UP, "abvd", "cldf")
    P = {r["ID"]: str(r["Concepticon_ID"]).split(".")[0] for r in read_csv(os.path.join(abvd, "parameters.csv"))}
    out = defaultdict(list)
    for r in read_csv(os.path.join(abvd, "forms.csv")):
        if r["Language_ID"] == "269" and P.get(r["Parameter_ID"]) not in (None, "", "None"):
            for alt in re.split(r"[/,]", r["Value"]):
                toks = ra.clean_pmp(alt)
                if toks:
                    out[P[r["Parameter_ID"]]].append(toks)
    return out


def classify():
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    concepts = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"] for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    pmp = pmp_forms()
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if lects[r["Lect_ID"]]["Role"] != "TAP"
            and pmp.get(concepts.get(r["Concept_ID"]))]
    members = defaultdict(list)
    for r in rows:
        members[r["Cognateset_ID"]].append(r)
    status = {}
    glotto = {k: v["Glottocode"] for k, v in lects.items()}
    for sid, rs in members.items():
        ps = pmp[concepts[rs[0]["Concept_ID"]]]
        if RULE["kind"] == "R0":
            best = min(ned(sca_string(p), sca_string(segs[r["Form_ID"]])) for p in ps for r in rs
                       if segs[r["Form_ID"]])
            status[sid] = "retention" if best <= 0.5 else "innovation"
        else:
            status[sid] = clf.set_status([(r["Lect_ID"], segs[r["Form_ID"]]) for r in rs], ps, RULE, glotto)
    os.makedirs(DER, exist_ok=True)
    write_csv(os.path.join(DER, f"cognate_set_status{SUF}.csv"),
              [dict(Cognateset_ID=s, Concept_ID=members[s][0]["Concept_ID"], Status=status[s],
                    Lects=" ".join(sorted({r["Lect_ID"] for r in members[s]})),
                    Forms="; ".join(f"{r['Lect_ID']}:{''.join(segs[r['Form_ID']])}" for r in members[s]))
               for s in sorted(members)])
    return lects, rows, members, status, segs


def group(lects, lid):
    if lid in LI:
        return "LI"
    return GROUP_OF.get(lects[lid]["Group"], "other")


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [float(a["Latitude"]), float(a["Longitude"]),
                                            float(b["Latitude"]), float(b["Longitude"])])
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def e17(lects, rows, members, status, segs, stable):
    # (i) exclusive innovations containing LI
    cls = Counter()
    by_stratum = defaultdict(Counter)
    inventory = []
    for sid, rs in members.items():
        if status[sid] != "innovation":
            continue
        ls = {r["Lect_ID"] for r in rs}
        if not ls & set(LI):
            continue
        others = {group(lects, l) for l in ls if l not in LI}
        if not others:
            c = "LI only"
        elif len(others) == 1:
            c = "LI + " + next(iter(others))
        elif others <= {"Tetun", "Habu", "Kawaimina"}:
            c = "LI + several Eastern Timor"
        else:
            c = "LI + mixed"
        cls[c] += 1
        cid = rs[0]["Concept_ID"]
        by_stratum["stable" if cid in stable else "other"][c] += 1
        if c != "LI only" and c != "LI + mixed":
            inventory.append(dict(Class=c, Concept_ID=cid, Stable=cid in stable, Cognateset_ID=sid,
                                  Forms="; ".join(f"{lects[r['Lect_ID']]['Name']}: {''.join(segs[r['Form_ID']])}"
                                                  for r in rs)))
    inventory.sort(key=lambda x: (x["Class"], x["Concept_ID"]))
    write_csv(os.path.join(LIT, f"e17_exclusive_innovations{SUF}.csv"), inventory)
    # (ii) per-lect sharing rate with LI, against distance
    sets_of = defaultdict(set)   # (lect, concept) -> innovation sets
    attested = defaultdict(set)
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        if status[r["Cognateset_ID"]] == "innovation":
            sets_of[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    out_rows = []
    for L, info in lects.items():
        if L in LI or info["Role"] not in ("Timor AN", "Outgroup AN"):
            continue
        rec = dict(Lect=L, Name=info["Name"], Group=group(lects, L))
        for stratum, keep in (("all", None), ("stable", stable)):
            rates, dists = [], []
            for li in LI:
                common = attested[li] & attested[L]
                if keep is not None:
                    common &= keep
                if len(common) < 10:
                    continue
                shared = sum(1 for c in common if sets_of[(li, c)] & sets_of[(L, c)])
                rates.append(shared / len(common))
                dists.append(km(lects[li], info))
            rec[f"rate_{stratum}"] = round(float(np.mean(rates)), 4) if rates else None
            rec["km"] = round(float(np.mean(dists)), 1) if dists else None
        out_rows.append(rec)
    res = dict(exclusive_counts=dict(cls), exclusive_by_stratum={k: dict(v) for k, v in by_stratum.items()})
    for stratum in ("all", "stable"):
        pts = [r for r in out_rows if r[f"rate_{stratum}"] is not None and r["km"]]
        x = np.log([r["km"] for r in pts])
        y = np.array([r[f"rate_{stratum}"] for r in pts])
        b, a = np.polyfit(x, y, 1)
        for r, xi, yi in zip(pts, x, y):
            r[f"resid_{stratum}"] = round(float(yi - (a + b * xi)), 4)
        g = defaultdict(list)
        for r in pts:
            g[r["Group"]].append(r[f"resid_{stratum}"])
        res[f"regression_{stratum}"] = dict(slope_per_log_km=round(float(b), 4), lects=len(pts),
                                            mean_residual_by_group={k: dict(mean=round(float(np.mean(v)), 4),
                                                                            n=len(v)) for k, v in sorted(g.items())})
    write_csv(os.path.join(LIT, f"e17_sharing_rates{SUF}.csv"), sorted(out_rows, key=lambda r: -(r["rate_all"] or 0)))
    json.dump(res, open(os.path.join(LIT, f"e17_innovations{SUF}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return sets_of, attested


def e18(sets_of, attested, stable):
    out = {}
    for A, B, C in TRIPLETS:
        res_t = {}
        for stratum in ("all", "stable", "other"):
            per_concept = defaultdict(lambda: np.zeros(3))  # n_AB, n_AC, n_BC
            for a, b, c in product(T[A], T[B], T[C]):
                common = attested[a] & attested[b] & attested[c]
                for k in common:
                    if stratum == "stable" and k not in stable or stratum == "other" and k in stable:
                        continue
                    sa, sb, sc = sets_of[(a, k)], sets_of[(b, k)], sets_of[(c, k)]
                    v = per_concept[k]
                    v[0] += bool((sa & sb) - sc)
                    v[1] += bool((sa & sc) - sb)
                    v[2] += bool((sb & sc) - sa)
            M = np.array(list(per_concept.values())) if per_concept else np.zeros((0, 3))
            tot = M.sum(axis=0)
            names = [f"{A}+{B}", f"{A}+{C}", f"{B}+{C}"]
            t = int(np.argmax(tot))
            minor = [i for i in range(3) if i != t]

            def dstat(v):
                s = v[minor[0]] + v[minor[1]]
                return (v[minor[0]] - v[minor[1]]) / s if s else 0.0
            D = dstat(tot)
            m = len(M)
            jk = np.array([dstat(tot - M[i]) for i in range(m)]) if m > 1 else np.array([0.0])
            se = math.sqrt((m - 1) / m * ((jk - jk.mean()) ** 2).sum()) if m > 1 else float("nan")
            res_t[stratum] = dict(concepts=m, counts={n: int(x) for n, x in zip(names, tot)}, tree_pair=names[t],
                                  D=dict(pair_excess=f"{names[minor[0]]} vs {names[minor[1]]}", value=round(D, 3),
                                         se=round(se, 3), Z=round(D / se, 2) if se and se > 0 else None))
        out[f"({A}, {B}, {C})"] = res_t
        print(f"({A}, {B}, {C})", json.dumps(res_t, ensure_ascii=False))
    json.dump(out, open(os.path.join(LIT, f"e18_triplets{SUF}.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    os.makedirs(LIT, exist_ok=True)
    stable, _ = ex.stable_concepts()
    lects, rows, members, status, segs = classify()
    print(Counter(status.values()), "cognate sets")
    sets_of, attested = e17(lects, rows, members, status, segs, stable)
    e18(sets_of, attested, stable)
