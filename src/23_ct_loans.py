"""E12b (A4.5): are Lakalei-Idate's Central Timor cognates loans or inherited?

Forms of Idate and Lakalei in cognate sets shared with Central Timor but not Tetun (results/exploratory/
e4_lakalei_idate_sets.csv) are checked, target by target, against the Lakalei-Idate and Central Timor expert majority
reflexes (derived/reflex_atlas/expert_tokens.csv). Only targets where the two differ are diagnostic.

Writes derived/loans/central_timor_in_lakalei_idate.csv.

    python3 src/23_ct_loans.py
"""
import importlib
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, RES, read_csv, write_csv  # noqa: E402
from pipeline import variant_rows  # noqa: E402

loans = importlib.import_module("22_tetun_loans")
LI_LECTS = {"idat1237", "idat1237-cribas", "laka1255"}
LI_G = ["idat1237", "laka1255"]
CT_G = ["mamb1306", "kema1243", "tuku1254"]


def pooled_majority(cells, gs, target, position):
    c = Counter()
    for g in gs:
        c.update(cells.get((g, target, position)) or Counter())
    if sum(c.values()) < 2:
        c = Counter()
        for g in gs:
            c.update(cells.get((g, target, None)) or Counter())
    return c.most_common(1)[0][0] if sum(c.values()) >= 2 else None


def main():
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
    sets = {r["Cognateset_ID"]: r for r in read_csv(os.path.join(RES, "exploratory", "e4_lakalei_idate_sets.csv"))
            if r["With_CentralTimor"] == "True" and r["With_Tetun"] == "False"}
    rows = []
    for r in variant_rows("d1", "lexstat", "primary"):
        if r["Lect_ID"] not in LI_LECTS or r["Cognateset_ID"] not in sets:
            continue
        s = sets[r["Cognateset_ID"]]
        ct_ev, li_ev = [], []
        for t in auto.get(r["Form_ID"], []):
            mine = pooled_majority(cells, LI_G, t["Target"], t["Position"])
            ct = pooled_majority(cells, CT_G, t["Target"], t["Position"])
            if not mine or not ct or mine == ct:
                continue
            if t["Class"] == ct:
                ct_ev.append(f"*{t['Target']}>{t['Class']} (CT) vs {mine} (LI) in {t['Form']} < *{t['PMP']}")
            elif t["Class"] == mine:
                li_ev.append(f"*{t['Target']}>{t['Class']} (LI) vs {ct} (CT) in {t['Form']} < *{t['PMP']}")
        verdict = ("probable Central Timor loan" if ct_ev and not li_ev else "inherited or old" if li_ev and not ct_ev
                   else "conflicting" if ct_ev else "undecidable")
        rows.append(dict(Form_ID=r["Form_ID"], Lect_ID=r["Lect_ID"], Concept_ID=r["Concept_ID"],
                         Cognateset_ID=r["Cognateset_ID"], Exclusive=s["Outside_Central_Timor"] == "False",
                         Stable=s["Stable"], Verdict=verdict, CT_Evidence="; ".join(ct_ev),
                         LI_Evidence="; ".join(li_ev)))
    write_csv(os.path.join(REPO, "derived", "loans", "central_timor_in_lakalei_idate.csv"), rows)
    print(len(rows), "Lakalei-Idate forms in sets shared with Central Timor but not Tetun")
    print("all:", Counter(r["Verdict"] for r in rows))
    print("exclusive sets only:", Counter(r["Verdict"] for r in rows if r["Exclusive"]))
    for r in rows:
        if r["Verdict"] != "undecidable":
            print(" ", r["Lect_ID"], r["Concept_ID"], r["Verdict"], "|", r["CT_Evidence"] or r["LI_Evidence"])


if __name__ == "__main__":
    main()
