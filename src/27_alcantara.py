"""E16 (Addendum 6): Idaté data from Alcantara (2015), checked against Liabut's sound-change coding.

Alcantara, Maressa Xavier. 2015. Descrição fonética e fonológica da língua idaté do Timor Leste. MA thesis,
Universidade de São Paulo. Appendix 2 lists the 184 examples used in the thesis (fieldwork mainly in Laclubar).

    python3 src/27_alcantara.py parse <thesis.pdf>     # -> derived/alcantara2015_idate/forms.csv
    python3 src/27_alcantara.py reflexes                # concept mapping, E9-style alignment, 11 characters
    python3 src/27_alcantara.py rerun                   # only if Idaté's coding changed

Alignment uses the first phonetic variant as printed, because the phonological column drops the glottal stop
(Alcantara treats it as glottalization), and *k > ʔ is one of the characters.
"""
import importlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict

from lingpy import Pairwise, ipa2tokens

sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, RES, UP, ned, read_csv, sca_string, write_csv  # noqa: E402

ra = importlib.import_module("19_reflex_atlas")
inn = importlib.import_module("21_innovations")
lit = importlib.import_module("25_literature_checks")
te = importlib.import_module("20_total_evidence")
OUT = os.path.join(REPO, "derived", "alcantara2015_idate")
TE = os.path.join(RES, "total_evidence")
IQ = os.environ.get("IQTREE", "iqtree2")

# Portuguese gloss (as printed) -> ABVD concept name. Mapped by meaning only; glosses without a clear ABVD
# counterpart (e.g. 'gordo' adjective vs ABVD 'fat/grease' noun, 'magro' vs 'thin' of objects) are left out.
GLOSS_MAP = {
    "rir": "to laugh", "água": "water", "plantar": "to plant", "pedra": "stone", "atar": "to tie up, fasten",
    "sentar": "to sit", "casa": "house", "agulha": "needle", "fígado": "liver", "comprar": "to buy",
    "ouvir": "to hear", "queimar": "to burn", "lua": "moon", "chorar": "to cry", "viver, morar": "to live, be alive",
    "vir": "to come", "língua (parte do corpo humano)": "tongue", "cavar um buraco": "to dig", "cavar": "to dig",
    "branco": "white", "boca": "mouth", "grande": "big", "grama": "grass", "osso": "bone", "barriga": "belly",
    "asa": "wing", "pesado": "heavy", "vento": "wind", "nadar": "to swim", "direita": "right", "matar": "to kill",
    "bater": "to hit", "quem": "who?", "abrir": "to open, uncover", "vermelho": "red", "mosquito": "mosquito",
    "dormir": "to sleep", "piolho": "louse", "pé": "leg/foot", "céu": "sky", "quando": "when?", "ovo": "egg",
    "órgão genital masculino, ovos": "egg", "fogo": "fire", "morder": "to bite", "eu": "I", "um": "One",
    "mãe": "mother", "pai": "father", "chuva": "rain", "rato": "rat", "ombro": "shoulder", "medo": "to fear",
    "comer": "to eat", "quatro": "Four", "pássaro": "bird", "telhado": "thatch/roof", "estragado": "rotten",
    "frio": "cold", "amarelo": "yellow", "apertar": "to squeeze", "outros": "other", "atirar a flecha": "to shoot",
    "dizer": "to say", "ele,ela": "he/she",
}


def parse(pdf):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    lines = txt.split("APÊNDICE 2")[-1].split("EMAIL PARA CONTATO")[0].splitlines()
    entries, page = [], 138
    for ln in lines:
        if re.fullmatch(r"\s{20,}\d{3}\s*", ln):
            page = int(ln.strip()) + 1
            continue
        m = re.match(r"^\s{0,4}(\d{1,3})\s{2,}(.*)$", ln)
        if m:
            cols = re.split(r"\s{2,}", m.group(2).strip())
            entries.append(dict(Number=m.group(1), Page=page, cols=[cols]))
        elif entries and ln.strip() and not ln.strip().startswith(("Número", "Lista de")):
            entries[-1]["cols"].append(re.split(r"\s{2,}", ln.strip()))
    out = []
    for i, e in enumerate(entries, 1):
        first = e["cols"][0]
        phon = first[0] if first else ""
        phonol = first[1] if len(first) > 1 else ""
        gloss = " ".join(first[2:])
        for extra in e["cols"][1:]:
            for c in extra:
                if c.startswith(("~", "[")) or (c.endswith("]") and "‘" not in c and "/" not in c):
                    phon += " " + c
                elif c.startswith("/"):
                    phonol += " " + c
                else:
                    gloss += " " + c
        if not gloss.strip() and phonol.startswith("‘"):  # layout slip (entry 67): gloss landed in column 2
            gloss, m2 = phonol, re.search(r"/[^/]+/", phon)
            phonol = m2.group(0) if m2 else ""
            phon = phon.replace(phonol, "").replace("  ", " ")
        gloss = re.sub(r"\s+", " ", gloss).strip().strip("‘’'").strip()
        out.append(dict(Seq=i, Number=e["Number"], Page=e["Page"], Phonetic=phon.strip(), Phonological=phonol.strip(),
                        Gloss_pt=gloss))
    os.makedirs(OUT, exist_ok=True)
    write_csv(os.path.join(OUT, "forms.csv"), out)
    print(len(out), "entries")


def first_variant(phonetic):
    v = phonetic.split("~")[0]
    v = v.replace("[", "").replace("]", "").replace("/", "")
    v = unicodedata.normalize("NFC", v)
    for ch in "ˈˌ.- ̩̪̚":
        v = v.replace(ch, "")
    return v.replace("Ɂ", "ʔ").replace("ː", "").replace(":", "")


def reflexes():
    abvd = os.path.join(UP, "abvd", "cldf")
    params = {r["ID"]: r for r in read_csv(os.path.join(abvd, "parameters.csv"))}
    by_name = {r["Name"]: r["ID"] for r in params.values()}
    pmp = defaultdict(list)
    for r in read_csv(os.path.join(abvd, "forms.csv")):
        if r["Language_ID"] == "269":
            toks = ra.clean_pmp(r["Value"])
            if toks:
                pmp[r["Parameter_ID"]].append((toks, ra._MA_P))
    forms = read_csv(os.path.join(OUT, "forms.csv"))
    concept_rows, by_concept = [], defaultdict(list)
    for f in forms:
        name = GLOSS_MAP.get(f["Gloss_pt"])
        if name:
            pid = by_name[name]
            concept_rows.append(dict(Seq=f["Seq"], Gloss_pt=f["Gloss_pt"], ABVD_Concept=name,
                                     Concepticon_ID=params[pid]["Concepticon_ID"]))
            v = first_variant(f["Phonetic"])
            toks = ipa2tokens(v, merge_vowels=False)
            by_concept[pid].append((f["Seq"], v, toks))
    write_csv(os.path.join(OUT, "concepts.csv"), concept_rows)
    tokens = []
    for pid, flist in by_concept.items():
        seen = set()
        for ptoks, ma_p in pmp.get(pid, []):
            best = None
            for seq, v, toks in flist:
                if v in seen:
                    continue
                d = ned(sca_string(ptoks), sca_string(toks))
                if d <= 0.5 and (best is None or d < best[0]):
                    best = (d, seq, v, toks)
            if not best:
                continue
            seen.add(best[2])
            pw = Pairwise([(" ".join(ptoks), " ".join(best[3]))])
            pw.align(distance=True, mode="global")
            a, b, _ = pw.alignments[0]
            k = -1
            for j, x in enumerate(a):
                if x == "-":
                    continue
                k += 1
                if ptoks[k] in ra.CONSONANTS:
                    tg = "ma-p" if (ma_p and k == 2) else ptoks[k]
                    tokens.append(dict(Seq=best[1], Concept=params[pid]["Name"], PMP="".join(ptoks), Index=k,
                                       Target=tg, Position=ra.position(k, len(ptoks)), Form=best[2], Reflex=b[j],
                                       Class=ra.rclass(b[j], tg), NED=round(best[0], 3)))
    write_csv(os.path.join(OUT, "tokens.csv"), tokens)
    # the 11 characters, from these tokens alone
    pooled, pos = defaultdict(Counter), defaultdict(Counter)
    for t in tokens:
        if t["Class"] not in ("", "other"):
            pooled[t["Target"]][t["Class"]] += 1
            pos[(t["Target"], t["Position"])][t["Class"]] += 1
    def majority(c):
        """Majority class with at least 2 tokens; a tie for first place has no majority."""
        top = c.most_common(2)
        if sum(c.values()) < 2 or (len(top) > 1 and top[0][1] == top[1][1]):
            return None
        return top[0][0]

    coding = {}
    for name, tgt, states in inn.CHARS:
        c = pooled.get(tgt, Counter())
        m = majority(c)
        coding[name] = dict(value="?" if m is None else str(int(m in states)), tokens=dict(c))
    for name, tgt, p, states in lit.NEW:
        c = pos.get((tgt, p), Counter())
        m = majority(c)
        coding[name] = dict(value="?" if m is None else str(int(m in states)), tokens=dict(c))
    current = {r["Taxon"]: r for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                                "innovation_matrix_24_hull.csv"))}["idat1237-cribas"]
    for name in coding:
        coding[name]["current"] = current[name]
        a, b = coding[name]["value"], current[name]
        coding[name]["status"] = ("no data" if a == "?" else "fills a gap" if b == "?" else
                                  "agrees" if a == b else "differs")
    res = dict(entries=len(forms), mapped_to_concepts=len(concept_rows), concepts=len(by_concept),
               aligned_tokens=len(tokens), coding=coding)
    os.makedirs(os.path.join(RES, "literature"), exist_ok=True)
    json.dump(res, open(os.path.join(RES, "literature", "e16_alcantara_idate.json"), "w"), indent=1,
              ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


def rerun():
    res = json.load(open(os.path.join(RES, "literature", "e16_alcantara_idate.json")))
    rows = {r["Taxon"]: r for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                             "innovation_matrix_24_hull.csv"))}
    names = [c[0] for c in inn.CHARS] + [c[0] for c in lit.NEW]
    changed = {n: c["value"] for n, c in res["coding"].items() if c["status"] in ("fills a gap", "differs")}
    if not changed:
        print("no change in Idaté's coding; nothing to rerun")
        return
    mat = {t: [r[n] for n in names] for t, r in rows.items()}
    for n, v in changed.items():
        mat["idat1237-cribas"][names.index(n)] = v
    keep = {t: r for t, r in mat.items() if any(x != "?" for x in r)}
    with open(os.path.join(TE, "innov11_alc.phy"), "w") as fh:
        fh.write(f"{len(keep)} {len(names)}\n")
        for t, r in keep.items():
            fh.write(f"{te.tx(t)} {''.join(r)}\n")
    nlex = int(open(os.path.join(TE, "lex.phy")).readline().split()[1])
    open(os.path.join(TE, "te_innov11_alc.nex"), "w").write(
        "#nexus\nbegin sets;\n"
        f"  charset lex = lex.phy: 1-{nlex};\n  charset inn = innov11_alc.phy: 1-{len(names)};\n"
        "  charpartition mine = GTR2+FO+G4:lex, GTR2+FO:inn;\nend;\n")
    subprocess.run([IQ, "-T", "1", "-seed", "1234", "-redo", "-quiet", "-B", "1000", "-p", "te_innov11_alc.nex",
                    "-pre", "te_innov11_alc"], cwd=TE, check=True)
    res["rerun"] = dict(changed_cells=changed, lexical_plus_11_innovations=te.support_from_splits(
        os.path.join(TE, "te_innov11_alc.splits.nex")))
    json.dump(res, open(os.path.join(RES, "literature", "e16_alcantara_idate.json"), "w"), indent=1,
              ensure_ascii=False)
    print(json.dumps(res["rerun"], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "parse":
        parse(sys.argv[2])
    elif cmd == "reflexes":
        reflexes()
    elif cmd == "rerun":
        rerun()
