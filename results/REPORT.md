# Steps 1 to 4: results

Run 2026-10-10 under the frozen protocol (`PROTOCOL.md` v1, freeze commit `35b913c`). No hypothesis test has been run.

## Gate: failed on G2

| Condition | Rule | Result | Pass |
|---|---|---|---|
| G1 | D1 known-answer clades ≥ 80% (LexStat, UPGMA) | 14 of 15 (93%) | yes |
| G2 | D2 known-answer clades ≥ 80% (LexStat, UPGMA) | 4 of 6 (67%) | **no** |
| G3 | B-cubed F ≥ 0.75, D2 LexStat vs expert | 0.81 | yes |
| G4 | Mantel r ≥ 0.70, D1 LexStat vs D2 expert distances | r = 0.90, p = 0.0001, 24 lects | yes |

Per the protocol, steps 5 to 8 stay closed until an addendum fixes the cause and the gate is rerun. A proposed addendum is at the end of `PROTOCOL.md`.

## Data (step 1)

- **D1, LexiRumah:** 70 lects, 152 concepts, 10,555 forms. Each lect has 112 to 152 concepts (median 144).
- **D2, ABVD:** 30 lects, 210 concepts, 5,433 forms, 4,197 expert cognate judgments.
- **Finding: LexiRumah has no expert cognates.** All 95,201 of its cognate judgments are automatic (`biglexstat`). Expert scoring therefore uses ABVD.
- **ABVD rule casualties:** Tokodede, Dadu'a, Dai and North Babar each have 99 expert-coded forms, one under the frozen cut-off of 100, so they are out of D2. They are all still in D1.

## Cognates (step 2)

| Comparison | Precision | Recall | F |
|---|---|---|---|
| D2 LexStat vs ABVD experts | 0.88 | 0.75 | **0.81** |
| D2 SCA vs ABVD experts | 0.80 | 0.81 | 0.80 |
| D1 LexStat vs LexiRumah `biglexstat` | 0.46 | 0.92 | 0.61 |

- LexStat errs toward splitting: it rarely lumps non-cognates, and it misses about a quarter of the expert links.
- LexiRumah's own `biglexstat` sets are much broader than ours. Neither is a gold standard, so this row is descriptive only.

## Loans (step 3)

| Flag | D1 forms | D2 forms | What it mostly catches |
|---|---|---|---|
| L1 expert loan | n/a | 41 | ABVD's own flags |
| L2 contact set | 2,714 in 151 sets | n/a | sets shared by Austronesian and TAP lects |
| L3 Indonesian | 385 | 193 | mostly inherited look-alikes (*mata* 'eye' 47, 'white' 35, 'rope' 30), plus real loans in TAP (Bunak *ikan* 'fish'; Makasae *lima* 'five', *tana* 'hand') |
| L4 Portuguese | 29 | 1 | *cantar* 'sing' in 24 lects across both families; *estrada* 'road'; *avó/avô* |
| L5 Tetun look-alike | 740 | 115 | highest in Lakalei (52), Welaun (52, 50), Habu (49) and Idaté (44, 31) |

- **The disputed lects carry the most Tetun-like vocabulary.** Idaté, Lakalei, Habu and Welaun are exactly the lects the Hull–Edwards contrast is about. Tetun is the regional lingua franca, so this similarity could be contact or close inheritance. Telling the two apart is the hardest part of steps 5 to 8.
- **The planned sensitivity checks don't work for those lects.** Dropping the L5 forms (variant V-tetun) leaves Idaté, Lakalei, Habu and Galoli under the 100-concept minimum, so they fall out of the tree. Dropping contact sets (V-contact) removes 28 lects. As written, neither variant can test C1.

## Known-answer checks (step 4)

Clades recovered on the primary data:

| Dataset | Cognates | UPGMA | NJ |
|---|---|---|---|
| D1 | LexStat | 14 / 15 | 15 / 15 |
| D1 | SCA | 15 / 15 | 15 / 15 |
| D1 | `biglexstat` | 13 / 15 | 13 / 15 |
| D2 | **expert** | **4 / 6** | 5 / 6 |
| D2 | LexStat | 4 / 6 | 4 / 6 |
| D2 | SCA | 3 / 6 | 3 / 6 |

- **D1 works well.**
  - Every dialect group comes back with ≥ 93% bootstrap support, and Rote-Meto with 97%.
  - The one UPGMA miss is the TAP clade. Bunak's basic vocabulary is closer to neighbouring Mambae (distance 0.80) than to Fataluku, Makasae or Oirata (0.89 to 0.94), which fits heavy Austronesian contact.
  - NJ recovers the TAP clade at 95%.
- **D2 fails for two separate reasons.**
  - **Weak checks.** Two of the six checks fail with the expert cognates too: Luang + Wetan (bootstrap 1%) and Perai + Aputai (16%). A sister-pair check in a 30-lect tree is fragile, and these two can't separate good cognate detection from bad.
  - **One real miss.** LexStat doesn't pair Atoni (Meto) with Termanu (Rote), which the experts pair at 90%. Many ABVD Atoni entries are inflected or compound (*ʔat maɛt* 'I die', *manu tɛkoʔ* 'chicken egg'), and LexStat finds only 46 of the 78 links the experts make. In D1, where the LexiRumah Meto forms are citation forms, Rote-Meto is recovered.
- **Counting both, the automatic cognates match the experts on D2.** Both recover 4 of 6 checks.

## Files

- `results/gate.json`: the gate, with the lects dropped in each variant.
- `results/known_answers.csv`: every check in every configuration, with bootstrap support.
- `results/scores/`: B-cubed totals and per-concept scores.
- `results/loans/`: flags per form and counts per lect.
- `results/cognates/`: automatic cognate sets.
- `results/distances/` and `results/trees/`: distance matrices and Newick trees for every configuration.

The trees are written out because the clade checks need them. While diagnosing the TAP miss, the D1 LexStat UPGMA tree was viewed in full (see Addendum 1). No hypothesis clade has been scored.
