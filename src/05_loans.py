"""Step 3: loan screening (PROTOCOL.md section 4).

L1 expert loan flags (ABVD), L2 contact sets (Austronesian + TAP in one automatic set, D1), L3 Indonesian,
L4 Portuguese, L5 near-identical to Tetun in a non-Tetun Timor lect. Near-identical = NED <= 0.20 on SCA sound
classes, forms of 3+ segments. Writes results/loans/{d1,d2}_flags.csv and a per-lect summary.

    python3 src/05_loans.py
"""
import json
import os
from collections import Counter, defaultdict

from common import DATA, INDO, PORT, REF, RES, ned, ortho_tokens, read_csv, sca_string, write_csv

NEAR = 0.20
D1_TETUN = {"tetu1246", "tetu1245-suai"}
D2_TETUN = {"134", "403", "1366"}
D2_TIMOR_OTHER = {"167", "61", "300", "1368", "1365", "42"}  # Mambai, Kemak, Galolen, Waima'a, Naueti, Atoni


def near(form_toks, ref_strings):
    if len([t for t in form_toks if t not in ("+", "_")]) < 3:
        return None
    s = sca_string(form_toks)
    best = None
    for word, r in ref_strings:
        d = ned(s, r)
        if d <= NEAR and (best is None or d < best[1]):
            best = (word, d)
    return best


def portuguese_by_concepticon():
    pt = defaultdict(list)
    for r in read_csv(os.path.join(DATA, "screen", "portuguese_ids.csv")):
        toks = ortho_tokens(r["Form"], PORT, ("o", "a", "os", "as"))
        if toks:
            pt[r["Concepticon_ID"]].append((r["Form"], sca_string(toks)))
    return pt


def screen(ds):
    forms = read_csv(os.path.join(DATA, ds, "forms.csv"))
    concepts = {r["ID"]: r for r in read_csv(os.path.join(DATA, ds, "concepts.csv"))}
    pt = portuguese_by_concepticon()

    indo = defaultdict(list)
    if ds == "d1":
        for cid, c in concepts.items():
            toks = ortho_tokens(c["Indonesian"] or "", INDO)
            if toks:
                indo[cid].append((c["Indonesian"], sca_string(toks)))
        role = {r["Lect_ID"]: r["Role"] for r in read_csv(os.path.join(REF, "d1_lects.csv"))}
        is_tap = {l: role[l] == "TAP" for l in role}
        tetun, timor_other = D1_TETUN, {l for l in role if role[l] == "Timor AN"} - D1_TETUN
        cog = {r["Form_ID"]: r["Cognateset_ID"] for r in read_csv(os.path.join(RES, "cognates", "d1_lexstat.csv"))}
        fam = defaultdict(set)
        for r in forms:
            fam[cog.get(r["ID"])].add("TAP" if is_tap[r["Lect_ID"]] else "AN")
        contact = {s for s, f in fam.items() if s and len(f) == 2}
    else:
        for r in read_csv(os.path.join(DATA, "screen", "indonesian_abvd.csv")):
            toks = ortho_tokens(r["Form"], INDO)
            if toks:
                indo[r["Concept_ID"]].append((r["Form"], sca_string(toks)))
        tetun, timor_other = D2_TETUN, D2_TIMOR_OTHER
        cog, contact = {}, set()

    tet = defaultdict(list)
    for r in forms:
        if r["Lect_ID"] in tetun:
            tet[r["Concept_ID"]].append((r["Form"], sca_string(r["Segments"].split())))

    out = []
    for r in forms:
        toks = r["Segments"].split()
        cpt = concepts.get(r["Concept_ID"], {})
        ci = str(cpt.get("Concepticon_ID") or "").split(".")[0]
        l3 = near(toks, indo.get(r["Concept_ID"], []))
        l4 = near(toks, pt.get(ci, [])) if ci else None
        l5 = near(toks, tet.get(r["Concept_ID"], [])) if r["Lect_ID"] in timor_other else None
        out.append(dict(Form_ID=r["ID"], Lect_ID=r["Lect_ID"], Concept_ID=r["Concept_ID"], Form=r["Form"],
                        L1_expert=(r.get("Loan") == "True"), L2_contact=(cog.get(r["ID"]) in contact),
                        L3_indonesian=bool(l3), L3_match=l3[0] if l3 else "",
                        L4_portuguese=bool(l4), L4_match=l4[0] if l4 else "",
                        L5_tetun=bool(l5), L5_match=l5[0] if l5 else ""))
    write_csv(os.path.join(RES, "loans", f"{ds}_flags.csv"), out)

    per = defaultdict(Counter)
    for o in out:
        p = per[o["Lect_ID"]]
        p["forms"] += 1
        for k in ("L1_expert", "L2_contact", "L3_indonesian", "L4_portuguese", "L5_tetun"):
            p[k] += bool(o[k])
    write_csv(os.path.join(RES, "loans", f"{ds}_by_lect.csv"),
              [dict(Lect_ID=l, **c) for l, c in sorted(per.items())],
              ["Lect_ID", "forms", "L1_expert", "L2_contact", "L3_indonesian", "L4_portuguese", "L5_tetun"])
    tot = Counter()
    for c in per.values():
        tot.update(c)
    return dict(tot, contact_sets=len(contact))


if __name__ == "__main__":
    s = {ds: screen(ds) for ds in ("d1", "d2")}
    with open(os.path.join(RES, "loans", "summary.json"), "w") as fh:
        json.dump(s, fh, indent=1)
    print(json.dumps(s, indent=1))
