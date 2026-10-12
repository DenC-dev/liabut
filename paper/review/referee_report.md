# Referee report

**Journal:** *Language Dynamics and Change*
**Manuscript:** "Liabut: a pre-registered computational test of how Timor's Austronesian languages branch" (working paper dated 11 October 2026)
**Recommendation:** Major revision

**Scope of this review.** I read the manuscript (`paper/liabut.md`, abstract in `paper/title.tex`, built PDF), `PROTOCOL.md` with Addenda 1 to 10, `results/REPORT.md`, `results/LITERATURE.md`, the result files under `results/` and the code under `src/`. Addendum 11 (E37 to E39) was still running and is outside this report.

**My own checks.** Where I say "I recomputed", I ran short, read-only scripts in a scratch directory on the repository's own trees, character matrices and MCMC samples. No project file was changed.

---

## 1. Summary of the submission

The paper asks whether the basic vocabulary of Timor's Austronesian languages fits better with Hull's Ramelaic/Fabronic classification or with the split by Edwards and by Grimes and Edwards (2026) into Central Timor and Timor-Babar. It focuses on two contrasts: where Lakalei-Idate belongs (C1) and where Welaun belongs (C2).

The data are LexiRumah wordlists with automatic LexStat cognates. A pre-registered distance-tree bootstrap rule returns "unresolved" for both contrasts. Thirty-six further analyses follow, governed by ten dated addenda; by the paper's own account all but two are post hoc.

Bayesian (MrBayes) and maximum-likelihood (IQ-TREE) analyses of 24 lects place Welaun in Central Timor (posterior 0.86) and Lakalei-Idate as sister to Central Timor (0.91). No analysis recovers Hull's Fabronic, Timor-Babar or Eastern Timor as lexical groups. On lists collected independently of Grimes and Edwards, Lakalei-Idate + Nuclear Central Timor gets 97% UFBoot, and AU tests reject Lakalei-Idate + Eastern Timor (p = 0.025) and Timor-Babar (p = 0.042).

Two new tools are introduced to separate inheritance from contact: a lexical "triplet" site-pattern test and ABC models of borrowing. After calibration, the paper concludes that only Welaun's known Tetun contact is statistically secure and that the ABC cannot separate the two placements of Lakalei-Idate. It also argues that the phonological evidence for the eastern placement does not discriminate, because eleven coded changes cost the same number of parsimony steps on both trees.

The paper concludes that C1 is formally unresolved but "leans towards Central Timor", with Lakalei-Idate as an old member of a central Timor dialect chain. All data and code are public.

---

## 2. Major concerns

Concerns are ordered by how much they affect the conclusions.

### M1. The C1 result and the "no Timor-Babar" result depend on where the tree is rooted, and the root is set by two Flores lects that attach to Rote-Meto

**Where:** Abstract; Table 2; Figure 2; Table 3; Section 7 (E36); Protocol Addendum 2.4 (unrooted MrBayes, outgroup Lamaholot).

**Problem.** All the model-based trees are unrooted. They are read as if rooted on the Flores-Lembata pair (Lamaholot, Sika), but that pair does not sit outside Timor in the trees. It attaches to Rote-Meto + Helong:
- In the unconstrained MrBayes run, the split {Lamaholot, Sika, Helong, Amarasi, Termanu, Dela} against all other taxa has posterior 0.949 (split 36 in `results/bayes/unconstrained.parts` / `.tstat`).
- The same grouping has 77% UFBoot in the lexical ML tree (`results/total_evidence/lex_only.treefile`).

Once the outgroup sits inside "Timor-Babar", Timor-Babar cannot come out as a clade in any analysis. The rest of the tree is then a chain: Central Timor, then Lakalei-Idate, then Tetun, then everything else. If that same unrooted tree is rooted on the Central Timor stem, it becomes exactly Grimes and Edwards's tree, (Central Timor, (Lakalei-Idate, (Tetun, ...))), with Lakalei-Idate as the first lineage to branch off within Timor-Babar. So "Lakalei-Idate sister to Central Timor" and "Lakalei-Idate basal in Timor-Babar" are one unrooted tree with two root positions.

I checked this on the constrained trees:
- The IQ-TREE tree constrained to Timor-Babar (`results/ml/timor_babar.treefile`) differs from the unconstrained tree mainly in where the Flores pair sits. The pair moves from beside Rote-Meto to the junction between Central Timor and the rest. Lakalei-Idate stays next to Central Timor and becomes the first branch of Timor-Babar.
- The same holds for the E36 tree on the independent lists (`results/literature/e28/au_timor_babar.treefile` against `lex_independent.treefile`).

So three of the headline numbers measure the cost of moving two Flores lects away from their lexical neighbours in Rote and western Timor: the ln BF of −7.0 for Timor-Babar, its 11.7 to 12.0 log-likelihood cost, and the AU rejection of Timor-Babar on the independent lists (p = 0.042). None of them tests how the languages of Timor are related to each other. The 97% for Lakalei-Idate + Nuclear Central Timor on the independent lists has the same dependence on the root.

**Why it matters.**
- C1 as Grimes and Edwards pose it is a question about where the root of the Timor tree lies: is Central Timor a primary branch, with Lakalei-Idate inside Timor-Babar? In their classification (building on Donohue and Grimes 2008), Central Timor and Timor-Babar are separate Malayo-Polynesian branches. Nothing in that classification makes Flores-Lembata an outgroup to both, and E34 imposes a single Timor clade that their classification does not posit.
- If contact or shared retention across the Savu Sea has pulled Flores-Lembata towards Rote-Meto, the observed trees would result even if Grimes and Edwards are right.
- The phonology says the same. Flores-Lembata keeps \*p (10 of 10 tokens, E2). For Flores to sit inside the group defined by \*p lenition, \*p would have to be restored in Flores or to have weakened independently several times.

**The pre-registered model would have handled this better.** Step 7 of the protocol specified a BEAST2 relaxed clock with a Yule prior, which estimates a root. Addendum 2.4 replaced it with unrooted MrBayes, which does not.

**The strict-clock runs do not settle the root either.** I recomputed root positions from the E34 MCMC samples. Even with the 22 Timor-region taxa forced into one clade, the first split inside Timor separates Kisar-Luang-Tela-Masbuar from the rest in 97.5% of post-burn-in samples. Tela-Masbuar's branch in the ML trees is 0.67 to 0.84, against 0.05 to 0.2 for most other lects, so this looks like a long branch attracting the root. No analysis in the paper therefore estimates the root independently of these problems.

**Fixes.**
- **Report C1 as an unrooted result.** The findings that do not depend on the root are these: Lakalei-Idate sits next to Central Timor in the unrooted tree, and a grouping of Lakalei-Idate with Eastern Timor is disfavoured (E6, E36). Neither "Lakalei-Idate + Central Timor 0.91" nor "Timor-Babar 0.00" should be presented as a test of Grimes and Edwards without that caveat.
- **Estimate the root without relying on the Flores pair:**
  - use several outgroups at different distances (for example Sulawesi or Philippine lects from ABVD, Malay, or PMP reconstructions as a pseudo-taxon);
  - run the relaxed-clock model that was pre-registered (BEAST2 or RevBayes) and summarise where it puts the root;
  - repeat without Tela-Masbuar.
  Report the posterior probability of each root position: on the Central Timor stem, on the Lakalei-Idate stem, and elsewhere.
- **Show where the Flores pair attaches** in every tree, with its support. Either drop the "Timor-Babar" row of Table 2 or label it as a statement about rooting.
- **Re-run E36 with the outgroup's position held fixed** in both the constrained and the unconstrained trees, so that the AU test compares only the relationships among the Timor languages.

### M2. Lexical trees cannot test a subgroup defined by sound changes, and E29's verdict that the sound changes do not discriminate comes from coding choices

**Where:** Section 5 (paragraphs 1 and 2, Table 3); the Discussion ("the coded sound changes cost the same on either tree"); the Abstract; E29 (`src/34_addendum9.py`, `e29_sound_fit.json`); `derived/sound_change_matrix/innovation_matrix_24_hull.csv`.

**Problem 1: the logic is applied unevenly.** Timor-Babar and Central Timor are defined by sound changes found only in their members. A lexical tree mixes inheritance, shared retention and borrowing. The paper accepts this for Timor-Babar: its Discussion says lexical non-support "does not refute Timor-Babar". The same reasoning covers Lakalei-Idate, since a Lakalei-Idate lexicon can also be "reshaped by contact". The paper treats the lexicon as uninformative about Timor-Babar but informative about where Lakalei-Idate belongs, and gives no reason for the difference.

The paper's own data show that the lexical method rarely recovers higher-level groups defined by sound changes, including groups nobody here disputes. In the pre-registered distance trees (`hypotheses/summary_d1_lexstat.csv`, UPGMA/NJ bootstrap):
- West Rote-Meto (Dela + Meto; Grimes and Edwards §4.8.1) gets 0/0;
- Southwest Maluku gets 0/30;
- Nuclear Central Timor gets 37/75.

Tetun also groups lexically with Central Timor and Lakalei-Idate (0.90), against Grimes and Edwards's Eastern Timor, as it already did in Gray et al. (2009; 0.71). Lexical non-support is therefore normal for sound-change-defined groups in this region, so its absence for Timor-Babar tells us little. This is the relevant known-answer test, and the paper does not report it.

**Problem 2: E29 depends on two coding choices.** The claim that the eleven coded changes "need 30 steps" on either placement rests on choices a historical linguist would not make:
- The Flores outgroups are coded "?" (unknown) for \*p lenition, although E2 records \*p kept in 10 of 10 Flores-Lembata tokens. With the ancestral state left open, parsimony can put \*p lenition at the base of the whole tree.
- Fitch parsimony allows changes to reverse, so it lets Central Timor turn \*h back into \*p. The paper's own wording ("the eastern-looking changes can sit below that group at no extra cost") describes exactly that reversal.

I recomputed with the repository's trees, rooted on Lamaholot: H is `lex_only.treefile`, G is `e21_abc/G.treefile`, GE is `e29/GE.treefile`.

| Count for \*p > h/ʔ/∅ | H (lexical tree) | G (LI + Eastern Timor) | GE (Grimes and Edwards's split) |
|---|---|---|---|
| Fitch, outgroups "?" (as in E29) | 1 | 1 | 1 |
| Fitch, outgroups coded \*p-retaining | 2 | 2 | 2 |
| Irreversible lenition, outgroups coded \*p-retaining | 6 | 4 | 2 |

The irreversible count assumes lenitions do not reverse, which is the standard assumption. Under it, the change that defines Timor-Babar has to happen independently six times on the lexical tree and twice on Grimes and Edwards's tree, so that change clearly favours their tree. Summed over all eleven characters as coded, the irreversible counts are 47, 45 and 49. The other characters are too sparse and too often parallel to say much either way.

**Problem 3: the diagnostics are judged by different standards.**
- \*ŋ > n is set aside because it "also occurs in Sika". Yet \*d > r, l is then called "a Central Timor change" in Lakalei-Idate (Section 5, paragraph 2), although the matrix codes it 1 in Sika and in Dela as well.
- The Report (A3.5) said plainly that "no sound change unites Lakalei-Idate with Central Timor alone" and that "on the comparative method's own standard ... Grimes and Edwards's placement stands". The manuscript drops this, along with:
  - the native-word \*p evidence: Lakalei-Idate keeps \*p in 0 of 6 native words against 54 of 55 in Nuclear Central Timor (Fisher p = 1.3 × 10⁻⁷, E2);
  - further native cases cited by Grimes and Edwards (\*pija, \*hapuy);
  - the contrast between \*ma-p > b in Lakalei-Idate and \*mp in Central Timor.

**Problem 4: the combined analyses cannot show agreement.** Table 3 adds 8 to 17 sound-change characters to 1,353 lexical characters, with each character weighted equally. The phonology is about 1% of the matrix. That "every combined analysis gives the same answer" is therefore expected from the design. It does not show that the phonology agrees with the lexical tree.

**Fixes.**
- Bring the comparative-method framing and the omitted phonological evidence back into Section 5.
- Re-run E29 with the outgroup's ancestral state coded from E2 and with irreversible or asymmetric costs (Camin-Sokal or Dollo parsimony, or an asymmetric Mk model with the root fixed to the PMP state). Report results separately for each defining change.
- Hold every change to the same standard: if Sika's \*ŋ > n disqualifies that change, Sika's and Dela's \*d > r disqualifies \*d > r.
- Report how often the lexical method recovers undisputed sound-change-defined groups, as a calibration. State plainly that lexical data cannot overturn a subgroup defined by sound changes unless they also establish the root.
- Replace the equal-weight combination in Table 3 with a direct test of the phonological characters on the rival trees (for example their marginal likelihood or parsimony cost with each lexical tree held fixed), or drop the claim that the combined analyses are informative.

### M3. The data reported do not justify "leans towards Central Timor"

**Where:** the last sentences of the Abstract; the Discussion paragraph "Lakalei-Idate remains unresolved, but the balance has moved"; Section 7.

**Problem.** Setting aside M1 and M2, the lean rests on trees built from lexical similarity. That evidence has further weaknesses that the paper never brings together.

- **It depends on how cognates are coded.** Support for Lakalei-Idate + Central Timor is:
  - 65% with the primary coding and 92% with SCA;
  - 15% and 20% with LexStat thresholds of 0.35 and 0.75;
  - 0% with LexiRumah's own cognates;
  - 0% with the consensus coding of E27, where the clade including Welaun disappears and only Lakalei-Idate + Nuclear Central Timor (55%) remains.

  UFBoot values below 95 are weak support (Hoang et al. 2018), so the 56 to 80 in Table 3 should not be read as support.
- **Lakalei-Idate itself does not hold together in the ML trees.** The two languages form a group in only:
  - 53% of primary lexical replicates;
  - 42% with eleven sound changes added;
  - 48% with SCA, 27% with LexiRumah's cognates;
  - 6% with the consensus coding;
  - 5% on the independent lists, where Lakalei falls inside Nuclear Central Timor (94%) and Idaté-Cribas falls outside it.

  The 97% for "Lakalei-Idate + Nuclear Central Timor" is therefore support for a group in which Idaté and Lakalei are not each other's closest relatives. Both Hull and Grimes and Edwards treat Lakalei-Idate as a unit, so a tree that splits it is a warning sign.
- **Each member leans towards its own neighbour.** In the observed statistics of E32 (R2 rule, stable concepts):
  - Idaté-Cribas shares more innovations with Habu (13) than with Nuclear Central Timor (10);
  - Lakalei shares more with Nuclear Central Timor (13) than with Habu (6).

  Lakalei is 10 km from Mambae, and Idaté is 5 to 11 km from Habu (E20 distances). E14 (ASJP) also placed Idaté nearest to Habu. This pattern fits contact or a dialect continuum as well as it fits descent, and the E20 split test shows that the items only Lakalei shares are the borrowable ones.
- **Counts of shared innovations do not lean towards Central Timor.** Innovations Lakalei-Idate shares exclusively:
  - with Central Timor: 7 under the original R0 rule, 6 under the chosen R2 rule, and fewer after the paper's own etymological check (M4);
  - with the eastern groups: 9.

  Glottometry, the method closest to the comparative method, gives σ = 0.08 for Lakalei-Idate + Eastern Timor, 0.06 for Lakalei-Idate + Central Timor, and 0 for Hull's Ramelaic.
- **Two further checks do not support the lean.** The ABC cannot separate the placements (M6), and the confirmatory predictions failed against Tetun in both replications.

**Fixes.**
- In the Abstract and the conclusion, report C1 as unresolved with no lean. If a lean is kept, state it exactly: "Lakalei-Idate's basic vocabulary is most similar to Central Timor's, which fits Central Timor descent and a Timor-Babar language with a Central Timor lexical layer equally well."
- Force Lakalei-Idate to be monophyletic in the ML, AU and UFBoot analyses (every hypothesis agrees on it), and also analyse Idaté and Lakalei separately.
- Remove "an old member of a central Timor dialect chain" from the Abstract unless a linkage model is actually tested (M10).

### M4. Many of the "shared innovations" are retentions or cognate errors

**Where:** Section 6 ("Shared innovations"); Figure 4; Table 5 (E30, E35); `derived/innovations/reviewer_packet_lakalei_idate_stable.csv`; `e17_exclusive_innovations*.csv`.

**Problem.** To decide whether a cognate set is an innovation or a retention, the classifier compares it with ABVD's PMP form for the same concept. The cut-off is an SCA distance of 0.5 under R0, or 0.4 after substituting each language's regular reflexes under R2. This misses retentions whose forms are short, compounded, shifted in meaning or regularly changed. Validated against experts, the classifier finds only 70% (R0) to 75% (R2) of retentions. Retentions are by nature widely shared, so misclassified ones make up a disproportionate part of the shared-"innovation" counts behind E17, E18, E20, E22, E26 to E28 and E31 and E32.

The 24 sets in the reviewer packet show how large the problem is. Many are recognisable retentions of PMP or PCEMP words:

| Concept | Forms | Etymon |
|---|---|---|
| '2sg' | *oː* | PMP \*(i)kahu |
| 'eat' | Mambae and Idaté *aː* | PMP \*kaən |
| 'water' | Lakalei *wɛːr*, Tugun *ɛːr* | PMP \*wahiR |
| 'leaf' | *ai-roː* | \*kayu + \*dahun |
| 'hair' | *ulu-roː* | compound with \*qulu and \*dahun |
| 'tail' | *hiʔor* | \*ikuR |
| 'good' | *hia(n)* | \*ma-pia |
| 'laugh' | *mali* | PCEMP \*malip |
| 'stand' | *ʔamiri* | \*ma-diRi |
| 'far' (very probably) | *roː* | \*ma-zauq |
| 'small' (very probably) | *ana(k)* | \*anak 'child' |

E35 caught only 6 of the 24.

The seven "exclusive" Lakalei-Idate + Central Timor innovations of E17 (R0 rule) include:
- 'tail' (tail-1644), which both the chosen R2 rule and the strict ACD check classify as inherited;
- two separate 'wife' sets: wife-2376 (Idaté *mahinɑn* ~ Mambae *hinɛ*) and wife-2380 (Lakalei *hɛːn* ~ Kemak *heːr*). These are plausibly one etymon (\*b<in>ahi) that LexStat split and that is therefore counted twice;
- 'who', which pairs Idaté *ʔɛta* with Railaco Mambae *sepdua*, and these are not cognate;
- 'dry', Lakalei *kiʔɑs* ~ Mambae *glia*, which is doubtful.

The text says only that "one of the seven, 'wife'" is a retention. What survives is 'cry' (*sɛro*) and 'spit', perhaps 'dry'. The eastern sets have not been checked either.

**Why it matters.** Misclassified retentions inflate the counts shared with conservative lineages, and Lakalei-Idate is the conservative lineage with the short branch (LITERATURE.md, E18). This is the classic problem of shared retentions mistaken for shared innovations, which the triplet test was meant to avoid.

**Fix.** Before resubmission, have an Austronesianist judge every set that enters the decisive counts (the packet is small), together with the E17 exclusive inventories on both sides. Report triplet counts and exclusive counts on checked sets only. This should be a precondition for any claim based on shared innovations; the paper itself lists it under "what would settle it".

### M5. As implemented, the triplet test does not separate descent from contact

**Where:** Methods, item 2; Section 6 ("Triplet test"); Figure 4; Table 6; `src/28_innovations_contact.py` (E18); `src/36_triplet_power.py`; `e31_triplet_power.json`.

**Problems.**

1. **No outgroup to fix which state is new.** In ABBA-BABA (Green et al. 2010; Durand et al. 2011), the new state is defined by comparison with an outgroup. Here an "innovation" only has to differ from the PMP form. The code counts a set shared by A and B and absent from C, wherever else it occurs. So an innovation made above the triplet (in proto-Timor, or an areal word) that C later lost counts as evidence that A and B are the "tree pair". The rate at which each lineage replaces words then decides the tree pair. A fast-changing C (Tetun as a lingua franca, or Kawaimina under Papuan contact) loses more of the older innovations, so A and B win even if they are not a clade.
2. **The rule "largest count = tree pair" is never calibrated.** E31 calibrated D but not this rule, and its own output shows the rule failing. With no borrowing, on the true tree H, the Lakalei-Idate + Habu count equals or exceeds the true tree pair on borrowable concepts in 63% of simulations. No simulation under G checks how often Lakalei-Idate + Nuclear Central Timor would come out as the largest stable-concept pair if Lakalei-Idate were really eastern. The E32 predictive checks suggest that it often would.
3. **The Welaun control is weak.**
   - Its D is not unusual under the null (p = 0.15; `p_upper` in E31); only its jackknife Z is (p = 0.002).
   - Under the consensus coding (E27), Welaun + Tetun becomes the tree pair even on stable concepts (10 against 8). The known-answer check therefore fails under one of the paper's own codings.
   - Welaun's contact is recent borrowing from a lingua franca. That is a different kind of contact from the old contact between neighbouring dialects that is at issue for Lakalei-Idate.
4. **"Stable" concepts are less stable here.** The Leipzig-Jakarta borrowability figures (Tadmor, Haspelmath and Taylor 2010) come mostly from borrowing out of unrelated or prestige languages. Closely related neighbouring varieties borrow basic vocabulary far more readily. A tree pair in the stable stratum is therefore weaker evidence of descent here than the paper assumes.
5. **The null is circular.** The E31 null and the ABC are simulated on the ML tree, with branch lengths estimated from the same data. Any contact that shortened Lakalei-Idate's branch or drew it towards Central Timor is already built into the null.
6. **Reporting.**
   - The counts are summed over combinations of lects (for example 184 for 98 concepts in the Lakalei-Idate, Nuclear Central Timor, Kawaimina triplet). Figure 4's caption says they count concepts.
   - The tree pair is picked as the largest count, and D is then computed from the same data.

**Fixes.**
- Fix the direction of change with a designated outgroup: count only sets absent from Flores, Rote-Meto and Wetar, or report four-taxon patterns.
- Calibrate the tree-pair rule by simulating under both H and G, with and without borrowing, and report its error rates.
- Re-run on checked sets (M4).
- Present the test as exploratory and descriptive. Put its false-positive rate (22% to 33% at Z ≥ 2) and its power (30% for 20% borrowing at the calibrated threshold) in the main text wherever the test is used.

### M6. The ABC results mostly restate their priors, and the design cannot answer the question

**Where:** Table 4; Section 6 ("How much borrowing each placement needs"); `src/31_borrowing_abc.py`, `src/37_abc2.py`; `e21_borrowing_abc.json`, `e32_abc2.json`.

**Problems.**
- **The posteriors are close to the priors.** Borrowing parameters have uniform priors from 0 to 0.6, with median 0.30 and a 90% interval of 0.03 to 0.57.
  - In E32 the posterior medians are 22% to 25%, with 90% intervals between 2% and 57%.
  - E21's "28% (4–53%) from Central Timor" is close to the prior too. Only E21's model H moves noticeably (16%, 1–41%).

  Table 4 presents these numbers as the "borrowing needed"; mostly they restate the prior.
- **The design cannot tell the models apart.**
  - The random forest's prior error rate is 36%, where 50% would be chance.
  - With 36 two-sided checks, about 1.8 would fail even if a model fitted perfectly. "0 of 36 predictive checks failed" for both models therefore points to very wide predictive distributions, not to a good fit.
  - The summary statistics are a handful of triplet counts. That is the situation in which ABC model choice is known to be unreliable (Robert et al. 2011).
- **The simulator is misspecified.**
  - Borrowing replaces the states of both Lakalei-Idate lects at the tips at once, with the same donor and the same concepts. The model therefore cannot represent the layer that only Lakalei shares with Mambae (E20), or the Idaté-Habu affinity, which are what 12 of the 36 statistics in E32 were added to capture.
  - The H and G trees and their branch lengths are ML estimates from the same data (see M5, point 5).
- **Pre-declared readings are not reported.**
  - Addendum 8 declared G "hard to defend lexically" if its stable borrowing exceeded 0.2. This triggered in E21 (0.276).
  - The equivalent rule in Addendum 9 triggered again in E32 (0.254).

  The manuscript reports neither. In fairness to G, H needs the same amounts in E32 (0.24 from Central Timor and 0.25 from the east), which shows that the rule is measuring the prior.

**Fixes.**
- Report each prior next to its posterior.
- Take E21 out of the main text: it has been superseded, and its preference for G came from allowing borrowing in one direction only.
- Either remove the ABC or redesign it, with borrowing specific to each lect, borrowing at internal nodes, more informative statistics (full site-pattern spectra), trees not fitted to the same data, and simulation-based calibration of both model choice and parameters.
- Report the pre-declared readings and explain why they are uninformative.

### M7. Pre-registration, deviations from it and the order of analyses are under-reported, and the title and abstract overstate the confirmatory content

**Where:** Title; Abstract; Methods ("Pre-registration"); Section 4; Limitations; `PROTOCOL.md`; `gate.json`.

**Problems.**

- **Little of the paper is confirmatory.**
  - The pre-registered decision is "unresolved" for both contrasts.
  - The only other confirmatory tests, E26 and E28, failed against Tetun (47% of combinations; 45 against 44).
  - Prediction P2 fails under the chosen R2 rule (31%; `e26_dialect_replication_r2.json`).
  - By the paper's own account, everything else beyond the frozen protocol is post hoc.
  - The protocol was frozen on 10 October and Addenda 1 to 10 followed by 11 October, each written after the previous results had been seen.
- **Several deviations are not disclosed in the manuscript.** They belong in the Methods, with a table of deviations:
  - the gate failed under the pre-registered rules (`gate.json`: `passed_under_v1_rules` false) and was then changed;
  - even the gate's first condition (G1) missed the split between the Papuan and Austronesian languages (KA2-TAP; UPGMA bootstrap 5% on the primary data);
  - before Addendum 2, the analyst had seen the full UPGMA tree including the Timor lects, so steps 5 to 8 were not blind (REPORT.md: "Not blind");
  - the pre-registered BEAST2 relaxed-clock model was replaced by unrooted MrBayes (Addendum 2.4), which bears directly on M1;
  - the pre-registered direct comparison of a Hull-constrained with an Edwards-constrained run became separate forced-against-forbidden runs for each clade.
- **One statement is wrong.** The paper says the decision rule did not use the Bayesian analyses. Step 8 of the protocol includes "the Bayes factor favours Edwards strongly" as one of its conditions. The bootstrap conditions failed first, which is not the same thing.
- **Follow-ups were aimed mostly at unfavourable results.**
  - E21 favoured G, and E32 was designed in response.
  - E6's AU test did not reject G (p = 0.07). E36 then ran the AU test again on the matrix that had just given the strongest tree signal.
  - P1 and P4 failed against Tetun. The R2 and ACD reruns followed and are described as raising the share "from 47% to 79%", still short of the 80% bar.
  - The LexiRumah coding that grouped Lakalei-Idate with Habu was set aside using a Mantel diagnostic "added after the trees" (E15).

  The main support, the tree placement, received fewer probes of its key assumptions: the root, whether Lakalei-Idate holds together, and contamination by retentions.
- **The AU tests are not corrected for multiple testing.** E25 corrects only the D statistics and binomial tests. The AU tests highlighted in the Abstract are not corrected across E6 and E36. Applying Holm's correction across those five AU tests, or across the four tests of the alternatives, rejects no constrained tree: the smallest adjusted p is 0.0248 × 4 = 0.099.

**Fixes.**
- Retitle, for example "...: a lexical-phylogenetic study with a pre-registered core".
- Open the Abstract with the pre-registered verdict and the failed confirmatory predictions.
- Add a table of deviations, and separate confirmatory from exploratory results in the structure of the paper.
- Correct the AU tests across all topology tests run.
- Ideally, pre-register a short second round and run it before resubmitting. It would cover rooting, checked cognates, and tests that keep Lakalei-Idate together, with a decision rule stated in advance.

### M8. The way the Bayes factors are presented invites misreading

**Where:** Table 2; Abstract.

**Problem.** A Bayes factor comparing a clade forced against the same clade forbidden equals the posterior odds divided by the prior odds; the Report's own cross-check gives 10.3 and 8.2. Under a uniform prior on topologies, any particular group of five or six taxa has a tiny prior probability. Any clade with a modest posterior therefore gets a "strong" Bayes factor:
- Hull's Ramelaic, with posterior 0.13, gets ln BF +8.0.
- Central Timor with Welaun, which cannot be a clade at the same time, gets +10.3.
- Compared directly, the two forced runs differ by only 0.38 log units (−8092.25 against −8091.87).
- The Timor-Babar Bayes factor also depends on the root (M1).

**Fixes.**
- Explain this in the caption and cite Bergsten, Nilsson and Ronquist (2013).
- Report direct comparisons of marginal likelihoods for the contrasts that matter, with the forced-against-forbidden values as secondary information:
  - Lakalei-Idate + Central Timor against Lakalei-Idate + Eastern Timor;
  - Welaun + Central Timor against Welaun + Tetun;
  - all under a common rooting.

### M9. C2 (Welaun) is reported selectively

**Where:** Abstract; Table 2; Discussion, paragraph 1.

**Problem.** The paper says Welaun "belongs with Central Timor" and that its Tetun contact "is the one signal that passes every check". Several results point the other way and are not mentioned:
- The pre-registered distance trees favour Welaun + Tetun (51/59) over Central Timor (14/17).
- Under the consensus coding, Central Timor with Welaun gets 0%, and the Welaun control's tree pair becomes Welaun + Tetun on stable concepts.
- Under the rooted clock, Central Timor with Welaun has posterior 0.29.
- Addendum 2.1 of the protocol stated in advance that "C2 cannot be settled lexically" and would not be decided on lexical grounds alone.
- The Introduction does not say that Hull withdrew the claim that Welaun is a Tetun dialect in 2003, placing Bekais between Tetun and Dawan. That makes C2 a weak contrast.

The strongest lexical evidence for Edwards (2019) is the contrast between stable and borrowable vocabulary. In E1, Welaun + Tetun gets 2/4 on stable concepts and 74/81 on the rest. That evidence is real.

**Fixes.**
- Report all of the results above.
- Phrase C2 as "once borrowable vocabulary is set aside, the lexical evidence is consistent with Edwards (2019)".
- Cite Hull (2003).

### M10. Alternative explanations are named but not tested

**Where:** Discussion; Limitations.

- **Tetun as a lingua franca.** Tetun Terik, and later Tetun Praça (Tetun Dili), has been a vehicular language over much of Timor for centuries.
  - The lexical trees put Tetun with Central Timor and Lakalei-Idate (0.90), against its classification by sound changes.
  - Hull's Ramelaic jumps to 88% to 95% when Tetun look-alikes are removed. The paper dismisses that variant as confounded, which is fair, but the result still shows that where Lakalei-Idate attaches depends on Tetun-shaped vocabulary.
  - Older Tetun loans that have adapted to the borrowing language's sound system are invisible to the near-identity screen (normalised edit distance ≤ 0.2).
  - If Tetun's lexical position is due to contact, as the Report suggests, the (Tetun, (LI, CT)) backbone that E29 relies on is due to contact as well.

  *Recommended:* show the C1 results with Tetun removed from the taxon set. Also screen all sets cognate with Tetun for adapted loans, using the expert reflex atlas as E12 did.
- **Papuan contact.**
  - On the primary data the method fails a family-level known answer: UPGMA does not separate the Papuan lects from the Austronesian ones (bootstrap 5%) unless contact sets are removed (99.8%).
  - The V-contact variant removes only the Papuan-side forms of a contact set (Addendum 1.2), so Papuan loans in Austronesian lects remain.
  - The Kawaimina languages border Makasae, and the Bunak area adjoins Kemak-, Mambae- and Tetun-speaking areas. Word replacement driven by Papuan contact could lower Eastern Timor's lexical cohesion and push Lakalei-Idate towards Central Timor through shared retention.

  *Recommended:* count the sets each lect shares with Papuan languages, and re-run with every set that has a Papuan member removed.
- **Dialect chain or linkage.** The paper ends on a linkage reading (Ross 1988; François 2014) but tests it only through glottometry. Glottometry shows Lakalei-Idate tied about equally to both sides and Hull's Ramelaic at zero. A linkage reading fits Grimes and Edwards as well as Hull; they already describe Wetar-Atauro as "overlapping subgroups". *Recommended:* present glottometry with resampling intervals, and network splits (a NeighborNet with split support). State which observations would distinguish a Timor-Babar subgroup defined by shared innovations from a Timor-Babar linkage.
- **Unequal rates and conservatism.** Lakalei-Idate is a conservative lineage with a short branch. Blust (2000) showed how this kind of rate variation misleads lexicostatistical subgrouping in Austronesian. This belongs in the discussion beside M1 and M4.

### M11. Treelikeness and dating are over-interpreted

**Where:** Section 4 (delta scores); Section 6 ("Glottometry and dating"); Discussion ("broke away about when Central Timor itself diversified").

**Treelikeness.**
- The protocol says tree results are "reported as weak" if mean delta exceeds 0.3. The 37-lect set passes (0.24) only because it includes 11 Mambae and 8 Kemak dialects.
- The 24-taxon set behind every model-based result has a mean delta of 0.334, and the paper does not label those results as weak.
- The list of "most reticulate lects" leaves out Tetun Dili (0.293, above Idaté at 0.285) and Tetun Suai (0.283, equal to Habu).

**Dating.** "Their split (0.48) is barely older than Central Timor's own diversification (0.47)" compares node heights of most recent common ancestors (MRCAs). Those heights are computed whether or not the group is a clade in a given sample.
- Central Timor with Welaun is a clade in only 29% of E34 samples.
- I find the MRCA of Central Timor including Welaun identical to the MRCA of Lakalei-Idate + Central Timor in 71% of samples, so the near-equality mostly follows from the definition.
- Using Nuclear Central Timor instead, the median gap is 0.07 (95%: 0 to 0.16), about a fifth of Nuclear Central Timor's height.
- As noted under M1, the strict clock still roots inside Timor, on Kisar-Luang-Tela-Masbuar, in 97.5% of samples.

**Fixes.**
- Label the 24-taxon results as weak, as the protocol requires.
- Compute node heights only in samples where the group is a clade, and compare Lakalei-Idate + Nuclear Central Timor with Nuclear Central Timor.
- Use a relaxed clock, and drop Tela-Masbuar or reduce its weight.
- Remove the dating sentence from the Discussion unless it survives these changes.

### M12. Missing literature

The paper should engage with the following.

- **Linkages and subgrouping theory:** Ross (1988) on linkages; François (2014); Durie and Ross (1996); Blust (2000), "Why lexicostatistics doesn't work"; Heggarty, Maguire and McMahon (2010).
- **Central Malayo-Polynesian and the region:**
  - Blust (1993);
  - Donohue and Grimes (2008), which matters for whether a Flores outgroup can root a "Timor" clade;
  - Klamer, Reesink and van Staden (2008) on East Nusantara as a linguistic area;
  - Schapper (2020) on sound changes spreading across eastern Timor;
  - Hull (2001b) on the Timoric Sprachbund.
- **Tetun and Welaun:** Hull (2003) on Welaun (Bekais); van Klinken (1999); Williams-van Klinken, Hajek and Nordlinger (2002); Hajek (2006) on Tetun Dili and contact.
- **Borrowing and lexical phylogenies:** Greenhill, Currie and Gray (2009); Nelson-Sathi et al. (2011); Greenhill, Drummond and Gray (2010) on how robust Austronesian trees are; Bowern and Atkinson (2012).
- **Combining character types, and irreversible change:** Ringe, Warnow and Taylor (2002); Nicholls and Gray (2008) on the stochastic Dollo model.
- **Automatic cognate detection for phylogenetics:** Rama, List, Wahle and Jäger (2018).
- **Statistics and software:**
  - D statistic: Green et al. (2010); Durand et al. (2011).
  - ABC model choice: Robert et al. (2011); Csilléry et al. (2010).
  - Bayes factors and marginal likelihoods: Bergsten, Nilsson and Ronquist (2013); Kass and Raftery (1995); Xie et al. (2011).
  - Topology tests: Goldman, Anderson and Rodrigo (2000) for the SOWH test.
  - Delta scores and Q-residuals: Holland et al. (2002); Gray, Bryant and Greenhill (2010).
  - Leipzig-Jakarta list: Tadmor, Haspelmath and Taylor (2010).
  - Software: Ronquist et al. (2012); Minh et al. (2020); Hoang et al. (2018).
- **Grimes and Edwards (2026) beyond their sound changes.** Their lexical and morphosyntactic arguments are not discussed.
- **Hull's own work.** The classification being tested is known mostly at second hand:
  - Hull (1998) and Carvalho (2001) could not be obtained;
  - it is unclear whether Hull (2001) was read directly.

  A paper that tests Hull's grouping should say which of his works were read first-hand. It should also make every effort to obtain Hull (1998), whose lexical percentages can be compared directly with the paper's results.

---

## 3. Minor concerns

**Framing and wording**
1. **Title and abstract.** See M7. The Abstract also calls Lakalei-Idate + Eastern Timor "its eastern placement". Grimes and Edwards only allow that grouping as a possibility; their main claim, Lakalei-Idate within Timor-Babar, depends on the root (M1). Say so.
2. **Number of addenda.** The paper says "ten dated addenda", but `PROTOCOL.md` now has eleven; Addendum 11 governs analyses not in this version. Update the number or state the cut-off.
3. **History of the draft.** Phrases such as "The first version also read ...", "Calibration withdraws that reading" and Table 5's column "Limitation of the first version" describe an unpublished earlier draft that journal readers will not have. Move this history to a supplementary changelog and report the current analyses directly.
4. **"Misclasses"** (Table 5) should be "misclassifies".
5. **"Grimes and Edwards do not cite Hull"** (Introduction) is a fair statement of fact but would sit better in a footnote.
6. **Novelty claim.** "This is their first cognate-based phylogenetic placement" should read "to our knowledge". Edwards (2019) already gives lexical percentages for Welaun.
7. **Names and spelling.** Make these consistent and define each on first use: Idaté/Idate, Habu/Habun, Tetun/Tetum, Welaun/Bekais, Lakalei-Idate/Idalaka. Give Glottocodes in a table.

**Methods and data descriptions**

8. **Data section.** "Flagged and screened in sensitivity variants" is inaccurate:
   - Indonesian and Portuguese look-alikes (rules L3 and L4) are removed from the primary data, not only in variants;
   - V-contact removes only the Papuan-side forms of contact sets (Addendum 1.2).

   Say so.
9. **Missing methods detail:**
   - Give versions and citations for LingPy, MrBayes, IQ-TREE and SplitsPy.
   - Give MCMC lengths, priors, burn-in and the stepping-stone settings.
   - Explain how the 1,353 characters were built, including how missing concepts were coded.
   - Say whether IQ-TREE used an ascertainment-bias correction. MrBayes used coding=noabsencesites, but the IQ-TREE runs use GTR2+FO+G4 without +ASC. This affects branch lengths and therefore the simulators in E21, E31 and E32.
10. **UFBoot.** Say that UFBoot is not a standard bootstrap and that values below 95 are not conventionally read as support. Consider reporting SH-aLRT or the standard bootstrap alongside.
11. **The pre-registered rule.** It relies on UPGMA, which assumes a clock and is known to be misled by unequal rates in Austronesian (Blust 2000). The rule had little chance of resolving higher-level groups; say so when interpreting "unresolved".

**Tables and figures**

12. **Table 2.**
    - The row label "C1: Hull's Ramelaic" conflates the contrast with one clade.
    - "0.13 as drawn (without Welaun)" is awkward.
    - Add the posterior for Flores + Rote-Meto + Helong (0.95).
13. **Table 3.** Add columns for Lakalei-Idate + Eastern Timor and for Lakalei-Idate itself, and give the number of sound-change characters in each row.
14. **Table 4.** Give the prior median and interval in each row (M6). Report the random forest's posterior for the chosen model (0.625) as well as its votes.
15. **Table 5.**
    - The E27 row omits that Central Timor with Welaun gets 0% and Lakalei-Idate 6%.
    - It also omits that against Habu the stable-concept pairing ties (26/26), or loses under R2 (21/25).
    - The E35 row should say "at least 6 of 24".
16. **Table 6.** The "Reading" column asserts contact ("with a Tetun layer"; "the Tetun link is in borrowable words"). As the caption says, none of these excesses survives correction, and the test is uncalibrated for these triplets. Reword them under the paper's own E25 rule.
17. **Figure 2.** Show where Sika attaches and the 0.95 split. Consider an unrooted display or a NeighborNet beside the rooted cladogram.
18. **Figure 3.** Print token counts in the cells, and check that the colours are distinguishable for colour-blind readers.
19. **Figure 4.** Correct the caption: the counts are summed over combinations of lects. Overlay the E31 null intervals so readers can see that only Welaun stands out.

**Specific statements in the results**

20. **Split test (Section 6).**
    - "binomial p = 0.11" is the test over all concepts (8 against 2); the test on borrowable concepts only (6 against 1) gives p = 0.125.
    - Also report the sensitivity run with Idaté-Cribas. On stable concepts it gives 3 sets shared by both, 4 in Lakalei only and 2 in Idaté only, which weakens the "old layer" reading.
21. **Section 7.**
    - "LI+NCT beats LI+Tetun on the pooled lists (36 to 29)" omits that NCT + Tetun is also 36, so under R2 there is no single tree pair.
    - "Replicates against Habu and Kawaimina in every combination" holds under R0 only; under R2 the share against Habu is 94%.
22. **Log-likelihood differences.** The repository gives 10.4, 10.5 and 10.6 for the same comparison (from the AU re-optimisation and from the search log-likelihoods), and 11.7 against 12.0 for Timor-Babar. State which value is used and why they differ.
23. **Table 1** lists ASJP and Alcantara as "independent checks", but the outcome of E14 (uninformative, with Idaté nearest Habu) is not reported. Report it or drop the row.

**Citations, archiving and length**

24. **Citations.**
    - Cite the Leipzig-Jakarta list to Tadmor, Haspelmath and Taylor (2010) as well as Tadmor (2009).
    - Check that Edwards (2021, *Rote-Meto Comparative Dictionary*) is the right source for the Central Timor/Timor-Babar classification; the protocol cites the Glottolog coding and an Edwards and Grimes (2021) item.
    - Give LexiRumah's full citation and DOI.
    - Archive the repository, for example with a Zenodo DOI.
25. **Length.** The paper fits 36 analyses into 13 pages, so several (E19, E21, E23, E33) get one sentence each. Move the uninformative analyses to a supplement and expand the decisive ones: the root, the decisive cognate sets, and whether Lakalei-Idate holds together.

---

## 4. Number check

I checked the numbers below against the result files. "OK" means the paper's value matches the file to the stated rounding.

| # | Paper's statement | File and value | Verdict |
|---|---|---|---|
| 1 | ln BF for C1 is +8.0 | `bayes/bayes_factors.json`: 8.02 | OK |
| 2 | ln BF for C2 is +10.3 | `bayes/bayes_factors.json`: 10.25 | OK |
| 3 | ln BF for Timor-Babar is −7.0 | `bayes/bayes_factors.json`: −7.02 | OK |
| 4 | Posteriors 0.13 / 0.86 / 0.91 / 0.00 | `bayes/posterior_clades.json`: 0.132 / 0.864 / 0.905 / 0.0 | OK |
| 5 | Stepping-stone runs agree within 0.8 log units | largest gap is in c1pos: −8091.93 against −8092.72, i.e. 0.79 | OK |
| 6 | Split-frequency difference 0.005; minimum ESS 1,074 | `unconstrained.log`: 0.005474; `.pstat` minESS 1073.5 | OK |
| 7 | 1,353 characters | `matrix.nex`: nchar=1353 | OK |
| 8 | B-cubed F 0.81 (P 0.88, R 0.75); Mantel r 0.90 | `scores/bcubed.json`: 0.8118 / 0.8789 / 0.7542; `gate.json`: 0.898 | OK |
| 9 | Mean delta 0.24 (37 lects) and 0.33 (24 lects) | `network/treelikeness.json`: 0.2404 / 0.334 | OK |
| 10 | Most reticulate lects: Welaun, Tokodede, Galoli, Lakalei, Idaté, Habu | `per_lect_delta_timor_an.csv`: Welaun-Mahein ranks 3rd; Tetun Dili 6th (0.293, above Idaté); Tetun Suai 0.2833, level with Habu 0.2834 | Selective (Tetun omitted) |
| 11 | Ramelaic 88% to 95% with Tetun look-alikes removed; Fabronic, Timor-Babar and Eastern Timor 0% to 3% | `summary_d1_lexstat.csv`: 0.876 / 0.951; highest of the others 0.030 | OK |
| 12 | "The gate passed under an addendum adopted before any contested clade was scored" | `gate.json`: `passed_under_v1_rules` false; G1 missed KA2-TAP | Incomplete |
| 13 | "The Bayesian analyses, which the rule did not use for the decision" | Protocol step 8 includes a Bayes factor condition | Inaccurate |
| 14 | Table 3: 65, 56, 80, 75, 0.88, 57 | `total_evidence/iqtree_support.json`, `mrbayes_posterior.json`, `innovation_support.json`, `e13`: 65, 56, 80, 75, 0.884, 57 | OK |
| 15 | Parsimony 30 / 30 / 29 steps; Grimes and Edwards's split costs 12 log-likelihood units | `e29_sound_fit.json`: 30 / 30 / 29; −11.97 | OK as computed (see M2) |
| 16 | Idaté \*j > r in 5 of 12 tokens; \*d > r, l in 8 of 9 and 5 of 7 | `e29` (E29b): 5/12; 8/9; 5/7 | OK |
| 17 | LI + CT 92% (SCA), 65% (primary), 15% to 20% (thresholds 0.35 and 0.75); LexiRumah cognates give LI + Habu 51% and Mantel r 0.70 | `e15_coding_robustness.json`: 92 / 65 / 15 / 20; node with 51 in `e15/lex_biglexstat.contree`; Mantel 0.696 | OK |
| 18 | 7 exclusive LI + CT innovations against 9 eastern; "one of the seven, 'wife'" is a retention | `e17_innovations.json` (R0): 7 against 3+3+2+1 = 9. The chosen R2 rule gives 6 against 9. The seven include 'tail' (tail-1644), which R2 and the strict ACD check both class as inherited, two 'wife' sets, and 'who' (ʔɛta ~ sepdua) | Discrepancy: at least two of the seven are retentions; the chosen rule gives 6, and 5 after E35 |
| 19 | Welaun triplet Z 6.9 (borrowable) and 0.6 (stable) | `e18_triplets.json`: 6.89 / 0.55 | OK |
| 20 | Null D 0.44 to 0.47; observed 0.12 to 0.65; Z ≥ 2 fires in 27% of null runs; Welaun's Z beyond 99.8% of the null; 5% false positives and 30% power at 20% borrowing | `e31`: 0.438–0.467; 0.12–0.65; 0.268; `p_upper_Z` 0.002; 0.054; 0.30 | OK (but Welaun's D itself has p = 0.15) |
| 21 | Split test: 5 of 8 stable items shared by both; 6 of 8 borrowable items in Lakalei only; p = 0.11 | `e20_split_test.json`: 5/2/1 and 1/6/1; p = 0.109 for all concepts, 0.125 for borrowable only | Minor mislabel |
| 22 | E21: 0.125 / 0.875; 16% (1–41%); 28% (4–53%) | `e21_borrowing_abc.json`: 0.125 / 0.875; 0.161 (0.01–0.407); 0.276 (0.041–0.531) | OK (prior median is 0.30) |
| 23 | E32: forest votes 0.45 / 0.55; rejection posterior 0.42 / 0.58; 24% (4–52%) and 25% (4–55%); 0 and 0 failed checks; prior error 36% | `e32_abc2.json`: 0.454 / 0.546; 0.417 / 0.583; 0.241 (0.042–0.521); 0.254 (0.038–0.552); 0 / 0; 0.355 | OK |
| 24 | The unconstrained tree is better by 10.5 log units; AU p = 0.07 | `ml/summary.json`: −8560.15 against −8570.69, a gap of 10.55; `au_test.csv`: p-AU 0.0707 (gap 10.36 after re-optimisation) | OK (the repository reports this gap as 10.4, 10.5 and 10.6 in different places) |
| 25 | Glottometry σ: 1.42; 0.06 with Central Timor; 0.08 with Eastern Timor; 0 for Ramelaic | `e22_glottometry.json`: 1.42 / 0.06 / 0.08 / 0.0 | OK |
| 26 | Rooted clock: 77% Central Timor side, Habu 11%, heights 0.48 against 0.47; earlier run 80%, 0.29 against 0.27 | `e34`: 0.486 + 0.258 + 0.025 = 0.769; 0.106; 0.475 / 0.465. `e23`: 0.291 / 0.274 | OK; the 80% cannot be verified (`e23_dating.json` stores no sister distribution) |
| 27 | E25: 40 tests, only Welaun survives | `e25_multiple_testing.json`: 40 tests; the only Holm survivor is the Welaun borrowable-word test | OK |
| 28 | E26: 100% against Habu and Kawaimina, 47% against Tetun; 84% for Tetun Dili | `e26_dialect_replication.json`: 1.0 / 1.0 / 0.473; the Tetun Dili breakdown is not stored | OK; the 84% cannot be verified |
| 29 | E28: 97%; Timor-Babar and LI + Eastern Timor 0%; 45 to 44; Lakalei inside Nuclear Central Timor 94%; Tetun Dili + Suai 100% | `e28_independent.json`: 97 / 0 / 0; stable LI+Tetun 45, LI+NCT 44; node support 94 in the treefile; `e28b`: 100 | OK |
| 30 | E27: LI + Nuclear Central Timor 55%; Timor-Babar and LI + Eastern Timor 0% | `e27_consensus.json`: 55 / 0 / 0; also Central Timor with Welaun 0 and Lakalei-Idate 6, both unreported | OK but selective |
| 31 | E30: 3,801 forms; balanced accuracy 0.755 → 0.791 | `e30_classifier.json`: 3801; 0.7546 → 0.7914 | OK |
| 32 | R2: 36 to 29 on the pooled lists; 47% → 79% | `e35` (R2, ABVD forms only, single-survey lists, stable): 36 / 29 / 36, so NCT + Tetun also has 36; `e26_r2`: 0.789 | The tie with NCT + Tetun is omitted |
| 33 | E35: 55 sets (strict), 126 (loose); 19 to 9; 6 of 24 | `e35` strict: 55 moved; loose: 126; representative lists with ACD, stable: 19 / 9 / 6; 6 packet sets reclassified | OK |
| 34 | E36: gap 19.5, p = 0.025; gap 14.8, p = 0.042 | `e36_au_independent.json`: 19.48 / 0.0248; 14.761 / 0.042 | OK (not corrected across E6 and E36) |
| 35 | Table 6 counts (all five triplets) | `e24_other_branches.json`: all match | OK |
| 36 | Data: 257 tables and 14,401 forms; 94% agreement (249 of 264); 998 trees | REPORT and `derived/README.md`: 249/264; `gray2009_timor_clades.json`: 998 | OK |
| 37 | "Ten dated addenda" | `PROTOCOL.md` contains Addenda 1 to 11 | Out of date |

**What the check shows.** The arithmetic is very clean: 30 of the 37 items match the files exactly or to rounding. Where there are discrepancies, they come from what is reported and what is left out, not from miscalculation:
- the count of exclusive Lakalei-Idate + Central Timor innovations (item 18);
- the tie omitted from the pooled-list triplet under R2 (item 32);
- the E27 values left out (item 30);
- the Tetun lects left out of the reticulation list (item 10);
- how the gate and the decision rule are described (items 12 and 13).

Two numbers cannot be checked against the stored outputs: the 80% in item 26 and the 84% in item 28.

---

## 5. Recommendation: major revision

**What is publishable now.**
- The submission is unusually transparent. Data, code, protocol and every deviation are public, and the arithmetic checks out almost everywhere.
- Several of its products are useful to the field:
  - the machine-readable Grimes and Edwards tables;
  - the reflex atlases;
  - the calibration showing that a naive lexical D statistic is badly inflated by unequal rates of change.
- Two results could be published as they stand:
  - the pre-registered core result: the bootstrap rule cannot resolve C1 or C2;
  - the root-independent finding that Lakalei-Idate does not group lexically with Eastern Timor.

**Why the main interpretation does not hold.**
- The "lean towards Central Timor" rests on an unrooted lexical tree that is identical to Grimes and Edwards's tree rooted on the Central Timor stem.
- The evidence that seems to reject Timor-Babar measures where two Flores lects attach.
- The phonological evidence was set aside because of a coding choice. Once that is corrected, the change that defines Timor-Babar favours Grimes and Edwards.
- The shared-innovation evidence includes many retentions.

**What a revised version needs.**
1. Treat C1 as a question about the root, and estimate the root independently.
2. Re-run the sound-change comparison with the ancestral state fixed and with lenition treated as irreversible.
3. Have the decisive cognate sets checked by a specialist.
4. Rebuild the title and abstract around the pre-registered, unresolved result, and present the lexical findings as exploratory.
5. Cut the uninformative analyses.

If, after these steps, the lexical evidence still favours Central Timor under an independently estimated root, the paper would make a strong contribution. If it does not, a well-documented negative result is still worth publishing in this journal. I would like to see the revised version.
