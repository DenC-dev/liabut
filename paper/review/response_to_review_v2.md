# Response to the review of version 2

Version 3 (13 October 2026) restructures the paper around the review's main point. It does not add analyses indiscriminately; it shows more clearly what the existing analyses establish, why they disagree, and what follows. Two targeted sensitivity analyses the review asked for were declared first (PROTOCOL.md, Addendum 14) and run (E56, E57). Everything else is reorganisation, documentation and new tables built from existing results.

Items marked **Not done here** need people or data outside this project; the materials for each are in the repository.

## Novelty

- **First computational placement, first systematic cognate analysis, first classification.** The Introduction now separates the three. To our knowledge the six languages receive their first cognate-based computational phylogenetic placement here. Their first systematic cognate analysis is not new: LexiRumah codes them and Grimes and Edwards (2026) compare them by the comparative method. Nor is their first historical classification (Hull 1998, 2001a; Edwards 2019; Grimes and Edwards 2026).

## What the analyses establish

- **No more analyses indiscriminately.** Only E56 and E57 were added, both requested. The main text now has one primary analysis, the second-round rule, with six robustness checks. The other exploratory results moved to a separate Supplement (8 pages) with a register of every analysis and where it is reported.
- **Prominent table of analysis classes.** Table 2 separates the original pre-registered tests, the pre-declared replications, the second-round analyses and the exploratory analyses, with what each can establish.
- **One principal table.** Table 12 sets the two classifications against the main lines of evidence, with the class of each.
- **Multiple testing.** A short paragraph in the Design section summarises the three families of tests and their corrections, and states that no conclusion rests on an uncorrected p-value.
- **Bayes factor of +11.8 against the corrected AU tests.** The Topology tests section now explains that they answer different questions. The Bayes factor compares two hypotheses under a model that treats every shared word as inherited, and small per-character advantages accumulate over 1,353 characters. The AU test asks whether the constrained tree is significantly worse, allowing for resampling and selection. They agree on the direction and differ on how far it survives sampling variation.
- **Show, suggest, unknown.** The abstract and the Discussion are now organised around these three, in the review's terms.
- **Title.** Now "Where do Idaté and Lakalei belong? A pre-registered lexical-phylogenetic test of two classifications of Timor's Austronesian languages".

## The cognate evidence

- **Independently reviewed decisive comparisons. Not done here.** `derived/audit/decisive_comparisons.csv` lists all 47 decisive sets on both sides, with forms, etyma, Grimes and Edwards's treatment, the correspondence result and every audit entry, plus blank columns for a specialist. `SPECIALIST_REVIEW.md` explains what is needed.
- **Explicit regular correspondences. Partly done.** E52 tested regular correspondences in the decisive sets and found too few in these 152-concept lists to classify them, which the paper now reports in the main text. **Reconstructed forms are not supplied.** The table has a `Reconstruction` column for the specialist rather than guessed proto-forms.
- **Audit trail for exclusions.** `derived/audit/exclusions.csv` gives every excluded or reclassified form and set (4,527 rows) with a reason code: Indonesian, Portuguese and Tetun look-alikes (with the sound-change verdict on each Tetun case), Papuan-contact screening, Papuan-shared sets, review flags, Austronesian Comparative Dictionary and Grimes and Edwards retentions, coding errors, doubtful sets and polarisation. The codes are defined in `DATA_DICTIONARY.md`.
- **Retentions against innovations.** The Methods and the section "Shared retentions and shared innovations" now state which comparisons can support a subgroup and which only show that older vocabulary was preserved, with examples of each kind of reclassification.

## The sound changes

1. **Fuller table of reflexes and environments.** Table 9 gives every \*p reflex for the focal languages by environment (word-initial, between vowels, before \*u), from both atlases; the full token list is `derived/audit/p_reflexes.csv`. It also shows that \*palu 'hit', earlier read as a counter-example, has b in the eastern languages too and counts for neither side.
2. **Competing explanations.** Table 10 evaluates shared innovation, independent change, restoration and diffusion against the reflexes. Restoration is implausible. Independent change has demonstrably happened (Welaun). Shared innovation and diffusion cannot be told apart with these data.
3. **Reversibility sensitivity (E56).** Table 11 scores the three trees with the cost of restoring \*p from a tenth to a thousand times the cost of losing it. For \*p lenition the trees tie up to equal costs, and Grimes and Edwards's tree wins from twice the cost upwards. Over all characters the lexical tree is never the cheapest.
4. **Why the comparative method's evidence counts differently.** A new paragraph in the Discussion explains why one regular, directional sound change and 1,353 presence-absence characters cannot be weighed by counting, and why the sound-change evidence here is strong in kind but thin in amount.

## The root

- **Choice of outgroups.** The Methods now justify the three kinds of outgroup against the usual criteria (outside the ingroup, close enough to share cognates, free of its contact history), and say which criterion each kind meets.
- **The reconstruction as a pseudo-taxon.** The Methods now set out the risks: circularity, no borrowing or gaps, one etymon per meaning, and a pull towards conservative lineages. The PMP-only rooting is read only as a check.
- **Outgroup and missing-data sensitivity (E57).** Nine runs, each leaving out one outgroup (PMP included), coding missing data as absence, or keeping only concepts attested in all seven outgroups. The root never falls on the Central Timor stem (0.00 in every run). Whether it falls on the Flores or the Rote-Meto branch depends on these choices, and the rooted clade ranges from 0.86 to 0.98.
- **Rooted lexical clade against inherited subgroup.** The Root section now says explicitly what a rooted lexical clade does and does not establish.

## Before publication

- **Clean, documented workflow.** `reproduce.sh principal` rebuilds every estimate in the main text from the stored codings and tree samples, plus the figures, both PDFs and the website. `reproduce.sh full` reruns everything from pinned upstream data. `results/principal_estimates.csv` traces each main-text estimate to its file and key.
- **Data dictionary.** `DATA_DICTIONARY.md` covers every lect (with list sources), dataset, cognate assignment, character coding, retention status and exclusion code.
- **Provenance and permissions.** `PROVENANCE.md` gives sources, commits, licences and uses. All lexical data are CC BY 4.0 except Alcantara's (2015) forms, which are flagged.
- **Comparison with the 494-item field lists. Not done here.** They are not public; the paper says the comparison should be made if they become available.
- **Independent replication. Not done here.** `REPLICATION.md` sets out what to rerun, what to compare and the tolerances that count as agreement.
