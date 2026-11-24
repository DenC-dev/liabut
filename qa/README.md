# Release QA and research validation

Run from the repository root (or any directory):

- `python qa/check_release.py` checks release integrity.
- `python qa/benchmark_cognates.py` compares D2 automatic LexStat/SCA clusters with confident expert-coded cognate judgments and writes `qa/cognate_benchmark.json`.

The cognate benchmark scores unordered form pairs within each concept. Expert rows marked `Doubt=True` are excluded. A pair is reference-positive when the forms share at least one confident expert cognate-set label. The benchmark currently covers the forms for which expert judgments exist; it does not treat unlabeled forms as negatives.

The benchmark also reports the protocol's B-cubed scores (using the first expert set per form, matching `src/04_score.py`) and a separate pairwise sensitivity analysis excluding doubtful judgments. The committed classification sensitivity report summarizes the already-run threshold/method variants in `results/literature/e15_coding_robustness.json`. An independent replication checklist is in [`independent_replication_checklist.md`](independent_replication_checklist.md); completing it requires a researcher outside the original analysis.

The committed benchmark report is a reproducible agreement assessment, not an independent gold standard. Pairwise observations are dependent, and this release does not include held-out threshold tuning or independent expert adjudication. Precision, recall and F1 should therefore be read as descriptive agreement with the supplied coding.

GitHub Actions runs both the release check and benchmark on pushes, pull requests and manual dispatch. These checks do not establish the validity of the project's historical classification.
