"""Step 2a: automatic cognate detection (PROTOCOL.md section 3).

LexStat (threshold 0.55, Infomap, 1,000 scorer runs) and SCA (threshold 0.45, Infomap) on D1 and D2, seed 1234.
Writes results/cognates/{d1,d2}_{lexstat,sca}.csv with Form_ID, Lect_ID, Concept_ID, Cognateset_ID.

    python3 src/03_cognates.py [d1|d2]
"""
import copy
import os
import random
import sys
import time

import numpy as np
from lingpy import LexStat

from common import DATA, RES, SEED, read_csv, write_csv


def run(ds):
    forms = read_csv(os.path.join(DATA, ds, "forms.csv"))
    D = {0: ["doculect", "concept", "ipa", "tokens", "formid"]}
    for i, r in enumerate(forms, 1):
        toks = r["Segments"].split()
        D[i] = [r["Lect_ID"], r["Concept_ID"], "".join(toks), toks, r["ID"]]

    for method, thr in (("lexstat", 0.55), ("sca", 0.45)):
        random.seed(SEED)
        np.random.seed(SEED)
        t0 = time.time()
        lex = LexStat(copy.deepcopy(D), check=False)
        if method == "lexstat":
            lex.get_scorer(runs=1000)
        lex.cluster(method=method, threshold=thr, cluster_method="infomap", ref="cog")
        out = [dict(Form_ID=lex[k, "formid"], Lect_ID=lex[k, "doculect"], Concept_ID=lex[k, "concept"],
                    Cognateset_ID=f"{lex[k, 'concept']}-{lex[k, 'cog']}") for k in lex]
        write_csv(os.path.join(RES, "cognates", f"{ds}_{method}.csv"), out)
        print(ds, method, len(out), "forms", len({o['Cognateset_ID'] for o in out}), "sets",
              f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    for ds in (sys.argv[1:] or ["d2", "d1"]):
        run(ds)
