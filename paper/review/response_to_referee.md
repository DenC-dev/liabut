# Response to the referee (mock review, version 1 → version 2)

The referee's report is `paper/review/referee_report.md`. Every new analysis was declared in Addendum 12 of `PROTOCOL.md`, with a binding decision rule for C1, and pushed before it was run (commit `808b471`). Results are in `results/literature/e40*` to `e50*`, and are summarised in `results/LITERATURE.md` under "Eighth round".

## Major concerns

**M1. Rooting.**
- *What we did.* We estimated the root with seven outgroups beyond Flores, coded jointly with the Timor data (E40: Tagalog, Buginese, Uma; Kambera, Bima, Manggarai; PMP as a pseudo-taxon). We also ran a relaxed clock with and without Tela-Masbuar (E41), and repeated the AU tests with the outgroups holding the root and Lakalei-Idate kept together (E45).
- *Result.* The root falls on the Flores or the Rote-Meto + Helong branch in every analysis, never on the Central Timor stem (MrBayes with all seven outgroups: Flores 0.93, Rote-Meto + Helong 0.07; relaxed clock: Rote-Meto + Helong 0.42 to 0.52, Flores 0.11 to 0.23, Central Timor stem 0.00), so Lakalei-Idate + Central Timor is a rooted clade (0.96 to 1.00) and Timor-Babar never is. Even so, no topology test rejects any placement once corrected over all eleven tests.
- *Paper.* C1 is now framed as partly a question about the root, the Flores pair's attachment (0.95) is reported, and the Timor-Babar Bayes factor is explained.

**M2. Sound changes.**
- *What we did.* We re-scored the eleven characters with the Flores pair coded from the atlases (\*p retained) under Fitch, Camin-Sokal and Dollo costs (E42).
- *Result.* Under irreversible change, \*p lenition needs 6 origins on the lexical tree, 4 on G and 2 on GE, which is the referee's count. The totals are mixed.
- *Paper.* We restored the comparative-method evidence (E2, E2b, Grimes and Edwards's native cases, \*ŋ > g, \*ma-p) and applied one standard to every diagnostic. We dropped the equal-weight combined analyses from the main text.
- *Calibration (E43).* MrBayes recovers 6 of 10 undisputed sound-change groups at 0.95, and ML recovers 4.

**M3. "Leans Central Timor".** The claim is withdrawn.
- *What we did.* We kept Lakalei-Idate together and also analysed each member alone (E44).
- *Result.* Kept together, it joins Central Timor at 70% (primary) and 98% (independent). Lakalei alone is Central Timor-like; Idaté alone leans partly towards Habu (38%).
- *Decision rule.* By the Addendum 12 rule, C1 is unresolved by the vocabulary.

**M4. Retentions among the "innovations".**
- *What we did.* We reclassified 66 sets: the referee's list, E35 strict and E37 (E46). The Central Timor exclusive sets drop from 6 to 2. The eastern exclusive sets (9) have had automatic checks only, which the paper says.
- *Packet.* A second reviewer packet covers the exclusive sets on both sides (`derived/innovations/reviewer_packet_exclusive_sets.csv`).

**M5. Triplet test.**
- *Polarisation (E46).* We polarised the test by outgroups, in two ways: all nine outgroups on the E40 coding, and the referee's Flores, Rote-Meto + Helong and Wetar on the primary coding. Cleaned and polarised, the pairing loses to Habu on the representative lists.
- *Calibration.* We calibrated the tree-pair rule under H and G with no borrowing: it holds in 21% (H) against 3% (G), or 15% against 5% when polarised.
- *Paper.* Counts are now described as summed over combinations of lects, and the false-positive and power figures are given in the main text.

**M6. ABC.** The priors are now given next to the posteriors, and E21 is moved out of the main text. The pre-declared readings are reported, together with why they are uninformative. The paper presents the ABC as unable to separate the placements, with the reasons the referee gives.

**M7. Pre-registration.**
- *Framing.* We retitled the paper "with a pre-registered core". The Abstract now opens with the pre-registered verdict and the failed predictions.
- *Deviations.* A table of deviations is in the Methods. It covers the gate under v1, the analyst not being blind, BEAST2 replaced by MrBayes, forced-against-forbidden runs and 50 stones, step 8's Bayes factor condition, and C2.
- *Statistics.* Holm's correction now runs across all eleven topology tests, and nothing is rejected.
- *Second round.* We ran the pre-registered second round with a decision rule, as the referee suggested.

**M8. Bayes factors.** The caption now explains them, citing Bergsten, Nilsson and Ronquist (2013). Direct stepping-stone comparisons (E47): Lakalei-Idate + Central Timor against Lakalei-Idate + Eastern Timor, ln BF +11.8; Central Timor with Welaun against Welaun + Tetun, +7.6. The SOWH tests (E38) reject the eastern placement on both matrices (p = 0.01). Neither overrides the corrected AU result in the decision rule.

**M9. C2.** The paper now reports all C2 results, including those against Central Timor. C2 is rephrased as "consistent with Edwards (2019) once borrowable vocabulary is set aside", and Hull (2003) is cited.

**M10. Alternative explanations.** The new analyses:
- With Tetun removed, Lakalei-Idate + Central Timor gets 94% (E48a).
- With the 132 Papuan-shared sets removed, it gets 46% (E48b). Central Timor and Lakalei-Idate share more sets with Papuan lects than Eastern Timor does.
- Glottometry with resampling intervals (E50) gives 0.06 (0 to 0.31) against 0.08 (0 to 0.41).

The Discussion now treats linkage, the Sprachbund (Hull 2001b; Schapper 2020) and unequal rates (Blust 2000).

**M11. Treelikeness and dating.**
- *Treelikeness.* The 24-taxon results are labelled weak, as the protocol requires, and the reticulation list now includes the Tetun lects.
- *Dating.* Node heights are now computed only where the clades exist (E49). Lakalei-Idate + Nuclear Central Timor is older than Nuclear Central Timor by a median of 21% of the latter's height. The "barely older" sentence is removed. Under the relaxed clock the gap is 21% of Central Timor's height (95%: 4 to 71%). Dropping Tela-Masbuar moves root mass from Kisar-Luang to the western branches (E41).

**M12. Literature.** Added: Donohue and Grimes (2008), Hull (2001b, 2003), Blust (2000), Ross (1988), François (2014), Heggarty et al. (2010), Klamer, Reesink and van Staden (2008), Schapper (2020), Hajek (2006), Williams-van Klinken et al. (2002), Greenhill, Currie and Gray (2009), Ringe, Warnow and Taylor (2002), Nicholls and Gray (2008), Rama et al. (2018), Green et al. (2010), Durand et al. (2011), Robert et al. (2011), Csilléry et al. (2010), Bergsten et al. (2013), Goldman et al. (2000), Holland et al. (2002), Gray, Bryant and Greenhill (2010), Tadmor, Haspelmath and Taylor (2010), Ronquist et al. (2012), Minh et al. (2020), Hoang et al. (2018). Hull (1998) and Carvalho (2001) are still unobtainable, and the paper says which of Hull's works were read.

## Minor concerns

These are addressed as listed, with the following exceptions:

- Figure 3 token counts (minor 18) remain in the repository.
- No Zenodo DOI yet (minor 24). `CITATION.cff` and `.zenodo.json` are added, and the GitHub–Zenodo link needs enabling by the repository owner.
- Two numbers that could not be verified are now stored: the E23 sister distribution (81% on the Central Timor side) and the E26 Tetun Dili breakdown (84%).
