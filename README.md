# Liabut

**A pre-registered computational test of how the Austronesian languages of Timor branch.**

*Liabut* is coined from Tetun *lia* 'word, speech' and *abut* 'root': the roots of words. The project asks how Timor's languages branch from one another, and which of them are closest kin. (It was called Sanak until 11 October 2026.)

Dennis Crowley, Phaistos Labs.

- **Working paper:** [`paper/liabut.pdf`](paper/liabut.pdf), a Phaistos Labs preprint (not peer reviewed). Source in [`paper/`](paper); rebuild with `bash paper/build.sh`.
- **Website:** [`docs/index.html`](docs/index.html), for GitHub Pages at <https://denc-dev.github.io/liabut/>.

## The question

Two classifications disagree.

- **Hull (1998, 2001)** puts all of Timor's Austronesian languages in one *Timoric* group, split into *Ramelaic* (Mambae, Kemak, Tokodede, Idaté, Lakalei) and *Fabronic* (Tetun, Habun, Kawaimina, Galoli, Wetarese, Meto).
- **Edwards (2021)** and **Grimes and Edwards (2026)** make *Central Timor* (Mambae, Kemak, Tokodede, Welaun) a separate branch of Malayo-Polynesian. Everything else, including Idaté and Lakalei, belongs to *Timor-Babar*, defined by the sound change *p > h.

The sharpest point of disagreement is where Idaté and Lakalei belong (contrast C1). A second is whether Welaun is a Tetun dialect or a Central Timor language (C2).

The method follows Robinson and Holton (2012), who used lexical data to find subgroups in Alor-Pantar that sound changes alone couldn't settle.

## Results in brief

- **Hull's Fabronic (Timoric A) gets no lexical support.** It gets 0% support in every analysis.
- **Timor-Babar and Eastern Timor get no lexical support either.** They get 0–3% bootstrap support, and the Bayes factor runs against Timor-Babar (ln BF −7.0). They rest on sound changes, so this does not refute them.
- **Welaun is Central Timor (C2).** The Bayes factor is +10.3, and its Tetun look disappears on borrowing-resistant vocabulary.
- **Idaté-Lakalei (C1) remains unresolved, but leans Central Timor.**
  - Every tree puts it next to Central Timor (posterior 0.91; ln BF +8.0 for Hull's Ramelaic), and so do lists collected independently of Grimes and Edwards (97% UFBoot, a confirmatory test in Addendum 9).
  - On those independent lists an AU test rejects Lakalei-Idate + Eastern Timor (p = 0.025) and Timor-Babar (p = 0.042) as lexical groups. On the original lists it did not (p = 0.07).
  - Taking out words that the Austronesian Comparative Dictionary traces to PAN, PMP, Proto-Central-Eastern or Proto-Central Malayo-Polynesian leaves the stable-vocabulary pairing with Central Timor in place.
  - Its sound changes look like Timor-Babar's (*p > h, *ŋ > n, no *ŋ > g). But scored by parsimony, the coded changes cost the same on either placement (30 steps), and Welaun, a Central Timor language, also has *p > h.
  - A borrowing model with borrowing from both sides can't separate the two placements (posterior 0.58 against 0.42). An earlier one-way version had favoured Grimes and Edwards's (0.875); that preference doesn't survive.
  - On stable vocabulary, shared replacements pair Idaté-Lakalei with Central Timor against Habu and Kawaimina for every choice of dialect list, but not against Tetun: that prediction failed in both confirmatory replications (with Tetun Dili, and by one concept with both Tetun lists pooled).
  - No contact signal for Idaté-Lakalei survives calibration against unequal rates or multiple-testing correction; only Welaun's Tetun loans do.
  - Support depends on cognate coding (15–97%), though Timor-Babar gets 0 under every coding and data set.
  - Hull (1998, 2001) and Carvalho (2001) already grouped Idaté-Lakalei this way. Hull's *b > h evidence shows up in Grimes and Edwards's own data, but Galoli and Ili'uun share it (see [`results/LITERATURE.md`](results/LITERATURE.md)).
- **The low-level groups are confirmed:** Lakalei-Idate, Kawaimina, Wetar-Atauro, Wetar, Nuclear Rote, Kisar-Luang and Babar.
- **The pre-registered step 8 verdict is "unresolved" for both C1 and C2.**

## New data

The expansion (Addendum 4) built datasets that didn't exist in machine-readable form. They are in [`derived/`](derived), each documented in [`derived/README.md`](derived/README.md).

- **Grimes and Edwards (2026) comparative tables as data:** 14,401 forms from 257 tables, mapped to 207 Glottocodes, with the authors' highlighted reflexes.
- **Reflex atlases of PMP consonants.**
  - Expert: 8,426 tokens across 186 languages.
  - Automatic: 4,978 tokens across 64 LexiRumah lects.
  - The two agree on 94% of tokens.
- **Innovation profiles:** eight diagnostic sound changes coded for 65 Timor-region languages.
- **Loans identified by sound change:** 740 Tetun look-alikes classified, 21 of them as probable loans.
- **Cognate sets exclusive to Lakalei-Idate and Central Timor**, including 'cry' (Idaté *sɛro*, Mambae *sero*, Welaun *soː*, against *tanis* < *taŋis elsewhere).
- **Idaté word list from Alcantara (2015):** 184 forms from Laclubar, machine-readable, with PMP alignments.
- **Retention or innovation status for every cognate set** in the 24-taxon analysis, measured against Proto-Malayo-Polynesian (`derived/innovations/`).

## What's new

This was checked against the published literature on 10 October 2026. See *Novelty check* in the report.

- **First cognate-based phylogenetic placement of Idaté, Lakalei, Welaun, Habu, Midiki and Helong.**
  - None of them is in ABVD, so none appears in the Bayesian Austronesian tree of Gray et al. (2009).
  - Idaté, Welaun, Habu and Helong do have short ASJP lists, so they sit in ASJP's global automated similarity data. No study was found that examines those results for Timor.
  - Kaiping and Klamer (2022) used LexiRumah for the Papuan languages only.
- **First explicit test of Hull against Edwards / Grimes and Edwards.** Grimes and Edwards (2026) do not cite Hull.
- **New results.**
  - Lakalei-Idate's vocabulary sits with Central Timor, and geography doesn't explain the tie. Its sound changes go the other way.
  - Welaun sits in Central Timor once borrowing is controlled.
  - Tetun similarity in the disputed languages is concentrated in borrowable words.
  - LexiRumah's automatic cognates are validated for Timor's Austronesian languages.
  - Total-evidence trees (vocabulary plus sound changes) for these languages, and the datasets listed under *New data*.
  - Welaun's *p > h breaks Timor-Babar's single defining change, and *ŋ > n turns up in the outgroup.
- **Confirmations rather than discoveries.**
  - The lexical absence of Timor-Babar and of Hull's Fabronic, and Tetun's lexical pull towards Central Timor, are already in Gray et al.'s 2009 posterior trees. Re-scored here (`results/gray2009_timor_clades.json`), they give Timor-Babar 0.00 and Tetum + Mambai + Kemak 0.71. As far as could be found, this was never written up.
  - The low-level groups and the *p and *ŋ diagnostics were already known.

See [`results/REPORT.md`](results/REPORT.md) for the full write-up and [`results/figures/`](results/figures) for the charts.

## How it was done

| Step | What | Where |
|---|---|---|
| 0 | Protocol frozen before any analysis; ten addenda, each dated and pushed before the tests it governs | `PROTOCOL.md`, `PROTOCOL.sha256` |
| 1 | Datasets: D1 = LexiRumah (70 lects, 152 concepts); D2 = ABVD with expert cognates (30 lects) | `data/` |
| 2 | Automatic cognates (LexStat, SCA), scored against the ABVD experts | `results/cognates/`, `results/scores/` |
| 3 | Loan screening: Indonesian, Portuguese, Tetun look-alikes, Austronesian–Papuan contact sets | `results/loans/` |
| 4 | Known-answer checks and gate | `results/known_answers.csv`, `results/gate.json` |
| 5 | Bootstrap support for 30 hypothesis clades (Hull, Edwards, Grimes and Edwards) | `results/hypotheses/` |
| 6 | Treelikeness (delta scores, Q-residuals) and a NeighborNet | `results/network/` |
| 7 | Bayesian constraint tests (MrBayes stepping-stone, Bayes factors) | `results/bayes/` |
| 8 | Pre-registered decision | `results/decision.json` |
| E1–E5 | Exploratory: borrowing-resistant vocabulary, *p and *ŋ reflexes (automatic and by hand), Tetun affinity, retentions, geography | `results/exploratory/` |
| E6 | Maximum-likelihood cross-check (IQ-TREE, AU test) | `results/ml/` |
| E7–E9 | Grimes and Edwards tables as data; expert and automatic reflex atlases | `derived/ge2026_tables/`, `derived/reflex_atlas/` |
| E10–E11 | Sound-change characters; total-evidence trees (IQ-TREE, MrBayes) | `derived/sound_change_matrix/`, `results/total_evidence/` |
| E12 | Loans identified by sound change; rerun without them | `derived/loans/`, `results/total_evidence/loan_rerun.json` |
| Lit. | Literature scan; E13 Hull's *b/*k characters; E14 independent ASJP Idaté list | `results/LITERATURE.md`, `results/literature/` |
| Lit. 2 | E15 cognate-coding robustness (after Kaiping and Klamer 2022); E16 Alcantara (2015) Idaté data | `results/literature/`, `derived/alcantara2015_idate/` |
| Lit. 3 | E17 shared lexical innovations; E18 triplet contact test; E19 contacTrees (uninformative) | `results/literature/`, `derived/innovations/` |
| Lit. 4 | E20 Idaté-vs-Lakalei split test; E21 borrowing simulation (ABC); E22 glottometry; E23 strict-clock dating; E24 other branches | `results/literature/` |
| Lit. 5 | Addendum 9, the limitations tested: E25 multiple testing; E26 dialect replication and E28 independent data (confirmatory); E27 consensus cognates and reviewer packet; E29 sound changes on rival trees; E30 classifier validation; E31 triplet null and power; E32 two-way ABC; E33 correspondence loan test; E34 rooted clock | `results/literature/`, `derived/innovations/` |
| Lit. 6 | Addendum 10: E35 words inherited from above the Timor groups (Austronesian Comparative Dictionary); E36 AU tests on the independent lists | `results/literature/` |

## Rerun

```
pip install lingpy==2.6.14 python-igraph pandas numpy scipy matplotlib biopython SplitsPy==0.0.10 scikit-learn
./src/01_fetch.sh                 # upstream data at pinned commits
cd src
python3 02_build_dataset.py       # step 1
python3 03_cognates.py            # step 2a (about 7 minutes)
python3 04_score.py               # step 2b
python3 05_loans.py               # step 3
python3 06_known_answers.py       # step 4 and the gate
python3 07_hypotheses.py          # step 5 (about an hour)
python3 08_network.py             # step 6
python3 09_bayes.py nexus         # step 7: needs MrBayes 3.2.7a on the PATH or in $MRBAYES
python3 09_bayes.py run unconstrained c1pos c1neg c2pos c2neg tbpos tbneg
python3 09_bayes.py summarize
python3 10_exploratory.py         # E1, E3, E3b
python3 11_sound_changes.py       # E2
python3 14_retentions.py          # E4
python3 15_post_hoc.py e2b        # E2b, hand-check table
python3 15_post_hoc.py e5         # E5, geography
python3 15_post_hoc.py e6         # E6: needs IQ-TREE 2 on the PATH or in $IQTREE
python3 16_posterior.py           # posterior clade probabilities
python3 17_gray2009.py            # novelty check against Gray et al. 2009 posterior trees
python3 18_ge_tables.py <path to a clone of github.com/langsci/526>   # E7
python3 19_reflex_atlas.py        # E8, E9
python3 20_total_evidence.py matrix   # E10
python3 21_innovations.py         # E10b
python3 20_total_evidence.py iqtree   # E11 (IQ-TREE)
python3 20_total_evidence.py mrbayes  # E11 (MrBayes, several hours)
python3 20_total_evidence.py supports
python3 20_total_evidence.py summary
python3 22_tetun_loans.py         # E12
python3 23_ct_loans.py            # E12b
python3 24_figures_expansion.py
python3 25_literature_checks.py e13      # Addendum 5
python3 25_literature_checks.py e13s     # sensitivity, not pre-declared
python3 25_literature_checks.py e14 <path to a clone of github.com/lexibank/asjp>
python3 26_coding_robustness.py cognates  # Addendum 6, E15
python3 26_coding_robustness.py trees
python3 26_coding_robustness.py fit       # diagnostic, not pre-declared
python3 27_alcantara.py parse <Alcantara 2015 thesis PDF>   # E16
python3 27_alcantara.py reflexes
python3 27_alcantara.py rerun
python3 28_innovations_contact.py         # Addendum 7, E17 and E18
python3 29_contactrees.py xml             # E19: needs BEAST 2.6.7 + contacTrees 1.1.0 on the classpath (see the script)
python3 30_more_tests.py all              # Addendum 8: E20, E22, E24
python3 31_borrowing_abc.py               # E21 (about 15 minutes)
python3 33_dating.py run && python3 33_dating.py summarize   # E23
python3 35_classifier.py                  # E30 (run before the reruns below)
RETENTION_RULE=chosen python3 28_innovations_contact.py && RETENTION_RULE=chosen python3 30_more_tests.py all   # E30 reruns (*_r2)
python3 34_addendum9.py all               # E25-E29 (E27-E29 need IQ-TREE)
python3 36_triplet_power.py               # E31
RETENTION_RULE=chosen python3 37_abc2.py  # E32 (about 15 minutes)
python3 38_correspondences.py             # E33
python3 33_dating.py run rooted && python3 33_dating.py summarize rooted   # E34
python3 39_addendum10.py all              # E35 (needs data/upstream/acd), E36 (IQ-TREE)
python3 12_decide.py              # step 8
python3 13_figures.py
```

The paper and website rebuild from the results with `bash paper/build.sh` (pandoc 3 and XeLaTeX) and `python3 paper/make_site.py`.

## Data and licences

- **LexiRumah 3.0.1** (Kaiping, Edwards and Klamer 2019), CC-BY 4.0. Its cognate judgments are all automatic.
- **ABVD** (Greenhill, Blust and Gray 2008), CC-BY 4.0. Source of the expert cognates and of the Proto-Malayo-Polynesian forms used in E2.
- **IDS** Portuguese list (Key and Comrie), CC-BY 4.0.
- **Glottolog 5.3**, CC-BY 4.0.
- **Gray, Drummond and Greenhill (2009)** posterior trees, via phlorest/gray_et_al2009, CC-BY 4.0 (novelty check only).
- **Concepticon**: the Leipzig-Jakarta list (Tadmor 2009), CC-BY 4.0.
- **ASJP v21** (Wichmann, Holman and Brown), via lexibank/asjp, CC-BY 4.0. Used only for the E14 Idaté check.
- **ACD**, the Austronesian Comparative Dictionary (Blust, Trussel and Smith), via lexibank/acd, CC-BY 4.0. Used only for E35.
- **Natural Earth** 10m land and country boundaries, public domain, clipped in `paper/data/` for the maps.
- **Fonts** in `paper/fonts/`: Alegreya and Gentium Book Plus, SIL Open Font License 1.1.
- **Grimes and Edwards (2026)**, CC-BY 4.0. Their subgroups and comparative tables were read from the book's LaTeX source (github.com/langsci/526); the tables are re-released as data in `derived/ge2026_tables/` under the same licence. Their full wordlists are not released, so they aren't used.

The code is MIT (`LICENSE`). The data keep their source licences; please cite the sources above.
