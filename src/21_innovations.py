"""E10b (A4.4): binary diagnostic innovations from the expert reflex atlas.

Characters follow the changes Grimes and Edwards (2026) use to define or support subgroups:
  p_lenited    *p > h, ʔ, ∅          (Timor-Babar)
  ng_velar     *ŋ > g, k             (Central Timor)
  ng_n         *ŋ > n                (Eastern Timor; Timor-Babar per Edwards 2019)
  j_rhotic     *j > r                (Eastern Timor)
  j_l          *j > l                (Central Timor; some Lakalei-Idate words)
  R_zero       *R > ∅                (Eastern Timor; supporting for Central Timor)
  b_lenited    *b > h or labial fricative (Central Timor; Lakalei-Idate)
  d_liquid     *d > r or l           (Central Timor)
A language is coded 1 if its majority reflex class (>= 2 expert tokens) is in the set, 0 if another class, ? if unknown.

Writes derived/sound_change_matrix/innovation_profiles.csv (every language in the Timor-Babar and Central Timor
chapters) and runs IQ-TREE on the 24 step-7 taxa: innovations alone, and lexical + innovations.

    python3 src/21_innovations.py
"""
import importlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, RES, read_csv, write_csv  # noqa: E402

te = importlib.import_module("20_total_evidence")
OUT = os.path.join(REPO, "derived", "sound_change_matrix")
TE = os.path.join(RES, "total_evidence")
IQ = os.environ.get("IQTREE", "iqtree2")

CHARS = [
    ("p_lenited", "p", {"h", "glottal stop", "∅"}),
    ("ng_velar", "ŋ", {"velar stop"}),
    ("ng_n", "ŋ", {"n"}),
    ("j_rhotic", "j", {"rhotic"}),
    ("j_l", "j", {"l"}),
    ("R_zero", "R", {"∅"}),
    ("b_lenited", "b", {"h", "labial fricative"}),
    ("d_liquid", "d", {"rhotic", "l"}),
]


def counts_by(key_fn, tokens):
    c = defaultdict(Counter)
    for r in tokens:
        if r["Class"] not in ("", "other"):
            for k in key_fn(r):
                c[(k, r["Target"])][r["Class"]] += 1
    return c


def code(counter):
    if not counter or sum(counter.values()) < 2:
        return None
    return counter.most_common(1)[0][0]


def profiles():
    toks = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"))
    forms = read_csv(os.path.join(REPO, "derived", "ge2026_tables", "forms.csv"))
    timor = {f["Glottocode"] for f in forms if f["Glottocode"] and f["File"][:3] in ("04-", "05-")}
    labels = defaultdict(set)
    for f in forms:
        if f["Glottocode"] in timor:
            labels[f["Glottocode"]].add(f["Language"])
    c = counts_by(lambda r: [r["Glottocode"]], toks)
    rows = []
    for g in sorted(timor):
        row = dict(Glottocode=g, Labels="; ".join(sorted(labels[g])))
        for name, tgt, states in CHARS:
            cl = code(c.get((g, tgt)))
            row[name] = "?" if cl is None else int(cl in states)
            row[name + "_tokens"] = sum(c.get((g, tgt), Counter()).values())
        rows.append(row)
    write_csv(os.path.join(OUT, "innovation_profiles.csv"), rows)
    return rows


def taxon_matrix():
    toks = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"))
    g2t = defaultdict(list)
    for t, gs in te.TAXON_GLOTTO.items():
        for g in gs:
            g2t[g].append(t)
    c = counts_by(lambda r: g2t.get(r["Glottocode"], []), toks)
    mat = {}
    for t in te.TAXON_GLOTTO:
        mat[t] = []
        for name, tgt, states in CHARS:
            cl = code(c.get((t, tgt)))
            mat[t].append("?" if cl is None else str(int(cl in states)))
    write_csv(os.path.join(OUT, "innovation_matrix_24.csv"),
              [dict(Taxon=t, **{n: v for (n, _, _), v in zip(CHARS, r)}) for t, r in mat.items()])
    return mat


def run_trees(mat):
    os.makedirs(TE, exist_ok=True)
    keep = {t: r for t, r in mat.items() if any(x != "?" for x in r)}  # IQ-TREE rejects all-missing rows
    with open(os.path.join(TE, "innov.phy"), "w") as fh:
        fh.write(f"{len(keep)} {len(CHARS)}\n")
        for t, r in keep.items():
            fh.write(f"{te.tx(t)} {''.join(r)}\n")
    nlex = te.lexical_phy(os.path.join(TE, "lex.phy"))
    base = [IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000"]
    subprocess.run(base + ["-s", "innov.phy", "-st", "BIN", "-m", "GTR2+FO", "-pre", "innov"], cwd=TE, check=True)
    open(os.path.join(TE, "te_innov.nex"), "w").write(
        "#nexus\nbegin sets;\n"
        f"  charset lex = lex.phy: 1-{nlex};\n  charset inn = innov.phy: 1-{len(CHARS)};\n"
        "  charpartition mine = GTR2+FO+G4:lex, GTR2+FO:inn;\nend;\n")
    subprocess.run(base + ["-p", "te_innov.nex", "-pre", "te_innov"], cwd=TE, check=True)
    res = dict(innovations_only=te.support_from_splits(os.path.join(TE, "innov.splits.nex")),
               lexical_plus_innovations=te.support_from_splits(os.path.join(TE, "te_innov.splits.nex")))
    json.dump(res, open(os.path.join(TE, "innovation_support.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    prof = profiles()
    print(len(prof), "Timor-region languages profiled")
    mat = taxon_matrix()
    for t, r in mat.items():
        print(f"{t:18s} {' '.join(r)}")
    run_trees(mat)
