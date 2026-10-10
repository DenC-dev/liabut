"""Step 7: Bayesian constraint tests with MrBayes 3.2.7a (PROTOCOL.md section 7, as implemented by Addendum 2).

Binary cognate presence/absence (D1, LexStat, primary data) for 24 lects (one per language; see BAYES_TAXA),
restriction data with coding=noabsencesites, gamma rate variation, unrooted, Flores-Lembata as outgroup.
Each contrast is run twice, with the clade forced (positive constraint) and forbidden (negative constraint);
marginal likelihoods come from stepping-stone sampling. ln BF = lnML(positive) - lnML(negative).

    python3 src/09_bayes.py nexus            # write the matrix
    python3 src/09_bayes.py run NAME [NAME]  # run analyses (unconstrained, c1pos, c1neg, ...)
    python3 src/09_bayes.py summarize
"""
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict

from common import RES
from pipeline import variant_rows

MB = os.environ.get("MRBAYES", "mb")
OUT = os.path.join(RES, "bayes")

BAYES_TAXA = ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun", "idat1237-cribas", "laka1255",
              "tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237", "galo1243", "dadu1237", "funa1237",
              "koto1251", "term1237", "dela1252", "ilma1240", "kaha1239", "kisa1266", "luan1264", "tela1241",
              "lama1277-lewoi", "sika1262-hewa"]
OUTGROUP = ["lama1277-lewoi", "sika1262-hewa"]
CT = ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun"]
RAMELAIC = ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "idat1237-cribas", "laka1255"]
TB = [t for t in BAYES_TAXA if t not in CT + OUTGROUP]

# name -> (constraint taxa, positive?)
ANALYSES = {
    "unconstrained": (None, None),
    "c1pos": (RAMELAIC, True), "c1neg": (RAMELAIC, False),   # C1: Hull's Ramelaic
    "c2pos": (CT, True), "c2neg": (CT, False),               # C2: Edwards's Central Timor (with Welaun)
    "tbpos": (TB, True), "tbneg": (TB, False),               # Timor-Babar excludes Central Timor
}
SS = dict(ngen=5000000, nsteps=50, alpha=0.4, samplefreq=500, burninss=-1, diagnfreq=50000)
MCMC = dict(ngen=2000000, samplefreq=1000, diagnfreq=50000)


def tx(t):
    return re.sub(r"[^A-Za-z0-9_]", "_", t)


def matrix():
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if r["Lect_ID"] in BAYES_TAXA]
    attested = defaultdict(set)
    sets = defaultdict(set)
    concept_of = {}
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        sets[r["Cognateset_ID"]].add(r["Lect_ID"])
        concept_of[r["Cognateset_ID"]] = r["Concept_ID"]
    chars = sorted(sets, key=lambda s: (concept_of[s], s))
    data = {}
    for t in BAYES_TAXA:
        data[t] = "".join(("1" if t in sets[s] else "0") if concept_of[s] in attested[t] else "?" for s in chars)
    return data, chars, concept_of


def write_nexus():
    os.makedirs(OUT, exist_ok=True)
    data, chars, concept_of = matrix()
    with open(os.path.join(OUT, "matrix.nex"), "w") as fh:
        fh.write("#NEXUS\nbegin data;\n")
        fh.write(f"  dimensions ntax={len(data)} nchar={len(chars)};\n")
        fh.write("  format datatype=restriction missing=? gap=-;\n  matrix\n")
        for t, s in data.items():
            fh.write(f"    {tx(t):24s} {s}\n")
        fh.write("  ;\nend;\n")
    with open(os.path.join(OUT, "characters.csv"), "w") as fh:
        fh.write("Index,Cognateset_ID,Concept_ID\n")
        for i, c in enumerate(chars, 1):
            fh.write(f"{i},{c},{concept_of[c]}\n")
    print(f"matrix: {len(data)} taxa, {len(chars)} characters")


def mb_block(name, seed=1234):
    taxa, pos = ANALYSES[name]
    lines = ["begin mrbayes;", "  set autoclose=yes nowarn=yes seed=%d swapseed=%d;" % (seed, seed + 1),
             "  execute matrix.nex;",
             "  outgroup %s;" % tx(OUTGROUP[0]),
             "  lset coding=noabsencesites rates=gamma;",
             "  prset brlenspr=unconstrained:exp(10.0);"]
    if taxa:
        kind = "" if pos else " negative"
        lines.append(f"  constraint con{kind} = {' '.join(tx(t) for t in taxa)};")
        lines.append("  prset topologypr=constraints(con);")
    if name == "unconstrained":
        m = MCMC
        lines.append(f"  mcmcp ngen={m['ngen']} samplefreq={m['samplefreq']} diagnfreq={m['diagnfreq']} "
                     f"nruns=2 nchains=2 printfreq=100000 filename={name};")
        lines.append("  mcmc;")
        lines.append(f"  sumt filename={name} burnin=1000 contype=allcompat;")
        lines.append(f"  sump filename={name} burnin=1000;")
    else:
        s = SS
        lines.append(f"  ss ngen={s['ngen']} nsteps={s['nsteps']} alpha={s['alpha']} samplefreq={s['samplefreq']} "
                     f"burninss={s['burninss']} diagnfreq={s['diagnfreq']} nruns=2 nchains=1 printfreq=200000 "
                     f"filename={name};")
    lines += ["end;", ""]
    return "\n".join(lines)


def run(name):
    path = os.path.join(OUT, f"{name}.nex")
    open(path, "w").write(mb_block(name))
    t0 = time.time()
    with open(os.path.join(OUT, f"{name}.log"), "w") as log:
        subprocess.run([MB, f"{name}.nex"], cwd=OUT, stdout=log, stderr=subprocess.STDOUT, check=False)
    print(name, f"{(time.time() - t0) / 60:.1f} min", flush=True)


def ss_marginal(name):
    """Mean marginal likelihood over runs, from the MrBayes log."""
    txt = open(os.path.join(OUT, f"{name}.log"), errors="ignore").read()
    m = re.search(r"Marginal likelihood \(ln\)\s*\n(.*?)-{20,}\n\s*Mean:\s*(-?[\d.]+)", txt, re.S)
    runs = re.findall(r"^\s*(\d+)\s+(-?\d+\.\d+)\s*$", m.group(1), re.M) if m else []
    return (float(m.group(2)) if m else None), [float(v) for _, v in runs]


def summarize():
    out = {}
    for n in ANALYSES:
        if n == "unconstrained" or not os.path.exists(os.path.join(OUT, f"{n}.log")):
            continue
        mean, runs = ss_marginal(n)
        out[n] = dict(lnML=mean, runs=runs)
    res = {}
    for c, label in (("c1", "C1: Ramelaic (Hull) forced vs forbidden"),
                     ("c2", "C2: Central Timor incl. Welaun (Edwards) forced vs forbidden"),
                     ("tb", "Timor-Babar excluding Central Timor forced vs forbidden")):
        p, n = out.get(f"{c}pos", {}).get("lnML"), out.get(f"{c}neg", {}).get("lnML")
        if p is not None and n is not None:
            res[c] = dict(test=label, lnML_pos=p, lnML_neg=n, lnBF_pos_minus_neg=round(p - n, 2),
                          verdict=("strong for forced" if p - n >= 5 else "strong against" if n - p >= 5 else "not strong"))
    json.dump(dict(marginals=out, contrasts=res, ss_settings=SS, taxa=BAYES_TAXA),
              open(os.path.join(OUT, "bayes_factors.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "nexus":
        write_nexus()
    elif cmd == "run":
        for n in sys.argv[2:]:
            run(n)
    elif cmd == "summarize":
        summarize()
