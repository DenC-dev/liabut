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
