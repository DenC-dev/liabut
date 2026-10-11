# Alcantara (2015) Idaté word list

Machine-readable version of Appendix 2 of Alcantara (2015). The appendix lists the 184 examples used in the thesis, from fieldwork mainly in Laclubar.

Cite: Alcantara, Maressa Xavier. 2015. *Descrição fonética e fonológica da língua idaté do Timor Leste*. MA thesis, Universidade de São Paulo. doi:10.11606/D.8.2014.tde-11052015-171431.

| File | Contents |
|---|---|
| `forms.csv` | All 184 entries as printed: number, page, phonetic transcription (with variants), phonological transcription, and Portuguese gloss. |
| `concepts.csv` | The 67 entries whose gloss maps to an ABVD concept. The mapping was made by meaning, before any alignment. |
| `tokens.csv` | 41 PMP consonant tokens from the 17 entries that align to an ABVD Proto-Malayo-Polynesian form (E9 rule: SCA NED ≤ 0.5). |

- **Built by** `src/27_alcantara.py parse <thesis.pdf>` and `src/27_alcantara.py reflexes`.
- **Corrections.** Parsing fixed one layout slip, in entry 67. Source typos are kept as printed:
  - entry 34 has [ˈa.da] but /ˈa.na/;
  - entry 82's gloss reads "veia’az";
  - entry 76 is numbered twice.
- **Selection.** Alcantara left out words identical to Tetun, so these forms are not a random sample of Idaté vocabulary.
- **Rights.** The forms remain the author's data, reproduced here for research with attribution. They are not covered by this repository's licence.
