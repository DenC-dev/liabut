#!/usr/bin/env bash
# Build the Liabut working paper: figures, static Alegreya instances, then pandoc + XeLaTeX.
#   bash paper/build.sh        (needs python3 with matplotlib, shapely, biopython, fonttools; pandoc >= 3; xelatex)
set -euo pipefail
export LC_ALL=C.UTF-8   # pandoc reads -V values in the locale encoding; without UTF-8 the PDF title metadata is garbled
# Reproducible builds: the date of this version stands in for "now" in the PDF and SVG metadata, so rebuilding
# unchanged sources gives identical files. Change it with the version line in title.tex.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1791849600}"   # 13 October 2026
export FORCE_SOURCE_DATE=1
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
  -V pagetitle="Where do Idaté and Lakalei belong?" \
  -V title-meta="Where do Idaté and Lakalei belong? A pre-registered lexical-phylogenetic test of two classifications of Timor’s Austronesian languages" \
  -V author-meta="Dennis Crowley" -V lang=en-GB
pandoc supplement.md -o liabut_supplement.pdf --pdf-engine=xelatex --number-sections \
  -H phaistos.tex -H supp_numbering.tex -B supp_title.tex --lua-filter=floattables.lua \
  -V documentclass=article -V fontsize=11pt -V papersize=a4 -V fontfamily=fontspec \
  -V geometry:top=26mm -V geometry:bottom=28mm -V geometry:left=30mm -V geometry:right=30mm \
  -V pagetitle="Where do Idaté and Lakalei belong? Supplement" \
  -V title-meta="Where do Idaté and Lakalei belong? Supplement: the exploratory analyses" \
  -V author-meta="Dennis Crowley" -V lang=en-GB
echo "wrote paper/liabut.pdf and paper/liabut_supplement.pdf"
