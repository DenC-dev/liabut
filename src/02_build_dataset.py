"""Step 1: build D1 (LexiRumah) and D2 (ABVD) from the pinned upstream data, following PROTOCOL.md section 2.

Writes data/d1/ and data/d2/ (tracked) plus data/screen/ (Indonesian and Portuguese reference words).

    python3 src/02_build_dataset.py
"""
import json
import os
from collections import Counter, defaultdict

import pandas as pd

from common import DATA, REF, UP, clean_abvd, read_csv, write_csv


def build_d1():
    lr = os.path.join(UP, "lexirumah", "cldf")
    sel = read_csv(os.path.join(REF, "d1_lects.csv"))
    group = {r["Lect_ID"]: r for r in sel}
    lects = pd.read_csv(os.path.join(lr, "lects.csv"))
    forms = pd.read_csv(os.path.join(lr, "forms.csv"), low_memory=False)
    concepts = pd.read_csv(os.path.join(lr, "concepts.csv"))
    cogs = pd.read_csv(os.path.join(lr, "cognates.csv"), low_memory=False)

    missing = sorted(set(group) - set(lects.ID))
    assert not missing, f"lects not in LexiRumah: {missing}"
    f = forms[forms.Lect_ID.isin(group) & forms.Segments.notna()].copy()
    f = f[f.Segments.str.strip() != ""]

    # concept rule: attested in >= 75% of D1 lects
    cover = f.groupby("Concept_ID").Lect_ID.nunique()
    keep = sorted(cover[cover >= 0.75 * len(group)].index)
    f = f[f.Concept_ID.isin(keep)]

    out_forms = [dict(ID=r.ID, Lect_ID=r.Lect_ID, Concept_ID=r.Concept_ID, Value=r.Form_according_to_Source,
                      Form=r.Form, Segments=r.Segments, Source=r.Source) for r in f.itertuples()]
    write_csv(os.path.join(DATA, "d1", "forms.csv"), out_forms)

    lmeta = lects.set_index("ID")
    n_conc = f.groupby("Lect_ID").Concept_ID.nunique()
    write_csv(os.path.join(DATA, "d1", "lects.csv"), [
        dict(ID=l, Name=lmeta.loc[l, "Name"], Family=lmeta.loc[l, "Family"], Glottocode=lmeta.loc[l, "Glottocode"],
             Latitude=lmeta.loc[l, "Latitude"], Longitude=lmeta.loc[l, "Longitude"], Group=group[l]["Group"],
             Role=group[l]["Role"], Concepts=int(n_conc.get(l, 0))) for l in group])

    c = concepts[concepts.ID.isin(keep)]
    write_csv(os.path.join(DATA, "d1", "concepts.csv"), [
        dict(ID=r.ID, English=r.English, Indonesian=r.Indonesian, Concepticon_ID=r.Concepticon_ID,
             Semantic_Field=r.Semantic_Field) for r in c.itertuples()])

    bl = cogs[cogs.Form_ID.isin(set(f.ID))]
    write_csv(os.path.join(DATA, "d1", "cognates_biglexstat.csv"),
              [dict(Form_ID=r.Form_ID, Cognateset_ID=r.Cognateset_ID) for r in bl.itertuples()])
    return dict(lects=len(group), concepts=len(keep), forms=len(f),
                concepts_per_lect_min=int(n_conc.min()), concepts_per_lect_median=float(n_conc.median()),
                biglexstat_judgments=len(bl))


def build_d2():
    ab = os.path.join(UP, "abvd", "cldf")
    L = pd.read_csv(os.path.join(ab, "languages.csv"))
    F = pd.read_csv(os.path.join(ab, "forms.csv"), low_memory=False)
    C = pd.read_csv(os.path.join(ab, "cognates.csv"), low_memory=False)
    P = pd.read_csv(os.path.join(ab, "parameters.csv"))
    F["Language_ID"] = F.Language_ID.astype(str)
    L["ID"] = L.ID.astype(str)

    box = L[L.Latitude.between(-11.2, -7.4) & L.Longitude.between(122.5, 130.5)
            & ~L.Name.str.startswith("Proto", na=False)]
    exp = C[C.Cognate_Detection_Method == "expert"].merge(F[["ID", "Language_ID"]], left_on="Form_ID",
                                                          right_on="ID", suffixes=("", "_f"))
    coded = exp.groupby("Language_ID").Form_ID.nunique()
    langs = [l for l in box.ID if coded.get(l, 0) >= 100]

    f = F[F.Language_ID.isin(langs)].copy()
    rows, dropped = [], Counter()
    for r in f.itertuples():
        toks = clean_abvd(str(r.Form))
        if toks is None:
            dropped[r.Language_ID] += 1
            continue
        rows.append(dict(ID=r.ID, Lect_ID=r.Language_ID, Concept_ID=r.Parameter_ID, Value=r.Value, Form=r.Form,
                         Segments=" ".join(toks), Loan=bool(r.Loan)))
    write_csv(os.path.join(DATA, "d2", "forms.csv"), rows)
    kept = {r["ID"] for r in rows}
    e = exp[exp.Form_ID.isin(kept)]
    write_csv(os.path.join(DATA, "d2", "cognates_expert.csv"),
              [dict(Form_ID=r.Form_ID, Cognateset_ID=r.Cognateset_ID, Doubt=r.Doubt) for r in e.itertuples()])
    lm = L.set_index("ID")
    write_csv(os.path.join(DATA, "d2", "lects.csv"), [
        dict(ID=l, Name=lm.loc[l, "Name"], Glottocode=lm.loc[l, "Glottocode"], Latitude=lm.loc[l, "Latitude"],
             Longitude=lm.loc[l, "Longitude"], Expert_Coded_Forms=int(coded.get(l, 0))) for l in langs])
    write_csv(os.path.join(DATA, "d2", "concepts.csv"),
              [dict(ID=r.ID, English=r.Name, Concepticon_ID=r.Concepticon_ID) for r in P.itertuples()])

    # Indonesian reference forms for L3 (ABVD language 362)
    indo = F[F.Language_ID == "362"]
    write_csv(os.path.join(DATA, "screen", "indonesian_abvd.csv"),
              [dict(Concept_ID=r.Parameter_ID, Form=r.Form) for r in indo.itertuples()])
    return dict(lects=len(langs), lect_ids=langs, concepts=int(f.Parameter_ID.nunique()), forms=len(rows),
                forms_dropped_tokenization=dict(dropped), expert_judgments=len(e), loans_flagged=int(f.Loan.sum()))


def build_portuguese():
    ids = os.path.join(UP, "ids", "cldf")
    F = pd.read_csv(os.path.join(ids, "forms.csv"), low_memory=False)
    P = pd.read_csv(os.path.join(ids, "parameters.csv"))
    pt = F[F.Language_ID.astype(str) == "178"].merge(P[["ID", "Concepticon_ID"]], left_on="Parameter_ID",
                                                      right_on="ID", suffixes=("", "_p"))
    pt = pt[pt.Concepticon_ID.notna()]
    write_csv(os.path.join(DATA, "screen", "portuguese_ids.csv"),
              [dict(Concepticon_ID=int(r.Concepticon_ID), Form=r.Form) for r in pt.itertuples()])
    return dict(forms=len(pt), concepts=int(pt.Concepticon_ID.nunique()))


if __name__ == "__main__":
    summary = dict(d1=build_d1(), d2=build_d2(), portuguese=build_portuguese())
    os.makedirs(os.path.join(DATA), exist_ok=True)
    with open(os.path.join(DATA, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))
