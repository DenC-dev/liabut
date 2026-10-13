# For an independent replicator

Liabut's analyses have so far been run only by the author (with AI assistance). Before the results are relied on, someone not involved should rerun the main analyses. This file says what to rerun, what to compare, and what counts as agreement.

## Set-up

- Python 3.10 or later, `pip install -r requirements.txt` (LingPy is pinned at 2.6.14; other versions change the cognate sets).
- IQ-TREE 2.3.6 (`$IQTREE`), MrBayes 3.2.7a (`$MRBAYES`), pandoc 3 and XeLaTeX for the paper.
- `./src/01_fetch.sh` clones the upstream data at the commits listed in `PROVENANCE.md`.

## Two levels

1. **From the stored codings** (`bash reproduce.sh principal`, about two minutes, longer if the stored E57 IQ-TREE runs are deleted first). Reruns the deterministic analyses behind the main text and rebuilds `results/principal_estimates.csv`. Agreement here checks the code that turns codings and tree samples into the reported numbers.
2. **From the upstream data** (`bash reproduce.sh full`, many hours). Recodes cognates, reruns every tree. Agreement here checks the whole pipeline. It sets `LEGACY_NFD=1`, so the Portuguese loan screen behaves as it did when the stored results were made; with `LEGACY_NFD=0` it flags one more D2 form (Waima'a *kasa* 'to hunt', like Portuguese *caçar*), a cognate set of one that carries no grouping information.

## What to compare

`results/principal_estimates.csv` lists every estimate in the paper's main text, with the file and key it comes from. Compare your copy with the published one.

| Kind of estimate | Counts as agreement |
|---|---|
| Decisions, counts, parsimony steps, Holm-adjusted p | identical |
| Cognate sets | identical with LingPy 2.6.14 and seed 1234; otherwise report the share of forms in the same set |
| UFBoot percentages | within 5 points (bootstrap and search are stochastic across platforms) |
| MrBayes posteriors | within 0.05 |
| Stepping-stone ln marginal likelihoods | within 1 log unit; ln Bayes factors within 2 |
| AU and SOWH p | same side of 0.05 |

## Independent choices worth trying

Agreement under the author's choices is the first step. The analyses most open to a different reasonable choice are:

- the retention rule (R2): an expert's classification of the decisive sets instead (`SPECIALIST_REVIEW.md`);
- the outgroups for rooting: other Western or Central Malayo-Polynesian lists from ABVD;
- the stable-concept list: Swadesh-100 instead of Leipzig-Jakarta.

## Reporting

Please open an issue with your platform, versions, the `principal_estimates.csv` you obtained, and any difference beyond the tolerances above. Replicators who want it will be named in the paper.
