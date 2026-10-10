"""Post hoc analyses of Addendum 3 (A3.2-A3.4): E2b diagnostic words, E5 geography, E6 maximum likelihood.

    python3 src/15_post_hoc.py e2b|e5|e6
"""
import json
import math
import os
import re
import subprocess
import sys
from collections import defaultdict

import numpy as np

from common import DATA, REF, RES, UP, ned, read_csv, sca_string, write_csv

EXP = os.path.join(RES, "exploratory")
IQ = os.environ.get("IQTREE", "iqtree2")


# ------------------------------------------------------------------------------------------------- E2b
SHOW = [("mamb1306-Slete", "Mambae"), ("kema1243-kaila", "Kemak"), ("tuku1254", "Tokodede"),
        ("tetu1246", "Tetun Dili"), ("tetu1245-suai", "S. Tetun")]
FOCUS = {"idat1237": "Idate", "idat1237-cribas": "Idate (Cribas)", "laka1255": "Lakalei",
         "west2547-welaun": "Welaun", "west2547-mahein": "Welaun (Mahein)"}


def e2b():
    det = read_csv(os.path.join(EXP, "e2_reflexes_allconcepts.csv"))
    forms = defaultdict(list)
    for r in read_csv(os.path.join(UP, "lexirumah", "cldf", "forms.csv")):
        if r["Segments"]:
            forms[(r["Lect_ID"], r["Concept_ID"])].append(r["Segments"].split())
    rows = []
    for d in det:
        if d["Lect_ID"] not in FOCUS:
            continue
        own = d["Form"]
        own_toks = None
        for t in forms[(d["Lect_ID"], d["Concept_ID"])]:
            if "".join(x for x in t if x not in "+_") == own:
                own_toks = [x for x in t if x not in "+_"]
        tet = [t for lid in ("tetu1246", "tetu1245-suai") for t in forms[(lid, d["Concept_ID"])]]
        shaped = False
        if own_toks and len(own_toks) >= 3:
            s = sca_string(own_toks)
            shaped = any(ned(s, sca_string([x for x in t if x not in "+_"])) <= 0.20 for t in tet)
        row = dict(Lect=FOCUS[d["Lect_ID"]], Concept=d["Concept_ID"], PMP="*" + d["PMP"], Target="*" + d["Target"],
                   Form=own, Reflex=d["Reflex"], Class=d["Class"], Tetun_Shaped=shaped)
        for lid, name in SHOW:
            row[name] = " ~ ".join("".join(x for x in t if x not in "+_") for t in forms[(lid, d["Concept_ID"])][:2])
        rows.append(row)
    rows.sort(key=lambda r: (r["Target"], r["Concept"], r["Lect"]))
    write_csv(os.path.join(EXP, "e2b_diagnostic_words.csv"), rows)
    summ = defaultdict(lambda: defaultdict(int))
    for r in rows:
        key = ("Idate+Lakalei" if r["Lect"].startswith(("Idate", "Lakalei")) else "Welaun")
        tag = f"{r['Target']} {r['Class']} {'tetun-shaped' if r['Tetun_Shaped'] else 'native'}"
        summ[key][tag] += 1
    out = {k: dict(v) for k, v in summ.items()}
    json.dump(out, open(os.path.join(EXP, "e2b_summary.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


# ------------------------------------------------------------------------------------------------- E5
def haversine(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def e5():
    lects = read_csv(os.path.join(DATA, "d1", "lects.csv"))
    timor = [l for l in lects if l["Role"] == "Timor AN"]
    pos = {l["ID"]: (float(l["Latitude"]), float(l["Longitude"])) for l in timor}
    grp = {l["ID"]: l["Group"] for l in timor}
    D = {}
    with open(os.path.join(RES, "distances", "d1_lexstat_primary.csv")) as fh:
        head = fh.readline().strip().split(",")[1:]
        for line in fh:
            p = line.strip().split(",")
            for j, v in enumerate(p[1:]):
                D[(p[0], head[j])] = float(v)
    ids = [l["ID"] for l in timor]
    pairs = [(a, b) for i, a in enumerate(ids) for b in ids[i + 1:]]
    x = np.array([math.log(max(haversine(pos[a], pos[b]), 1.0)) for a, b in pairs])
    y = np.array([D[(a, b)] for a, b in pairs])
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    sd = res.std()
    r = float(np.corrcoef(x, y)[0, 1])
    LI = {"Idate", "Lakalei"}
    agg = defaultdict(list)
    for (a, b), e, km, dd in zip(pairs, res, np.exp(x), y):
        ga, gb = grp[a], grp[b]
        if (ga in LI) != (gb in LI):
            other = gb if ga in LI else ga
            agg[other].append((e / sd, km, dd))
        if ga == "Welaun" or gb == "Welaun":
            other = gb if ga == "Welaun" else ga
            if other != "Welaun":
                agg["Welaun→" + other].append((e / sd, km, dd))
    out = [dict(Pair=("Lakalei-Idate → " + k) if not k.startswith("Welaun") else k.replace("→", " → "),
                Pairs=len(v), Mean_km=round(float(np.mean([t[1] for t in v])), 1),
                Mean_distance=round(float(np.mean([t[2] for t in v])), 3),
                Mean_std_residual=round(float(np.mean([t[0] for t in v])), 2))
           for k, v in sorted(agg.items())]
    write_csv(os.path.join(EXP, "e5_geography_residuals.csv"), out)
    json.dump(dict(intercept=round(float(coef[0]), 4), slope_per_log_km=round(float(coef[1]), 4), r=round(r, 3),
                   pairs=len(pairs)), open(os.path.join(EXP, "e5_model.json"), "w"), indent=1)
    print(f"r(log km, distance) = {r:.3f}; slope {coef[1]:.4f}")
    for o in out:
        print(o)


# ------------------------------------------------------------------------------------------------- E6
def tx(t):
    return re.sub(r"[^A-Za-z0-9_]", "_", t)


def e6():
    sys.path.insert(0, os.path.dirname(__file__))
    import importlib
    bayes = importlib.import_module("09_bayes")
    out = os.path.join(RES, "ml")
    os.makedirs(out, exist_ok=True)
    data, chars, _ = bayes.matrix()
    with open(os.path.join(out, "matrix.phy"), "w") as fh:
        fh.write(f"{len(data)} {len(chars)}\n")
        for t, s in data.items():
            fh.write(f"{tx(t)} {s}\n")
    T = [tx(t) for t in bayes.BAYES_TAXA]
    CT = [tx(t) for t in bayes.CT]
    LI = [tx("idat1237-cribas"), tx("laka1255")]
    NCT = [x for x in CT if x != tx("west2547-welaun")]
    OUTG = [tx(t) for t in bayes.OUTGROUP]
    ET = [tx(t) for t in ("tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237")]
    TB = [x for x in T if x not in CT + OUTG]
    cons = {"ramelaic": NCT + LI, "central_timor": CT, "ct_plus_li": CT + LI, "timor_babar": TB,
            "li_eastern_timor": LI + ET}
    base = [IQ, "-s", "matrix.phy", "-st", "BIN", "-m", "GTR2+FO+G4", "-T", "1", "-seed", "1234", "-redo", "-quiet"]
    subprocess.run(base + ["-B", "1000", "-pre", "free"], cwd=out, check=True)
    for name, clade in cons.items():
        rest = [x for x in T if x not in clade]
        open(os.path.join(out, f"{name}.constr"), "w").write(f"(({','.join(clade)}),{','.join(rest)});\n")
        subprocess.run(base + ["-g", f"{name}.constr", "-pre", name], cwd=out, check=True)
    names = ["free"] + list(cons)
    with open(os.path.join(out, "candidates.trees"), "w") as fh:
        for n in names:
            fh.write(open(os.path.join(out, f"{n}.treefile")).read().strip() + "\n")
    subprocess.run(base + ["-z", "candidates.trees", "-n", "0", "-zb", "10000", "-au", "-pre", "au"], cwd=out,
                   check=True)
    txt = open(os.path.join(out, "au.iqtree")).read()
    block = txt.split("USER TREES")[1]
    rows = []
    for line in block.splitlines():
        m = re.match(r"\s*(\d+)\s+(-?\d+\.\d+)\s+(\d+\.?\d*)\s+(.*)$", line)
        if m:
            vals = re.findall(r"(-?\d+\.?\d*(?:e-?\d+)?)\s*([+-])?", m.group(4))
            rows.append(dict(Tree=names[int(m.group(1)) - 1], logL=float(m.group(2)), deltaL=float(m.group(3)),
                             raw=m.group(4).strip()))
    lnl = {n: float(re.search(r"Log-likelihood of the tree:\s*(-?\d+\.\d+)",
                              open(os.path.join(out, f"{n}.iqtree")).read()).group(1)) for n in names}
    write_csv(os.path.join(out, "au_test.csv"), rows)
    json.dump(dict(logL=lnl, au_rows=rows), open(os.path.join(out, "summary.json"), "w"), indent=1)
    print(json.dumps(lnl, indent=1))
    for r in rows:
        print(r)


if __name__ == "__main__":
    {"e2b": e2b, "e5": e5, "e6": e6}[sys.argv[1]]()
