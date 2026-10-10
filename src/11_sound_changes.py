"""Exploratory E2 (Addendum 2, A2.5): reflexes of PMP *p and *ŋ in every D1 lect.

Timor-Babar is defined by *p > h/0; Central Timor keeps *p and has *ng > g (Grimes and Edwards 2026, ch. 4-5).
For D1 concepts that have an ABVD Proto-Malayo-Polynesian form (language 269), each lect form is aligned to the PMP
form (LingPy SCA, global). A pair is kept if the SCA sound-class strings are within NED 0.5; the best-scoring form
per lect and concept is used. The aligned segment under PMP *p (not word-final) and *ng is then classed.

    python3 src/11_sound_changes.py
"""
import csv
import os
import re
import unicodedata
from collections import Counter, defaultdict

from lingpy import Pairwise
from lingpy.sequence.sound_classes import ipa2tokens

from common import DATA, RES, UP, ned, read_csv, sca_string, write_csv
from pipeline import lect_names, roles

P_KEEP = {"p", "b", "f", "v", "ɸ", "β", "pf", "bv", "ʋ"}
P_LOSS = {"-", "h", "ʔ", "ɦ"}
NG_VELAR = {"g", "k", "ɡ", "q", "ɣ", "x", "ŋg", "ŋk", "kʰ", "gʰ"}
NG_NASAL = {"ŋ", "n", "ɲ", "m", "ŋː", "nː"}


def base(tok):
    t = unicodedata.normalize("NFD", tok)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.replace("ⁿ", "").replace("ː", "").replace("ˑ", "").replace("ʷ", "").replace("ʲ", "").replace("'", "")
    t = t.replace("ʰ", "")
    return t or tok


def clean_pmp(v):
    """PMP form -> (tokens, excluded indices). *p right after the *ma- prefix is excluded, following Grimes and
    Edwards (2026, ch. 4), who treat *ma-p separately because most Timor-Babar languages have *ma-p > p, b."""
    v = v.split(",")[0].split("/")[0].strip()
    v = re.sub(r"\(.*?\)", "", v).replace("*", "").strip()
    v = v.split()[0] if v else ""
    ma_p = bool(re.match(r"^ma-p", v))
    v = v.replace("-", "").replace("<", "").replace(">", "")
    v = unicodedata.normalize("NFD", v)
    v = "".join(ch for ch in v if unicodedata.category(ch) != "Mn")  # strip stress accents
    v = v.replace("e", "ə").replace("ʀ", "R").replace("C", "ts").replace("N", "ɲ").replace("j", "ɟ")
    if not v:
        return None
    toks = ipa2tokens(v, merge_vowels=False)
    return toks, ({2} if ma_p else set())


def pmp_forms():
    F = read_csv(os.path.join(UP, "abvd", "cldf", "forms.csv"))
    P = {r["ID"]: r["Concepticon_ID"] for r in read_csv(os.path.join(UP, "abvd", "cldf", "parameters.csv"))}
    out = defaultdict(list)
    for r in F:
        if r["Language_ID"] == "269":
            res = clean_pmp(r["Value"])
            if res and P.get(r["Parameter_ID"]):
                out[P[r["Parameter_ID"]]].append(res)
    return out


def classify(seg, target):
    b = base(seg)
    if target == "p":
        return "kept" if b in P_KEEP else "lost" if b in P_LOSS else "other"
    return "velar" if b in NG_VELAR else "nasal" if b in NG_NASAL else "lost" if b in P_LOSS else "other"


def reflexes(forms, cmap, pmp):
    by = defaultdict(list)
    for f in forms:
        by[(f["Lect_ID"], f["Concept_ID"])].append(f["Segments"].split())
    detail = []
    for (lect, concept), flist in by.items():
        for ptoks, excluded in pmp.get(cmap.get(concept), []):
            targets = [(i, t) for i, t in enumerate(ptoks)
                       if ((t == "p" and i < len(ptoks) - 1) or t == "ŋ") and i not in excluded]
            if not targets:
                continue
            best = None
            for toks in flist:
                toks = [t for t in toks if t not in ("+", "_")]
                dist = ned(sca_string(ptoks), sca_string(toks))
                if dist <= 0.5 and (best is None or dist < best[0]):
                    best = (dist, toks)
            if best is None:
                continue
            pw = Pairwise([(" ".join(ptoks), " ".join(best[1]))])
            pw.align(distance=True, mode="global")
            almA, almB, _ = pw.alignments[0]
            col, k = {}, -1
            for j, a in enumerate(almA):
                if a != "-":
                    k += 1
                    col[k] = j
            for i, t in targets:
                seg = almB[col[i]]
                tgt = "p" if t == "p" else "ŋ"
                detail.append(dict(Lect_ID=lect, Concept_ID=concept, PMP="".join(ptoks), Target=tgt,
                                   Position="initial" if i == 0 else "medial", Form="".join(best[1]),
                                   Reflex=seg, Class=classify(seg, tgt), NED=round(best[0], 3)))
    return detail


def summarise(detail, key, keys):
    out = []
    for kv in keys:
        rec = dict(kv)
        sel = [d for d in detail if key(d) == kv[0][1]]
        for tgt, tag, classes in (("p", "p", ("kept", "lost", "other")), ("ŋ", "ng", ("velar", "nasal", "lost", "other"))):
            c = Counter(d["Class"] for d in sel if d["Target"] == tgt)
            n = sum(c.values())
            rec[f"{tag}_N"] = n
            for cl in classes:
                rec[f"{tag}_{cl}"] = round(c[cl] / n, 2) if n else None
        out.append(rec)
    return out


def main():
    os.makedirs(os.path.join(RES, "exploratory"), exist_ok=True)
    pmp = pmp_forms()
    role, names = roles(), lect_names("d1")
    groups = {r["Lect_ID"]: r["Group"] for r in read_csv(os.path.join(os.path.dirname(DATA), "reference", "d1_lects.csv"))}
    d1_concepts = read_csv(os.path.join(DATA, "d1", "concepts.csv"))
    lr_concepts = read_csv(os.path.join(UP, "lexirumah", "cldf", "concepts.csv"))
    lr_forms = [dict(Lect_ID=r["Lect_ID"], Concept_ID=r["Concept_ID"], Segments=r["Segments"])
                for r in read_csv(os.path.join(UP, "lexirumah", "cldf", "forms.csv"))
                if r["Lect_ID"] in groups and r["Segments"]]
    runs = {"d1concepts": (read_csv(os.path.join(DATA, "d1", "forms.csv")), d1_concepts),
            "allconcepts": (lr_forms, lr_concepts)}
    for tag, (forms, concepts) in runs.items():
        cmap = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in concepts}
        detail = [d for d in reflexes(forms, cmap, pmp) if role.get(d["Lect_ID"]) != "TAP"]
        write_csv(os.path.join(RES, "exploratory", f"e2_reflexes_{tag}.csv"), detail)
        lects = sorted({d["Lect_ID"] for d in detail})
        by_lect = summarise(detail, lambda d: d["Lect_ID"],
                            [(("Lect_ID", l), ("Name", names[l]), ("Group", groups[l])) for l in lects])
        write_csv(os.path.join(RES, "exploratory", f"e2_by_lect_{tag}.csv"), by_lect)
        gs = list(dict.fromkeys(groups[l] for l in groups if role.get(l) != "TAP"))
        by_group = summarise(detail, lambda d: groups[d["Lect_ID"]], [(("Group", g),) for g in gs])
        write_csv(os.path.join(RES, "exploratory", f"e2_by_group_{tag}.csv"), by_group)
        print("==", tag, len(detail), "reflexes")
        for r in by_group:
            print(f"{r['Group'][:18]:18s} *p n={r['p_N']:3d} kept {r['p_kept']} lost {r['p_lost']} other {r['p_other']}"
                  f" | *ŋ n={r['ng_N']:3d} velar {r['ng_velar']} nasal {r['ng_nasal']} lost {r['ng_lost']}")


if __name__ == "__main__":
    main()
