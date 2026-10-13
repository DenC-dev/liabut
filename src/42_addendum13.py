"""Addendum 13: E51 (partial cognates), E52 (correspondence regularity), E53 (fuller phonology),
E54 (learned retention classifier), E55 (network split support).

    python3 src/42_addendum13.py e51code      # LingPy Partial on D1 (long)
    python3 src/42_addendum13.py e51          # merge check, IQ-TREE, triplets
    python3 src/42_addendum13.py e52|e53|e53mb|e53sum|e54|e55
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
from common import DATA, REPO, RES, SEED, ned, read_csv, sca_string, write_csv  # noqa: E402
from pipeline import flags, variant_rows  # noqa: E402

a12 = importlib.import_module("41_addendum12")
a9 = a12.a9
te = a12.te
tx = a12.tx
LIT = a12.LIT
TAXA, LI, NCT, CT, ET, FLORES, RMH, TB = a12.TAXA, a12.LI, a12.NCT, a12.CT, a12.ET, a12.FLORES, a12.RMH, a12.TB
W51 = os.path.join(LIT, "e51")


# ---------------------------------------------------------------- E51
def morphemes(seg):
    toks = ["+" if t in ("+", "_") else t for t in seg.split()]
    out = []
    for t in toks:
        if t == "+" and (not out or out[-1] == "+"):
            continue
        out.append(t)
    while out and out[-1] == "+":
        out.pop()
    return out


def e51code():
    from lingpy.compare.partial import Partial
    os.makedirs(W51, exist_ok=True)
    forms = read_csv(os.path.join(DATA, "d1", "forms.csv"))
    D = {0: ["doculect", "concept", "ipa", "tokens", "formid"]}
    i = 0
    for r in forms:
        toks = morphemes(r["Segments"])
        if not [t for t in toks if t != "+"]:
            continue
        i += 1
        D[i] = [r["Lect_ID"], r["Concept_ID"], "".join(t for t in toks if t != "+"), toks, r["ID"]]
    random.seed(SEED)
    np.random.seed(SEED)
    t0 = time.time()
    part = Partial(copy.deepcopy(D), check=False)
    part.get_partial_scorer(runs=1000)
    part.partial_cluster(method="lexstat", threshold=0.55, cluster_method="infomap", ref="cogids")
    out = []
    for k in part:
        cogids = part[k, "cogids"]
        morph = " ".join(part[k, "tokens"]).split(" + ")
        for j, cid in enumerate(cogids):
            out.append(dict(Form_ID=part[k, "formid"], Lect_ID=part[k, "doculect"], Concept_ID=part[k, "concept"],
                            Morpheme=j, Segments=morph[j] if j < len(morph) else "",
                            Cognateset_ID=f"{part[k, 'concept']}-p{cid}"))
    write_csv(os.path.join(W51, "partial_cognates.csv"), out)
    print(len(out), "morphemes", len({o["Cognateset_ID"] for o in out}), "sets", f"{time.time() - t0:.0f}s")


def e51_rows():
    fl = flags("d1")
    out = []
    for r in read_csv(os.path.join(W51, "partial_cognates.csv")):
        g = fl.get(r["Form_ID"])
        if g is None or "True" in (g["L1_expert"], g["L3_indonesian"], g["L4_portuguese"]):
            continue
        out.append(r)
    return out


def e51():
    rows = e51_rows()
    full = {r["Form_ID"]: r["Cognateset_ID"] for r in read_csv(os.path.join(RES, "cognates", "d1_lexstat.csv"))}
    by_form = defaultdict(list)
    for r in rows:
        by_form[r["Form_ID"]].append(r)
    res = {}
    # (a) merge check on the flagged sets
    flagged = ["wife-2376", "wife-2380", "leaf-949", "hair-710", "hair-713", "to_spit-2149", "2sg_informal-32",
               "to_eat-1843", "water-2293", "tail-1644", "good-637", "to_laugh-1997", "to_stand-2176", "far-478",
               "small-1519", "who-2359", "dry-416", "to_cry-1808"]
    fset = defaultdict(set)
    for fid, sid in full.items():
        fset[sid].add(fid)
    merge = {}
    for sid in flagged:
        pm = Counter()
        for fid in fset.get(sid, ()):
            for r in by_form.get(fid, []):
                pm[r["Cognateset_ID"]] += 1
        # which other full-word sets share these morpheme sets
        partners = set()
        for p in pm:
            for r in rows:
                if r["Cognateset_ID"] == p:
                    partners.add(full.get(r["Form_ID"]))
        merge[sid] = dict(morpheme_sets=dict(pm.most_common(4)),
                          full_sets_linked=sorted(x for x in partners if x and x != sid)[:8])
    res["merge_check"] = merge
    w = merge["wife-2376"]["morpheme_sets"].keys() & merge["wife-2380"]["morpheme_sets"].keys()
    res["wife_sets_share_a_morpheme_set"] = bool(w)
    # (b) IQ-TREE on the 24 taxa
    os.makedirs(W51, exist_ok=True)
    p = os.path.join(W51, "partial.phy")
    nchar = a9.phy(rows, TAXA, p)
    res["characters"] = nchar
    if not os.path.exists(os.path.join(W51, "partial.splits.nex")):
        a9.iqtree(p, "partial", ("-B", "1000"))
    names = [tx(t) for t in TAXA]
    res["UFBoot unconstrained"] = a12.clade_support(os.path.join(W51, "partial.splits.nex"), a12.focal_sets(LI, names))
    open(os.path.join(W51, "li.constr"), "w").write(
        "((" + ",".join(tx(t) for t in LI) + ")," + ",".join(n for n in names if n not in [tx(t) for t in LI]) + ");\n")
    if not os.path.exists(os.path.join(W51, "partial_li.splits.nex")):
        a9.iqtree(p, "partial_li", ("-B", "1000", "-g", "li.constr"))
    res["UFBoot Lakalei-Idate kept together"] = a12.clade_support(os.path.join(W51, "partial_li.splits.nex"),
                                                                  a12.focal_sets(LI, names))
    # (c) triplets: morpheme sets classed by R2, polarised by Flores, Rote-Meto + Helong, Wetar
    rule = json.load(open(os.path.join(LIT, "e30_classifier.json")))["chosen"]
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    concepts = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    pmp = a9.ic.pmp_forms()
    glotto = {k: v["Glottocode"] for k, v in lects.items()}
    rows_an = [r for r in rows if lects[r["Lect_ID"]]["Role"] != "TAP" and pmp.get(concepts.get(r["Concept_ID"]))]
    mem = defaultdict(list)
    for r in rows_an:
        mem[r["Cognateset_ID"]].append(r)
    status = {}
    for sid, rs in mem.items():
        ps = pmp[concepts[rs[0]["Concept_ID"]]]
        status[sid] = a9.clf.set_status([(r["Lect_ID"], r["Segments"].split()) for r in rs], ps, rule, glotto)
    west = {l for l, v in lects.items() if v["Group"] in ("Flores-Lembata", "Rote", "Meto", "Helong", "Wetar")}
    status_pol = {s: ("innovation" if v == "innovation" and not ({r["Lect_ID"] for r in mem[s]} & west)
                      else "retention") for s, v in status.items()}
    stable, _ = a9.ex.stable_concepts()
    res["triplets R2"] = a12.trip_block(rows_an, status, stable)
    res["triplets R2 polarised"] = a12.trip_block(rows_an, status_pol, stable)
    json.dump(res, open(os.path.join(LIT, "e51_partial_cognates.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in res.items() if k != "merge_check"}, indent=0, ensure_ascii=False)[:3000])
    print("wife share:", res["wife_sets_share_a_morpheme_set"])
    for k, v in merge.items():
        print(k, v)


# ---------------------------------------------------------------- E52
PAIRS = [("laka1255", "mamb1306-Slete", "CT"), ("laka1255", "tuku1254", "CT"), ("laka1255", "kema1243-kaila", "CT"),
         ("idat1237-cribas", "mamb1306-Slete", "CT"), ("laka1255", "habu1241", "east"),
         ("laka1255", "tetu1245-suai", "east"), ("idat1237-cribas", "habu1241", "east"),
         ("idat1237-cribas", "tetu1245-suai", "east")]
VOWELS = set("AEIOUY")


def sca_align(a, b):
    from lingpy import Pairwise
    from lingpy.sequence.sound_classes import tokens2class
    p = Pairwise(" ".join(a), " ".join(b))
    p.align(mode="global")
    alA, alB, _ = p.alignments[0]

    def cls(seq):
        out = []
        for t in seq:
            out.append("-" if t == "-" else tokens2class([te_tie(t)], "sca")[0])
        return out
    return cls(alA), cls(alB)


def te_tie(t):
    return re.sub(r"([td])([ʃʒszɕʑ])", "\\1\u0361\\2", t) if "\u0361" not in t else t


def e52():
    from scipy.stats import fisher_exact
    rows = variant_rows("d1", "lexstat", "primary")
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"]
            for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    st = {r["Cognateset_ID"]: r["Status"] for r in read_csv(os.path.join(REPO, "derived", "innovations",
                                                                       "cognate_set_status_r2.csv"))}
    form_of = defaultdict(dict)
    for r in rows:
        form_of[r["Cognateset_ID"]].setdefault(r["Lect_ID"], segs[r["Form_ID"]])
    packet = {r["Cognateset_ID"] for r in read_csv(os.path.join(REPO, "derived", "innovations",
                                                               "reviewer_packet_lakalei_idate_stable.csv"))}
    excl = {r["Cognateset_ID"]: r["Class"] for r in read_csv(os.path.join(LIT, "e17_exclusive_innovations_r2.csv"))}
    decisive = packet | set(excl)
    res = dict(pairs={}, decisive={}, summary={})
    per_set = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # sid -> side -> [loan, inherit]
    reference = defaultdict(lambda: [0, 0, 0])                  # side -> [loan-like, inherited-like, uninformative]
    for A, B, side in PAIRS:
        shared = [s for s, m in form_of.items() if A in m and B in m and m[A] and m[B]]
        al = {s: sca_align(form_of[s][A], form_of[s][B]) for s in shared}
        base = defaultdict(Counter)
        for s in shared:
            if st.get(s) == "retention":
                ca, cb = al[s]
                for x, y in zip(ca, cb):
                    if y != "-" and y not in VOWELS:
                        base[y][x] += 1
        diag = {}
        for y, cnt in base.items():
            top, n = cnt.most_common(1)[0]
            if top != y and n >= 2:
                diag[y] = top
        res["pairs"][f"{A} ~ {B}"] = dict(shared=len(shared), baseline=sum(st.get(s) == "retention" for s in shared),
                                          diagnostic={k: v for k, v in sorted(diag.items())})

        def score(s):
            ca, cb = al[s]
            loan = inh = 0
            for x, y in zip(ca, cb):
                if y in diag:
                    if x == y:
                        loan += 1
                    elif x == diag[y]:
                        inh += 1
            return loan, inh
        for s in shared:
            l, i = score(s)
            if s in decisive:
                per_set[s][side][0] += l
                per_set[s][side][1] += i
            elif st.get(s) == "innovation":
                k = 0 if (l and not i) else 1 if (i and not l) else 2
                reference[side][k] += 1

    def verdict(l, i):
        return "loan-like" if l and not i else "inherited-like" if i and not l else "uninformative"
    counts = {"CT": Counter(), "east": Counter()}
    for s in sorted(decisive):
        sides = {}
        for side, (l, i) in per_set[s].items():
            v = verdict(l, i)
            sides[side] = dict(loan_like_positions=l, inheritance_like_positions=i, verdict=v)
        src = "packet" if s in packet else ""
        if s in excl:
            src = (src + " " if src else "") + "exclusive " + excl[s]
        res["decisive"][s] = dict(source=src, by_side=sides)
        # count each set on the side it is decisive for
        want = []
        if s in excl:
            want = ["CT"] if excl[s] == "LI + CT" else ["east"] if excl[s] in (
                "LI + Habu", "LI + Tetun", "LI + Kawaimina", "LI + several Eastern Timor") else []
        else:
            want = list(sides)
        for side in want:
            counts[side][sides.get(side, {}).get("verdict", "no pair available")] += 1
    for side in ("CT", "east"):
        d = counts[side]
        ref = reference[side]
        tab = [[d["loan-like"], d["inherited-like"]], [ref[0], ref[1]]]
        p = float(fisher_exact(tab)[1]) if sum(map(sum, tab)) else None
        res["summary"][side] = dict(decisive=dict(d), reference=dict(loan_like=ref[0], inherited_like=ref[1],
                                                                      uninformative=ref[2]),
                                    decisive_loan_share=round(d["loan-like"] / max(1, d["loan-like"] + d["inherited-like"]), 3),
                                    reference_loan_share=round(ref[0] / max(1, ref[0] + ref[1]), 3), fisher_p=p)
    json.dump(res, open(os.path.join(LIT, "e52_correspondences.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res["summary"], indent=1))
    print(json.dumps(res["pairs"], indent=0, ensure_ascii=False)[:1500])


# ---------------------------------------------------------------- E55
def dist_matrix(rows, taxa, concepts, weights=None):
    sets = defaultdict(set)
    for r in rows:
        sets[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    att = {t: {c for (l, c) in sets if l == t} for t in taxa}
    w = weights or {c: 1 for c in concepts}
    n = len(taxa)
    d = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            both = [c for c in concepts if c in att[taxa[i]] and c in att[taxa[j]] and w.get(c, 0)]
            tot = sum(w[c] for c in both)
            sh = sum(w[c] for c in both if sets[(taxa[i], c)] & sets[(taxa[j], c)])
            d[i, j] = d[j, i] = 1 - sh / tot if tot else 1.0
    return d


def nnet_splits(taxa, d):
    import splitspy.nnet.nnet_algo as nnet
    labels = [tx(t) for t in taxa]
    cycle, splits = nnet.neighbor_net(labels, [list(map(float, r)) for r in d])
    out = {}
    allt = frozenset(labels)
    for sp in splits:
        a = frozenset(labels[i - 1] for i in sp.part1())
        w = sp.get_weight()
        out[a] = out[allt - a] = max(w, out.get(a, 0))
    return out


TARGET_SPLITS = {"Lakalei-Idate": LI, "Lakalei-Idate + Central Timor": LI + CT,
                 "Lakalei-Idate + Nuclear Central Timor": LI + NCT, "Lakalei + Nuclear Central Timor": ["laka1255"] + NCT,
                 "Lakalei-Idate + Habu": LI + ["habu1241"], "Idate + Habu": ["idat1237-cribas", "habu1241"],
                 "Lakalei-Idate + Eastern Timor": LI + ET, "Central Timor": CT, "Nuclear Central Timor": NCT}


def e55(nboot=200):
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if r["Lect_ID"] in TAXA]
    concepts = sorted({r["Concept_ID"] for r in rows})
    obs = nnet_splits(TAXA, dist_matrix(rows, TAXA, concepts))
    rng = np.random.default_rng(20261013)
    hits = defaultdict(list)
    for b in range(int(nboot)):
        draw = Counter(rng.choice(concepts, len(concepts)))
        sp = nnet_splits(TAXA, dist_matrix(rows, TAXA, concepts, weights=dict(draw)))
        for k, v in TARGET_SPLITS.items():
            hits[k].append(sp.get(frozenset(tx(t) for t in v), 0.0))
    res = dict(bootstrap=int(nboot), splits={})
    for k, v in TARGET_SPLITS.items():
        h = np.array(hits[k])
        res["splits"][k] = dict(observed_weight=round(obs.get(frozenset(tx(t) for t in v), 0.0), 4),
                                share_nonzero=round(float(np.mean(h > 1e-9)), 3),
                                median_weight=round(float(np.median(h)), 4))
    ct_side = max(res["splits"][k]["share_nonzero"] for k in ("Lakalei-Idate + Central Timor",
                                                               "Lakalei-Idate + Nuclear Central Timor",
                                                               "Lakalei + Nuclear Central Timor"))
    east = max(res["splits"][k]["share_nonzero"] for k in ("Lakalei-Idate + Habu", "Idate + Habu",
                                                            "Lakalei-Idate + Eastern Timor"))
    res["reading"] = ("linkage signature" if ct_side >= 0.5 and east >= 0.5 else
                      "subgroup signature (Central Timor side)" if ct_side >= 0.5 and east <= 0.1 else
                      "subgroup signature (eastern side)" if east >= 0.5 and ct_side <= 0.1 else "unclear")
    res["max_share"] = dict(central_timor_side=ct_side, eastern_side=east)
    json.dump(res, open(os.path.join(LIT, "e55_network_splits.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E53
KEEP = {"p": "labial stop", "b": "labial stop", "t": "coronal stop", "d": "coronal stop", "k": "velar stop",
        "g": "velar stop", "q": None, "j": "affricate", "z": "affricate", "s": "sibilant", "l": "l", "R": "rhotic",
        "r": "rhotic", "m": "m", "n": "n", "ŋ": "ŋ", "ñ": "ɲ", "w": "w", "y": "y", "h": "h", "c": "affricate"}
W53 = os.path.join(LIT, "e53")


def keep_class(target):
    if target in KEEP:
        return KEEP[target]
    return target   # vowels and sequences: the PMP sequence itself


def e53_matrix():
    exp = defaultdict(Counter)
    for r in read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv")):
        if r["Class"] in ("", "other"):
            continue
        exp[(r["Glottocode"], r["Target"], r["Position"])][r["Class"]] += 1
    auto = defaultdict(Counter)
    for r in read_csv(os.path.join(REPO, "derived", "reflex_atlas", "automatic_tokens.csv")):
        if r["Class"] in ("", "other"):
            continue
        auto[(r["Lect_ID"], r["Target"], r["Position"])][r["Class"]] += 1
    keys = sorted({(t, p) for (_, t, p) in exp})
    major = {}
    for taxon in TAXA:
        gl = te.TAXON_GLOTTO[taxon]
        for (t, p) in keys:
            c = Counter()
            for g in gl:
                c.update(exp.get((g, t, p), Counter()))
            src = "expert"
            if sum(c.values()) < 2 and taxon in FLORES:
                c = auto.get((taxon, t, p), Counter())
                src = "automatic"
            if sum(c.values()) >= 2:
                top = c.most_common(2)
                if len(top) == 1 or top[0][1] > top[1][1]:
                    major[(taxon, t, p)] = (top[0][0], src)
    chars, mat = [], {t: [] for t in TAXA}
    for (t, p) in keys:
        classes = {major[(x, t, p)][0] for x in TAXA if (x, t, p) in major}
        for cl in sorted(classes):
            if cl == keep_class(t):
                continue
            col = {x: ("?" if (x, t, p) not in major else "1" if major[(x, t, p)][0] == cl else "0") for x in TAXA}
            if sum(v == "1" for v in col.values()) >= 2 and sum(v == "0" for v in col.values()) >= 2:
                chars.append(f"*{t} {p} > {cl}")
                for x in TAXA:
                    mat[x].append(col[x])
    return chars, mat


def e53():
    from Bio import Phylo
    from scipy.stats import binomtest
    os.makedirs(W53, exist_ok=True)
    chars, mat = e53_matrix()
    write_csv(os.path.join(W53, "matrix.csv"), [dict(Taxon=t, **{c: v for c, v in zip(chars, mat[t])}) for t in TAXA])
    trees = {"H": os.path.join(RES, "total_evidence", "lex_only.treefile"),
             "G": os.path.join(LIT, "e21_abc", "G.treefile"), "GE": os.path.join(LIT, "e29", "GE.treefile")}
    rooted = {k: a12.root_on(Phylo.read(v, "newick"), FLORES) for k, v in trees.items()}
    per = {}
    for i, ch in enumerate(chars):
        st = {tx(t): mat[t][i] for t in TAXA}
        per[ch] = {k: dict(fitch=a9.fitch(t, st), camin_sokal=a12.camin_sokal(t, st), dollo=a12.dollo(t, st))
                   for k, t in rooted.items()}
    tot = {k: {m: sum(per[c][k][m] for c in chars) for m in ("fitch", "camin_sokal", "dollo")} for k in trees}
    cmp = {}
    for a, b in (("GE", "H"), ("G", "H"), ("GE", "G")):
        for m in ("camin_sokal", "dollo", "fitch"):
            better = sum(per[c][a][m] < per[c][b][m] for c in chars)
            worse = sum(per[c][a][m] > per[c][b][m] for c in chars)
            p = float(binomtest(better, better + worse).pvalue) if better + worse else None
            cmp[f"{a} vs {b}, {m}"] = dict(chars_favouring_first=better, chars_favouring_second=worse, sign_test_p=p)
    li_chars = [c for c in chars if per[c]["GE"]["camin_sokal"] != per[c]["H"]["camin_sokal"]]
    res = dict(characters=len(chars), coded_cells={t: sum(v != "?" for v in mat[t]) for t in TAXA},
               totals=tot, comparisons=cmp, characters_that_differ_H_GE={c: per[c] for c in li_chars})
    json.dump(res, open(os.path.join(LIT, "e53_phonology.json"), "w"), indent=1, ensure_ascii=False)
    print(len(chars), "characters")
    print(json.dumps(tot, indent=0))
    print(json.dumps(cmp, indent=0))
    # nexus for the phonology-only MrBayes run
    keep = [t for t in TAXA if any(v != "?" for v in mat[t])]
    with open(os.path.join(W53, "phon.nex"), "w") as fh:
        fh.write(f"#NEXUS\nbegin data;\n  dimensions ntax={len(keep)} nchar={len(chars)};\n"
                 '  format datatype=standard symbols="01" missing=? gap=-;\n  matrix\n')
        for t in keep:
            fh.write(f"    {tx(t):24s} {''.join(mat[t])}\n")
        fh.write("  ;\nend;\n")
    block = "\n".join(["#NEXUS", "begin mrbayes;", "  set autoclose=yes nowarn=yes seed=1234 swapseed=1235;",
                       "  execute phon.nex;", f"  outgroup {tx(FLORES[0])};", "  lset coding=variable rates=gamma;",
                       "  mcmcp ngen=2000000 samplefreq=1000 diagnfreq=50000 nruns=2 nchains=2 printfreq=200000 "
                       "filename=phon;", "  mcmc;", "  sumt filename=phon burnin=500 contype=allcompat;",
                       "  sump filename=phon burnin=500;", "end;", ""])
    open(os.path.join(W53, "phon_run.nex"), "w").write(block)


def e53mb():
    with open(os.path.join(W53, "phon.log"), "w") as fh:
        subprocess.run([a12.MB, "phon_run.nex"], cwd=W53, stdout=fh, stderr=subprocess.STDOUT, check=True)


def e53sum():
    pre = os.path.join(W53, "phon")
    order = [l.split()[0] for l in open(os.path.join(W53, "phon.nex")).read().split("matrix")[1].split(";")[0]
             .strip().splitlines()]
    mb = a12.mb_split_probs(pre, order)

    def p(ts):
        return round(mb.get(frozenset(tx(t) for t in ts if tx(t) in order), 0.0), 3)
    res = {"Lakalei-Idate": p(LI), "Lakalei-Idate + Central Timor": p(LI + CT),
           "Lakalei-Idate + Nuclear Central Timor": p(LI + NCT), "Lakalei-Idate + Eastern Timor": p(LI + ET),
           "Timor-Babar (unrooted split)": p(TB), "Central Timor": p(CT), "Nuclear Central Timor": p(NCT),
           "Eastern Timor": p(ET), "convergence": a12.mb_conv(pre)}
    trees = a12.mb_trees(pre)
    res["rooted on Flores"] = a12.tally(trees, [t for t in TAXA if tx(t) in order], tx(FLORES[0]))
    out = json.load(open(os.path.join(LIT, "e53_phonology.json")))
    out["mrbayes_phonology_only"] = res
    json.dump(out, open(os.path.join(LIT, "e53_phonology.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E54
def acd_by_sense():
    a10 = importlib.import_module("39_addendum10")
    idx = defaultdict(list)
    for s in read_csv(os.path.join(a10.ACD, "cognatesets.csv")):
        m = re.match(r"(\w+)\s+(\*\S+(?:\s+\S+)*?)\s+'(.*)'\s*$", s["Name"])
        if not m or m.group(1) not in a10.LEVELS or " " in m.group(2).strip():
            continue
        toks = a10.clean_etymon(m.group(2))
        if toks:
            for sense in a10.senses(m.group(3).lower()):
                idx[sense].append(toks)
    return idx, a10.keyword


def cons_only(s):
    return "".join(ch for ch in s if ch not in VOWELS)


def set_features(members, pmps, etyma, glotto):
    """members: [(lect, tokens)]; pmps, etyma: [tokens]."""
    clf = a9.clf
    raw, r2, r2c, mean_r2, best_len = 9.0, 9.0, 9.0, [], 0
    for lid, toks in members:
        if not toks:
            continue
        s_toks = sca_string(toks)
        m_best = 9.0
        for p in pmps:
            raw = min(raw, ned(sca_string(p), s_toks))
            pr = sca_string(clf.predicted(p, lid, glotto.get(lid, "")))
            d = ned(pr, s_toks)
            m_best = min(m_best, d)
            if d < r2:
                r2, best_len = d, len(toks)
            cp, ct = cons_only(pr), cons_only(s_toks)
            if cp and ct:
                r2c = min(r2c, ned(cp, ct))
        mean_r2.append(m_best)
    acd = 1.0
    for lid, toks in members:
        if not toks:
            continue
        for e in etyma:
            acd = min(acd, ned(sca_string(clf.predicted(e, lid, glotto.get(lid, ""))), sca_string(toks)))
    nl = len({l for l, _ in members})
    return [min(raw, 1.5), min(r2, 1.5), float(np.mean(mean_r2)) if mean_r2 else 1.5, acd, float(bool(etyma)),
            min(r2c, 1.5), math.log(nl), best_len]


FEATURES = ["raw_ned", "r2_ned", "r2_mean", "acd_ned", "has_acd", "r2_consonant_ned", "log_lects", "best_len"]


def e54_training():
    cl = importlib.import_module("35_classifier")
    pmp_toks, pmp_sets = cl.abvd_pmp()
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d2", "lects.csv"))}
    glotto = {k: v["Glottocode"] for k, v in lects.items()}
    forms = {f["ID"]: f for f in read_csv(os.path.join(DATA, "d2", "forms.csv"))}
    pnames = {c["ID"]: c["English"] for c in read_csv(os.path.join(DATA, "d2", "concepts.csv"))}
    expert = defaultdict(set)
    for r in read_csv(os.path.join(DATA, "d2", "cognates_expert.csv")):
        expert[r["Form_ID"]].add(r["Cognateset_ID"])
    idx, keyword = acd_by_sense()
    members = defaultdict(list)
    for r in read_csv(os.path.join(RES, "cognates", "d2_lexstat.csv")):
        f = forms.get(r["Form_ID"])
        if f and pmp_toks.get(f["Concept_ID"]) and pmp_sets.get(f["Concept_ID"]):
            members[r["Cognateset_ID"]].append(r["Form_ID"])
    X, y, groups = [], [], []
    for sid, fids in members.items():
        concept = forms[fids[0]]["Concept_ID"]
        mem = [(forms[f]["Lect_ID"], [x for x in forms[f]["Segments"].split() if x not in "+_"]) for f in fids]
        kw = keyword(pnames.get(concept, ""))
        feats = set_features(mem, pmp_toks[concept], idx.get(kw, []) if kw else [], glotto)
        for f in fids:
            if expert.get(f):
                X.append(feats)
                y.append(int(bool(expert[f] & pmp_sets[concept])))
                groups.append(concept)
    return np.array(X), np.array(y), np.array(groups)


def bal_acc(y, p):
    tp = ((p == 1) & (y == 1)).sum(); fn = ((p == 0) & (y == 1)).sum()
    tn = ((p == 0) & (y == 0)).sum(); fp = ((p == 1) & (y == 0)).sum()
    se = tp / (tp + fn) if tp + fn else 0
    sp = tn / (tn + fp) if tn + fp else 0
    return (se + sp) / 2, se, sp


def e54():
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    X, y, g = e54_training()
    print(len(y), "forms;", int(y.sum()), "retentions", flush=True)
    models = {"logistic": lambda: make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced",
                                                                                      max_iter=2000)),
              "gradient_boosting": lambda: GradientBoostingClassifier(random_state=1)}
    res = dict(forms=int(len(y)), retentions=int(y.sum()), features=FEATURES, models={})
    r2_cv = []
    for name, mk in models.items():
        pred = np.zeros(len(y), dtype=int)
        for tr, te_ in GroupKFold(n_splits=5).split(X, y, g):
            m = mk()
            if name == "gradient_boosting":
                w = np.where(y[tr] == 1, 0.5 / y[tr].mean(), 0.5 / (1 - y[tr].mean()))
                m.fit(X[tr], y[tr], sample_weight=w)
            else:
                m.fit(X[tr], y[tr])
            pred[te_] = (m.predict_proba(X[te_])[:, 1] >= 0.5).astype(int)
        ba, se, sp = bal_acc(y, pred)
        res["models"][name] = dict(balanced_accuracy=round(float(ba), 4), retention_recall=round(float(se), 4),
                                   innovation_recall=round(float(sp), 4))
    # R2 (threshold 0.4) on the same forms, for a like-for-like comparison
    r2p = (X[:, 1] <= 0.4).astype(int)
    ba, se, sp = bal_acc(y, r2p)
    res["R2_same_forms"] = dict(balanced_accuracy=round(float(ba), 4), retention_recall=round(float(se), 4),
                                innovation_recall=round(float(sp), 4))
    res["R2_stored"] = json.load(open(os.path.join(LIT, "e30_classifier.json")))["chosen_scores"]["balanced_accuracy"]
    best = max(res["models"], key=lambda k: res["models"][k]["balanced_accuracy"])
    res["best_model"] = best
    res["adopted"] = res["models"][best]["balanced_accuracy"] > res["R2_stored"] + 0.01
    print(json.dumps(res, indent=1), flush=True)
    if res["adopted"]:
        m = models[best]()
        if best == "gradient_boosting":
            w = np.where(y == 1, 0.5 / y.mean(), 0.5 / (1 - y.mean()))
            m.fit(X, y, sample_weight=w)
        else:
            m.fit(X, y)
        res["rerun"] = e54_rerun(m)
    json.dump(res, open(os.path.join(LIT, "e54_learned_classifier.json"), "w"), indent=1, ensure_ascii=False)


def e54_rerun(model):
    a28 = a9.ic
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    glotto = {k: v["Glottocode"] for k, v in lects.items()}
    concepts = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    english = {c["ID"]: c["English"] for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"]
            for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    pmp = a28.pmp_forms()
    idx, keyword = acd_by_sense()
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if lects[r["Lect_ID"]]["Role"] != "TAP"
            and pmp.get(concepts.get(r["Concept_ID"]))]
    members = defaultdict(list)
    for r in rows:
        members[r["Cognateset_ID"]].append(r)
    status = {}
    for sid, rs in members.items():
        c = rs[0]["Concept_ID"]
        kw = keyword(english[c])
        f = set_features([(r["Lect_ID"], segs[r["Form_ID"]]) for r in rs], pmp[concepts[c]],
                         idx.get(kw, []) if kw else [], glotto)
        status[sid] = "retention" if model.predict_proba(np.array([f]))[0, 1] >= 0.5 else "innovation"
    st_r2 = {r["Cognateset_ID"]: r["Status"] for r in read_csv(os.path.join(REPO, "derived", "innovations",
                                                                           "cognate_set_status_r2.csv"))}
    changed = sum(1 for s in status if st_r2.get(s) and st_r2[s] != status[s])
    write_csv(os.path.join(REPO, "derived", "innovations", "cognate_set_status_learned.csv"),
              [dict(Cognateset_ID=s, Concept_ID=members[s][0]["Concept_ID"], Status=status[s],
                    Status_R2=st_r2.get(s, "")) for s in sorted(status)])
    stable, _ = a9.ex.stable_concepts()
    west = {l for l, v in lects.items() if v["Group"] in ("Flores-Lembata", "Rote", "Meto", "Helong", "Wetar")}
    flagged = set(a12.REFEREE_FLAGS) | {r["Cognateset_ID"] for r in read_csv(os.path.join(LIT, "e35_reclassified_sets_strict.csv"))} \
        | {r["Cognateset_ID"] for r in read_csv(os.path.join(LIT, "e37_ge_verdicts.csv")) if r["Verdict"] == "inherited"}
    clean = {s: ("retention" if s in flagged else v) for s, v in status.items()}
    pol = {s: ("innovation" if v == "innovation" and not ({r["Lect_ID"] for r in members[s]} & west) else "retention")
           for s, v in clean.items()}
    out = dict(sets=len(status), innovations=sum(v == "innovation" for v in status.values()),
               innovations_R2=sum(v == "innovation" for s, v in st_r2.items() if s in status), changed_vs_R2=changed)
    out["triplets learned"] = a12.trip_block(rows, status, stable)
    out["triplets learned, cleaned"] = a12.trip_block(rows, clean, stable)
    out["triplets learned, cleaned and polarised"] = a12.trip_block(rows, pol, stable)
    # E17-style exclusive counts
    side = Counter()
    for sid, rs in members.items():
        if status[sid] != "innovation":
            continue
        ls = {r["Lect_ID"] for r in rs}
        if not ls & set(LI):
            continue
        others = {a28.group(lects, l) for l in ls if l not in a28.LI}
        if len(others) == 1:
            o = next(iter(others))
            side["Central Timor" if o == "CT" else "eastern" if o in ("Tetun", "Habu", "Kawaimina") else "other"] += 1
        elif others and others <= {"Tetun", "Habu", "Kawaimina"}:
            side["eastern"] += 1
    out["exclusive_counts"] = dict(side)
    out["condition_4_sensitivity"] = out["triplets learned, cleaned and polarised"][
        "LI+NCT strictly largest on stable vs all three"]
    for k in ("triplets learned", "triplets learned, cleaned", "triplets learned, cleaned and polarised"):
        print(k, out[k]["LI+NCT strictly largest on stable vs all three"])
        for kk, vv in out[k].items():
            if kk.startswith(("repr", "single")):
                print("   ", kk, vv["stable"]["counts"])
    print(out["exclusive_counts"], out["changed_vs_R2"])
    return out


if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])
