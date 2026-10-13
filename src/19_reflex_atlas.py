"""E8 and E9 (Addendum 4): expert and automatic reflex atlases, and their agreement.

E8  expert atlas   from derived/ge2026_tables/reflexes.csv (Grimes and Edwards 2026, highlighted reflexes)
E9  automatic atlas from LexiRumah forms (all concepts, all D1 Austronesian lects) aligned to ABVD PMP forms,
    extending E2 from *p and *ŋ to every PMP consonant

Reflexes are grouped into classes (A4.1): place of articulation matters, voicing does not.

Writes derived/reflex_atlas/{expert,automatic}.csv, {expert,automatic,agreement}_tokens.csv.

    python3 src/19_reflex_atlas.py
"""
import os
import re
import unicodedata
from collections import Counter, defaultdict

from lingpy import Pairwise

from common import DATA, REF, REPO, UP, ned, read_csv, sca_string, write_csv
from pipeline import roles

OUT = os.path.join(REPO, "derived", "reflex_atlas")
CONSONANTS = set("p t k q b d g j z s h m n ŋ ñ l r R w y c".split())
CLASS = [
    ("labial stop", "pbɓ"), ("labial fricative", "fvɸβʋ"), ("coronal stop", "tdɗʈɖ"), ("velar stop", "kgqɡɠ"),
    ("sibilant", "szʃʒɕʑ"), ("h", "hɦħ"), ("glottal stop", "ʔ"), ("m", "m"), ("n", "n"), ("ɲ", "ɲñ"),
    ("ŋ", "ŋ"), ("l", "lɭʎ"), ("rhotic", "rɾɹʁRχ"), ("w", "w"), ("y", "yj"),
]


def base(tok):
    t = unicodedata.normalize("NFD", tok or "")
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    for x in "ⁿːˑʷʲʰ'ˀ":
        t = t.replace(x, "")
    return t


def rclass(reflex, target):
    """Reflex string -> class label. Vowel targets keep their (simplified) quality."""
    r = base(reflex).strip()
    if r in ("", "-", "∅", "(unmarked)"):
        return "∅"
    if target not in CONSONANTS:
        return r[:2]
    first = r[0]
    if first in "ʧʤʦʣ" or (first in "dt" and len(r) > 1 and r[1] in "ʒʃzs\u0361"):
        return "affricate"
    for name, chars in CLASS:
        if first in chars:
            return name
    if first in "aeiouəɛɔɨʊɪæɑ":
        return "vowel"
    return "other"


def etymon_key(marked):
    """'*ma-⟦p⟧utiq' -> ('maputiq', index of first highlighted char, 'ma-p' flag)."""
    v = marked.split(",")[0].split("/")[0].strip()
    v = re.sub(r"\(.*?\)", "", v).replace("*", "").strip()
    v = v.split()[0] if v else ""
    ma_p = v.startswith("ma-")
    v = v.replace("-", "").replace("<", "").replace(">", "")
    v = unicodedata.normalize("NFD", v)
    v = "".join(ch for ch in v if unicodedata.category(ch) != "Mn")
    v = v.replace("e", "ə").replace("ʀ", "R").replace("C", "c").replace("N", "ñ")
    idx = v.find("⟦")
    plain = v.replace("⟦", "").replace("⟧", "")
    return plain, idx, ma_p


def position(idx, length):
    return "initial" if idx == 0 else "final" if idx == length - 1 else "medial"


# ------------------------------------------------------------------------------------------------- E8
def expert_tokens():
    forms = {f["ID"]: f for f in read_csv(os.path.join(REPO, "derived", "ge2026_tables", "forms.csv"))}
    out = []
    for r in read_csv(os.path.join(REPO, "derived", "ge2026_tables", "reflexes.csv")):
        if not r["Glottocode"]:
            continue
        key, idx, ma_p = etymon_key(forms[r["Form_ID"]]["Etymon_Marked"])
        target = "ma-p" if (ma_p and idx == 2 and r["Target"] == "p") else r["Target"]
        if idx < 0:
            continue
        reflex, source = r["Reflex"], "highlight"
        if reflex == "(unmarked)":
            # not highlighted: either a zero reflex or a comparison row; read the reflex off an alignment instead
            form = [ch for ch in unicodedata.normalize("NFC", r["Form"]) if ch not in " -.()"]
            reflex, source = "", "aligned"
            if form and len(target) == 1:
                pw = Pairwise([(" ".join(key), " ".join(form))])
                pw.align(distance=True, mode="global")
                a, b, _ = pw.alignments[0]
                k = -1
                for j, x in enumerate(a):
                    if x != "-":
                        k += 1
                        if k == idx:
                            reflex = b[j]
                            break
        out.append(dict(r, Reflex=reflex, Source=source, Key=key, Index=idx, Position=position(idx, len(key)),
                        Target=target, Class=rclass(reflex, target)))
    return out


def expert_atlas(tokens):
    by = defaultdict(Counter)
    labels = defaultdict(set)
    for r in tokens:
        by[(r["Glottocode"], r["Target"], r["Position"])][r["Class"]] += 1
        labels[r["Glottocode"]].add(r["Language"])
    out = []
    for (g, t, pos), c in sorted(by.items()):
        n = sum(c.values())
        top, k = c.most_common(1)[0]
        out.append(dict(Glottocode=g, Labels="; ".join(sorted(labels[g])), Target=t, Position=pos, Tokens=n,
                        Majority=top, Majority_Share=round(k / n, 2),
                        Distribution="; ".join(f"{a}:{b}" for a, b in c.most_common())))
    write_csv(os.path.join(OUT, "expert.csv"), out)
    return out


# ------------------------------------------------------------------------------------------------- E9
_MA_P = False


def clean_pmp(v):
    v = v.split(",")[0].split("/")[0].strip()
    v = re.sub(r"\(.*?\)", "", v).replace("*", "").strip()
    v = v.split()[0] if v else ""
    global _MA_P
    _MA_P = v.startswith("ma-p")
    v = v.replace("-", "").replace("<", "").replace(">", "")
    v = unicodedata.normalize("NFD", v)
    v = "".join(ch for ch in v if unicodedata.category(ch) != "Mn")
    v = v.replace("e", "ə").replace("ʀ", "R").replace("C", "c").replace("N", "ñ")
    return list(v) if v else None


def automatic_atlas():
    abvd = os.path.join(UP, "abvd", "cldf")
    P = {r["ID"]: r["Concepticon_ID"] for r in read_csv(os.path.join(abvd, "parameters.csv"))}
    pmp = defaultdict(list)
    for r in read_csv(os.path.join(abvd, "forms.csv")):
        if r["Language_ID"] == "269" and P.get(r["Parameter_ID"]):
            toks = clean_pmp(r["Value"])
            if toks:
                pmp[P[r["Parameter_ID"]]].append((toks, _MA_P))
    role = roles()
    lr = os.path.join(UP, "lexirumah", "cldf")
    cmap = {c["ID"]: str(c["Concepticon_ID"]).split(".")[0] for c in read_csv(os.path.join(lr, "concepts.csv"))}
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv")) if l["Role"] != "TAP"}
    forms = defaultdict(list)
    for r in read_csv(os.path.join(lr, "forms.csv")):
        if r["Lect_ID"] in lects and r["Segments"]:
            forms[(r["Lect_ID"], r["Concept_ID"])].append((r["ID"], [t for t in r["Segments"].split() if t not in "+_"]))
    tokens = []
    for (lect, concept), flist in forms.items():
        for ptoks, ma_p in pmp.get(cmap.get(concept), []):
            best = None
            for fid, toks in flist:
                d = ned(sca_string(ptoks), sca_string(toks))
                if d <= 0.5 and (best is None or d < best[0]):
                    best = (d, fid, toks)
            if not best:
                continue
            pw = Pairwise([(" ".join(ptoks), " ".join(best[2]))])
            pw.align(distance=True, mode="global")
            a, b, _ = pw.alignments[0]
            k = -1
            for j, x in enumerate(a):
                if x == "-":
                    continue
                k += 1
                if ptoks[k] in CONSONANTS:
                    tg = "ma-p" if (ma_p and k == 2) else ptoks[k]
                    tokens.append(dict(Lect_ID=lect, Glottocode=lects[lect]["Glottocode"], Concept_ID=concept,
                                       Form_ID=best[1], PMP="".join(ptoks), Key="".join(ptoks), Index=k, Target=tg,
                                       Position=position(k, len(ptoks)), Form="".join(best[2]), Reflex=b[j],
                                       Class=rclass(b[j], tg), NED=round(best[0], 3)))
    write_csv(os.path.join(OUT, "automatic_tokens.csv"), tokens)
    by = defaultdict(Counter)
    for t in tokens:
        by[(t["Lect_ID"], t["Target"], t["Position"])][t["Class"]] += 1
    out = []
    for (l, tg, pos), c in sorted(by.items()):
        n = sum(c.values())
        top, k = c.most_common(1)[0]
        out.append(dict(Lect_ID=l, Glottocode=lects[l]["Glottocode"], Name=lects[l]["Name"], Target=tg,
                        Position=pos, Tokens=n,
                        Majority=top, Majority_Share=round(k / n, 2),
                        Distribution="; ".join(f"{a}:{b}" for a, b in c.most_common())))
    write_csv(os.path.join(OUT, "automatic.csv"), out)
    return out, tokens


GLOTTO_FALLBACK = {"sout2898": ["sout2898", "tetu1245", "east2473", "nort2869"], "tetu1246": ["tetu1245", "east2473"],
                   "midi1237": ["kair1265"], "eray1237": ["iliu1237"], "ilma1240": ["iliu1237"],
                   "kaha1239": ["tugu1245"], "uhak1237": ["pera1257"], "ilpu1239": ["aput1237"],
                   "luan1264": ["luan1263"], "weta1243": ["weta1243", "luan1263"], "dela1252": ["dela1251"],
                   "lewo1249": ["lama1277"], "tana1283": ["sika1262"], "wela1235": ["wela1235"]}


def groups_for(glottocode):
    return [glottocode] + GLOTTO_FALLBACK.get(glottocode, [])


def agreement(exp_tokens, auto_tokens):
    """Token-level check: same language (or its listed fallbacks), same PMP etymon, same target position."""
    ex = defaultdict(list)
    for e in exp_tokens:
        if e["Source"] == "highlight":
            ex[(e["Glottocode"], e["Key"], int(e["Index"]))].append(e)
    rows = []
    for a in auto_tokens:
        for g in groups_for(a["Glottocode"]):
            hits = [h for h in ex.get((g, a["Key"], int(a["Index"])), []) if h["Target"] == a["Target"]]
            if hits:
                classes = Counter(h["Class"] for h in hits)
                rows.append(dict(Lect_ID=a["Lect_ID"], Glottocode=g, Etymon=a["Key"], Target=a["Target"],
                                 Position=a["Position"], Form=a["Form"], Auto_Reflex=a["Reflex"], Auto_Class=a["Class"],
                                 Expert_Forms=" | ".join(sorted({h["Form"] for h in hits})),
                                 Expert_Classes=" | ".join(sorted(classes)), Agree=a["Class"] in classes))
                break
    write_csv(os.path.join(OUT, "agreement_tokens.csv"), rows)
    total = sum(r["Agree"] for r in rows)
    print(f"token agreement: {total}/{len(rows)} = {total / max(len(rows), 1):.2f}")
    by_t = defaultdict(list)
    for r in rows:
        by_t[r["Target"]].append(r["Agree"])
    for t, v in sorted(by_t.items(), key=lambda x: -len(x[1]))[:15]:
        print(f"  *{t}: {sum(v)}/{len(v)}")
    return rows


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    etok = expert_tokens()
    write_csv(os.path.join(OUT, "expert_tokens.csv"), etok)
    ex = expert_atlas(etok)
    print(f"expert atlas: {len(etok)} tokens, {len(ex)} language x target x position cells, "
          f"{len({e['Glottocode'] for e in ex})} languages")
    au, tok = automatic_atlas()
    print(f"automatic atlas: {len(au)} lect x target x position cells from {len(tok)} aligned tokens")
    agreement(etok, tok)
