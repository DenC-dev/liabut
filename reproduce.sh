#!/usr/bin/env bash
# Reproduce Liabut's results.
#
#   bash reproduce.sh principal   reruns the deterministic analyses behind the main text from the stored cognate
#                                 codings and tree samples, rebuilds results/principal_estimates.csv, the figures,
#                                 the paper (PDF and supplement) and the website. About two minutes when the stored IQ-TREE runs are present.
#   bash reproduce.sh full        runs the whole pipeline from the upstream data (many hours; MrBayes, IQ-TREE and,
#                                 for E19/E39, BEAST 2.6.7 with contacTrees). The order follows README.md.
#
# Needs: Python 3.10+ with requirements.txt; IQ-TREE 2.3.6 ($IQTREE); MrBayes 3.2.7a ($MRBAYES) for full;
# pandoc 3 and XeLaTeX for the paper. Seeds are fixed in the scripts (1234 unless stated).
set -euo pipefail
cd "$(dirname "$0")"
mode="${1:-principal}"
t0=$(date +%s)
step() { echo; echo "== $*"; }

if [[ "$mode" == "full" ]]; then
  # The stored loan flags were made before the Unicode fix in common.ortho_tokens (results/LITERATURE.md, eleventh
  # round). LEGACY_NFD=1 reproduces them exactly; set LEGACY_NFD=0 for the corrected screen (one more D2 flag).
  export LEGACY_NFD="${LEGACY_NFD:-1}"
  step "upstream data at pinned commits"; ./src/01_fetch.sh
  # every step of README.md "Rerun", in order
  ( cd src && sed -n '/^```$/,/^```$/p' ../README.md | sed '1d;$d' | grep -v '^pip install' | grep -v '^\./src/01_fetch' \
      | grep -v '^cd src' | sed 's|MRBAYES=/path/to/mb ||' | while IFS= read -r line; do
          if [[ "$line" == *"<"* ]]; then echo "-- skipped (needs a local file or clone; run by hand): $line"; continue; fi
          echo "-- $line"; bash -c "${line%%#*}"; done )
fi

step "sound changes: E42 and the reversibility sweep (E56)"
( cd src && python3 41_addendum12.py e42 >/dev/null && python3 43_addendum14.py e56 )
step "shared innovations, cleaned and polarised (E46)"
( cd src && python3 41_addendum12.py e46 >/dev/null )
step "root sensitivity (E57; IQ-TREE runs are skipped where stored)"
( cd src && python3 43_addendum14.py e57 )
step "audit trail and decisive comparisons"
( cd src && python3 43_addendum14.py audit && python3 43_addendum14.py decisive && python3 43_addendum14.py reflexes >/dev/null )
step "principal estimates"
python3 src/44_principal.py
step "figures, paper, supplement, website"
bash paper/build.sh
python3 paper/make_site.py
echo; echo "done in $(( $(date +%s) - t0 )) s"
