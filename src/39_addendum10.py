"""Addendum 10: E35 (words inherited from above the Timor groups, from the Austronesian Comparative Dictionary)
and E36 (AU topology tests on the E28 data independent of Grimes and Edwards).

    python3 src/39_addendum10.py e35|e35_strict|e36|all     (e35_strict is post hoc: exact-sense gloss matches)
Needs data/upstream/acd (src/01_fetch.sh) and, for E36, IQ-TREE ($IQTREE).
"""
import importlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, UP, ned, read_csv, sca_string, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

a9 = importlib.import_module("34_addendum9")
ic = a9.ic
ex = a9.ex
clf = a9.clf
ra = importlib.import_module("19_reflex_atlas")
LIT = os.path.join(RES, "literature")
ACD = os.path.join(UP, "acd", "cldf")
LEVELS = ("PAN", "PMP", "PCEMP", "PCMP")
IQ = os.environ.get("IQTREE", "iqtree2")


# ---------------------------------------------------------------- E35
def keyword(english):
    g = re.sub(r"\(.*?\)", " ", english.split(";")[0]).replace("?", " ")
    words = [w for w in re.findall(r"[a-z]+", g.lower()) if w not in ("to", "the", "a")]
    return words[0] if words else None


def clean_etymon(form):
    f = re.sub(r"[₀-₉0-9]", "", form)
    f = f.replace("*", "")
    toks = ra.clean_pmp(f)
    return toks


def senses(gloss):
    out = []
    for part in re.split(r"[;,]", re.sub(r"\(.*?\)", " ", gloss)):
        w = re.sub(r"[^a-z ]", " ", part.lower()).split()
        while w and w[0] in ("to", "the", "a", "an", "be"):
            w = w[1:]
        if w:
            out.append(" ".join(w))
    return out


def acd_etyma(strict=False):
    """concept_id -> [(level, name, tokens)] for PAN/PMP/PCEMP/PCMP etyma whose gloss contains the concept keyword
    (the pre-declared rule). strict=True (post hoc): some sense of the gloss must be exactly the keyword."""
    concepts = read_csv(os.path.join(DATA, "d1", "concepts.csv"))
    kws = {c["ID"]: keyword(c["English"]) for c in concepts}
    sets = read_csv(os.path.join(ACD, "cognatesets.csv"))
    out = defaultdict(list)
    for s in sets:
        m = re.match(r"(\w+)\s+(\*\S+(?:\s+\S+)*?)\s+'(.*)'\s*$", s["Name"])
        if not m or m.group(1) not in LEVELS:
            continue
        level, form, gloss = m.group(1), m.group(2), m.group(3).lower()
        if " " in form.strip():
            continue      # phrases ('*qiteluR ni manuk') are not single words
        toks = clean_etymon(form)
        if not toks:
            continue
        for cid, kw in kws.items():
            if not kw or kw in ("pl", "sg"):
                continue
            hit = kw in senses(gloss) if strict else re.search(rf"\b{re.escape(kw)}\b", gloss)
            if hit:
                out[cid].append((level, s["Name"], toks))
    return out


def e35(strict=False):
    suf = "_strict" if strict else ""
    rule = json.load(open(os.path.join(LIT, "e30_classifier.json")))["chosen"]
    stable, _ = ex.stable_concepts()
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    glotto = {k: v["Glottocode"] for k, v in lects.items()}
    concepts = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in read_csv(os.path.join(DATA, "d1", "concepts.csv"))}
    segs = {f["ID"]: [t for t in f["Segments"].split() if t not in "+_"]
            for f in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    pmp = ic.pmp_forms()
    ety = acd_etyma(strict)
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if lects[r["Lect_ID"]]["Role"] != "TAP"
            and pmp.get(concepts.get(r["Concept_ID"]))]
    members = defaultdict(list)
    for r in rows:
        members[r["Cognateset_ID"]].append(r)

    def best(rs, refs):
        b, which = 9.0, None
        for lab, p in refs:
            for r in rs:
                toks = segs[r["Form_ID"]]
                if not toks:
                    continue
                d = ned(sca_string(clf.predicted(p, r["Lect_ID"], glotto.get(r["Lect_ID"], ""))), sca_string(toks))
                if d < b:
                    b, which = d, lab
        return b, which
    base, enlarged, moved = {}, {}, []
    for sid, rs in members.items():
        c = rs[0]["Concept_ID"]
        b0, _ = best(rs, [("ABVD PMP", p) for p in pmp[concepts[c]]])
        base[sid] = "retention" if b0 <= rule["t"] else "innovation"
        refs = [("ABVD PMP", p) for p in pmp[concepts[c]]] + [(name, toks) for _, name, toks in ety.get(c, [])]
        b1, which = best(rs, refs)
        enlarged[sid] = "retention" if b1 <= rule["t"] else "innovation"
        if base[sid] != enlarged[sid]:
            moved.append(dict(Cognateset_ID=sid, Concept=c, Etymon=which, NED=round(b1, 3),
                              Lects=" ".join(sorted({r["Lect_ID"] for r in rs})),
                              Forms="; ".join(f"{r['Lect_ID']}:{''.join(segs[r['Form_ID']])}" for r in rs)[:400]))
    write_csv(os.path.join(LIT, f"e35_reclassified_sets{suf}.csv"), moved)
    # triplets with the enlarged statuses
    T = ic.T
    res = dict(rule=rule, concepts_with_acd_etyma=sum(1 for c in set(concepts) if ety.get(c)),
               acd_etyma_used=sum(len(v) for v in ety.values()), sets=len(members),
               innovations_before=sum(v == "innovation" for v in base.values()),
               innovations_after=sum(v == "innovation" for v in enlarged.values()), moved=len(moved))
    for name, status in (("R2_ABVD_only", base), ("R2_with_ACD", enlarged)):
        att, so = a9.index(rows, status)
        trip = {f"(LI, NCT, {x})": a9.triplet(so, att, stable, T["LI"], T["NCT"], T[x], ("LI", "NCT", x))
                for x in ("Tetun", "Habu", "Kawaimina", "Galoli")}
        trip["(Welaun, NCT, Tetun)"] = a9.triplet(so, att, stable, T["Welaun"], T["NCT"], T["Tetun"],
                                                  ("Welaun", "NCT", "Tetun"))
        indep = {f"(LI, NCT, {x})": a9.triplet(so, att, stable, ["idat1237", "laka1255"],
                                                ["mamb1306", "kema1243", "tuku1254"], lst, ("LI", "NCT", x))
                 for x, lst in (("Tetun", ["tetu1246", "tetu1245-suai"]), ("Habu", ["habu1241"]),
                                ("Kawaimina", ["waim1252", "midi1237", "naue1237"]))}
        res[name] = dict(representative=trip, single_survey=indep)
    after = res["R2_with_ACD"]
    res["stable_pairing_stands"] = all(after[k][f"(LI, NCT, {x})"]["stable"]["ab_strictly_largest"]
                                       for k in ("representative", "single_survey") for x in ("Habu", "Kawaimina"))
    # annotate the reviewer packet
    pk = os.path.join(REPO, "derived", "innovations", "reviewer_packet_lakalei_idate_stable.csv")
    packet = read_csv(pk)
    tag = "ACD_strict" if strict else "ACD"
    for row in packet:
        rs = members.get(row["Cognateset_ID"], [])
        refs = [(name, toks) for _, name, toks in ety.get(row["Concept"], [])]
        b, which = best(rs, refs) if refs and rs else (9.0, None)
        row[f"{tag}_best_etymon"] = which or ""
        row[f"{tag}_NED"] = round(b, 3) if which else ""
        row[f"Status_with_{tag}"] = enlarged.get(row["Cognateset_ID"], "")
    cols = ["Cognateset_ID", "Concept", "Counted_as", "Status", "Status_with_ACD", "ACD_best_etymon", "ACD_NED",
            "Status_with_ACD_strict", "ACD_strict_best_etymon", "ACD_strict_NED", "PMP",
            "Mean_coding_agreement", "Forms", "Specialist_verdict", "Notes"]
    for row in packet:
        for c in cols:
            row.setdefault(c, "")
    write_csv(pk, packet, header=cols)
    res["packet_sets_reclassified"] = [r["Cognateset_ID"] for r in packet if r[f"Status_with_{tag}"] == "retention"]
    json.dump(res, open(os.path.join(LIT, f"e35_acd_check{suf}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in res.items() if k not in ("R2_ABVD_only", "R2_with_ACD")}, indent=1))
    for name in ("R2_ABVD_only", "R2_with_ACD"):
        for grp in ("representative", "single_survey"):
            for k, v in res[name][grp].items():
                print(name, grp, k, v["stable"]["counts"], v["other"]["counts"])


# ---------------------------------------------------------------- E36
def e36():
    wd = os.path.join(LIT, "e28")
    phy = os.path.join(wd, "lex_independent.phy")
    taxa = [l.split()[0] for l in open(phy).read().splitlines()[1:]]
    tx = a9.tx
    nct = [tx(t) for t in ("mamb1306", "kema1243", "tuku1254")]
    li = [tx(t) for t in ("idat1237-cribas", "laka1255")]
    et = [tx(t) for t in ("tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237")]
    out_g = [tx(t) for t in ("lama1277-lewoi", "sika1262-hewa")]
    tb = [t for t in taxa if t not in nct + out_g]

    def constraint(name, group):
        rest = [t for t in taxa if t not in group]
        path = os.path.join(wd, f"{name}.constr")
        open(path, "w").write("((" + ",".join(group) + ")," + ",".join(rest) + ");\n")
        return path
    trees = {}
    for name, group in (("li_eastern_timor", li + et), ("timor_babar", tb)):
        constraint(name, group)
        subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-s", "lex_independent.phy",
                        "-m", "GTR2+FO+G4", "-g", f"{name}.constr", "-pre", f"au_{name}"], cwd=wd, check=True)
        trees[name] = open(os.path.join(wd, f"au_{name}.treefile")).read().strip()
    trees = {"free": open(os.path.join(wd, "lex_independent.treefile")).read().strip(), **trees}
    open(os.path.join(wd, "au_candidates.trees"), "w").write("\n".join(trees.values()) + "\n")
    subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-s", "lex_independent.phy",
                    "-m", "GTR2+FO+G4", "-te", "lex_independent.treefile", "-z", "au_candidates.trees",
                    "-zb", "10000", "-au", "-n", "0", "-pre", "au_test"], cwd=wd, check=True)
    txt = open(os.path.join(wd, "au_test.iqtree")).read()
    block = txt.split("USER TREES")[1]
    res = {}
    for name, line in zip(trees, [l for l in block.splitlines() if re.match(r"\s+\d+\s+-?\d", l)]):
        f = line.split()
        res[name] = dict(logL=float(f[1]), deltaL=float(f[2]), p_AU=float(f[-2]),
                         rejected=f[-1] == "-")
    json.dump(res, open(os.path.join(LIT, "e36_au_independent.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("e35", "all"):
        e35()
    if cmd in ("e35_strict", "all"):
        e35(strict=True)    # post hoc: exact-sense gloss match
    if cmd in ("e36", "all"):
        e36()
