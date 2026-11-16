#!/usr/bin/env bash
# Build the Liabut paper: figures, static Alegreya instances (website), then pdfLaTeX.
#   bash paper/build.sh        (needs python3 with matplotlib, shapely, biopython, fonttools; pdflatex; qpdf)
set -euo pipefail
export LC_ALL=C.UTF-8   # the scripts read and write UTF-8 (Idaté, Waima’a)
# Reproducible builds: the date of this version stands in for "now" in the PDF and SVG metadata, so rebuilding
# unchanged sources gives identical files. Change it with each new version of the paper.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1794787200}"   # 16 November 2026
export FORCE_SOURCE_DATE=1
cd "$(dirname "$0")"
python3 make_figures.py
mkdir -p build/fonts
for w in 400 500; do
  python3 -m fontTools.varLib.instancer fonts/Alegreya-Variable.ttf "wght=$w" -o "build/fonts/Alegreya-$w.ttf" -q
  python3 -m fontTools.varLib.instancer fonts/Alegreya-Italic-Variable.ttf "wght=$w" -o "build/fonts/Alegreya-Italic-$w.ttf" -q
done
# The paper: pdfLaTeX from latex/liabut.tex (supplement included as an appendix). liabut_supplement.pdf is that
# appendix on its own, for the website. The figures in latex/figures/ are Latin Modern versions of the ones above.
rm -rf build/latex && mkdir -p build/latex && cp -r latex/liabut.tex latex/figures build/latex/
( cd build/latex && for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error liabut.tex >/dev/null; done )
cp build/latex/liabut.pdf liabut.pdf
first=$(sed -n 's/^\\newlabel{supplement}{{[^}]*}{\([0-9]*\)}.*/\1/p' build/latex/liabut.aux)
qpdf --deterministic-id liabut.pdf --pages . "$first"-z -- liabut_supplement.pdf
echo "wrote paper/liabut.pdf and paper/liabut_supplement.pdf"
