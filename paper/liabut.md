# Introduction

Two classifications of the Austronesian languages of Timor disagree. Hull (1998, 2001) groups them all as *Timoric*, split into *Ramelaic* (Mambae, Kemak, Tokodede and Idalaka, that is Idaté and Lakalei) and *Fabronic* (Tetun, Habun, the Kawaimina languages, Galoli, Wetarese, Dawan and Bekais or Welaun). He proposed that Ramelaic descends from Old Idalaka (as summarised by Albuquerque 2009). Carvalho (2001, cited in Fogaça 2015) proposed the same two-way split. Edwards (2019, 2021) and Grimes and Edwards (2026) instead make *Central Timor* (Mambae, Kemak, Tokodede and Welaun) a separate branch of Malayo-Polynesian, defined by \*ŋ > \*g > k, and place every other Austronesian language of Timor, Idaté and Lakalei included, in *Timor-Babar*, defined by \*p > \*h. Grimes and Edwards do not cite Hull.

The two disagree most sharply on two points. **C1**: does Lakalei-Idate belong with Central Timor, as in Hull, or with Timor-Babar, as in Edwards and Grimes and Edwards? **C2**: is Welaun a dialect of Tetun, as Hull (1998) first had it, or a Central Timor language (Edwards 2019)?

Grimes and Edwards argue from historical phonology, supported by morphosyntax and the lexicon. The only earlier phylogeny covering Timor, Gray, Drummond and Greenhill (2009), includes Tetum, Mambai and Kemak but none of Idaté, Lakalei, Welaun, Habu, Midiki or Helong. This paper asks what the basic vocabulary says, using a pre-registered design in the spirit of Robinson and Holton (2012), who used lexical phylogenetics where sound changes had left the subgrouping of Alor-Pantar unresolved. It then asks how far the lexical signal reflects inheritance rather than contact, and how robust each answer is.

# Data

| Source | Contents | Use |
|-------------|------------------|----------|
| LexiRumah 3.0.1 (Kaiping, Edwards and Klamer 2019) | 70 Timor-region lects, 152 concepts | Main lexical data (D1) |
| ABVD (Greenhill, Blust and Gray 2008) | 30 lects with expert cognate judgements; Proto-Malayo-Polynesian (PMP) forms | Validation (D2); PMP etyma |
| Grimes and Edwards (2026), LaTeX source | 257 comparative tables, 14,401 forms, reflexes marked by the authors | Sound-change atlas and characters |
| ASJP v21 (Wichmann, Holman and Brown) | 40-item lists, including Idaté from Purwa et al. (1994) | Independent check |
| Alcantara (2015) | 184 Idaté forms from fieldwork in Laclubar | Independent check |
| Gray et al. (2009) via phlorest | 998 posterior trees | Comparison |

: Data sources.

Each lect needed at least 100 of the 152 concepts. Forms that look like loans from Indonesian or Portuguese, forms that look like Tetun, and contact sets shared with neighbouring Papuan languages were flagged and screened in sensitivity variants. Idaté, Lakalei, Welaun, Habu, Midiki and Helong are absent from ABVD; this is their first cognate-based phylogenetic placement. Idaté, Welaun, Habu and Helong do have short ASJP lists. The Idaté and Lakalei lists come from surveys by Klamer (2002) and Dawson (2014), not from Edwards or Grimes. Figure 1 shows the 24 lects used in the model-based analyses, one per language.

![The 24 lects used in the Bayesian and maximum-likelihood analyses, one per language. Lakalei-Idate (red) lies between Central Timor (blue) and the Eastern Timor languages of Grimes and Edwards (dark grey); the dashed line is the border between Timor-Leste and Indonesia. Coordinates from LexiRumah; coastlines from Natural Earth.](figures/map.pdf){width=100%}

# Methods

**Pre-registration.** The protocol was frozen and fingerprinted (SHA-256) before any analysis. Ten dated addenda, each pushed to a public repository before the tests it governs, extended it. Everything after the frozen protocol is post hoc and is labelled as such, except two replications in Addendum 9 whose predictions were stated in advance. The pre-registered decision rule required a contested clade to reach 70% bootstrap support in both UPGMA and NJ trees, on the primary data and on two screened variants.

**Cognates.** Automatic cognate detection used LexStat (threshold 0.55) and SCA (0.45) with Infomap clustering in LingPy (List, Greenhill and Gray 2017). Scored against the ABVD expert judgements, LexStat reaches a B-cubed F of 0.81 (precision 0.88, recall 0.75); distances from the automatic cognates match ABVD expert distances at Mantel r = 0.90. A gate of known low-level groups had to be recovered before any contested clade was scored.

**Trees.** Distance trees (UPGMA, NJ) with 1,000 concept bootstraps were built for 30 hypothesis clades. Treelikeness was measured with delta scores and Q-residuals. Bayesian analyses in MrBayes 3.2.7a used 24 lects and 1,353 binary cognate characters (restriction model with gamma rate variation). Each contested clade was run forced and forbidden, and Bayes factors were computed from stepping-stone marginal likelihoods. Maximum-likelihood trees used IQ-TREE 2.3.6 with ultrafast bootstrap.

**Sound changes.** The marked reflexes in Grimes and Edwards's tables were turned into an expert reflex atlas; LexiRumah forms aligned to ABVD PMP forms gave an automatic atlas. The two agree on 94% of tokens (249 of 264). Eight diagnostic changes, later eleven, were coded as binary characters and combined with the lexicon.

**Inheritance and contact.** Each cognate set was classed as a PMP retention or an innovation (the PMP word was replaced). The rule was validated against ABVD's experts and improved (Section 7). On that basis:

1. Exclusive shared innovations were counted, with a control for geographic distance.
2. A triplet site-pattern test, the lexical counterpart of the ABBA-BABA statistic, counts for three groups the concepts on which exactly two share an innovation. The largest count marks the tree pair, and an imbalance between the other two marks contact. It was run separately on the 60 Leipzig-Jakarta concepts (Tadmor 2009) and on the rest, with Welaun's known Tetun contact as a check, and was later calibrated by simulation.
3. A split test asks which member of Lakalei-Idate carries each signal.
4. Approximate Bayesian computation (ABC) estimates the borrowing that each placement of Lakalei-Idate would need.
5. Historical glottometry (Kalyan and François 2018) and strict-clock analyses give a non-tree and a dated view.

**Robustness (Addenda 9 and 10).** Twelve further analyses target the limitations of the first version: multiple-testing correction (Holm 1979; Benjamini and Hochberg 1995), replication with other dialect representatives and with lists independent of Grimes and Edwards, a consensus of five cognate codings, a retention classifier validated against experts, the sound changes scored by parsimony on the rival trees, a simulated null and power analysis for the triplet test, an ABC with borrowing in both directions and random-forest model choice (Pudlo et al. 2016), a correspondence-based loan test, a clock rooted on the outgroup, a check of shared innovations against the Austronesian Comparative Dictionary (Blust, Trussel and Smith), and AU topology tests (Shimodaira 2002) on the independent lists. Analyses are numbered E1 to E36 as in the repository.

# Results: the pre-registered tests

The gate passed under an addendum adopted before any contested clade was scored. Only low-level groups reach the 70% bar in both distance trees: Lakalei-Idate, Kawaimina, Wetar-Atauro, Nuclear Rote, Kisar-Luang and Babar. Hull's Fabronic, Timor-Babar and Eastern Timor score 0 to 3%. Ramelaic reaches 88 to 95% only when Tetun look-alikes are removed, a variant the protocol flagged in advance as confounded, because removing those words removes the evidence Edwards's placement predicts. Mean delta is 0.24 for 37 lects and 0.33 for one lect per language; the most reticulate lects are the contested ones (Welaun, Tokodede, Galoli, Lakalei, Idaté, Habu).

| Bayesian test (24 lects) | ln BF, forced against forbidden | Unconstrained posterior |
|------------------|--------|--------------|
| C1: Hull's Ramelaic | +8.0 | 0.13 as drawn (without Welaun) |
| C2: Central Timor with Welaun | +10.3 | 0.86 |
| Lakalei-Idate + Central Timor with Welaun | | 0.91 |
| Timor-Babar | −7.0 | 0.00 |
| Eastern Timor, with or without Lakalei-Idate | | 0.00 |
| Welaun + Tetun | | 0.00 |

: Bayesian constraint tests and posterior clade probabilities. Stepping-stone runs agree within 0.8 log units; the unconstrained runs converged (split-frequency difference 0.005, minimum ESS 1,074).

The pre-registered decision was **unresolved** for both C1 and C2, because neither contested clade reached the bootstrap bar. The Bayesian analyses, which the rule did not use for the decision, favour Central Timor with Welaun, with Lakalei-Idate as its sister (Figure 2).

![Consensus tree (all compatible splits) of the unconstrained Bayesian analysis, 24 lects and 1,353 cognate characters, drawn as a cladogram and rooted on Lamaholot. Numbers are posterior probabilities; unlabelled nodes exceed 0.99.](figures/tree.pdf){width=78%}

# Results: sound changes and combined evidence

Lakalei-Idate's sound changes resemble Timor-Babar's: it has \*p lenition and \*ŋ > n, and lacks Central Timor's \*ŋ > g/k and \*j > l (Figure 3). Two facts weaken these as diagnostics. Welaun, a Central Timor language on every other count, also has \*p > h; and \*ŋ > n also occurs in Sika, a Flores outgroup. Hull's own Ramelaic evidence, initial \*b- > h, is visible in Grimes and Edwards's tables: Lakalei-Idate shares it with Mambae, Kemak and Tokodede, against Tetun's \*b- > f and Kawaimina's \*b- > w, but Galoli and Ili'uun share it too.

![Eight diagnostic sound changes coded from the reflexes Grimes and Edwards (2026) mark in their comparative tables, for the languages of Timor, Wetar-Atauro and Rote-Meto (Southwest Maluku is omitted here and shown in the repository). Outlined cells rest on fewer than two expert tokens. The last column merges \*b > h and \*b > f, so it is not the same character as Hull's initial \*b- > h.](figures/sounds.pdf){width=80%}

The coded changes do not, in fact, favour Grimes and Edwards's tree. Scored by Fitch parsimony, the eleven characters need 30 steps on the lexical ML tree (Lakalei-Idate beside Central Timor), 30 on the tree constrained to Lakalei-Idate + Eastern Timor, and 29 on a tree constrained to Grimes and Edwards's top split, which costs 12 log-likelihood units in the lexicon. Because Tetun is sister to Lakalei-Idate + Central Timor in the lexical tree, the eastern-looking changes can sit below that group at no extra cost. Pooling expert, automatic and Alcantara tokens also shows how thin some cells are: Idaté's \*j > r rests on 5 of 12 tokens, and both members have \*d > r, l, a Central Timor change, in 8 of 9 and 5 of 7 tokens (mostly automatic).

| Analysis (24 lects) | Lakalei-Idate + Central Timor | Timor-Babar |
|------------------------|----------|------|
| Vocabulary only, ML (UFBoot %) | 65 | 0 |
| Vocabulary + 17 sound-change characters, ML | 56 | 0 |
| Vocabulary + 8 diagnostic changes, ML | 80 | 0 |
| Vocabulary + 11 changes (with Hull's \*b, \*k), ML | 75 | 0 |
| Vocabulary + 17 characters, Bayesian posterior | 0.88 | 0.00 |
| Vocabulary without 21 probable Tetun loans, ML | 57 | 0 |

: Combined analyses.

Support depends on how cognates are coded, a check modelled on Kaiping and Klamer (2022). Lakalei-Idate + Central Timor gets 92% with SCA cognates and 65% with the primary coding, but 15 to 20% at LexStat thresholds of 0.35 and 0.75; at those thresholds Lakalei-Idate still groups with Mambae, Kemak and Tokodede, alone or with Tetun and Habu added. LexiRumah's own published cognates put it with neighbouring Habu (51%); that coding fits the expert judgements worst (Mantel r 0.70) and does not recover Central Timor. Timor-Babar receives no support under any of the five codings.

# Results: inheritance or contact for Lakalei-Idate

**Shared innovations.** Lakalei-Idate shares 7 exclusive innovations with Central Timor (among them 'cry' *sɛro*, against *tanis* < \*taŋis almost everywhere else) and 9 with the Eastern Timor groups combined. One of the seven, 'wife' (Idaté *mahinɑn*, Mambae *hinɛ*), continues PAN \*b<in>ahi 'woman, wife' according to the Austronesian Comparative Dictionary, so it is a shared retention.

**Triplet test.** On stable concepts, Lakalei-Idate + Nuclear Central Timor (Mambae, Kemak, Tokodede) is the largest pair against every other group tested with the representative lists (Figure 4), though not against Tetun Dili (Section 7). The test recovers Welaun's Tetun contact, and places it where contact should be: in borrowable vocabulary (Z = 6.9), not in stable vocabulary (Z = 0.6). The first version also read Lakalei-Idate's extra sharing with Tetun, Habu and Kawaimina as possible contact. Calibration withdraws that reading. With the tree's unequal branch lengths and no borrowing at all, simulation gives D values centred on 0.44 to 0.47 for these triplets, and every observed value (0.12 to 0.65) lies inside that null; the jackknife rule (Z ≥ 2) fires in 27% of contact-free simulations. Welaun's borrowable-word Z exceeds 99.8% of the null. Once calibrated, the test has a 5% false-positive rate but detects 20% borrowing from Habu only 30% of the time.

![Triplet counts on stable (Leipzig-Jakarta) and borrowable concepts. Each bar is one triplet of the focal group (Welaun or Lakalei-Idate), Nuclear Central Timor (Mambae, Kemak and Tokodede) and a third group; the numbers count concepts on which exactly that pair shares an innovation. Welaun, whose Tetun contact is documented, is the control. Against a simulated null with unequal rates, only Welaun's excess in borrowable words stands out.](figures/triplets.pdf){width=100%}

**Which half carries the signal.** In stable vocabulary, five of the eight Central Timor items are shared by both Idaté and Lakalei, so they predate the split between them. In borrowable vocabulary, six of eight are found only in Lakalei and match Mambae, spoken 10 km away ('cloud' *sabai*, 'neck', 'eat' *mia* ~ *mua*). The counts are small (binomial p = 0.11), and a correspondence test finds these items no closer to identity than inherited words, so the recent-loan reading is not confirmed.

**How much borrowing each placement needs.**

| ABC, 20,000 runs per model | Sister to Central Timor | Within Eastern Timor |
|----------|-----------|-----------|
| One-way borrowing (E21): posterior | 0.125 | 0.875 |
| One-way: borrowing needed, stable, median (90%) | 16% (1–41%) from the east | 28% (4–53%) from Central Timor |
| Two-way borrowing (E32): random-forest votes | 0.45 | 0.55 |
| Two-way: rejection posterior | 0.42 | 0.58 |
| Two-way: Central Timor borrowing, stable | 24% (4–52%) | 25% (4–55%) |
| Two-way: posterior predictive checks failed (of 36) | 0 | 0 |

: Approximate Bayesian computation. The one-way models allow borrowing from the other side only; the two-way models allow it from both, with 36 summary statistics. Random-forest prior error for the two-way models: 36%.

The first simulation preferred Grimes and Edwards's placement, but only with each model borrowing from one side. Allowing borrowing in both directions removes the preference: neither placement reaches the 0.9 bar, both reproduce every summary statistic, and the random forest misclassifies 36% of its own simulations. The summary counts cannot separate descent from borrowing here. On the full lexical likelihood, the unconstrained tree is better than the constrained one by 10.5 log units, although an AU test does not reject the constrained tree on these lists (p = 0.07); on lists independent of Grimes and Edwards it does (Section 7).

**Glottometry and dating.** Glottometry finds cohesive groups only at low levels. Lakalei-Idate is cohesive on its own (subgroupiness 1.42) and tied almost equally weakly to Central Timor (0.06) and to Eastern Timor (0.08); Hull's Ramelaic scores 0. Under a strict clock rooted on the Flores outgroup, about 77% of posterior samples place Lakalei-Idate with Central Timor (Habu 11%), and their split (relative height 0.48) is barely older than Central Timor's own diversification (0.47); the earlier run, whose clock put the root on Tela-Masbuar, gave the same picture (80%; 0.29 against 0.27). A contact-aware phylogeny (contacTrees; Neureiter et al. 2022) did not reach a stable solution: it kept adding contact edges, each moving 14 to 23% of the vocabulary, so it is not reported further.

# Robustness and replication

| Limitation of the first version | Check (Addendum 9) | Outcome |
|---------|-------------|-------------|
| About twenty post hoc tests, uncorrected | Holm and Benjamini–Hochberg over 40 tests (E25) | Only Welaun's Tetun contact survives |
| Results could hinge on the chosen dialect lists | Every combination of 11 Mambae, 8 Kemak, 2 Idaté and 2 Tetun lists, predictions stated in advance (E26) | Stable-vocabulary pairing with Central Timor holds against Habu and Kawaimina (100%) but not Tetun (47%, failing on Tetun Dili) |
| LexiRumah shares sources and an editor with Grimes and Edwards | Lists collected by others only, predictions stated in advance (E28) | Lakalei-Idate + Nuclear Central Timor 97%; Timor-Babar and Lakalei-Idate + Eastern Timor 0%; not a same-collector effect; stable pairing fails narrowly against Tetun (45 to 44) |
| Automatic cognates; coding dependence | Consensus of five codings (E27); reviewer packet | Timor-Babar and Lakalei-Idate + Eastern Timor 0%; Lakalei-Idate + Nuclear Central Timor 55% |
| Retention classifier misclasses changed retentions | Validated on 3,801 expert-judged forms; reflex-aware rule (E30) | Balanced accuracy 0.755 → 0.791; main patterns unchanged |
| Triplet test assumes equal rates | Simulated null and power (E31) | Contact readings for Lakalei-Idate withdrawn; Welaun's stands |
| Borrowing simulation one-directional, 18 counts | Two-way ABC, 36 statistics, random forests, predictive checks (E32) | Placements indistinguishable |
| Sound changes taken as pointing east | Parsimony on rival trees; token intervals (E29) | 30 steps on either placement |
| Comparative method not applied | Identity of aligned forms against inherited baseline (E33) | No loan signal; low power |
| Clock rooted on a long, sparse branch | Root constrained to the outgroup (E34) | Same picture: 77% Central Timor side |
| Innovations judged against ABVD's PMP forms only | Etyma from PAN to PCMP in the Austronesian Comparative Dictionary added (E35) | Stable pairing with Central Timor stands, against Tetun too; 6 of the 24 decisive sets are inherited |
| Lexical preference not tested for significance | AU tests on the independent lists (E36) | Lakalei-Idate + Eastern Timor rejected (p = 0.025); Timor-Babar rejected (p = 0.042) |

: What Addenda 9 and 10 checked, and what came out.

The two confirmatory replications give a mixed but informative result. Lists independent of Grimes and Edwards strengthen the tree placement of Lakalei-Idate beside Mambae, Kemak and Tokodede (97%), and in that tree Lakalei falls inside Nuclear Central Timor (94%) while Idaté-Cribas stays outside. Adding Klamer's other 2002 lists shows this is not a collector effect: his Tetun Dili list joins Tetun Suai (100%), not his Mambae and Kemak lists. The stable-vocabulary pairing replicates against Habu and Kawaimina in every combination and on the independent lists, but against Tetun only with Tetun Suai: with Tetun Dili, the lingua franca, Lakalei-Idate + Tetun is the larger pair in 84% of combinations, and with the two Tetun lists pooled it wins by one concept (45 to 44). Part of this is the classifier: with the validated rule, Lakalei-Idate + Nuclear Central Timor beats Lakalei-Idate + Tetun on the pooled lists (36 to 29), and the share of combinations rises from 47% to 79%.

Two final checks bear on the same question. Taking out words that the Austronesian Comparative Dictionary traces to PAN, PMP, PCEMP or PCMP removes 55 sets from the innovation counts under a strict gloss match (126 under the looser rule declared in advance), and the stable pairing with Central Timor survives both, now against Tetun as well (19 to 9 on the representative lists). And on the independent lists, an AU test rejects both Lakalei-Idate + Eastern Timor (ΔlnL 19.5, p = 0.025) and Timor-Babar (ΔlnL 14.8, p = 0.042) as lexical groups, which the original lists did not (p = 0.07).

# Results: other disputed branches

| Triplet | Counts, all concepts (stable) | Reading |
|-------|------------------|----------|
| Habu, Tetun, Kawaimina | Habu+Tetun 15 (5); Habu+Kawaimina 11 (5); Tetun+Kawaimina 4 (2) | Unresolved; the Tetun link is in borrowable words |
| Waima'a, Naueti, Midiki | Waima'a+Naueti 10 (7); Waima'a+Midiki 7 (4); Naueti+Midiki 2 (1) | Leans towards Grimes and Edwards's Waima'a-Naueti |
| Galoli, Wetar, Dadu'a | Galoli+Dadu'a 20 (13); Galoli+Wetar 6 (2); Wetar+Dadu'a 6 (4) | Galoli pairs with Dadu'a, not with the Wetar lects |
| Galoli, Wetar, Tetun | Galoli+Wetar 12 (8); Galoli+Tetun 6 (4); Wetar+Tetun 0 (0) | Galoli belongs with Wetar-Atauro, with a Tetun layer |
| Helong, Meto, Rote | Meto+Rote 17 (12); Helong+Meto 10 (8); Helong+Rote 3 (2) | Rote-Meto holds; Helong outside it |

: Triplet tests on other disputed placements. The tree pairs are robust to the classifier change; none of the contact excesses survives multiple-testing correction.

# Discussion

**What the vocabulary shows.** There is no lexical support for Hull's Fabronic, for Timor-Babar or for Eastern Timor, under every coding, with an improved classifier and with lists independent of Grimes and Edwards. This does not refute Timor-Babar, which Grimes and Edwards define by sound changes rather than by shared vocabulary; it means that, if Timor-Babar is a subgroup, its lexicon has since been reshaped by contact. Welaun belongs with Central Timor, and its Tetun appearance sits in borrowable vocabulary, in agreement with Edwards (2019); that contact is the one signal that passes every check. The low-level groups hold, and Galoli pairs with Dadu'a.

**Lakalei-Idate remains unresolved, but the balance has moved.** Every tree places it beside Mambae, Kemak and Tokodede, now also on lists collected independently of Grimes and Edwards (97%), where an AU test rejects the eastern placement (p = 0.025). The two arguments that seemed to favour the eastern placement no longer discriminate: the coded sound changes cost the same on either tree, and the borrowing simulation cannot separate the placements once borrowing runs both ways. The contact readings in the other direction have weakened too, since none of Lakalei-Idate's eastern excesses stands out once unequal rates are modelled. What remains against the Central Timor placement is the qualitative weight Grimes and Edwards give to \*p and \*ŋ as innovations, and the pull of Tetun Dili on stable vocabulary. The reading that fits most of the evidence is an old, conservative member of a central Timor dialect chain, close to Hull's Ramelaic, which broke away about when Central Timor itself diversified and kept ties to the east.

**What would settle it.** A specialist's review of the 24 cognate sets behind Lakalei-Idate's stable-vocabulary signal (the packet is in the repository); Grimes and Edwards's 494-item field lists for Idaté and Lakalei, which are not public; Alcantara's full 800-word Idaté corpus; and a full regular-correspondence analysis of complete wordlists, which these short lists cannot support.

# Limitations

Apart from two replications with predictions stated in advance, the analyses after the frozen protocol are post hoc; after correction, only Welaun's Tetun contact is statistically secure. The confirmatory predictions failed against Tetun in both replications. The cognates are automatic and have not been checked by a specialist; a consensus of five codings and a validated classifier reduce, but do not remove, that dependence, and the strict consensus favours recent loans. LexiRumah is still a single compilation, although its Idaté, Lakalei and replacement Central Timor lists come from collectors other than Edwards and Grimes. Some sound-change cells for Idaté and Lakalei rest on a handful of tokens. The calibrated triplet test has low power, so not detecting contact is weak evidence against it; the ABC cannot separate the placements; the correspondence test is underpowered. The Austronesian Comparative Dictionary lists few forms for most Timor languages, so the etymological check works mainly through reconstructed etyma, and its looser declared version produced false matches. Hull (1998) and Carvalho (2001) could not be obtained and are cited from secondary sources.

# Data and code {.unnumbered}

All data, code, results, the protocol and its addenda are at <https://github.com/DenC-dev/liabut>. The numbered scripts in `src/` rerun every analysis from pinned upstream data. The derived datasets (Grimes and Edwards's tables as data, expert and automatic reflex atlases, sound-change matrices, loan classifications, the Alcantara Idaté list, the retention or innovation status of every cognate set, and the specialist review packet) are in `derived/`. Code is MIT-licensed; data keep their sources' licences.

# Use of AI {.unnumbered}

The code, the analyses and the drafting of this paper were carried out with substantial assistance from Claude (Anthropic), an AI system, under the author's direction. Every analysis, decision and correction is recorded in the public repository so that it can be checked.

# References {.unnumbered}

::: {.refs}
Albuquerque, Davi Borges de. 2009. Pré-história, história e contatos lingüísticos em Timor Leste. *Domínios de Lingu@gem* 3(2): 75–93.

Alcantara, Maressa Xavier. 2015. *Descrição fonética e fonológica da língua idaté do Timor Leste*. MA thesis, Universidade de São Paulo.

Benjamini, Yoav and Yosef Hochberg. 1995. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society B* 57(1): 289–300.

Blust, Robert, Stephen Trussel and Alexander D. Smith. *The Austronesian Comparative Dictionary*. CLDF release, lexibank/acd (commit 16085f2).

Dawson, Virginia. 2014. Manatuto survey word lists. PARADISEC collection VD1. In Kaiping, Edwards and Klamer (2019).

Edwards, Owen. 2019. Reintroducing Welaun. *Oceanic Linguistics* 58(1): 31–58.

Edwards, Owen. 2021. *Rote-Meto Comparative Dictionary*. Canberra: ANU Press.

Fogaça, Jessé Silveira. 2015. *Aspectos gramaticais da língua Makasae de Timor-Leste*. PhD thesis, Universidade de Brasília.

Gray, Russell D., Alexei J. Drummond and Simon J. Greenhill. 2009. Language phylogenies reveal expansion pulses and pauses in Pacific settlement. *Science* 323: 479–483.

Greenhill, Simon J., Robert Blust and Russell D. Gray. 2008. The Austronesian Basic Vocabulary Database. *Evolutionary Bioinformatics* 4: 271–283.

Grimes, Charles E. and Owen Edwards. 2026. *The Austronesian languages of eastern Indonesia and Timor-Leste: Unravelling their prehistory and classification*. Berlin: Language Science Press.

Holm, Sture. 1979. A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2): 65–70.

Hull, Geoffrey. 1998. The basic lexical affinities of Timor's Austronesian languages: a preliminary investigation. *Studies in Languages and Cultures of East Timor* 1: 97–202.

Hull, Geoffrey. 2001. O mapa linguístico de Timor Leste: uma orientação dialectológica. *Studies in Languages and Cultures of East Timor* 4: 1–19.

Kaiping, Gereon A. and Marian Klamer. 2022. The dialect chain of the Timor-Alor-Pantar language family: a new analysis using systematic Bayesian phylogenetics. *Language Dynamics and Change* 12(2): 274–326.

Kaiping, Gereon A., Owen Edwards and Marian Klamer, eds. 2019. *LexiRumah* 3.0. Leiden University Centre for Linguistics.

Kalyan, Siva and Alexandre François. 2018. Freeing the comparative method from the tree model: a framework for historical glottometry. *Senri Ethnological Studies* 98: 59–89.

Klamer, Marian. 2002. Timor-Leste survey word lists. In Kaiping, Edwards and Klamer (2019).

List, Johann-Mattis, Simon J. Greenhill and Russell D. Gray. 2017. The potential of automatic word comparison for historical linguistics. *PLOS ONE* 12(1): e0170046.

Neureiter, Nico et al. 2022. Detecting contact in language trees: a Bayesian phylogenetic model with horizontal transfer. *Humanities and Social Sciences Communications* 9.

Pudlo, Pierre, Jean-Michel Marin, Arnaud Estoup, Jean-Marie Cornuet, Mathieu Gautier and Christian P. Robert. 2016. Reliable ABC model choice via random forests. *Bioinformatics* 32(6): 859–866.

Purwa, I Made et al. 1994. *Struktur bahasa Idate*. Jakarta: Pusat Pembinaan dan Pengembangan Bahasa.

Robinson, Laura C. and Gary Holton. 2012. Internal classification of the Alor-Pantar language family using computational methods applied to the lexicon. *Language Dynamics and Change* 2(2): 123–149.

Shimodaira, Hidetoshi. 2002. An approximately unbiased test of phylogenetic tree selection. *Systematic Biology* 51(3): 492–508.

Tadmor, Uri. 2009. Loanwords in the world's languages: findings and results. In Martin Haspelmath and Uri Tadmor (eds.), *Loanwords in the World's Languages: A Comparative Handbook*, 55–75. Berlin: De Gruyter Mouton.

Wichmann, Søren, Eric W. Holman and Cecil H. Brown, eds. *The ASJP Database*, version 21. Lexibank CLDF release.
:::
