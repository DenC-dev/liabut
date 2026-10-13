# For a specialist reviewer

Liabut's main question is whether Lakalei and Idaté share a common ancestor with Mambae, Kemak and Tokodede (Hull) or with the Eastern Timor languages inside Timor-Babar (Grimes and Edwards). The vocabulary evidence on that question rests on a few dozen cognate sets. They were coded automatically and checked only partly, by a mock review and by etymological matching. They need checking by someone who knows these languages, on both sides of the dispute.

## What to review

`derived/audit/decisive_comparisons.csv`, 47 rows:

- 24 sets behind Lakalei-Idate's stable-vocabulary triplet counts (`Source` = packet), shared with Nuclear Central Timor or with Tetun, Habu or Kawaimina;
- 23 sets Lakalei-Idate shares with exactly one other group (`Source` = exclusive set), 6 on the Central Timor side and 9 on the eastern side among them.

Each row gives the forms, the nearest etymon above the Timor groups (PAN to PCMP, from the Austronesian Comparative Dictionary), how Grimes and Edwards's tables treat it, the result of the correspondence test (E52), every audit entry, and whether it is still counted.

## What to fill in

For each row, in `Specialist_verdict`:

1. **Cognate?** Are the forms in the set cognate, and are any forms missing from it that belong?
2. **Old or new?** Does the set continue an etymon older than the groups being compared (a retention, which says nothing about subgrouping), or is it a replacement (an innovation)?
3. **Inherited or borrowed?** For the Lakalei or Idaté form, is there evidence of borrowing: a sound that does not match the regular correspondences, a meaning shift typical of loans, or a known Tetun, Mambae or Habu source?

In `Reconstruction`, where you can, the form of the innovation in the proto-language of the group that shares it, with the correspondences that support it. Liabut leaves this column blank rather than guess.

The sound-change side needs the same eye: `derived/audit/p_reflexes.csv` lists every \*p token for the focal lects in both atlases, with its environment.

## Contact

Please open an issue on the repository or write to the author. Reviewers who want it will be named in the paper.
