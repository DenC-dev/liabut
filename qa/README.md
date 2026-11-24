# Release QA

Run `python qa/check_release.py` from the repository root (or any directory).

The dependency-free check verifies the committed D1 corpus record counts,
unique identifiers, form-to-lect and form-to-concept references, source
attribution, and that every file cited by `results/principal_estimates.csv`
exists in the release.

GitHub Actions runs this check on pushes, pull requests, and manual dispatch.
It checks release integrity, not the linguistic validity of cognate judgments,
retention classifications, tree models, or interpretations.
