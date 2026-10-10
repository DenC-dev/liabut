"""Exploratory analyses E1 and E3 (Addendum 2, A2.5). Not part of the step 8 decision.

E1: hypothesis-clade support on the 60 Leipzig-Jakarta (borrowing-resistant) concepts vs the other 92.
E3: each Timor lect's cognate overlap with Tetun on stable vs other concepts.
E3b (added after E1-E3 had run, so post hoc): nearest groups to Lakalei-Idate and to Welaun.

    python3 src/10_exploratory.py
"""
import importlib.util
import math
import os

from common import DATA, RES, read_csv, write_csv
from pipeline import build, lect_names, roles, variant_rows

spec = importlib.util.spec_from_file_location("hyp", os.path.join(os.path.dirname(__file__), "07_hypotheses.py"))
hyp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hyp)

TETUN = {"tetu1246", "tetu1245-suai"}


def stable_concepts():
    import csv
    with open(os.path.join(DATA, "screen", "leipzig_jakarta_tadmor2009.tsv"), encoding="utf-8") as fh:
        lj = {r["CONCEPTICON_ID"] for r in csv.DictReader(fh, delimiter="\t")}
    concepts = read_csv(os.path.join(DATA, "d1", "concepts.csv"))
    stable = {c["ID"] for c in concepts if str(c["Concepticon_ID"]).split(".")[0] in lj}
    return stable, {c["ID"] for c in concepts} - stable


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return round(c - h, 3), round(c + h, 3)


def e1(stable, other):
    hyps = hyp.hypotheses()
    rows = []
    for label, cset in (("stable_LJ", stable), ("other", other)):
        for v in ("primary", "tetun"):
            b = build("d1", "lexstat", v, concept_filter=cset)
            for r in hyp.evaluate(b, hyps):
                r.update(Concept_Set=label, Variant=v, Concepts=len(b["concepts"]))
                rows.append(r)
            print("E1", label, v, "done", flush=True)
    write_csv(os.path.join(RES, "exploratory", "e1_stable_vs_other.csv"), rows,
              ["Concept_Set", "Variant", "Concepts", "Hypothesis", "Name", "Contrast", "Members_Present",
               "Lects_In_Tree", "Testable", "UPGMA", "NJ", "UPGMA_Bootstrap", "NJ_Bootstrap"])


def e3(stable, other):
    rows = variant_rows("d1", "lexstat", "primary")
    sets = {}
    for r in rows:
        sets.setdefault((r["Lect_ID"], r["Concept_ID"]), set()).add(r["Cognateset_ID"])
    tet = {}
    for (l, c), s in sets.items():
        if l in TETUN:
            tet.setdefault(c, set()).update(s)
    role = roles()
    names = lect_names("d1")
    out = []
    for l in sorted({l for l, _ in sets}):
        if role.get(l) not in ("Timor AN", "TAP") or l in TETUN:
            continue
        rec = dict(Lect_ID=l, Name=names[l], Role=role[l])
        for label, cset in (("Stable", stable), ("Other", other)):
            cs = [c for c in cset if (l, c) in sets and c in tet]
            k = sum(bool(sets[(l, c)] & tet[c]) for c in cs)
            rec[f"{label}_N"] = len(cs)
            rec[f"{label}_Shared"] = round(k / len(cs), 3) if cs else None
            rec[f"{label}_CI"] = "%s-%s" % wilson(k, len(cs))
        rec["Other_minus_Stable"] = round(rec["Other_Shared"] - rec["Stable_Shared"], 3)
        out.append(rec)
    out.sort(key=lambda r: -r["Other_Shared"])
    write_csv(os.path.join(RES, "exploratory", "e3_tetun_affinity.csv"), out)
    for r in out[:20]:
        print(f"{r['Name'][:28]:28s} stable {r['Stable_Shared']} (n={r['Stable_N']})  other {r['Other_Shared']} "
              f"(n={r['Other_N']})  diff {r['Other_minus_Stable']}")




def e3b(stable, other):
    """Post hoc (labelled in the report): mean LexStat distance from Lakalei-Idate and from Welaun to each group,
    on all, stable and other concepts."""
    import numpy as np
    groups = {}
    for r in read_csv(os.path.join(os.path.dirname(DATA), "reference", "d1_lects.csv")):
        groups.setdefault(r["Group"], []).append(r["Lect_ID"])
    focal = {"Lakalei-Idate": groups["Idate"] + groups["Lakalei"], "Welaun": groups["Welaun"]}
    out = []
    for label, cset in (("all", None), ("stable_LJ", stable), ("other", other)):
        b = build("d1", "lexstat", "primary", concept_filter=cset)
        idx = {l: i for i, l in enumerate(b["lects"])}
        for f, fl in focal.items():
            for g, gl in groups.items():
                if g in ("Idate", "Lakalei") and f == "Lakalei-Idate" or (g == "Welaun" and f == "Welaun"):
                    continue
                vals = [b["d"][idx[a], idx[c]] for a in fl for c in gl if a in idx and c in idx]
                out.append(dict(Focal=f, Concepts=label, Group=g, Mean_Distance=round(float(np.nanmean(vals)), 3)))
    write_csv(os.path.join(RES, "exploratory", "e3b_nearest_groups.csv"), out)
    for f in ("Lakalei-Idate", "Welaun"):
        for label in ("all", "stable_LJ", "other"):
            rows = sorted([r for r in out if r["Focal"] == f and r["Concepts"] == label], key=lambda r: r["Mean_Distance"])
            print(f, label, ", ".join(f"{r['Group']} {r['Mean_Distance']}" for r in rows[:6]))


if __name__ == "__main__":
    os.makedirs(os.path.join(RES, "exploratory"), exist_ok=True)
    s, o = stable_concepts()
    print(len(s), "stable,", len(o), "other concepts")
    e3(s, o)
    e3b(s, o)
    e1(s, o)
