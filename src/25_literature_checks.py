"""Addendum 5: checks prompted by the literature scan (results/LITERATURE.md).

E13  Hull's Ramelaic sound changes (*b, *k) as extra binary characters, added to the eight of E10b.
E14  An independent Idaté wordlist (ASJP v21, from Purwa et al. 1994) compared with Timor lists by LDND.

    python3 src/25_literature_checks.py e13
    python3 src/25_literature_checks.py e13s     # sensitivity, not pre-declared
    python3 src/25_literature_checks.py e14 <path to a clone of github.com/lexibank/asjp>
"""
import csv
import importlib
import json
import os
import random
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, RES, read_csv, write_csv  # noqa: E402

te = importlib.import_module("20_total_evidence")
inn = importlib.import_module("21_innovations")
OUT = os.path.join(REPO, "derived", "sound_change_matrix")
TE = os.path.join(RES, "total_evidence")
LIT = os.path.join(RES, "literature")
IQ = os.environ.get("IQTREE", "iqtree2")

# E13: (name, PMP target, position, classes that count as the change)
NEW = [
    ("b_h_initial", "b", "initial", {"h", "∅"}),
    ("k_lost_initial", "k", "initial", {"∅", "glottal stop"}),
    ("k_lost_medial", "k", "medial", {"∅", "glottal stop"}),
]


def _cells(path, key):
    c = defaultdict(Counter)
    for r in read_csv(path):
        if r["Class"] not in ("", "other"):
            c[(r[key], r["Target"], r["Position"])][r["Class"]] += 1
    return c


def _code(expert, auto, glottocodes, tgt, pos, states):
    """Expert majority (>= 2 tokens), else automatic majority (>= 2 tokens). Returns (value, source, n)."""
    for src, cells in (("expert", expert), ("automatic", auto)):
        c = Counter()
        for g in glottocodes:
            c.update(cells.get((g, tgt, pos), Counter()))
        n = sum(c.values())
        if n >= 2:
            return int(c.most_common(1)[0][0] in states), src, n
    return None, "", 0


def e13():
    expert = _cells(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"), "Glottocode")
    auto = _cells(os.path.join(REPO, "derived", "reflex_atlas", "automatic_tokens.csv"), "Glottocode")
    # profiles for every Timor-region language in the E10b profile file
    prof = read_csv(os.path.join(OUT, "innovation_profiles.csv"))
    rows = []
    for p in prof:
        row = dict(Glottocode=p["Glottocode"], Labels=p["Labels"])
        for name, tgt, pos, states in NEW:
            v, src, n = _code(expert, auto, [p["Glottocode"]], tgt, pos, states)
            row[name] = "?" if v is None else v
            row[name + "_source"] = src
            row[name + "_tokens"] = n
        rows.append(row)
    write_csv(os.path.join(OUT, "hull_ramelaic_profiles.csv"), rows)
    # 24-taxon matrix: E10b's eight characters plus the three new ones
    old = {r["Taxon"]: r for r in read_csv(os.path.join(OUT, "innovation_matrix_24.csv"))}
    names8 = [c[0] for c in inn.CHARS]
    mat, out = {}, []
    for t, gs in te.TAXON_GLOTTO.items():
        new = []
        rec = dict(Taxon=t, **{n: old[t][n] for n in names8})
        for name, tgt, pos, states in NEW:
            v, src, n = _code(expert, auto, gs, tgt, pos, states)
            new.append("?" if v is None else str(v))
            rec[name] = new[-1]
            rec[name + "_source"] = src
        mat[t] = [old[t][n] for n in names8] + new
        out.append(rec)
    write_csv(os.path.join(OUT, "innovation_matrix_24_hull.csv"), out)
    for r in out:
        print(f"{r['Taxon']:18s}", " ".join(r[n] for n in names8), "|",
              " ".join(f"{r[n]}{'a' if r[n + '_source'] == 'automatic' else ''}" for n, *_ in NEW))
    # trees
    keep = {t: r for t, r in mat.items() if any(x != "?" for x in r)}
    nchar = len(names8) + len(NEW)
    with open(os.path.join(TE, "innov11.phy"), "w") as fh:
        fh.write(f"{len(keep)} {nchar}\n")
        for t, r in keep.items():
            fh.write(f"{te.tx(t)} {''.join(r)}\n")
    nlex = te.lexical_phy(os.path.join(TE, "lex.phy"))
    base = [IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000"]
    subprocess.run(base + ["-s", "innov11.phy", "-st", "BIN", "-m", "GTR2+FO", "-pre", "innov11"], cwd=TE, check=True)
    open(os.path.join(TE, "te_innov11.nex"), "w").write(
        "#nexus\nbegin sets;\n"
        f"  charset lex = lex.phy: 1-{nlex};\n  charset inn = innov11.phy: 1-{nchar};\n"
        "  charpartition mine = GTR2+FO+G4:lex, GTR2+FO:inn;\nend;\n")
    subprocess.run(base + ["-p", "te_innov11.nex", "-pre", "te_innov11"], cwd=TE, check=True)
    res = dict(innovations_only_11=te.support_from_splits(os.path.join(TE, "innov11.splits.nex")),
               lexical_plus_11_innovations=te.support_from_splits(os.path.join(TE, "te_innov11.splits.nex")),
               for_comparison_E10b=json.load(open(os.path.join(TE, "innovation_support.json"))))
    os.makedirs(LIT, exist_ok=True)
    json.dump(res, open(os.path.join(LIT, "e13_hull_characters.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


def e13_sensitivity():
    """Added after E13 was seen (not pre-declared): drop the two *k characters, whose Lakalei-Idate cells rest on
    at most four automatic tokens (one a misalignment, Idaté nusaː 'how'), keeping E10b's eight plus b_h_initial."""
    rows = {r["Taxon"]: r for r in read_csv(os.path.join(OUT, "innovation_matrix_24_hull.csv"))}
    names = [c[0] for c in inn.CHARS] + ["b_h_initial"]
    mat = {t: [r[n] for n in names] for t, r in rows.items()}
    keep = {t: r for t, r in mat.items() if any(x != "?" for x in r)}
    with open(os.path.join(TE, "innov9.phy"), "w") as fh:
        fh.write(f"{len(keep)} {len(names)}\n")
        for t, r in keep.items():
            fh.write(f"{te.tx(t)} {''.join(r)}\n")
    nlex = int(open(os.path.join(TE, "lex.phy")).readline().split()[1])
    base = [IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000"]
    subprocess.run(base + ["-s", "innov9.phy", "-st", "BIN", "-m", "GTR2+FO", "-pre", "innov9"], cwd=TE, check=True)
    open(os.path.join(TE, "te_innov9.nex"), "w").write(
        "#nexus\nbegin sets;\n"
        f"  charset lex = lex.phy: 1-{nlex};\n  charset inn = innov9.phy: 1-{len(names)};\n"
        "  charpartition mine = GTR2+FO+G4:lex, GTR2+FO:inn;\nend;\n")
    subprocess.run(base + ["-p", "te_innov9.nex", "-pre", "te_innov9"], cwd=TE, check=True)
    path = os.path.join(LIT, "e13_hull_characters.json")
    res = json.load(open(path))
    res["sensitivity_not_predeclared"] = dict(
        note="k characters dropped after E13 was seen; eight E10b characters plus b_h_initial",
        innovations_only_9=te.support_from_splits(os.path.join(TE, "innov9.splits.nex")),
        lexical_plus_9_innovations=te.support_from_splits(os.path.join(TE, "te_innov9.splits.nex")))
    json.dump(res, open(path, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res["sensitivity_not_predeclared"], indent=1, ensure_ascii=False))


# ---------------------------------------------------------------- E14
ASJP_LISTS = {
    "IDATE": "Idaté",
    "MAMBAE": "CT", "KEMAK": "CT", "TUKUDEDE": "CT", "WELAUN": "CT",
    "TETUN": "ET", "HABU": "ET", "NAUETE": "ET", "WAIMAA": "ET", "GALOLI": "ET", "TALUR": "ET",
    "UAB_METO": "W", "AMARASI": "W", "TERMANU": "W", "HELONG": "W",
}
CT = {k for k, v in ASJP_LISTS.items() if v == "CT"}
ETG = {k for k, v in ASJP_LISTS.items() if v == "ET"}
E14_CLADES = {
    "Idaté + Central Timor": CT | {"IDATE"},
    "Idaté + Nuclear Central Timor": {"IDATE", "MAMBAE", "KEMAK", "TUKUDEDE"},
    "Idaté + Eastern Timor and Galoli": ETG | {"IDATE"},
    "Central Timor": CT,
}


def asjp_clean(f):
    """ASJPcode -> list of symbols: drop spaces and the modifiers * " ~ $ (an approximation of LDND practice)."""
    return [ch for ch in f if ch not in ' *"~$-']


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def ldn(a, b):
    return lev(a, b) / max(len(a), len(b), 1)


def load_asjp(repo):
    words = defaultdict(lambda: defaultdict(list))
    with open(os.path.join(repo, "cldf", "forms.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            if r["Language_ID"] in ASJP_LISTS and r["Loan"] != "true" and r["Form"]:
                words[r["Language_ID"]][r["Parameter_ID"]].append(asjp_clean(r["Form"]))
    return words


def pair_tables(words, langs):
    """Per pair: same-meaning LDN by meaning, and different-meaning LDN by meaning pair (min over synonyms)."""
    same, diff = {}, {}
    for i, a in enumerate(langs):
        for b in langs[i + 1:]:
            ma, mb = words[a], words[b]
            same[(a, b)] = {m: min(ldn(x, y) for x in ma[m] for y in mb[m]) for m in ma if m in mb}
            diff[(a, b)] = {(m1, m2): min(ldn(x, y) for x in ma[m1] for y in mb[m2])
                            for m1 in ma for m2 in mb if m1 != m2}
    return same, diff


def ldnd_matrix(langs, same, diff, weights=None):
    n = len(langs)
    D = np.zeros((n, n))
    for i, a in enumerate(langs):
        for j in range(i + 1, n):
            b = langs[j]
            s, d = same[(a, b)], diff[(a, b)]
            w = weights or {}
            sw = [(v, w.get(m, 1)) for m, v in s.items() if w.get(m, 1)]
            dw = [(v, w.get(m1, 1) * w.get(m2, 1)) for (m1, m2), v in d.items() if w.get(m1, 1) * w.get(m2, 1)]
            if not sw or not dw:
                D[i, j] = D[j, i] = np.nan
                continue
            num = sum(v * k for v, k in sw) / sum(k for _, k in sw)
            den = sum(v * k for v, k in dw) / sum(k for _, k in dw)
            D[i, j] = D[j, i] = num / den
    return D


def nj_splits(D, names):
    """Neighbor joining; returns the leaf sets of all clusters formed (each is one side of a tree split)."""
    D = D.copy()
    nodes = [frozenset([x]) for x in names]
    splits = []
    while len(nodes) > 3:
        n = len(nodes)
        r = D.sum(axis=1)
        Q = (n - 2) * D - r[:, None] - r[None, :]
        np.fill_diagonal(Q, np.inf)
        i, j = np.unravel_index(np.argmin(Q), Q.shape)
        new = nodes[i] | nodes[j]
        splits.append(new)
        dnew = 0.5 * (D[i] + D[j] - D[i, j])
        keep = [k for k in range(n) if k not in (i, j)]
        D2 = np.zeros((len(keep) + 1, len(keep) + 1))
        D2[:-1, :-1] = D[np.ix_(keep, keep)]
        D2[-1, :-1] = D2[:-1, -1] = dnew[keep]
        D = D2
        nodes = [nodes[k] for k in keep] + [new]
    return splits


def has_split(splits, clade, allnames):
    c, comp = frozenset(clade), frozenset(allnames) - frozenset(clade)
    return any(s == c or s == comp for s in splits)


def e14(repo, reps=1000, seed=1234):
    words = load_asjp(repo)
    langs = [l for l in ASJP_LISTS if l in words]
    same, diff = pair_tables(words, langs)
    D = ldnd_matrix(langs, same, diff)
    idx = {l: i for i, l in enumerate(langs)}
    i0 = idx["IDATE"]
    ranking = sorted(((langs[j], ASJP_LISTS[langs[j]], round(float(D[i0, j]), 3), len(same[tuple(sorted(
        ("IDATE", langs[j]), key=langs.index))])) for j in range(len(langs)) if j != i0), key=lambda x: x[2])

    def contrast(M):
        ct = np.nanmean([M[i0, idx[l]] for l in CT])
        et = np.nanmean([M[i0, idx[l]] for l in ETG])
        return ct - et

    def nearest(M):
        row = [(M[i0, j], langs[j]) for j in range(len(langs)) if j != i0 and not np.isnan(M[i0, j])]
        return min(row)[1]

    base = dict(contrast_CT_minus_ET=round(float(contrast(D)), 4),
                splits={k: has_split(nj_splits(D, langs), v, langs) for k, v in E14_CLADES.items()})
    rng = random.Random(seed)
    meanings = sorted({m for l in langs for m in words[l]}, key=lambda x: int(x))
    sup, cons, near, filled = Counter(), [], Counter(), 0
    for _ in range(reps):
        draw = Counter(rng.choice(meanings) for _ in meanings)
        w = {m: draw.get(m, 0) for m in meanings}
        M = ldnd_matrix(langs, same, diff, w)
        if np.isnan(M[~np.eye(len(langs), dtype=bool)]).any():
            filled += 1
            M = np.where(np.isnan(M), D, M)
        cons.append(contrast(M))
        near[nearest(M)] += 1
        sp = nj_splits(M, langs)
        for k, v in E14_CLADES.items():
            sup[k] += has_split(sp, v, langs)
    cons = np.array(cons)
    res = dict(
        lists={l: dict(group=ASJP_LISTS[l], words=sum(len(v) for v in words[l].values()), meanings=len(words[l]))
               for l in langs},
        idate_ranking=[dict(list=a, group=g, LDND=d, shared_meanings=n) for a, g, d, n in ranking],
        full_data=base,
        bootstrap=dict(replicates=reps, replicates_with_filled_cells=filled,
                       contrast_CT_minus_ET_mean=round(float(cons.mean()), 4),
                       contrast_CT_minus_ET_95ci=[round(float(np.percentile(cons, 2.5)), 4),
                                                  round(float(np.percentile(cons, 97.5)), 4)],
                       share_contrast_below_zero=round(float((cons < 0).mean()), 3),
                       nearest_to_idate={k: v / reps for k, v in near.most_common()},
                       nj_split_support={k: sup[k] / reps for k in E14_CLADES}))
    os.makedirs(LIT, exist_ok=True)
    json.dump(res, open(os.path.join(LIT, "e14_asjp_idate.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(LIT, "e14_asjp_ldnd.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([""] + langs)
        for i, l in enumerate(langs):
            w.writerow([l] + [("" if i == j else round(float(D[i, j]), 4)) for j in range(len(langs))])
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1] == "e13":
        e13()
    elif sys.argv[1] == "e13s":
        e13_sensitivity()
    elif sys.argv[1] == "e14":
        e14(sys.argv[2])
