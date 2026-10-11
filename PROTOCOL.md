# Timor subgrouping study: pre-registered protocol (v1)

Dennis Crowley, Phaistos Labs. Analysis code written with Claude.
Frozen 2026-10-10. The SHA-256 hashes of this file and of `reference/*.csv` are in `PROTOCOL.sha256`, and the freeze commit comes before any analysis commit. Any change after the freeze goes in a dated addendum at the end of this file, and anything decided after seeing results is labelled post hoc.

## 1. Question

How should the Austronesian languages of Timor be subgrouped? Two classifications disagree.

- **Hull (1998, 2001).** A Timoric group with two branches. *Ramelaic* (Timoric B): Mambae, Kemak, Tokodede and Idalaka (Idaté plus Lakalei). *Fabronic* or *Extra-Ramelaic* (Timoric A): Tetun, Habun, Kawaimina, Galoli, Wetarese, Bekais and Dawan (Meto). Van Engelenhoven (2009) adds Makuva and the Luangic-Kisaric languages to Timoric A. Hull (1998) also treated Welaun as a Tetun dialect, which he withdrew in 2003.
- **Edwards (2021), as coded in Glottolog 5.3.** *Central Timor* (Mambae, Kemak, Tokodede, Welaun) is its own Malayo-Polynesian branch. Everything else belongs to *Timor-Babar*: Lakalei-Idate, Eastern Timor (Central Timoric A = Tetun and Habu; Kawaimina), Wetar-Atauro (Galoli, Dadu'a, Wetar), Helong, Rote-Meto and Southwest Maluku (with Babar).
- **Grimes and Edwards (2026)** set out nine Wallacean subgroups. The book is open access (CC-BY 4.0, Language Science Press) but could not be read from the analysis environment. Its Timor subgroups will be encoded by addendum **before step 5**. Its 292-variety wordlist is not released as a dataset (the deposited appendices cover single words such as 'banana' and are CC BY-NC), so it is not used as data here.

**Contrasts.**

- **C1, Idaté and Lakalei.** Hull puts them with Mambae, Kemak and Tokodede (Ramelaic). Edwards puts them in Timor-Babar, away from Central Timor. This is the main test.
- **C2, Welaun.** With Central Timor (Edwards) or inside Tetun (Hull 1998). This is a weaker contrast since Hull withdrew the claim.
- The internal Edwards groups (Eastern Timor, Central Timoric A, Kawaimina, Wetar-Atauro, Southwest Maluku, Timor-Babar) are tested one by one for lexical support.

**What a lexical test can and can't show.** Shared vocabulary mixes inheritance, shared retention and contact. Edwards's groups rest on exclusively shared sound changes; Hull's rest mainly on lexicon. A lexical tree that disagrees with an innovation-defined group shows that the vocabulary points elsewhere, and does not by itself refute the group. Results are reported in those terms.

Robinson and Holton (2012) is the precedent: computational methods on lexical data recovered subgroups in Alor-Pantar where the sound changes alone could not.

## 2. Data (step 1)

| Source | Version | Licence | Use |
|---|---|---|---|
| LexiRumah (Kaiping, Edwards and Klamer 2019) | 3.0.1, `lessersunda/lexirumah-data` commit `e10af03` | CC-BY 4.0 | D1, the main dataset |
| ABVD (Greenhill, Blust and Gray 2008) | `lexibank/abvd` commit `4a5795e` | CC-BY 4.0 | D2, expert cognates |
| Glottolog | 5.3 | CC-BY 4.0 | reference groups |
| IDS (Key and Comrie) | `lexibank/ids` commit `bf6c9f8`, Portuguese list | CC-BY 4.0 | Portuguese loan screen |

**LexiRumah has no expert cognate sets.** Its 95,201 cognate judgments are all automatic (`Source = biglexstat`), and its borrowings table is empty. Expert cognates therefore come from ABVD, which covers 12 of the Timor languages, plus Rote, Wetar, Southwest Maluku, Babar and Flores-Lembata.

**D1 (LexiRumah).** The 70 lects in `reference/d1_lects.csv`.

- 37 Austronesian lects on Timor: 11 Mambae, 8 Kemak, Tokodede, 2 Welaun, 2 Idaté, Lakalei, 2 Tetun, Habu, Waima'a, Midiki, Naueti, Galoli, Dadu'a, Helong (Funai) and 3 Meto.
- 6 Timor-Alor-Pantar (TAP) lects: 3 Bunak, Fataluku, Makasae and Oirata.
- Outgroups: 5 Rote, 5 Wetar, Kisar, Roma, Luang, Wetan, 10 Babar, and 3 Flores-Lembata (Sika Hewa, Lamaholot Lewoingu, Kedang) as the root.
- **Concepts.** Those with at least one form in at least 75% of the D1 lects. A lect left with fewer than 100 of these concepts after loan filtering is dropped and reported.

**D2 (ABVD).** ABVD languages within latitude −11.2 to −7.4 and longitude 122.5 to 130.5 that have at least 100 forms with expert cognate IDs, excluding proto-languages. All 210 ABVD concepts are used. A form without an expert cognate ID counts as missing for the expert distances.

**Before the freeze**, the lect lists, coordinates, coverage counts and cognate-source columns were inspected. No cognate detection, distances or trees were computed on these data.

## 3. Cognates (step 2)

- **Primary: LexStat** (LingPy 2.6.14), threshold 0.55, Infomap clustering, scorer with 1,000 runs, random seed 1234.
- **Secondary: SCA**, threshold 0.45, Infomap.
- **D1 also:** LexiRumah's own `biglexstat` sets, as a third automatic opinion.
- **D1 tokens:** LexiRumah `Segments`.
- **D2 tokens:** ABVD `Form`, cleaned and then tokenized with LingPy `ipa2tokens`.
  - Cleaning drops `- | = ( )` and spaces and turns `:` into `ː`.
  - A form is dropped if more than a third of its tokens get no sound class.
- **Scoring:** B-cubed precision, recall and F (Amigó et al. 2009; LingPy `bcubes`) of the automatic sets against the ABVD expert sets on D2. Only forms with an expert cognate ID are scored.

## 4. Loans (step 3)

| Rule | What it flags | Used how |
|---|---|---|
| L1 | ABVD forms marked `Loan = True` by the experts | removed in D2 |
| L2 | Automatic cognate sets that contain both Austronesian and TAP forms ("contact sets") | kept in the primary data; dropped in variant V-contact |
| L3 | Forms near-identical to the Indonesian word for the concept (Indonesian gloss in LexiRumah `concepts.csv`; ABVD language 362 for D2) | removed |
| L4 | Forms near-identical to the Portuguese word (IDS, matched by Concepticon ID) | removed |
| L5 | Forms in non-Tetun Timor lects near-identical to a Tetun form of the same concept | kept in the primary data; dropped in variant V-tetun |

- **"Near-identical"** means normalized edit distance ≤ 0.20 between SCA sound-class strings, for forms of 3 or more segments.
  - Indonesian and Portuguese spellings are converted to rough IPA first (ng → ŋ, ny → ɲ, c → tʃ, j → dʒ in Indonesian; ch → ʃ, lh → ʎ, nh → ɲ, qu → k, ç → s, j → ʒ in Portuguese).
- **Inheritance confound.** L3 and L5 can flag inherited words: Malay and Tetun are related to the Timor languages, so *mata* 'eye' matches everywhere. L3 removal hits all Austronesian lects alike, so it costs a little signal without favouring either hypothesis. L5 is a sensitivity variant only, for that reason.
- **Data variants.**
  - *Primary:* L1, L3 and L4 removed.
  - *V-all:* nothing removed.
  - *V-contact:* primary minus contact sets.
  - *V-tetun:* primary minus L5 forms.

## 5. Distances and trees

- **Distance** between lects *a* and *b* = 1 − (concepts where they share at least one cognate set) ÷ (concepts where both have a form). Pairs with fewer than 50 shared concepts are flagged.
- **Trees:** UPGMA (primary for the known-answer checks) and neighbour-joining.
- **Bootstrap:** 1,000 resamples of concepts, seed 1234.
- **Clade checks.**
  - UPGMA (rooted): a group is recovered if some node's leaf set equals the group exactly.
  - NJ (unrooted): a group is recovered if it is one side of a split.
  - For hypothesis clades, the lects in the `Prune` column are removed first.

## 6. Known-answer checks (step 4) and the gate

`reference/known_answers.csv` lists 21 checks.

- Tier 1: dialect groups of one Glottolog language, 9 in D1 and 3 in D2.
- Tier 2: established low-level groups and the TAP–Austronesian split, 6 in D1 and 3 in D2.
- None of them is part of the dispute.

**Gate.** The hypothesis tests (section 7) run only if all four conditions hold on the primary data with LexStat cognates and UPGMA:

- **G1.** At least 80% of the D1 checks are recovered.
- **G2.** At least 80% of the D2 checks are recovered.
- **G3.** Pooled B-cubed F ≥ 0.75 on D2. The threshold is our own choice, set before seeing any score.
- **G4.** Mantel correlation ≥ 0.70 (Pearson, 9,999 permutations, p < 0.01) between the D1 LexStat distances and the D2 expert distances over the matched lects in `reference/lect_map.csv`.

The same checks are also reported for expert cognates on D2 (the benchmark), for SCA and `biglexstat`, for NJ, and for every data variant. These extra runs are descriptive and do not enter the gate.

**If the gate fails**, no hypothesis test is run. An addendum names the fix, and the gate is rerun before anything else.

## 7. Hypothesis tests (steps 5 to 8, after the gate)

The clades are in `reference/hypotheses.csv`.

- **Step 5. Distance trees.** UPGMA and NJ on D1 (LexStat, SCA) and D2 (expert, LexStat), with bootstrap support for every hypothesis clade. A clade counts as **lexically supported** if bootstrap support is ≥ 70% under both UPGMA and NJ on D1 with LexStat, and it stays at ≥ 70% under V-contact and V-tetun.
- **Step 6. Treelikeness.** NeighborNet and delta scores (Holland et al. 2002) for the Timor Austronesian lects. If mean delta > 0.3, the tree results are reported as weak.
- **Step 7. Bayesian constraint test.**
  - Model: BEAST2 binary CTMC on cognate presence/absence with gamma rate variation, relaxed clock and Yule prior.
  - Two constrained runs: Hull (Ramelaic monophyletic) and Edwards (Central Timor monophyletic, Timor-Babar monophyletic).
  - Comparison: stepping-stone marginal likelihoods with 100 steps. ln BF ≥ 5 counts as strong (Kass and Raftery 1995).
  - Data: D1 primary, with LexStat cognates.
- **Step 8. Decision for C1.**
  - **Edwards** if EDW-CT and EDW-LI are lexically supported, HULL-R is not, and the Bayes factor favours Edwards strongly.
  - **Hull** if the reverse holds.
  - **Unresolved** otherwise, with the evidence on each side reported.
  - C2 is decided the same way with HULL98-W and EDW-CT.

## 8. Outputs

Everything goes in `results/`: cognate sets, loan flags, distance matrices, trees (Newick), check tables and a gate summary (`results/gate.json`). Code is MIT. Data keep their source licences (CC-BY 4.0) and are cited as above.

## References

- Amigó, E., J. Gonzalo, J. Artiles and F. Verdejo. 2009. A comparison of extrinsic clustering evaluation metrics based on formal constraints. *Information Retrieval* 12: 461–486.
- Edwards, Owen. 2021. Classification of the Austronesian languages of Timor (Central Timor and Timor-Babar), used here as coded in Glottolog 5.3 and as summarised in the Wikipedia article "Timoric languages". See also Edwards and Grimes (2021), Glottolog reference 660819.
- Greenhill, Simon J., Robert Blust and Russell D. Gray. 2008. The Austronesian Basic Vocabulary Database: from bioinformatics to lexomics. *Evolutionary Bioinformatics* 4: 271–283.
- Grimes, Charles E. and Owen Edwards. 2026. *The Austronesian languages of eastern Indonesia and Timor-Leste: Unravelling their prehistory and classification*. Berlin: Language Science Press. Appendices: doi:10.18710/3CT9RO.
- Hammarström, Harald, Robert Forkel, Martin Haspelmath and Sebastian Bank. 2026. Glottolog 5.3. Leipzig: Max Planck Institute for Evolutionary Anthropology.
- Holland, Barbara R., Katharina T. Huber, Andreas Dress and Vincent Moulton. 2002. δ plots: a tool for analyzing phylogenetic distance data. *Molecular Biology and Evolution* 19: 2051–2059.
- Hull, Geoffrey. 1998. The basic lexical affinities of Timor's Austronesian languages: a preliminary investigation. *Studies in Languages and Cultures of East Timor* 1.
- Hull, Geoffrey. 2001a, 2001b. Fabronic and Ramelaic membership as summarised in *Língua e Literatura* (Universidade de São Paulo), article 105477, p. 316.
- Kaiping, Gereon A., Owen Edwards and Marian Klamer (eds.). 2019. *LexiRumah 3.0.1*. Leiden University Centre for Linguistics.
- Kass, Robert E. and Adrian E. Raftery. 1995. Bayes factors. *Journal of the American Statistical Association* 90: 773–795.
- Key, Mary Ritchie and Bernard Comrie (eds.). *The Intercontinental Dictionary Series*.
- List, Johann-Mattis, Simon J. Greenhill and Russell D. Gray. 2017. The potential of automatic word comparison for historical linguistics. *PLOS ONE* 12: e0170046.
- Robinson, Laura C. and Gary Holton. 2012. Internal classification of the Alor-Pantar language family using computational methods applied to the lexicon. *Language Dynamics and Change* 2: 123–149.
- van Engelenhoven, Aone. 2009. Additions to Timoric A (Makuva, Luangic-Kisaric), as summarised in the Wikipedia article "Timoric languages".

## Addenda

The v1 text above is unchanged since the freeze; the only edit is this section, which replaced the line "(none yet)". To check, run `git show 35b913c:PROTOCOL.md | sha256sum` and compare with `PROTOCOL.sha256`. The `reference/*.csv` files are unchanged and still match it directly (`sha256sum -c` passes for them).

### Addendum 1 (2026-10-10, ADOPTED by the PI the same day; post hoc)

**Status.** The gate failed on G2 (see `results/REPORT.md`). Everything below was written after seeing the step 1–4 results, so it is **post hoc**. While diagnosing the TAP miss, the analyst also viewed the full D1 LexStat UPGMA tree, including the Timor lects. None of the changes uses that tree's Timor topology, but readers should know it was seen. The PI adopted A1.1 to A1.3 on 2026-10-10, so steps 5 to 8 run under the amended gate. Results under the v1 rules are kept in `results/gate_v1.json` and `results/known_answers_v1.csv`.

**A1.1 Make G2 relative to the expert benchmark.**

- *Reason.* Two of the six D2 checks (Luang + Wetan, Perai + Aputai) fail with the ABVD expert cognates too. They can't tell good cognate detection from bad.
- *Proposed rule.* G2 passes if LexStat recovers at least as many D2 checks as the expert cognates do under UPGMA.
- *Result if adopted.* 4 vs 4, so G2 passes and the gate passes.
- *Known weakness carried forward.* LexStat misses Atoni + Rote in D2 because the ABVD Atoni entries are inflected or compound. D2 results in step 5 would use the expert cognates as D2's primary set.

**A1.2 Keep every lect in the sensitivity variants.**

- *Reason.* V-tetun drops Idaté, Lakalei, Habu and Galoli below 100 concepts, and V-contact drops 28 lects. Neither variant can then test C1.
- *Proposed rule.*
  - The 100-concept minimum applies to the primary data only. Sensitivity variants keep every lect that passes on the primary data, and lects under 100 concepts in a variant are flagged rather than dropped.
  - V-contact removes only the TAP-side forms of a contact set. The direction of borrowing can't be read automatically, and removing the Austronesian forms too would wipe out shared inherited Austronesian vocabulary.

**A1.3 Encode Grimes and Edwards (2026).** Before step 5, add their Timor subgroups to `reference/hypotheses.csv` from the book (CC-BY 4.0, Zenodo record 18323007), with page references.

### Addendum 2 (2026-10-10, before any hypothesis clade was scored)

Written after the gate passed under Addendum 1 and before step 5 was run. As noted in Addendum 1, the analyst has seen the full D1 LexStat UPGMA tree, so steps 5 to 8 are not blind. The rules below are fixed before any hypothesis clade is scored or any Bayesian run is made.

**A2.1 Grimes and Edwards (2026) clades.** These are encoded in `reference/hypotheses_addendum2.csv`, 19 clades taken from the book's LaTeX source (github.com/langsci/526, CC-BY 4.0): sections 4.3, 4.4, 4.8, 4.8.1–4.8.3 and 5.5.

- Timor-Babar is defined by *p > h. Central Timor (Welaun, Kemak, Tokodede, Mambae) is defined by *ŋ > g and keeps *p.
- The book places Dadu'a in Atauro, not Wetar.
- It calls Wetar-Atauro "two overlapping subgroups", which is a linkage rather than a clade.
- It treats Eastern Timor as tentative, and allows that Eastern Timor and Lakalei-Idate may form a higher node.
- It does not discuss Hull.
- It reports that Welaun is lexically closer to Tetun (55–58%) than to Central Timor, which it explains as contact (citing Edwards 2019). **A lexical test is therefore expected to put Welaun with Tetun under either view, so C2 cannot be settled lexically.** C2 is reported, but it is not decided on lexical grounds alone.

**A2.2 Step 5 details.**

- Hypothesis clades from both files are checked on every configuration in step 4. Lects in `Prune` are removed first.
- The v1 rule applies: a clade is lexically supported if bootstrap support is ≥ 70% under both UPGMA and NJ on D1 LexStat primary, and also under V-contact and V-tetun.
- Robustness check, added here: the same tests with the six TAP lects removed (Austronesian-only trees). It is reported beside the main result and does not replace it.

**A2.3 Step 6 details.**

- Delta scores (Holland et al. 2002) and Q-residuals (Gray et al. 2010) on D1 LexStat primary distances: for all 37 Timor Austronesian lects, for all 64 Austronesian lects, and per lect.
- A NeighborNet (SplitsPy 0.0.10) on the 24 Bayesian taxa (A2.4), for display.

**A2.4 Step 7 details.**

- *Software.* MrBayes 3.2.7a replaces BEAST2. BEAST2 and its model-selection package could not be set up in this environment, and MrBayes has built-in stepping-stone sampling and positive/negative topology constraints.
- *Taxa.* 24 lects, one per language, chosen by highest coverage on the primary data: Mambae (Letefoho), Kemak (Kailaku), Tokodede, Welaun, Idaté (Cribas), Lakalei, Tetun (Suai), Habu, Waima'a, Midiki, Naueti, Galoli, Dadu'a, Helong (Funai), Meto (Kotos), Termanu, Dela, Ili'uun (Ilmaumau), Tugun, Kisar, Luang, Tela-Masbuar, and the roots Lamaholot (Lewoingu) and Sika (Hewa).
  - Southern Tetun is used rather than Tetun Dili because Tetun Dili is a creole with heavy Portuguese input.
- *Data and model.*
  - Data: binary cognate-set presence/absence from D1 LexStat primary, 1,353 characters.
  - Model: restriction data with coding=noabsencesites, gamma rates, exponential(10) branch lengths, unrooted, outgroup Lamaholot.
- *Contrasts.* Each is run with the clade forced (hard constraint) and forbidden (negative constraint):
  - C1: Ramelaic {Mambae, Kemak, Tokodede, Idaté, Lakalei}
  - C2: Central Timor {Mambae, Kemak, Tokodede, Welaun}
  - TB: Timor-Babar, meaning all non-Central-Timor, non-root taxa
- *Sampling.*
  - Stepping-stone: 5,000,000 generations, 50 steps, α = 0.4, 2 runs.
  - An unconstrained run (2,000,000 generations, 2 runs × 2 chains) gives posterior clade probabilities.
- *Reading the result.* ln BF = lnML(forced) − lnML(forbidden). |ln BF| ≥ 5 counts as strong.

**A2.5 Exploratory analyses.** These are labelled exploratory and do not enter the step 8 decision.

- **E1, stable vocabulary.**
  - The 60 D1 concepts on the Leipzig-Jakarta list (Tadmor 2009, via Concepticon) are the stable set; the other 92 concepts are the complement.
  - Step 5 clade support is recomputed on each set.
  - A grouping that holds on the stable set is less likely to be contact.
- **E2, sound-change diagnostics.**
  - For D1 concepts with an ABVD Proto-Malayo-Polynesian form (ABVD language 269), each lect's form is aligned to the PMP form (LingPy SCA, global alignment). The pair is kept if the SCA sound-class strings are within NED 0.5.
  - The reflexes of *p (not word-final) and *ŋ are then classed:
    - *p retained (p b f v ɸ β, with or without prenasalisation) vs lost or weakened (h ʔ ∅)
    - *ŋ > velar stop (g k) vs other
  - This replicates the defining changes of Timor-Babar and Central Timor (Grimes and Edwards 2026). It is not independent of their sources.
- **E3, Tetun affinity by stability.** For each Timor lect, the share of concepts where it shares a cognate with Tetun (either Tetun lect), on the stable set and on the complement. Contact should raise affinity more in the complement.

**A2.6 Step 8** applies the v1 decision rules to C1 and C2. Support for the Grimes and Edwards clades is reported alongside.

### Addendum 3 (2026-10-10, post hoc)

Written after the step 5 and 6 results and E1–E4 had been seen, and before any of the analyses below were run. Nothing here changes the step 8 decision rules.

**A3.1 Interrupted Bayesian runs.** The runs c1neg and c2neg stopped at step 10 of 50 when the session restarted. They are rerun from scratch with the same settings and seeds. The partial outputs are kept in `results/bayes/partial_killed/`.

**A3.2 E2b, the diagnostic words by hand.** Every Proto-Malayo-Polynesian etymon with *ŋ, or with *p not in final position, that E2 matched in Idaté, Lakalei or Welaun is printed with the forms in:

- Mambae (Letefoho), Kemak (Kailaku) and Tokodede
- Tetun Dili and Southern Tetun
- the lect itself

A form counts as *Tetun-shaped* if it is near-identical (L5 rule) to a Tetun form for the same concept. Tetun-shaped forms could be loans, so only forms that are not Tetun-shaped count as native evidence.

**A3.3 E5, geography.**

- *Model.* An ordinary least squares fit of D1 LexStat primary distance on the log of great-circle distance (from the LexiRumah coordinates), across all pairs of the 37 Timor Austronesian lects.
- *What is reported.* Mean residuals for Lakalei-Idate against each group.
- *Reading.* A tie that is no closer than proximity predicts fits contact as well as it fits descent.

**A3.4 E6, maximum-likelihood cross-check.** IQ-TREE 2.3.6 on the 24-taxon matrix of A2.4 (binary, GTR2+FO+G4).

- *Trees.*
  - An unconstrained search with 1,000 ultrafast bootstraps.
  - Constrained searches with each of these forced: Ramelaic, Central Timor with Welaun, Nuclear Central Timor plus Lakalei-Idate, Timor-Babar, and Lakalei-Idate with Eastern Timor.
- *Test.* An AU test (10,000 RELL replicates) across all the resulting trees. A tree with p < 0.05 is rejected.

**A3.5 Verdicts.** The step 8 outcomes are reported exactly as the rules give them. A separate section, labelled as the analyst's interpretation, weighs all the evidence: lexical, Bayesian, maximum-likelihood, sound change, contact and geography.

### Addendum 4 (2026-10-10, post hoc expansion)

Written after the step 1–8 results and the novelty check had been seen. Data extraction (E7) was run before this text was written. None of the analyses E8–E12 had been run. Nothing here changes the step 8 decision.

**Aim.** Widen the comparison until it yields new data, then use that data on C1.

**E7. Machine-readable Grimes and Edwards (2026) tables** (`src/18_ge_tables.py`, `derived/ge2026_tables/`).

- Every comparative table in the book's LaTeX source with a PMP row is parsed, 257 tables in all.
- Each form keeps the authors' bold-red highlighting of the reflex, and their grey marking of non-cognates.
- Table rows are mapped to Glottocodes through the book's Appendix A, plus an alias list for abbreviated labels.
- The book is CC-BY 4.0. This derived dataset carries the same licence and must be cited to Grimes and Edwards (2026).

**E8. Expert reflex atlas.** For each language and PMP target segment, the distribution of expert-highlighted reflexes in cognate forms, from E7.

**E9. Automatic reflex atlas.**

- E2 is extended to all PMP consonants, every LexiRumah concept and every D1 Austronesian lect, using the same alignment rule as E2.
- *Validation.* For each language that is in both atlases, check whether the automatic majority reflex equals the expert majority reflex, per target. Agreement is reported per target and per language.

**E10. Sound-change character matrix.**

- *Characters.* One multistate character per PMP target segment. The state is the language's majority reflex in E8, with reflexes grouped into classes: voiceless stop, voiced stop, fricative, h, glottal stop, ∅, nasal, liquid or rhotic, glide.
- *Coding rule.* A language is coded for a target only if E8 has at least 2 cognate tokens for it.
- *Taxa.* The 24 step-7 taxa, matched by Glottocode. When several E7 labels map to one Glottocode (Mambae varieties), all their tokens are pooled.

**E11. Phonology-only and total-evidence trees** for the 24 taxa.

- **(a) Phonology only.** IQ-TREE MK+G on E10, with 1,000 ultrafast bootstraps.
- **(b) Total evidence, maximum likelihood.** IQ-TREE with two partitions: the 1,353 lexical characters under GTR2+FO+G4, and E10 under MK+G.
- **(c) Total evidence, Bayesian.** MrBayes unconstrained, with a restriction partition (coding=noabsencesites, gamma) and a standard partition (Mk, gamma). The run length and sampling are as in A2.4.
- **Reading, stated before running.** Report the support or posterior probability for:
  - Lakalei-Idate + Central Timor (with Welaun);
  - Timor-Babar including Lakalei-Idate;
  - Lakalei-Idate + Eastern Timor.
  
  A support of 0.5 or more for one of them, and less for the others, counts as that grouping winning in that analysis. Anything else counts as unresolved.

**E12. Tetun loans identified by sound change.** This automates the criterion Grimes and Edwards use for Welaun.

- *Which forms.* LexiRumah forms in non-Tetun Timor lects that are Tetun look-alikes (L5).
- *Classes.* Each form gets one of three labels:
  - **probable loan**: one of its reflexes breaks the lect's own expert majority reflex (E8) and matches Tetun's;
  - **probably inherited**: it shows the lect's own regular reflex where Tetun differs;
  - **undecidable**: neither applies.
- *Rerun.* Step 5 and the E11(b) tree are repeated with the probable loans removed, as a sensitivity check.

**Amendments to Addendum 4, made after E8 and E9 had been run and before E10–E12.**

- **A4.1 Reflex classes.** The class list declared for E10 would have merged *ŋ > n with *ŋ retained, which is the very contrast that defines Timor-Babar. It would also have split *ŋ > g from *ŋ > k, which is a single change.
  - *New rule.* Classes now separate place of articulation and ignore voicing: labial stop, labial fricative, coronal stop, velar stop, affricate, sibilant, h, ʔ, ∅, m, n, ɲ, ŋ, l, rhotic, w, y.
  - *Applies to* E8, E9 and E10.
- **A4.2 Unhighlighted expert forms.** Grimes and Edwards sometimes list a language without highlighting it. They do this for comparison rows, such as Lakalei and Idaté in their table 04-16. So a cognate form with no highlight is not a zero reflex.
  - *New rule.* For such forms, the reflex is read off an SCA alignment of the form with the etymon and labelled `Source = aligned`. E9 is validated against highlighted tokens only.
- **A4.3 Positions.** E10 keeps one character per PMP target, pooling positions as declared. A sensitivity version with one character per target and position is also reported.
- **A4.4 E10b (post hoc).** This was added after the E11(a, b) results had been seen and before E10b was run.
  - *Why.* The A4.1 coding treats *p > h, *p > ʔ and *p > ∅ as unrelated states. Grimes and Edwards treat them as one lenition. So E10 cannot recover Timor-Babar, whose defining change it is.
  - *What E10b is.* Binary characters for the diagnostic changes Grimes and Edwards name, each taken from the expert atlas (majority class, at least 2 tokens):
    - *p lenited (h, ʔ, ∅);
    - *ŋ > velar stop;
    - *ŋ > n;
    - *j > rhotic;
    - *j > l;
    - *R > ∅;
    - *b > h or labial fricative;
    - *d > rhotic or l.
  - *Outputs.* E10b is reported as an innovation profile for every Timor-region language in the expert atlas, plus a phonology-only tree and a total-evidence ML tree for the 24 taxa.
- **A4.5 E12b (post hoc).** This was added after E12 had been run and before E12b was.
  - *Why.* E12 can only find Tetun loans. For C1 the relevant contact is loans from Central Timor into Lakalei-Idate.
  - *Which forms.* The Idaté and Lakalei forms in the cognate sets that Lakalei-Idate shares with Central Timor but not with Tetun (from E4).
  - *Test.* Each form's reflexes (E9) are checked against the Lakalei-Idate and Central Timor expert majorities (E8), at the targets where those two differ:
    - **probable Central Timor loan**: the form shows Central Timor's reflex;
    - **inherited or old**: it shows Lakalei-Idate's own reflex;
    - **undecidable**: no such target.
  - *Reading.* If the shared words carry Lakalei-Idate's own sound changes, they predate those changes, which argues against recent borrowing from Central Timor.

### Addendum 5 (2026-10-11, post hoc, prompted by a literature scan)

Written after the literature scan in `results/LITERATURE.md` and before E13 and E14 were run.

- **Why.**
  - **Hull's evidence for Ramelaic.** Hull's Ramelaic was said to rest on shared reflexes of *b and *k (Hull 2001, as summarised by Albuquerque 2009). Grimes and Edwards's own chapters record the same facts but treat them as separate developments:
    - *b > h in all positions is a defining change of Lakalei-Idate (their §4.4), and also of Kemak, Mambae, and Liquiçá and Bazartete Tokodede (their §5.4);
    - initial *k > ∅ is found in all Central Timor languages (their §5.4).
  - **A gap in E10b.** E10b coded *b as "h or labial fricative", pooled over positions. That merges Tetun's initial *b > f with *b > h, so E10b could not see the contrast.
  - **An independent wordlist.** ASJP (v21) has an Idaté list from a source independent of LexiRumah: Purwa et al. (1994), *Struktur bahasa Idate*.
- **Disclosure.** Before writing this addendum, the following had been seen:
  - pooled expert-atlas counts of *b, *k, *j and *ma-p reflexes per language (reproduced in `results/LITERATURE.md`);
  - Grimes and Edwards's text on *b and *k;
  - the 33 words of the ASJP Idaté list.

  No tree, support value or distance using the new characters or the ASJP lists had been computed.
- **E13: Hull's Ramelaic changes as characters.**
  - *New characters.* Three are added to the eight of E10b:
    - `b_h_initial`: word-initial *b > h or ∅;
    - `k_lost_initial`: word-initial *k > ∅ or ʔ;
    - `k_lost_medial`: word-medial *k > ʔ or ∅.
  - *Coding.* Each language takes the majority class of the expert atlas at that position (at least 2 tokens). Where the expert atlas has fewer than 2 tokens, the automatic atlas (E9, at least 2 tokens) is used, and that cell is flagged.
  - *Outputs.*
    - profiles for every Timor-region language and for the 24 taxa;
    - an ML tree on the 11 innovations;
    - an ML tree on the lexical characters plus the 11 innovations.

    Models and clades are as in E10b and E11.
  - *Reading.*
    - If Lakalei-Idate + Central Timor holds or rises and Timor-Babar stays at 0, the C1 lean is strengthened.
    - If Timor-Babar or Lakalei-Idate + Eastern Timor appears, it is weakened.
- **E14: independent ASJP check.**
  - *Lists.*
    - Idaté;
    - Central Timor: Mambae, Kemak, Tokodede (ASJP `TUKUDEDE`), Welaun;
    - Eastern Timor and Galoli: Tetun, Habu, Naueti, Waima'a, Galoli, Talur;
    - western Timor and Rote: Uab Meto, Amarasi, Termanu, Helong.

    Tetun Dili is left out because it is a lingua franca with a heavy Portuguese layer. Forms flagged as loans are dropped.
  - *Distance.* LDND (Wichmann et al. 2010) on the ASJP transcriptions, taking the minimum over synonyms.
  - *Outputs.*
    - Idaté's distances to every list, ranked;
    - the difference between its mean distance to Central Timor and its mean distance to Eastern Timor and Galoli, with a 1,000-replicate bootstrap over meanings;
    - an NJ tree with 1,000 bootstrap replicates over meanings, scored for Idaté + Central Timor, Idaté + Eastern Timor and Galoli, and Central Timor.
  - *Reading.*
    - Only the Idaté list is independent of the main datasets. The other lists come from ABVD, Hull (1998), Capell (1944), Edwards (2019) and others.
    - The lists are short: 18–48 words.
    - A clear result in either direction counts as independent evidence. An unclear one is reported as uninformative.

### Addendum 6 (2026-10-11, post hoc, prompted by Kaiping and Klamer 2022 and Alcantara 2015)

Written before E15 and E16 were run. No reflex, tree or support value from them had been computed.

**What had been seen.**

- Kaiping and Klamer (2022) in full.
- From Alcantara (2015), only the first ~60 pages were readable, which contain about 30 glossed Idaté forms in figure captions and Table 1. One of those forms had been noticed: Idaté *boʔur* against Tetun *bokur* 'fat', with medial *k > ʔ.

**E15: does C1 depend on how cognates are coded?** This follows Kaiping and Klamer's robustness design (their D2–D4).

- *Codings.* The 24-taxon lexical matrix (step 7 taxa, `primary` variant) is rebuilt from each of these, with everything else unchanged:
  - (a) LexStat with threshold 0.35, which splits more;
  - (b) LexStat with threshold 0.75, which lumps more (both with the same scorer settings as step 2);
  - (c) SCA with threshold 0.45 (the existing step 2 variant);
  - (d) LexiRumah's own published automatic cognates (`biglexstat`).
- *Not used.*
  - OnlinePMI, which isn't available in the pinned LingPy.
  - Kaiping and Klamer's loan rule, which codes a concept absent when a lect's only form is cognate with Tetun. That is right for Papuan languages, but here Tetun is a sister language, so the rule would delete inherited cognates.
- *Test.* IQ-TREE GTR2+FO+G4 with 1,000 UFBoot replicates, as in E6 and E11. Supports are read from `.splits.nex` for the six E11 clades.
- *Reading.*
  - If Lakalei-Idate + Central Timor stays the best-supported placement under every coding, and Timor-Babar and Lakalei-Idate + Eastern Timor stay near 0, the lexical side of C1 doesn't depend on the coding.
  - If any coding puts Lakalei-Idate elsewhere with at least 50% support, that is reported as a weakness.

**E16: Alcantara's Idaté data**, run only if the full thesis can be obtained.

- *Data.* Every glossed Idaté form in the thesis, mainly Appendix 2, transcribed as printed, with source page.
- *Concepts.* The Portuguese glosses are mapped to Concepticon by hand before any form is aligned. The mapping is saved separately.
- *Reflexes.* Each form is aligned with the ABVD PMP form for the same concept, following the E9 procedure exactly: the closest form with SCA NED ≤ 0.5, global alignment, A4.1 classes, positions.
- *Characters.* The 11 E13 characters are coded for Idaté from these tokens alone (majority class, at least 2 tokens), and compared with Idaté's current coding.
- *Rerun.* If any of Idaté's cells changes (filled from ?, or flipped), the vocabulary + 11 innovations ML tree (E13) is rerun with Alcantara's coding in those cells.
- *Reading.*
  - Cells moving towards the Eastern Timor pattern (*ŋ > n, *j > r, *b- not h, *k kept) weaken the C1 lean.
  - Cells moving towards the Central Timor pattern strengthen it.
  - Cells that don't change mean the earlier coding is confirmed by an independent source.

### Addendum 7 (2026-10-11, post hoc): separating inheritance from contact

Written before E17–E19 were run.

- **Already seen.** E4 (exclusive cognate links) and the E14/E15 hints of an Idaté–Habu link.
- **Not yet seen.** No retention/innovation classification and no triplet counts have been computed.

**Shared definitions (E17, E18).**

- *Cognates.* D1 LexStat (0.55) cognates, `primary` variant, Austronesian lects only.
- *Which concepts count.* Only concepts that have an ABVD Proto-Malayo-Polynesian form, matched through Concepticon.
- *Retention or innovation.* A cognate set counts as a **retention** if any of its forms is within SCA NED 0.5 of a PMP form for that concept (the E9 rule). Otherwise it counts as an **innovation**, meaning it replaced the PMP word.
- *Groups.*
  - LI: idat1237, idat1237-cribas, laka1255.
  - CT: all Mambae, Kemak, Tokodede and Welaun lects. NCT is CT without Welaun.
  - Separate groups: Tetun; Habu; Kawaimina (Waima'a, Midiki, Naueti); Galoli.
  - Everything else is "other".
- *Stable concepts.* The 60 Leipzig-Jakarta concepts used in E1.

**E17: shared lexical innovations.**

- *Exclusive innovations.* Each innovation set that contains an LI lect is classed by which other groups have it. Exclusive LI + CT sets are counted against exclusive LI + Tetun, LI + Habu, LI + Kawaimina and LI + Galoli sets. The exclusive sets are listed as an inventory.
- *Rates with geography controlled.* For every other Timor-region Austronesian lect, the rate is the share of commonly attested concepts on which it has the same innovation set as Idaté or Lakalei.
  - This rate is regressed on log distance.
  - Mean residuals are reported per group, for all concepts and for stable concepts.
- *Reading.*
  - More exclusive LI + CT innovations than exclusive LI + Tetun/Habu/Kawaimina ones, together with a positive Central Timor residual, supports the C1 lean.
  - The reverse weakens it.

**E18: triplet test for contact.** This is a site-pattern test, the lexical analogue of ABBA-BABA.

- *Lects.* The step-7 taxa: Lakalei-Idate (Idaté-Cribas, Lakalei); NCT (Mambae-Leten, Kemak-Kailaku, Tokodede); Welaun; Tetun-Suai; Habu; Kawaimina (Waima'a, Midiki, Naueti); Galoli.
- *Counting.* Take a triplet of groups (A, B, C). For each combination of one lect per group, and each concept attested in all three: if exactly two of the three share the same innovation set, count one for that pair.
- *Reading the counts.*
  - The pair with the largest total is the triplet's tree pair.
  - The other two counts should be equal if there was no contact. Their imbalance is D = (n_AC − n_BC) / (n_AC + n_BC).
  - The standard error comes from a delete-one-concept jackknife. |Z| ≥ 3 counts as significant.
- *Known-answer check, run first.* (Welaun, NCT, Tetun) should give the tree pair Welaun + NCT and a significant Welaun–Tetun excess. If it doesn't, E18 is reported as uninformative.
- *C1 tests.*
  - (LI, NCT, X) for X = Tetun, Habu, Kawaimina, Galoli.
  - (LI, Tetun, Habu).

  NCT is used so that Welaun's Tetun layer doesn't enter the CT side. Each test is run on all concepts, stable concepts and other concepts.
- *Reading for C1.*
  - LI + NCT as the tree pair on stable concepts, with any LI–X excess falling in non-stable concepts, supports Central Timor descent with contact from X.
  - LI + X as the tree pair on stable concepts supports Lakalei-Idate with X, with Central Timor contact.

**E19: a phylogeny with contact edges (contacTrees; Neureiter et al. 2022).**

- *Condition.* Run only if BEAST 2 and contacTrees can be compiled here from their GitHub sources, since Maven Central is unreachable.
- *Model.* The 24 step-7 taxa, with concept-partitioned binary characters as in the contacTrees examples.
- *What is reported.* Posterior support for contact edges between Lakalei-Idate and each other lineage, and the posterior of Lakalei-Idate + Central Timor.
- *Status.* Exploratory. If the chain doesn't converge (ESS < 100 on the posterior), that is reported and nothing is read from it.

### Addendum 8 (2026-10-11, post hoc): which half carries the signal, how much borrowing, glottometry, dating, other branches

Written before E20–E24 were run.

- **Already seen.** The E17/E18 results and the lect distances: Lakalei–Mambae about 10 km; Idaté–Mambae 38 km; Idaté–Habu 5–11 km.
- **Not yet seen.** None of the statistics below have been computed.

**E20: which member of Lakalei-Idate carries the Central Timor signal?**

- *Lists.* The primary comparison uses the two lists from the same source (`klamer02`): Idaté `idat1237` and Lakalei `laka1255`. A sensitivity check uses Idaté-Cribas (`dawson14`).
- *Which sets count.* Using E17's innovation sets, take the "CT-type" sets in Lakalei-Idate: present in Central Timor, absent from Tetun, Habu and Kawaimina. Count, over concepts attested in both lists, how many are in both Idaté and Lakalei, Lakalei only, and Idaté only. "Habu-type" and "Tetun-type" sets are counted the same way.
- *Test.* A two-sided binomial test of Lakalei-only against Idaté-only for each type.
- *Reading.*
  - Recent contact predicts Lakalei-only ≫ Idaté-only for CT-type sets (Lakalei sits next to Mambae), and Idaté-only ≫ Lakalei-only for Habu-type sets.
  - Inheritance, or contact older than the Idaté–Lakalei split, predicts that "both" dominates and that the two "only" counts are similar.

**E21: how much borrowing would each tree need?** This is approximate Bayesian computation.

- *Simulation.* Word replacement is simulated on the 24-taxon ML lexical tree (`lex_only.treefile`):
  - one character per concept, with the root holding the PMP retention;
  - per-concept rates from Gamma(1);
  - stable (Leipzig-Jakarta) concepts at a rate factor r_s;
  - the observed pattern of missing data.
- *Two models.*
  - **H**: the ML topology (Lakalei-Idate sister to Central Timor), plus borrowing into proto-Lakalei-Idate from Eastern Timor lects.
  - **G**: Lakalei-Idate regrafted as sister to Eastern Timor (Tetun, Habu, Kawaimina), as Grimes and Edwards allow, plus borrowing into proto-Lakalei-Idate from Nuclear Central Timor.
  - In both, a borrowed concept takes a random donor lect's class. The borrowing probabilities b_s (stable concepts) and b_o (other concepts) are free.
- *Priors.* Rate scale s ~ U(1, 12); r_s ~ U(0.2, 1); b_s, b_o ~ U(0, 0.6). Models equally likely.
- *Summary statistics.* The 18 E18 triplet counts: (LI, NCT, X) for X = Tetun, Habu, Kawaimina, on stable and other concepts.
- *Runs.* 20,000 simulations per model, keeping the closest 1% by standardised Euclidean distance.
- *Reported.* Model posterior probabilities, and the posterior of b_s and b_o under each model.
- *Reading.* If model G needs b_s above 0.2 (a fifth of core vocabulary borrowed from Central Timor), its placement is hard to defend lexically. If it fits with b_s ≤ 0.1, the lexical evidence doesn't discriminate.

**E22: historical glottometry** (Kalyan and François 2018).

- *Taxa.* The 22 Timor-region step-7 taxa (the Flores outgroup is left out).
- *Innovations.* E17 lexical innovation sets present in at least 2 taxa and absent from the Flores outgroup, plus the 11 E13 sound-change characters (taxa coded 1).
- *Statistics for a group G.*
  - ε = innovations whose taxon set is exactly G.
  - p = innovations that all of G's members have.
  - q = innovations that cross-cut G.
  - κ = p / (p + q); σ = ε × κ.
- *Missing data.* An innovation counts towards G only if every member of G has the concept attested, or the character coded.
- *Reported.* The 15 groups with the highest σ, and σ and κ for the named hypotheses.

**E23: relative dating.**

- *Run.* MrBayes, step-7 data and model, strict clock with a uniform clock tree prior, no calibrations. Two runs, 2,000,000 generations.
- *Reported.*
  - Posterior median relative heights (root = 1) of the most recent common ancestors of Lakalei-Idate, Nuclear Central Timor, Central Timor, Lakalei-Idate + Central Timor, Eastern Timor, Kawaimina, Rote-Meto and Wetar-Atauro.
  - Clade posteriors.
- *Status.* Descriptive.

**E24: other disputed branches.** The E18 triplet test (stable against other concepts, Welaun check as control) is applied to:

| Triplet | Rival groupings |
|---|---|
| (Habu, Tetun, Kawaimina) | Glottolog's Central Timoric A (Habu + Tetun) against Hull's Northern Fabronic (Habu + Kawaimina) |
| (Waima'a, Naueti, Midiki) | Grimes and Edwards's Waima'a-Naueti |
| (Galoli, Wetar, Dadu'a) | Galoli's place in Wetar-Atauro |
| (Galoli, Wetar, Tetun) | Galoli with Wetar, or with Tetun |
| (Helong, Meto, Rote) | Helong's neighbour Meto, or Rote |

- *Lists.* Wetar = Ili'uun and Tugun (ilma1240, kaha1239); Meto = Kotos Amarasi; Rote = Termanu and Dela; Helong = Funai.
- *Reading.* As for E18: the tree pair on stable concepts, and contact where an excess concentrates in other concepts.

### Addendum 9 (2026-10-11, post hoc): reducing the limitations

Written and pushed before any E25–E34 statistic was computed.

- **Name.** The project is renamed from Sanak to Liabut (Tetun *lia* 'word, speech' + *abut* 'root'). Earlier addenda are left as written.
- **Already seen.** Every result of E1–E24; the lect list, form counts and the source key of every D1 form (to plan E26 and E28); the LexiRumah `sources.bib` entries for those keys; that ABVD codes its Proto-Malayo-Polynesian forms (language 269) into expert cognate sets.
- **Not yet seen.** None of the statistics below.
- **Status.** E26 and E28 carry predictions stated here and are the confirmatory part of this addendum. Everything else is post hoc and reported as such.

**E25: multiple testing.** The family is every frequentist test reported for E18, E20 and E24: the jackknife D statistics (two-sided normal p from Z) for each triplet and stratum, and the E20 binomial tests (primary lists). The Welaun control is counted once. Holm–Bonferroni (α = 0.05) and Benjamini–Hochberg (q = 0.05) are applied across the family. Each new family below (E26, E28, E31, E33) is corrected within itself the same way. Any claim in the write-up that rests on a test that does not survive Holm is reworded.

**E26: replication across dialect representatives (confirmatory).** E18 used one representative per group. Here the triplet test is rerun for every combination of Mambae (11 lects), Kemak (8), Idaté (`idat1237`, `idat1237-cribas`) and Tetun (`tetu1245-suai`, `tetu1246`), with Tokodede, Lakalei, Habu and the Kawaimina lects fixed. The E18 combination is reported separately and left out of the counts. Primary coding and the E17 retention rule.

- *P1.* On stable concepts, Lakalei-Idate + Nuclear Central Timor is the largest pair against Tetun, against Habu and against Kawaimina, each in at least 80% of combinations.
- *P2.* Against Habu, on other (borrowable) concepts, Lakalei-Idate + Habu is at least as large as Lakalei-Idate + Nuclear Central Timor in at least 50% of combinations.
- *P3.* With the second Welaun lect (`west2547-mahein`) in the control triplet, the Welaun–Tetun excess has a larger Z on other concepts than on stable concepts, and Z ≥ 2 on other concepts, in at least 80% of combinations.

**E27: consensus cognates.** For the 24 step-7 taxa, a pair of forms counts as cognate under the consensus coding when the five E15 codings agree on average: forms are clustered within each concept by average linkage on the share of codings that put them in different sets, cut at 0.2 (on average, at least 4 of 5 codings agree). Then: (a) the E15 ML tree with UFBoot; (b) the E18 triplets. *Expectation, not a test:* Timor-Babar and Lakalei-Idate + Eastern Timor stay at or below 5% UFBoot. A reviewer packet is written: every cognate set that enters Lakalei-Idate's stable-concept triplet counts, with forms, PMP etymon, retention status and how many codings agree, for a specialist to check.

**E28: data independent of Grimes and Edwards (confirmatory).** (a) A provenance table: source key, collector and year for each step-7 taxon. (b) An independent taxon set: Edwards- or Grimes-collected lists are swapped for lists by other collectors where one exists (Kemak Kailaku → Kemak Atabai `kema1243`, Klamer 2002; South Mambae Letefoho, which has Grimes forms → Mambae Ainaro `mamb1306`, Klamer 2002) and dropped where none exists (Welaun, Helong, Amarasi). (c) The E15 ML tree (UFBoot) on that set, and the E18 triplets with Nuclear Central Timor = Mambae Ainaro, Kemak Atabai, Tokodede; Lakalei-Idate = Idaté `idat1237` and Lakalei, all from the single 2002 Klamer survey; Tetun = both Tetun lects.

- *P4.* On stable concepts, Lakalei-Idate + Nuclear Central Timor is the largest pair against Tetun, Habu and Kawaimina.
- *P5.* In the ML tree, Timor-Babar and Lakalei-Idate + Eastern Timor get at most 5% UFBoot.

**E29: do the sound changes fit Grimes and Edwards's tree better, and by how much?** The 11 E13 characters on the 24 taxa. Fitch parsimony length of the set, and of each character, on (H) the unconstrained ML lexical tree, (G) the E21 constrained tree (Lakalei-Idate + Eastern Timor) and (GE) an ML tree constrained to Grimes and Edwards's top split (Central Timor against the rest of the Timor-region taxa). Reported: lengths and the step difference H − G, beside the lexical likelihood difference (10.5). *E29b.* For Idaté and Lakalei, the number of tokens behind each coded cell (expert, automatic and Alcantara 2015) with a Wilson 95% interval for the majority reflex.

**E30: the retention classifier, validated and improved.** Validation set: the 30 D2 lects, where ABVD's expert judgements say whether each form is cognate with the PMP form (a retention). Each rule classifies the D2 LexStat sets as in E17 and is scored at the form level.

- *R0.* The E17 rule (some member within SCA NED 0.5 of a PMP form).
- *R1.* The same with the threshold chosen from 0.3, 0.4, …, 0.8.
- *R2.* Reflex-aware: before comparison, each PMP consonant is replaced by the lect's majority reflex (expert atlas; else automatic atlas; else unchanged), with the threshold chosen as in R1.
- *Choice.* Highest balanced accuracy. A rule must beat a simpler one (R0 < R1 < R2) by more than 0.01 to be chosen.
- *If the choice is not R0*, E17, E18, E20 and E22 are rerun with it and E32 uses it; both versions are reported.

**E31: the triplet test under unequal rates, and its power.** With the E21 simulator (no borrowing, ML lexical tree with its branch lengths; rate scale and stable factor drawn from E21's accepted model-H runs), 2,000 datasets give a null distribution of D for each E18 triplet and stratum. Reported: where the observed D falls in it (one-sided empirical p). Power: borrowing into proto-Lakalei-Idate from Habu at 0, 5, 10, 20 and 30% of other concepts (none in stable), 500 datasets each; the share of datasets with Z ≥ 2 for the Habu excess in other concepts, and in stable concepts. *Validation criteria:* false detections at 0% at most 10%; detection at 20% at least 50%. If they fail, the E18 contact readings are withdrawn.

**E32: a fuller borrowing model.** Both placements (H: ML topology; G: E21 constrained tree) get the same bidirectional borrowing: into proto-Lakalei-Idate from Nuclear Central Timor and from the Eastern Timor lects, each with its own stable and other probability (four parameters, each U(0, 0.6)); s ~ U(1, 12), r_s ~ U(0.2, 1). Retention rule as chosen in E30. Summary statistics (36): the 18 E18 counts; the six (Lakalei-Idate, Tetun, Habu) counts; and (Idaté, NCT, Habu) and (Lakalei, NCT, Habu) counts by stratum (12). 20,000 simulations per model.

- *Model choice.* ABC random forest (500 trees) with the posterior probability of the chosen model estimated by a regression forest on the out-of-bag misclassification indicator (Pudlo et al. 2016); rejection ABC (closest 1%) alongside.
- *Parameters.* Rejection ABC (closest 1%) within each model.
- *Posterior predictive checks.* 500 datasets per model from its accepted parameters; a two-sided p for each statistic; the number of statistics with p < 0.05.
- *Reading.* A placement is favoured only if its posterior probability is at least 0.9 and it fails no more posterior predictive checks than the other. G's placement stays "hard to defend lexically" if its median stable borrowing from Nuclear Central Timor exceeds 0.2.

**E33: regular correspondences as a loan test.** For the lect pairs (Lakalei, Mambae Letefoho), (Idaté-Cribas, Mambae Letefoho), (Idaté-Cribas, Habu), (Lakalei, Habu), (Lakalei, Tetun Suai) and (Idaté-Cribas, Tetun Suai), the two forms in every shared LexStat set are aligned (LingPy SCA, global). The identity share of a set is the share of aligned positions (gaps included) where the two segments are identical, ignoring length and stress marks. Recent loans should be closer to identical than the pair's inherited baseline (its shared retentions).

- *P6.* (Lakalei, Mambae): shared innovations on other concepts have a higher identity share than shared innovations on stable concepts (one-sided Mann–Whitney).
- *P7.* (Idaté-Cribas, Habu): shared innovations have a higher identity share than the pair's shared retentions (one-sided Mann–Whitney).
- *P8.* (Lakalei, Mambae) and (Idaté-Cribas, Mambae): shared innovations on stable concepts do not have a higher identity share than the pair's retentions.

**E34: a rooted clock.** E23 rerun with one change: a topology constraint making the 22 Timor-region taxa a clade, so the root falls between the Flores outgroup and Timor. Reported as in E23. Descriptive.

**Not addressable here, and why.** A specialist check of the cognates needs a specialist (E27's packet is for that). Grimes and Edwards's 494-item field lists are not public. Hull (1998) and Carvalho (2001) could not be obtained; Hull (1998) is in *Studies in Languages and Cultures of East Timor* 1: 97–202.

### Addendum 10 (2026-10-11, post hoc): an expert etymological check and topology tests on independent data

Written and pushed before E35 or E36 was computed.

- **Already seen.** All results through E34; the E6 AU test (Lakalei-Idate + Eastern Timor not rejected, p = 0.07); that the Austronesian Comparative Dictionary (ACD; Blust, Trussel and Smith, CLDF release `lexibank/acd`) lists reflexes for Tetun (523 forms), Galoli (53), Idaté (14), Waima'a (14), Mambai (12) and Kemak (10), and labels each etymon with its proto-language and gloss.
- **Not yet seen.** Any E35 or E36 statistic.

**E35: words inherited from above the Timor groups.** A shared innovation only counts for subgrouping if it is not inherited from a higher node. The E17 rule compares each cognate set with ABVD's PMP word for that meaning only.

- *Reference set.* ABVD's PMP form plus every ACD etymon reconstructed for PAN, PMP, PCEMP or PCMP whose gloss contains the concept's English gloss (its first word, as a whole word).
- *Rule.* The E30 rule (R2, reflex-aware, NED ≤ 0.4) against the enlarged reference set. A set that matches an ACD etymon is reclassified as inherited.
- *Reported.* How many sets move, and which; the E18 triplets (representative lists) and the E28 single-survey triplets rerun with the new statuses; the 24 reviewer-packet sets annotated with any matching ACD etymon.
- *Reading.* If Lakalei-Idate + Nuclear Central Timor stays the largest pair on stable concepts against Habu and Kawaimina in both reruns, the stable-pairing result stands; if it does not, that result is withdrawn.

**E36: topology tests on independent data.** IQ-TREE AU test (10,000 RELL replicates) on the E28 independent matrix, comparing the unconstrained tree with trees constrained to (a) Lakalei-Idate + Eastern Timor and (b) Timor-Babar (all Timor-region taxa outside Nuclear Central Timor). Reported: ΔlnL and p-AU. *Reading:* a constrained tree with p-AU < 0.05 is rejected by the vocabulary; otherwise the vocabulary prefers the unconstrained tree without excluding the alternative.

### Addendum 11 (2026-10-11, post hoc): Grimes and Edwards's own judgements, a parametric bootstrap, and a capped contact model

Written and pushed before E37–E39 were computed.

- **Already seen.** All results through E36; the column layout of `derived/ge2026_tables/forms.csv` and its table captions, one of which is "Lakalei-Idate lexically specific innovations" (its rows have not been looked at).
- **Not yet seen.** Any E37–E39 statistic.

**E37: the decisive sets against Grimes and Edwards's tables.** Sets checked: the 24 reviewer-packet sets and the E17 sets that Lakalei-Idate shares exclusively with one other group.

- *Matching.* A LexiRumah form matches a form in Grimes and Edwards's tables if the languages correspond (same Glottocode, or the E8 fallbacks), the table gloss contains the concept's English keyword as a whole word, and the SCA NED between the forms is at most 0.5.
- *Verdict per set.* "Inherited" if a member matches a form the authors mark as cognate with a reconstructed etymon (its `Cognate` flag true); "Lakalei-Idate innovation" if a member matches a row of their Lakalei-Idate innovations table; "not in the tables" otherwise.
- *Rerun.* E18 stable-concept triplets (representative and single-survey lists, E30 rule) with "inherited" sets reclassified as retentions.
- *Reading.* As E35: the stable-vocabulary pairing stands if Lakalei-Idate + Nuclear Central Timor stays the largest pair against Habu and Kawaimina in both reruns.

**E38: a parametric bootstrap of the eastern placement (SOWH test).** For the primary 24-taxon lexical matrix and the E28 independent matrix:

- *Null.* Binary characters simulated on the tree constrained to Lakalei-Idate + Eastern Timor, with the GTR2+FO+G4 parameters IQ-TREE estimates on it. Each simulated matrix copies the observed missing cells, and each character must contain at least one 1 among its observed cells (as real cognate sets do).
- *Statistic.* ΔlnL = lnL(unconstrained ML) − lnL(ML under the constraint), each by IQ-TREE with the same model.
- *Replicates.* 100 per matrix. p = (1 + number of simulated ΔlnL ≥ observed) / 101.
- *Reading.* p < 0.05 rejects the eastern placement for that matrix.

**E39: contacTrees with a cap of five contact edges.** E19 configuration A (no rate variation) with the upper bound on contact edges set to 5 and the expected number of contacts fixed at 1. One chain, as long as 4 hours allow (up to 2,000,000 steps), 10% burn-in.

- *Reported.* The number of contact edges sampled; Lakalei-Idate's sister in the base tree; the share of samples with a contact edge touching Lakalei-Idate; ESS of the posterior.
- *Reading.* If the ESS of the posterior is below 100, the run is uninformative, as E19 was.

### Addendum 12 (2026-10-11, post hoc): a second round after a mock referee report, with a decision rule stated in advance

Written and pushed before any E40–E50 statistic was computed. Prompted by a mock referee report (`paper/build/referee_report.md`) that asked for the root to be estimated, the sound changes to be re-scored with a fixed ancestral state, Lakalei-Idate to be kept together, the shared-innovation counts to be polarised and cleaned, and a short pre-registered second round with its own decision rule.

- **Already seen.** All results through E37; E38 for the primary matrix after 51 of 100 replicates (p about 0.02); E39 in progress, not summarised. From the referee report: that the Flores pair attaches to Rote-Meto + Helong (posterior 0.949); the referee's recomputed counts for \*p lenition under irreversible change with Flores coded \*p-retaining (6, 4 and 2 origins on H, G and GE); that in E34 the first split inside Timor puts Kisar-Luang-Tela-Masbuar on one side in 97.5% of samples; and the support values for West Rote-Meto, Southwest Maluku and Nuclear Central Timor in the pre-registered distance trees. For E40, the number of D1 concepts each candidate ABVD outgroup list covers (97 to 110 of 152); no tree, distance or cognate statistic with those lists.
- **Not yet seen.** Any statistic below.
- **Status.** Exploratory, except that the decision rule at the end is binding on how the paper reports C1.

**E40: the root, estimated with outgroups beyond Flores.**

- *Outgroups.* From ABVD, mapped to D1 concepts by Concepticon ID, ABVD loans dropped: far, Western Malayo-Polynesian: Tagalog (ABVD 277), Buginese (48), Uma (999); near, Central Malayo-Polynesian outside Timor and Flores-Lembata: Kambera (32), Bima (14), Manggarai (84); and Blust's Proto-Malayo-Polynesian (269) as a pseudo-taxon. Malay is left out because Indonesian look-alikes are screened from the Timor lists.
- *Coding.* LexStat on all D1 forms plus the outgroup forms, with the D1 settings (threshold 0.55, Infomap, 1,000 scorer runs, seed 1234). Timor and Flores forms keep the D1 primary screening; outgroup forms are not screened. Binary presence/absence matrices as in step 7.
- *Analyses.* (a) Primary: the 24 step-7 taxa plus all seven outgroups; MrBayes as in step 7 (2,000,000 generations, two runs) with Tagalog as the outgroup, and IQ-TREE (GTR2+FO+G4, 1,000 UFBoot). (b) Sensitivities, IQ-TREE only: the far set alone, the near set alone, PMP alone.
- *Reading of each tree.* The tree is reduced to the 24 step-7 taxa plus the root reference (Tagalog; Kambera for the near set; PMP for PMP alone) and rooted on it. Reported: the posterior or UFBoot of each root position among the 24 (Flores pair against the rest; Central Timor with or without Welaun against the rest; Lakalei-Idate + Central Timor against the rest; Rote-Meto + Helong, with or without Flores, against the rest; other), and of the rooted clades Lakalei-Idate + Central Timor (with or without Welaun), Timor-Babar including Lakalei-Idate (as step 7 defines it), Lakalei-Idate + Eastern Timor, and the 22 Timor-region taxa.

**E41: a relaxed clock.** The step-7 matrix, MrBayes with an independent-gamma-rates relaxed clock (`brlenspr=clock:uniform`, `clockvarpr=igr`), no topology constraint, 3,000,000 generations, two runs. Then again without Tela-Masbuar. Reported as E40, with the root read from the clock.

**E42: the sound changes with a fixed ancestral state and irreversible change.** The eleven E29 characters on the three E29 trees, rooted on the Flores pair, and also rooted where E40(a) puts the root if one position has posterior at least 0.5.

- *Coding.* The Flores pair is coded from the automatic and expert atlases where it has at least two tokens; \*p is coded retained in both (E2: 10 of 10 tokens).
- *Costs.* Fitch, as in E29; Camin-Sokal (each change may arise several times and never reverts; the root has the PMP state); Dollo (one origin, any number of losses). Reported per character and in total.
- *One standard.* For each character, the taxa outside its defining group that also show it (for example Sika for \*ŋ > n; Sika and Dela for \*d > r). The native-word \*p counts of E2 (Lakalei-Idate against Nuclear Central Timor, Fisher's exact test) are restated from the stored output.

**E43: how often the lexicon recovers subgroups that sound changes define.** Every Grimes and Edwards group in `reference/hypotheses.csv` with at least two taxa in the analysed set, other than the contested ones (Timor-Babar, Central Timor, Eastern Timor, Eastern Timor + Lakalei-Idate): its support in the pre-registered distance trees (stored), the step-7 MrBayes posterior and the lexical ML UFBoot, and (where it has taxa in it) E40(a). Reported: the share recovered at 0.95 / 95, by group size.

**E44: Lakalei-Idate kept together, and its members alone.** On the primary matrix and the E28 independent matrix, IQ-TREE (GTR2+FO+G4, 1,000 UFBoot): (a) with Lakalei-Idate constrained to be monophyletic; (b) with Lakalei removed (Idaté alone); (c) with Idaté removed (Lakalei alone). Reported: UFBoot of the focal taxon or pair with Central Timor (with or without Welaun), with Nuclear Central Timor, with Eastern Timor, with Habu, and its sister in the ML tree.

**E45: topology tests with the root held by the outgroups.** On the E40 matrices for the step-7 taxa and for the E28 independent taxa (each plus the seven outgroups), every candidate tree has Lakalei-Idate monophyletic. Candidates: the best tree under that constraint alone; Lakalei-Idate + Central Timor (with Welaun) as a rooted clade (all outgroups outside); Timor-Babar including Lakalei-Idate as a rooted clade (Central Timor, Flores and all outgroups outside); Lakalei-Idate + Eastern Timor. AU tests, 10,000 RELL replicates. Holm's correction is applied (i) within E45 and (ii) across every topology test in the project (E6, E36, E45).

**E46: shared innovations, polarised, cleaned and calibrated.**

- *Polarised.* On the E40 coding, a set counts as an innovation only if no outgroup taxon (Flores pair and the seven E40 outgroups) is in it, where any has the concept. As a sensitivity, the referee's version on the primary coding: the R2 innovations absent from Flores, Rote-Meto + Helong and Wetar.
- *Cleaned.* In the primary coding, the sets the referee names as retentions or errors (reviewer packet: '2sg', 'eat', 'water', 'leaf', 'hair', 'tail', 'good', 'laugh', 'stand', 'far', 'small'; E17: tail-1644, 'who', 'dry'; the two 'wife' sets merged) and every set E35 (strict) or E37 marks as inherited are removed.
- *Reported.* E18 triplets for (Lakalei-Idate, Nuclear Central Timor, X), X = Tetun, Habu, Kawaimina, by stratum, representative and single-survey lists; E17 exclusive counts on both sides after cleaning.
- *Calibration of the tree-pair rule.* The E31 simulator with no borrowing, 1,000 datasets on H and 1,000 on G (E21's constrained tree), each with parameters drawn from E21's accepted runs for that model. Reported: how often Lakalei-Idate + Nuclear Central Timor is the largest stable-concept pair against all three X at once, unpolarised and polarised on the Flores pair.

**E47: direct marginal likelihoods.** Stepping-stone runs with the c2pos settings for: Lakalei-Idate + Central Timor (with Welaun) forced; Lakalei-Idate + Eastern Timor forced; Welaun + Tetun forced. Reported: ln BF for Lakalei-Idate + Central Timor against Lakalei-Idate + Eastern Timor, and for Central Timor with Welaun (c2pos) against Welaun + Tetun.

**E48: without Tetun, and without Papuan-shared sets.** IQ-TREE (1,000 UFBoot) on the primary matrix (a) with Tetun removed; (b) with every cognate set that has a Papuan (TAP) member in D1 removed. Reported as E44(a), plus the number of sets each step-7 taxon shares with any Papuan lect.

**E49: node heights where the clade exists.** In E34 and E41 samples where both Nuclear Central Timor and Lakalei-Idate + Nuclear Central Timor are clades, the height of the second minus the first, absolute and relative to the first; the share of samples where both exist.

**E50: glottometry with intervals.** E22 (R2 rule) on 1,000 bootstrap resamples of concepts; 95% intervals for σ of Lakalei-Idate + Central Timor, Lakalei-Idate + Eastern Timor and Hull's Ramelaic.

**Housekeeping.** The E23 sister distribution and the E26 Tetun Dili breakdown, quoted earlier but never stored, are recomputed and stored.

**Decision rule for C1 in this round (binding on the write-up).**

- *Central Timor* is reported as lexically supported only if all four hold: (1) in E40(a) MrBayes, Lakalei-Idate + Central Timor (with or without Welaun) is a rooted clade with posterior at least 0.95, and it has UFBoot at least 95 in at least two of the three E40(b) sensitivities; (2) in E44(a) it has UFBoot at least 95 on both matrices; (3) in E45, the Lakalei-Idate + Eastern Timor and Timor-Babar trees are both rejected after Holm within E45 (p < 0.05); (4) in E46, polarised and cleaned, Lakalei-Idate + Nuclear Central Timor is the strictly largest stable-concept pair against Tetun, Habu and Kawaimina, and the calibration shows the tree-pair rule picking it under G in under 20% of datasets.
- *Grimes and Edwards* is reported as lexically supported if Timor-Babar including Lakalei-Idate is a rooted clade with posterior at least 0.95 in E40(a), or if E40(a) puts the root on the Central Timor stem with posterior at least 0.95 and Lakalei-Idate + Eastern Timor is not rejected in E45.
- *Otherwise* C1 is reported as unresolved by the vocabulary, with no lean, in the title, abstract and conclusion. What the vocabulary does show is reported as such (for example, that Lakalei-Idate + Eastern Timor is disfavoured).
- C2 gets no new decision; the write-up reports all C2 results, including those against Central Timor.
