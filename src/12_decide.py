"""Step 8: apply the pre-registered decision rules (PROTOCOL.md section 7, A2.6) and collect the headline numbers.

C1 (Idate and Lakalei):
  Edwards  if EDW-CT and EDW-LI are lexically supported, HULL-R is not, and ln BF(Ramelaic forced - forbidden) <= -5
  Hull     if HULL-R is lexically supported, EDW-CT is not, and ln BF >= 5
  otherwise unresolved
C2 (Welaun): the same with HULL98-W against EDW-CT, using ln BF(Central Timor forced - forbidden).

    python3 src/12_decide.py
"""
import json
import os

from common import RES, read_csv


def main():
    summ = {r["Hypothesis"]: r for r in read_csv(os.path.join(RES, "hypotheses", "summary_d1_lexstat.csv"))}
    sup = lambda h: summ[h]["Lexically_Supported"] == "True"
    bf_path = os.path.join(RES, "bayes", "bayes_factors.json")
    bf = json.load(open(bf_path))["contrasts"] if os.path.exists(bf_path) else {}
    c1_bf = bf.get("c1", {}).get("lnBF_pos_minus_neg")
    c2_bf = bf.get("c2", {}).get("lnBF_pos_minus_neg")

    if sup("EDW-CT") and sup("EDW-LI") and not sup("HULL-R") and c1_bf is not None and c1_bf <= -5:
        c1 = "Edwards"
    elif sup("HULL-R") and not sup("EDW-CT") and c1_bf is not None and c1_bf >= 5:
        c1 = "Hull"
    else:
        c1 = "unresolved"
    if sup("EDW-CT") and not sup("HULL98-W") and c2_bf is not None and c2_bf >= 5:
        c2 = "Edwards"
    elif sup("HULL98-W") and not sup("EDW-CT") and c2_bf is not None and c2_bf <= -5:
        c2 = "Hull 1998"
    else:
        c2 = "unresolved"

    out = dict(
        C1=dict(decision=c1, lexically_supported={h: sup(h) for h in ("HULL-R", "EDW-CT", "EDW-LI", "GE-NCT")},
                lnBF_ramelaic_forced_minus_forbidden=c1_bf),
        C2=dict(decision=c2, lexically_supported={h: sup(h) for h in ("HULL98-W", "EDW-CT")},
                lnBF_central_timor_forced_minus_forbidden=c2_bf),
        TB=dict(lexically_supported=sup("EDW-TB"), lnBF_timor_babar_forced_minus_forbidden=bf.get("tb", {}).get("lnBF_pos_minus_neg")),
        all_lexically_supported=[h for h in summ if sup(h)])
    json.dump(out, open(os.path.join(RES, "decision.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
