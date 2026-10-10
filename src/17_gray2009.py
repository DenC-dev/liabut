"""Novelty check (post hoc): how often do the Timor clades appear in the published Gray, Drummond & Greenhill (2009)
Austronesian posterior trees? Those trees use ABVD expert cognates for 400 languages, including Tetum, Mambai, Kemak,
Galoli (Talur), Atoni, Roti, Wetar, Southwest Maluku and Babar, but not Idate, Lakalei, Welaun, Habu, Kawaimina,
Tokodede, Dadu'a or Helong.

Data: phlorest/gray_et_al2009 (CC-BY 4.0), commit 85dd9d8, fetched into data/upstream/gray_et_al2009.

    python3 src/17_gray2009.py
"""
import json
import os
import re
import subprocess
import zipfile
from io import StringIO

from Bio import Phylo

from common import RES, UP

REPO = "https://github.com/phlorest/gray_et_al2009.git"
COMMIT = "85dd9d89de4dbeac26da87815689de5a4b8df6f5"

BAB = ["CentralMasela", "Dai", "DaweraDaweloor", "EastMasela", "Emplawas", "Imroing", "NorthBabar", "Serili",
       "SouthEastBabar", "TelaMasbuar"]
WET = ["Iliun", "Erai", "Perai", "Tugun", "Aputai"]
SWM = ["Kisar", "Letinese", "Luang", "Teun", "Nila", "Serua", "Selaru"] + BAB  # Glottolog 5.3 Southwest Maluku
TB = ["Tetum", "Talur", "Atoni", "RotiTermanu_D"] + WET + SWM  # Timor-Babar members present in the 2009 data
CLADES = {
    "Central Timor core (Mambai, Kemak)": ["Mambai", "Kemak"],
    "Tetum + Mambai + Kemak": ["Tetum", "Mambai", "Kemak"],
    "Timor-Babar (members present)": TB,
    "Timor-Babar + Mambai + Kemak (one Timor clade)": TB + ["Mambai", "Kemak"],
    "Wetar-Atauro (Talur + Wetar)": ["Talur"] + WET,
    "Wetar": WET,
    "Rote-Meto (Atoni, Roti)": ["Atoni", "RotiTermanu_D"],
    "Southwest Maluku (members present)": SWM,
    "Babar": BAB,
    "Hull's Fabronic (Tetum, Talur, Wetar, Atoni, Kisar, Leti, Luang)": ["Tetum", "Talur", "Atoni"] + WET +
                                                                      ["Kisar", "Letinese", "Luang"],
}


def fetch():
    path = os.path.join(UP, "gray_et_al2009")
    if not os.path.isdir(path):
        subprocess.run(["git", "clone", "-q", REPO, path], check=True)
    subprocess.run(["git", "-C", path, "checkout", "-q", COMMIT], check=True)
    trees = os.path.join(path, "cldf", "post", "posterior.trees")
    if not os.path.exists(trees):
        zipfile.ZipFile(os.path.join(path, "cldf", "posterior.trees.zip")).extractall(os.path.dirname(trees))
    return trees


def main():
    txt = open(fetch()).read()
    trees = re.findall(r"tree\s+\S+\s*=\s*(?:\[&R\]\s*)?(\(.*?;)", txt)
    hits = {k: 0 for k in CLADES}
    for t in trees:
        tr = Phylo.read(StringIO(t), "newick")
        sets = {frozenset(x.name for x in c.get_terminals()) for c in tr.find_clades() if not c.is_terminal()}
        for k, v in CLADES.items():
            hits[k] += frozenset(v) in sets
    out = dict(source="Gray, Drummond & Greenhill 2009, posterior trees via phlorest/gray_et_al2009@" + COMMIT[:7],
               trees=len(trees), clades={k: round(v / len(trees), 3) for k, v in hits.items()})
    json.dump(out, open(os.path.join(RES, "gray2009_timor_clades.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
