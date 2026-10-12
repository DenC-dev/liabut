"""Addendum 11: E37 (the decisive sets against Grimes and Edwards's own tables), E38 (SOWH parametric bootstrap of the
eastern placement), and the summary of E39 (contacTrees capped at five contact edges; run with BEAST, see 29).

    python3 src/40_addendum11.py e37
    python3 src/40_addendum11.py e38 [primary|independent] [reps]     # needs IQ-TREE ($IQTREE); about 30 min each
    python3 src/40_addendum11.py e39                                  # summarises e19_contactrees/ct_C_cap5.*
"""
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from io import StringIO

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, ned, read_csv, sca_string, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

a9 = importlib.import_module("34_addendum9")
a10 = importlib.import_module("39_addendum10")
ic, ex, clf, tx = a9.ic, a9.ex, a9.clf, a9.tx
ra = importlib.import_module("19_reflex_atlas")
LIT = os.path.join(RES, "literature")
IQ = os.environ.get("IQTREE", "iqtree2")
GE = os.path.join(REPO, "derived", "ge2026_tables", "forms.csv")


# ---------------------------------------------------------------- E37
def ge_codes(lect_id, glottocode):
    return ra.groups_for(glottocode) + ra.groups_for(lect_id.split("-")[0])


def e37():
    rule = json.load(open(os.path.join(LIT, "e30_classifier.json")))["chosen"]
    stable, _ = ex.stable_concepts()
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    concepts = read_csv(os.path.join(DATA, "d1", "concepts.csv"))
    kw = {c["ID"]: a10.keyword(c["English"]) for c in concepts}
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"]
            for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    ge = defaultdict(list)
    for r in read_csv(GE):
        ge[r["Glottocode"]].append(r)
    # sets to check: the reviewer packet and E17's exclusive Lakalei-Idate sets
    packet = read_csv(os.path.join(REPO, "derived", "innovations", "reviewer_packet_lakalei_idate_stable.csv"))
    excl = read_csv(os.path.join(LIT, "e17_exclusive_innovations.csv"))
    check = {r["Cognateset_ID"]: "packet" for r in packet}
    for r in excl:
        check.setdefault(r["Cognateset_ID"], "E17 " + r["Class"])
    rows = variant_rows("d1", "lexstat", "primary")
    members = defaultdict(list)
    for r in rows:
        members[r["Cognateset_ID"]].append(r)

    def ge_match(r):
        k = kw.get(r["Concept_ID"])
        toks = segs[r["Form_ID"]]
        if not k or not toks:
            return []
        out = []
        for code in dict.fromkeys(ge_codes(r["Lect_ID"], lects[r["Lect_ID"]]["Glottocode"])):
            for g in ge.get(code, []):
                if not re.search(rf"\b{re.escape(k)}\b", g["Gloss"].lower()):
                    continue
                form = re.sub(r"[⟦⟧\-=]", "", g["Form"])
                d = ned(sca_string(list(form)), sca_string(toks))
                if d <= 0.5:
                    out.append((d, g))
        return sorted(out, key=lambda x: x[0])
    verdicts = []
    for sid, why in check.items():
        rs = members.get(sid, [])
        hits = []
        for r in rs:
            for d, g in ge_match(r)[:1]:
                hits.append((r, d, g))
        if any("Lakalei-Idate lexically specific innovations" in g["Caption"] for _, _, g in hits):
            v = "Lakalei-Idate innovation"
        elif any(g["Cognate"] == "True" and g["Etymon"].startswith("*") for _, _, g in hits):
            v = "inherited"
        elif hits:
            v = "in the tables, not marked cognate"
        else:
            v = "not in the tables"
        verdicts.append(dict(Cognateset_ID=sid, Checked_because=why, Concept=rs[0]["Concept_ID"] if rs else "",
                             Verdict=v,
                             Evidence="; ".join(f"{r['Lect_ID']}:{''.join(segs[r['Form_ID']])} ~ {g['Language']} "
                                                f"{g['Form']} ({g['Etymon']}; table {g['Table']} '{g['Caption'][:50]}'; "
                                                f"cognate {g['Cognate']}; NED {d:.2f})" for r, d, g in hits)[:900]))
    write_csv(os.path.join(LIT, "e37_ge_verdicts.csv"), verdicts)
    counts = Counter(v["Verdict"] for v in verdicts)
    # rerun the stable triplets with "inherited" sets reclassified
    status, _ = a9.statuses(rows, rule)
    inherited = {v["Cognateset_ID"] for v in verdicts if v["Verdict"] == "inherited"}
    status2 = {k: ("retention" if k in inherited else v) for k, v in status.items()}
    T = ic.T
    res = dict(rule=rule, sets_checked=len(verdicts), verdicts=dict(counts),
               by_reason={w: dict(Counter(v["Verdict"] for v in verdicts if v["Checked_because"] == w))
                          for w in sorted({v["Checked_because"] for v in verdicts})})
    for name, st in (("E30_rule", status), ("with_GE_verdicts", status2)):
        att, so = a9.index(rows, st)
        res[name] = dict(
            representative={f"(LI, NCT, {x})": a9.triplet(so, att, stable, T["LI"], T["NCT"], T[x], ("LI", "NCT", x))
                            for x in ("Tetun", "Habu", "Kawaimina", "Galoli")},
            single_survey={f"(LI, NCT, {x})": a9.triplet(so, att, stable, ["idat1237", "laka1255"],
                                                          ["mamb1306", "kema1243", "tuku1254"], lst, ("LI", "NCT", x))
                           for x, lst in (("Tetun", ["tetu1246", "tetu1245-suai"]), ("Habu", ["habu1241"]),
                                          ("Kawaimina", ["waim1252", "midi1237", "naue1237"]))})
    after = res["with_GE_verdicts"]
    res["stable_pairing_stands"] = all(after[k][f"(LI, NCT, {x})"]["stable"]["ab_strictly_largest"]
                                       for k in ("representative", "single_survey") for x in ("Habu", "Kawaimina"))
    json.dump(res, open(os.path.join(LIT, "e37_ge_check.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in res.items() if k not in ("E30_rule", "with_GE_verdicts")}, indent=1))
    for name in ("E30_rule", "with_GE_verdicts"):
        for grp in ("representative", "single_survey"):
            for k, v in res[name][grp].items():
                print(name, grp, k, v["stable"]["counts"])


# ---------------------------------------------------------------- E38
SETS = {
    "primary": dict(phy=os.path.join(RES, "total_evidence", "lex.phy"),
                    free=os.path.join(RES, "total_evidence", "lex_only"),
                    cons_tree=os.path.join(LIT, "e21_abc", "G"),
                    constraint=os.path.join(LIT, "e21_abc", "constraint_LI_ET.nwk")),
    "independent": dict(phy=os.path.join(LIT, "e28", "lex_independent.phy"),
                        free=os.path.join(LIT, "e28", "lex_independent"),
                        cons_tree=os.path.join(LIT, "e28", "au_li_eastern_timor"),
                        constraint=os.path.join(LIT, "e28", "li_eastern_timor.constr")),
}


def read_phy(path):
    lines = open(path).read().split("\n")
    n, m = map(int, lines[0].split())
    data = {}
    for l in lines[1:]:
        if l.strip():
            name, seq = l.split()
            data[name] = seq
    return data, m


def model_params(iqfile):
    txt = open(iqfile).read()
    pi0 = float(re.search(r"pi\(0\) = ([\d.]+)", txt).group(1))
    rates = [float(x) for x in re.findall(r"^\s+\d\s+([\d.]+)\s+0\.25\s*$", txt, re.M)]
    lnl = float(re.search(r"Log-likelihood of the tree:\s*(-?[\d.]+)", txt).group(1))
    return pi0, rates, lnl


def simulate(tree, taxa, pi0, rates, mask, rng):
    """Binary CTMC (GTR2) with G4 rates on an unrooted tree; mask[taxon] = bool array of observed cells."""
    m = len(next(iter(mask.values())))
    pi1 = 1 - pi0
    mu = 1 / (2 * pi0 * pi1)
    out = {t: np.zeros(m, dtype=np.int8) for t in taxa}
    todo = np.arange(m)
    while len(todo):
        k = len(todo)
        r = np.array(rates)[rng.integers(0, len(rates), k)]
        root_state = (rng.random(k) < pi1).astype(np.int8)
        states = {}

        def walk(clade, st):
            states[clade] = st
            for ch in clade.clades:
                t = (ch.branch_length or 0.0) * r
                e = np.exp(-mu * t)
                p01 = pi1 * (1 - e)
                p10 = pi0 * (1 - e)
                u = rng.random(k)
                nst = np.where(st == 0, (u < p01).astype(np.int8), (u >= p10).astype(np.int8))
                walk(ch, nst)
        walk(tree.root, root_state)
        tips = {c.name: states[c] for c in tree.get_terminals()}
        for t in taxa:
            out[t][todo] = tips[t]
        ok = np.zeros(k, dtype=bool)
        for t in taxa:
            ok |= (tips[t] == 1) & mask[t][todo]
        todo = todo[~ok]
    return out


def e38(which="primary", reps=100):
    from Bio import Phylo
    S = SETS[which]
    data, m = read_phy(S["phy"])
    taxa = list(data)
    mask = {t: np.array([c != "?" for c in s]) for t, s in data.items()}
    pi0, rates, lnl_c = model_params(S["cons_tree"] + ".iqtree")
    _, _, lnl_f = model_params(S["free"] + ".iqtree")
    obs = lnl_f - lnl_c
    tree = Phylo.read(S["cons_tree"] + ".treefile", "newick")
    rng = np.random.default_rng(20261014 + (0 if which == "primary" else 1))
    wd = os.path.join(LIT, "e38", which)
    os.makedirs(wd, exist_ok=True)
    shutil.copy(S["constraint"], os.path.join(wd, "constraint.nwk"))
    out_path = os.path.join(LIT, f"e38_sowh_{which}.json")
    deltas = json.load(open(out_path))["deltas"] if os.path.exists(out_path) else []
    for i in range(len(deltas), reps):
        sim = simulate(tree, taxa, pi0, rates, mask, rng)
        with open(os.path.join(wd, "sim.phy"), "w") as fh:
            fh.write(f"{len(taxa)} {m}\n")
            for t in taxa:
                fh.write(t + " " + "".join("?" if not mask[t][j] else str(sim[t][j]) for j in range(m)) + "\n")
        ll = {}
        for name, extra in (("free", []), ("cons", ["-g", "constraint.nwk"])):
            subprocess.run([IQ, "-T", "1", "-seed", str(1000 + i), "-redo", "-quiet", "-s", "sim.phy",
                            "-m", "GTR2+FO+G4", "-pre", f"s_{name}", *extra], cwd=wd, check=True)
            ll[name] = model_params(os.path.join(wd, f"s_{name}.iqtree"))[2]
        deltas.append(round(ll["free"] - ll["cons"], 3))
        p = (1 + sum(d >= obs for d in deltas)) / (1 + len(deltas))
        json.dump(dict(matrix=which, observed_delta=round(obs, 3), model=dict(pi0=pi0, gamma_rates=rates),
                       replicates=len(deltas), p=round(p, 4), deltas=deltas,
                       null_median=round(float(np.median(deltas)), 3),
                       null_95=round(float(np.percentile(deltas, 95)), 3)),
                  open(out_path, "w"), indent=1)
        print(which, i, deltas[-1], "p", round(p, 3), flush=True)
    for f in os.listdir(wd):
        if f.startswith("s_") or f == "sim.phy":
            os.remove(os.path.join(wd, f))


# ---------------------------------------------------------------- E39
def e39():
    wd = os.path.join(LIT, "e19_contactrees")
    log = [l for l in open(os.path.join(wd, "ct_C_cap5.log")) if not l.startswith("#")]
    head = log[0].split("\t")
    rows = [dict(zip(head, l.strip().split("\t"))) for l in log[1:] if l.strip()]
    burn = len(rows) // 10
    post = rows[burn:]
    def col(name):
        return np.array([float(r[name]) for r in post if name in r])
    def ess(x):
        x = x - x.mean()
        n = len(x)
        if n < 10 or x.var() == 0:
            return float("nan")
        ac = np.correlate(x, x, mode="full")[n - 1:] / (x.var() * n)
        s = 0.0
        for k in range(1, n):
            if ac[k] < 0.05:
                break
            s += ac[k]
        return n / (1 + 2 * s)
    conv_name = [h for h in head if "convCount" in h][0]
    res = dict(samples=len(rows), burnin=burn, last_state=int(float(rows[-1][head[0]])),
               posterior_ess=round(ess(col("posterior")), 1), likelihood_ess=round(ess(col("likelihood")), 1),
               contact_edges=dict(Counter(int(float(v)) for v in col(conv_name))))
    # base-tree summary: Lakalei-Idate's sister and contact edges touching it, from the tree log
    trees = open(os.path.join(wd, "ct_C_cap5.trees")).read()
    tl = re.findall(r"tree STATE_(\d+)\s*=\s*(?:\[[^\]]*\]\s*)?(.+?);", trees)
    tl = tl[len(tl) // 10:]
    trans = dict(re.findall(r"^\s*(\d+)\s+([^,;\s]+)[,;]?\s*$", trees.split("Translate")[1].split(";")[0], re.M)) \
        if "Translate" in trees else {}
    sis, touch = Counter(), 0
    clade_sets = {"Lakalei-Idate": ["idat1237-cribas", "laka1255"],
                  "Nuclear Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254"],
                  "Central Timor with Welaun": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun"],
                  "Lakalei-Idate + Nuclear Central Timor": ["idat1237-cribas", "laka1255", "mamb1306-Slete",
                                                            "kema1243-kaila", "tuku1254"],
                  "Lakalei-Idate + Central Timor with Welaun": ["idat1237-cribas", "laka1255", "mamb1306-Slete",
                                                                "kema1243-kaila", "tuku1254", "west2547-welaun"],
                  "Tetun + Habu": ["tetu1245-suai", "habu1241"],
                  "Lakalei-Idate + Tetun + Habu": ["idat1237-cribas", "laka1255", "tetu1245-suai", "habu1241"],
                  "Welaun + Lakalei-Idate + Tetun + Habu": ["west2547-welaun", "idat1237-cribas", "laka1255",
                                                           "tetu1245-suai", "habu1241"],
                  "Eastern Timor": ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"],
                  "Lakalei-Idate + Eastern Timor": ["idat1237-cribas", "laka1255", "tetu1245-suai", "habu1241",
                                                    "waim1252", "midi1237", "naue1237"]}
    clade_hits = Counter()
    from Bio import Phylo
    lab = {v: k for k, v in trans.items()}
    li_ids = {lab.get(tx("idat1237-cribas"), tx("idat1237-cribas")), lab.get(tx("laka1255"), tx("laka1255"))}

    def parse(st):
        """Extended Newick -> (children, label); a hybrid leaf has children None and label '#N'."""
        i = 0

        def node():
            nonlocal i
            kids = None
            if st[i] == "(":
                kids = []
                i += 1
                while True:
                    kids.append(node())
                    if st[i] == ",":
                        i += 1
                        continue
                    i += 1  # ')'
                    break
            j = i
            while i < len(st) and st[i] not in ",():;":
                i += 1
            label = st[j:i]
            if i < len(st) and st[i] == ":":
                i += 1
                while i < len(st) and st[i] not in ",();":
                    i += 1
            return (kids, label)
        return node()

    def leaves(nd):
        kids, label = nd
        if kids is None:
            return set() if label.startswith("#") else {label}
        return set().union(*(leaves(k) for k in kids))
    pair_counts = Counter()
    nm = {v: k for k, v in lab.items()}

    def label_of(ids):
        names = sorted(trans.get(i, i) for i in ids)
        return " + ".join(names) if len(names) <= 3 else f"{len(names)} lects incl. " + ", ".join(names[:2])
    for _, nwk in tl:
        st = re.sub(r"\[[^\]]*\]", "", nwk).strip()
        try:
            rt = parse(st)
        except Exception:
            rt = None
        if rt is not None:
            ends = defaultdict(dict)
            stack = [rt]
            while stack:
                kids, label = stack.pop()
                if kids is None:
                    continue
                real = [k for k in kids if not (k[0] is None and k[1].startswith("#"))]
                for k in kids:
                    if k[0] is None and k[1].startswith("#"):
                        ends[k[1]]["branch"] = set().union(*(leaves(r) for r in real)) if real else set()
                if "#" in label:
                    ends["#" + label.split("#")[1]]["node"] = leaves((kids, label))
                stack.extend(kids)
            for e, d in ends.items():
                if "branch" in d and "node" in d:
                    pair_counts[" <-> ".join(sorted([label_of(d["node"]), label_of(d["branch"])]))] += 1
        try:
            root = parse(st)
        except Exception:
            continue
        hits = False
        stack = [root]
        while stack:
            kids, label = stack.pop()
            if kids is None:
                continue
            labels = [k[1] for k in kids if k[0] is None and k[1].startswith("#")]
            real = [k for k in kids if not (k[0] is None and k[1].startswith("#"))]
            if labels:   # a contact edge attaches on the branch above the real children here
                below = set().union(*(leaves(k) for k in real)) if real else set()
                if below and below <= li_ids:
                    hits = True
            if "#" in label and leaves((kids, label)) <= li_ids:
                hits = True
            stack.extend(kids)
        touch += hits
        base = re.sub(r"#\d+", "", re.sub(r"\[[^\]]*\]", "", nwk))
        try:
            t = Phylo.read(StringIO(base + ";"), "newick")
        except Exception:
            continue
        for c in t.get_terminals():
            c.name = trans.get(c.name, c.name)
        names = {c.name: c for c in t.get_terminals() if c.name}
        allt = frozenset(names)
        cls = set()
        for k in t.find_clades():
            L = frozenset(x.name for x in k.get_terminals() if x.name)
            cls.add(L)
            cls.add(allt - L)
        for cname, members in clade_sets.items():
            if frozenset(tx(m) for m in members) in cls:
                clade_hits[cname] += 1
        li = [names.get(tx("idat1237-cribas")), names.get(tx("laka1255"))]
        if None in li:
            continue
        a = t.common_ancestor(li)
        path = t.get_path(a)
        parent = path[-2] if len(path) > 1 else t.root
        inside = set(x.name for x in a.get_terminals())
        sis[" + ".join(sorted(c.name for c in parent.get_terminals() if c.name and c.name not in inside))] += 1
    n = sum(sis.values())
    res["base_tree_samples"] = n
    res["lakalei_idate_sister"] = {k: round(v / n, 3) for k, v in sis.most_common(8)} if n else {}
    res["contact_edge_endpoints_top"] = {k: round(v / len(tl), 3) for k, v in pair_counts.most_common(12)}
    res["base_tree_clades"] = {k: round(clade_hits[k] / n, 3) for k in clade_sets} if n else {}
    res["share_with_contact_edge_on_lakalei_idate_branches"] = round(touch / len(tl), 3) if tl else None
    res["informative"] = bool(res["posterior_ess"] == res["posterior_ess"] and res["posterior_ess"] >= 100)
    json.dump(res, open(os.path.join(LIT, "e39_contactrees_cap5.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "e37":
        e37()
    elif cmd == "e38":
        e38(sys.argv[2] if len(sys.argv) > 2 else "primary", int(sys.argv[3]) if len(sys.argv) > 3 else 100)
    elif cmd == "e39":
        e39()
