"""Addendum 12 (second round after a mock referee report): E40-E50.

    python3 src/41_addendum12.py e40code        joint LexStat coding of D1 + seven ABVD outgroups
    python3 src/41_addendum12.py e40iq          IQ-TREE (UFBoot) on the four E40 taxon sets
    python3 src/41_addendum12.py e40mb          MrBayes on the E40 primary set (long)
    python3 src/41_addendum12.py e40sum         root positions and rooted clades
    python3 src/41_addendum12.py e41 [no_tela]  relaxed clock (long)
    python3 src/41_addendum12.py e41sum
    python3 src/41_addendum12.py e42|e43|e44|e45|e46|e48|e49|e50|house
    python3 src/41_addendum12.py e47 NAME       stepping-stone run (long); e47sum
Needs IQ-TREE ($IQTREE) and MrBayes ($MRBAYES).
"""
import copy
import importlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, SEED, UP, clean_abvd, read_csv, write_csv  # noqa: E402
from pipeline import flags, variant_rows  # noqa: E402

bayes = importlib.import_module("09_bayes")
te = importlib.import_module("20_total_evidence")
a9 = importlib.import_module("34_addendum9")
ra = importlib.import_module("19_reflex_atlas")
LIT = os.path.join(RES, "literature")
IQ = os.environ.get("IQTREE", "iqtree2")
MB = os.environ.get("MRBAYES", "mb")
tx = te.tx

TAXA = list(bayes.BAYES_TAXA)
FLORES = list(bayes.OUTGROUP)
CT = list(bayes.CT)
NCT = ["mamb1306-Slete", "kema1243-kaila", "tuku1254"]
LI = ["idat1237-cribas", "laka1255"]
ET = ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"]
TB = list(bayes.TB)
RMH = ["term1237", "dela1252", "koto1251", "funa1237"]
SWM = ["kisa1266", "luan1264", "tela1241"]
OG = {"og-tagalog": ("277", "far"), "og-buginese": ("48", "far"), "og-uma": ("999", "far"),
      "og-kambera": ("32", "near"), "og-bima": ("14", "near"), "og-manggarai": ("84", "near"),
      "og-pmp": ("269", "proto")}
SETS = {"primary": list(OG), "far": [k for k, v in OG.items() if v[1] == "far"],
        "near": [k for k, v in OG.items() if v[1] == "near"], "pmp": ["og-pmp"]}
REF = {"primary": "og-tagalog", "far": "og-tagalog", "near": "og-kambera", "pmp": "og-pmp"}
W40 = os.path.join(LIT, "e40")


def indep_taxa():
    return [a9.SWAP.get(t, t) for t in TAXA if t not in a9.DROP]


# ---------------------------------------------------------------- E40 coding
def e40code():
    from lingpy import LexStat
    os.makedirs(W40, exist_ok=True)
    d1c = {}
    for c in read_csv(os.path.join(DATA, "d1", "concepts.csv")):
        d1c.setdefault(str(c["Concepticon_ID"]).split(".")[0], []).append(c["ID"])
    abvd = os.path.join(UP, "abvd", "cldf")
    P = {r["ID"]: str(r["Concepticon_ID"]).split(".")[0] for r in read_csv(os.path.join(abvd, "parameters.csv"))}
    lang = {v[0]: k for k, v in OG.items()}
    rows = []
    for r in read_csv(os.path.join(abvd, "forms.csv")):
        lid = lang.get(r["Language_ID"])
        if not lid or P.get(r["Parameter_ID"]) not in d1c:
            continue
        if str(r.get("Loan", "")).lower() in ("true", "1"):
            continue
        if lid == "og-pmp":
            alts = [ra.clean_pmp(a) for a in re.split(r"[/,]", r["Value"])]
        else:
            alts = [clean_abvd(str(r["Form"]))]
        for k, toks in enumerate(a for a in alts if a):
            for cid in d1c[P[r["Parameter_ID"]]]:
                rows.append(dict(ID=f"abvd-{r['ID']}-{k}-{cid}", Lect_ID=lid, Concept_ID=cid, Segments=" ".join(toks)))
    forms = read_csv(os.path.join(DATA, "d1", "forms.csv")) + rows
    write_csv(os.path.join(W40, "outgroup_forms.csv"), rows)
    D = {0: ["doculect", "concept", "ipa", "tokens", "formid"]}
    for i, r in enumerate(forms, 1):
        toks = r["Segments"].split()
        D[i] = [r["Lect_ID"], r["Concept_ID"], "".join(toks), toks, r["ID"]]
    random.seed(SEED)
    np.random.seed(SEED)
    t0 = time.time()
    lex = LexStat(copy.deepcopy(D), check=False)
    lex.get_scorer(runs=1000)
    lex.cluster(method="lexstat", threshold=0.55, cluster_method="infomap", ref="cog")
    out = [dict(Form_ID=lex[k, "formid"], Lect_ID=lex[k, "doculect"], Concept_ID=lex[k, "concept"],
                Cognateset_ID=f"{lex[k, 'concept']}-{lex[k, 'cog']}") for k in lex]
    write_csv(os.path.join(W40, "cognates_lexstat.csv"), out)
    print(len(out), "forms", len({o["Cognateset_ID"] for o in out}), "sets", f"{time.time() - t0:.0f}s",
          Counter(r["Lect_ID"] for r in rows))


def e40_rows():
    """Joint coding, with the D1 primary screening for D1 forms; outgroup forms unscreened."""
    fl = flags("d1")
    out = []
    for r in read_csv(os.path.join(W40, "cognates_lexstat.csv")):
        if r["Lect_ID"].startswith("og-"):
            out.append(r)
            continue
        g = fl.get(r["Form_ID"])
        if g is None or "True" in (g["L1_expert"], g["L3_indonesian"], g["L4_portuguese"]):
            continue
        out.append(r)
    return out


def write_phy(rows, taxa, path):
    """Binary presence/absence (as step 7); only sets with a member among taxa."""
    return a9.phy(rows, taxa, path)


def e40iq():
    rows = e40_rows()
    for name, og in SETS.items():
        taxa = TAXA + og
        p = os.path.join(W40, f"{name}.phy")
        n = write_phy(rows, taxa, p)
        print(name, len(taxa), "taxa", n, "characters", flush=True)
        if not os.path.exists(os.path.join(W40, f"{name}.ufboot")):
            a9.iqtree(p, name, ("-B", "1000", "-wbt"))
    # independent taxa, for E45
    p = os.path.join(W40, "indep_primary.phy")
    print("indep_primary", write_phy(rows, indep_taxa() + SETS["primary"], p))


# ---------------------------------------------------------------- reading trees
def read_trees(path, fmt="newick"):
    from Bio import Phylo
    return list(Phylo.parse(path, fmt))


def mb_done(prefix):
    return os.path.exists(prefix + ".log") and "Analysis completed" in open(prefix + ".log").read()


def mb_trees(prefix, burnin=0.25):
    """MrBayes .t files (both runs), burn-in removed. Parsed by hand so that clock comments ([&B ...]) are fine."""
    from io import StringIO
    from Bio import Phylo
    out = []
    for run in (1, 2):
        txt = open(f"{prefix}.run{run}.t").read()
        trans = dict(re.findall(r"^\s*(\d+)\s+([^,;\s]+)[,;]?\s*$", txt.split("translate")[1].split(";")[0], re.M))
        ts = []
        for line in txt.splitlines():
            line = line.strip()
            if not line.startswith("tree gen."):
                continue
            nwk = re.sub(r"\[[^\]]*\]", "", line.split("=", 1)[1]).strip()
            t = Phylo.read(StringIO(nwk), "newick")
            for c in t.get_terminals():
                c.name = trans.get(c.name, c.name)
            ts.append(t)
        out += ts[int(len(ts) * burnin):]
    return out


def reduce_root(tree, keep, ref):
    """Prune to keep + ref, root on ref; return (ingroup clades as frozensets, root split smaller side)."""
    t = copy.deepcopy(tree)
    names = {c.name for c in t.get_terminals()}
    for n in names - set(keep) - {ref}:
        t.prune(n)
    t.root_with_outgroup(ref)
    ing = [c for c in t.root.clades if not (c.is_terminal() and c.name == ref)]
    clades = set()
    for c in t.find_clades():
        if c.is_terminal() and c.name == ref:
            continue
        leaves = frozenset(x.name for x in c.get_terminals()) - {ref}
        if 1 < len(leaves):
            clades.add(leaves)
    allin = frozenset(keep)
    # root split = the bipartition of the ingroup at the root
    if len(ing) == 1:
        kids = ing[0].clades
    else:
        kids = ing
    sides = [frozenset(x.name for x in k.get_terminals()) - {ref} for k in kids]
    if len(sides) == 2:
        split = min(sides, key=len)
    else:
        split = "polytomy"
    return clades, split, allin


ROOT_CATS = [
    ("Flores pair | rest", lambda s: s == {tx(t) for t in FLORES}),
    ("Central Timor (with or without Welaun) | rest", lambda s: s in ({tx(t) for t in CT}, {tx(t) for t in NCT})),
    ("Lakalei-Idate + Central Timor | rest", lambda s: s in ({tx(t) for t in CT + LI}, {tx(t) for t in NCT + LI})),
    ("Lakalei-Idate | rest", lambda s: s == {tx(t) for t in LI}),
    ("Rote-Meto + Helong (with or without Flores) | rest",
     lambda s: s in ({tx(t) for t in RMH}, {tx(t) for t in RMH + FLORES})),
    ("Kisar-Luang-Tela-Masbuar or part | rest", lambda s: bool(s) and s <= {tx(t) for t in SWM}),
]


def tally(trees, ingroup, ref):
    ing = [tx(t) for t in ingroup]
    cl = {"LI + Central Timor (with or without Welaun)": [{tx(t) for t in CT + LI}, {tx(t) for t in NCT + LI}],
          "Timor-Babar incl. LI": [{tx(t) for t in TB if t in ingroup}],
          "LI + Eastern Timor": [{tx(t) for t in LI + ET}],
          "Timor-region taxa (all but Flores)": [{tx(t) for t in ingroup if t not in FLORES}],
          "Central Timor (with Welaun)": [{tx(t) for t in CT if t in ingroup}],
          "Nuclear Central Timor": [{tx(t) for t in NCT}],
          "Lakalei-Idate": [{tx(t) for t in LI}]}
    roots, clade_hits, n = Counter(), Counter(), 0
    for t in trees:
        clades, split, _ = reduce_root(t, ing, ref)
        n += 1
        cat = "polytomy" if split == "polytomy" else next((k for k, f in ROOT_CATS if f(set(split))), None)
        if cat is None:
            cat = "other: " + " ".join(sorted(split)) if len(split) <= 6 else f"other ({len(split)} taxa)"
        roots[cat] += 1
        for k, wants in cl.items():
            if any(frozenset(w) in clades for w in wants):
                clade_hits[k] += 1
    return dict(n=n, root_positions={k: round(v / n, 3) for k, v in roots.most_common()},
                root_categories={k: round(roots.get(k, 0) / n, 3) for k, _ in ROOT_CATS},
                rooted_clades={k: round(clade_hits[k] / n, 3) for k in cl})


def e40sum():
    res = {}
    for name in SETS:
        uf = os.path.join(W40, f"{name}.ufboot")
        if os.path.exists(uf):
            ml = read_trees(os.path.join(W40, f"{name}.treefile"))
            res[f"{name} ML tree"] = tally(ml, TAXA, tx(REF[name]))
            res[f"{name} UFBoot"] = tally(read_trees(uf), TAXA, tx(REF[name]))
            res[f"{name} ML tree"]["lnL"] = a9.lnl(os.path.join(W40, f"{name}.iqtree"))
    mbp = os.path.join(W40, "mb", "primary")
    if os.path.exists(mbp + ".log") and "Analysis completed" in open(mbp + ".log").read():
        res["primary MrBayes"] = tally(mb_trees(mbp), TAXA, tx("og-tagalog"))
        res["primary MrBayes"]["convergence"] = mb_conv(mbp)
    json.dump(res, open(os.path.join(LIT, "e40_root.json"), "w"), indent=1)
    for k, v in res.items():
        print(k, json.dumps(v["root_positions"])[:300])
        print("   ", json.dumps(v["rooted_clades"]))


def mb_conv(prefix):
    out = {}
    try:
        txt = open(prefix + ".mcmc").read().strip().splitlines()
        last = [l for l in txt if re.match(r"^\d", l)][-1].split()
        out["final_asdsf"] = float(last[-1])
    except Exception:
        pass
    try:
        ps = [l.split() for l in open(prefix + ".pstat").read().splitlines()[2:] if l.strip()]
        out["min_ess"] = round(min(float(x[-3]) for x in ps if len(x) > 3 and re.match(r"^[\d.]+$", x[-3])), 1)
        out["max_psrf"] = round(max(float(x[-1]) for x in ps if re.match(r"^[\d.]+$", x[-1])), 3)
    except Exception:
        pass
    return out


def nexus_from_phy(phy, nex):
    lines = open(phy).read().splitlines()
    ntax, nchar = map(int, lines[0].split())
    with open(nex, "w") as fh:
        fh.write(f"#NEXUS\nbegin data;\n  dimensions ntax={ntax} nchar={nchar};\n"
                 "  format datatype=restriction missing=? gap=-;\n  matrix\n")
        for l in lines[1:]:
            n, s = l.split()
            fh.write(f"    {n:24s} {s}\n")
        fh.write("  ;\nend;\n")


def e40mb():
    wd = os.path.join(W40, "mb")
    os.makedirs(wd, exist_ok=True)
    nexus_from_phy(os.path.join(W40, "primary.phy"), os.path.join(wd, "matrix.nex"))
    m = bayes.MCMC
    block = "\n".join(["#NEXUS", "begin mrbayes;", "  set autoclose=yes nowarn=yes seed=1234 swapseed=1235;",
                       "  execute matrix.nex;", f"  outgroup {tx('og-tagalog')};",
                       "  lset coding=noabsencesites rates=gamma;", "  prset brlenspr=unconstrained:exp(10.0);",
                       f"  mcmcp ngen={m['ngen']} samplefreq={m['samplefreq']} diagnfreq={m['diagnfreq']} "
                       "nruns=2 nchains=2 printfreq=100000 filename=primary;", "  mcmc;",
                       "  sumt filename=primary burnin=500 contype=allcompat;",
                       "  sump filename=primary burnin=500;", "end;", ""])
    open(os.path.join(wd, "primary.nex"), "w").write(block)
    t0 = time.time()
    with open(os.path.join(wd, "primary.log"), "w") as fh:
        subprocess.run([MB, "primary.nex"], cwd=wd, stdout=fh, stderr=subprocess.STDOUT, check=True)
    print(f"e40 MrBayes done in {time.time() - t0:.0f}s")


# ---------------------------------------------------------------- E42
DEFINING = {"p_lenited": ("Timor-Babar", TB), "ng_velar": ("Central Timor", CT), "ng_n": ("Eastern Timor", ET),
            "j_rhotic": ("Eastern Timor", ET), "j_l": ("Central Timor", CT), "R_zero": ("Eastern Timor", ET),
            "b_lenited": ("Central Timor + Lakalei-Idate", CT + LI), "d_liquid": ("Central Timor", CT),
            "b_h_initial": ("Ramelaic", NCT + LI), "k_lost_initial": ("Ramelaic", NCT + LI),
            "k_lost_medial": ("Ramelaic", NCT + LI)}


def e42_matrix():
    inn = importlib.import_module("21_innovations")
    mat = {r["Taxon"]: dict(r) for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                                "innovation_matrix_24_hull.csv"))}
    chars = list(DEFINING)
    auto = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "automatic_tokens.csv"))
    defs = {n: (tg, None, st) for n, tg, st in inn.CHARS}
    defs.update({n: (tg, pos, st) for n, tg, pos, st in a9.HULL_CHARS})
    filled = {}
    for t in FLORES:
        for ch in chars:
            if mat[t][ch] in ("0", "1"):
                continue
            if ch == "p_lenited":
                mat[t][ch] = "0"
                filled[f"{t} {ch}"] = "0 (E2: *p kept in 10 of 10 Flores-Lembata tokens)"
                continue
            tg, pos, st = defs[ch]
            c = Counter(r["Class"] for r in auto if r["Lect_ID"] == t and r["Target"] == tg
                        and (pos is None or r["Position"] == pos) and r["Class"] not in ("", "other"))
            top = c.most_common(2)
            if sum(c.values()) >= 2 and (len(top) == 1 or top[0][1] > top[1][1]):
                mat[t][ch] = str(int(top[0][0] in st))
                filled[f"{t} {ch}"] = f"{mat[t][ch]} (automatic atlas: {dict(c)})"
            else:
                filled[f"{t} {ch}"] = f"? (automatic atlas: {dict(c)})"
    return mat, chars, filled


def root_on(tree, taxa):
    t = copy.deepcopy(tree)
    names = [c.name for c in t.get_terminals()]
    want = [tx(x) for x in taxa]
    t.root_with_outgroup(next(n for n in names if n not in want))
    t.root_with_outgroup(want if len(want) > 1 else want[0])
    return t


def camin_sokal(tree, states):
    """Irreversible 0 -> 1, root state 0; '?' free. Returns the minimum number of origins."""
    INF = 10 ** 6

    def go(c):
        if c.is_terminal():
            v = states.get(c.name, "?")
            return (0 if v in ("0", "?") else INF, 0 if v in ("1", "?") else INF)
        f0, f1 = 0, 0
        for ch in c.clades:
            a0, a1 = go(ch)
            f0 += min(a0, 1 + a1)
            f1 += a1
        return (min(f0, INF), min(f1, INF))
    r0, r1 = go(tree.root)
    return min(r0, 1 + r1)


def dollo(tree, states):
    """One origin (above the MRCA of all 1s), any number of losses, no regain. Returns 1 + losses (0 if no 1s)."""
    ones = [c for c in tree.get_terminals() if states.get(c.name) == "1"]
    if not ones:
        return 0
    m = tree.common_ancestor(ones) if len(ones) > 1 else ones[0]
    INF = 10 ** 6

    def go(c):
        if c.is_terminal():
            v = states.get(c.name, "?")
            return (0 if v in ("0", "?") else INF, 0 if v in ("1", "?") else INF)
        g0, g1 = 0, 0
        for ch in c.clades:
            a0, a1 = go(ch)
            g0 += a0
            g1 += min(a1, 1 + a0)
        return (min(g0, INF), min(g1, INF))
    return 1 + go(m)[1]


def e42(root_split=None):
    from Bio import Phylo
    mat, chars, filled = e42_matrix()
    trees = {"H": os.path.join(RES, "total_evidence", "lex_only.treefile"),
             "G": os.path.join(LIT, "e21_abc", "G.treefile"),
             "GE": os.path.join(LIT, "e29", "GE.treefile")}
    rootings = {"Flores pair": FLORES}
    res_note = None
    e40 = os.path.join(LIT, "e40_root.json")
    if os.path.exists(e40):
        mb = json.load(open(e40)).get("primary MrBayes")
        if mb:
            top, p = next(iter(mb["root_positions"].items()))
            res_note = dict(position=top, posterior=p)
            rt = {"Central Timor (with or without Welaun) | rest": CT,
                  "Lakalei-Idate + Central Timor | rest": CT + LI,
                  "Flores pair | rest": None, "Lakalei-Idate | rest": LI,
                  "Rote-Meto + Helong (with or without Flores) | rest": RMH + FLORES}.get(top)
            if p >= 0.5 and rt:
                rootings["E40 MAP root"] = rt
    res = dict(characters=chars, flores_coding=filled, trees={}, e40_root=res_note)
    for name, path in trees.items():
        base = Phylo.read(path, "newick")
        for rname, rt in rootings.items():
            t = root_on(base, rt)
            per = {}
            for ch in chars:
                st = {tx(k): v[ch] for k, v in mat.items()}
                per[ch] = dict(fitch=a9.fitch(t, st), camin_sokal=camin_sokal(t, st), dollo=dollo(t, st))
            res["trees"][f"{name}, rooted on {rname}"] = dict(
                per_character=per, totals={k: sum(v[k] for v in per.values()) for k in ("fitch", "camin_sokal", "dollo")})
    # one standard: who shows each change outside its defining group
    res["outside_defining_group"] = {ch: dict(group=g, taxa=[t for t in TAXA if mat[t][ch] == "1" and t not in mem])
                                     for ch, (g, mem) in DEFINING.items()}
    # native *p, restated from E2 (results/exploratory/e2_by_lect.csv) with Fisher's exact test
    from scipy.stats import fisher_exact
    e2 = {r["Group"]: r for r in read_csv(os.path.join(RES, "exploratory", "e2_by_group_d1concepts.csv"))}

    def kept(groups):
        n = sum(int(e2[g]["p_N"]) for g in groups)
        k = sum(round(float(e2[g]["p_kept"] or 0) * int(e2[g]["p_N"])) for g in groups)
        return k, n
    kl, nl = kept(["Idate", "Lakalei"])
    kn, nn = kept(["Mambae", "Kemak", "Tokodede"])
    res["e2_p_kept"] = dict(lakalei_idate=[kl, nl], nuclear_central_timor=[kn, nn],
                            fisher_p=float(fisher_exact([[kl, nl - kl], [kn, nn - kn]])[1]),
                            note="all matched words, Tetun-shaped included (E2); E2b lists the native cases")
    json.dump(res, open(os.path.join(LIT, "e42_sound_irreversible.json"), "w"), indent=1, ensure_ascii=False)
    for k, v in res["trees"].items():
        print(k, v["totals"], "p_lenited:", v["per_character"]["p_lenited"])
    print(json.dumps(res["outside_defining_group"], ensure_ascii=False))
    print(res["e2_p_kept"])
    print(json.dumps(filled, ensure_ascii=False, indent=0))


# ---------------------------------------------------------------- E43
def mb_split_probs(prefix, order):
    parts = {}
    for line in open(prefix + ".parts"):
        m = re.match(r"\s*(\d+)\s+([.*]+)\s*$", line)
        if m:
            parts[m.group(1)] = m.group(2)
    prob = {}
    for line in open(prefix + ".tstat"):
        p = line.split()
        if p and p[0].isdigit():
            prob[p[0]] = float(p[2])
    n = len(order)
    out = {}
    for pid, s in parts.items():
        on = frozenset(order[i] for i, c in enumerate(s) if c == "*")
        out[on] = prob.get(pid, 1.0 if len(on) in (1, n - 1) else 0.0)
        out[frozenset(order) - on] = out[on]
    return out


def e43():
    hyp = read_csv(os.path.join(REPO, "reference", "hypotheses.csv")) + \
        read_csv(os.path.join(REPO, "reference", "hypotheses_addendum2.csv"))
    dist = {r["Hypothesis"]: r for r in read_csv(os.path.join(RES, "hypotheses", "summary_d1_lexstat.csv"))}
    contested = {"GE-TB", "GE-CT", "GE-ET", "GE-ETLI", "EDW-TB", "EDW-CT", "EDW-ET", "HULL-R", "HULL-F", "HULL98-W"}
    mb = mb_split_probs(os.path.join(RES, "bayes", "unconstrained"), [tx(t) for t in TAXA])
    ml = os.path.join(RES, "total_evidence", "lex_only.splits.nex")
    e40 = os.path.join(W40, "mb", "primary")
    e40trees = mb_trees(e40) if os.path.exists(e40 + ".run2.t") else None
    rows, seen = [], set()
    for h in hyp:
        if h["ID"] in contested or not h["ID"].startswith(("GE-", "EDW-")):
            continue
        mem = [t for t in TAXA if t in set(h["Members"].split())]
        key = frozenset(mem)
        if len(mem) < 2 or len(mem) >= len(TAXA) - 1 or key in seen:
            continue
        seen.add(key)
        d = dist.get(h["ID"], {})
        sup_ml = a9.splits_support(ml, {"x": mem})["x"]
        row = dict(ID=h["ID"], Name=h["Name"], Taxa_in_24=len(mem), Members=" ".join(mem),
                   Distance_UPGMA=d.get("Primary_UPGMA", ""), Distance_NJ=d.get("Primary_NJ", ""),
                   MrBayes=round(mb.get(frozenset(tx(t) for t in mem), 0.0), 3), ML_UFBoot=sup_ml)
        if e40trees:
            want = frozenset(tx(t) for t in mem)
            hits = sum(want in reduce_root(t, [tx(x) for x in TAXA], tx("og-tagalog"))[0] for t in e40trees)
            row["E40_rooted"] = round(hits / len(e40trees), 3)
        rows.append(row)
    write_csv(os.path.join(LIT, "e43_known_groups.csv"), rows)
    summ = dict(groups=len(rows),
                recovered_MrBayes_095=sum(r["MrBayes"] >= 0.95 for r in rows),
                recovered_ML_95=sum(r["ML_UFBoot"] >= 95 for r in rows),
                by_size={})
    for lo, hi in ((2, 2), (3, 4), (5, 30)):
        sub = [r for r in rows if lo <= r["Taxa_in_24"] <= hi]
        summ["by_size"][f"{lo}-{hi} taxa"] = dict(n=len(sub), MrBayes_095=sum(r["MrBayes"] >= 0.95 for r in sub),
                                                  ML_95=sum(r["ML_UFBoot"] >= 95 for r in sub))
    json.dump(dict(summary=summ, groups=rows), open(os.path.join(LIT, "e43_known_groups.json"), "w"), indent=1)
    for r in rows:
        print(r["ID"], r["Name"][:30], r["Taxa_in_24"], r["Distance_UPGMA"], r["Distance_NJ"], r["MrBayes"],
              r["ML_UFBoot"], r.get("E40_rooted", ""))
    print(json.dumps(summ))


# ---------------------------------------------------------------- E44, E48
def read_phy(path):
    lines = open(path).read().splitlines()
    return {l.split()[0]: l.split()[1] for l in lines[1:] if l.strip()}


def write_reduced(src, dst, drop_taxa=(), drop_cols=()):
    m = {k: v for k, v in read_phy(src).items() if k not in set(drop_taxa)}
    n = len(next(iter(m.values())))
    keep = [j for j in range(n) if j not in set(drop_cols) and any(s[j] == "1" for s in m.values())]
    with open(dst, "w") as fh:
        fh.write(f"{len(m)} {len(keep)}\n")
        for k, s in m.items():
            fh.write(f"{k} {''.join(s[j] for j in keep)}\n")
    return list(m), len(keep)


def clade_support(splits, sets):
    return {k: a9.splits_support(splits, {"x": v})["x"] if v else None for k, v in sets.items()}


def focal_sets(focal, names, indep=False):
    ct = [t for t in (["mamb1306", "kema1243", "tuku1254"] if indep else CT) if tx(t) in names]
    nct = [t for t in (["mamb1306", "kema1243", "tuku1254"] if indep else NCT) if tx(t) in names]
    et = [t for t in ET if tx(t) in names]
    f = [t for t in focal if tx(t) in names]
    out = {"with Central Timor (with Welaun if present)": f + ct, "with Nuclear Central Timor": f + nct,
           "with Eastern Timor": f + et, "with Habu": f + ["habu1241"], "with Tetun": f + ["tetu1245-suai"],
           "focal": f if len(f) > 1 else None}
    return {k: v for k, v in out.items() if v is None or all(tx(t) in names for t in v)}


def sister(treefile, focal):
    from Bio import Phylo
    t = Phylo.read(treefile, "newick")
    t = root_on(t, FLORES)
    f = [tx(x) for x in focal]
    node = t.common_ancestor(f) if len(f) > 1 else next(c for c in t.get_terminals() if c.name == f[0])
    if len(f) > 1 and len(node.get_terminals()) != len(f):
        return "focal not monophyletic in the ML tree"
    path = t.get_path(node)
    parent = path[-2] if len(path) > 1 else t.root
    sib = [c for c in parent.clades if c is not node]
    return sorted(x.name for s in sib for x in s.get_terminals())


def e44():
    wd = os.path.join(LIT, "e44")
    os.makedirs(wd, exist_ok=True)
    mats = {"primary": os.path.join(RES, "total_evidence", "lex.phy"),
            "independent": os.path.join(LIT, "e28", "lex_independent.phy")}
    res = {}
    for mname, src in mats.items():
        names = list(read_phy(src))
        indep = mname == "independent"
        # (a) Lakalei-Idate constrained monophyletic
        p = os.path.join(wd, f"{mname}.phy")
        write_reduced(src, p)
        open(os.path.join(wd, f"{mname}_li.constr"), "w").write(
            "((" + ",".join(tx(t) for t in LI) + ")," + ",".join(n for n in names if n not in [tx(t) for t in LI]) + ");\n")
        pre = f"{mname}_li_mono"
        if not os.path.exists(os.path.join(wd, pre + ".splits.nex")):
            a9.iqtree(p, pre, ("-B", "1000", "-g", f"{mname}_li.constr"))
        sp = os.path.join(wd, pre + ".splits.nex")
        res[f"{mname}: Lakalei-Idate monophyletic"] = dict(
            support=clade_support(sp, focal_sets(LI, names, indep)),
            sister=sister(os.path.join(wd, pre + ".treefile"), LI),
            lnL=a9.lnl(os.path.join(wd, pre + ".iqtree")))
        # (b), (c) one member alone
        for keep, drop in (("Idate alone", "laka1255"), ("Lakalei alone", "idat1237-cribas")):
            q = os.path.join(wd, f"{mname}_{drop}_dropped.phy")
            nm, nc = write_reduced(src, q, drop_taxa=[tx(drop)])
            pre = f"{mname}_{drop}_dropped"
            if not os.path.exists(os.path.join(wd, pre + ".splits.nex")):
                a9.iqtree(q, pre, ("-B", "1000"))
            focal = [t for t in LI if t != drop]
            res[f"{mname}: {keep}"] = dict(
                support=clade_support(os.path.join(wd, pre + ".splits.nex"), focal_sets(focal, nm, indep)),
                sister=sister(os.path.join(wd, pre + ".treefile"), focal), characters=nc)
        print(mname, json.dumps({k: v for k, v in res.items() if k.startswith(mname)}, indent=0), flush=True)
    json.dump(res, open(os.path.join(LIT, "e44_li_together.json"), "w"), indent=1)


def e48():
    wd = os.path.join(LIT, "e48")
    os.makedirs(wd, exist_ok=True)
    src = os.path.join(RES, "total_evidence", "lex.phy")
    names = list(read_phy(src))
    res = {}
    # (a) without Tetun
    p = os.path.join(wd, "no_tetun.phy")
    nm, nc = write_reduced(src, p, drop_taxa=[tx("tetu1245-suai")])
    if not os.path.exists(os.path.join(wd, "no_tetun.splits.nex")):
        a9.iqtree(p, "no_tetun", ("-B", "1000"))
    res["without Tetun"] = dict(support=clade_support(os.path.join(wd, "no_tetun.splits.nex"), focal_sets(LI, nm)),
                                sister=sister(os.path.join(wd, "no_tetun.treefile"), LI), characters=nc)
    # (b) without sets that have a Papuan member
    roles = {l["ID"]: l["Role"] for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    rows = variant_rows("d1", "lexstat", "primary")
    papuan_sets = {r["Cognateset_ID"] for r in rows if roles.get(r["Lect_ID"]) == "TAP"}
    chars = [r["Cognateset_ID"] for r in read_csv(os.path.join(RES, "bayes", "characters.csv"))]
    drop = [j for j, c in enumerate(chars) if c in papuan_sets]
    p = os.path.join(wd, "no_papuan_sets.phy")
    nm, nc = write_reduced(src, p, drop_cols=drop)
    if not os.path.exists(os.path.join(wd, "no_papuan_sets.splits.nex")):
        a9.iqtree(p, "no_papuan_sets", ("-B", "1000"))
    res["without Papuan-shared sets"] = dict(
        support=clade_support(os.path.join(wd, "no_papuan_sets.splits.nex"), focal_sets(LI, nm)),
        sister=sister(os.path.join(wd, "no_papuan_sets.treefile"), LI), characters=nc, sets_dropped=len(drop))
    members = defaultdict(set)
    for r in rows:
        members[r["Cognateset_ID"]].add(r["Lect_ID"])
    res["sets_shared_with_Papuan_per_taxon"] = {
        t: sum(1 for s in papuan_sets if t in members[s]) for t in TAXA}
    json.dump(res, open(os.path.join(LIT, "e48_tetun_papuan.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E45
def e45():
    wd = os.path.join(LIT, "e45")
    os.makedirs(wd, exist_ok=True)
    res = {}
    for mname, taxa, indep in (("primary", TAXA, False), ("independent", indep_taxa(), True)):
        src = os.path.join(W40, "primary.phy" if not indep else "indep_primary.phy")
        p = os.path.join(wd, f"{mname}.phy")
        write_reduced(src, p)
        allt = list(read_phy(p))
        ct = [tx(t) for t in (["mamb1306", "kema1243", "tuku1254"] if indep else CT)]
        li = [tx(t) for t in LI]
        et = [tx(t) for t in ET]
        fl = [tx(t) for t in FLORES]
        og = [tx(t) for t in OG]
        tb = [n for n in allt if n not in ct + fl + og + li]
        strs = {
            "free (Lakalei-Idate together)": "((" + ",".join(li) + ")," + ",".join(n for n in allt if n not in li) + ");",
            "Lakalei-Idate + Central Timor, rooted": "(((" + ",".join(li) + ")," + ",".join(ct) + "),"
            + ",".join(n for n in allt if n not in li + ct) + ");",
            "Timor-Babar incl. Lakalei-Idate, rooted": "(((" + ",".join(li) + ")," + ",".join(tb) + "),"
            + ",".join(n for n in allt if n not in li + tb) + ");",
            "Lakalei-Idate + Eastern Timor": "(((" + ",".join(li) + ")," + ",".join(et) + "),"
            + ",".join(n for n in allt if n not in li + et) + ");"}
        trees = {}
        for i, (name, s) in enumerate(strs.items()):
            cf = f"{mname}_c{i}.constr"
            open(os.path.join(wd, cf), "w").write(s + "\n")
            pre = f"{mname}_c{i}"
            if not os.path.exists(os.path.join(wd, pre + ".treefile")):
                a9.iqtree(p, pre, ("-g", cf))
            trees[name] = open(os.path.join(wd, pre + ".treefile")).read().strip()
        open(os.path.join(wd, f"{mname}_candidates.trees"), "w").write("\n".join(trees.values()) + "\n")
        if not os.path.exists(os.path.join(wd, f"{mname}_au.iqtree")):
            a9.iqtree(p, f"{mname}_au", ("-te", f"{mname}_c0.treefile", "-z", f"{mname}_candidates.trees",
                                         "-zb", "10000", "-au", "-n", "0"))
        txt = open(os.path.join(wd, f"{mname}_au.iqtree")).read().split("USER TREES")[1]
        lines = [l for l in txt.splitlines() if re.match(r"\s+\d+\s+-?\d", l)]
        res[mname] = {}
        for name, line in zip(trees, lines):
            f = line.split()
            res[mname][name] = dict(logL=float(f[1]), deltaL=float(f[2]), p_AU=float(f[-2]))
    # Holm within E45 (constrained trees only) and across every topology test in the project
    fam45 = [(m, k, v["p_AU"]) for m, d in res.items() for k, v in d.items() if not k.startswith("free")]
    adj45 = a9.holm([p for _, _, p in fam45])
    for (m, k, _), a in zip(fam45, adj45):
        res[m][k]["holm_within_E45"] = round(a, 4)
    e6 = {r["Tree"]: r for r in read_csv(os.path.join(RES, "ml", "au_test.csv"))}
    e36 = json.load(open(os.path.join(LIT, "e36_au_independent.json")))
    allp = [(f"E6 {k}", float(re.findall(r"[\d.]+", e6[k]["raw"])[-1])) for k in ("ramelaic", "timor_babar", "li_eastern_timor")]
    allp += [(f"E36 {k}", v["p_AU"]) for k, v in e36.items() if k != "free"]
    allp += [(f"E45 {m} {k}", p) for m, k, p in fam45]
    adj = a9.holm([p for _, p in allp])
    res["holm_all_topology_tests"] = {n: dict(p=p, holm=round(a, 4)) for (n, p), a in zip(allp, adj)}
    json.dump(res, open(os.path.join(LIT, "e45_au_rooted.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E41, E47 (MrBayes)
def e41(variant="all"):
    wd = os.path.join(LIT, "e41_relaxed_clock")
    os.makedirs(wd, exist_ok=True)
    src = os.path.join(RES, "total_evidence", "lex.phy")
    name = "igr" if variant == "all" else "igr_no_tela"
    p = os.path.join(wd, f"{name}.phy")
    write_reduced(src, p, drop_taxa=[] if variant == "all" else [tx("tela1241")])
    nexus_from_phy(p, os.path.join(wd, f"{name}_matrix.nex"))
    block = "\n".join(["#NEXUS", "begin mrbayes;", "  set autoclose=yes nowarn=yes seed=1234 swapseed=1235;",
                       f"  execute {name}_matrix.nex;", "  lset coding=noabsencesites rates=gamma;",
                       "  prset brlenspr=clock:uniform clockvarpr=igr clockratepr=fixed(1.0);",
                       f"  mcmcp ngen=3000000 samplefreq=1000 diagnfreq=50000 nruns=2 nchains=2 printfreq=200000 "
                       f"filename={name};", "  mcmc;", f"  sumt filename={name} burnin=750 contype=allcompat;",
                       f"  sump filename={name} burnin=750;", "end;", ""])
    open(os.path.join(wd, f"{name}.nex"), "w").write(block)
    t0 = time.time()
    with open(os.path.join(wd, f"{name}.log"), "w") as fh:
        subprocess.run([MB, f"{name}.nex"], cwd=wd, stdout=fh, stderr=subprocess.STDOUT, check=True)
    print(f"e41 {name} done in {time.time() - t0:.0f}s")


def rooted_tally(trees, taxa):
    names = [tx(t) for t in taxa]
    cl = {"LI + Central Timor (with or without Welaun)": [{tx(t) for t in CT + LI}, {tx(t) for t in NCT + LI}],
          "Timor-Babar incl. LI": [{tx(t) for t in TB if tx(t) in names}],
          "LI + Eastern Timor": [{tx(t) for t in LI + ET}],
          "Timor-region taxa (all but Flores)": [{n for n in names if n not in [tx(t) for t in FLORES]}],
          "Central Timor (with Welaun)": [{tx(t) for t in CT}], "Nuclear Central Timor": [{tx(t) for t in NCT}],
          "Lakalei-Idate": [{tx(t) for t in LI}]}
    roots, hits = Counter(), Counter()
    for t in trees:
        kids = t.root.clades
        sides = [frozenset(x.name for x in k.get_terminals()) for k in kids]
        split = min(sides, key=len) if len(sides) == 2 else "polytomy"
        cat = "polytomy" if split == "polytomy" else next((k for k, f in ROOT_CATS if f(set(split))), None)
        if cat is None:
            cat = "other: " + " ".join(sorted(split)) if len(split) <= 6 else f"other ({len(split)} taxa)"
        roots[cat] += 1
        clades = {frozenset(x.name for x in c.get_terminals()) for c in t.find_clades() if not c.is_terminal()}
        for k, wants in cl.items():
            if any(frozenset(w) in clades for w in wants):
                hits[k] += 1
    n = len(trees)
    return dict(n=n, root_positions={k: round(v / n, 3) for k, v in roots.most_common(12)},
                root_categories={k: round(roots.get(k, 0) / n, 3) for k, _ in ROOT_CATS},
                rooted_clades={k: round(hits[k] / n, 3) for k in cl})


def e41sum():
    wd = os.path.join(LIT, "e41_relaxed_clock")
    res = {}
    for name, taxa in (("igr", TAXA), ("igr_no_tela", [t for t in TAXA if t != "tela1241"])):
        pre = os.path.join(wd, name)
        if mb_done(pre):
            res[name] = rooted_tally(mb_trees(pre), taxa)
            res[name]["convergence"] = mb_conv(pre)
    # E34 (strict clock, Timor constrained) for comparison, same reading
    e34 = os.path.join(LIT, "e34_rooted_clock", "clock")
    res["E34 strict clock (for comparison)"] = rooted_tally(mb_trees(e34), TAXA)
    json.dump(res, open(os.path.join(LIT, "e41_relaxed_clock.json"), "w"), indent=1)
    for k, v in res.items():
        print(k, json.dumps(v["root_positions"])[:400])
        print("   ", json.dumps(v["rooted_clades"]), v.get("convergence"))


E47 = {"c1H": CT + LI, "c1G": LI + ET, "c2T": ["west2547-welaun", "tetu1245-suai"]}


def e47(name):
    wd = os.path.join(LIT, "e47")
    os.makedirs(wd, exist_ok=True)
    m = os.path.join(wd, "matrix.nex")
    if not os.path.exists(m):
        open(m, "w").write(open(os.path.join(RES, "bayes", "matrix.nex")).read())
    s = bayes.SS
    block = "\n".join(["#NEXUS", "begin mrbayes;", "  set autoclose=yes nowarn=yes seed=1234 swapseed=1235;",
                       "  execute matrix.nex;", f"  outgroup {tx(FLORES[0])};",
                       "  lset coding=noabsencesites rates=gamma;", "  prset brlenspr=unconstrained:exp(10.0);",
                       f"  constraint con = {' '.join(tx(t) for t in E47[name])};",
                       "  prset topologypr=constraints(con);",
                       f"  ss ngen={s['ngen']} nsteps={s['nsteps']} alpha={s['alpha']} samplefreq={s['samplefreq']} "
                       f"burninss={s['burninss']} diagnfreq={s['diagnfreq']} nruns=2 nchains=1 printfreq=200000 "
                       f"filename={name};", "end;", ""])
    open(os.path.join(wd, f"{name}.nex"), "w").write(block)
    t0 = time.time()
    with open(os.path.join(wd, f"{name}.log"), "w") as fh:
        subprocess.run([MB, f"{name}.nex"], cwd=wd, stdout=fh, stderr=subprocess.STDOUT, check=True)
    print(f"e47 {name} done in {time.time() - t0:.0f}s")


def ss_marginal(logfile):
    txt = open(logfile).read()
    m = re.findall(r"Mean:\s+(-?[\d.]+)", txt.split("Marginal likelihood")[-1]) if "Marginal likelihood" in txt else []
    if m:
        return float(m[-1])
    vals = re.findall(r"^\s+Mean:?\s+(-?[\d.]+)", txt, re.M)
    return float(vals[-1]) if vals else None


def e47sum():
    wd = os.path.join(LIT, "e47")
    ml = {n: ss_marginal(os.path.join(wd, f"{n}.log")) for n in E47 if os.path.exists(os.path.join(wd, f"{n}.log"))}
    ml["c2pos (Central Timor with Welaun, step 7)"] = json.load(open(os.path.join(RES, "bayes", "bayes_factors.json")))[
        "marginals"]["c2pos"]["lnML"]
    res = dict(marginals=ml)
    if ml.get("c1H") and ml.get("c1G"):
        res["lnBF LI+CT vs LI+ET"] = round(ml["c1H"] - ml["c1G"], 2)
    if ml.get("c2T"):
        res["lnBF CT with Welaun vs Welaun+Tetun"] = round(ml["c2pos (Central Timor with Welaun, step 7)"] - ml["c2T"], 2)
    json.dump(res, open(os.path.join(LIT, "e47_direct_bf.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E49
def heights(trees, a, b):
    """a, b: taxon lists; b nested in a expected. Height(a MRCA) - height(b MRCA) where both are clades."""
    A, B = frozenset(tx(t) for t in a), frozenset(tx(t) for t in b)
    diffs, rel, n_both = [], [], 0
    for t in trees:
        clades = {frozenset(x.name for x in c.get_terminals()): c for c in t.find_clades() if not c.is_terminal()}
        if A in clades and B in clades:
            n_both += 1
            ha = t.distance(clades[A], next(iter(clades[A].get_terminals())))
            hb = t.distance(clades[B], next(iter(clades[B].get_terminals())))
            diffs.append(ha - hb)
            rel.append((ha - hb) / hb if hb else np.nan)
    q = lambda v: [round(float(np.nanpercentile(v, x)), 3) for x in (2.5, 50, 97.5)] if v else None
    return dict(samples=len(trees), both_clades=round(n_both / len(trees), 3), diff_q=q(diffs), relative_q=q(rel))


def e49():
    res = {}
    for name, pre in (("E34 strict clock", os.path.join(LIT, "e34_rooted_clock", "clock")),
                      ("E41 relaxed clock", os.path.join(LIT, "e41_relaxed_clock", "igr")),
                      ("E41 relaxed clock, no Tela-Masbuar", os.path.join(LIT, "e41_relaxed_clock", "igr_no_tela"))):
        if mb_done(pre):
            tr = mb_trees(pre)
            res[name] = {"LI + NCT over NCT": heights(tr, LI + NCT, NCT),
                         "LI + CT (with Welaun) over CT": heights(tr, LI + CT, CT)}
    json.dump(res, open(os.path.join(LIT, "e49_heights.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E46
REFEREE_FLAGS = {  # sets the referee names as retentions or cognate errors (packet and E17)
    "2sg_informal-32": "retention (PMP *(i)kahu)", "to_eat-1843": "retention (PMP *kaən)",
    "water-2293": "retention (PMP *wahiR)", "leaf-949": "retention (*kayu + *dahun)",
    "hair-710": "retention (compound with *qulu, *dahun)", "tail-1644": "retention (*ikuR)",
    "good-637": "retention (*ma-pia)", "to_laugh-1997": "retention (PCEMP *malip)",
    "to_stand-2176": "retention (*ma-diRi)", "far-478": "retention, very probably (*ma-zauq)",
    "small-1519": "retention, very probably (*anak)", "wife-2376": "retention (*b<in>ahi; split by LexStat)",
    "wife-2380": "retention (*b<in>ahi; split by LexStat)", "who-2359": "not cognate (ʔɛta ~ sepdua)",
    "dry-416": "doubtful cognate (kiʔɑs ~ glia)"}
SINGLE = {"LI": ["idat1237", "laka1255"], "NCT": ["mamb1306", "kema1243", "tuku1254"],
          "Tetun": ["tetu1246", "tetu1245-suai"], "Habu": ["habu1241"], "Kawaimina": ["waim1252", "midi1237", "naue1237"]}


def trip_block(rows, status, stable):
    att, so = a9.index(rows, status)
    T = a9.ic.T
    out = {}
    for lists, L in (("representative", T), ("single_survey", SINGLE)):
        for x in ("Tetun", "Habu", "Kawaimina"):
            r = a9.triplet(so, att, stable, L["LI"], L["NCT"], L[x], ("LI", "NCT", x))
            out[f"{lists} (LI, NCT, {x})"] = {k: dict(counts=v["counts"], ab_strictly_largest=v["ab_strictly_largest"])
                                             for k, v in r.items() if k in ("stable", "other")}
    out["LI+NCT strictly largest on stable vs all three"] = {
        lists: all(out[f"{lists} (LI, NCT, {x})"]["stable"]["ab_strictly_largest"] for x in ("Tetun", "Habu", "Kawaimina"))
        for lists in ("representative", "single_survey")}
    return out


def e46():
    stable, _ = a9.ex.stable_concepts()
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    res = {}
    # (a) polarised on the E40 coding: innovation = no outgroup taxon in the set
    outg = set(FLORES) | set(OG) | {l for l, v in lects.items() if v["Group"] == "Flores-Lembata"}
    rows = [r for r in e40_rows() if r["Lect_ID"] in outg or lects.get(r["Lect_ID"], {}).get("Role") != "TAP"]
    og_concepts = {r["Concept_ID"] for r in rows if r["Lect_ID"] in outg}
    members = defaultdict(set)
    for r in rows:
        members[r["Cognateset_ID"]].add(r["Lect_ID"])
    status = {}
    for r in rows:
        if r["Concept_ID"] in og_concepts:
            s = r["Cognateset_ID"]
            status[s] = "retention" if members[s] & outg else "innovation"
    ing_rows = [r for r in rows if r["Lect_ID"] not in outg]
    res["polarised by outgroups (E40 coding)"] = trip_block(ing_rows, status, stable)
    # (a') referee's version on the primary coding: R2 innovations absent from Flores, Rote-Meto + Helong, Wetar
    st_r2 = {r["Cognateset_ID"]: r["Status"] for r in read_csv(os.path.join(REPO, "derived", "innovations",
                                                                           "cognate_set_status_r2.csv"))}
    prim = [r for r in variant_rows("d1", "lexstat", "primary") if lects[r["Lect_ID"]]["Role"] != "TAP"
            and r["Cognateset_ID"] in st_r2]
    west = {l for l, v in lects.items() if v["Group"] in ("Flores-Lembata", "Rote", "Meto", "Helong", "Wetar")}
    pm = defaultdict(set)
    for r in prim:
        pm[r["Cognateset_ID"]].add(r["Lect_ID"])
    st_ref = {s: ("innovation" if v == "innovation" and not (pm[s] & west) else "retention") for s, v in st_r2.items()}
    res["R2, absent from Flores, Rote-Meto + Helong and Wetar"] = trip_block(prim, st_ref, stable)
    # (b) cleaned: referee flags + E35 strict + E37 inherited, R2 primary coding
    e35s = {r["Cognateset_ID"] for r in read_csv(os.path.join(LIT, "e35_reclassified_sets_strict.csv"))}
    e37 = {r["Cognateset_ID"] for r in read_csv(os.path.join(LIT, "e37_ge_verdicts.csv")) if r["Verdict"] == "inherited"}
    flagged = set(REFEREE_FLAGS) | e35s | e37
    st_clean = {s: ("retention" if s in flagged else v) for s, v in st_r2.items()}
    res["R2 baseline"] = trip_block(prim, st_r2, stable)
    res["R2 cleaned"] = trip_block(prim, st_clean, stable)
    res["R2 cleaned and polarised (Flores, Rote-Meto + Helong, Wetar)"] = trip_block(
        prim, {s: ("retention" if s in flagged else v) for s, v in st_ref.items()}, stable)
    res["cleaning"] = dict(referee_flags=REFEREE_FLAGS, e35_strict=len(e35s), e37_inherited=sorted(e37),
                           innovations_reclassified=sum(1 for s in st_r2 if st_r2[s] == "innovation" and s in flagged))
    # (c) E17 exclusive counts after cleaning
    ex17 = read_csv(os.path.join(LIT, "e17_exclusive_innovations_r2.csv"))
    side = lambda c: "Central Timor" if c == "LI + CT" else ("eastern" if c in (
        "LI + Habu", "LI + Kawaimina", "LI + Tetun", "LI + several Eastern Timor") else "other")
    before, after = Counter(), Counter()
    kept = defaultdict(list)
    for r in ex17:
        before[side(r["Class"])] += 1
        if r["Cognateset_ID"] not in flagged:
            after[side(r["Class"])] += 1
            kept[side(r["Class"])].append(f"{r['Concept_ID']} ({r['Cognateset_ID']})")
    res["E17 exclusive (R2)"] = dict(before=dict(before), after_cleaning=dict(after), kept=dict(kept),
                                     note="Central Timor side checked by the referee and by E35/E37; the eastern side "
                                          "by E35/E37 only")
    json.dump(res, open(os.path.join(LIT, "e46_triplets_clean.json"), "w"), indent=1, ensure_ascii=False)
    for k, v in res.items():
        if isinstance(v, dict) and "LI+NCT strictly largest on stable vs all three" in v:
            print(k, v["LI+NCT strictly largest on stable vs all three"])
            for kk, vv in v.items():
                if kk.startswith(("representative", "single")):
                    print("   ", kk, vv["stable"]["counts"])
    print(json.dumps(res["E17 exclusive (R2)"], ensure_ascii=False, indent=0))
    print(res["cleaning"]["innovations_reclassified"], "innovations reclassified")


def e46cal(n=1000):
    """Tree-pair rule calibration: no borrowing, on H and on G, unpolarised and polarised on the Flores pair."""
    abc = importlib.import_module("31_borrowing_abc")
    tp = importlib.import_module("36_triplet_power")
    rng = np.random.default_rng(20261012)
    H, G = abc.trees()
    stable, _ = abc.ex.stable_concepts()
    lects, rows, members, status, segs = abc.ic.classify()
    attested = defaultdict(set)
    for r in rows:
        attested[r["Lect_ID"]].add(r["Concept_ID"])
    concepts = sorted({r["Concept_ID"] for r in rows})
    smask = np.array([c in stable for c in concepts])
    allx = set(TAXA)
    att_idx = {l: np.array([c in attested[l] for c in concepts]) for l in allx}
    ref = np.load(os.path.join(LIT, "e21_abc", "reference_table.npz"), allow_pickle=True)
    S, P, M, obs = ref["S"], ref["P"], ref["M"], ref["obs"]
    sd = S.std(axis=0)
    sd[sd == 0] = 1
    d = np.sqrt((((S - obs) / sd) ** 2).sum(axis=1))
    X = {"Tetun": ["tetu1245-suai"], "Habu": ["habu1241"], "Kawaimina": ["waim1252", "midi1237", "naue1237"]}

    def counts(tip, xs, polar):
        n = np.zeros(3)
        fl = [tip[tx(f)] for f in FLORES]
        for a in LI:
            for b in NCT:
                for c in xs:
                    m = att_idx[a] & att_idx[b] & att_idx[c] & smask
                    A, B, C = tip[tx(a)], tip[tx(b)], tip[tx(c)]
                    ok = m
                    if polar:
                        ok = m & (A != fl[0]) & (A != fl[1]) & (B != fl[0]) & (B != fl[1]) & (C != fl[0]) & (C != fl[1])
                    n[0] += np.sum(ok & (A == B) & (A != 0) & (C != A))
                    n[1] += np.sum(ok & (A == C) & (A != 0) & (B != A))
                    n[2] += np.sum(ok & (B == C) & (B != 0) & (A != B))
        return n
    res = {}
    for model, tree in (("H", H), ("G", G)):
        info = abc.branches(tree)
        own = np.where(M == model)[0]
        acc = own[np.argsort(d[own])[: int(0.01 * len(own))]]
        wins = {False: [], True: []}
        for _ in range(n):
            th = P[rng.choice(acc)]
            tip = abc.simulate(info, model, (th[0], th[1], 0.0, 0.0), concepts, smask, None, rng)
            for polar in (False, True):
                ok = []
                for xs in X.values():
                    c = counts(tip, xs, polar)
                    ok.append(c[0] > c[1] and c[0] > c[2])
                wins[polar].append(all(ok))
        res[f"true tree {model}"] = {"unpolarised: LI+NCT strictly largest vs all three": round(float(np.mean(wins[False])), 3),
                                     "polarised on Flores": round(float(np.mean(wins[True])), 3), "datasets": n}
        print(model, res[f"true tree {model}"], flush=True)
    json.dump(res, open(os.path.join(LIT, "e46_tree_pair_calibration.json"), "w"), indent=1)


# ---------------------------------------------------------------- E50
def e50(n=1000):
    os.environ["RETENTION_RULE"] = "chosen"
    mt = importlib.import_module("30_more_tests")
    S = mt.setup()
    lects = S["lects"]
    taxa = [t for t in TAXA if t not in FLORES]
    flores = {l for l, info in lects.items() if info["Group"] == "Flores-Lembata"}
    items = []
    for s, ls in S["inn"].items():
        if ls & flores:
            continue
        c = S["concept_of"][s]
        T = frozenset(t for t in taxa if t in ls)
        if len(T) >= 2:
            items.append((T, frozenset(t for t in taxa if c in S["attested"][t]), c))
    sc = {r["Taxon"]: r for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                           "innovation_matrix_24_hull.csv"))}
    for ch in DEFINING:
        T = frozenset(t for t in taxa if sc[t][ch] == "1")
        A = frozenset(t for t in taxa if sc[t][ch] in ("0", "1"))
        if 2 <= len(T) < len(A):
            items.append((T, A, None))
    concepts = sorted({c for _, _, c in items if c})
    cidx = {c: i for i, c in enumerate(concepts)}

    def sigma(G, w):
        G = frozenset(G)
        eps = p = q = 0.0
        for T, A, c in items:
            if not G <= A:
                continue
            k = 1.0 if c is None else w[cidx[c]]
            if T == G:
                eps += k
            if G <= T:
                p += k
            elif T & G and T - G and G - T:
                q += k
        return eps * (p / (p + q) if p + q else 0.0)
    rng = np.random.default_rng(20261014)
    obs = {k: round(sigma(v, np.ones(len(concepts))), 2) for k, v in mt.NAMED.items()}
    boot = {k: [] for k in mt.NAMED}
    for _ in range(n):
        w = np.bincount(rng.integers(0, len(concepts), len(concepts)), minlength=len(concepts)).astype(float)
        for k, v in mt.NAMED.items():
            boot[k].append(sigma(v, w))
    res = dict(replicates=n, concepts=len(concepts), items=len(items), observed=obs,
               interval95={k: [round(float(np.percentile(v, 2.5)), 2), round(float(np.percentile(v, 97.5)), 2)]
                           for k, v in boot.items()},
               share_zero={k: round(float(np.mean(np.array(v) == 0)), 3) for k, v in boot.items()})
    pairs = [k for k in mt.NAMED]
    li_ct = "Lakalei-Idate + Central Timor" if "Lakalei-Idate + Central Timor" in pairs else None
    li_et = "Lakalei-Idate + Eastern Timor" if "Lakalei-Idate + Eastern Timor" in pairs else None
    if li_ct and li_et:
        res["share_LI_CT_gt_LI_ET"] = round(float(np.mean(np.array(boot[li_ct]) > np.array(boot[li_et]))), 3)
    json.dump(res, open(os.path.join(LIT, "e50_glottometry_boot.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


# ---------------------------------------------------------------- housekeeping
def house():
    """E26 (R0, as pre-registered): the Tetun share split by Tetun lect, stored."""
    from itertools import product
    stable, _ = a9.ex.stable_concepts()
    lects, rows, members, status, segs = a9.ic.classify()
    attested, sets_of = a9.index(rows, status)
    by = defaultdict(list)
    for l, info in lects.items():
        by[info["Group"]].append(l)
    E18 = ("mamb1306-Slete", "kema1243-kaila", "idat1237-cribas", "tetu1245-suai")
    out = {}
    for t in ("tetu1246", "tetu1245-suai"):
        ok, lt = [], []
        for m, k, i in product(sorted(by["Mambae"]), sorted(by["Kemak"]), ["idat1237", "idat1237-cribas"]):
            if (m, k, i, t) == E18:
                continue
            r = a9.triplet(sets_of, attested, stable, [i, "laka1255"], [m, k, "tuku1254"], [t], ("LI", "NCT", "Tetun"))
            ok.append(r["stable"]["ab_strictly_largest"])
            c = r["stable"]["counts"]
            lt.append(c["LI+Tetun"] > c["LI+NCT"])
        out[t] = dict(combinations=len(ok), share_LI_NCT_largest_on_stable=round(float(np.mean(ok)), 3),
                      share_LI_Tetun_larger_than_LI_NCT_on_stable=round(float(np.mean(lt)), 3))
    out["rule"] = a9.ic.RULE
    json.dump(out, open(os.path.join(LIT, "e26_tetun_breakdown.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def packet2():
    """Reviewer packet for the E17 exclusive sets on both sides (R2 rule), with every automatic or review flag."""
    ex17 = read_csv(os.path.join(LIT, "e17_exclusive_innovations_r2.csv"))
    e35s = {r["Cognateset_ID"]: r["Etymon"] for r in read_csv(os.path.join(LIT, "e35_reclassified_sets_strict.csv"))}
    e37 = {r["Cognateset_ID"]: r["Verdict"] for r in read_csv(os.path.join(LIT, "e37_ge_verdicts.csv"))}
    rows = []
    for r in ex17:
        sid = r["Cognateset_ID"]
        rows.append(dict(Cognateset_ID=sid, Shared_with=r["Class"].replace("LI + ", ""), Concept=r["Concept_ID"],
                         Stable=r["Stable"], Forms=r["Forms"], Review_flag=REFEREE_FLAGS.get(sid, ""),
                         ACD_strict_etymon=e35s.get(sid, ""), Grimes_Edwards_tables=e37.get(sid, "not checked"),
                         Specialist_verdict="", Notes=""))
    write_csv(os.path.join(REPO, "derived", "innovations", "reviewer_packet_exclusive_sets.csv"), rows)
    print(len(rows), "sets written")


if __name__ == "__main__":
    cmd = sys.argv[1]
    fn = globals()[cmd]
    fn(*sys.argv[2:])
