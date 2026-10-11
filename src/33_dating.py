"""E23 (Addendum 8): relative node ages from a strict-clock MrBayes analysis of the step-7 data.
E34 (Addendum 9): the same with the 22 Timor-region taxa constrained to a clade, so the root sits on the Flores outgroup.

    python3 src/33_dating.py run [rooted]         # 2 runs x 2 chains, 2,000,000 generations (needs MrBayes: $MRBAYES or mb)
    python3 src/33_dating.py summarize [rooted]   # relative heights (root = 1) of named MRCAs, clade posteriors, LI's sister
"""
import importlib
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import RES  # noqa: E402

bayes = importlib.import_module("09_bayes")
OUT = os.path.join(RES, "literature", "e23_dating")
MB = os.environ.get("MRBAYES", "mb")
tx = bayes.tx
NODES = {
    "Lakalei-Idate": ["idat1237-cribas", "laka1255"],
    "Nuclear Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254"],
    "Central Timor (with Welaun)": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun"],
    "Lakalei-Idate + Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun",
                                      "idat1237-cribas", "laka1255"],
    "Eastern Timor (Tetun, Habu, Kawaimina)": ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"],
    "Kawaimina": ["waim1252", "midi1237", "naue1237"],
    "Rote-Meto": ["koto1251", "term1237", "dela1252"],
    "Wetar-Atauro (with Galoli)": ["galo1243", "dadu1237", "ilma1240", "kaha1239"],
    "Timor-region taxa (no Flores)": [t for t in bayes.BAYES_TAXA if t not in bayes.OUTGROUP],
}


def outdir(rooted):
    return os.path.join(RES, "literature", "e34_rooted_clock") if rooted else OUT


def run(rooted=False):
    OUT = outdir(rooted)
    os.makedirs(OUT, exist_ok=True)
    data, chars, _ = bayes.matrix()
    with open(os.path.join(OUT, "matrix.nex"), "w") as fh:
        fh.write("#NEXUS\nbegin data;\n")
        fh.write(f"  dimensions ntax={len(data)} nchar={len(chars)};\n")
        fh.write("  format datatype=restriction missing=? gap=-;\n  matrix\n")
        for t, s in data.items():
            fh.write(f"    {tx(t):24s} {s}\n")
        fh.write("  ;\nend;\n")
    block = "\n".join([
        "begin mrbayes;",
        "  set autoclose=yes nowarn=yes seed=2026 swapseed=2027;",
        "  execute matrix.nex;",
        "  lset coding=noabsencesites rates=gamma;",
        "  prset brlenspr=clock:uniform clockratepr=fixed(1.0);",
        *(["  constraint timor = " + " ".join(tx(t) for t in NODES["Timor-region taxa (no Flores)"]) + ";",
           "  prset topologypr=constraints(timor);"] if rooted else []),
        "  mcmcp ngen=2000000 samplefreq=1000 diagnfreq=50000 nruns=2 nchains=2 printfreq=200000 filename=clock;",
        "  mcmc;",
        "  sumt filename=clock burnin=500 contype=allcompat;",
        "  sump filename=clock burnin=500;",
        "end;", ""])
    open(os.path.join(OUT, "clock.nex"), "w").write(block)
    with open(os.path.join(OUT, "clock.log"), "w") as log:
        subprocess.run([MB, "clock.nex"], cwd=OUT, stdout=log, stderr=subprocess.STDOUT, check=False)


def trees(path, burnin=0.25):
    from io import StringIO

    from Bio import Phylo
    txt = open(path).read()
    trans = {}
    if "translate" in txt:
        block = txt.split("translate")[1].split(";")[0]
        for line in block.strip().splitlines():
            p = line.strip().rstrip(",").split()
            if len(p) == 2:
                trans[p[0]] = p[1]
    lines = [l for l in txt.splitlines() if l.strip().startswith("tree ")]
    lines = lines[int(len(lines) * burnin):]
    for l in lines:
        nwk = l.split("=", 1)[1].strip()
        nwk = nwk[nwk.index("("):] if "(" in nwk else nwk
        t = Phylo.read(StringIO(nwk), "newick")
        for c in t.get_terminals():
            c.name = trans.get(c.name, c.name)
        yield t


def sister_label(t, names):
    li = t.common_ancestor([names[tx(m)] for m in NODES["Lakalei-Idate"]])
    parent = t.get_path(li)[-2] if len(t.get_path(li)) > 1 else t.root
    sis = sorted(c.name for c in parent.get_terminals() if c not in li.get_terminals())
    return " + ".join(sis)


def summarize(rooted=False):
    OUT = outdir(rooted)
    heights = {k: [] for k in NODES}
    mono = {k: 0 for k in NODES}
    sisters = {}
    n = 0
    for run in (1, 2):
        for t in trees(os.path.join(OUT, f"clock.run{run}.t")):
            n += 1
            depths = t.depths()
            root_h = max(depths[c] for c in t.get_terminals())
            names = {c.name: c for c in t.get_terminals()}
            for k, members in NODES.items():
                tips = [names[tx(m)] for m in members]
                m = t.common_ancestor(tips)
                heights[k].append((root_h - depths[m]) / root_h)
                mono[k] += len(m.get_terminals()) == len(tips)
            lab = sister_label(t, names)
            sisters[lab] = sisters.get(lab, 0) + 1
    res = {k: dict(rel_height_median=round(float(np.median(v)), 3),
                   rel_height_95=[round(float(np.percentile(v, 2.5)), 3), round(float(np.percentile(v, 97.5)), 3)],
                   clade_posterior=round(mono[k] / n, 3)) for k, v in heights.items()}
    res["_samples"] = n
    res["_lakalei_idate_sister"] = {k: round(v / n, 3) for k, v in sorted(sisters.items(), key=lambda x: -x[1])[:12]}
    name = "e34_rooted_clock.json" if rooted else "e23_dating.json"
    json.dump(res, open(os.path.join(RES, "literature", name), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    {"run": run, "summarize": summarize}[sys.argv[1]](rooted=sys.argv[2:] == ["rooted"])
