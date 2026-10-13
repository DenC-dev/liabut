# Introduction

Two classifications of the Austronesian languages of Timor disagree about where Idaté and Lakalei belong. Hull (1998, 2001a) groups all of Timor's Austronesian languages as *Timoric*, split into *Ramelaic* (Mambae, Kemak, Tokodede and Idalaka, that is Idaté and Lakalei) and *Fabronic* (Tetun, Habun, the Kawaimina languages, Galoli, Wetarese, Dawan and Bekais or Welaun), and proposes that Ramelaic descends from Old Idalaka (as summarised by Albuquerque 2009). Carvalho (2001, cited in Fogaça 2015) proposed the same two-way split. Edwards (2019, 2021) and Grimes and Edwards (2026), building on Donohue and Grimes (2008), instead make *Central Timor* (Mambae, Kemak, Tokodede and Welaun) a separate branch of Malayo-Polynesian, defined by \*ŋ > \*g > k, and place every other Austronesian language of Timor, Idaté and Lakalei included, in *Timor-Babar*, defined by \*p > \*h.[^hull]

[^hull]: Grimes and Edwards (2026) do not discuss Hull's classification.

The disagreement comes down to two questions. **C1**: does Lakalei-Idate (Hull's Idalaka) share a common ancestor with Central Timor, as in Hull, or with the other Timor-Babar languages, as in Grimes and Edwards? **C2**: is Welaun a dialect of Tetun, as Hull (1998) first had it, or a Central Timor language (Edwards 2019)? Hull (2003) himself withdrew the Tetun-dialect claim, so C2 is the weaker contrast, and this paper concentrates on C1.

Grimes and Edwards argue from historical phonology, supported by morphosyntax and the lexicon. That sets two limits on what vocabulary can say. A subgroup defined by a shared sound change is not refuted by a lexical tree that fails to recover it, because shared vocabulary mixes inheritance, shared retention and borrowing (Blust 2000; Heggarty, Maguire and McMahon 2010). And if Central Timor is a primary branch, a tree with Lakalei-Idate beside Central Timor and a tree with Lakalei-Idate as the first branch of Timor-Babar can be the same unrooted tree, so C1 is partly a question about the root.

**What is new here, stated precisely.** Gray, Drummond and Greenhill (2009), the only earlier phylogeny covering Timor, includes Tetum, Mambai and Kemak but none of Idaté, Lakalei, Welaun, Habu, Midiki or Helong, which are absent from ABVD. Three kinds of novelty need separating:

- *Computational phylogenetic placement.* To our knowledge this paper gives these six languages their first cognate-based computational phylogenetic placement.
- *Systematic cognate analysis.* This is not new. LexiRumah codes cognates automatically for all of them (Kaiping, Edwards and Klamer 2019), and Grimes and Edwards (2026) compare them systematically by the comparative method, with reconstructions and regular correspondences.
- *Historical classification.* This is not new either. All six are classified by Hull (1998, 2001a) and by Grimes and Edwards (2026), and Welaun by Edwards (2019), who also gives lexical percentages for it.

**Design.** The study has a protocol frozen before any analysis, two replications with predictions declared in advance, a second round of analyses governed by a decision rule declared before it was run, and a larger body of exploratory work. Robinson and Holton (2012) used lexical phylogenetics where sound changes had left the subgrouping of Alor-Pantar unresolved; here the question is the reverse, whether the vocabulary can arbitrate between a classification built on sound changes and an older one. The paper distinguishes throughout between what the data show, what they suggest, and what remains unknown, and closes on each in turn. The exploratory analyses that do not bear directly on C1 are in the Supplement.

# Data

| Source | Contents | Use |
|-------------|------------------|----------|
| LexiRumah 3.0.1 (Kaiping, Edwards and Klamer 2019) | 70 Timor-region lects, 152 concepts | Main lexical data (D1) |
| ABVD (Greenhill, Blust and Gray 2008) | 30 lects with expert cognate judgements; Proto-Malayo-Polynesian (PMP) forms; Tagalog, Buginese, Uma, Kambera, Bima, Manggarai | Validation (D2); PMP etyma; outgroups for rooting |
| Grimes and Edwards (2026), LaTeX source | 257 comparative tables, 14,401 forms, reflexes marked by the authors | Sound-change atlas and characters |
| Austronesian Comparative Dictionary (Blust, Trussel and Smith) | Etyma from PAN to PCMP | Etymological check |

: Data sources. All are CC BY 4.0. The repository's `PROVENANCE.md` gives versions, commits and permissions, and `DATA_DICTIONARY.md` documents every lect, character, cognate assignment and exclusion code.

Each lect needed at least 100 of the 152 concepts. Forms that look like Indonesian or Portuguese loans are removed from the primary data; forms that look like Tetun loans, and Papuan-side forms resembling Austronesian ones, are removed only in sensitivity variants. The Idaté and Lakalei lists come from surveys by Klamer (2002) and Dawson (2014), not from Edwards or Grimes. Figure 1 shows the 24 lects used in the model-based analyses, one per language. Names follow LexiRumah, with Idaté for Idate, Habu for Habun, Tetun for Tetum and Welaun for Bekais.

![The 24 lects used in the Bayesian and maximum-likelihood analyses, one per language. Lakalei-Idate (red) lies between Central Timor (blue) and the Eastern Timor languages of Grimes and Edwards (dark grey); the dashed line is the border between Timor-Leste and Indonesia. Coordinates from LexiRumah; coastlines from Natural Earth.](figures/map.pdf){width=100%}

# Design: what each analysis can establish

The protocol was frozen and fingerprinted (SHA-256) on 10 October 2026, before any analysis. Fourteen dated addenda, each pushed to the public repository before the analyses it governs, extended it; each was written after the results of the previous ones had been seen. The analyses therefore fall into four classes that can establish different things (Table 2).

| Class | Analyses | What it can establish |
|-----------------|---------------------|-------------------------|
| Original pre-registered tests | Steps 1 to 8: distance trees with concept bootstraps; decision rule of 70% support in both UPGMA and NJ, on the primary data and two screened variants | Results evaluated under the initial protocol, subject to the deviations in Table 3 |
| Pre-declared replications | Addendum 9, predictions P1 to P5 (E26, E28) | Tests of predictions stated before those analyses were run |
| Second-round analyses | Addendum 12: E40 (root), E44 (Lakalei-Idate kept together), E45 (topology tests), E46 (cleaned, polarised innovations), under a decision rule declared in advance | Tests governed by an explicitly declared rule, written after earlier results had been seen |
| Exploratory analyses | Everything else, including the Bayes factors, the sound-change scoring, the contact models and Addenda 13 and 14 | Hypothesis-generating evidence and robustness checks, not independent confirmation |

: What each class of analysis can establish.

**Primary analysis.** Of the confirmatory components, the second round's rule bears most directly on C1, and it is treated as the primary analysis. It reports Central Timor as lexically supported only if four conditions all hold (Table 4), and Grimes and Edwards's placement only if Timor-Babar is a rooted clade or the root sits on the Central Timor stem. Six robustness checks accompany it: the independent word lists, each member of Lakalei-Idate alone, other cognate codings, removing Tetun or sets shared with Papuan languages, other outgroups and missing-data treatments for the root (E57), and other assumptions about the reversibility of sound change (E56). The remaining analyses, numbered E1 to E57 as in the repository, are in the Supplement.

| Protocol | What happened |
|------------------|-----------------------------|
| Gate: all four conditions under the v1 rules | G2 failed. Addendum 1 made G2 relative to the expert benchmark the same day, before any contested clade was scored |
| Steps 5 to 8 blind to the Timor topology | While diagnosing the gate, the analyst saw the full UPGMA tree, Timor lects included |
| Step 7: BEAST2, relaxed clock, Yule prior | Replaced by unrooted MrBayes (Addendum 2.4); a relaxed clock was run only in the second round |
| Step 7: Hull-constrained against Edwards-constrained runs, 100 stepping stones | Each clade forced against forbidden, 50 stones; direct comparisons added in the second round |
| Step 8: the decision uses bootstrap rules and a Bayes factor | The bootstrap conditions failed first, so the Bayes factor never decided anything |

: Deviations from the frozen protocol.

**Multiple testing.** Three families of tests were run. Eleven AU topology tests (E6, E36, E45) are corrected together by Holm's (1979) method; none rejects any placement (smallest adjusted p = 0.12). Forty triplet tests of contact (E18, E24) are corrected together; only Welaun's excess sharing with Tetun in borrowable words survives (E25). The remaining exploratory results are reported as estimates, not as tests, and the few uncorrected p-values in the Supplement are marked as such. None of the conclusions below rests on an uncorrected p-value.

# Methods

**Cognates.** LexStat (threshold 0.55) with Infomap clustering in LingPy 2.6.14 (List, Greenhill and Gray 2017). Scored against ABVD's expert judgements, it reaches a B-cubed F of 0.81 (precision 0.88, recall 0.75). Automatic cognates suffice for phylogenetic reconstruction in some families but not all (Rama et al. 2018), so four other codings are used as checks: SCA, LexStat at two other thresholds, a consensus of five codings (E27) and morpheme-level partial cognates (E51; List, Lopez and Bapteste 2016).

**Trees.** Each cognate set is one binary character; a lect without the concept is coded missing. The 24 lects give 1,353 characters. MrBayes 3.2.7a (Ronquist et al. 2012) used the restriction model with no all-absent sites, gamma rate variation and exponential(10) branch lengths; IQ-TREE 2.3.6 (Minh et al. 2020) used GTR2+FO+G4 with 1,000 ultrafast bootstrap replicates (UFBoot; Hoang et al. 2018), conventionally read as support only at 95 or above.

**Rooting.** A root needs outgroups that are certainly outside the ingroup, close enough to share cognates with it, and free of its contact history (Nixon and Carpenter 1993). No single choice meets all three, so three kinds were used, from ABVD, coded together with the Timor data (E40): three Western Malayo-Polynesian languages (Tagalog, Buginese, Uma), outside Central Malayo-Polynesian on every classification but distant; three Central Malayo-Polynesian languages of Sumba, Sumbawa and western Flores (Kambera, Bima, Manggarai), closer but in the same Lesser Sunda contact sphere; and Blust's PMP reconstruction (Blust 2013) as a pseudo-taxon. A reconstruction is a risky taxon. It is built partly from the languages being rooted and their relatives; it has no borrowings, no gaps of the usual kind and one etymon per meaning; and its forms lean towards conservative, well-documented languages, which can pull the root towards conservative lineages. The PMP-only rooting is therefore read as a check, never alone, and E57 reruns the root without it, without each other outgroup in turn, with missing data coded as absence, and on the 99 concepts attested in all seven outgroups. A relaxed clock (E41) gives a root without outgroups.

**Retentions and innovations.** A shared word is evidence for a subgroup only if it is a shared innovation; a shared retention says nothing. Each cognate set is classed as a PMP retention or an innovation by its distance from ABVD's PMP word after substituting each lect's regular reflexes (rule R2, balanced accuracy 0.79 against ABVD's experts; a learned classifier did not beat it, E54). The sets behind the decisive counts were then checked: by a mock review, against strict Austronesian Comparative Dictionary etyma (E35) and against Grimes and Edwards's own tables (E37). Sets also present in Flores, Rote-Meto or Wetar are set aside as probably old (polarisation). Every reclassification has a reason code in the repository's audit trail (`derived/audit/exclusions.csv`), and the 47 decisive sets are tabulated with their forms, etyma and audit entries for specialist review (`derived/audit/decisive_comparisons.csv`).

**Contact.** The triplet test counts, for three groups, the concepts on which exactly two share an innovation (the lexical counterpart of ABBA-BABA; Green et al. 2010; Durand et al. 2011), separately on the 60 Leipzig-Jakarta concepts (Tadmor 2009) and on the rest, with nulls simulated under unequal rates (E31) and a calibration of the decision rule (E46).

**Sound changes.** The marked reflexes in Grimes and Edwards's tables were turned into an expert reflex atlas; LexiRumah forms aligned to PMP gave an automatic atlas, agreeing on 94% of tokens. Eleven changes were coded as binary characters and scored on three rooted trees (the lexical tree H, Lakalei-Idate + Eastern Timor G, and Grimes and Edwards's top split GE) by Fitch (Fitch 1971), Camin-Sokal (Camin and Sokal 1965) and Dollo (Farris 1977) parsimony, and by Sankoff (1975) parsimony with the cost of restoring a lost sound varied from a tenth to a thousand times the cost of losing it (E56).

# Results

## Pre-registered tests and replications

Only low-level groups reach the 70% bar in both distance trees: Lakalei-Idate, Kawaimina, Wetar-Atauro, Nuclear Rote, Kisar-Luang and Babar. Hull's Ramelaic scores 22% (UPGMA) and 55% (NJ); Fabronic, Timor-Babar and Eastern Timor 0 to 3%. The pre-registered decision is **unresolved** for both C1 and C2. The rule relies on UPGMA, which assumes a clock and is misled by unequal rates (Blust 2000), so it had little chance of resolving higher-level groups. The replications partly failed. Across 351 combinations of dialect lists (E26), Lakalei-Idate + Nuclear Central Timor (Mambae, Kemak, Tokodede) was the largest stable-vocabulary pair against Habu and Kawaimina in every combination but against Tetun in only 47% (86% with Tetun Suai, 9% with Tetun Dili, the lingua franca). On lists collected independently of Grimes and Edwards (E28), the prediction failed against Tetun by one concept (45 to 44), while the prediction that Timor-Babar and Lakalei-Idate + Eastern Timor get at most 5% held (0%).

## The primary analysis

| Condition for reporting Central Timor (Addendum 12) | Result | Met? |
|-------------------------------------|-------------|----|
| 1. Root: Lakalei-Idate + Central Timor a rooted clade, MrBayes posterior ≥ 0.95, and UFBoot ≥ 95 in two of three outgroup sets | Posterior 1.00; UFBoot 98, 98 and 97 | Yes |
| 2. Lakalei-Idate kept together: UFBoot ≥ 95 with Central Timor on both list sets | 70 (primary), 98 (independent) | No |
| 3. Lakalei-Idate + Eastern Timor and Timor-Babar both rejected after Holm, root held by outgroups | Not rejected (adjusted p 0.06 and 0.11 for Timor-Babar; 0.52 and 0.28 for the eastern placement, within E45) | No |
| 4. Cleaned, polarised stable pairing largest against Tetun, Habu and Kawaimina, with the tree-pair rule producing it under G in under 20% | Fails against Habu (10 to 12) | No |

: The primary analysis: the second round's decision rule for C1. Grimes and Edwards's placement would have been reported as lexically supported if Timor-Babar were a rooted clade (posterior ≥ 0.95), or if the root sat on the Central Timor stem (≥ 0.95) and Lakalei-Idate + Eastern Timor were not rejected; neither happened (posterior 0.00 for both).

By the rule declared before the second round, **C1 is unresolved by the vocabulary**. Only the root condition holds. The next sections take each condition in turn and show why the evidence divides.

## The root

| Analysis | Root on Flores | Root on Rote-Meto + Helong | Root on Central Timor stem | Lakalei-Idate + Central Timor a rooted clade |
|----------------|-----|-----|-----|-----|
| All seven outgroups, MrBayes | 0.93 | 0.07 | 0.00 | 1.00 |
| All seven outgroups, UFBoot | 0.87 | 0.12 | 0.00 | 0.98 |
| Far outgroups only | 0.16 | 0.77 | 0.00 | 0.98 |
| Near outgroups only | 0.94 | 0.03 | 0.00 | 0.98 |
| PMP only | 0.04 | 0.70 | 0.00 | 0.97 |
| Relaxed clock, no outgroups | 0.11 | 0.42 | 0.00 | 0.96 |
| *E57: without Tagalog / Buginese / Uma* | *0.89 / 0.87 / 0.83* | *0.10 / 0.12 / 0.15* | *0.00* | *0.97 / 0.96 / 0.97* |
| *E57: without Kambera / Bima / Manggarai* | *0.81 / 0.92 / 0.46* | *0.17 / 0.07 / 0.51* | *0.00* | *0.95 / 0.97 / 0.98* |
| *E57: without PMP* | *0.96* | *0.03* | *0.00* | *0.97* |
| *E57: missing data coded as absence* | *0.36* | *0.60* | *0.00* | *0.86* |
| *E57: only the 99 concepts attested in all seven outgroups* | *0.83* | *0.13* | *0.00* | *0.96* |

: Where the root falls. Each tree is reduced to the 24 lects and rooted on Tagalog (Buginese without Tagalog; Kambera for the near set; PMP for PMP alone). Rows in italics are the E57 sensitivity runs, all UFBoot. In the relaxed clock the remaining 0.47 is spread over other branches, 0.17 of it on Kisar-Luang-Tela-Masbuar. Timor-Babar is a rooted clade in none (0.00 throughout).

In no analysis, and under no outgroup choice or missing-data treatment, does the root fall on the Central Timor stem (Table 5). It falls on the Flores or the Rote-Meto + Helong branch; which of the two depends on the outgroups and on how missing data are coded, but Central Timor and Lakalei-Idate stay on the same side. This rules out one reconciliation, that the lexical tree is Grimes and Edwards's tree rooted in a different place.

It does not establish an inherited subgroup. A rooted clade in a lexical tree means that the languages in it share more cognate presences and absences with each other than with the outgroups, in a pattern the model attributes to descent. It becomes evidence for a subgroup only if those shared features are innovations, inherited rather than borrowed, and not retentions concentrated in conservative lineages. The outgroups also attach by lexical similarity, so contact across the Savu Sea, or Rote-Meto's conservatism, could pull them west.

![Consensus tree (all compatible splits) of the Bayesian analysis with seven outgroups (grey), 31 lects and 1,599 cognate characters coded together (E40), rooted on Tagalog and drawn as a cladogram. Numbers are posterior probabilities; unlabelled nodes exceed 0.99.](figures/tree.pdf){width=80%}

## How robust is the placement?

| UFBoot % | With Central Timor | With Nuclear Central Timor | With Eastern Timor | With Habu |
|--------------------------|-----|-----|-----|-----|
| Primary lists, Lakalei-Idate kept together | 70 | 41 | 0 | 0 |
| Independent lists, kept together | 98 | 98 | 0 | 0 |
| Primary lists, Idaté alone | 52 | 3 | 2 | 38 |
| Primary lists, Lakalei alone | 84 | 75 | 0 | 0 |
| Without Tetun (E48) | 94 | 8 | 1 | 2 |
| Without 132 sets shared with Papuan lects (E48) | 46 | 51 | 0 | 0 |
| Consensus of five codings (E27) | 0 | 55 | 0 | |
| Partial cognates, kept together (E51) | 28 | 73 | 0 | 12 |
| LexiRumah's own cognates (E15) | 0 | | | 51 (Lakalei-Idate + Habu) |

: Robustness checks on the placement of Lakalei-Idate. On the independent lists Central Timor has no Welaun. Other codings are in the Supplement.

No coding, taxon set or list set puts Lakalei-Idate with Eastern Timor (0 to 7%). Support for the Central Timor side varies from 0% to 98% with choices that should not matter historically (Table 6; a check modelled on Kaiping and Klamer 2022): which cognate coding is used, whether the pair is forced together, which lists represent the languages. Lakalei on its own is Central Timor-like in every run; Idaté leans partly towards Habu, its neighbour 5 to 11 km away. Removing Tetun raises the Central Timor link, so Tetun loans are not what holds it together; removing the sets shared with Papuan languages lowers it, and Mambae, Kemak, Welaun, Idaté and Lakalei each share 40 to 49 sets with Papuan lects against 30 to 37 for Tokodede and the Eastern Timor languages, so some of the link may run through shared contact with Bunak.

## Topology tests and Bayes factors

| Constrained tree | Lists | Test | p | p, Holm over all eleven |
|-------------------------------|----------|------|-----|-----|
| Timor-Babar, rooted (E45) | Primary | AU | 0.011 | 0.12 |
| Lakalei-Idate + Eastern Timor (E45) | Primary | AU | 0.17 | 0.69 |
| Timor-Babar, rooted (E45) | Independent | AU | 0.022 | 0.22 |
| Lakalei-Idate + Eastern Timor (E45) | Independent | AU | 0.070 | 0.47 |
| Lakalei-Idate + Eastern Timor, Lakalei-Idate free to split (E38) | Primary | SOWH | 0.01 | |

: Topology tests. AU tests (Shimodaira 2002) use 10,000 RELL replicates, with the root held by the seven outgroups and Lakalei-Idate kept together; the parametric bootstrap (SOWH) uses 100 replicates. All eleven AU tests of the project are in the Supplement. The direct Bayesian comparison of the same two placements gives ln BF +11.8 for Lakalei-Idate + Central Timor (E47).

The Bayes factor and the corrected AU tests answer different questions, and the difference explains why one looks decisive and the other does not. The stepping-stone Bayes factor compares the average fit of two hypotheses over every tree and branch length consistent with each, assuming the model is correct. With 1,353 characters a small advantage per character accumulates into a large factor (+11.8), and because both hypotheses share the same model, which treats every shared word as inherited, the factor measures which placement that model prefers. The AU test asks whether the constrained tree fits significantly worse than the best tree, allowing for the variation one would see by resampling concepts and for having chosen the best of several candidates. Uncorrected it leans the same way (p = 0.011 to 0.17); after correction for eleven tests nothing is rejected. The two agree on the direction, towards Central Timor, and disagree on how far the preference survives sampling variation. The parametric bootstrap (SOWH; Goldman, Anderson and Rodrigo 2000) points the same way as the Bayes factor but is known to reject too readily when the model is misspecified (Susko 2014). The primary analysis required the corrected tests, so the direction is reported as a lean of the vocabulary under a no-borrowing model, not as a rejection of the eastern placement.

## Shared retentions and shared innovations

| Stable concepts, representative lists | LI + NCT | LI + X | NCT + X |
|-----------------------------|-----|-----|-----|
| X = Tetun: as first counted | 21 | 12 | 10 |
| X = Tetun: retentions and errors removed | 10 | 5 | 6 |
| X = Tetun: also without sets found in Flores, Rote-Meto or Wetar | 8 | 5 | 0 |
| X = Habu: as first counted | 23 | 19 | 15 |
| X = Habu: retentions and errors removed | 12 | 12 | 4 |
| X = Habu: also without sets found in Flores, Rote-Meto or Wetar | 10 | 12 | 0 |
| X = Kawaimina: as first counted | 80 | 38 | 23 |
| X = Kawaimina: retentions and errors removed | 42 | 27 | 13 |
| X = Kawaimina: also without sets found in Flores, Rote-Meto or Wetar | 36 | 21 | 1 |

: Triplet counts on stable concepts (E46): concepts on which exactly two of three groups share an innovation. LI is Lakalei-Idate; NCT is Nuclear Central Timor (Mambae, Kemak, Tokodede). Counts are summed over the combinations of lects in each group, so they exceed the number of concepts.

Shared vocabulary only supports a subgroup where it is a shared innovation. As first counted, Lakalei-Idate's stable vocabulary pairs it with Nuclear Central Timor against all three eastern groups (Table 8). Of the 66 "innovations" reclassified in review, most were retentions: sets that continue an etymon older than any of the groups compared, such as PMP \*(i)kahu '2sg' and \*ikuR 'tail', which the automatic rule had missed because the forms have changed a great deal. Three were coding errors (the two 'wife' sets continue one etymon, PAN \*b\<in\>ahi, which the coding split, and 'who' grouped non-cognate forms) and one was doubtful ('dry'). Once these are removed, the pairing with Central Timor still beats Tetun and Kawaimina, ties with Habu, and loses to Habu once sets also found outside the triplet are set aside. Coded by morpheme instead (E51), and not cleaned by hand, the polarised counts lean further towards Tetun (18 against 10) and Habu (14 against 13), although loose morpheme coding also picks up Tetun loans inside compounds.

Calibration matters for reading these counts. With no borrowing, the rule "Lakalei-Idate + Nuclear Central Timor strictly largest against all three groups" is satisfied in only 21% of datasets simulated on the lexical tree and 3% on the eastern tree (15% and 5% with polarised counts), so it rarely produces the pattern by accident but usually misses it when it is true (E46). And unequal branch lengths alone produce large imbalances between the minority pairs: a naive Z ≥ 2 rule fires in 27% of contact-free simulations (E31), so none of Lakalei-Idate's excess sharing in either direction is evidence of contact, and none is evidence against it.

Lakalei-Idate shares only a handful of innovations with exactly one other group (E17). After review two remain on the Central Timor side, 'cry' (*sɛro*, against *tanis* < \*taŋis almost everywhere else) and 'spit', against nine on the eastern side that passed the automatic and etymological checks but have not been reviewed by hand. The comparison is uneven until they are. A test of regular sound correspondences in these sets (E52) found too few regular non-identity correspondences in these short lists (0 to 2 sound classes per lect pair) to tell loans from inheritance.

## The sound changes

**The reflexes.** Table 9 gives every \*p token for the focal languages in the two atlases, by phonological environment (`derived/audit/p_reflexes.csv`). Mambae, Kemak and Tokodede keep a labial in every environment (p, or f in Mambae; one ʔ in Tokodede's \*kəpit 'narrow'). The eastern languages have h in every environment, with an occasional ʔ between vowels. Lakalei and Idaté have h word-initially (\*pitu > *hitu* 'seven') but also loss (\*pija > *ila* 'how much'), loss or h between vowels (\*əpat > *aːt* 'four', \*ma-nipis > *mihis* 'thin'), and w before \*u (\*hapuy > *wai* 'fire'). Welaun, a Central Timor language on every other count, has h, ʔ and loss. In \*palu 'hit' nearly every language has b (Tetun *baku*, Lakalei *baʔu*, Tokodede *bɔnu*, Waima'a *baː*), so that word is a separate development and counts for neither side.

| Language | Word-initial \*p | Between vowels | Before \*u |
|----------|----------|----------|----------|
| Mambae, Kemak, Tokodede | p, f (\*pija, \*puqun, \*pusəj) | p, f (\*əpat, \*nipən, \*nipay); ʔ once (\*kəpit) | p, f (\*hapuy) |
| Welaun | h (\*piliq) | ∅ (\*əpat), ʔ (\*ma-nipis) | ʔ (\*hapuy) |
| Lakalei | h (\*pitu), ∅ (\*pija) | ∅ (\*əpat, \*nipən), h (\*ma-nipis) | w (\*hapuy) |
| Idaté | h (\*pitu), ∅ (\*pija) | ∅ (\*əpat), h (\*ma-nipis) | w (\*hapuy) |
| Tetun | h (\*piliq) | h (\*əpat, \*nipən), ʔ (\*ma-nipis) | |
| Habu | h (\*pitu, \*pija) | h (\*əpat, \*hipi), ʔ (\*nipən) | h (\*hapuy) |
| Kawaimina | h (\*pitu, \*pija, \*punti, \*panaq) | h (\*əpat, \*ma-nipis) | |
| Flores pair | p | p | p |

: Reflexes of PMP \*p by environment, from the expert and automatic atlases (Welaun's 'fire' from its word list). Etyma in brackets.

**Four explanations.** The loss of \*p in Lakalei-Idate could have four sources, which predict different things (Table 10).

| Explanation | What it predicts | What the reflexes show | Assessment |
|-------------|-----------------|------------------|------------|
| Shared innovation: one change in an ancestor of Lakalei-Idate and the eastern languages | The same outcome in the same environments in every daughter, apart from later changes and loans | The eastern languages have h throughout; Lakalei-Idate has h, loss and w | Compatible if Lakalei-Idate later lost h or rounded it before \*u, both common changes; not uniquely predicted |
| Independent change in several lineages | Lenition in more than one branch, possibly with different outcomes | Welaun has h, ʔ and loss although it groups with Central Timor on every other count; p > h is among the most frequent lenitions (Kümmel 2007) | Plausible: it has happened at least twice on Timor |
| Restoration: Central Timor lenited \*p and later restored it | Regular p in Central Timor continuing an earlier h | Regular p or f in 54 of 55 matched words, native ones included | Implausible: h > p is essentially unattested as a regular change, and borrowing could not restore p so regularly |
| Diffusion across varieties already separate | Spread by contact, outcomes varying by language, shared by neighbours regardless of subgroup | Welaun, in long contact with Tetun, has h; Lakalei-Idate's outcomes differ from the eastern ones; it borders Mambae (p) and Habu (h) | Plausible; fits a Timorese Sprachbund (Hull 2001b; Schapper 2020); cannot be told apart from a shared innovation with these data |

: Competing explanations for the loss of \*p in Lakalei-Idate.

Restoration is the least plausible of the four, which is why irreversible scoring is the appropriate default (Campbell 2013). The data cannot separate a shared innovation from diffusion or parallel change, and Welaun shows that parallel change has happened.

**How much the scoring assumption matters.** Table 11 scores the trees with the cost of a restoration set from a tenth of the cost of a change to a thousand times it (E56). For \*p lenition the three trees tie when a restoration costs no more than a change. As soon as it costs twice as much, Grimes and Edwards's tree is cheapest, and at five times or more the lexical tree needs six origins against their two. Over all eleven characters, and over a fuller set of 36 characters from every reflex in the expert atlas (E53), the lexical tree is never the uniquely cheapest under any cost: Grimes and Edwards's tree wins when restorations are cheap, and the tree with Lakalei-Idate in Eastern Timor when they are costly, mainly because it groups Tetun with Habu and Kawaimina.

| Cost of a restoration, relative to a change | \*p lenition: H / G / GE | Eleven characters: H / G / GE | 36 characters: H / G / GE |
|-------------|-----------|-----------|-----------|
| 0.1 | 1.1 / 1.1 / 1.1 | 22.1 / 21.8 / **21.4** | 60.1 / 59.8 / **59.6** |
| 0.5 | 1.5 / 1.5 / 1.5 | 31.5 / 31.5 / **30.0** | 85.5 / 85.5 / **85.0** |
| 1 | 2 / 2 / 2 | 38 / 38 / **37** | 99 / **97** / 99 |
| 2 | 3 / 3 / **2** | **44** / 45 / **44** | 107 / **100** / 103 |
| 3 | 4 / 4 / **2** | 47 / 47 / 47 | 108 / **100** / 105 |
| 5 or more | 6 / 4 / **2** | 49 / **47** / 50–51 | 108 / **100** / 107 |

: Sankoff parsimony costs on the three trees, rooted on the Flores pair with the root state fixed at the PMP state (E56). H is the lexical tree, G Lakalei-Idate + Eastern Timor, GE Grimes and Edwards's top split. Bold marks the cheapest tree in each column; nothing is bold where all three tie.

![Eight diagnostic sound changes coded from the reflexes Grimes and Edwards (2026) mark in their comparative tables, for the languages of Timor, Wetar-Atauro and Rote-Meto (Southwest Maluku is in the repository). Outlined cells rest on fewer than two expert tokens. The last column merges \*b > h and \*b > f, so it is not the same character as Hull's initial \*b- > h.](figures/sounds.pdf){width=80%}

## Welaun (C2)

Welaun goes with Central Timor in the model-based trees (posterior 0.86), its similarity to Tetun sits in borrowable words (the one contact signal that survives correction, E25), and compared directly Central Timor with Welaun beats Welaun + Tetun by ln BF +7.6 (E47). The pre-registered distance trees favour Welaun + Tetun (51% and 59%) and the consensus coding gives Central Timor with Welaun 0%. Addendum 2.1 stated in advance that C2 cannot be settled lexically. Once borrowable vocabulary is set aside, the lexical evidence is consistent with Edwards (2019).

# Discussion

## Weighing the evidence

| Line of evidence | Hull: Lakalei-Idate with Central Timor | Grimes and Edwards: Lakalei-Idate in Timor-Babar | Class |
|--------------------|--------------------|--------------------|---------|
| Pre-registered distance trees | Ramelaic 22% and 55%, below the bar | Timor-Babar 0 to 3% | Pre-registered |
| Unrooted Bayesian tree | Lakalei-Idate + Central Timor 0.91 | Lakalei-Idate + Eastern Timor 0.00; compatible only with a root on the Central Timor stem | Exploratory |
| Root from outgroups and a relaxed clock | Rooted clade 0.86 to 1.00 | The root never falls on the Central Timor stem | Second round (met) |
| Lakalei-Idate kept together | 70% (primary), 98% (independent) | Not supported (0%) | Second round (not met) |
| Topology tests after correction | Not rejected | Not rejected | Second round (not met) |
| Direct Bayes factor, no-borrowing model | Favoured, ln BF +11.8 | Disfavoured under that model | Exploratory |
| Shared innovations, cleaned and polarised | Ahead of Tetun and Kawaimina | Habu ahead (12 against 10) | Second round (not met) |
| Exclusive shared innovations | Two after review | Up to nine, not yet reviewed | Exploratory |
| \*p lenition | Six origins if irreversible | Two origins if irreversible; tie if reversible | Exploratory |
| Fuller phonology, any reversibility | Never the cheapest tree | Cheapest when restorations are cheap | Exploratory |

: The two classifications against the main lines of evidence for C1.

The vocabulary and the phonology point in different directions, and Table 12 shows where the division lies. The lexical evidence leans towards Central Timor wherever it treats shared words as inherited, and weakens wherever retentions, coding choices and the internal split of Lakalei-Idate are taken into account. The sound-change evidence favours Grimes and Edwards wherever a lost \*p is assumed not to come back, and never favours the lexical tree.

**Why the comparative method's evidence counts differently.** The two kinds of evidence are not interchangeable, and counting characters would mislead. A regular sound change is a structured character: it applies across the lexicon, is directional (p > h is common, h > p essentially unknown), and can be polarised without outgroups. A lexical character is cheap and noisy: each of the 1,353 sets records presence or absence in one meaning, cannot tell inheritance from shared retention or borrowing on its own, and is correlated with its neighbours through contact and differences in rate. So 1,353 lexical characters against one defining change is not a fair measure of the evidence on each side. Sound changes also spread by contact, however (Schapper 2020), and a single change is one character: Welaun shows that this one has arisen more than once. The comparative method's evidence here is strong in kind but thin in amount, and the lexical evidence is plentiful but needs the comparative method's checks to become a claim about subgroups.

## What the data show

- Model-based lexical trees place Lakalei-Idate beside Central Timor and never with the Eastern Timor languages, and seven outgroups root the tree outside that pair under every outgroup set and missing-data treatment tried.
- That support is sensitive to coding and taxon selection (0 to 98%), Idaté on its own leans partly towards Habu, and no topology test rejects either placement after correction.
- Once identified retentions and errors are removed, Lakalei-Idate's shared stable innovations no longer favour Central Timor over Habu.
- \*p lenition fits Grimes and Edwards's tree better whenever a restoration costs at least twice a lenition; the sound changes never fit the lexical tree best.
- Lexical trees here also miss about half of the subgroups that sound changes define and nobody disputes (E43), so a missing lexical Timor-Babar says little about Timor-Babar.

## What the data suggest

The pattern fits a history shaped by contact or a linkage as well as by descent. Lakalei resembles Mambae, its neighbour 10 km away, and Idaté resembles Habu, 5 to 11 km away. A split network (E55) shows Lakalei-Idate with Central Timor in 47% of resampled networks and Idaté with Habu in 45%, and glottometry ties Lakalei-Idate about equally weakly to both sides. Such cross-cutting ties are what a dialect linkage leaves (Ross 1988; François 2014), and Grimes and Edwards already describe Wetar-Atauro as "overlapping subgroups". Shared contact with Papuan neighbours may carry part of the Central Timor link; East Nusantara is a linguistic area in its own right (Klamer, Reesink and van Staden 2008). Lakalei-Idate is also a conservative lineage with a short branch, the situation in which lexicostatistics misleads (Blust 2000) and retentions misread as innovations inflate the sharing between conservative lineages.

## What remains unknown

Whether either classification's subgroup is historically correct. A Timor-Babar subgroup and a Timor-Babar linkage differ in whether \*p lenition spread as one change before the daughters diverged or across varieties already separate, and the present data cannot tell them apart. Settling C1 needs evidence this study could not produce:

- an independent review, by historical linguists who know these languages, of the 47 decisive cognate comparisons on both sides, with reconstructed forms and the correspondences that support them (the table and instructions are in the repository's `SPECIALIST_REVIEW.md`);
- regular sound correspondences from fuller word lists, which the 152-concept lists cannot supply (E52); Grimes and Edwards's 494-item field lists for Idaté and Lakalei are not public, and a comparison with them should be made if they become available;
- Hull (1998), whose lexical percentages could be compared directly, and Alcantara's (2015) full Idaté corpus;
- an independent replication of the main analyses (`REPLICATION.md`; `reproduce.sh` rebuilds every estimate in the main text from the stored codings).

# Limitations

The confirmatory content is small: the pre-registered rule returned "unresolved", the replications failed against Tetun, and the second round's rule returned "unresolved" again. Everything else is exploratory and was planned after earlier results had been seen; follow-up analyses were often prompted by unfavourable results. The cognates are automatic and only partly checked; the checks in this paper reduce that dependence but do not remove it. LexiRumah is a single compilation, although its Idaté, Lakalei and replacement Central Timor lists come from collectors other than Edwards and Grimes. Some sound-change cells for Idaté and Lakalei rest on a handful of tokens. The simulated nulls use trees estimated from the same data, so contact that shaped those trees is built into the null. Hull (1998), Hull (2001b) and Carvalho (2001) could not be obtained; Hull's classification is cited from Hull (2001a, 2003) and secondary sources.

# Data and code {.unnumbered}

All data, code, results, the protocol and its addenda are at <https://github.com/DenC-dev/liabut>. `reproduce.sh principal` rebuilds every estimate in the main text from the stored codings and tree samples, and lists each with its source file in `results/principal_estimates.csv`; `reproduce.sh full` reruns the whole pipeline from pinned upstream data. `DATA_DICTIONARY.md` documents every lect, character, cognate assignment and exclusion code; `PROVENANCE.md` gives sources, versions and permissions; `derived/audit/` holds the exclusion trail, the decisive comparisons and the \*p reflex table. The Supplement reports the exploratory analyses not discussed here. Code is MIT-licensed; data keep their sources' licences.

# Use of AI {.unnumbered}

The code, the analyses and the drafting of this paper were carried out with substantial assistance from Claude (Anthropic), an AI system, under the author's direction. The mock referee report that prompted the second round was also written by Claude and is not an independent review. Every analysis, decision and correction is recorded in the public repository so that it can be checked.

# References {.unnumbered}

::: {.refs}
Albuquerque, Davi Borges de. 2009. Pré-história, história e contatos lingüísticos em Timor Leste. *Domínios de Lingu@gem* 3(2): 75–93.

Alcantara, Maressa Xavier. 2015. *Descrição fonética e fonológica da língua idaté do Timor Leste*. MA thesis, Universidade de São Paulo.

Blust, Robert, Stephen Trussel and Alexander D. Smith. *The Austronesian Comparative Dictionary*. CLDF release, lexibank/acd (commit 16085f2).

Blust, Robert. 2000. Why lexicostatistics doesn't work: the 'universal constant' hypothesis and the Austronesian languages. In Colin Renfrew, April McMahon and Larry Trask (eds.), *Time Depth in Historical Linguistics*, 311–331. Cambridge: McDonald Institute for Archaeological Research.

Blust, Robert. 2013. *The Austronesian Languages*. Revised edition. Canberra: Asia-Pacific Linguistics.

Camin, Joseph H. and Robert R. Sokal. 1965. A method for deducing branching sequences in phylogeny. *Evolution* 19(3): 311–326.

Campbell, Lyle. 2013. *Historical Linguistics: An Introduction*. 3rd edition. Edinburgh: Edinburgh University Press.

Dawson, Virginia. 2014. Manatuto survey word lists. PARADISEC collection VD1. In Kaiping, Edwards and Klamer (2019).

Donohue, Mark and Charles E. Grimes. 2008. Yet more on the position of the languages of eastern Indonesia and East Timor. *Oceanic Linguistics* 47(1): 114–158.

Durand, Eric Y., Nick Patterson, David Reich and Montgomery Slatkin. 2011. Testing for ancient admixture between closely related populations. *Molecular Biology and Evolution* 28(8): 2239–2252.

Edwards, Owen. 2019. Reintroducing Welaun. *Oceanic Linguistics* 58(1): 31–58.

Edwards, Owen. 2021. *Rote-Meto Comparative Dictionary*. Canberra: ANU Press.

Farris, James S. 1977. Phylogenetic analysis under Dollo's Law. *Systematic Zoology* 26(1): 77–88.

Fitch, Walter M. 1971. Toward defining the course of evolution: minimum change for a specific tree topology. *Systematic Zoology* 20(4): 406–416.

Fogaça, Jessé Silveira. 2015. *Aspectos gramaticais da língua Makasae de Timor-Leste*. PhD thesis, Universidade de Brasília.

François, Alexandre. 2014. Trees, waves and linkages: models of language diversification. In Claire Bowern and Bethwyn Evans (eds.), *The Routledge Handbook of Historical Linguistics*, 161–189. London: Routledge.

Goldman, Nick, Jon P. Anderson and Allen G. Rodrigo. 2000. Likelihood-based tests of topologies in phylogenetics. *Systematic Biology* 49(4): 652–670.

Gray, Russell D., Alexei J. Drummond and Simon J. Greenhill. 2009. Language phylogenies reveal expansion pulses and pauses in Pacific settlement. *Science* 323: 479–483.

Green, Richard E. et al. 2010. A draft sequence of the Neandertal genome. *Science* 328: 710–722.

Greenhill, Simon J., Robert Blust and Russell D. Gray. 2008. The Austronesian Basic Vocabulary Database. *Evolutionary Bioinformatics* 4: 271–283.

Grimes, Charles E. and Owen Edwards. 2026. *The Austronesian languages of eastern Indonesia and Timor-Leste: Unravelling their prehistory and classification*. Berlin: Language Science Press.

Heggarty, Paul, Warren Maguire and April McMahon. 2010. Splits or waves? Trees or webs? How divergence measures and network analysis can unravel language histories. *Philosophical Transactions of the Royal Society B* 365: 3829–3843.

Hoang, Diep Thi, Olga Chernomor, Arndt von Haeseler, Bui Quang Minh and Le Sy Vinh. 2018. UFBoot2: improving the ultrafast bootstrap approximation. *Molecular Biology and Evolution* 35(2): 518–522.

Holm, Sture. 1979. A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2): 65–70.

Hull, Geoffrey. 1998. The basic lexical affinities of Timor's Austronesian languages: a preliminary investigation. *Studies in Languages and Cultures of East Timor* 1: 97–202.

Hull, Geoffrey. 2001a. O mapa linguístico de Timor Leste: uma orientação dialectológica. *Studies in Languages and Cultures of East Timor* 4: 1–19.

Hull, Geoffrey. 2001b. A morphological overview of the Timoric Sprachbund. *Studies in Languages and Cultures of East Timor* 4.

Hull, Geoffrey. 2003. Lia-Bekais nia fatin iha dalen-lubun Timór. *Studies in Languages and Cultures of East Timor* 5: 55–78.

Kaiping, Gereon A. and Marian Klamer. 2022. The dialect chain of the Timor-Alor-Pantar language family: a new analysis using systematic Bayesian phylogenetics. *Language Dynamics and Change* 12(2): 274–326.

Kaiping, Gereon A., Owen Edwards and Marian Klamer, eds. 2019. *LexiRumah* 3.0. Leiden University Centre for Linguistics.

Klamer, Marian, Ger Reesink and Miriam van Staden. 2008. East Nusantara as a linguistic area. In Pieter Muysken (ed.), *From Linguistic Areas to Areal Linguistics*, 95–149. Amsterdam: John Benjamins.

Klamer, Marian. 2002. Timor-Leste survey word lists. In Kaiping, Edwards and Klamer (2019).

Kümmel, Martin Joachim. 2007. *Konsonantenwandel: Bausteine zu einer Typologie des Lautwandels und ihre Konsequenzen für die vergleichende Rekonstruktion*. Wiesbaden: Reichert.

List, Johann-Mattis, Philippe Lopez and Eric Bapteste. 2016. Using sequence similarity networks to identify partial cognates in multilingual wordlists. In *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, 599–605.

List, Johann-Mattis, Simon J. Greenhill and Russell D. Gray. 2017. The potential of automatic word comparison for historical linguistics. *PLOS ONE* 12(1): e0170046.

Minh, Bui Quang, Heiko A. Schmidt, Olga Chernomor, Dominik Schrempf, Michael D. Woodhams, Arndt von Haeseler and Robert Lanfear. 2020. IQ-TREE 2: new models and efficient methods for phylogenetic inference in the genomic era. *Molecular Biology and Evolution* 37(5): 1530–1534.

Nixon, Kevin C. and James M. Carpenter. 1993. On outgroups. *Cladistics* 9(4): 413–426.

Rama, Taraka, Johann-Mattis List, Johannes Wahle and Gerhard Jäger. 2018. Are automatic methods for cognate detection good enough for phylogenetic reconstruction in historical linguistics? *Proceedings of NAACL-HLT 2018*, 393–400.

Robinson, Laura C. and Gary Holton. 2012. Internal classification of the Alor-Pantar language family using computational methods applied to the lexicon. *Language Dynamics and Change* 2(2): 123–149.

Ronquist, Fredrik et al. 2012. MrBayes 3.2: efficient Bayesian phylogenetic inference and model choice across a large model space. *Systematic Biology* 61(3): 539–542.

Ross, Malcolm D. 1988. *Proto Oceanic and the Austronesian Languages of Western Melanesia*. Pacific Linguistics C-98. Canberra: Australian National University.

Sankoff, David. 1975. Minimal mutation trees of sequences. *SIAM Journal on Applied Mathematics* 28(1): 35–42.

Schapper, Antoinette. 2020. The origins of isolating word structure in eastern Timor. In David Gil and Antoinette Schapper (eds.), *Austronesian Undressed: How and Why Languages Become Isolating*, 391–446. Amsterdam: John Benjamins.

Shimodaira, Hidetoshi. 2002. An approximately unbiased test of phylogenetic tree selection. *Systematic Biology* 51(3): 492–508.

Susko, Edward. 2014. Tests for two trees using likelihood methods. *Molecular Biology and Evolution* 31(4): 1029–1039.

Tadmor, Uri. 2009. Loanwords in the world's languages: findings and results. In Martin Haspelmath and Uri Tadmor (eds.), *Loanwords in the World's Languages: A Comparative Handbook*, 55–75. Berlin: De Gruyter Mouton.
:::
