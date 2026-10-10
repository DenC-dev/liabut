"""Shared data assembly for steps 4 to 8: cognate rows per configuration, loan variants, distance tensors.

Variant rules follow PROTOCOL.md section 4 as amended by Addendum 1 (A1.2):
- primary  : drop L1 (expert loan), L3 (Indonesian) and L4 (Portuguese) forms
- all      : drop nothing
- contact  : primary, minus the TAP-side forms of contact sets (L2)
- tetun    : primary, minus L5 (Tetun look-alike) forms
The 100-concept minimum is applied on the primary data only; variants keep the same lects.
"""
import os
from functools import lru_cache

from common import DATA, REF, RES, cognate_tensors, distance, read_csv

MIN_CONCEPTS = 100


@lru_cache(maxsize=None)
def forms(ds):
    return {r["ID"]: r for r in read_csv(os.path.join(DATA, ds, "forms.csv"))}


@lru_cache(maxsize=None)
def flags(ds):
    return {r["Form_ID"]: r for r in read_csv(os.path.join(RES, "loans", f"{ds}_flags.csv"))}


@lru_cache(maxsize=None)
def roles():
    return {r["Lect_ID"]: r["Role"] for r in read_csv(os.path.join(REF, "d1_lects.csv"))}


@lru_cache(maxsize=None)
def lect_names(ds):
    return {r["ID"]: r["Name"] for r in read_csv(os.path.join(DATA, ds, "lects.csv"))}


@lru_cache(maxsize=None)
def all_lects(ds):
    return tuple(r["ID"] for r in read_csv(os.path.join(DATA, ds, "lects.csv")))


@lru_cache(maxsize=None)
def cognate_rows(ds, method):
    f = forms(ds)
    if method == "expert":
        src = read_csv(os.path.join(DATA, "d2", "cognates_expert.csv"))
    elif method == "biglexstat":
        src = read_csv(os.path.join(DATA, "d1", "cognates_biglexstat.csv"))
    else:
        src = read_csv(os.path.join(RES, "cognates", f"{ds}_{method}.csv"))
    rows = []
    for r in src:
        x = f.get(r["Form_ID"])
        if x:
            rows.append(dict(Form_ID=r["Form_ID"], Lect_ID=x["Lect_ID"], Concept_ID=x["Concept_ID"],
                             Cognateset_ID=r["Cognateset_ID"]))
    return tuple(tuple(sorted(r.items())) for r in rows)


def variant_rows(ds, method, variant, concept_filter=None):
    fl = flags(ds)
    role = roles()
    out = []
    for t in cognate_rows(ds, method):
        r = dict(t)
        g = fl[r["Form_ID"]]
        if concept_filter is not None and r["Concept_ID"] not in concept_filter:
            continue
        if variant != "all" and "True" in (g["L1_expert"], g["L3_indonesian"], g["L4_portuguese"]):
            continue
        if variant == "contact" and g["L2_contact"] == "True" and role.get(r["Lect_ID"]) == "TAP":
            continue
        if variant == "tetun" and g["L5_tetun"] == "True":
            continue
        out.append(r)
    return out


def coverage(rows, lects):
    cov = {l: set() for l in lects}
    for r in rows:
        if r["Lect_ID"] in cov:
            cov[r["Lect_ID"]].add(r["Concept_ID"])
    return {l: len(c) for l, c in cov.items()}


@lru_cache(maxsize=None)
def primary_lects(ds, method):
    cov = coverage(variant_rows(ds, method, "primary"), all_lects(ds))
    return tuple(l for l in all_lects(ds) if cov[l] >= MIN_CONCEPTS)


def build(ds, method, variant, lects=None, concept_filter=None):
    """Returns dict(lects, concepts, S, A, d, shared, coverage, below_min)."""
    rows = variant_rows(ds, method, variant, concept_filter)
    lects = list(lects or primary_lects(ds, method))
    concepts = sorted({r["Concept_ID"] for r in rows})
    S, A = cognate_tensors(rows, lects, concepts)
    d, shared = distance(S, A)
    cov = coverage(rows, lects)
    return dict(lects=lects, concepts=concepts, S=S, A=A, d=d, shared=shared, coverage=cov,
                below_min={l: c for l, c in cov.items() if c < MIN_CONCEPTS}, rows=rows)
