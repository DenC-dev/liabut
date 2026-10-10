"""Posterior probabilities of the key splits in the unconstrained MrBayes run (A2.4), from unconstrained.parts and
unconstrained.tstat. A clade counts as present when its taxa form one side of a split (trees are unrooted).

    python3 src/16_posterior.py
"""
import importlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import RES  # noqa: E402

bayes = importlib.import_module("09_bayes")
OUT = os.path.join(RES, "bayes")
T = bayes.BAYES_TAXA
LI = ["idat1237-cribas", "laka1255"]
NCT = ["mamb1306-Slete", "kema1243-kaila", "tuku1254"]
ET = ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"]
CLADES = {
    "Ramelaic (Hull): Nuclear Central Timor + Lakalei-Idate": NCT + LI,
    "Central Timor with Welaun (Edwards; G&E)": bayes.CT,
    "Central Timor with Welaun + Lakalei-Idate": bayes.CT + LI,
    "Nuclear Central Timor (no Welaun)": NCT,
    "Lakalei-Idate": LI,
    "Timor-Babar (Edwards; G&E)": bayes.TB,
    "Eastern Timor + Lakalei-Idate (G&E, possible)": ET + LI,
    "Eastern Timor (G&E)": ET,
    "Welaun + Tetun (Hull 1998)": ["west2547-welaun", "tetu1245-suai"],
    "Southern Tetun + Central Timor with Welaun + Lakalei-Idate": ["tetu1245-suai"] + bayes.CT + LI,
    "Kawaimina (Midiki, Waima'a, Naueti)": ["midi1237", "waim1252", "naue1237"],
}


def main():
    parts = {}
    for line in open(os.path.join(OUT, "unconstrained.parts")):
        m = re.match(r"\s*(\d+)\s+([.*]+)\s*$", line)
        if m:
            parts[m.group(1)] = m.group(2)
    prob = {}
    for line in open(os.path.join(OUT, "unconstrained.tstat")):
        p = line.split()
        if p and p[0].isdigit():
            prob[p[0]] = (float(p[2]), int(float(p[1])))
    n = len(T)
    splits = {}
    for pid, s in parts.items():
        on = frozenset(i for i, c in enumerate(s) if c == "*")
        splits[on] = prob.get(pid, (1.0, None))[0] if len(on) not in (1, n - 1) else 1.0
    out = {}
    for name, taxa in CLADES.items():
        idx = frozenset(T.index(t) for t in taxa)
        comp = frozenset(range(n)) - idx
        out[name] = round(max(splits.get(idx, 0.0), splits.get(comp, 0.0)), 3)
    json.dump(out, open(os.path.join(OUT, "posterior_clades.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
