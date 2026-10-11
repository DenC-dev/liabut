# Sanak

**A pre-registered computational test of how the Austronesian languages of Timor branch.**

*Sanak* means 'branch' in Tetun and 'kin' in Malay (*sanak saudara*, 'relatives'). The project asks how Timor's languages branch from one another, and which of them are closest kin.

Dennis Crowley, Phaistos Labs.

## The question

Two classifications disagree.

- **Hull (1998, 2001)** puts all of Timor's Austronesian languages in one *Timoric* group, split into *Ramelaic* (Mambae, Kemak, Tokodede, Idaté, Lakalei) and *Fabronic* (Tetun, Habun, Kawaimina, Galoli, Wetarese, Meto).
- **Edwards (2021)** and **Grimes and Edwards (2026)** make *Central Timor* (Mambae, Kemak, Tokodede, Welaun) a separate branch of Malayo-Polynesian. Everything else, including Idaté and Lakalei, belongs to *Timor-Babar*, defined by the sound change *p > h.

The sharpest point of disagreement is where Idaté and Lakalei belong (contrast C1). A second is whether Welaun is a Tetun dialect or a Central Timor language (C2).

The method follows Robinson and Holton (2012), who used lexical data to find subgroups in Alor-Pantar that sound changes alone couldn't settle.

## Results in brief

- **Hull's Fabronic (Timoric A) is not a lexical group.** It gets 0% support in every analysis.
- **Timor-Babar and Eastern Timor are not lexical groups either.** They get 0–3% bootstrap support, and the Bayes factor runs against Timor-Babar (ln BF −7.0). They rest on sound changes.
- **Welaun is Central Timor (C2).** The Bayes factor is +10.3, and its Tetun look disappears on borrowing-resistant vocabulary.
- **Idaté-Lakalei (C1) leans Central Timor.**
  - Its vocabulary sits with Central Timor (ln BF +8.0 for Hull's Ramelaic).
  - Its sound changes look like Timor-Babar (*p > h, *ŋ > n, no *ŋ > g). But Welaun, a Central Timor language, also has *p > h, and *ŋ > n is found in the Flores outgroup too.
  - Combining vocabulary with sound changes coded from Grimes and Edwards's own tables puts Lakalei-Idate with Central Timor every time (posterior 0.88, ML 56–80%). Timor-Babar gets 0.
  - This reading is post hoc and the sound-change data are thin, so it is a lean, not a settlement.
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

## What's new

This was checked against the published literature on 10 October 2026. See *Novelty check* in the report.

- **First computational placement of Idaté, Lakalei, Welaun, Habu, Midiki and Helong.**
  - None of them is in ABVD, so none appears in the Bayesian Austronesian tree of Gray et al. (2009).
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
| 0 | Protocol frozen before any analysis; four addenda, each dated and pushed before the tests it governs | `PROTOCOL.md`, `PROTOCOL.sha256` |
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

## Rerun

```
pip install lingpy==2.6.14 python-igraph pandas numpy scipy matplotlib biopython SplitsPy==0.0.10
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
python3 12_decide.py              # step 8
python3 13_figures.py
```

## Data and licences

- **LexiRumah 3.0.1** (Kaiping, Edwards and Klamer 2019), CC-BY 4.0. Its cognate judgments are all automatic.
- **ABVD** (Greenhill, Blust and Gray 2008), CC-BY 4.0. Source of the expert cognates and of the Proto-Malayo-Polynesian forms used in E2.
- **IDS** Portuguese list (Key and Comrie), CC-BY 4.0.
- **Glottolog 5.3**, CC-BY 4.0.
- **Gray, Drummond and Greenhill (2009)** posterior trees, via phlorest/gray_et_al2009, CC-BY 4.0 (novelty check only).
- **Concepticon**: the Leipzig-Jakarta list (Tadmor 2009), CC-BY 4.0.
- **Grimes and Edwards (2026)**, CC-BY 4.0. Their subgroups and comparative tables were read from the book's LaTeX source (github.com/langsci/526); the tables are re-released as data in `derived/ge2026_tables/` under the same licence. Their full wordlists are not released, so they aren't used.

The code is MIT (`LICENSE`). The data keep their source licences; please cite the sources above.
