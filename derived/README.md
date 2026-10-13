# Derived datasets

These datasets were built for Liabut's expansion (Addendum 4 in `PROTOCOL.md`). None of them existed in machine-readable form before. Each folder says where its data come from and how to cite it.

## `ge2026_tables/`: the comparative tables of Grimes and Edwards (2026)

Grimes and Edwards print their evidence as tables. Each has a gloss row and a PMP row with the target segment in bold red, then one row per language, with the reflex in bold red and non-cognates greyed out. This folder turns those tables into data.

| File | Contents |
|---|---|
| `forms.csv` | One row per language form. Covers 257 comparative tables, 250 of which have language rows, and 14,401 forms, 12,537 of them marked cognate. Each row has the gloss, the PMP etymon (with the target marked `⟦ ⟧`), the form (with the authors' highlight marked `⟦ ⟧`) and the cognacy flag. |
| `reflexes.csv` | One row per highlighted target: PMP segment → reflex. |
| `languages.csv` | The 328 row labels, mapped to 207 Glottocodes through the book's Appendix A plus an alias list. That covers 93% of forms. |

- **Built by** `src/18_ge_tables.py`, from the book's LaTeX source (github.com/langsci/526, commit 9169a5c of 18 March 2026).
- **Table labels.** `Table` is the book's own label (`03-28` is Table 3.28). Six tables have no label and are identified by file and character offset. Until 13 October 2026, 13 tables whose captions contain environment notation had a wrong label (`\#` or `\gap`) and a truncated caption; the forms themselves were unaffected (results/LITERATURE.md, eleventh round).
- **Licence.** CC-BY 4.0, following the book. Cite: Grimes, Charles E. and Owen Edwards. 2026. *The Austronesian languages of eastern Indonesia and Timor-Leste: Unravelling their prehistory and classification*. Berlin: Language Science Press.
- **What the data mean.** The highlights are the authors' judgments. Errors in parsing or mapping are ours.

## `reflex_atlas/`: reflexes of PMP consonants, language by language

| File | Contents |
|---|---|
| `expert_tokens.csv`, `expert.csv` | 8,426 tokens of PMP target segments in cognate forms from the tables above. They are summarised per language, target and position into 2,593 cells across 186 languages. `Source = highlight` means the authors marked the reflex (6,130 tokens). `Source = aligned` means it was read off an alignment because the row wasn't highlighted (2,296 tokens). |
| `automatic_tokens.csv`, `automatic.csv` | 4,978 tokens from LexiRumah: 64 Austronesian lects and 146 concepts, aligned to ABVD Proto-Malayo-Polynesian forms. |
| `agreement_tokens.csv` | The automatic reflex compared with the authors' highlighted reflex for the same word. They agree on **94%** of tokens (249 of 264): *p 49/51, *ŋ 30/32, *b 86/93, *j 29/32. |

- **Built by** `src/19_reflex_atlas.py`.
- **Reflex classes** follow place of articulation and ignore voicing (Addendum 4, A4.1).

## `sound_change_matrix/`: sound-change characters

| File | Contents |
|---|---|
| `innovation_profiles.csv` | Eight diagnostic changes (A4.4), coded 1, 0 or ? for 65 Timor-region languages, with token counts. |
| `innovation_matrix_24.csv` | The same characters for the 24 taxa used in the Bayesian analyses. |
| `characters_*.csv`, `matrix_*.csv`, `phon_*.phy` | Multistate characters (E10): one per PMP target, and one per target and position. |
| `hull_ramelaic_profiles.csv`, `innovation_matrix_24_hull.csv` | Three more characters (Addendum 5, E13): word-initial *b > h; initial and medial *k loss. Each cell is flagged by whether it comes from the expert or the automatic atlas. |

- **Built by** `src/20_total_evidence.py`, `src/21_innovations.py` and `src/25_literature_checks.py`.

## `loans/`: loans identified by sound change

| File | Contents |
|---|---|
| `tetun_loans.csv` | 740 Tetun look-alikes in non-Tetun Timor lects. 21 are classed as probable loans, 15 as probably inherited and 704 as undecidable, by checking each form's reflexes against the lect's own regular reflexes and Tetun's (E12). |
| `central_timor_in_lakalei_idate.csv` | The same test on 104 Lakalei-Idate forms that share a cognate set with Central Timor but not with Tetun (E12b). |
| `lakalei_idate_central_timor_exclusive_sets.csv` | 10 cognate sets found only in Lakalei-Idate and Central Timor, with Tetun, Habu and Kawaimina forms for comparison. |

- **Built by** `src/22_tetun_loans.py` and `src/23_ct_loans.py`.
- **How far to trust it.** The loan classes are a heuristic. Grimes and Edwards confirm some of them, such as Welaun *nani* 'swim' (a probable loan), but the classifier has not been validated against expert loan judgments.

## `alcantara2015_idate/`: Idaté word list from Alcantara (2015)

184 Idaté forms from a phonological description based on fieldwork in Laclubar, with concept mapping and aligned PMP tokens (Addendum 6, E16). See the folder's own README for the source, corrections and rights.

## `innovations/`: retention or innovation status of cognate sets

`cognate_set_status.csv` lists every D1 LexStat cognate set, among the Austronesian lects, for concepts with an ABVD Proto-Malayo-Polynesian form. Each set is classed as a **retention** (a form within SCA NED 0.5 of PMP) or an **innovation** (the PMP word was replaced). The file gives the set's lects and forms.

- **Built by** `src/28_innovations_contact.py` (Addendum 7, E17).
- **Accuracy.** The rule is strict, so some heavily changed retentions are counted as innovations (for example, 'tail' *hiʔor* < *ikuR).

Addendum 9 adds two files here:

- `innovations/cognate_set_status_r2.csv`: the same classification with the reflex-aware rule chosen in E30 (balanced accuracy 0.791 against ABVD's experts, against 0.755 for the original rule).
- `innovations/reviewer_packet_lakalei_idate_stable.csv`: the 24 cognate sets behind Lakalei-Idate's stable-vocabulary triplet counts, with forms, PMP etyma, status and how far the five codings agree, plus blank columns for a specialist's verdict. Addendum 10 added the closest Austronesian Comparative Dictionary etymon for each set (PAN to PCMP), under the declared and the strict gloss match, with the resulting status.
