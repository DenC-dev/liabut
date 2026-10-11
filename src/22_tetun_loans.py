"""E12 (Addendum 4): Tetun loans identified by sound change, and a rerun without them.

For each Tetun look-alike (L5) in a non-Tetun Timor lect, the automatic reflexes of that form (E9 tokens) are compared
with the lect's own expert majority reflex and with Tetun's (E8), target by target. Only targets where the lect and
Tetun differ are diagnostic.
  probable loan       some diagnostic target follows Tetun, none follows the lect
  probably inherited  some diagnostic target follows the lect, none follows Tetun
  conflicting         both
  undecidable         no diagnostic target in the form

Writes derived/loans/tetun_loans.csv and results/total_evidence/loan_rerun.json.

    python3 src/22_tetun_loans.py
"""
import importlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import (DATA, REPO, RES, SEED, bootstrap_support, cognate_tensors, read_csv,  # noqa: E402
                    write_csv)
from pipeline import variant_rows  # noqa: E402

te = importlib.import_module("20_total_evidence")
bayes = importlib.import_module("09_bayes")
ra = importlib.import_module("19_reflex_atlas")
OUT = os.path.join(REPO, "derived", "loans")
TE = os.path.join(RES, "total_evidence")
TETUN = ["tetu1245", "east2473", "sout2898", "nort2869"]
IQ = os.environ.get("IQTREE", "iqtree2")


def majority(cells, glottocodes, target, position):
    for key in [(g, target, position) for g in glottocodes] + [(g, target, None) for g in glottocodes]:
        c = cells.get(key)
        if c and sum(c.values()) >= 2:
            return c.most_common(1)[0][0]
    return None


def classify():
    exp = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"))
    cells = defaultdict(Counter)
    for r in exp:
        if r["Class"] in ("", "other"):
            continue
        cells[(r["Glottocode"], r["Target"], r["Position"])][r["Class"]] += 1
        cells[(r["Glottocode"], r["Target"], None)][r["Class"]] += 1
    auto = defaultdict(list)
    for t in read_csv(os.path.join(REPO, "derived", "reflex_atlas", "automatic_tokens.csv")):
        auto[t["Form_ID"]].append(t)
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}
    flags = [f for f in read_csv(os.path.join(RES, "loans", "d1_flags.csv")) if f["L5_tetun"] == "True"]
    rows = []
    for f in flags:
        g = lects[f["Lect_ID"]]["Glottocode"]
        own = ra.groups_for(g)
        loan_ev, inh_ev = [], []
        for t in auto.get(f["Form_ID"], []):
            mine = majority(cells, own, t["Target"], t["Position"])
            tet = majority(cells, TETUN, t["Target"], t["Position"])
            if not mine or not tet or mine == tet:
                continue
            if t["Class"] == tet:
                loan_ev.append(f"*{t['Target']}>{t['Class']} (Tetun) vs {mine} ({lects[f['Lect_ID']]['Name']})")
            elif t["Class"] == mine:
                inh_ev.append(f"*{t['Target']}>{t['Class']} (own) vs {tet} (Tetun)")
        verdict = ("probable loan" if loan_ev and not inh_ev else "probably inherited" if inh_ev and not loan_ev
                   else "conflicting" if loan_ev else "undecidable")
        rows.append(dict(Form_ID=f["Form_ID"], Lect_ID=f["Lect_ID"], Lect=lects[f["Lect_ID"]]["Name"],
                         Concept_ID=f["Concept_ID"], Form=f["Form"], Tetun_Match=f["L5_match"], Verdict=verdict,
                         Loan_Evidence="; ".join(loan_ev), Inherited_Evidence="; ".join(inh_ev)))
    os.makedirs(OUT, exist_ok=True)
    write_csv(os.path.join(OUT, "tetun_loans.csv"), rows)
    print(Counter(r["Verdict"] for r in rows))
    by = defaultdict(Counter)
    for r in rows:
        by[r["Lect"]][r["Verdict"]] += 1
    for l, c in sorted(by.items(), key=lambda x: -x[1]["probable loan"])[:12]:
        print(f"  {l:30s} {dict(c)}")
    return {r["Form_ID"] for r in rows if r["Verdict"] == "probable loan"}


def rerun(loans):
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if r["Form_ID"] not in loans]
    lects_all = [r["ID"] for r in read_csv(os.path.join(DATA, "d1", "lects.csv"))]
    per = Counter()
    for r in {(r["Lect_ID"], r["Concept_ID"]) for r in rows}:
        per[r[0]] += 1
    lects = [l for l in lects_all if per[l] >= 100]
    concepts = sorted({r["Concept_ID"] for r in rows})
    S, A = cognate_tensors(rows, lects, concepts)
    hyp = {r["ID"]: r for r in read_csv(os.path.join(REPO, "reference", "hypotheses.csv"))}
    hyp.update({r["ID"]: r for r in read_csv(os.path.join(REPO, "reference", "hypotheses_addendum2.csv"))})
    ids = ["HULL-R", "EDW-CT", "GE-NCT", "EDW-LI", "EDW-TB", "GE-ETLI", "HULL98-W"]
    groups = []
    for h in ids:
        prune = set(hyp[h]["Prune"].split())
        keep = [l for l in lects if l not in prune]
        groups.append([keep.index(x) for x in hyp[h]["Members"].split() if x in keep])
    out = {}
    # bootstrap needs one lect set per clade because of pruning; run per clade
    for h, g in zip(ids, groups):
        prune = set(hyp[h]["Prune"].split())
        keep_idx = [i for i, l in enumerate(lects) if l not in prune]
        Sk, Ak = S[:, keep_idx][:, :, keep_idx], A[:, keep_idx][:, :, keep_idx]
        u = bootstrap_support(Sk, Ak, [g], 1000, SEED, "upgma")[0]
        n = bootstrap_support(Sk, Ak, [g], 1000, SEED, "nj")[0]
        out[h] = dict(UPGMA=round(float(u), 3), NJ=round(float(n), 3))
    # ML on the 24 taxa without probable loans
    attested, sets, concept_of = defaultdict(set), defaultdict(set), {}
    for r in rows:
        if r["Lect_ID"] in bayes.BAYES_TAXA:
            attested[r["Lect_ID"]].add(r["Concept_ID"])
            sets[r["Cognateset_ID"]].add(r["Lect_ID"])
            concept_of[r["Cognateset_ID"]] = r["Concept_ID"]
    chars = sorted(sets, key=lambda s: (concept_of[s], s))
    with open(os.path.join(TE, "lex_noloans.phy"), "w") as fh:
        fh.write(f"{len(bayes.BAYES_TAXA)} {len(chars)}\n")
        for t in bayes.BAYES_TAXA:
            fh.write(f"{te.tx(t)} " + "".join(("1" if t in sets[s] else "0") if concept_of[s] in attested[t] else "?"
                                               for s in chars) + "\n")
    subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000", "-s", "lex_noloans.phy",
                    "-m", "GTR2+FO+G4", "-pre", "lex_noloans"], cwd=TE, check=True)
    res = dict(probable_loans_removed=len(loans), lects=len(lects), concepts=len(concepts), bootstrap=out,
               ML_ufboot=te.support_from_splits(os.path.join(TE, "lex_noloans.splits.nex")))
    json.dump(res, open(os.path.join(TE, "loan_rerun.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    loans = classify()
    rerun(loans)
