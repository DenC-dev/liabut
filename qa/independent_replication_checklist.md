# Independent replication checklist

This packet is for a researcher who did not develop the original analysis. A successful run by the original author or an automated CI job is not independent replication.

## Before running

- Clone the public repository and record the commit SHA.
- Read PROTOCOL.md, PROTOCOL.sha256, every dated addendum, and REPLICATION.md.
- Verify the protocol and reference-data hashes before running.
- Record operating system, Python version, package versions, external executable versions, and random seeds.
- Do not silently update upstream data, change thresholds, or repair inputs. Record any necessary deviation before proceeding.

## Minimum replication

1. Run bash reproduce.sh principal from a clean checkout.
2. Compare every output listed in results/principal_estimates.csv with the committed result.
3. Compare numerical outputs using tolerances declared before examining discrepancies.
4. Confirm that the same source files and data variants are used.
5. Record missing dependencies, skipped steps, warnings, and deviations.
6. Re-run the focal C1/C2 analyses from the numbered source scripts if the principal reproduction does not cover them.

## Scientific review

- Inspect the decisive cognate sets on both sides of the C1 placement.
- Review expert-vs-automatic cognate scores and the 70% clade-support criterion.
- Check whether contact, shared retention, and inherited innovation are distinguished consistently.
- Verify that the sensitivity summary is based on the same input codings and that no result is described as more decisive than its uncertainty permits.
- State whether the independent run reproduces the numerical results, the interpretation, both, or neither.

## Reporting template

Report the independent researcher's name and affiliation, date, repository SHA, environment, commands run, output comparison, deviations, and a signed conclusion. If no independent researcher has completed this checklist, the project must continue to say independent replication is outstanding.

## What this checklist does not claim

The committed QA scripts validate release integrity, reproduce the cognate benchmark and summarize already-run sensitivity analyses. They do not substitute for an independent rerun of the full pipeline or specialist adjudication of the decisive historical-linguistic evidence.
