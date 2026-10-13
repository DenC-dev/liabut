"""Collect every estimate the paper's main text reports into results/principal_estimates.csv, with the file and key
it comes from, so each number can be traced and rechecked. Run after the analyses (see reproduce.sh).

    python3 src/44_principal.py
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import REPO, RES  # noqa: E402

LIT = os.path.join(RES, "literature")


def J(path):
    return json.load(open(os.path.join(RES, path), encoding="utf-8"))


def get(path, *keys):
    d = J(path)
    for k in keys:
        d = d[k]
    return d


ROWS = [
    # (section, estimate, file, keys, script)
    ("Pre-registered", "C1 decision (step 8)", "decision.json", ("C1", "decision"), "src/12_decide.py"),
    ("Pre-registered", "C2 decision (step 8)", "decision.json", ("C2", "decision"), "src/12_decide.py"),
    ("Trees", "Posterior, Lakalei-Idate + Central Timor (unrooted)", "bayes/posterior_clades.json",
     ("Central Timor with Welaun + Lakalei-Idate",), "src/09_bayes.py"),
    ("Trees", "Posterior, Timor-Babar (unrooted)", "bayes/posterior_clades.json", ("Timor-Babar (Edwards; G&E)",),
     "src/09_bayes.py"),
    ("Trees", "Posterior, Lakalei-Idate + Eastern Timor (unrooted)", "bayes/posterior_clades.json",
     ("Eastern Timor + Lakalei-Idate (G&E, possible)",), "src/09_bayes.py"),
    ("Root", "Root on Flores, seven outgroups, MrBayes", "literature/e40_root.json",
     ("primary MrBayes", "root_categories", "Flores pair | rest"), "src/41_addendum12.py e40sum"),
    ("Root", "Root on Rote-Meto + Helong, seven outgroups, MrBayes", "literature/e40_root.json",
     ("primary MrBayes", "root_categories", "Rote-Meto + Helong (with or without Flores) | rest"),
     "src/41_addendum12.py e40sum"),
    ("Root", "Root on Central Timor stem, seven outgroups, MrBayes", "literature/e40_root.json",
     ("primary MrBayes", "root_categories", "Central Timor (with or without Welaun) | rest"),
     "src/41_addendum12.py e40sum"),
    ("Root", "Lakalei-Idate + Central Timor rooted clade, MrBayes", "literature/e40_root.json",
     ("primary MrBayes", "rooted_clades", "LI + Central Timor (with or without Welaun)"), "src/41_addendum12.py e40sum"),
    ("Root", "Same, UFBoot, all seven outgroups", "literature/e40_root.json",
     ("primary UFBoot", "rooted_clades", "LI + Central Timor (with or without Welaun)"), "src/41_addendum12.py e40sum"),
    ("Root", "Same, UFBoot, far outgroups", "literature/e40_root.json",
     ("far UFBoot", "rooted_clades", "LI + Central Timor (with or without Welaun)"), "src/41_addendum12.py e40sum"),
    ("Root", "Same, UFBoot, near outgroups", "literature/e40_root.json",
     ("near UFBoot", "rooted_clades", "LI + Central Timor (with or without Welaun)"), "src/41_addendum12.py e40sum"),
    ("Root", "Timor-Babar rooted clade, MrBayes", "literature/e40_root.json",
     ("primary MrBayes", "rooted_clades", "Timor-Babar incl. LI"), "src/41_addendum12.py e40sum"),
    ("Root", "Root on Central Timor stem in every E57 variant below 0.05", "literature/e57_root_sensitivity.json",
     ("robust (CT stem share < 0.05 in every variant)",), "src/43_addendum14.py e57"),
    ("Kept together", "UFBoot with Central Timor, primary lists", "literature/e44_li_together.json",
     ("primary: Lakalei-Idate monophyletic", "support", "with Central Timor (with Welaun if present)"),
     "src/41_addendum12.py e44"),
    ("Kept together", "UFBoot with Central Timor, independent lists", "literature/e44_li_together.json",
     ("independent: Lakalei-Idate monophyletic", "support", "with Central Timor (with Welaun if present)"),
     "src/41_addendum12.py e44"),
    ("Kept together", "UFBoot with Habu, Idaté alone, primary lists", "literature/e44_li_together.json",
     ("primary: Idate alone", "support", "with Habu"), "src/41_addendum12.py e44"),
    ("Topology tests", "AU p, Timor-Babar rooted, primary", "literature/e45_au_rooted.json",
     ("primary", "Timor-Babar incl. Lakalei-Idate, rooted", "p_AU"), "src/41_addendum12.py e45"),
    ("Topology tests", "AU p, Lakalei-Idate + Eastern Timor, primary", "literature/e45_au_rooted.json",
     ("primary", "Lakalei-Idate + Eastern Timor", "p_AU"), "src/41_addendum12.py e45"),
    ("Topology tests", "AU p, Lakalei-Idate + Eastern Timor, independent", "literature/e45_au_rooted.json",
     ("independent", "Lakalei-Idate + Eastern Timor", "p_AU"), "src/41_addendum12.py e45"),
    ("Topology tests", "Smallest Holm-adjusted p over all eleven tests", "literature/e45_au_rooted.json",
     ("holm_all_topology_tests", "E45 primary Timor-Babar incl. Lakalei-Idate, rooted", "holm"),
     "src/41_addendum12.py e45"),
    ("Topology tests", "SOWH p, eastern placement, primary", "literature/e38_sowh_primary.json", ("p",),
     "src/40_addendum11.py e38"),
    ("Bayes factors", "ln BF, Lakalei-Idate + Central Timor against Lakalei-Idate + Eastern Timor",
     "literature/e47_direct_bf.json", ("lnBF LI+CT vs LI+ET",), "src/41_addendum12.py e47sum"),
    ("Bayes factors", "ln BF, Central Timor with Welaun against Welaun + Tetun", "literature/e47_direct_bf.json",
     ("lnBF CT with Welaun vs Welaun+Tetun",), "src/41_addendum12.py e47sum"),
    ("Shared innovations", "Cleaned, polarised, stable: LI + NCT against Habu",
     "literature/e46_triplets_clean.json",
     ("R2 cleaned and polarised (Flores, Rote-Meto + Helong, Wetar)", "representative (LI, NCT, Habu)", "stable",
      "counts", "LI+NCT"), "src/41_addendum12.py e46"),
    ("Shared innovations", "Cleaned, polarised, stable: LI + Habu", "literature/e46_triplets_clean.json",
     ("R2 cleaned and polarised (Flores, Rote-Meto + Helong, Wetar)", "representative (LI, NCT, Habu)", "stable",
      "counts", "LI+Habu"), "src/41_addendum12.py e46"),
    ("Sound changes", "*p kept, Lakalei-Idate (kept, words)", "literature/e42_sound_irreversible.json",
     ("e2_p_kept", "lakalei_idate"), "src/41_addendum12.py e42"),
    ("Sound changes", "*p kept, Nuclear Central Timor (kept, words)", "literature/e42_sound_irreversible.json",
     ("e2_p_kept", "nuclear_central_timor"), "src/41_addendum12.py e42"),
    ("Sound changes", "*p lenition, origins on the lexical tree if irreversible", "literature/e56_reversibility.json",
     ("p lenition", "1000", "cost", "H"), "src/43_addendum14.py e56"),
    ("Sound changes", "*p lenition, origins on Grimes and Edwards's split if irreversible",
     "literature/e56_reversibility.json", ("p lenition", "1000", "cost", "GE"), "src/43_addendum14.py e56"),
    ("Sound changes", "*p lenition, cheapest tree when a restoration costs as much as a change",
     "literature/e56_reversibility.json", ("p lenition", "1", "cheapest"), "src/43_addendum14.py e56"),
    ("Sound changes", "*p lenition, cheapest tree when a restoration costs twice a change",
     "literature/e56_reversibility.json", ("p lenition", "2", "cheapest"), "src/43_addendum14.py e56"),
    ("Calibration", "Undisputed sound-change groups recovered at posterior 0.95 (of 10)",
     "literature/e43_known_groups.json", ("summary", "recovered_MrBayes_095"), "src/41_addendum12.py e43"),
]


def main():
    out = []
    for sec, name, path, keys, script in ROWS:
        v = get(path, *keys)
        out.append(dict(Section=sec, Estimate=name, Value=json.dumps(v, ensure_ascii=False), File=f"results/{path}",
                        Key=" > ".join(keys), Produced_by=script))
    p = os.path.join(RES, "principal_estimates.csv")
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(f"{r['Section']:20s} {r['Estimate'][:70]:70s} {r['Value']}")
    print("wrote", os.path.relpath(p, REPO))


if __name__ == "__main__":
    main()
