# Data dictionary

This file describes every lect, character, cognate assignment and exclusion code used in Liabut's analyses. Paths are relative to the repository root. Provenance and licences are in [`PROVENANCE.md`](PROVENANCE.md).

## Datasets

| Name | What it is | Where |
|---|---|---|
| D1 | LexiRumah 3.0.1: 70 lects of the Timor region (Austronesian and Papuan), 152 concepts, 10,555 forms | `data/d1/` |
| D2 | ABVD: 30 Austronesian lists with expert cognate judgements, used to score the automatic cognates and the retention rule | `data/d2/` |
| Outgroups | Seven ABVD lists coded together with D1 for rooting (E40, E57): Tagalog, Buginese, Uma, Kambera, Bima, Manggarai, and Blust's Proto-Malayo-Polynesian | `results/literature/e40/outgroup_forms.csv` |
| Expert atlas | The reflexes Grimes and Edwards (2026) mark in their 257 comparative tables | `derived/ge2026_tables/`, `derived/reflex_atlas/expert*.csv` |
| Automatic atlas | D1 forms aligned to ABVD's PMP forms | `derived/reflex_atlas/automatic*.csv` |

## Lects

`data/d1/lects.csv`

| Column | Meaning |
|---|---|
| `ID` | LexiRumah lect ID. A suffix (for example `-Slete`) picks one dialect list of a language |
| `Name` | LexiRumah name |
| `Family` | Austronesian or Timor-Alor-Pantar |
| `Glottocode` | Glottolog 5.3 code |
| `Latitude`, `Longitude` | LexiRumah coordinates (used for the maps only) |
| `Group` | LexiRumah's group label |
| `Role` | `Timor AN` (37 Austronesian lists from Timor), `Outgroup AN` (24 lists from Rote, Wetar, Luangic-Kisaric and Babar), `Root AN` (3 Flores-Lembata lists, the pre-registered root), `TAP` (6 Papuan lists, used only for loan screening and E48) |
| `Concepts` | Number of the 152 concepts attested |

### The 24 lects in the model-based analyses

One list per language, chosen by the rule in PROTOCOL.md step 7 (most concepts; ties to the list collected independently of Grimes and Edwards). The "independent lists" variant (E28, E36, E44) swaps in other collectors' lists where they exist; see `src/34_addendum9.py` (`SWAP`, `DROP`).

| ID | Language (lect) | Grimes and Edwards group | LexiRumah group | Concepts | Main list source |
|---|---|---|---|---|---|
| `mamb1306-Slete` | Mambae (South Mambae, Letefoho) | Central Timor | Mambae | 148 | fogaca17, grimes14 |
| `kema1243-kaila` | Kemak (Kailaku) | Central Timor | Kemak | 150 | edwards18-kemak |
| `tuku1254` | Tokodede | Central Timor | Tokodede | 140 | klamer02 |
| `west2547-welaun` | Welaun | Central Timor | Welaun | 150 | edwards18-welaun |
| `idat1237-cribas` | Idaté | Lakalei-Idate | Idate | 146 | dawson14 |
| `laka1255` | Lakalei | Lakalei-Idate | Lakalei | 140 | klamer02 |
| `tetu1245-suai` | Tetun (Suai) | Eastern Timor | Tetun | 127 | klamer16 |
| `habu1241` | Habu | Eastern Timor | Habu | 146 | dawson14 |
| `waim1252` | Waima’a | Eastern Timor (Kawaimina) | Kawaimina | 150 | himmelmann06 |
| `midi1237` | Midiki | Eastern Timor (Kawaimina) | Kawaimina | 146 | dawson14 |
| `naue1237` | Naueti | Eastern Timor (Kawaimina) | Kawaimina | 140 | veloso16 |
| `galo1243` | Galoli | Wetar-Atauro | Galoli | 122 | Cristo12, cristo11 |
| `dadu1237` | Dadu’a | Wetar-Atauro | Dadu'a | 142 | penn06 |
| `funa1237` | Helong (Funai) | Helong | Helong | 150 | edwards18 |
| `koto1251` | Amarasi (Kotos) | Meto (Rote-Meto) | Meto | 150 | edwardsbani17 |
| `term1237` | Termanu | Rote (Rote-Meto) | Rote | 146 | fox95 |
| `dela1252` | Dela | Rote (Rote-Meto) | Rote | 139 | tamelan16 |
| `ilma1240` | Ili’uun (Ilmaumau) | Wetar-Atauro | Wetar | 141 | hinton00 |
| `kaha1239` | Tugun | Wetar-Atauro | Wetar | 141 | hinton00 |
| `kisa1266` | Kisar | Kisar-Luang | Luangic-Kisaric | 145 | taber93 |
| `luan1264` | Luang | Kisar-Luang | Luangic-Kisaric | 145 | taber93 |
| `tela1241` | Tela-Masbuar | Babar | Babar | 145 | taber93 |
| `lama1277-lewoi` | Lamaholot (Ile Mandiri, Lewoingu) | Flores-Lembata (first root) | Flores-Lembata | 152 | klamer15 |
| `sika1262-hewa` | Sika (Hewa) | Flores-Lembata (first root) | Flores-Lembata | 152 | fricke14, keraf1978 |

Group abbreviations used throughout: **CT**, Central Timor (Mambae, Kemak, Tokodede, Welaun); **NCT**, Nuclear Central Timor (CT without Welaun); **LI**, Lakalei-Idate; **ET**, Eastern Timor (Tetun, Habu, Kawaimina); **TB**, Timor-Babar (everything in the Timor region outside CT); **RMH**, Rote-Meto + Helong.

## Concepts and forms

`data/d1/concepts.csv`: `ID` (LexiRumah concept ID), `English`, `Indonesian`, `Concepticon_ID`, `Semantic_Field`. The 60 Leipzig-Jakarta concepts (Tadmor 2009) mapped through Concepticon are the **stable** concepts (`data/screen/leipzig_jakarta_tadmor2009.tsv`); the other 92 are **borrowable**.

`data/d1/forms.csv`: `ID` (form ID), `Lect_ID`, `Concept_ID`, `Value` (as published), `Form` (normalised IPA), `Segments` (space-separated tokens; `+` marks a morpheme boundary, `_` a word boundary), `Source` (LexiRumah source key for the collector's list).

## Cognate assignments

| File | Columns | Method |
|---|---|---|
| `results/cognates/d1_lexstat.csv` | `Form_ID`, `Lect_ID`, `Concept_ID`, `Cognateset_ID` | Primary coding: LingPy LexStat, threshold 0.55, Infomap, 1,000 scorer runs, seed 1234 |
| `results/cognates/` (other files) | same | SCA (0.45) and LexStat at 0.35 and 0.75 (E15) |
| `results/literature/e27/consensus_cognates.csv` | same | Consensus coding (E27) |
| `results/literature/e40/cognates_lexstat.csv` | same | Primary method on D1 plus the seven outgroups together (E40, E57) |
| `results/literature/e51/partial_cognates.csv` | adds `Morpheme`, `Segments` | LingPy Partial, morpheme-level sets (E51) |

`Cognateset_ID` is `<concept>-<cluster number>`. A set is internal to one concept.

## Lexical characters

`results/bayes/characters.csv` (`Index`, `Cognateset_ID`, `Concept_ID`) lists the 1,353 binary characters of the 24-lect matrix in column order; the matrices themselves are the `.phy` and `.nex` files beside each analysis.

- **Coding.** `1` the lect has a form in the set; `0` the lect has the concept but no form in the set; `?` the lect lacks the concept. E57(b) recodes `?` as `0`.
- **Screening.** Primary analyses drop forms with codes `LOAN-SOURCE`, `LOAN-INDONESIAN` and `LOAN-PORTUGUESE` (below). Screened variants also drop `CONTACT-SCREEN` or `TETUN-LOOKALIKE` forms.
- **Retention status.** `derived/innovations/cognate_set_status_r2.csv`: `Status` is `retention` if the set is within reflex-aware normalised edit distance 0.4 of the ABVD PMP form (rule R2, balanced accuracy 0.791 against ABVD's experts), else `innovation`. Concepts without an ABVD PMP form get no status. `cognate_set_status.csv` is the original rule (R0, NED 0.5).

## Sound-change characters

| File | Characters | Coding |
|---|---|---|
| `derived/sound_change_matrix/innovation_matrix_24_hull.csv` | Eleven characters (E13, E29, E42): `p_lenited` (\*p > h, ʔ, ∅), `ng_velar` (\*ŋ > g, k), `ng_n` (\*ŋ > n), `j_rhotic`, `j_l`, `R_zero`, `b_lenited`, `d_liquid`, `b_h_initial`, `k_lost_initial`, `k_lost_medial` | `1` the lect's majority reflex shows the change; `0` it does not; `?` fewer than two tokens. `*_source` columns say which atlas decided |
| `results/literature/e53/matrix.csv` | 36 characters (E53): every (target, position, reflex class) in the expert atlas other than the class that keeps the PMP sound, kept if at least two of the 24 have it and two lack it | as above |
| `derived/audit/p_reflexes.csv` | Every \*p token for 13 focal lects in both atlases | `Environment` is word-initial, between vowels, before a consonant, after a consonant or word-final, read from the PMP form |

The Flores pair is coded from the automatic atlas where the expert atlas lacks it (E42 records each filled cell).

## Exclusion and reclassification codes

Every row is in `derived/audit/exclusions.csv` (`Level`, `ID`, `Lect_ID`, `In_24`, `Concept_ID`, `Form`, `Code`, `Applies_to`, `Reason`, `Source_analysis`); counts are in `exclusions_summary.json`.

| Code | Level | Meaning | Applies to |
|---|---|---|---|
| `LOAN-SOURCE` | form | Marked as a loan in the source list (checked; no D1 form is marked) | every analysis except the unscreened variant |
| `LOAN-INDONESIAN` | form | Matches the Indonesian word for the concept | every analysis except the unscreened variant |
| `LOAN-PORTUGUESE` | form | Matches the Portuguese word for the concept | every analysis except the unscreened variant |
| `CONTACT-SCREEN` | form | Papuan-lect form resembling an Austronesian one | the contact-screened variant only |
| `TETUN-LOOKALIKE` | form | Near-identical to the Tetun word; `Reason` adds the sound-change verdict from `derived/loans/tetun_loans.csv` (probable loan, probably inherited, undecidable) | the Tetun-screened variant only |
| `RET-REVIEW` | set | An "innovation" the review identified as continuing a PMP or PCEMP etymon | cleaned counts (E46) and the second-round decision |
| `ERR-SPLIT` | set | One etymon split into two sets by the automatic coding ('wife') | as above |
| `ERR-NONCOGNATE` | set | Non-cognate forms grouped together ('who') | as above |
| `DOUBTFUL` | set | Doubtful cognacy ('dry') | as above |
| `RET-ACD` | set | Strict match to an Austronesian Comparative Dictionary etymon, PAN to PCMP (E35) | as above |
| `RET-GE-TABLES` | set | Shown as inherited in Grimes and Edwards's tables (E37) | as above |
| `POL-WEST` | set | An R2 innovation also present in Flores, Rote-Meto, Helong or Wetar, so probably old | polarised counts only (E46, E51) |
| `PAPUAN-SHARED` | set | Has a member in a Papuan lect | the E48 sensitivity run only |

## Decisive comparisons

`derived/audit/decisive_comparisons.csv` lists the 24 sets behind Lakalei-Idate's stable-concept triplet counts and the 23 sets it shares exclusively with one other group (E17), with forms, the nearest etymon above the Timor groups, Grimes and Edwards's treatment, the E52 correspondence result, every audit entry, whether the set is still counted after cleaning, and blank `Reconstruction` and `Specialist_verdict` columns for review (see [`SPECIALIST_REVIEW.md`](SPECIALIST_REVIEW.md)).

## Results files

Each analysis E1 to E57 writes a JSON or CSV under `results/` or `results/literature/`, named after its number; `results/principal_estimates.csv` lists every estimate the paper's main text reports, with the file and key it comes from.
