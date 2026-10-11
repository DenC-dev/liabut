"""Addendum 9: E25 (multiple testing), E26 (dialect representatives), E27 (consensus cognates),
E28 (data independent of Grimes and Edwards), E29 (sound changes on rival trees).

    python3 src/34_addendum9.py e25|e26|e27|e28|e29|all
Needs IQ-TREE ($IQTREE) for E27, E28 and E29. Outputs in results/literature/ (e25_* ... e29_*).
"""
import importlib
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, UP, read_csv, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

ic = importlib.import_module("28_innovations_contact")
ex = importlib.import_module("10_exploratory")
bayes = importlib.import_module("09_bayes")
te = importlib.import_module("20_total_evidence")
clf = importlib.import_module("35_classifier")
inn = importlib.import_module("21_innovations")
LIT = os.path.join(RES, "literature")
IQ = os.environ.get("IQTREE", "iqtree2")
tx = te.tx
R0 = dict(kind="R0", t=0.5)


# ---------------------------------------------------------------- shared helpers
def norm_p(z):
    return math.erfc(abs(z) / math.sqrt(2)) if z is not None else None


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def bh(ps):
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i], reverse=True)
    adj, run = [0.0] * m, 1.0
    for k, i in enumerate(order):
        rank = m - k
        run = min(run, ps[i] * m / rank)
        adj[i] = min(1.0, run)
    return adj


def statuses(rows, rule):
    """Retention/innovation status for arbitrary cognate rows (same logic as E17 / E30)."""
    concepts = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0]
                for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"]
            for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    glotto = {l["ID"]: l["Glottocode"] for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    pmp = ic.pmp_forms()
    members = defaultdict(list)
    for r in rows:
        if pmp.get(concepts.get(r["Concept_ID"])):
            members[r["Cognateset_ID"]].append(r)
    out = {}
    for sid, rs in members.items():
        ps = pmp[concepts[rs[0]["Concept_ID"]]]
        out[sid] = clf.set_status([(r["Lect_ID"], segs[r["Form_ID"]]) for r in rs], ps, rule, glotto)
    return out, members


def index(rows, status):
    attested, sets_of = defaultdict(set), defaultdict(set)
    for r in rows:
        if r["Cognateset_ID"] not in status:
            continue
        attested[r["Lect_ID"]].add(r["Concept_ID"])
        if status[r["Cognateset_ID"]] == "innovation":
            sets_of[(r["Lect_ID"], r["Concept_ID"])].add(r["Cognateset_ID"])
    return attested, sets_of


def triplet(sets_of, attested, stable, A, B, C, names=("A", "B", "C")):
    out = {}
    for stratum in ("all", "stable", "other"):
        per = defaultdict(lambda: np.zeros(3))
        for a, b, c in product(A, B, C):
            for k in attested[a] & attested[b] & attested[c]:
                if stratum == "stable" and k not in stable or stratum == "other" and k in stable:
                    continue
                sa, sb, sc = sets_of[(a, k)], sets_of[(b, k)], sets_of[(c, k)]
                v = per[k]
                v[0] += bool((sa & sb) - sc)
                v[1] += bool((sa & sc) - sb)
                v[2] += bool((sb & sc) - sa)
        M = np.array(list(per.values())) if per else np.zeros((0, 3))
        tot = M.sum(axis=0) if len(M) else np.zeros(3)
        labels = [f"{names[0]}+{names[1]}", f"{names[0]}+{names[2]}", f"{names[1]}+{names[2]}"]
        # D is always the A+C excess over B+C (the contact direction of interest), as in E18 when A+B is the tree pair
        def d(v):
            s = v[1] + v[2]
            return (v[1] - v[2]) / s if s else 0.0
        D = d(tot)
        m = len(M)
        jk = np.array([d(tot - M[i]) for i in range(m)]) if m > 1 else np.array([0.0])
        se = math.sqrt((m - 1) / m * ((jk - jk.mean()) ** 2).sum()) if m > 1 else float("nan")
        out[stratum] = dict(concepts=m, counts={n: int(x) for n, x in zip(labels, tot)},
                            largest=labels[int(np.argmax(tot))] if tot.max() > 0 else None,
                            ab_strictly_largest=bool(tot[0] > tot[1] and tot[0] > tot[2]),
                            D=round(D, 3), Z=round(D / se, 2) if se and se > 0 else None)
    return out


def phy(rows, taxa, path):
    attested, sets, concept_of = defaultdict(set), defaultdict(set), {}
    for r in rows:
        if r["Lect_ID"] in taxa:
            attested[r["Lect_ID"]].add(r["Concept_ID"])
            sets[r["Cognateset_ID"]].add(r["Lect_ID"])
            concept_of[r["Cognateset_ID"]] = r["Concept_ID"]
    chars = sorted(sets, key=lambda s: (concept_of[s], s))
    with open(path, "w") as fh:
        fh.write(f"{len(taxa)} {len(chars)}\n")
        for t in taxa:
            fh.write(tx(t) + " " + "".join(("1" if t in sets[s] else "0") if concept_of[s] in attested[t] else "?"
                                           for s in chars) + "\n")
    return len(chars)


def iqtree(phyfile, prefix, extra=()):
    wd = os.path.dirname(phyfile)
    subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-s", os.path.basename(phyfile),
                    "-m", "GTR2+FO+G4", "-pre", prefix, *extra], cwd=wd, check=True)


def splits_support(splitsfile, clades):
    txt = open(splitsfile).read()
    labels = {int(i): n for i, n in re.findall(r"\[(\d+)\]\s+'?([^'\n]+)'?", txt.split("TAXLABELS")[1].split(";")[0])}
    allt = frozenset(labels.values())
    splits = {}
    for line in txt.split("MATRIX")[1].split(";")[0].strip().splitlines():
        m = re.match(r"\s*(\d+(?:\.\d+)?)\s+([\d\s]+),?", line)
        if m:
            side = frozenset(labels[int(i)] for i in m.group(2).split())
            w = float(m.group(1))
            splits[side] = max(w, splits.get(side, 0))
            splits[allt - side] = max(w, splits.get(allt - side, 0))
    return {k: splits.get(frozenset(tx(x) for x in v) & allt, 0) for k, v in clades.items()}


def lnl(iqfile):
    m = re.search(r"Log-likelihood of the tree:\s*(-?[\d.]+)", open(iqfile).read())
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------- E25
def e25():
    out = {}
    for suf in ("", "_r2"):
        tests = []
        e18 = json.load(open(os.path.join(LIT, f"e18_triplets{suf}.json")))
        for k, v in e18.items():
            for st in ("all", "stable", "other"):
                z = v[st]["D"]["Z"]
                if z is not None:
                    tests.append(dict(test=f"E18 {k} {st}: {v[st]['D']['pair_excess']}", Z=z, p=norm_p(z)))
        e24 = json.load(open(os.path.join(LIT, f"e24_other_branches{suf}.json")))
        for k, v in e24.items():
            if k.startswith("(Welaun"):
                continue
            for st in ("all", "stable", "other"):
                z = v[st]["D"]["Z"]
                if z is not None:
                    tests.append(dict(test=f"E24 {k} {st}: {v[st]['D']['pair_excess']}", Z=z, p=norm_p(z)))
        e20 = json.load(open(os.path.join(LIT, f"e20_split_test{suf}.json")))["primary_idat1237"]
        for typ, v in e20.items():
            for st, r in v.items():
                if r["binomial_p"] is not None:
                    tests.append(dict(test=f"E20 {typ} {st}: Lakalei-only {r['lakalei_only']} vs Idate-only "
                                           f"{r['idate_only']}", Z=None, p=r["binomial_p"]))
        ps = [t["p"] for t in tests]
        for t, h, b in zip(tests, holm(ps), bh(ps)):
            t.update(p=round(t["p"], 5), holm=round(h, 4), bh=round(b, 4), survives_holm=h < 0.05, survives_bh=b < 0.05)
        out["primary_rule" if not suf else "chosen_rule_R2"] = dict(
            tests=len(tests), nominal_p_below_0_05=sum(t["p"] < 0.05 for t in tests),
            survive_holm=[t["test"] for t in tests if t["survives_holm"]],
            survive_bh=[t["test"] for t in tests if t["survives_bh"]], table=sorted(tests, key=lambda t: t["p"]))
    json.dump(out, open(os.path.join(LIT, "e25_multiple_testing.json"), "w"), indent=1, ensure_ascii=False)
    for k, v in out.items():
        print(k, v["tests"], "tests;", v["nominal_p_below_0_05"], "nominal;", "Holm:", v["survive_holm"], "BH:",
              v["survive_bh"])


# ---------------------------------------------------------------- E26
def e26():
    stable, _ = ex.stable_concepts()
    lects, rows, members, status, segs = ic.classify()       # primary coding, E17 rule (R0) unless env says otherwise
    attested, sets_of = index(rows, status)
    by = defaultdict(list)
    for l, info in lects.items():
        by[info["Group"]].append(l)
    mamb, kemak = sorted(by["Mambae"]), sorted(by["Kemak"])
    idate, tetun = ["idat1237", "idat1237-cribas"], ["tetu1245-suai", "tetu1246"]
    E18 = ("mamb1306-Slete", "kema1243-kaila", "idat1237-cribas", "tetu1245-suai")
    X = {"Tetun": None, "Habu": ["habu1241"], "Kawaimina": ["waim1252", "midi1237", "naue1237"]}
    res = {}
    for xname in X:
        stable_ok, habu_other = [], []
        for m, k, i, t in product(mamb, kemak, idate, tetun if xname == "Tetun" else [None]):
            if (m, k, i, t or "tetu1245-suai") == E18:
                continue
            C = [t] if xname == "Tetun" else X[xname]
            r = triplet(sets_of, attested, stable, [i, "laka1255"], [m, k, "tuku1254"], C, ("LI", "NCT", xname))
            stable_ok.append(r["stable"]["ab_strictly_largest"])
            if xname == "Habu":
                c = r["other"]["counts"]
                habu_other.append(c["LI+Habu"] >= c["LI+NCT"])
        res[xname] = dict(combinations=len(stable_ok), share_LI_NCT_largest_on_stable=round(float(np.mean(stable_ok)), 3))
        if xname == "Habu":
            res[xname]["share_LI_Habu_at_least_LI_NCT_on_other"] = round(float(np.mean(habu_other)), 3)
    ctrl = []
    for m, k, t in product(mamb, kemak, tetun):
        r = triplet(sets_of, attested, stable, ["west2547-mahein"], [m, k, "tuku1254"], [t], ("Welaun", "NCT", "Tetun"))
        zo, zs = r["other"]["Z"], r["stable"]["Z"]
        ctrl.append(dict(ok=zo is not None and zo >= 2 and (zs is None or zo > zs), Z_other=zo, Z_stable=zs))
    res["Welaun-Mahein control"] = dict(combinations=len(ctrl), share_passing=round(float(np.mean([c["ok"] for c in ctrl])), 3),
                                        median_Z_other=float(np.median([c["Z_other"] or 0 for c in ctrl])),
                                        median_Z_stable=float(np.median([c["Z_stable"] or 0 for c in ctrl])))
    res["predictions"] = {
        "P1 Tetun": res["Tetun"]["share_LI_NCT_largest_on_stable"] >= 0.8,
        "P1 Habu": res["Habu"]["share_LI_NCT_largest_on_stable"] >= 0.8,
        "P1 Kawaimina": res["Kawaimina"]["share_LI_NCT_largest_on_stable"] >= 0.8,
        "P2 Habu borrowable": res["Habu"]["share_LI_Habu_at_least_LI_NCT_on_other"] >= 0.5,
        "P3 Welaun-Mahein control": res["Welaun-Mahein control"]["share_passing"] >= 0.8}
    res["rule"] = ic.RULE
    json.dump(res, open(os.path.join(LIT, f"e26_dialect_replication{ic.SUF}.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


# ---------------------------------------------------------------- E27
CODINGS = ["lexstat", "lexstat035", "lexstat075", "sca", "biglexstat"]
CLADES24 = {"LI + CT (with Welaun)": bayes.CT + ["idat1237-cribas", "laka1255"],
            "LI + Nuclear CT": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "idat1237-cribas", "laka1255"],
            "Timor-Babar": bayes.TB, "LI + Eastern Timor": te.LI + te.ET, "Central Timor (with Welaun)": bayes.CT,
            "Lakalei-Idate": te.LI}


def e27():
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import squareform
    taxa = bayes.BAYES_TAXA
    lab = {}
    base = None
    for m in CODINGS:
        rows = [r for r in variant_rows("d1", m, "primary") if r["Lect_ID"] in taxa]
        lab[m] = {r["Form_ID"]: r["Cognateset_ID"] for r in rows}
        if m == "lexstat":
            base = rows
    by_concept = defaultdict(list)
    for r in base:
        by_concept[r["Concept_ID"]].append(r)
    cons = []
    agree_of = {}
    for c, rs in by_concept.items():
        fids = [r["Form_ID"] for r in rs]
        n = len(fids)
        if n == 1:
            cons.append(dict(rs[0], Cognateset_ID=f"{c}-k1"))
            continue
        D = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                votes = [lab[m][fids[i]] == lab[m][fids[j]] for m in CODINGS if fids[i] in lab[m] and fids[j] in lab[m]]
                a = float(np.mean(votes)) if votes else 0.0
                D[i, j] = D[j, i] = 1 - a
        Z = linkage(squareform(D, checks=False), method="average")
        cl = fcluster(Z, t=0.2, criterion="distance")
        for r, k, i in zip(rs, cl, range(n)):
            cons.append(dict(r, Cognateset_ID=f"{c}-k{k}"))
        for i in range(n):
            agree_of[fids[i]] = {fids[j]: 1 - D[i, j] for j in range(n) if j != i}
    wd = os.path.join(LIT, "e27")
    os.makedirs(wd, exist_ok=True)
    write_csv(os.path.join(wd, "consensus_cognates.csv"), [dict(Form_ID=r["Form_ID"], Lect_ID=r["Lect_ID"],
              Concept_ID=r["Concept_ID"], Cognateset_ID=r["Cognateset_ID"]) for r in cons])
    nchar = phy(cons, taxa, os.path.join(wd, "lex_consensus.phy"))
    iqtree(os.path.join(wd, "lex_consensus.phy"), "lex_consensus", ("-B", "1000"))
    sup = splits_support(os.path.join(wd, "lex_consensus.splits.nex"), CLADES24)
    stable, _ = ex.stable_concepts()
    res = dict(characters=nchar, sets=len({r["Cognateset_ID"] for r in cons}), ufboot=sup)
    T = ic.T
    for rule_name, rule in (("R0", R0), ("R2", clf.chosen_rule() if os.environ.get("RETENTION_RULE") == "chosen"
                                          else json.load(open(os.path.join(LIT, "e30_classifier.json")))["chosen"])):
        status, _ = statuses(cons, rule)
        attested, sets_of = index(cons, status)
        res[f"triplets_{rule_name}"] = {f"(LI, NCT, {x})": triplet(sets_of, attested, stable, T["LI"], T["NCT"], T[x],
                                                                   ("LI", "NCT", x))
                                        for x in ("Tetun", "Habu", "Kawaimina", "Galoli")}
        res[f"triplets_{rule_name}"]["(Welaun, NCT, Tetun)"] = triplet(sets_of, attested, stable, T["Welaun"], T["NCT"],
                                                                       T["Tetun"], ("Welaun", "NCT", "Tetun"))
    res["expectation_TB_and_LI_ET_at_most_5"] = sup["Timor-Babar"] <= 5 and sup["LI + Eastern Timor"] <= 5
    json.dump(res, open(os.path.join(LIT, "e27_consensus.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    packet(agree_of)


def packet(agree_of):
    """Reviewer packet: every cognate set behind Lakalei-Idate's stable-concept triplet counts (primary coding, R0)."""
    stable, _ = ex.stable_concepts()
    lects, rows, members, status, segs = ic.classify()
    attested, sets_of = index(rows, status)
    T = ic.T
    pmp = ic.pmp_forms()
    concepts = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    seen = {}
    for x in ("Tetun", "Habu", "Kawaimina", "Galoli"):
        for a, b, c in product(T["LI"], T["NCT"], T[x]):
            for k in attested[a] & attested[b] & attested[c] & stable:
                sa, sb, sc = sets_of[(a, k)], sets_of[(b, k)], sets_of[(c, k)]
                for pair, ss in (("LI+NCT", (sa & sb) - sc), (f"LI+{x}", (sa & sc) - sb)):
                    for sid in ss:
                        seen.setdefault(sid, set()).add(pair)
    out = []
    for sid, pairs in sorted(seen.items()):
        rs = members[sid]
        fids = [r["Form_ID"] for r in rs]
        ag = [agree_of.get(f, {}).get(g) for f in fids for g in fids if f < g]
        ag = [a for a in ag if a is not None]
        out.append(dict(Cognateset_ID=sid, Concept=rs[0]["Concept_ID"], Counted_as=" ".join(sorted(pairs)),
                        Status=status[sid], PMP=" / ".join("".join(p) for p in pmp.get(concepts[rs[0]["Concept_ID"]], [])),
                        Mean_coding_agreement=round(float(np.mean(ag)), 2) if ag else "",
                        Forms="; ".join(f"{lects[r['Lect_ID']]['Name']}: {''.join(segs[r['Form_ID']])}" for r in rs
                                        if r["Lect_ID"] in bayes.BAYES_TAXA),
                        Specialist_verdict="", Notes=""))
    write_csv(os.path.join(REPO, "derived", "innovations", "reviewer_packet_lakalei_idate_stable.csv"), out)
    print("packet", len(out), "sets")


# ---------------------------------------------------------------- E28
SWAP = {"kema1243-kaila": "kema1243", "mamb1306-Slete": "mamb1306"}
DROP = ["west2547-welaun", "funa1237", "koto1251"]


def bib():
    txt = open(os.path.join(UP, "lexirumah", "cldf", "sources.bib"), encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", txt, re.S):
        body = m.group(2)
        f = {k.lower(): v.strip() for k, v in re.findall(r"(\w+)\s*=\s*\{(.*?)\},?\s*\n", body + "\n")}
        out[m.group(1).strip()] = f
    return out


def e28():
    B = bib()
    src = defaultdict(Counter)
    for r in read_csv(os.path.join(DATA, "d1", "forms.csv")):
        src[r["Lect_ID"]][r["Source"]] += 1
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    prov = []
    for t in bayes.BAYES_TAXA + list(SWAP.values()):
        keys = [k for s in src[t] for k in s.split(";")]
        people = []
        for k in dict.fromkeys(keys):
            e = B.get(k.strip(), {})
            people.append(f"{k.strip()} ({e.get('author', '?')}; collector {e.get('collector', e.get('author', '?'))}; "
                          f"{e.get('year', '?')})")
        text = " ".join(people)
        prov.append(dict(Lect=t, Name=lects[t]["Name"], Forms=sum(src[t].values()), Sources="; ".join(people),
                         Edwards_or_Grimes=bool(re.search(r"Edwards|Grimes", text))))
    write_csv(os.path.join(LIT, "e28_provenance.csv"), prov)
    taxa = [SWAP.get(t, t) for t in bayes.BAYES_TAXA if t not in DROP]
    rows = variant_rows("d1", "lexstat", "primary")
    wd = os.path.join(LIT, "e28")
    os.makedirs(wd, exist_ok=True)
    nchar = phy([r for r in rows if r["Lect_ID"] in taxa], taxa, os.path.join(wd, "lex_independent.phy"))
    iqtree(os.path.join(wd, "lex_independent.phy"), "lex_independent", ("-B", "1000"))
    nct = ["mamb1306", "kema1243", "tuku1254"]
    li = ["idat1237-cribas", "laka1255"]
    et = ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"]
    tb = [t for t in taxa if t not in nct + bayes.OUTGROUP]
    clades = {"LI + Nuclear CT": nct + li, "Timor-Babar (all Timor-region taxa outside Nuclear CT)": tb,
              "LI + Eastern Timor": li + et, "Nuclear CT": nct, "Lakalei-Idate": li}
    sup = splits_support(os.path.join(wd, "lex_independent.splits.nex"), clades)
    stable, _ = ex.stable_concepts()
    _, rows2, _, status, _ = ic.classify()
    attested, sets_of = index(rows2, status)
    X = {"Tetun": ["tetu1246", "tetu1245-suai"], "Habu": ["habu1241"], "Kawaimina": ["waim1252", "midi1237", "naue1237"]}
    trip = {f"(LI, NCT, {x})": triplet(sets_of, attested, stable, ["idat1237", "laka1255"], nct, X[x], ("LI", "NCT", x))
            for x in X}
    res = dict(taxa=taxa, characters=nchar, ufboot=sup, triplets_single_survey=trip,
               edwards_or_grimes_lects=[p["Lect"] for p in prov if p["Edwards_or_Grimes"]],
               predictions={"P4 " + x: trip[f"(LI, NCT, {x})"]["stable"]["ab_strictly_largest"] for x in X},
               rule=ic.RULE)
    res["predictions"]["P5 Timor-Babar and LI+ET <= 5"] = (sup["Timor-Babar (all Timor-region taxa outside Nuclear CT)"]
                                                           <= 5 and sup["LI + Eastern Timor"] <= 5)
    json.dump(res, open(os.path.join(LIT, f"e28_independent{ic.SUF}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


def e28b():
    """Post hoc, after E28: is the Lakalei + Nuclear CT signal a same-collector effect (Klamer 2002 lists)?
    (a) E28 taxa minus Galoli (30 of its forms are co-collected by Grimes); (b) Idate from Klamer 2002 and Tetun Dili
    from Klamer 2002 added, so all six of that survey's lists are present."""
    rows = variant_rows("d1", "lexstat", "primary")
    base = [SWAP.get(t, t) for t in bayes.BAYES_TAXA if t not in DROP]
    sets = {"a_no_galoli": [t for t in base if t != "galo1243"],
            "b_klamer_survey": [t for t in base if t != "idat1237-cribas"] + ["idat1237", "tetu1246"],
            "c_both_idate_both_tetun": base + ["idat1237", "tetu1246"]}
    wd = os.path.join(LIT, "e28")
    out = {}
    for name, taxa in sets.items():
        phy([r for r in rows if r["Lect_ID"] in taxa], taxa, os.path.join(wd, f"lex_{name}.phy"))
        iqtree(os.path.join(wd, f"lex_{name}.phy"), f"lex_{name}", ("-B", "1000"))
        nct = ["mamb1306", "kema1243", "tuku1254"]
        li = [t for t in taxa if t.startswith("idat") or t == "laka1255"]
        clades = {"LI + Nuclear CT": nct + li, "Nuclear CT": nct, "Lakalei-Idate": li,
                  "Lakalei + Nuclear CT": nct + ["laka1255"], "Klamer 2002 lists": [t for t in taxa if t in
                  ("mamb1306", "kema1243", "tuku1254", "idat1237", "laka1255", "tetu1246")],
                  "Tetun Dili + Tetun Suai": ["tetu1246", "tetu1245-suai"],
                  "Timor-Babar": [t for t in taxa if t not in nct + bayes.OUTGROUP],
                  "LI + Eastern Timor": li + [t for t in taxa if t in ("tetu1245-suai", "tetu1246", "habu1241", "waim1252",
                                                                     "midi1237", "naue1237")]}
        out[name] = dict(taxa=taxa, ufboot=splits_support(os.path.join(wd, f"lex_{name}.splits.nex"), clades))
        print(name, out[name]["ufboot"], flush=True)
    json.dump(out, open(os.path.join(LIT, "e28b_collector_check.json"), "w"), indent=1)


# ---------------------------------------------------------------- E29
HULL_CHARS = [("b_h_initial", "b", "initial", {"h", "∅"}), ("k_lost_initial", "k", "initial", {"∅", "glottal stop"}),
              ("k_lost_medial", "k", "medial", {"∅", "glottal stop"})]


def fitch(tree, states):
    """Fitch length of one binary character with '?' as missing, on a Bio.Phylo tree."""
    steps = 0

    def go(c):
        nonlocal steps
        if c.is_terminal():
            v = states.get(c.name, "?")
            return {"0", "1"} if v not in ("0", "1") else {v}
        sets = [go(ch) for ch in c.clades]
        cur = sets[0]
        for s in sets[1:]:
            inter = cur & s
            if inter:
                cur = inter
            else:
                cur = cur | s
                steps += 1
        return cur
    go(tree.root)
    return steps


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 2), round((c + h) / d, 2)]


def e29():
    from Bio import Phylo
    wd = os.path.join(LIT, "e29")
    os.makedirs(wd, exist_ok=True)
    lex = os.path.join(RES, "total_evidence", "lex.phy")
    ct = bayes.CT
    other = [t for t in bayes.BAYES_TAXA if t not in ct + bayes.OUTGROUP]
    cons = os.path.join(wd, "constraint_GE.nwk")
    open(cons, "w").write("((" + ",".join(tx(t) for t in ct) + "),(" + ",".join(tx(t) for t in other) + "),"
                          + ",".join(tx(t) for t in bayes.OUTGROUP) + ");\n")
    open(os.path.join(wd, "lex.phy"), "w").write(open(lex).read())
    if not os.path.exists(os.path.join(wd, "GE.treefile")):
        iqtree(os.path.join(wd, "lex.phy"), "GE", ("-g", "constraint_GE.nwk"))
    trees = {"H (unconstrained ML)": os.path.join(RES, "total_evidence", "lex_only.treefile"),
             "G (LI + Eastern Timor)": os.path.join(LIT, "e21_abc", "G.treefile"),
             "GE (Central Timor | rest)": os.path.join(wd, "GE.treefile")}
    lnls = {"H (unconstrained ML)": lnl(os.path.join(RES, "total_evidence", "lex_only.iqtree")),
            "G (LI + Eastern Timor)": lnl(os.path.join(LIT, "e21_abc", "G.iqtree")),
            "GE (Central Timor | rest)": lnl(os.path.join(wd, "GE.iqtree"))}
    mat = {r["Taxon"]: r for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                          "innovation_matrix_24_hull.csv"))}
    chars = [c[0] for c in inn.CHARS] + [c[0] for c in HULL_CHARS]
    res = dict(characters=chars, trees={})
    for name, path in trees.items():
        t = Phylo.read(path, "newick")
        per = {ch: fitch(t, {tx(k): v[ch] for k, v in mat.items()}) for ch in chars}
        res["trees"][name] = dict(total_steps=sum(per.values()), per_character=per, lexical_lnL=lnls[name])
    h = res["trees"]["H (unconstrained ML)"]
    for name in trees:
        r = res["trees"][name]
        r["steps_minus_H"] = r["total_steps"] - h["total_steps"]
        r["lnL_minus_H"] = round(r["lexical_lnL"] - h["lexical_lnL"], 2) if r["lexical_lnL"] and h["lexical_lnL"] else None
    # E29b: tokens behind Idate and Lakalei's cells
    exp = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"))
    auto = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "automatic_tokens.csv"))
    alc = read_csv(os.path.join(REPO, "derived", "alcantara2015_idate", "tokens.csv"))
    defs = [(n, tg, None, st) for n, tg, st in inn.CHARS] + HULL_CHARS
    cells = {}
    for who, gl, lids, use_alc in (("Idate", "idat1237", {"idat1237", "idat1237-cribas"}, True),
                                   ("Lakalei", "laka1255", {"laka1255"}, False)):
        for name, tg, pos, st in defs:
            counts = {}
            for srcname, toks, keep in (("expert", exp, lambda r: r["Glottocode"] == gl),
                                        ("automatic", auto, lambda r: r["Lect_ID"] in lids),
                                        ("alcantara", alc if use_alc else [], lambda r: True)):
                sel = [r for r in toks if keep(r) and r["Target"] == tg and (pos is None or r["Position"] == pos)
                       and r["Class"] not in ("", "other")]
                counts[srcname] = (sum(r["Class"] in st for r in sel), len(sel))
            k = sum(v[0] for v in counts.values())
            n = sum(v[1] for v in counts.values())
            cells[f"{who} {name}"] = dict(with_change=k, tokens=n, share=round(k / n, 2) if n else None,
                                          wilson95=wilson(k, n), by_source={s: list(v) for s, v in counts.items()},
                                          coded=mat["idat1237-cribas" if who == "Idate" else "laka1255"][name])
    res["E29b_tokens"] = cells
    json.dump(res, open(os.path.join(LIT, "e29_sound_fit.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: (v["total_steps"], v["steps_minus_H"], v["lnL_minus_H"]) for k, v in res["trees"].items()}))
    for k, v in cells.items():
        print(k, v["with_change"], "/", v["tokens"], v["wilson95"], "coded", v["coded"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    for name, fn in (("e25", e25), ("e26", e26), ("e27", e27), ("e28", e28), ("e28b", e28b), ("e29", e29)):
        if cmd in (name, "all"):
            fn()
