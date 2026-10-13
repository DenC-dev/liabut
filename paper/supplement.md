# Register of analyses

The main text reports the pre-registered tests, the replications, the primary analysis and six robustness checks. This Supplement reports the other analyses that bear on the two questions. Every analysis, including those not discussed here, has its script, declaration and result file in the repository; `results/LITERATURE.md` describes each in turn, and `PROTOCOL.md` holds the declarations. Analyses are numbered as there.

| Analyses | Addendum | Class | What they do | Reported |
|------|----|------|------------------|------|
| Steps 1 to 8 | Protocol | Pre-registered | Distance trees, the gate, Bayesian trees, the decision | Main text |
| E1 to E6 | 3 | Exploratory | Stable against borrowable concepts; \*p retention; geography; AU tests | S2, S5 |
| E7 to E12 | 4 | Exploratory | Grimes and Edwards's tables as data; reflex atlases; total-evidence trees; Tetun loans | S7; repository |
| E13 to E16 | 5, 6 | Exploratory | Hull's \*b and \*k; an ASJP check; cognate-coding robustness; Alcantara's Idaté data | S3; repository |
| E17 to E24 | 7, 8 | Exploratory | Shared innovations; triplet tests; contact-aware trees; the split test; borrowing simulation; glottometry; dating; other branches | S6, S8, S9, S10 |
| E25 to E34 | 9 | Two confirmatory (E26, E28), the rest exploratory | Multiple testing; replications; consensus cognates; sound changes on rival trees; classifier validation; triplet null and power; two-way borrowing model; correspondences; rooted clock | Main text; S4, S6, S7, S8 |
| E35, E36 | 10 | Exploratory | Etymological check; AU tests on independent lists | Main text; S5 |
| E37 to E39 | 11 | Exploratory | Grimes and Edwards's own judgements; parametric bootstrap; capped contact model | Main text; S8 |
| E40 to E50 | 12 | Second round (E40, E44, E45, E46 under the rule); the rest exploratory | Root; relaxed clock; irreversible sound changes; calibration; kept together; rooted AU tests; cleaned innovations; direct Bayes factors; other taxon sets; heights; glottometry intervals | Main text; S2, S4, S5, S7, S9 |
| E51 to E55 | 13 | Exploratory | Partial cognates; regular correspondences; fuller phonology; learned classifier; split networks | Main text; S3, S6, S7, S8 |
| E56, E57 | 14 | Exploratory, requested in review | Reversibility of sound change; root sensitivity | Main text |

: Register of analyses.

# Unrooted Bayesian trees and Bayes factors

| Unconstrained MrBayes, 24 lects (unrooted) | Posterior |
|------------------------------|------|
| Lakalei-Idate + Central Timor (with Welaun) | 0.91 |
| Central Timor with Welaun | 0.86 |
| Flores pair + Rote-Meto + Helong | 0.95 |
| Lakalei-Idate | 0.94 |
| Hull's Ramelaic (without Welaun) | 0.13 |
| Timor-Babar; Eastern Timor, with or without Lakalei-Idate; Welaun + Tetun | 0.00 |

: Unrooted Bayesian results (step 7). The runs converged (split-frequency difference 0.005, minimum ESS 1,074).

The unrooted trees put Lakalei-Idate beside Central Timor and never with Eastern Timor, Hull's Fabronic or Timor-Babar. The two Flores-Lembata lects, which step 7 used to root the tree, do not sit outside Timor: they attach to Rote-Meto + Helong (0.95). That is why the second round estimated the root with outgroups beyond Flores.

The protocol's Bayes factors compare a clade forced against the same clade forbidden. Such a factor equals the posterior odds over the prior odds, and any particular group of five or six lects has a tiny prior probability, so modest posteriors give large factors (Bergsten, Nilsson and Ronquist 2013): Ramelaic, at 0.13, gets ln BF +8.0, Central Timor with Welaun +10.3 and Timor-Babar −7.0. The direct comparisons in the main text (E47; +11.8 and +7.6) avoid that problem. Stepping-stone runs agree within 0.8 log units.

# Other codings and taxon sets

| UFBoot % | With Central Timor | With Nuclear Central Timor | With Eastern Timor | With Habu |
|--------------------------|-----|-----|-----|-----|
| Independent lists, Idaté alone | 79 | 79 | 7 | 13 |
| Independent lists, Lakalei alone | 99 | 99 | 0 | 0 |
| SCA cognates (E15) | 92 | | | |
| LexStat at thresholds 0.35 and 0.75 (E15) | 15, 20 | | | |
| Partial cognates, unconstrained (E51) | 23 | 65 | 0 | 10 |

: Placement of Lakalei-Idate under other codings and list sets, beyond the main text's Table 6.

Coding cognates by morpheme (E51) merges compounds the whole-word coding split: the two 'wife' sets share a morpheme set, and 16 of the 18 flagged decisive sets share one with at least one other full-word set. It moves support from Central Timor as a whole to Mambae, Kemak and Tokodede. A learned retention classifier (E54; gradient boosting on eight features, grouped cross-validation) reached a balanced accuracy of 0.788 against 0.791 for the reflex-aware rule, so the rule was kept.

# Topology tests

| Constrained tree | Data | ΔlnL | p (AU) | Holm, all eleven |
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

: All eleven AU tests (Shimodaira 2002), 10,000 RELL replicates. In E45 every tree keeps Lakalei-Idate together and the seven outgroups hold the root.

E36's rejection of the eastern placement on the independent lists (uncorrected p = 0.025) depended on letting Lakalei fall inside Nuclear Central Timor; with the pair kept together (E45) it is no longer rejected even uncorrected (p = 0.07). The parametric bootstrap (E38), with Lakalei-Idate free to split, gives p = 0.01 on both list sets: none of 100 simulated differences reached the observed ones (10.5 and 19.4 log units, against at most 3.2 and 4.8).

# Calibration

**Known groups (E43).** Of the ten Grimes and Edwards groups with at least two lects among the 24, other than the contested ones, the unrooted MrBayes tree recovers six at posterior 0.95 and the ML tree four at UFBoot 95. The failures include groups nobody disputes: West Rote-Meto (Dela + Meto: posterior 0.00, UFBoot 3), Kisar-Luang (0.00, UFBoot 2; Luang pairs with Tela-Masbuar instead), Tetun + Habu (0.00) and, narrowly, Lakalei-Idate itself (0.94, UFBoot 53). In the pre-registered distance trees Southwest Maluku gets 0% and 30%.

**The triplet test (E31).** With unequal branch lengths and no borrowing, the null D for Lakalei-Idate's triplets centres on 0.44 to 0.47; every observed value lies inside it, and the naive Z ≥ 2 rule fires in 27% of contact-free datasets. The calibrated test has a 5% false-positive rate and detects 20% borrowing from Habu 30% of the time.

**Treelikeness.** The protocol reports tree results as weak when mean delta (Holland et al. 2002; Gray, Bryant and Greenhill 2010) exceeds 0.3. For the 24 lects it is 0.33. The most reticulate lects are Welaun, Tokodede, Galoli, Lakalei, Tetun Dili and Idaté, followed by Habu and Tetun Suai.

# Shared innovations: other counts

| Stable concepts | LI + NCT | LI + X | NCT + X |
|-----------------------------|-----|-----|-----|
| Single-survey lists, cleaned and polarised: Tetun, Habu, Kawaimina | 12, 10, 30 | 10, 9, 18 | 2, 0, 0 |
| Polarised by all nine outgroups, representative: Tetun, Habu, Kawaimina | 23, 21, 69 | 14, 21, 38 | 5, 5, 9 |
| Partial cognates, polarised, not cleaned (E51): Tetun, Habu, Kawaimina | 10, 13, 48 | 18, 14, 24 | 3, 1, 6 |

: Other triplet counts on stable concepts (E46, E51).

On the single-survey lists Nuclear Central Timor + Tetun matches or beats Lakalei-Idate + Nuclear Central Timor until the counts are polarised. In the two halves of Lakalei-Idate, five of the eight stable Central Timor items are shared by both Idaté and Lakalei, while six of eight borrowable ones are found only in Lakalei and match Mambae, spoken 10 km away (binomial p = 0.125); with the other Idaté list the stable split becomes 3 shared, 4 in Lakalei only and 2 in Idaté only.

![Triplet counts on stable (Leipzig-Jakarta) and borrowable concepts, with the original retention rule, representative lists. Each bar is one triplet of the focal group (Welaun or Lakalei-Idate), Nuclear Central Timor and a third group. Welaun, whose Tetun contact is documented, is the control: against a simulated null with unequal rates, only its jackknife Z in borrowable words stands out.](figures/triplets.pdf){width=100%}

# Sound changes

| Steps on each tree, rooted on Flores | Lexical tree (H) | Lakalei-Idate + Eastern Timor (G) | Grimes and Edwards's split (GE) |
|-------------------------------|-----|-----|-----|
| \*p lenition, Fitch | 2 | 2 | 2 |
| \*p lenition, Camin-Sokal | 6 | 4 | 2 |
| \*p lenition, Dollo | 2 | 2 | 2 |
| All eleven, Fitch | 33 | 34 | 32 |
| All eleven, Camin-Sokal | 49 | 47 | 51 |
| All eleven, Dollo | 54 | 49 | 43 |
| Lexical log-likelihood, relative to H | 0 | −10.5 | −12.0 |

: The eleven sound-change characters on the rival trees (E42), with the root state free (Fitch) or fixed (Camin-Sokal, Dollo).

Several changes recur outside their defining groups: \*ŋ > n throughout Timor-Babar and in Sika; \*d > r, l in Sika and Dela; \*p > h in Welaun; Hull's initial \*b- > h in Galoli and Ili'uun. Lakalei-Idate also lacks Central Timor's \*ŋ > g (\*taliŋa 'ear' > Idaté *talina*, Mambae *teliga*) and has \*ma-p > b where Central Timor has \*mp. Lacking Central Timor's change fits both trees if Lakalei-Idate branched off before Central Timor made it.

**A fuller phonology (E53).** Every non-retention reflex class in the expert atlas, kept if at least two of the 24 lects have it and two lack it, gives 36 characters. Under Camin-Sokal, G beats H on 6 characters to 0 (sign test p = 0.03), but all six are changes Tetun shares with Kawaimina and, where it is coded, Habu, and only two involve Lakalei-Idate; GE ties H. A Bayesian tree from these characters alone (binary Mk, coding=variable) recovers Lakalei-Idate (0.81) but neither of its placements, nor Timor-Babar (0.00 each). Combining sound-change characters with the lexical matrix at equal weight cannot show agreement, because the phonology is about 1% of such a matrix (on weighting character types, see Ringe, Warnow and Taylor 2002); a likelihood treatment of irreversible change, such as the stochastic Dollo model (Nicholls and Gray 2008), would need far more characters.

# Contact and linkage models

**Borrowing simulations (E21, E32).** Approximate Bayesian computation (Csilléry et al. 2010) with borrowing from both sides into proto-Lakalei-Idate cannot separate the placements: the random forest (Pudlo et al. 2016) splits its votes 0.45 to 0.55 and misclassifies 36% of its own simulations, and the four stable-vocabulary borrowing parameters end with posterior medians of 22 to 25% and 90% intervals of about 2 to 57%, close to their U(0, 0.6) prior. The design's statistics are a handful of counts (Robert et al. 2011), and its simulator moves both Lakalei-Idate lects together, so it cannot represent Idaté's and Lakalei's different neighbours.

**Glottometry (E22, E50).** Historical glottometry (Kalyan and François 2018) finds cohesive groups only at low levels. With 95% intervals from resampling concepts, Lakalei-Idate's subgroupiness is 1.42 (0 to 3.65), its ties to Central Timor 0.06 (0 to 0.31) and to Eastern Timor 0.08 (0 to 0.41), and Hull's Ramelaic 0 in every resample.

**A contact-aware tree (E19, E39).** contacTrees (Neureiter et al. 2022) did not settle when left free. Capped at five transfer edges, it used all five in every sample, some between unlikely partners (Dela and Habu in 99% of samples). Its base tree puts Lakalei-Idate with Tetun and Habu (0.78), with a transfer edge between Lakalei and Tokodede in every sample. Because the model always uses the maximum number of edges it is misspecified, and its base tree should not be read as the history; it shows only that a few transfer events can carry the Central Timor signal as well as descent can.

**A split network (E55).** NeighborNet (Bryant and Moulton 2004) on the primary distances, with 200 concept bootstraps, shows Lakalei-Idate as a split in 89% of networks, Lakalei-Idate + Central Timor in 47%, Idaté + Habu in 45%, Lakalei + Nuclear Central Timor in 30%, and Lakalei-Idate + Eastern Timor in 2%. By the reading declared in advance this is "unclear": a linkage signature needed both sides in at least half of the networks.

**Correspondences (E33, E52).** Neither test can tell loans from inheritance in these lists. E33 finds the Lakalei items no closer to identity than inherited words. E52 found 0 to 2 regular non-identity correspondences per lect pair, from baselines of 24 to 30 shared retentions; of 18 decisive sets on each side, 5 were informative on the Central Timor side and 5 on the eastern side, splitting evenly between loan-like and inherited-like (Fisher p = 1.0 on both sides).

# Dating

Measured only in samples where both groups are clades (E49), the common ancestor of Lakalei-Idate and Central Timor is older than Central Timor's own by a median of 21% of the latter's height under the relaxed clock (95%: 4 to 71%), where Central Timor with Welaun is a clade in 72% of samples. Under the strict clock (E34), where both Nuclear Central Timor and Lakalei-Idate + Nuclear Central Timor are clades (49% of samples), the second is older by a median of 21% of the first's height (95%: 7 to 39%). Dropping Tela-Masbuar moves the relaxed clock's root mass from Kisar-Luang towards the western branches (E41).

# Welaun (C2)

On the 60 stable concepts Welaun + Tetun gets 2% (UPGMA) and 4% (NJ), on the other 92 concepts 74% and 81% (E1), and the triplet test locates the excess there (Z = 6.9 against 0.6). Under the consensus coding the Welaun control's tree pair becomes Welaun + Tetun even on stable concepts (10 to 8). Under the strict clock (E34) Central Timor with Welaun has posterior 0.29. Hull (2003) called Bekais a distinct language "structurally intermediate between Belunese Tetum and Dawan".

# Other disputed branches

| Triplet | Counts, all concepts (stable) | Reading |
|-------|------------------|----------|
| Habu, Tetun, Kawaimina | Habu+Tetun 15 (5); Habu+Kawaimina 11 (5); Tetun+Kawaimina 4 (2) | Unresolved |
| Waima'a, Naueti, Midiki | Waima'a+Naueti 10 (7); Waima'a+Midiki 7 (4); Naueti+Midiki 2 (1) | Waima'a+Naueti largest, as in Grimes and Edwards |
| Galoli, Wetar, Dadu'a | Galoli+Dadu'a 20 (13); Galoli+Wetar 6 (2); Wetar+Dadu'a 6 (4) | Galoli+Dadu'a largest |
| Galoli, Wetar, Tetun | Galoli+Wetar 12 (8); Galoli+Tetun 6 (4); Wetar+Tetun 0 (0) | Galoli+Wetar largest |
| Helong, Meto, Rote | Meto+Rote 17 (12); Helong+Meto 10 (8); Helong+Rote 3 (2) | Meto+Rote largest |

: Triplet tests on other disputed placements (E24). The imbalances between the other two pairs are uncalibrated for these triplets and none survives multiple-testing correction, so they are not read as contact.

# References {.unnumbered}

::: {.refs}
Bergsten, Johannes, Anders N. Nilsson and Fredrik Ronquist. 2013. Bayesian tests of topology hypotheses with an example from diving beetles. *Systematic Biology* 62(5): 660–673.

Bryant, David and Vincent Moulton. 2004. Neighbor-Net: an agglomerative method for the construction of phylogenetic networks. *Molecular Biology and Evolution* 21(2): 255–265.

Csilléry, Katalin, Michael G. B. Blum, Oscar E. Gaggiotti and Olivier François. 2010. Approximate Bayesian computation (ABC) in practice. *Trends in Ecology and Evolution* 25(7): 410–418.

Gray, Russell D., David Bryant and Simon J. Greenhill. 2010. On the shape and fabric of human history. *Philosophical Transactions of the Royal Society B* 365: 3923–3933.

Holland, Barbara R., Katharina T. Huber, Andreas Dress and Vincent Moulton. 2002. δ plots: a tool for analyzing phylogenetic distance data. *Molecular Biology and Evolution* 19(12): 2051–2059.

Hull, Geoffrey. 2003. Lia-Bekais nia fatin iha dalen-lubun Timór. *Studies in Languages and Cultures of East Timor* 5: 55–78.

Kalyan, Siva and Alexandre François. 2018. Freeing the comparative method from the tree model: a framework for historical glottometry. *Senri Ethnological Studies* 98: 59–89.

Neureiter, Nico et al. 2022. Detecting contact in language trees: a Bayesian phylogenetic model with horizontal transfer. *Humanities and Social Sciences Communications* 9.

Nicholls, Geoff K. and Russell D. Gray. 2008. Dated ancestral trees from binary trait data and their application to the diversification of languages. *Journal of the Royal Statistical Society B* 70(3): 545–566.

Pudlo, Pierre, Jean-Michel Marin, Arnaud Estoup, Jean-Marie Cornuet, Mathieu Gautier and Christian P. Robert. 2016. Reliable ABC model choice via random forests. *Bioinformatics* 32(6): 859–866.

Ringe, Don, Tandy Warnow and Ann Taylor. 2002. Indo-European and computational cladistics. *Transactions of the Philological Society* 100(1): 59–129.

Robert, Christian P., Jean-Marie Cornuet, Jean-Michel Marin and Natesh S. Pillai. 2011. Lack of confidence in approximate Bayesian computation model choice. *Proceedings of the National Academy of Sciences* 108(37): 15112–15117.

Shimodaira, Hidetoshi. 2002. An approximately unbiased test of phylogenetic tree selection. *Systematic Biology* 51(3): 492–508.
:::
