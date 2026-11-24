# Release QA and research validation

Run from the repository root (or any directory):

- `python qa/check_release.py` checks release integrity.
- `python qa/benchmark_cognates.py` compares D2 automatic LexStat/SCA clusters with confident expert-coded cognate judgments and writes `qa/cognate_benchmark.json`.

The cognate benchmark scores unordered form pairs within each concept. Expert rows marked `Doubt=True` are excluded. A pair is reference-positive when the forms share at least one confident expert cognate-set label. The benchmark currently covers the forms for which expert judgments exist; it does not treat unlabeled forms as negatives.

The committed benchmark report is a reproducible agreement assessment, not an independent gold standard. Pairwise observations are dependent, and this release does not include held-out threshold tuning or independent expert adjudication. Precision, recall and F1 should therefore be read as descriptive agreement with the supplied coding.

GitHub Actions runs both the release check and benchmark on pushes, pull requests and manual dispatch. These checks do not establish the validity of the project's historical classification.
