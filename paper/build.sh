#!/usr/bin/env bash
# Build the Liabut working paper: figures, static Alegreya instances, then pandoc + XeLaTeX.
#   bash paper/build.sh        (needs python3 with matplotlib, shapely, biopython, fonttools; pandoc >= 3; xelatex)
set -euo pipefail
cd "$(dirname "$0")"
python3 make_figures.py
mkdir -p build/fonts
for w in 400 500; do
  python3 -m fontTools.varLib.instancer fonts/Alegreya-Variable.ttf "wght=$w" -o "build/fonts/Alegreya-$w.ttf" -q
  python3 -m fontTools.varLib.instancer fonts/Alegreya-Italic-Variable.ttf "wght=$w" -o "build/fonts/Alegreya-Italic-$w.ttf" -q
done
pandoc liabut.md -o liabut.pdf --pdf-engine=xelatex --number-sections \
  -H phaistos.tex -B title.tex --lua-filter=floattables.lua \
  -V documentclass=article -V fontsize=11pt -V papersize=a4 -V fontfamily=fontspec \
  -V geometry:top=26mm -V geometry:bottom=28mm -V geometry:left=30mm -V geometry:right=30mm \
  -V pagetitle="Liabut: a lexical-phylogenetic study of how Timor’s Austronesian languages branch, with a pre-registered core" \
  -V title-meta="Liabut: a lexical-phylogenetic study of how Timor’s Austronesian languages branch, with a pre-registered core" \
  -V author-meta="Dennis Crowley" -V lang=en-GB
echo "wrote paper/liabut.pdf"
