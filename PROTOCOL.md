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

(none yet)
