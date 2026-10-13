# Provenance and permissions

Every dataset Liabut uses, where it came from, the exact version, its licence, and what it is used for. Upstream repositories are cloned by `src/01_fetch.sh` into `data/upstream/` at the commits below.

| Source | Version | Licence | Used for |
|---|---|---|---|
| LexiRumah (Kaiping, Edwards and Klamer 2019) | 3.0.1, `lessersunda/lexirumah-data` commit `e10af03` (2025-05-14) | CC BY 4.0 | All Timor-region word lists (D1). Its own cognate judgements are automatic and are not used except in E15 |
| ABVD (Greenhill, Blust and Gray 2008) | `lexibank/abvd` commit `4a5795e` (2026-10-04) | CC BY 4.0 | Expert cognate judgements (D2), PMP forms, and the six outgroup lists (E40, E57) |
| Blust's Proto-Malayo-Polynesian, as in ABVD | same | CC BY 4.0 | E2, the retention rule, and the PMP pseudo-taxon (E40, E57) |
| Austronesian Comparative Dictionary (Blust, Trussel and Smith) | `lexibank/acd` commit `16085f2` (2025-01-07) | CC BY 4.0 | Etymological check of the decisive sets (E35) |
| Intercontinental Dictionary Series, Portuguese (Key and Comrie) | `intercontinental-dictionary-series/ids` commit `bf6c9f8` | CC BY 4.0 | Loan screen (step 3) |
| Gray, Drummond and Greenhill (2009) posterior trees | `phlorest/gray_et_al2009` commit `85dd9d8` | CC BY 4.0 | Novelty check only |
| ASJP v21 | via `lexibank/asjp` | CC BY 4.0 | E14 only |
| Glottolog | 5.3 | CC BY 4.0 | Classification labels |
| Concepticon, Leipzig-Jakarta list (Tadmor 2009) | `data/screen/leipzig_jakarta_tadmor2009.tsv` | CC BY 4.0 | Stable concepts |
| Grimes and Edwards (2026), *The Austronesian languages of eastern Indonesia and Timor-Leste* | Language Science Press, LaTeX source `langsci/526` | CC BY 4.0 | Classification and comparative tables, re-released as data in `derived/ge2026_tables/` under the same licence |
| Alcantara (2015), MA thesis, Universidade de São Paulo | 184 forms transcribed from the thesis | Author's data, not covered by this repository's licence | E16 only; reproduced for research with attribution |
| Natural Earth | 10m land and boundaries | Public domain | Maps |
| Alegreya, Gentium Book Plus | `paper/fonts/` | SIL Open Font License 1.1 | Paper and website |

## The word lists behind each lect

LexiRumah compiles lists from many collectors; the `Source` column of `data/d1/forms.csv` names the list for every form, and `DATA_DICTIONARY.md` gives the main source of each of the 24 analysed lects. The Idaté and Lakalei lists come from Dawson (2014) and Klamer (2002), not from Grimes or Edwards. Several Central Timor and Rote-Meto lists come from Edwards (2018), which is why E28 and E36 rerun the analyses on lists collected independently of Grimes and Edwards.

## What is not available

- **Grimes and Edwards's 494-item field lists** for Idaté and Lakalei are not public. Their appendices on DataverseNO (doi:10.18710/3CT9RO, CC BY-NC 4.0) contain the language list and the questionnaire only.
- **Hull (1998)**, **Hull (2001b)** and **Carvalho (2001)** could not be obtained.

## Material written with AI assistance

The code, the analyses, the drafting of the paper and the mock referee report in `paper/review/referee_report.md` were produced with substantial assistance from Claude (Anthropic) under the author's direction. The mock report is not an independent peer review.

## Permissions

All lexical data used in the analyses are under CC BY 4.0 or in the public domain, so they can be redistributed with attribution; the Alcantara (2015) forms are the exception noted above. No new fieldwork was done and no personal data are held.
