# Timor subgrouping study

A pre-registered computational test of the competing classifications of the Austronesian languages of Timor: Hull's Ramelaic and Fabronic (1998, 2001) against Edwards's Central Timor and Timor-Babar (2021; Glottolog 5.3). The method follows Robinson and Holton (2012), who used lexical data to find subgroups in Alor-Pantar that sound changes alone couldn't settle.

Dennis Crowley, Phaistos Labs. Analysis code written with Claude.

## Status

| Step | What | Status |
|---|---|---|
| 0 | Protocol frozen (`PROTOCOL.md`, hashes in `PROTOCOL.sha256`) | done, commit `35b913c` |
| 1 | Build datasets D1 (LexiRumah) and D2 (ABVD) | done |
| 2 | Automatic cognates, scored against ABVD experts | done, B-cubed F = 0.81 |
| 3 | Loan screening | done |
| 4 | Known-answer checks and gate | done: **gate failed on G2** |
| 5–8 | Hypothesis tests (distance trees, NeighborNet, BEAST2, decision) | closed until Addendum 1 is decided |

The results are in [`results/REPORT.md`](results/REPORT.md). The proposed fix is Addendum 1 at the end of [`PROTOCOL.md`](PROTOCOL.md).

## Layout

| Path | Contents |
|---|---|
| `PROTOCOL.md` | Question, data rules, methods, gate, decision rules, addenda |
| `reference/` | Frozen tables: D1 lects, known-answer clades, hypothesis clades, ABVD–LexiRumah lect map |
| `data/d1/`, `data/d2/` | The two datasets as built by step 1 (CLDF-style CSVs) |
| `data/screen/` | Indonesian and Portuguese reference words for loan screening |
| `src/` | Pipeline, numbered in run order |
| `results/` | Cognates, scores, loan flags, distances, trees, checks, gate |

## Rerun

```
pip install lingpy==2.6.14 python-igraph pandas numpy scipy
./src/01_fetch.sh            # upstream data at pinned commits, into data/upstream/
cd src
python3 02_build_dataset.py  # step 1
python3 03_cognates.py       # step 2a, about 7 minutes
python3 04_score.py          # step 2b
python3 05_loans.py          # step 3
python3 06_known_answers.py  # step 4 and the gate
```

`00_reference.py` regenerates the frozen `reference/` tables. If you rerun it, check that `sha256sum -c PROTOCOL.sha256` still passes for them.

## Data and licences

- **LexiRumah 3.0.1** (Kaiping, Edwards and Klamer 2019), CC-BY 4.0. It has no expert cognate sets; all of its cognate judgments are automatic.
- **ABVD** (Greenhill, Blust and Gray 2008), CC-BY 4.0. Source of the expert cognates.
- **IDS** Portuguese list (Key and Comrie), CC-BY 4.0.
- **Glottolog 5.3**, CC-BY 4.0. Reference groups.
- **Grimes and Edwards (2026).** The book is CC-BY 4.0. Its appendices are CC BY-NC and hold single-word comparisons rather than a wordlist, so none of its data is used here.

The code is MIT (`LICENSE`). The data keep their source licences; please cite the sources above.
