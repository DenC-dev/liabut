"""E30 (Addendum 9): the retention/innovation classifier, validated against ABVD experts and improved.

A cognate set is a PMP *retention* if some member is close to a PMP form, else an *innovation* (the PMP word was
replaced). Rules:
  R0  some member within SCA NED 0.5 of a PMP form (the E17 rule)
  R1  the same with the threshold chosen from 0.3 ... 0.8
  R2  reflex-aware: each PMP consonant is first replaced by the lect's majority reflex (Grimes and Edwards's expert
      atlas, else the automatic atlas, else unchanged), threshold chosen as in R1
Validation: the 30 D2 (ABVD) lects, where experts say whether each form shares a cognate set with the PMP form.

    python3 src/35_classifier.py            # writes results/literature/e30_classifier.json
Other scripts use the chosen rule through retention_status() when RETENTION_RULE=chosen is set.
"""
import csv
import importlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import DATA, REPO, RES, UP, ned, read_csv, sca_string  # noqa: E402

ra = importlib.import_module("19_reflex_atlas")
LIT = os.path.join(RES, "literature")
ATLAS = os.path.join(REPO, "derived", "reflex_atlas")
THRESHOLDS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
SIMPLER_MARGIN = 0.01


# ---------------------------------------------------------------- reflex maps
def _majority(counter):
    return counter.most_common(1)[0][0] if counter else None


def reflex_maps():
    """(code, target, position) -> majority reflex string ('' = loss). Expert atlas by glottocode; automatic by
    LexiRumah lect and by glottocode."""
    exp = defaultdict(Counter)
    exp_any = defaultdict(Counter)
    for r in read_csv(os.path.join(ATLAS, "expert_tokens.csv")):
        if r["Target"] not in ra.CONSONANTS:
            continue
        refl = "" if r["Class"] == "∅" else ra.base(r["Reflex"]).strip()
        if refl in ("-",):
            continue
        exp[(r["Glottocode"], r["Target"], r["Position"])][refl] += 1
        exp_any[(r["Glottocode"], r["Target"])][refl] += 1
    auto = defaultdict(Counter)
    auto_any = defaultdict(Counter)
    for r in read_csv(os.path.join(ATLAS, "automatic_tokens.csv")):
        if r["Target"] not in ra.CONSONANTS:
            continue
        refl = "" if r["Class"] == "∅" else ra.base(r["Reflex"]).strip()
        for code in (r["Lect_ID"], r["Glottocode"]):
            auto[(code, r["Target"], r["Position"])][refl] += 1
            auto_any[(code, r["Target"])][refl] += 1
    return exp, exp_any, auto, auto_any


MAPS = None


def reflex(lect_id, glottocode, target, pos):
    global MAPS
    if MAPS is None:
        MAPS = reflex_maps()
    exp, exp_any, auto, auto_any = MAPS
    for g in ra.groups_for(glottocode):
        for key, table in (((g, target, pos), exp), ((g, target), exp_any)):
            m = _majority(table.get(key, Counter()))
            if m is not None:
                return m
    for code in [lect_id] + ra.groups_for(glottocode):
        for key, table in (((code, target, pos), auto), ((code, target), auto_any)):
            m = _majority(table.get(key, Counter()))
            if m is not None:
                return m
    return None


def predicted(pmp_tokens, lect_id, glottocode):
    out = []
    n = len(pmp_tokens)
    for i, t in enumerate(pmp_tokens):
        if t in ra.CONSONANTS:
            r = reflex(lect_id, glottocode, t, ra.position(i, n))
            if r is None:
                out.append(t)
            elif r:
                out.extend(list(r))
        else:
            out.append(t)
    return out or pmp_tokens


# ---------------------------------------------------------------- rules
def set_status(members, pmps, rule, glotto):
    """members: [(lect_id, tokens)]; pmps: [tokens]. rule: dict(kind='R0'|'R1'|'R2', t=float)."""
    best = 9.0
    for lid, toks in members:
        if not toks:
            continue
        for p in pmps:
            ref = predicted(p, lid, glotto.get(lid, "")) if rule["kind"] == "R2" else p
            best = min(best, ned(sca_string(ref), sca_string(toks)))
    return "retention" if best <= rule["t"] else "innovation"


def chosen_rule():
    path = os.path.join(LIT, "e30_classifier.json")
    if os.environ.get("RETENTION_RULE", "R0") == "chosen" and os.path.exists(path):
        return json.load(open(path))["chosen"]
    return dict(kind="R0", t=0.5)


# ---------------------------------------------------------------- validation on D2
def abvd_pmp():
    abvd = os.path.join(UP, "abvd", "cldf")
    toks, sets = defaultdict(list), defaultdict(set)
    fid_param = {}
    for r in read_csv(os.path.join(abvd, "forms.csv")):
        if r["Language_ID"] == "269":
            fid_param[r["ID"]] = r["Parameter_ID"]
            for alt in re.split(r"[/,]", r["Value"]):
                t = ra.clean_pmp(alt)
                if t:
                    toks[r["Parameter_ID"]].append(t)
    for r in read_csv(os.path.join(abvd, "cognates.csv")):
        if r["Form_ID"] in fid_param:
            sets[fid_param[r["Form_ID"]]].add(r["Cognateset_ID"])
    return toks, sets


def validate():
    pmp_toks, pmp_sets = abvd_pmp()
    lects = {l["ID"]: l for l in read_csv(os.path.join(DATA, "d2", "lects.csv"))}
    glotto = {k: v["Glottocode"] for k, v in lects.items()}
    forms = {f["ID"]: f for f in read_csv(os.path.join(DATA, "d2", "forms.csv"))}
    expert = defaultdict(set)
    for r in read_csv(os.path.join(DATA, "d2", "cognates_expert.csv")):
        expert[r["Form_ID"]].add(r["Cognateset_ID"])
    auto = read_csv(os.path.join(RES, "cognates", "d2_lexstat.csv"))
    members = defaultdict(list)
    for r in auto:
        f = forms.get(r["Form_ID"])
        if f and pmp_toks.get(f["Concept_ID"]) and pmp_sets.get(f["Concept_ID"]):
            members[r["Cognateset_ID"]].append(r["Form_ID"])
    truth = {}
    for sid, fids in members.items():
        for fid in fids:
            if expert.get(fid):
                truth[fid] = "retention" if expert[fid] & pmp_sets[forms[fid]["Concept_ID"]] else "innovation"
    rules = [dict(kind="R0", t=0.5)] + [dict(kind="R1", t=t) for t in THRESHOLDS] + \
            [dict(kind="R2", t=t) for t in THRESHOLDS]
    scores = []
    for rule in rules:
        tp = fp = tn = fn = 0
        for sid, fids in members.items():
            concept = forms[fids[0]]["Concept_ID"]
            mem = [(forms[f]["Lect_ID"], [x for x in forms[f]["Segments"].split() if x not in "+_"]) for f in fids]
            st = set_status(mem, pmp_toks[concept], rule, glotto)
            for f in fids:
                if f not in truth:
                    continue
                pos, true = st == "retention", truth[f] == "retention"
                tp += pos and true
                fp += pos and not true
                tn += (not pos) and (not true)
                fn += (not pos) and true
        sens = tp / (tp + fn) if tp + fn else 0
        spec = tn / (tn + fp) if tn + fp else 0
        prec = tp / (tp + fp) if tp + fp else 0
        scores.append(dict(rule=rule, n=tp + fp + tn + fn, balanced_accuracy=round((sens + spec) / 2, 4),
                           accuracy=round((tp + tn) / (tp + fp + tn + fn), 4), retention_recall=round(sens, 4),
                           innovation_recall=round(spec, 4), retention_precision=round(prec, 4),
                           expert_retentions=tp + fn, expert_innovations=tn + fp))
        print(scores[-1], flush=True)
    best = {}
    for kind in ("R0", "R1", "R2"):
        best[kind] = max((s for s in scores if s["rule"]["kind"] == kind), key=lambda s: s["balanced_accuracy"])
    chosen = best["R0"]
    for kind in ("R1", "R2"):
        if best[kind]["balanced_accuracy"] > chosen["balanced_accuracy"] + SIMPLER_MARGIN:
            chosen = best[kind]
    res = dict(validation_forms=scores[0]["n"], scores=scores, best_by_kind=best, chosen=chosen["rule"],
               chosen_scores=chosen)
    json.dump(res, open(os.path.join(LIT, "e30_classifier.json"), "w"), indent=1, ensure_ascii=False)
    print("chosen", chosen)


if __name__ == "__main__":
    validate()
