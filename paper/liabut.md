# Introduction

Two classifications of the Austronesian languages of Timor disagree. Hull (1998, 2001) groups them all as *Timoric*, split into *Ramelaic* (Mambae, Kemak, Tokodede and Idalaka, that is Idaté and Lakalei) and *Fabronic* (Tetun, Habun, the Kawaimina languages, Galoli, Wetarese, Dawan and Bekais or Welaun). He proposed that Ramelaic descends from Old Idalaka (as summarised by Albuquerque 2009). Carvalho (2001, cited in Fogaça 2015) proposed the same two-way split. Edwards (2019) and Grimes and Edwards (2026) instead make *Central Timor* (Mambae, Kemak, Tokodede and Welaun) a separate branch of Malayo-Polynesian, defined by \*ŋ > \*g > k, and place every other Austronesian language of Timor, Idaté and Lakalei included, in *Timor-Babar*, defined by \*p > \*h. Grimes and Edwards do not cite Hull.

The two disagree most sharply on two points. **C1**: does Lakalei-Idate belong with Central Timor, as in Hull, or with Timor-Babar, as in Edwards and Grimes and Edwards? **C2**: is Welaun a dialect of Tetun, as Hull (1998) first had it, or a Central Timor language (Edwards 2019)?

Grimes and Edwards argue from historical phonology, supported by morphosyntax and the lexicon. The only earlier phylogeny covering Timor, Gray, Drummond and Greenhill (2009), includes Tetum, Mambai and Kemak but none of Idaté, Lakalei, Welaun, Habu, Midiki or Helong. This paper asks what the basic vocabulary says, using a pre-registered design in the spirit of Robinson and Holton (2012), who used lexical phylogenetics where sound changes had left the subgrouping of Alor-Pantar unresolved. It then asks how far the lexical signal reflects inheritance rather than contact.

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

Each lect needed at least 100 of the 152 concepts. Forms that look like loans from Indonesian or Portuguese, forms that look like Tetun, and contact sets shared with neighbouring Papuan languages were flagged and screened in sensitivity variants. Idaté, Lakalei, Welaun, Habu, Midiki and Helong are absent from ABVD; this is their first cognate-based phylogenetic placement. Idaté, Welaun, Habu and Helong do have short ASJP lists. Figure 1 shows the 24 lects used in the model-based analyses, one per language.

![The 24 lects used in the Bayesian and maximum-likelihood analyses, one per language. Lakalei-Idate (red) lies between Central Timor (blue) and the Eastern Timor languages of Grimes and Edwards (dark grey); the dashed line is the border between Timor-Leste and Indonesia. Coordinates from LexiRumah; coastlines from Natural Earth.](figures/map.pdf){width=100%}

# Methods

**Pre-registration.** The protocol was frozen and fingerprinted (SHA-256) before any analysis. Eight dated addenda, each pushed to a public repository before the tests it governs, extended it. Everything after the frozen protocol is post hoc and is labelled as such. The pre-registered decision rule required a contested clade to reach 70% bootstrap support in both UPGMA and NJ trees, on the primary data and on two screened variants.

**Cognates.** Automatic cognate detection used LexStat (threshold 0.55) and SCA (0.45) with Infomap clustering in LingPy (List, Greenhill and Gray 2017). Scored against the ABVD expert judgements, LexStat reaches a B-cubed F of 0.81 (precision 0.88, recall 0.75); distances from the automatic cognates match ABVD expert distances at Mantel r = 0.90. A gate of known low-level groups had to be recovered before any contested clade was scored.

**Trees.** Distance trees (UPGMA, NJ) with 1,000 concept bootstraps were built for 30 hypothesis clades. Treelikeness was measured with delta scores and Q-residuals. Bayesian analyses in MrBayes 3.2.7a used 24 lects and 1,353 binary cognate characters (restriction model with gamma rate variation). Each contested clade was run forced and forbidden, and Bayes factors were computed from stepping-stone marginal likelihoods. Maximum-likelihood trees used IQ-TREE 2.3.6 with ultrafast bootstrap.

**Sound changes.** The marked reflexes in Grimes and Edwards's tables were turned into an expert reflex atlas; LexiRumah forms aligned to ABVD PMP forms gave an automatic atlas. The two agree on 94% of tokens (249 of 264). Eight diagnostic changes, later eleven, were coded as binary characters and combined with the lexicon.

**Inheritance and contact.** Five post hoc tests separate the two.

1. Each cognate set was classed as a PMP retention (some form within SCA normalised edit distance 0.5 of the PMP form) or an innovation (the PMP word was replaced). Exclusive shared innovations were counted, with a control for geographic distance.
2. A triplet site-pattern test, the lexical counterpart of the ABBA-BABA statistic: for three groups, it counts concepts on which exactly two share an innovation. The largest count marks the tree pair, and an imbalance between the other two marks contact. It was checked on Welaun's known Tetun contact and run separately on the 60 Leipzig-Jakarta concepts (Tadmor 2009) and on the rest.
3. A split test asks which member of Lakalei-Idate carries each signal.
4. Approximate Bayesian computation estimates the borrowing that each placement of Lakalei-Idate would need.
5. Historical glottometry (Kalyan and François 2018) and a strict-clock analysis give a non-tree and a dated view.

A contact-aware phylogeny (contacTrees; Neureiter et al. 2022) was also attempted.

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

**Shared innovations.** Lakalei-Idate shares 7 exclusive innovations with Central Timor (among them 'cry' *sɛro*, against *tanis* < \*taŋis almost everywhere else) and 9 with the Eastern Timor groups combined. With distance controlled, Tetun shares more innovations with Lakalei-Idate than expected, even on stable concepts.

**Triplet test.** The test recovers Welaun's Tetun contact (Z = 3.1), and places it where contact should be: in borrowable vocabulary (Z = 6.9), not in stable vocabulary (Z = 0.6). On stable concepts Lakalei-Idate + Nuclear Central Timor is the tree pair against every eastern group (Figure 4). In borrowable vocabulary, Habu overtakes Central Timor, the same signature as Welaun's Tetun contact.

![Triplet counts on stable (Leipzig-Jakarta) and borrowable concepts. Each bar is one triplet of the focal group (Welaun or Lakalei-Idate), Nuclear Central Timor (Mambae, Kemak and Tokodede) and a third group; the numbers count concepts on which exactly that pair shares an innovation. Welaun, whose Tetun contact is documented, is the control.](figures/triplets.pdf){width=100%}

**Which half carries the signal.** In stable vocabulary, five of the eight Central Timor items are shared by both Idaté and Lakalei, so they predate the split between them. In borrowable vocabulary, six of eight are found only in Lakalei and match Mambae, spoken 10 km away ('cloud' *sabai*, 'neck', 'eat' *mia* ~ *mua*). The counts are small (binomial p = 0.11).

**How much borrowing each placement needs.**

| ABC, 20,000 runs per model | Sister to Central Timor, eastern borrowing | Within Eastern Timor, Central Timor borrowing |
|----------|-----------|-----------|
| Posterior probability | 0.125 | 0.875 |
| Borrowing in stable vocabulary, median (90%) | 16% (1–41%) | 28% (4–53%) |
| Borrowing in other vocabulary | 13% (2–40%) | 30% (8–52%) |

: Approximate Bayesian computation on the 18 triplet counts. Cross-validation recovers the true model in 87 to 94% of simulations.

The simulation prefers Grimes and Edwards's placement, but only if Lakalei-Idate borrowed more than a quarter of its core vocabulary from Central Timor, and as much core vocabulary as other vocabulary, unlike Welaun's known contact. That exceeds the 20% bar set in advance for a defensible placement. On the full lexical likelihood, the unconstrained tree is better than the constrained one by 10.5 log units.

**Glottometry and dating.** Glottometry finds cohesive groups only at low levels. Lakalei-Idate is cohesive on its own (subgroupiness 1.42) and tied almost equally weakly to Central Timor (0.06) and to Eastern Timor (0.08); Hull's Ramelaic scores 0. Under a strict clock, about 80% of posterior samples still place Lakalei-Idate with Central Timor, and the split (relative height 0.29) is barely older than Central Timor's own diversification (0.27). contacTrees did not reach a stable solution: it kept adding contact edges, each moving 14 to 23% of the vocabulary, so it is not reported further.

# Results: other disputed branches

| Triplet | Counts, all concepts (stable) | Reading |
|-------|------------------|----------|
| Habu, Tetun, Kawaimina | Habu+Tetun 15 (5); Habu+Kawaimina 11 (5); Tetun+Kawaimina 4 (2) | Unresolved; the Tetun link is in borrowable words |
| Waima'a, Naueti, Midiki | Waima'a+Naueti 10 (7); Waima'a+Midiki 7 (4); Naueti+Midiki 2 (1) | Leans towards Grimes and Edwards's Waima'a-Naueti |
| Galoli, Wetar, Dadu'a | Galoli+Dadu'a 20 (13); Galoli+Wetar 6 (2); Wetar+Dadu'a 6 (4) | Galoli pairs with Dadu'a, not with the Wetar lects |
| Galoli, Wetar, Tetun | Galoli+Wetar 12 (8); Galoli+Tetun 6 (4); Wetar+Tetun 0 (0) | Galoli belongs with Wetar-Atauro, with a Tetun layer |
| Helong, Meto, Rote | Meto+Rote 17 (12); Helong+Meto 10 (8); Helong+Rote 3 (2) | Rote-Meto holds; Helong outside it |

: Triplet tests on other disputed placements.

# Discussion

**What the vocabulary shows.** There is no lexical support for Hull's Fabronic, for Timor-Babar or for Eastern Timor. This does not refute Timor-Babar, which Grimes and Edwards define by sound changes rather than by shared vocabulary; it means that, if Timor-Babar is a subgroup, its lexicon has since been reshaped by contact. Welaun belongs with Central Timor, and its Tetun appearance sits in borrowable vocabulary, in agreement with Edwards (2019). The low-level groups hold, and Galoli pairs with Dadu'a.

**Lakalei-Idate remains unresolved.** Every tree analysis places it beside Central Timor, and none supports Timor-Babar. Its stable Central Timor items predate the split between Idaté and Lakalei, and a recent Mambae layer is visible in Lakalei's borrowable words. But its eastern sharing is substantial, the phonology points east, and a model that allows borrowing cannot exclude Grimes and Edwards's placement if a quarter of the core vocabulary was borrowed. The reading that fits most of the evidence is an old, conservative member of a central Timor dialect chain, close to Hull's Ramelaic, which broke away about when Central Timor itself diversified and kept ties to the east. The comparative method's own test, regular sound correspondences across complete wordlists, has not yet been applied to these data.

**What would settle it.** Expert cognate judgements for the decisive concepts; Grimes and Edwards's 494-item field lists for Idaté and Lakalei, which are not public; Alcantara's full 800-word Idaté corpus; and the Indonesian-era grammars of Idaté (Purwa et al. 1994) and Kemak (Mandaru, Haan and Liufeto 1998).

# Limitations

Most results after the frozen protocol are post hoc, and about twenty analyses were run without correction for multiple testing. The cognates are automatic and have not been checked by a specialist, and the C1 result depends on how they are coded. LexiRumah and Grimes and Edwards share sources and an editor. The sound-change characters come from illustrative tables and are thin for Idaté and Lakalei. The retention classifier misclasses some heavily changed retentions (for example 'tail' *hiʔor* < \*ikuR). The triplet test assumes similar rates of change across lineages, an assumption the lexical tree does not meet. The simulation summarises the data in 18 counts and allows borrowing in one direction per model. Hull (1998) and Carvalho (2001) are cited from secondary sources.

# Data and code {.unnumbered}

All data, code, results, the protocol and its addenda are at <https://github.com/DenC-dev/sanak>. The numbered scripts in `src/` rerun every analysis from pinned upstream data. The derived datasets (Grimes and Edwards's tables as data, expert and automatic reflex atlases, sound-change matrices, loan classifications, the Alcantara Idaté list, and the retention or innovation status of every cognate set) are in `derived/`. Code is MIT-licensed; data keep their sources' licences.

# Use of AI {.unnumbered}

The code, the analyses and the drafting of this paper were carried out with substantial assistance from Claude (Anthropic), an AI system, under the author's direction. Every analysis, decision and correction is recorded in the public repository so that it can be checked.

# References {.unnumbered}

::: {.refs}
Albuquerque, Davi Borges de. 2009. Pré-história, história e contatos lingüísticos em Timor Leste. *Domínios de Lingu@gem* 3(2): 75–93.

Alcantara, Maressa Xavier. 2015. *Descrição fonética e fonológica da língua idaté do Timor Leste*. MA thesis, Universidade de São Paulo.

Edwards, Owen. 2019. Reintroducing Welaun. *Oceanic Linguistics* 58(1): 31–58.

Fogaça, Jessé Silveira. 2015. *Aspectos gramaticais da língua Makasae de Timor-Leste*. PhD thesis, Universidade de Brasília.

Gray, Russell D., Alexei J. Drummond and Simon J. Greenhill. 2009. Language phylogenies reveal expansion pulses and pauses in Pacific settlement. *Science* 323: 479–483.

Greenhill, Simon J., Robert Blust and Russell D. Gray. 2008. The Austronesian Basic Vocabulary Database. *Evolutionary Bioinformatics* 4: 271–283.

Grimes, Charles E. and Owen Edwards. 2026. *The Austronesian languages of eastern Indonesia and Timor-Leste: Unravelling their prehistory and classification*. Berlin: Language Science Press.

Hull, Geoffrey. 1998. The basic lexical affinities of Timor's Austronesian languages: a preliminary investigation. *Studies in Languages and Cultures of East Timor* 1.

Hull, Geoffrey. 2001. O mapa linguístico de Timor Leste: uma orientação dialectológica. *Studies in Languages and Cultures of East Timor* 4: 1–19.

Kaiping, Gereon A. and Marian Klamer. 2022. The dialect chain of the Timor-Alor-Pantar language family: a new analysis using systematic Bayesian phylogenetics. *Language Dynamics and Change* 12(2): 274–326.

Kaiping, Gereon A., Owen Edwards and Marian Klamer, eds. 2019. *LexiRumah* 3.0. Leiden University Centre for Linguistics.

Kalyan, Siva and Alexandre François. 2018. Freeing the comparative method from the tree model: a framework for historical glottometry. *Senri Ethnological Studies* 98: 59–89.

List, Johann-Mattis, Simon J. Greenhill and Russell D. Gray. 2017. The potential of automatic word comparison for historical linguistics. *PLOS ONE* 12(1): e0170046.

Mandaru, A. Mans, John W. Haan and Gomer Liufeto. 1998. *Morfologi dan sintaksis bahasa Kemak*. Jakarta: Pusat Pembinaan dan Pengembangan Bahasa.

Neureiter, Nico et al. 2022. Detecting contact in language trees: a Bayesian phylogenetic model with horizontal transfer. *Humanities and Social Sciences Communications* 9.

Purwa, I Made et al. 1994. *Struktur bahasa Idate*. Jakarta: Pusat Pembinaan dan Pengembangan Bahasa.

Robinson, Laura C. and Gary Holton. 2012. Internal classification of the Alor-Pantar language family using computational methods applied to the lexicon. *Language Dynamics and Change* 2(2): 123–149.

Tadmor, Uri. 2009. Loanwords in the world's languages: findings and results. In Martin Haspelmath and Uri Tadmor (eds.), *Loanwords in the World's Languages: A Comparative Handbook*, 55–75. Berlin: De Gruyter Mouton.

Wichmann, Søren, Eric W. Holman and Cecil H. Brown, eds. *The ASJP Database*, version 21. Lexibank CLDF release.
:::
