"""Exploratory E4 (post hoc, added after E1-E3 were seen): are Lakalei-Idate's lexical links to Central Timor
shared retentions or exclusive?

For each cognate set (D1, LexStat, primary) that contains Idate or Lakalei, record whether it also occurs in
Central Timor (Mambae, Kemak, Tokodede), in Tetun, and outside central Timor (Flores-Lembata, Rote-Meto, Helong,
Wetar, Kisar-Luang, Babar). A set found outside central Timor is a shared retention or a wider areal word and is
not evidence for a subgroup; a set limited to Lakalei-Idate plus one side is the kind of evidence that could be.

    python3 src/14_retentions.py
"""
import os
from collections import defaultdict

from common import RES, read_csv, write_csv
from pipeline import variant_rows

REF = os.path.join(os.path.dirname(RES), "reference")


def main():
    grp = {r["Lect_ID"]: r["Group"] for r in read_csv(os.path.join(REF, "d1_lects.csv"))}
    stable = set()
    import csv
    with open(os.path.join(os.path.dirname(RES), "data", "screen", "leipzig_jakarta_tadmor2009.tsv")) as fh:
        lj = {r["CONCEPTICON_ID"] for r in csv.DictReader(fh, delimiter="\t")}
    for c in read_csv(os.path.join(os.path.dirname(RES), "data", "d1", "concepts.csv")):
        if str(c["Concepticon_ID"]).split(".")[0] in lj:
            stable.add(c["ID"])
    LI = {"Idate", "Lakalei"}
    CT = {"Mambae", "Kemak", "Tokodede"}
    TET = {"Tetun"}
    WIDE = {"Flores-Lembata", "Rote", "Meto", "Helong", "Wetar", "Luangic-Kisaric", "Babar"}
    members = defaultdict(set)
    concept = {}
    for r in variant_rows("d1", "lexstat", "primary"):
        members[r["Cognateset_ID"]].add(grp[r["Lect_ID"]])
        concept[r["Cognateset_ID"]] = r["Concept_ID"]
    rows = []
    for s, g in members.items():
        if not g & LI:
            continue
        rows.append(dict(Cognateset_ID=s, Concept_ID=concept[s], Stable=concept[s] in stable,
                         With_CentralTimor=bool(g & CT), With_Tetun=bool(g & TET), Outside_Central_Timor=bool(g & WIDE),
                         Groups=" ".join(sorted(g))))
    write_csv(os.path.join(RES, "exploratory", "e4_lakalei_idate_sets.csv"), rows)
    out = []
    for subset, label in ((True, "stable"), (False, "other")):
        rs = [r for r in rows if r["Stable"] == subset]
        for side, other in (("With_CentralTimor", "With_Tetun"), ("With_Tetun", "With_CentralTimor")):
            sel = [r for r in rs if r[side] and not r[other]]
            wide = sum(r["Outside_Central_Timor"] for r in sel)
            out.append(dict(Concepts=label, Shared_With=side.replace("With_", ""), Not_With=other.replace("With_", ""),
                            Sets=len(sel), Also_Outside_Central_Timor=wide, Exclusive=len(sel) - wide))
    write_csv(os.path.join(RES, "exploratory", "e4_summary.csv"), out)
    for o in out:
        print(o)


if __name__ == "__main__":
    main()
