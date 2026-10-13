"""Addendum 14 (requested in review): E56 reversibility sweep, E57 root sensitivity, and documentation tables.

    python3 src/43_addendum14.py e56          Sankoff parsimony over restoration costs (seconds)
    python3 src/43_addendum14.py e57          IQ-TREE runs for the root variants (about 10 minutes), then the tally
    python3 src/43_addendum14.py audit        derived/audit/: exclusion and reclassification trail with reason codes
    python3 src/43_addendum14.py decisive     derived/audit/decisive_comparisons.csv
    python3 src/43_addendum14.py reflexes     derived/audit/p_reflexes.csv (every *p token for the focal lects)
Needs IQ-TREE ($IQTREE) for e57.
"""
import importlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, read_csv, write_csv  # noqa: E402

a12 = importlib.import_module("41_addendum12")
a13 = importlib.import_module("42_addendum13")
a9 = a12.a9
tx = a12.tx
LIT = a12.LIT
TAXA, FLORES, CT, NCT, LI, ET, TB = a12.TAXA, a12.FLORES, a12.CT, a12.NCT, a12.LI, a12.ET, a12.TB
AUDIT = os.path.join(REPO, "derived", "audit")
W57 = os.path.join(LIT, "e57")
RATIOS = [0.1, 0.25, 0.5, 1, 2, 3, 5, 10, 1000]


# ---------------------------------------------------------------- E56
def sankoff(tree, states, r):
    """Binary Sankoff: 0 -> 1 costs 1, 1 -> 0 costs r; '?' free; root state fixed at 0."""
    INF = 1e9

    def go(c):
        if c.is_terminal():
            v = states.get(c.name, "?")
            return (0.0 if v in ("0", "?") else INF, 0.0 if v in ("1", "?") else INF)
        f0, f1 = 0.0, 0.0
        for ch in c.clades:
            a0, a1 = go(ch)
            f0 += min(a0, 1 + a1)
            f1 += min(a1, r + a0)
        return (min(f0, INF), min(f1, INF))
    return go(tree.root)[0]


def rival_trees():
    from Bio import Phylo
    paths = {"H": os.path.join(RES, "total_evidence", "lex_only.treefile"),
             "G": os.path.join(LIT, "e21_abc", "G.treefile"),
             "GE": os.path.join(LIT, "e29", "GE.treefile")}
    return {k: a12.root_on(Phylo.read(v, "newick"), FLORES) for k, v in paths.items()}


def e56():
    trees = rival_trees()
    m42, c42, _ = a12.e42_matrix()
    c53, m53 = a13.e53_matrix()
    sets = {
        "p lenition": [{tx(k): v["p_lenited"] for k, v in m42.items()}],
        "eleven E42 characters": [{tx(k): v[ch] for k, v in m42.items()} for ch in c42],
        "36 E53 characters": [{tx(t): m53[t][i] for t in TAXA} for i in range(len(c53))],
    }
    res = {"ratios": RATIOS, "note": "cost of a restoration (1 -> 0) relative to a change (0 -> 1); root state 0"}
    for name, chars in sets.items():
        rows = {}
        for r in RATIOS:
            cost = {k: round(sum(sankoff(t, st, r) for st in chars), 3) for k, t in trees.items()}
            best = min(cost.values())
            rows[str(r)] = dict(cost=cost, cheapest=[k for k, v in cost.items() if abs(v - best) < 1e-9])
        res[name] = rows
    # checks against E42 (Camin-Sokal) and E53
    e42 = json.load(open(os.path.join(LIT, "e42_sound_irreversible.json")))
    for k in trees:
        cs = e42["trees"][f"{k}, rooted on Flores pair"]["per_character"]["p_lenited"]["camin_sokal"]
        assert res["p lenition"]["1000"]["cost"][k] == cs, (k, cs)
    json.dump(res, open(os.path.join(LIT, "e56_reversibility.json"), "w"), indent=1)
    for name in sets:
        print(name)
        for r in RATIOS:
            v = res[name][str(r)]
            print(f"  r={r:<6} H {v['cost']['H']:>7}  G {v['cost']['G']:>7}  GE {v['cost']['GE']:>7}  cheapest {v['cheapest']}")


# ---------------------------------------------------------------- E57
def phy_variant(rows, taxa, path, missing_as_absent=False):
    attested, sets, concept_of = defaultdict(set), defaultdict(set), {}
    for r in rows:
        if r["Lect_ID"] in taxa:
            attested[r["Lect_ID"]].add(r["Concept_ID"])
            sets[r["Cognateset_ID"]].add(r["Lect_ID"])
            concept_of[r["Cognateset_ID"]] = r["Concept_ID"]
    chars = sorted(sets, key=lambda s: (concept_of[s], s))
    miss = "0" if missing_as_absent else "?"
    with open(path, "w") as fh:
        fh.write(f"{len(taxa)} {len(chars)}\n")
        for t in taxa:
            fh.write(tx(t) + " " + "".join(("1" if t in sets[s] else "0") if concept_of[s] in attested[t] else miss
                                           for s in chars) + "\n")
    return len(chars)


def e57_variants(rows):
    og = list(a12.OG)
    out = {}
    for o in og:
        taxa = TAXA + [x for x in og if x != o]
        ref = "og-buginese" if o == "og-tagalog" else "og-tagalog"
        out[f"without {o[3:]}"] = dict(rows=rows, taxa=taxa, ref=ref, absent=False)
    out["missing coded as absent"] = dict(rows=rows, taxa=TAXA + og, ref="og-tagalog", absent=True)
    have = defaultdict(set)
    for r in rows:
        if r["Lect_ID"] in og:
            have[r["Concept_ID"]].add(r["Lect_ID"])
    full = {c for c, s in have.items() if len(s) == len(og)}
    out["only concepts attested in all seven outgroups"] = dict(
        rows=[r for r in rows if r["Concept_ID"] in full], taxa=TAXA + og, ref="og-tagalog", absent=False,
        concepts=len(full))
    return out


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def e57():
    os.makedirs(W57, exist_ok=True)
    rows = a12.e40_rows()
    res = {}
    for name, v in e57_variants(rows).items():
        s = slug(name)
        p = os.path.join(W57, f"{s}.phy")
        n = phy_variant(v["rows"], v["taxa"], p, v["absent"])
        if not os.path.exists(os.path.join(W57, f"{s}.ufboot")):
            a9.iqtree(p, s, ("-B", "1000", "-wbt"))
        uf = a12.tally(a12.read_trees(os.path.join(W57, f"{s}.ufboot")), TAXA, tx(v["ref"]))
        ml = a12.tally(a12.read_trees(os.path.join(W57, f"{s}.treefile")), TAXA, tx(v["ref"]))
        cats = uf["root_categories"]
        ct_stem = cats["Central Timor (with or without Welaun) | rest"] + cats["Lakalei-Idate + Central Timor | rest"]
        res[name] = dict(characters=n, taxa=len(v["taxa"]), reference=v["ref"], concepts=v.get("concepts"),
                         UFBoot=uf, ML_root=next(iter(ml["root_positions"])), ct_stem_share=round(ct_stem, 3))
        print(f"{name:52s} chars {n:5d}  CT stem {ct_stem:.3f}  LI+CT {uf['rooted_clades']['LI + Central Timor (with or without Welaun)']:.2f}"
              f"  TB {uf['rooted_clades']['Timor-Babar incl. LI']:.2f}  top {list(uf['root_positions'].items())[:2]}", flush=True)
    res["robust (CT stem share < 0.05 in every variant)"] = all(
        v["ct_stem_share"] < 0.05 for v in res.values() if isinstance(v, dict))
    json.dump(res, open(os.path.join(LIT, "e57_root_sensitivity.json"), "w"), indent=1)
    print("robust:", res["robust (CT stem share < 0.05 in every variant)"])


# ---------------------------------------------------------------- documentation tables
WEST_GROUPS = ("Flores-Lembata", "Rote", "Meto", "Helong", "Wetar")


def _lects():
    return {l["ID"]: l for l in read_csv(os.path.join(DATA, "d1", "lects.csv"))}


def flag_code(text):
    w = text.lower()
    if "split" in w:
        return "ERR-SPLIT"
    if "not cognate" in w:
        return "ERR-NONCOGNATE"
    if "doubtful" in w:
        return "DOUBTFUL"
    return "RET-REVIEW"


def audit():
    """Every form or cognate set excluded or reclassified anywhere in the analyses, with a reason code.
    Codes are defined in DATA_DICTIONARY.md."""
    from pipeline import flags, variant_rows
    os.makedirs(AUDIT, exist_ok=True)
    lects = _lects()
    in24 = set(TAXA)
    forms = {r["ID"]: r for r in read_csv(os.path.join(DATA, "d1", "forms.csv"))}
    tl = {r["Form_ID"]: r for r in read_csv(os.path.join(REPO, "derived", "loans", "tetun_loans.csv"))}
    out = []
    form_codes = [("L1_expert", "LOAN-SOURCE", "every analysis except the unscreened variant",
                   "marked as a loan in the source list"),
                  ("L3_indonesian", "LOAN-INDONESIAN", "every analysis except the unscreened variant",
                   "matches the Indonesian word for the concept (step 3 screen)"),
                  ("L4_portuguese", "LOAN-PORTUGUESE", "every analysis except the unscreened variant",
                   "matches the Portuguese word for the concept (step 3 screen)"),
                  ("L2_contact", "CONTACT-SCREEN", "the contact-screened variant only (Papuan lects)",
                   "Papuan-lect form resembling an Austronesian one (step 3 screen)"),
                  ("L5_tetun", "TETUN-LOOKALIKE", "the Tetun-screened variant only",
                   "near-identical to the Tetun word (step 3 screen)")]
    for fid, g in flags("d1").items():
        f = forms.get(fid, {})
        for col, code, scope, why in form_codes:
            if str(g.get(col)) != "True":
                continue
            reason = why
            if col == "L5_tetun" and fid in tl:
                t = tl[fid]
                reason += f"; sound-change verdict: {t['Verdict']}"
                ev = "; ".join(x for x in (t["Loan_Evidence"], t["Inherited_Evidence"]) if x)
                if ev:
                    reason += f" ({ev})"
            match = g.get({"L3_indonesian": "L3_match", "L4_portuguese": "L4_match", "L5_tetun": "L5_match"}.get(col, ""), "")
            out.append(dict(Level="form", ID=fid, Lect_ID=f.get("Lect_ID", ""), In_24=f.get("Lect_ID") in in24,
                            Concept_ID=f.get("Concept_ID", ""), Form=f.get("Form", ""), Code=code, Applies_to=scope,
                            Reason=reason + (f"; match: {match}" if match else ""), Source_analysis="step 3"))
    # set level: review flags, ACD strict, Grimes and Edwards tables
    st_r2 = {r["Cognateset_ID"]: r["Status"] for r in read_csv(os.path.join(REPO, "derived", "innovations",
                                                                           "cognate_set_status_r2.csv"))}
    for sid, why in a12.REFEREE_FLAGS.items():
        out.append(dict(Level="cognate set", ID=sid, Lect_ID="", In_24=True, Concept_ID=sid.rsplit("-", 1)[0], Form="",
                        Code=flag_code(why), Applies_to="E46 cleaned counts and the second-round decision",
                        Reason=f"{why}; R2 status before review: {st_r2.get(sid, 'n/a')}",
                        Source_analysis="mock review (paper/review)"))
    for r in read_csv(os.path.join(LIT, "e35_reclassified_sets_strict.csv")):
        out.append(dict(Level="cognate set", ID=r["Cognateset_ID"], Lect_ID="", In_24=True, Concept_ID=r["Concept"],
                        Form="", Code="RET-ACD", Applies_to="E46 cleaned counts and the second-round decision",
                        Reason=f"strict match to {r['Etymon']} (NED {r['NED']}); R2 status before: "
                               f"{st_r2.get(r['Cognateset_ID'], 'n/a')}", Source_analysis="E35"))
    for r in read_csv(os.path.join(LIT, "e37_ge_verdicts.csv")):
        if r["Verdict"] != "inherited":
            continue
        out.append(dict(Level="cognate set", ID=r["Cognateset_ID"], Lect_ID="", In_24=True, Concept_ID=r["Concept"],
                        Form="", Code="RET-GE-TABLES", Applies_to="E46 cleaned counts and the second-round decision",
                        Reason=f"inherited in Grimes and Edwards's tables: {r['Evidence']}", Source_analysis="E37"))
    # polarisation and Papuan-shared sets
    prim = variant_rows("d1", "lexstat", "primary")
    members = defaultdict(set)
    for r in prim:
        members[r["Cognateset_ID"]].add(r["Lect_ID"])
    west = {l for l, v in lects.items() if v["Group"] in WEST_GROUPS}
    for sid, st in st_r2.items():
        if st == "innovation" and members[sid] & west:
            out.append(dict(Level="cognate set", ID=sid, Lect_ID="", In_24=True, Concept_ID=sid.rsplit("-", 1)[0],
                            Form="", Code="POL-WEST", Applies_to="polarised counts only (E46, E51)",
                            Reason="R2 innovation also present in " + ", ".join(sorted(
                                lects[l]["Name"] for l in members[sid] & west)), Source_analysis="E46"))
    tap = {l for l, v in lects.items() if v["Role"] == "TAP"}
    chars = {r["Cognateset_ID"] for r in read_csv(os.path.join(RES, "bayes", "characters.csv"))}
    for sid in sorted(chars):
        if members[sid] & tap:
            out.append(dict(Level="cognate set", ID=sid, Lect_ID="", In_24=True, Concept_ID=sid.rsplit("-", 1)[0],
                            Form="", Code="PAPUAN-SHARED", Applies_to="the E48 sensitivity run only",
                            Reason="set has a member in a Papuan lect: " + ", ".join(sorted(
                                lects[l]["Name"] for l in members[sid] & tap))[:200], Source_analysis="E48"))
    write_csv(os.path.join(AUDIT, "exclusions.csv"), out)
    c = Counter(r["Code"] for r in out)
    json.dump(dict(rows=len(out), by_code=dict(c)), open(os.path.join(AUDIT, "exclusions_summary.json"), "w"), indent=1)
    print(len(out), "rows", dict(c))


def decisive():
    """The decisive cognate comparisons on both sides: E27 packet (stable, LI + NCT / LI + X) and E17 exclusive sets."""
    os.makedirs(AUDIT, exist_ok=True)
    packet = read_csv(os.path.join(REPO, "derived", "innovations", "reviewer_packet_lakalei_idate_stable.csv"))
    excl = read_csv(os.path.join(REPO, "derived", "innovations", "reviewer_packet_exclusive_sets.csv"))
    aud = defaultdict(list)
    for r in read_csv(os.path.join(AUDIT, "exclusions.csv")):
        if r["Level"] == "cognate set":
            aud[r["ID"]].append(f"{r['Code']}: {r['Reason']}")
    e52 = json.load(open(os.path.join(LIT, "e52_correspondences.json")))["decisive"]
    rows = []
    seen = set()
    for src, rs in (("packet (stable triplet counts)", packet), ("exclusive set (E17)", excl)):
        for r in rs:
            sid = r.get("Cognateset_ID") or r.get("Set") or r.get("ID")
            if not sid or (sid, src) in seen:
                continue
            seen.add((sid, src))
            corr = e52.get(sid, {}).get("by_side", {})
            corr_txt = "; ".join(f"{k}: {v['verdict']} ({v['loan_like_positions']} loan-like, "
                                 f"{v['inheritance_like_positions']} inheritance-like)" for k, v in corr.items())
            etym = (r.get("ACD_strict_best_etymon") or r.get("ACD_strict_etymon") or r.get("ACD_best_etymon") or
                    ("PMP *" + r["PMP"] if r.get("PMP") else ""))
            rows.append(dict(Cognateset_ID=sid, Source=src, Concept=r.get("Concept", ""),
                             Pairing=r.get("Counted_as") or ("LI + " + r["Shared_with"] if r.get("Shared_with") else ""),
                             Forms=r.get("Forms", ""), Etymon_above_Timor=etym,
                             Status_before_review=r.get("Status", "innovation"),
                             Grimes_Edwards_tables=r.get("Grimes_Edwards_tables", ""),
                             Reconstruction="to be supplied by specialist review",
                             Correspondence_test_E52=corr_txt or "no informative pair",
                             Audit="; ".join(aud.get(sid, [])) or "kept as an innovation",
                             Counted_after_cleaning="no" if aud.get(sid) and any(
                                 a.split(":")[0] in ("RET-REVIEW", "RET-ACD", "RET-GE-TABLES", "ERR-SPLIT",
                                                     "ERR-NONCOGNATE", "DOUBTFUL") for a in aud[sid]) else "yes",
                             Specialist_verdict=""))
    write_csv(os.path.join(AUDIT, "decisive_comparisons.csv"), rows)
    print(len(rows), "rows", Counter(r["Counted_after_cleaning"] for r in rows), Counter(r["Source"] for r in rows))


FOCAL = ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun", "laka1255", "idat1237-cribas",
         "tetu1245-suai", "habu1241", "waim1252", "naue1237", "midi1237", "lama1277-lewoi", "sika1262-hewa"]


def environment(pmp, idx):
    """Phonological environment of the PMP segment at idx: initial, intervocalic, preconsonantal, final."""
    segs = list(pmp)
    V = set("aeiouə")
    prev = segs[idx - 1] if idx > 0 else None
    nxt = segs[idx + 1] if idx + 1 < len(segs) else None
    if prev is None:
        return "word-initial"
    if nxt is None:
        return "word-final"
    if prev in V and nxt in V:
        return "between vowels"
    if nxt not in V:
        return "before a consonant"
    return "after a consonant"


def reflexes():
    """Every *p token for the focal lects in the automatic atlas, plus the expert atlas for the same lects."""
    os.makedirs(AUDIT, exist_ok=True)
    rows = []
    for r in read_csv(os.path.join(REPO, "derived", "reflex_atlas", "automatic_tokens.csv")):
        if r["Lect_ID"] in FOCAL and r["Target"] == "p":
            try:
                env = environment(r["PMP"], int(r["Index"]))
            except Exception:
                env = r["Position"]
            loan = ""
            rows.append(dict(Atlas="automatic", Lect_ID=r["Lect_ID"], Concept=r["Concept_ID"], PMP="*" + r["PMP"],
                             Position=r["Position"], Environment=env, Form=r["Form"], Reflex=r["Reflex"],
                             Reflex_class=r["Class"], NED_to_PMP=r["NED"], Note=loan))
    exp = read_csv(os.path.join(REPO, "derived", "reflex_atlas", "expert_tokens.csv"))
    gl = {t.split("-")[0] for t in FOCAL}
    for r in exp:
        g = r.get("Glottocode", "")
        if g in gl and r.get("Target") == "p":
            try:
                env = environment(re.sub(r"[^a-zəŋ]", "", r["Key"]), int(r["Index"]))
            except Exception:
                env = r["Position"]
            rows.append(dict(Atlas="expert (Grimes and Edwards tables)", Lect_ID=g, Concept=r["Caption"],
                             PMP=r["Etymon"], Position=r["Position"], Environment=env, Form=r["Form"],
                             Reflex=r["Reflex"], Reflex_class=r["Class"], NED_to_PMP="",
                             Note=f"{r['Language']}, table {r['Table']}"))
    write_csv(os.path.join(AUDIT, "p_reflexes.csv"), rows)
    summ = defaultdict(Counter)
    for r in rows:
        summ[(r["Atlas"].split()[0], r["Lect_ID"])][r["Reflex_class"]] += 1
    for k, v in sorted(summ.items()):
        print(k, dict(v))


if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])
