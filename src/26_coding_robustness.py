"""E15 (Addendum 6): does the C1 result depend on cognate coding? After Kaiping and Klamer (2022), D2-D4.

    python3 src/26_coding_robustness.py cognates   # LexStat at thresholds 0.35 and 0.75 (about 7 minutes)
    python3 src/26_coding_robustness.py trees      # 24-taxon ML trees for each coding
    python3 src/26_coding_robustness.py fit        # diagnostic: Mantel r of each coding against ABVD experts

Codings: lexstat035, lexstat075 (new), sca (step 2), biglexstat (LexiRumah's own automatic cognates), and the
primary lexstat (0.55) for reference. Writes results/literature/e15_coding_robustness.json.
"""
import copy
import importlib
import json
import os
import random
import subprocess
import sys
import time
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, RES, SEED, read_csv, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

bayes = importlib.import_module("09_bayes")
te = importlib.import_module("20_total_evidence")
OUT = os.path.join(RES, "literature", "e15")
IQ = os.environ.get("IQTREE", "iqtree2")
CODINGS = ["lexstat", "lexstat035", "lexstat075", "sca", "biglexstat"]


def cognates():
    from lingpy import LexStat
    forms = read_csv(os.path.join(DATA, "d1", "forms.csv"))
    D = {0: ["doculect", "concept", "ipa", "tokens", "formid"]}
    for i, r in enumerate(forms, 1):
        toks = r["Segments"].split()
        D[i] = [r["Lect_ID"], r["Concept_ID"], "".join(toks), toks, r["ID"]]
    random.seed(SEED)
    np.random.seed(SEED)
    t0 = time.time()
    lex = LexStat(copy.deepcopy(D), check=False)
    lex.get_scorer(runs=1000)
    for thr, tag in ((0.35, "lexstat035"), (0.75, "lexstat075")):
        ref = f"cog{tag}"
        lex.cluster(method="lexstat", threshold=thr, cluster_method="infomap", ref=ref)
        out = [dict(Form_ID=lex[k, "formid"], Lect_ID=lex[k, "doculect"], Concept_ID=lex[k, "concept"],
                    Cognateset_ID=f"{lex[k, 'concept']}-{lex[k, ref]}") for k in lex]
        write_csv(os.path.join(RES, "cognates", f"d1_{tag}.csv"), out)
        print(tag, len(out), "forms", len({o["Cognateset_ID"] for o in out}), "sets", f"{time.time() - t0:.0f}s",
              flush=True)


def matrix(method):
    rows = [r for r in variant_rows("d1", method, "primary") if r["Lect_ID"] in bayes.BAYES_TAXA]
    attested, sets, concept_of = defaultdict(set), defaultdict(set), {}
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        sets[r["Cognateset_ID"]].add(r["Lect_ID"])
        concept_of[r["Cognateset_ID"]] = r["Concept_ID"]
    chars = sorted(sets, key=lambda s: (concept_of[s], s))
    return {t: "".join(("1" if t in sets[s] else "0") if concept_of[s] in attested[t] else "?" for s in chars)
            for t in bayes.BAYES_TAXA}, len(chars)


def trees():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for m in CODINGS:
        data, n = matrix(m)
        with open(os.path.join(OUT, f"lex_{m}.phy"), "w") as fh:
            fh.write(f"{len(data)} {n}\n")
            for t, s in data.items():
                fh.write(f"{te.tx(t)} {s}\n")
        subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000", "-s", f"lex_{m}.phy",
                        "-m", "GTR2+FO+G4", "-pre", f"lex_{m}"], cwd=OUT, check=True)
        res[m] = dict(characters=n, support=te.support_from_splits(os.path.join(OUT, f"lex_{m}.splits.nex")))
        print(m, json.dumps(res[m], ensure_ascii=False), flush=True)
    json.dump(res, open(os.path.join(RES, "literature", "e15_coding_robustness.json"), "w"), indent=1,
              ensure_ascii=False)


def expert_fit():
    """Diagnostic, not pre-declared: how well each coding's distances match ABVD expert distances (step 4's G4)."""
    from pipeline import build
    ka = importlib.import_module("06_known_answers")
    from common import REF
    l2, d2 = (lambda b: (b["lects"], b["d"]))(build("d2", "expert", "primary"))
    pairs = [(r["ABVD_ID"], r["LexiRumah_ID"]) for r in read_csv(os.path.join(REF, "lect_map.csv"))]
    out = {}
    for m in CODINGS:
        b = build("d1", m, "primary")
        r, p, n = ka.mantel(b["d"], b["lects"], d2, l2, pairs, perms=999)
        out[m] = dict(mantel_r=round(r, 3), p=p, lects=n)
        print(m, out[m], flush=True)
    path = os.path.join(RES, "literature", "e15_coding_robustness.json")
    res = json.load(open(path))
    res["diagnostic_fit_to_ABVD_experts"] = out
    json.dump(res, open(path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    {"cognates": cognates, "trees": trees, "fit": expert_fit}[sys.argv[1]]()
