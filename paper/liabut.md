# Introduction

Two classifications of the Austronesian languages of Timor disagree. Hull (1998, 2001a) groups them all as *Timoric*, split into *Ramelaic* (Mambae, Kemak, Tokodede and Idalaka, that is Idaté and Lakalei) and *Fabronic* (Tetun, Habun, the Kawaimina languages, Galoli, Wetarese, Dawan and Bekais or Welaun). He proposed that Ramelaic descends from Old Idalaka (as summarised by Albuquerque 2009). Carvalho (2001, cited in Fogaça 2015) proposed the same two-way split. Edwards (2019, 2021) and Grimes and Edwards (2026) instead make *Central Timor* (Mambae, Kemak, Tokodede and Welaun) a separate branch of Malayo-Polynesian, defined by \*ŋ > \*g > k, and place every other Austronesian language of Timor, Idaté and Lakalei included, in *Timor-Babar*, defined by \*p > \*h. Building on Donohue and Grimes (2008), they treat Central Timor and Timor-Babar as separate Malayo-Polynesian branches rather than as daughters of one Timor node.[^hull]

[^hull]: Grimes and Edwards (2026) do not discuss Hull's classification.

The two disagree most sharply on two points. **C1**: does Lakalei-Idate belong with Central Timor, as in Hull, or with Timor-Babar, as in Edwards and Grimes and Edwards? **C2**: is Welaun a dialect of Tetun, as Hull (1998) first had it, or a Central Timor language (Edwards 2019)? Hull (2003) himself withdrew the Tetun-dialect claim, calling Bekais a distinct language "structurally intermediate between Belunese Tetum and Dawan", so C2 is a weaker contrast than C1.

Grimes and Edwards argue from historical phonology, supported by morphosyntax and the lexicon. Two limits on what vocabulary can say follow from that. First, a subgroup defined by shared sound changes is not refuted by a lexical tree that fails to recover it, because shared vocabulary mixes inheritance, shared retention and borrowing (Blust 2000; Heggarty, Maguire and McMahon 2010). Second, in Grimes and Edwards's terms C1 is partly a question about the root: if Central Timor is a primary branch, a tree with Lakalei-Idate beside Central Timor and a tree with Lakalei-Idate as the first branch of Timor-Babar can be the same unrooted tree.

The only earlier phylogeny covering Timor, Gray, Drummond and Greenhill (2009), includes Tetum, Mambai and Kemak but none of Idaté, Lakalei, Welaun, Habu, Midiki or Helong. This paper asks what basic vocabulary says about C1 and C2, in the spirit of Robinson and Holton (2012), who used lexical phylogenetics where sound changes had left the subgrouping of Alor-Pantar unresolved. It has a pre-registered core, a set of exploratory analyses, and a second round of analyses with its own decision rule, declared after a mock referee report and before it was run.

# Data

| Source | Contents | Use |
|-------------|------------------|----------|
| LexiRumah 3.0.1 (Kaiping, Edwards and Klamer 2019) | 70 Timor-region lects, 152 concepts | Main lexical data (D1) |
| ABVD (Greenhill, Blust and Gray 2008) | 30 lects with expert cognate judgements; Proto-Malayo-Polynesian (PMP) forms; Tagalog, Buginese, Uma, Kambera, Bima, Manggarai | Validation (D2); PMP etyma; outgroups for rooting |
| Grimes and Edwards (2026), LaTeX source | 257 comparative tables, 14,401 forms, reflexes marked by the authors | Sound-change atlas and characters |
| Austronesian Comparative Dictionary (Blust, Trussel and Smith) | Etyma from PAN to PCMP | Etymological check |
| ASJP v21 (Wichmann, Holman and Brown) | 40-item lists, including Idaté from Purwa et al. (1994) | Independent check (uninformative; Idaté nearest Habu) |
| Alcantara (2015) | 184 Idaté forms from fieldwork in Laclubar | Token counts for sound changes |
| Gray et al. (2009) via phlorest | 998 posterior trees | Comparison |

: Data sources.

Each lect needed at least 100 of the 152 concepts. Forms that look like Indonesian or Portuguese loans are removed from the primary data. Forms that look like Tetun loans, and the Papuan-side forms of sets shared with neighbouring Papuan languages, are removed only in sensitivity variants. Idaté, Lakalei, Welaun, Habu, Midiki and Helong are absent from ABVD; to our knowledge this is their first cognate-based phylogenetic placement, although Edwards (2019) gives lexical percentages for Welaun. The Idaté and Lakalei lists come from surveys by Klamer (2002) and Dawson (2014), not from Edwards or Grimes. Figure 1 shows the 24 lects used in the model-based analyses, one per language. Names follow LexiRumah, with Idaté for Idate, Habu for Habun, Tetun for Tetum and Welaun for Bekais; Lakalei-Idate is Hull's Idalaka. The repository lists every lect with its Glottocode.

![The 24 lects used in the Bayesian and maximum-likelihood analyses, one per language. Lakalei-Idate (red) lies between Central Timor (blue) and the Eastern Timor languages of Grimes and Edwards (dark grey); the dashed line is the border between Timor-Leste and Indonesia. Coordinates from LexiRumah; coastlines from Natural Earth.](figures/map.pdf){width=100%}

# Methods

**Pre-registration.** The protocol was frozen and fingerprinted (SHA-256) on 10 October 2026, before any analysis. Thirteen dated addenda, each pushed to a public repository before the analyses it governs, extended it; each was written after the results of the previous ones had been seen. Only three parts are confirmatory: the pre-registered decision rule (a contested clade needed 70% bootstrap support in both UPGMA and NJ trees, on the primary data and on two screened variants), the predictions of two replications in Addendum 9, and the decision rule of the second round (Addendum 12). Everything else is exploratory. Table 2 lists the deviations from the frozen protocol.

| Protocol | What happened |
|------------------|-----------------------------|
| Gate: all four conditions under the v1 rules | G2 failed. Addendum 1 made G2 relative to the expert benchmark the same day, before any contested clade was scored; G1 passed but missed the Papuan-Austronesian split (UPGMA bootstrap 5% on the primary data) |
| Steps 5 to 8 blind to the Timor topology | While diagnosing the gate, the analyst saw the full UPGMA tree, Timor lects included |
| Step 7: BEAST2, relaxed clock, Yule prior | Replaced by unrooted MrBayes (Addendum 2.4) because BEAST2 and its model-selection package could not be set up at the time; a relaxed clock was run only in the second round, in MrBayes |
| Step 7: Hull-constrained against Edwards-constrained runs, 100 stepping stones | Each clade forced against forbidden, 50 stones; direct comparisons added in the second round |
| Step 8: the decision uses bootstrap rules and a Bayes factor | The bootstrap conditions failed first, so the Bayes factor never decided anything |
| C2 decided like C1 | Addendum 2.1 stated before scoring that C2 cannot be settled lexically |

: Deviations from the frozen protocol.

**Cognates.** Automatic cognate detection used LexStat (threshold 0.55) and SCA (0.45) with Infomap clustering in LingPy 2.6.14 (List, Greenhill and Gray 2017). Scored against the ABVD expert judgements, LexStat reaches a B-cubed F of 0.81 (precision 0.88, recall 0.75); automatic and expert distances correlate at Mantel r = 0.90. Automatic cognates are known to suffice for phylogenetic reconstruction in some families but not all (Rama et al. 2018).

**Trees.** Distance trees (UPGMA, NJ) with 1,000 concept bootstraps were built for 30 hypothesis clades. Treelikeness was measured with delta scores and Q-residuals (Holland et al. 2002; Gray, Bryant and Greenhill 2010). For the model-based analyses, each cognate set is one binary character; a lect without the concept is coded missing. The 24 lects give 1,353 characters. MrBayes 3.2.7a (Ronquist et al. 2012) used the restriction model with no all-absent sites, gamma rate variation and exponential(10) branch lengths: 2,000,000 generations, two runs of two chains, samples every 1,000, 25% burn-in. Stepping-stone runs used 5,000,000 generations, 50 steps and α = 0.4. Maximum-likelihood trees used IQ-TREE 2.3.6 (Minh et al. 2020) with GTR2+FO+G4 and no ascertainment correction, and 1,000 ultrafast bootstrap replicates (UFBoot; Hoang et al. 2018). UFBoot values below 95 are not conventionally read as support.

**Sound changes.** The marked reflexes in Grimes and Edwards's tables were turned into an expert reflex atlas; LexiRumah forms aligned to ABVD PMP forms gave an automatic atlas. The two agree on 94% of tokens (249 of 264). Eleven changes were coded as binary characters (Section 6).

**Inheritance and contact.** Each cognate set was classed as a PMP retention or an innovation, by its distance from ABVD's PMP word after substituting each lect's regular reflexes (balanced accuracy 0.79 against ABVD's experts; a learned classifier with eight features did not beat it, at 0.788, E54). Exclusive shared innovations were counted; a triplet site-pattern test, the lexical counterpart of the ABBA-BABA statistic (Green et al. 2010; Durand et al. 2011), counts for three groups the concepts on which exactly two share an innovation, separately on the 60 Leipzig-Jakarta concepts (Tadmor 2009; Tadmor, Haspelmath and Taylor 2010) and on the rest. Approximate Bayesian computation (ABC; Csilléry et al. 2010), historical glottometry (Kalyan and François 2018), clock analyses and a contact-aware phylogeny (Neureiter et al. 2022) complete the set. Analyses are numbered E1 to E55 as in the repository.

**The second round.** A mock referee report raised four problems: the root, the coding of the sound changes, whether Lakalei-Idate holds together, and retentions among the "innovations". Addendum 12 answered with E40 to E50 and a decision rule for C1 (Section 10), all declared and pushed before any of them was run. Its main additions: seven outgroups beyond Flores, coded together with the Timor data (E40); a relaxed clock (E41); the sound changes scored with a fixed ancestral state and irreversible change (E42); a known-answer calibration on undisputed sound-change groups (E43); Lakalei-Idate kept together and split (E44); topology tests with the root held by the outgroups (E45); shared innovations polarised by the outgroups and cleaned of identified retentions (E46); direct marginal likelihoods (E47); and runs without Tetun and without sets shared with Papuan languages (E48).

**Last checks.** Addendum 13 added five exploratory analyses aimed at known sources of error, again declared before they were run: cognates coded by morpheme rather than by whole word (E51; List, Lopez and Bapteste 2016), regular sound correspondences in the decisive sets (E52), a fuller phonology of 36 sound-change characters (E53), a learned retention classifier (E54) and split networks (E55). They could not change the second round's verdict and did not.

# Results: the pre-registered core

Only low-level groups reach the 70% bar in both distance trees: Lakalei-Idate, Kawaimina, Wetar-Atauro, Nuclear Rote, Kisar-Luang and Babar. Hull's Ramelaic scores 22% (UPGMA) and 55% (NJ); Fabronic, Timor-Babar and Eastern Timor score 0 to 3%. The pre-registered decision is therefore **unresolved** for both C1 and C2. The rule relies on UPGMA, which assumes a clock and is misled by unequal rates (Blust 2000), so it had little chance of resolving higher-level groups.

The confirmatory predictions of Addendum 9 partly failed. Across 351 combinations of dialect lists (E26), Lakalei-Idate + Nuclear Central Timor (Mambae, Kemak, Tokodede) was the largest stable-vocabulary pair against Habu and Kawaimina in every combination, but against Tetun in only 47%: 86% with Tetun Suai and 9% with Tetun Dili, the lingua franca. Under the improved retention rule the Tetun share rises to 79%, still short of the 80% bar, and the prediction that Habu's link sits in borrowable words (P2) fails (31%). On lists collected independently of Grimes and Edwards (E28), the prediction failed against Tetun by one concept (45 to 44); the prediction that Timor-Babar and Lakalei-Idate + Eastern Timor get at most 5% held (0%).

The protocol reports tree results as weak when mean delta exceeds 0.3. For the 24 lects behind every model-based result, mean delta is 0.33, so the trees below are weak by that standard. The most reticulate lects are Welaun, Tokodede, Galoli, Lakalei, Tetun Dili and Idaté, followed by Habu and Tetun Suai, level at 0.28.

# Results: exploratory trees and the root

## The unrooted trees

| Unconstrained MrBayes, 24 lects (unrooted) | Posterior |
|------------------------------|------|
| Lakalei-Idate + Central Timor (with Welaun) | 0.91 |
| Central Timor with Welaun | 0.86 |
| Flores pair + Rote-Meto + Helong | 0.95 |
| Lakalei-Idate | 0.94 |
| Hull's Ramelaic (without Welaun) | 0.13 |
| Timor-Babar; Eastern Timor, with or without Lakalei-Idate; Welaun + Tetun | 0.00 |
| **Direct comparisons (stepping-stone)** | **ln BF** |
| Lakalei-Idate + Central Timor against Lakalei-Idate + Eastern Timor | +11.8 |
| Central Timor with Welaun against Welaun + Tetun | +7.6 |

: Bayesian results. A Bayes factor of a clade forced against the same clade forbidden equals the posterior odds over the prior odds, and any particular group of five or six lects has a tiny prior probability, so modest posteriors give large factors (Bergsten, Nilsson and Ronquist 2013): Ramelaic, at 0.13, gets ln BF +8.0, Central Timor with Welaun +10.3, Timor-Babar −7.0. The direct comparisons avoid that problem. Stepping-stone runs agree within 0.8 log units; the unconstrained runs converged (split-frequency difference 0.005, minimum ESS 1,074).

The unrooted trees put Lakalei-Idate beside Central Timor (0.91) and never with Eastern Timor, Hull's Fabronic or Timor-Babar. The two Flores-Lembata lects, which step 7 used to root the tree, do not sit outside Timor: they attach to Rote-Meto + Helong (0.95). So these trees cannot by themselves separate "Lakalei-Idate sister to Central Timor" from "Lakalei-Idate the first branch of Timor-Babar", and the Timor-Babar Bayes factor partly measures the cost of moving the Flores pair.

## The root

Seven outgroups beyond Flores were coded together with the Timor data (E40): three Western Malayo-Polynesian languages (Tagalog, Buginese, Uma), three Central Malayo-Polynesian languages outside Timor and Flores-Lembata (Kambera, Bima, Manggarai), and Blust's PMP reconstruction as a pseudo-taxon. The relaxed clock (E41) estimates a root without outgroups.

| Analysis | Root on Flores branch | Root on Rote-Meto + Helong | Root on Central Timor stem | Lakalei-Idate + Central Timor a rooted clade | Timor-Babar a rooted clade |
|----------------|-----|-----|-----|-----|-----|
| All seven outgroups, MrBayes | 0.93 | 0.07 | 0.00 | 1.00 | 0.00 |
| All seven outgroups, ML (UFBoot) | 0.87 | 0.12 | 0.00 | 0.98 | 0.00 |
| Far outgroups only (UFBoot) | 0.16 | 0.77 | 0.00 | 0.98 | 0.00 |
| Near outgroups only (UFBoot) | 0.94 | 0.03 | 0.00 | 0.98 | 0.00 |
| PMP only (UFBoot) | 0.04 | 0.70 | 0.00 | 0.97 | 0.00 |
| Relaxed clock, 24 lects | 0.11 | 0.42 | 0.00 | 0.96 | 0.00 |
| Relaxed clock, without Tela-Masbuar | 0.23 | 0.52 | 0.00 | 0.98 | 0.00 |
| Strict clock, root forced on Flores (E34) | 1.00 | | | 0.77 | 0.00 |

: Where the root falls. Each tree is reduced to the 24 lects and rooted on the reference outgroup (Tagalog; Kambera for the near set; PMP for PMP alone); the clocks give their own root. "Rooted clade" means the group excludes every outgroup. In the relaxed clocks the rest falls on Kisar-Luang-Tela-Masbuar (0.17 and 0.07) or is spread over other branches, none above 0.06. The MrBayes runs converged (split-frequency differences 0.008, 0.019 and 0.014).

In no analysis does the root fall on the Central Timor stem. With outgroups, it falls on the Flores branch (near outgroups, and all seven together) or on the Rote-Meto + Helong branch (far outgroups and PMP); the relaxed clocks favour Rote-Meto + Helong too, with or without Tela-Masbuar. Either way Central Timor and Lakalei-Idate end up on the same side of the root, so Lakalei-Idate + Central Timor is a rooted clade (0.96 to 1.00) and Timor-Babar never is. This answers the specific worry that the lexical tree is Grimes and Edwards's tree with a different root: the outgroups do not put the root where their tree needs it. It does not settle C1. The outgroups attach by lexical similarity too, and Rote-Meto's place next to the root could reflect conservatism or contact across the Savu Sea as much as an early split.

![Consensus tree (all compatible splits) of the Bayesian analysis with seven outgroups (grey), 31 lects and 1,599 cognate characters coded together (E40), rooted on Tagalog and drawn as a cladogram. Numbers are posterior probabilities; unlabelled nodes exceed 0.99.](figures/tree.pdf){width=80%}

## Does Lakalei-Idate hold together?

Both classifications treat Lakalei-Idate as a unit, but the lexical trees do not always keep it together: the pair forms a group in 94% of MrBayes samples but in 53% of primary UFBoot replicates, and in 5% on the independent lists, where Lakalei falls inside Nuclear Central Timor. E44 kept the pair together and then analysed each member alone.

| UFBoot % | With Central Timor | With Nuclear Central Timor | With Eastern Timor | With Habu |
|--------------------------|-----|-----|-----|-----|
| Primary lists, Lakalei-Idate kept together | 70 | 41 | 0 | 0 |
| Primary lists, Idaté alone | 52 | 3 | 2 | 38 |
| Primary lists, Lakalei alone | 84 | 75 | 0 | 0 |
| Independent lists, Lakalei-Idate kept together | 98 | 98 | 0 | 0 |
| Independent lists, Idaté alone | 79 | 79 | 7 | 13 |
| Independent lists, Lakalei alone | 99 | 99 | 0 | 0 |
| Primary lists without Tetun (E48) | 94 | 8 | 1 | 2 |
| Primary lists without 132 sets shared with Papuan lects (E48) | 46 | 51 | 0 | 0 |
| SCA cognates (E15) | 92 | | | |
| LexStat at thresholds 0.35 and 0.75 (E15) | 15, 20 | | | |
| LexiRumah's published cognates (E15) | 0 | | | 51 (Lakalei-Idate + Habu) |
| Consensus of five codings (E27) | 0 | 55 | 0 | |
| Partial cognates, by morpheme (E51) | 23 | 65 | 0 | 10 |
| Partial cognates, Lakalei-Idate kept together (E51) | 28 | 73 | 0 | 12 |

: Lakalei-Idate kept together, split, and under other codings and taxon sets. On the independent lists Central Timor has no Welaun.

Lakalei is consistently Central Timor-like; Idaté is pulled partly towards Habu, its neighbour 5 to 11 km away, on the primary lists (38%), less so on the independent ones (13%). In the observed counts, Idaté shares more stable-concept innovations with Habu (13) than with Nuclear Central Timor (10), and Lakalei the reverse (13 against 6). With the pair held together, Lakalei-Idate + Central Timor gets 70% on the primary lists and 98% on the independent ones. No coding or taxon set puts Lakalei-Idate with Eastern Timor. The support for Central Timor depends on the coding (0% to 92%; a check modelled on Kaiping and Klamer 2022), and drops to about half once the 132 sets shared with Papuan languages are removed. Mambae, Kemak, Welaun, Idaté and Lakalei each share 40 to 49 sets with Papuan lects, against 30 to 37 for Tokodede and the Eastern Timor languages, so part of the lexical link between Lakalei-Idate and Central Timor may run through shared contact with Bunak. Removing Tetun has the opposite effect: Lakalei-Idate + Central Timor rises to 94%. Coding cognates by morpheme (E51), which merges compounds the whole-word coding split, moves support from Central Timor with Welaun to Nuclear Central Timor (65%, and 73% kept together).

## Topology tests

| Constrained tree | Data | ΔlnL | p (AU) | Holm, all tests |
|-------------------------------|----------------|-----|-----|-----|
| Ramelaic (E6) | Primary | 1.1 | 0.47 | 1.00 |
| Timor-Babar (E6) | Primary | 11.7 | 0.067 | 0.47 |
| Lakalei-Idate + Eastern Timor (E6) | Primary | 10.4 | 0.071 | 0.47 |
| Lakalei-Idate + Eastern Timor (E36) | Independent | 19.5 | 0.025 | 0.22 |
| Timor-Babar (E36) | Independent | 14.8 | 0.042 | 0.34 |
| Lakalei-Idate + Central Timor, rooted (E45) | Primary + outgroups | 0.0 | 0.63 | 1.00 |
| Timor-Babar, rooted (E45) | Primary + outgroups | 29.9 | 0.011 | 0.12 |
| Lakalei-Idate + Eastern Timor (E45) | Primary + outgroups | 14.4 | 0.17 | 0.69 |
| Lakalei-Idate + Central Timor, rooted (E45) | Independent + outgroups | 0.0 | 0.59 | 1.00 |
| Timor-Babar, rooted (E45) | Independent + outgroups | 19.8 | 0.022 | 0.22 |
| Lakalei-Idate + Eastern Timor (E45) | Independent + outgroups | 15.8 | 0.070 | 0.47 |

: AU tests (Shimodaira 2002) with 10,000 RELL replicates. In E45 every tree keeps Lakalei-Idate together and the seven outgroups hold the root. Holm's correction runs over every topology test in the project. ΔlnL comes from the AU test's re-optimisation, so it differs slightly from the search log-likelihoods (10.5 rather than 10.4 for the eastern placement on the primary lists).

No test rejects Lakalei-Idate + Central Timor. Uncorrected, the eastern placement and Timor-Babar have p from 0.011 to 0.17. With the root held by the outgroups and Lakalei-Idate kept together (E45), a rooted Timor-Babar costs 20 to 30 log-likelihood units (p = 0.011 and 0.022), but Lakalei-Idate + Eastern Timor is no longer rejected even uncorrected on the independent lists (p = 0.07): E36's rejection depended on letting Lakalei fall inside Nuclear Central Timor. After Holm's (1979) correction over all eleven topology tests, none is rejected (smallest adjusted p = 0.12). Two other tests point the same way as the uncorrected AU tests. A parametric bootstrap of the eastern placement (SOWH; Goldman, Anderson and Rodrigo 2000; E38), with Lakalei-Idate free to split, gives p = 0.01 on both list sets: none of 100 simulated differences reached the observed ones (10.5 and 19.4 log units, against at most 3.2 and 4.8). And compared directly by stepping-stone sampling, Lakalei-Idate + Central Timor beats Lakalei-Idate + Eastern Timor by ln BF +11.8 (Table 3; E47). Both treat borrowed words as inherited, and the SOWH test is known to reject too readily when the model is misspecified (Susko 2014), so they do not override the corrected AU result; they do show that the vocabulary consistently disfavours the eastern placement.

## How often does vocabulary recover subgroups that sound changes define?

The lexicon's failure to recover Timor-Babar needs a baseline. Of the ten Grimes and Edwards groups with at least two lects in the analysed set, other than the contested ones, the unrooted MrBayes tree recovers six at posterior 0.95 and the ML tree four at UFBoot 95 (E43). The failures include groups nobody here disputes: West Rote-Meto (Dela + Meto: posterior 0.00, UFBoot 3), Kisar-Luang (0.00, UFBoot 2; Luang pairs with Tela-Masbuar instead), Tetun + Habu (0.00) and, narrowly, Lakalei-Idate itself (0.94, UFBoot 53); Nuclear Central Timor gets 0.95 but UFBoot 59. In the pre-registered distance trees Southwest Maluku gets 0% and 30%, and Nuclear Central Timor 37% and 75%. Lexical non-recovery is common for sound-change groups in this region, so the absence of a lexical Timor-Babar says little about Timor-Babar.

# Results: the sound changes

**What the comparative method shows.** In the automatic atlas, Lakalei-Idate keeps \*p in 0 of 6 words, against 54 of 55 in Mambae, Kemak and Tokodede (Fisher's exact p = 1.3 × 10⁻⁷, E2), and Flores-Lembata keeps it in 10 of 10. Some of the Lakalei-Idate words look like Tetun and could be loans, but native cases remain: \*əpat 'four' > Idaté *aːt* (Tetun *haːt*), \*nipən 'tooth' > Lakalei *niɑn*, and Grimes and Edwards's \*pija > *ila* 'how much' and \*hapuy > *wai* 'fire'. One counter-case keeps a labial (\*palu 'hit' > Idaté *paʔu*, Lakalei *baʔu*). Lakalei-Idate also lacks Central Timor's \*ŋ > g, as in \*taliŋa 'ear' > Idaté *talina* against Mambae *teliga*, and has \*ma-p > b where Central Timor has \*mp. Two facts limit these as diagnostics: Welaun, a Central Timor language on every other count, has \*p > h in native words (*hoat* 'four'), so the change happened more than once on Timor; and several changes recur outside their defining groups, in Sika for \*ŋ > n and \*d > r, l, in Dela for \*d > r, l, and in Galoli and Ili'uun for Hull's initial \*b- > h (E42).

![Eight diagnostic sound changes coded from the reflexes Grimes and Edwards (2026) mark in their comparative tables, for the languages of Timor, Wetar-Atauro and Rote-Meto (Southwest Maluku is omitted here and shown in the repository). Outlined cells rest on fewer than two expert tokens. The last column merges \*b > h and \*b > f, so it is not the same character as Hull's initial \*b- > h.](figures/sounds.pdf){width=80%}

**Scored on the rival trees.** E29 scored the eleven characters by Fitch parsimony with the Flores outgroups coded unknown for \*p, which lets \*p lenition sit at the base of the whole tree and lets it reverse. E42 coded the outgroups from the atlases (\*p retained) and counted irreversible change, rooted on the Flores pair.

| Steps on each tree, rooted on Flores | Lexical tree (H) | Lakalei-Idate + Eastern Timor (G) | Grimes and Edwards's split (GE) |
|-------------------------------|-----|-----|-----|
| \*p lenition, Fitch | 2 | 2 | 2 |
| \*p lenition, irreversible (Camin-Sokal) | 6 | 4 | 2 |
| \*p lenition, one origin and losses (Dollo) | 2 | 2 | 2 |
| All eleven, Fitch | 33 | 34 | 32 |
| All eleven, Camin-Sokal | 49 | 47 | 51 |
| All eleven, Dollo | 54 | 49 | 43 |
| Lexical log-likelihood, relative to H | 0 | −10.5 | −12.0 |

: The sound changes on the rival trees (E42). The lexical trees are the unconstrained ML tree and trees constrained to each alternative.

If lenition does not reverse, the change that defines Timor-Babar must arise six times on the lexical tree and twice on Grimes and Edwards's: that change clearly favours their tree. Under Dollo counting, where \*p lenition arises once and Central Timor's \*p is a restoration, the trees tie on that change. The other ten characters are sparse and often parallel, and their totals point different ways depending on the cost model. The phonology and the vocabulary therefore disagree about Lakalei-Idate, and that disagreement is the main finding of this section. Combining 8 to 17 sound-change characters with the 1,353 lexical characters, with equal weights, cannot show agreement, because the phonology is about 1% of such a matrix (on weighting character types, see Ringe, Warnow and Taylor 2002); those combined trees are left to the repository. A likelihood treatment of irreversible change, such as the stochastic Dollo model (Nicholls and Gray 2008), would need far more characters than eleven.

**A fuller phonology.** E53 turned every non-retention reflex class in the expert atlas into a character, 36 after filtering. Under irreversible change the eastern tree (G) beats the lexical tree on 6 characters to 0 (sign test p = 0.03), but all six are changes Tetun shares with Kawaimina and, where it is coded, Habu. G keeps those three together and the lexical tree does not, and only two of the six involve Lakalei-Idate. Grimes and Edwards's tree ties the lexical tree (2 to 2 characters under Camin-Sokal, 8 to 6 under Dollo, 1 to 3 under Fitch). A Bayesian tree from these characters alone recovers Lakalei-Idate (0.81) but neither of its placements, nor Timor-Babar (0.00 each). Beyond \*p lenition, then, the fuller phonology does not decide where Lakalei-Idate goes; its one clear preference concerns Tetun.

# Results: inheritance or contact for Lakalei-Idate

**Shared innovations, cleaned.** Under the validated rule, Lakalei-Idate shares 6 exclusive innovations with Central Timor and 9 with the Eastern Timor groups combined (E17). A review of the six found four errors: the two 'wife' sets continue one etymon, PAN \*b<in>ahi, that the automatic coding split (coding by morpheme merges them, E51); 'who' pairs non-cognate forms (Idaté *ʔɛta*, Mambae *sepdua*); and 'dry' is doubtful. That leaves 'cry' (*sɛro*, against *tanis* < \*taŋis almost everywhere else) and 'spit'. The 9 eastern sets passed the automatic checks (E35, E37) but have not been reviewed by hand, so the comparison is uneven and the counts should be read as 2 or 3 against at most 9.

**Triplet test.** Table 8 gives the stable-concept counts for (Lakalei-Idate, Nuclear Central Timor, X) under three treatments: the validated rule; the same with 66 identified retentions and errors reclassified (those found in review of the decisive sets, E35's strict etymological matches and E37's matches with Grimes and Edwards's tables); and the cleaned counts polarised by excluding sets present in Flores, Rote-Meto + Helong or Wetar.

| Stable concepts, representative lists | LI + NCT | LI + X | NCT + X |
|-----------------------------|-----|-----|-----|
| X = Tetun: validated rule | 21 | 12 | 10 |
| X = Tetun: cleaned | 10 | 5 | 6 |
| X = Tetun: cleaned and polarised | 8 | 5 | 0 |
| X = Habu: validated rule | 23 | 19 | 15 |
| X = Habu: cleaned | 12 | 12 | 4 |
| X = Habu: cleaned and polarised | 10 | 12 | 0 |
| X = Kawaimina: validated rule | 80 | 38 | 23 |
| X = Kawaimina: cleaned | 42 | 27 | 13 |
| X = Kawaimina: cleaned and polarised | 36 | 21 | 1 |
| *Single-survey lists, cleaned and polarised: Tetun, Habu, Kawaimina* | *12, 10, 30* | *10, 9, 18* | *2, 0, 0* |
| *Polarised by all nine outgroups, representative: Tetun, Habu, Kawaimina* | *23, 21, 69* | *14, 21, 38* | *5, 5, 9* |
| *Partial cognates, polarised, not cleaned (E51): Tetun, Habu, Kawaimina* | *10, 13, 48* | *18, 14, 24* | *3, 1, 6* |

: Triplet counts on stable concepts (E46). Counts are summed over the combinations of lects in each group (for example 2 × 3 × 3 for Kawaimina), so they exceed the number of concepts.

On the representative lists, Lakalei-Idate + Nuclear Central Timor stays the largest pair against Tetun and Kawaimina in every treatment; on the single-survey lists Nuclear Central Timor + Tetun matches or beats it until the counts are polarised (36 to 36 with the validated rule, 22 to 18 cleaned). Against Habu it ties once the retentions are removed and falls behind once the counts are polarised. The tree-pair rule itself was calibrated by simulation (E46): with no borrowing, on the lexical tree, Lakalei-Idate + Nuclear Central Timor comes out strictly largest against all three groups at once in only 21% of datasets (15% polarised); on the tree with Lakalei-Idate in Eastern Timor it does so in 3% (5%). The rule rarely produces the observed pattern by accident, but it misses it most of the time when it is true. Coded by morpheme and polarised (E51), the counts lean further away from Nuclear Central Timor, towards Tetun (18 to 10) and narrowly Habu (14 to 13); these counts are not cleaned by hand, and loose morpheme coding counts any shared element, which picks up Tetun loans inside compounds. The D statistic was calibrated earlier (E31): with unequal branch lengths and no borrowing, the null D for these triplets centres on 0.44 to 0.47, every observed value lies inside it, and the naive Z ≥ 2 rule fires in 27% of contact-free datasets. The calibrated test has a 5% false-positive rate and detects 20% borrowing from Habu 30% of the time. So none of Lakalei-Idate's excesses is evidence of contact, and none is evidence against it.

![Triplet counts on stable (Leipzig-Jakarta) and borrowable concepts, with the original retention rule used in E18 and E31 (Table 8 gives the validated-rule and cleaned counts), representative lists. Each bar is one triplet of the focal group (Welaun or Lakalei-Idate), Nuclear Central Timor (Mambae, Kemak and Tokodede) and a third group; the numbers are summed over combinations of lects. Welaun, whose Tetun contact is documented, is the control. Against a simulated null with unequal rates, only Welaun's jackknife Z in borrowable words stands out (beyond 99.8% of the null), although its D does not (p = 0.15).](figures/triplets.pdf){width=100%}

**Which half carries the signal.** In stable vocabulary, five of the eight Central Timor items are shared by both Idaté and Lakalei; in borrowable vocabulary, six of eight are found only in Lakalei and match Mambae, spoken 10 km away. The counts are small (binomial p = 0.125 for the borrowable items), and with the other Idaté list the stable split becomes 3 shared, 4 in Lakalei only and 2 in Idaté only, which weakens the reading that the shared items are old. A correspondence test (E33) finds the Lakalei items no closer to identity than inherited words. A stricter version (E52) looked for regular non-identity correspondences in eight lect pairs and found almost none (0 to 2 sound classes per pair, from 24 to 30 shared retentions), so most decisive sets cannot be tested, and the few that can split evenly between loan-like and inherited-like (Fisher p = 1.0 on both sides).

**Borrowing simulations.** ABC was run twice: with borrowing from one side only (E21, now superseded) and from both sides into proto-Lakalei-Idate (E32). In E32 the random forest (Pudlo et al. 2016) splits its votes 0.45 to 0.55 and misclassifies 36% of its own simulations; every borrowing parameter has the prior U(0, 0.6) (median 0.30, 90% interval 0.03 to 0.57), and the four stable-vocabulary ones end with posterior medians of 22 to 25% and 90% intervals of about 2 to 57%, close to that prior. Both models pass all 36 predictive checks, which with 36 two-sided checks points to wide predictive distributions rather than a good fit. The pre-declared reading that Grimes and Edwards's placement is "hard to defend lexically" if it needs more than 20% stable borrowing triggered (25%), but the other placement needs the same amount, so the rule measures the prior. The design cannot separate the placements: its statistics are a handful of counts (Robert et al. 2011), and its simulator moves both Lakalei-Idate lects together, so it cannot represent Idaté's and Lakalei's different neighbours.

**Glottometry and dating.** Glottometry finds cohesive groups only at low levels. With 95% intervals from resampling concepts (E50), Lakalei-Idate's subgroupiness is 1.42 (0 to 3.65), its ties to Central Timor 0.06 (0 to 0.31) and to Eastern Timor 0.08 (0 to 0.41), and Hull's Ramelaic 0 in every resample. Measured only in samples where both groups are clades (E49), the common ancestor of Lakalei-Idate and Central Timor is older than Central Timor's own by a median of 12% of the latter's height under the strict clock and 21% (95%: 4 to 71%) under the relaxed clock, where Central Timor with Welaun is a clade in 72% of samples.

**A contact-aware tree.** contacTrees (Neureiter et al. 2022), which adds horizontal transfer edges to a tree, did not settle when left free (E19): it kept adding edges. Capped at five edges (E39), it used all five in every sample, some between unlikely partners (Dela and Habu in 99% of samples). Its base tree puts Lakalei-Idate with Tetun and Habu (0.78) and Welaun beside them (1.00), apart from Nuclear Central Timor, with a transfer edge between Lakalei and Tokodede in every sample and between Mambae and Lakalei or Idaté in under a tenth. Because the model always uses the maximum number of edges, it is misspecified, and its base tree should not be read as the history. What it does show is that a few transfer events can carry the Central Timor signal in Lakalei-Idate's vocabulary as well as descent can.

**A split network.** NeighborNet (Bryant and Moulton 2004) on the primary distances with 200 concept bootstraps (E55) shows Lakalei-Idate as a split in 89% of networks, Lakalei-Idate + Central Timor in 47%, Idaté + Habu in 45% and Lakalei-Idate + Eastern Timor in 2%. By the reading declared in advance this is unclear, because neither side reaches half. The near balance, with Idaté rather than the pair on the eastern side, fits a linkage, but a short internal branch would look the same.

# Results: Welaun (C2)

Welaun goes with Central Timor in the model-based trees (posterior 0.86; Table 3) and its Tetun similarity sits in borrowable words: on the 60 stable concepts Welaun + Tetun gets 2% (UPGMA) and 4% (NJ), on the other 92 concepts 74% and 81% (E1), and the triplet test locates the excess there (Z = 6.9 against 0.6). Several results point the other way. The pre-registered distance trees favour Welaun + Tetun (51% and 59%) over Central Timor (14% and 17%). Under the consensus coding Central Timor with Welaun gets 0%, and the Welaun control's tree pair becomes Welaun + Tetun even on stable concepts (10 to 8). Under the strict clock (E34) Central Timor with Welaun has posterior 0.29. Compared directly (E47), Central Timor with Welaun beats Welaun + Tetun by ln BF +7.6. Addendum 2.1 stated in advance that C2 cannot be settled lexically. The fair summary is that once borrowable vocabulary is set aside, the lexical evidence is consistent with Edwards (2019).

# Results: other disputed branches

| Triplet | Counts, all concepts (stable) | Reading |
|-------|------------------|----------|
| Habu, Tetun, Kawaimina | Habu+Tetun 15 (5); Habu+Kawaimina 11 (5); Tetun+Kawaimina 4 (2) | Unresolved |
| Waima'a, Naueti, Midiki | Waima'a+Naueti 10 (7); Waima'a+Midiki 7 (4); Naueti+Midiki 2 (1) | Waima'a+Naueti largest, as in Grimes and Edwards |
| Galoli, Wetar, Dadu'a | Galoli+Dadu'a 20 (13); Galoli+Wetar 6 (2); Wetar+Dadu'a 6 (4) | Galoli+Dadu'a largest |
| Galoli, Wetar, Tetun | Galoli+Wetar 12 (8); Galoli+Tetun 6 (4); Wetar+Tetun 0 (0) | Galoli+Wetar largest |
| Helong, Meto, Rote | Meto+Rote 17 (12); Helong+Meto 10 (8); Helong+Rote 3 (2) | Meto+Rote largest |

: Triplet tests on other disputed placements (E24). The largest pairs are robust to the classifier change; the imbalances between the other two pairs are uncalibrated for these triplets and none survives multiple-testing correction, so they are not read as contact.

# The second-round decision

| Condition for reporting Central Timor (Addendum 12) | Result | Met? |
|-------------------------------------|-------------|----|
| 1. Root: Lakalei-Idate + Central Timor a rooted clade, MrBayes posterior ≥ 0.95, and UFBoot ≥ 95 in two of three outgroup sets | Posterior 1.00; UFBoot 98, 98 and 97 | Yes |
| 2. Lakalei-Idate kept together: UFBoot ≥ 95 with Central Timor on both list sets | 70 (primary), 98 (independent) | No |
| 3. Lakalei-Idate + Eastern Timor and Timor-Babar both rejected after Holm, root held by outgroups | Holm-adjusted p 0.06 and 0.11 (Timor-Babar), 0.52 and 0.28 (eastern placement) | No |
| 4. Polarised, cleaned stable pairing largest against Tetun, Habu and Kawaimina, with the tree-pair rule picking it under G in under 20% | Fails against Habu (10 to 12, representative lists); rule 5% under G | No |

: The second round's decision rule for C1. Grimes and Edwards's placement would be reported as lexically supported if Timor-Babar were a rooted clade (posterior ≥ 0.95), or if the root sat on the Central Timor stem (≥ 0.95) and Lakalei-Idate + Eastern Timor were not rejected; neither happened (posterior 0.00 for both).

By the rule declared before the second round, **C1 is unresolved by the vocabulary**. Only the root condition holds; the placement fails once Lakalei-Idate is kept together on the primary lists, once the topology tests are corrected, and once the shared innovations are cleaned.

# Discussion

**What the vocabulary shows.** Three results hold under every coding, taxon set and outgroup tried. No analysis groups Lakalei-Idate with Eastern Timor or recovers Hull's Fabronic, Timor-Babar or Eastern Timor as a lexical group. The low-level groups hold. And the outgroups and the relaxed clock put the root on the western side, never on the Central Timor stem, so the lexical tree is not simply Grimes and Edwards's tree with a different root. Within that frame the vocabulary places Lakalei-Idate beside Central Timor, and disfavours the eastern placement in a direct comparison (ln BF +11.8), but not robustly enough to pass the second round's rule.

**What it does not show.** The vocabulary does not refute Timor-Babar. Lexical trees here miss about half of the undisputed sound-change groups, so a missing lexical Timor-Babar is expected even if the group is real. Nor does the vocabulary place Lakalei-Idate securely in Central Timor: the support depends on the cognate coding, on Lakalei-Idate being forced together, and on sets shared with Papuan languages, and once the identified retentions are removed the shared innovations no longer favour Central Timor over Habu. The defining sound change, \*p lenition, favours Grimes and Edwards's tree if lenition does not reverse.

**Alternative explanations.** Four mechanisms could produce the lexical pattern without descent, and the data cannot rule any of them out.

- *Tetun as a lingua franca.* Simulations suggest that realistic borrowing rates rarely overturn lexical tree topologies (Greenhill, Currie and Gray 2009), but a lingua franca in sustained contact is not a realistic-rate case. Tetun itself groups lexically with Central Timor and Lakalei-Idate (0.90), against its classification by sound changes, as it already did in Gray et al. (2009). Removing Tetun raises Lakalei-Idate + Central Timor to 94% rather than lowering it, so Tetun is not what holds the pair together; but older Tetun loans that have adapted to the borrowing language would escape the near-identity screen (Hajek 2006; Williams-van Klinken, Hajek and Nordlinger 2002).
- *Papuan contact.* Central Timor and Lakalei-Idate share more sets with Papuan lects than Eastern Timor does, and removing those sets halves the support. East Nusantara is a linguistic area in its own right (Klamer, Reesink and van Staden 2008).
- *A dialect chain or linkage.* Grimes and Edwards already call Wetar-Atauro "overlapping subgroups". Lakalei's ties to Mambae and Idaté's to Habu, each with its nearest neighbour, are what a linkage (Ross 1988; François 2014) would produce, and glottometry ties Lakalei-Idate about equally weakly to both sides, as a split network does (47% and 45% of bootstrap networks, E55). Schapper (2020) explains much of eastern Timor's word structure by sound changes spreading within a Timorese Sprachbund, as Hull (2001b) had suggested. A Timor-Babar subgroup and a Timor-Babar linkage would differ in whether \*p lenition spread as one change before the daughters diverged or across already separate varieties, which the present data cannot tell apart.
- *Unequal rates.* Lakalei-Idate is a conservative lineage with a short branch, the situation in which lexicostatistics misleads (Blust 2000), and in which retentions misread as innovations inflate the counts shared with other conservative lineages.

**What would settle it.** A specialist's review of every cognate set behind the decisive counts, on both sides (the packet in the repository now covers the Central Timor side and the eastern exclusive sets); Grimes and Edwards's 494-item field lists for Idaté and Lakalei, which are not public; Hull (1998), whose lexical percentages could be compared directly; Alcantara's full Idaté corpus; and a regular-correspondence analysis of complete wordlists, which these short lists cannot support (E52 found too few regular correspondences in them).

# Limitations

The confirmatory content is small: the pre-registered rule returned "unresolved", the replications failed against Tetun, and the second round's rule returned "unresolved" again. Everything else is exploratory and was planned after earlier results had been seen; follow-up analyses were often prompted by unfavourable results, and the main tree placement received fewer probes until the second round. After correction, only Welaun's Tetun contact is statistically secure. The cognates are automatic and only partly checked; the consensus coding, partial cognates, the validated classifier and the etymological checks reduce but do not remove that dependence. LexiRumah is a single compilation, although its Idaté, Lakalei and replacement Central Timor lists come from collectors other than Edwards and Grimes. Some sound-change cells for Idaté and Lakalei rest on a handful of tokens. The simulated nulls (E31, E32, E46) use trees and branch lengths estimated from the same data, so contact that shaped those trees is built into the null. The outgroups are attached by lexical similarity and could be pulled towards western Timor by contact across the Savu Sea or by shared retention. Hull (1998), Hull (2001b) and Carvalho (2001) could not be obtained; Hull's classification is cited from Hull (2001a, 2003) and secondary sources.

# Data and code {.unnumbered}

All data, code, results, the protocol and its addenda are at <https://github.com/DenC-dev/liabut>. The numbered scripts in `src/` rerun every analysis from pinned upstream data. The derived datasets (Grimes and Edwards's tables as data, expert and automatic reflex atlases, sound-change matrices, loan classifications, the Alcantara Idaté list, the retention or innovation status of every cognate set, and the specialist review packet) are in `derived/`. Analyses not discussed here (E14, E19, E21, E23, E33 and the combined analyses) and the history of earlier drafts are in `results/REPORT.md` and `results/LITERATURE.md`. Code is MIT-licensed; data keep their sources' licences.

# Use of AI {.unnumbered}

The code, the analyses and the drafting of this paper were carried out with substantial assistance from Claude (Anthropic), an AI system, under the author's direction. The referee report that prompted the second round was also written by Claude, as a mock review. Every analysis, decision and correction is recorded in the public repository so that it can be checked.

# References {.unnumbered}

::: {.refs}
Albuquerque, Davi Borges de. 2009. Pré-história, história e contatos lingüísticos em Timor Leste. *Domínios de Lingu@gem* 3(2): 75–93.

Alcantara, Maressa Xavier. 2015. *Descrição fonética e fonológica da língua idaté do Timor Leste*. MA thesis, Universidade de São Paulo.

Bergsten, Johannes, Anders N. Nilsson and Fredrik Ronquist. 2013. Bayesian tests of topology hypotheses with an example from diving beetles. *Systematic Biology* 62(5): 660–673.

Blust, Robert. 2000. Why lexicostatistics doesn't work: the 'universal constant' hypothesis and the Austronesian languages. In Colin Renfrew, April McMahon and Larry Trask (eds.), *Time Depth in Historical Linguistics*, 311–331. Cambridge: McDonald Institute for Archaeological Research.

Blust, Robert, Stephen Trussel and Alexander D. Smith. *The Austronesian Comparative Dictionary*. CLDF release, lexibank/acd (commit 16085f2).

Bryant, David and Vincent Moulton. 2004. Neighbor-Net: an agglomerative method for the construction of phylogenetic networks. *Molecular Biology and Evolution* 21(2): 255–265.

Csilléry, Katalin, Michael G. B. Blum, Oscar E. Gaggiotti and Olivier François. 2010. Approximate Bayesian computation (ABC) in practice. *Trends in Ecology and Evolution* 25(7): 410–418.

Dawson, Virginia. 2014. Manatuto survey word lists. PARADISEC collection VD1. In Kaiping, Edwards and Klamer (2019).

Donohue, Mark and Charles E. Grimes. 2008. Yet more on the position of the languages of eastern Indonesia and East Timor. *Oceanic Linguistics* 47(1): 114–158.

Durand, Eric Y., Nick Patterson, David Reich and Montgomery Slatkin. 2011. Testing for ancient admixture between closely related populations. *Molecular Biology and Evolution* 28(8): 2239–2252.

Edwards, Owen. 2019. Reintroducing Welaun. *Oceanic Linguistics* 58(1): 31–58.

Edwards, Owen. 2021. *Rote-Meto Comparative Dictionary*. Canberra: ANU Press.

Fogaça, Jessé Silveira. 2015. *Aspectos gramaticais da língua Makasae de Timor-Leste*. PhD thesis, Universidade de Brasília.

François, Alexandre. 2014. Trees, waves and linkages: models of language diversification. In Claire Bowern and Bethwyn Evans (eds.), *The Routledge Handbook of Historical Linguistics*, 161–189. London: Routledge.

Goldman, Nick, Jon P. Anderson and Allen G. Rodrigo. 2000. Likelihood-based tests of topologies in phylogenetics. *Systematic Biology* 49(4): 652–670.

Gray, Russell D., Alexei J. Drummond and Simon J. Greenhill. 2009. Language phylogenies reveal expansion pulses and pauses in Pacific settlement. *Science* 323: 479–483.

Gray, Russell D., David Bryant and Simon J. Greenhill. 2010. On the shape and fabric of human history. *Philosophical Transactions of the Royal Society B* 365: 3923–3933.

Green, Richard E. et al. 2010. A draft sequence of the Neandertal genome. *Science* 328: 710–722.

Greenhill, Simon J., Robert Blust and Russell D. Gray. 2008. The Austronesian Basic Vocabulary Database. *Evolutionary Bioinformatics* 4: 271–283.

Greenhill, Simon J., Thomas E. Currie and Russell D. Gray. 2009. Does horizontal transmission invalidate cultural phylogenies? *Proceedings of the Royal Society B* 276: 2299–2306.

Grimes, Charles E. and Owen Edwards. 2026. *The Austronesian languages of eastern Indonesia and Timor-Leste: Unravelling their prehistory and classification*. Berlin: Language Science Press.

Hajek, John. 2006. Language contact and convergence in East Timor: the case of Tetun Dili. In Alexandra Y. Aikhenvald and R. M. W. Dixon (eds.), *Grammars in Contact*, 163–178. Oxford: Oxford University Press.

Heggarty, Paul, Warren Maguire and April McMahon. 2010. Splits or waves? Trees or webs? How divergence measures and network analysis can unravel language histories. *Philosophical Transactions of the Royal Society B* 365: 3829–3843.

Hoang, Diep Thi, Olga Chernomor, Arndt von Haeseler, Bui Quang Minh and Le Sy Vinh. 2018. UFBoot2: improving the ultrafast bootstrap approximation. *Molecular Biology and Evolution* 35(2): 518–522.

Holland, Barbara R., Katharina T. Huber, Andreas Dress and Vincent Moulton. 2002. δ plots: a tool for analyzing phylogenetic distance data. *Molecular Biology and Evolution* 19(12): 2051–2059.

Holm, Sture. 1979. A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2): 65–70.

Hull, Geoffrey. 1998. The basic lexical affinities of Timor's Austronesian languages: a preliminary investigation. *Studies in Languages and Cultures of East Timor* 1: 97–202.

Hull, Geoffrey. 2001a. O mapa linguístico de Timor Leste: uma orientação dialectológica. *Studies in Languages and Cultures of East Timor* 4: 1–19.

Hull, Geoffrey. 2001b. A morphological overview of the Timoric Sprachbund. *Studies in Languages and Cultures of East Timor* 4.

Hull, Geoffrey. 2003. Lia-Bekais nia fatin iha dalen-lubun Timór. *Studies in Languages and Cultures of East Timor* 5: 55–78.

Kaiping, Gereon A. and Marian Klamer. 2022. The dialect chain of the Timor-Alor-Pantar language family: a new analysis using systematic Bayesian phylogenetics. *Language Dynamics and Change* 12(2): 274–326.

Kaiping, Gereon A., Owen Edwards and Marian Klamer, eds. 2019. *LexiRumah* 3.0. Leiden University Centre for Linguistics.

Kalyan, Siva and Alexandre François. 2018. Freeing the comparative method from the tree model: a framework for historical glottometry. *Senri Ethnological Studies* 98: 59–89.

Klamer, Marian. 2002. Timor-Leste survey word lists. In Kaiping, Edwards and Klamer (2019).

Klamer, Marian, Ger Reesink and Miriam van Staden. 2008. East Nusantara as a linguistic area. In Pieter Muysken (ed.), *From Linguistic Areas to Areal Linguistics*, 95–149. Amsterdam: John Benjamins.

List, Johann-Mattis, Philippe Lopez and Eric Bapteste. 2016. Using sequence similarity networks to identify partial cognates in multilingual wordlists. In *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, 599–605.

List, Johann-Mattis, Simon J. Greenhill and Russell D. Gray. 2017. The potential of automatic word comparison for historical linguistics. *PLOS ONE* 12(1): e0170046.

Minh, Bui Quang, Heiko A. Schmidt, Olga Chernomor, Dominik Schrempf, Michael D. Woodhams, Arndt von Haeseler and Robert Lanfear. 2020. IQ-TREE 2: new models and efficient methods for phylogenetic inference in the genomic era. *Molecular Biology and Evolution* 37(5): 1530–1534.

Neureiter, Nico et al. 2022. Detecting contact in language trees: a Bayesian phylogenetic model with horizontal transfer. *Humanities and Social Sciences Communications* 9.

Nicholls, Geoff K. and Russell D. Gray. 2008. Dated ancestral trees from binary trait data and their application to the diversification of languages. *Journal of the Royal Statistical Society B* 70(3): 545–566.

Pudlo, Pierre, Jean-Michel Marin, Arnaud Estoup, Jean-Marie Cornuet, Mathieu Gautier and Christian P. Robert. 2016. Reliable ABC model choice via random forests. *Bioinformatics* 32(6): 859–866.

Purwa, I Made et al. 1994. *Struktur bahasa Idate*. Jakarta: Pusat Pembinaan dan Pengembangan Bahasa.

Rama, Taraka, Johann-Mattis List, Johannes Wahle and Gerhard Jäger. 2018. Are automatic methods for cognate detection good enough for phylogenetic reconstruction in historical linguistics? *Proceedings of NAACL-HLT 2018*, 393–400.

Ringe, Don, Tandy Warnow and Ann Taylor. 2002. Indo-European and computational cladistics. *Transactions of the Philological Society* 100(1): 59–129.

Robert, Christian P., Jean-Marie Cornuet, Jean-Michel Marin and Natesh S. Pillai. 2011. Lack of confidence in approximate Bayesian computation model choice. *Proceedings of the National Academy of Sciences* 108(37): 15112–15117.

Robinson, Laura C. and Gary Holton. 2012. Internal classification of the Alor-Pantar language family using computational methods applied to the lexicon. *Language Dynamics and Change* 2(2): 123–149.

Ronquist, Fredrik et al. 2012. MrBayes 3.2: efficient Bayesian phylogenetic inference and model choice across a large model space. *Systematic Biology* 61(3): 539–542.

Ross, Malcolm D. 1988. *Proto Oceanic and the Austronesian Languages of Western Melanesia*. Pacific Linguistics C-98. Canberra: Australian National University.

Schapper, Antoinette. 2020. The origins of isolating word structure in eastern Timor. In David Gil and Antoinette Schapper (eds.), *Austronesian Undressed: How and Why Languages Become Isolating*, 391–446. Amsterdam: John Benjamins.

Shimodaira, Hidetoshi. 2002. An approximately unbiased test of phylogenetic tree selection. *Systematic Biology* 51(3): 492–508.

Susko, Edward. 2014. Tests for two trees using likelihood methods. *Molecular Biology and Evolution* 31(4): 1029–1039.

Tadmor, Uri. 2009. Loanwords in the world's languages: findings and results. In Martin Haspelmath and Uri Tadmor (eds.), *Loanwords in the World's Languages: A Comparative Handbook*, 55–75. Berlin: De Gruyter Mouton.

Tadmor, Uri, Martin Haspelmath and Bradley Taylor. 2010. Borrowability and the notion of basic vocabulary. *Diachronica* 27(2): 226–246.

Wichmann, Søren, Eric W. Holman and Cecil H. Brown, eds. *The ASJP Database*, version 21. Lexibank CLDF release.

Williams-van Klinken, Catharina, John Hajek and Rachel Nordlinger. 2002. *Tetun Dili: A Grammar of an East Timorese Language*. Pacific Linguistics 528. Canberra: Australian National University.
:::
