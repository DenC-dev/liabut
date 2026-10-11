"""E10 and E11 (Addendum 4): sound-change character matrix and phonology-only / total-evidence trees.

E10  one multistate character per PMP target (A4.3: also per target x position, as a sensitivity), state = majority
     reflex class in the expert atlas (derived/reflex_atlas/expert_tokens.csv), coded when >= 2 tokens.
E11  (a) IQ-TREE MK+G+ASC on E10; (b) IQ-TREE partitioned lexical (GTR2+FO+G4) + phonology (MK+G+ASC);
     (c) MrBayes total evidence (run separately: python3 src/20_total_evidence.py mrbayes).

    python3 src/20_total_evidence.py matrix|iqtree|mrbayes|summary
"""
import importlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, RES, read_csv, write_csv  # noqa: E402

bayes = importlib.import_module("09_bayes")
OUT = os.path.join(REPO, "derived", "sound_change_matrix")
TE = os.path.join(RES, "total_evidence")
IQ = os.environ.get("IQTREE", "iqtree2")
MB = os.environ.get("MRBAYES", "mb")
SYMBOLS = "0123456789ABCDEFGHIJKLMNOPQRSTUV"

TAXON_GLOTTO = {
    "mamb1306-Slete": ["mamb1306"], "kema1243-kaila": ["kema1243"], "tuku1254": ["tuku1254"],
    "west2547-welaun": ["wela1235"], "idat1237-cribas": ["idat1237"], "laka1255": ["laka1255"],
    "tetu1245-suai": ["sout2898", "tetu1245", "east2473", "nort2869"], "habu1241": ["habu1241"],
    "waim1252": ["waim1252"], "midi1237": ["kair1265"], "naue1237": ["naue1237"], "galo1243": ["galo1243", "talu1239"],
    "dadu1237": ["dadu1237"], "funa1237": ["funa1237"], "koto1251": ["koto1251"], "term1237": ["term1237"],
    "dela1252": ["dela1251"], "ilma1240": ["iliu1237"], "kaha1239": ["tugu1245"], "kisa1266": ["kisa1266"],
    "luan1264": ["luan1263"], "tela1241": ["tela1241"], "lama1277-lewoi": ["lama1277"], "sika1262-hewa": ["sika1262"],
}
LI = ["idat1237-cribas", "laka1255"]
ET = ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"]
CLADES = {
    "Lakalei-Idate + Central Timor (with Welaun)": bayes.CT + LI,
    "Timor-Babar incl. Lakalei-Idate": bayes.TB,
    "Lakalei-Idate + Eastern Timor": LI + ET,
    "Central Timor (with Welaun)": bayes.CT,
    "Nuclear Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254"],
    "Lakalei-Idate": LI,
}


def tx(t):
    return re.sub(r"[^A-Za-z0-9_]", "_", t)


def matrix(by_position=False):
    toks = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"))
    g2taxa = defaultdict(list)
    for t, gs in TAXON_GLOTTO.items():
        for g in gs:
            g2taxa[g].append(t)
    counts = defaultdict(Counter)
    for r in toks:
        if r["Class"] in ("", "other"):
            continue
        key = (r["Target"], r["Position"]) if by_position else (r["Target"],)
        for t in g2taxa.get(r["Glottocode"], []):
            counts[(t, key)][r["Class"]] += 1
    keys = sorted({k for (_, k) in counts})
    rows, chars = {t: [] for t in TAXON_GLOTTO}, []
    for k in keys:
        states = {}
        for t in TAXON_GLOTTO:
            c = counts.get((t, k))
            if c and sum(c.values()) >= 2:
                states[t] = c.most_common(1)[0][0]
        distinct = sorted(set(states.values()))
        if len(states) < 4 or len(distinct) < 2:
            continue
        code = {s: SYMBOLS[i] for i, s in enumerate(distinct)}
        chars.append(dict(Character="*" + " ".join(k), Coded_Taxa=len(states),
                          States="; ".join(f"{code[s]}={s}" for s in distinct)))
        for t in TAXON_GLOTTO:
            rows[t].append(code[states[t]] if t in states else "?")
    return rows, chars, counts


def write_matrix():
    os.makedirs(OUT, exist_ok=True)
    for tag, bp in (("by_target", False), ("by_target_position", True)):
        rows, chars, counts = matrix(bp)
        write_csv(os.path.join(OUT, f"characters_{tag}.csv"), chars)
        with open(os.path.join(OUT, f"matrix_{tag}.csv"), "w") as fh:
            fh.write("Taxon," + ",".join(c["Character"] for c in chars) + "\n")
            for t, r in rows.items():
                fh.write(t + "," + ",".join(r) + "\n")
        with open(os.path.join(OUT, f"phon_{tag}.phy"), "w") as fh:
            fh.write(f"{len(rows)} {len(chars)}\n")
            for t, r in rows.items():
                fh.write(f"{tx(t)} {''.join(r)}\n")
        coded = {t: sum(x != "?" for x in r) for t, r in rows.items()}
        print(tag, len(chars), "characters; coded per taxon:", dict(sorted(coded.items(), key=lambda x: x[1])[:6]), "...")


def lexical_phy(path):
    data, chars, _ = bayes.matrix()
    with open(path, "w") as fh:
        fh.write(f"{len(data)} {len(chars)}\n")
        for t, s in data.items():
            fh.write(f"{tx(t)} {s}\n")
    return len(chars)


def support_from_splits(splitsfile):
    """UFBoot support (%) of each clade, read from IQ-TREE's .splits.nex (independent of rooting)."""
    txt = open(splitsfile).read()
    labels = {int(i): n for i, n in re.findall(r"\[(\d+)\]\s+'?([^'\n]+)'?", txt.split("TAXLABELS")[1].split(";")[0])}
    allt = frozenset(labels.values())
    splits = {}
    body = txt.split("MATRIX")[1].split(";")[0]
    for line in body.strip().splitlines():
        m = re.match(r"\s*(\d+(?:\.\d+)?)\s+([\d\s]+),?", line)
        if m:
            side = frozenset(labels[int(i)] for i in m.group(2).split())
            w = float(m.group(1))
            splits[side] = max(w, splits.get(side, 0))
            splits[allt - side] = max(w, splits.get(allt - side, 0))
    out = {}
    for label, taxa in CLADES.items():
        want = frozenset(tx(x) for x in taxa) & allt
        out[label] = splits.get(want, 0)
    return out


def support_from_tree(treefile, outgroup=tx("lama1277-lewoi")):
    from Bio import Phylo
    t = Phylo.read(treefile, "newick")
    names = {c.name for c in t.get_terminals()}
    if outgroup not in names:
        outgroup = tx("sika1262-hewa")
    t.root_with_outgroup(outgroup)
    n = len(names)
    out = {}
    for label, taxa in CLADES.items():
        want = frozenset(tx(x) for x in taxa) & frozenset(names)
        comp = frozenset(names) - want
        val = None
        for c in t.find_clades():
            leaves = frozenset(x.name for x in c.get_terminals())
            if leaves in (want, comp) and not c.is_terminal():
                val = c.confidence
        out[label] = val if val is not None else 0
    return out


def iqtree():
    os.makedirs(TE, exist_ok=True)
    nlex = lexical_phy(os.path.join(TE, "lex.phy"))
    res = {}
    for tag in ("by_target", "by_target_position"):
        src = os.path.join(OUT, f"phon_{tag}.phy")
        dst = os.path.join(TE, f"phon_{tag}.phy")
        open(dst, "w").write(open(src).read())
        base = [IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000"]
        subprocess.run(base + ["-s", f"phon_{tag}.phy", "-st", "MORPH", "-m", "MK+G+ASC", "-pre", f"phon_{tag}"],
                       cwd=TE, check=True)
        nphon = int(open(dst).readline().split()[1])
        open(os.path.join(TE, f"te_{tag}.nex"), "w").write(
            "#nexus\nbegin sets;\n"
            f"  charset lex = lex.phy: 1-{nlex};\n"
            f"  charset phon = phon_{tag}.phy: 1-{nphon};\n"
            "  charpartition mine = GTR2+FO+G4:lex, MK+G+ASC:phon;\nend;\n")
        subprocess.run(base + ["-p", f"te_{tag}.nex", "-pre", f"te_{tag}"], cwd=TE, check=True)
        res[tag] = dict(characters=nphon,
                        phonology_only=support_from_splits(os.path.join(TE, f"phon_{tag}.splits.nex")),
                        total_evidence_ML=support_from_splits(os.path.join(TE, f"te_{tag}.splits.nex")))
    subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000", "-s", "lex.phy",
                    "-m", "GTR2+FO+G4", "-pre", "lex_only"], cwd=TE, check=True)
    res["lexical_only_ML"] = support_from_splits(os.path.join(TE, "lex_only.splits.nex"))
    json.dump(res, open(os.path.join(TE, "iqtree_support.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


def mrbayes(tag="by_target"):
    os.makedirs(TE, exist_ok=True)
    data, lchars, _ = bayes.matrix()
    rows, pchars, _ = matrix(tag == "by_target_position")
    nl, npn = len(lchars), len(pchars)
    with open(os.path.join(TE, f"te_{tag}.mb.nex"), "w") as fh:
        fh.write("#NEXUS\nbegin data;\n")
        fh.write(f"  dimensions ntax={len(data)} nchar={nl + npn};\n")
        fh.write(f"  format datatype=mixed(restriction:1-{nl},standard:{nl + 1}-{nl + npn}) missing=? gap=-;\n  matrix\n")
        for t in TAXON_GLOTTO:
            fh.write(f"    {tx(t):24s} {data[t]}{''.join(rows[t])}\n")
        fh.write("  ;\nend;\n")
        fh.write("begin mrbayes;\n  set autoclose=yes nowarn=yes seed=1234 swapseed=1235;\n")
        fh.write(f"  charset lex = 1-{nl};\n  charset phon = {nl + 1}-{nl + npn};\n")
        fh.write("  partition by_type = 2: lex, phon;\n  set partition = by_type;\n")
        fh.write(f"  outgroup {tx('lama1277-lewoi')};\n")
        fh.write("  lset applyto=(1) coding=noabsencesites rates=gamma;\n")
        fh.write("  lset applyto=(2) coding=variable rates=gamma;\n")
        fh.write("  unlink shape=(all) pinvar=(all) statefreq=(all);\n  prset applyto=(all) ratepr=variable;\n")
        fh.write("  prset brlenspr=unconstrained:exp(10.0);\n")
        fh.write(f"  mcmcp ngen=2000000 samplefreq=1000 diagnfreq=50000 nruns=2 nchains=2 printfreq=100000 "
                 f"filename=te_{tag};\n  mcmc;\n  sumt filename=te_{tag} contype=allcompat;\n"
                 f"  sump filename=te_{tag};\nend;\n")
    with open(os.path.join(TE, f"te_{tag}.mb.log"), "w") as log:
        subprocess.run([MB, f"te_{tag}.mb.nex"], cwd=TE, stdout=log, stderr=subprocess.STDOUT, check=False)


def posterior(prefix):
    parts, prob = {}, {}
    for line in open(os.path.join(TE, f"{prefix}.parts")):
        m = re.match(r"\s*(\d+)\s+([.*]+)\s*$", line)
        if m:
            parts[m.group(1)] = m.group(2)
    for line in open(os.path.join(TE, f"{prefix}.tstat")):
        p = line.split()
        if p and p[0].isdigit():
            prob[p[0]] = float(p[2])
    taxa = list(TAXON_GLOTTO)
    n = len(taxa)
    splits = {frozenset(i for i, c in enumerate(s) if c == "*"): prob.get(pid, 0.0) for pid, s in parts.items()}
    out = {}
    for label, members in CLADES.items():
        idx = frozenset(taxa.index(t) for t in members)
        comp = frozenset(range(n)) - idx
        out[label] = round(max(splits.get(idx, 0.0), splits.get(comp, 0.0)), 3)
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "matrix":
        write_matrix()
    elif cmd == "iqtree":
        iqtree()
    elif cmd == "supports":  # re-read supports from existing IQ-TREE outputs
        res = {}
        for tag in ("by_target", "by_target_position"):
            res[tag] = dict(characters=int(open(os.path.join(TE, f"phon_{tag}.phy")).readline().split()[1]),
                            phonology_only=support_from_splits(os.path.join(TE, f"phon_{tag}.splits.nex")),
                            total_evidence_ML=support_from_splits(os.path.join(TE, f"te_{tag}.splits.nex")))
        res["lexical_only_ML"] = support_from_splits(os.path.join(TE, "lex_only.splits.nex"))
        res["E6_free_tree_check"] = support_from_splits(os.path.join(RES, "ml", "free.splits.nex"))
        json.dump(res, open(os.path.join(TE, "iqtree_support.json"), "w"), indent=1)
        print(json.dumps(res, indent=1))
    elif cmd == "mrbayes":
        mrbayes(sys.argv[2] if len(sys.argv) > 2 else "by_target")
    elif cmd == "summary":
        res = {tag: posterior(f"te_{tag}") for tag in ("by_target",) if os.path.exists(os.path.join(TE, f"te_{tag}.tstat"))}
        json.dump(res, open(os.path.join(TE, "mrbayes_posterior.json"), "w"), indent=1)
        print(json.dumps(res, indent=1))
