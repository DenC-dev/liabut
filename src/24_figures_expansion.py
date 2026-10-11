"""Figure for Addendum 4: innovation profiles of the Timor-region languages (E10b).

    python3 src/24_figures_expansion.py
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

from common import REPO, RES, read_csv  # noqa: E402

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#fcfcfb"
ON, OFF = "#2a78d6", "#dce6f3"
plt.rcParams.update({"font.family": "Inter", "font.size": 10, "figure.facecolor": SURF, "axes.facecolor": SURF,
                     "savefig.facecolor": SURF, "text.color": INK})

CHARS = [("p_lenited", "*p > h, ʔ, ∅"), ("ng_n", "*ŋ > n"), ("j_rhotic", "*j > r"), ("R_zero", "*R > ∅"),
         ("ng_velar", "*ŋ > g, k"), ("j_l", "*j > l"), ("d_liquid", "*d > r, l"), ("b_lenited", "*b > h, f")]
GROUPS = [
    ("Central Timor", ["mamb1306", "kema1243", "tuku1254", "wela1235"]),
    ("Lakalei-Idate", ["idat1237", "laka1255"]),
    ("Eastern Timor", ["east2473", "habu1241", "kair1265", "waim1252", "naue1237"]),
    ("Wetar-Atauro", ["galo1243", "dadu1237", "iliu1237", "tugu1245", "aput1237", "pera1257"]),
    ("Rote-Meto", ["term1237", "dela1251", "koto1251", "kusa1252"]),
    ("Southwest Maluku", ["kisa1266", "roma1332", "leti1246", "moaa1237", "luan1263", "weta1243", "teun1241",
                          "nila1244", "seru1245", "west2548", "dawe1237", "daii1240", "nort2860", "cent2072",
                          "east2462", "empl1237", "tela1241", "seri1255"]),
]
NAMES = {"mamb1306": "Mambae", "kema1243": "Kemak", "tuku1254": "Tokodede", "wela1235": "Welaun",
         "idat1237": "Idaté", "laka1255": "Lakalei", "east2473": "East Tetun", "habu1241": "Habu",
         "kair1265": "Midiki", "waim1252": "Waima'a", "naue1237": "Naueti", "galo1243": "Galoli",
         "dadu1237": "Dadu'a", "iliu1237": "Ili'uun", "tugu1245": "Tugun", "aput1237": "Aputai", "pera1257": "Perai",
         "term1237": "Termanu", "dela1251": "Dela-Oenale", "koto1251": "Kotos Amarasi", "kusa1252": "Kusa-Manea",
         "kisa1266": "Kisar", "roma1332": "Roma", "leti1246": "Leti", "moaa1237": "Moa", "luan1263": "Luang",
         "weta1243": "Wetan", "teun1241": "Teun", "nila1244": "Nila", "seru1245": "Serua", "west2548": "W. Damer",
         "dawe1237": "Dawera", "daii1240": "Dai", "nort2860": "N. Babar", "cent2072": "C. Marsela",
         "east2462": "E. Marsela", "empl1237": "Emplawas", "tela1241": "Tela-Masbuar", "seri1255": "Serili"}


def main():
    prof = {r["Glottocode"]: r for r in read_csv(os.path.join(REPO, "derived", "sound_change_matrix",
                                                               "innovation_profiles.csv"))}
    rows = []
    for gname, codes in GROUPS:
        for g in codes:
            if g in prof:
                rows.append((gname, g))
    fig, ax = plt.subplots(figsize=(7.6, 0.27 * len(rows) + 1.6))
    n = len(rows)
    for i, (gname, g) in enumerate(rows):
        y = n - 1 - i
        for j, (c, _) in enumerate(CHARS):
            v = prof[g][c]
            if v == "?":
                ax.add_patch(Rectangle((j + 0.04, y + 0.06), 0.92, 0.88, facecolor=SURF, edgecolor=GRID, lw=0.8))
            else:
                ax.add_patch(Rectangle((j + 0.04, y + 0.06), 0.92, 0.88, facecolor=ON if v == "1" else OFF,
                                       edgecolor=SURF, lw=2))
        ax.text(-0.15, y + 0.5, NAMES.get(g, g), ha="right", va="center", fontsize=9, color=INK)
    # group brackets
    start = 0
    for gname, codes in GROUPS:
        k = sum(1 for _, g in rows if _ == gname)
        if not k:
            continue
        top, bot = n - start, n - start - k
        ax.plot([len(CHARS) + 0.2] * 2, [bot + 0.12, top - 0.12], color=MUTED, lw=1.2)
        ax.text(len(CHARS) + 0.35, (top + bot) / 2, gname, va="center", fontsize=9, color=INK2)
        if start:
            ax.axhline(top, color=GRID, lw=0.8, xmin=0.0, xmax=1)
        start += k
    ax.set_xlim(-0.1, len(CHARS) + 2.6)
    ax.set_ylim(-0.2, n + 0.2)
    for j, (_, lab) in enumerate(CHARS):
        ax.text(j + 0.5, n + 0.35, lab, rotation=45, ha="left", va="bottom", fontsize=9, color=INK)
    ax.axvline(4, color=MUTED, lw=1, ls="--", ymax=n / (n + 0.4))
    ax.text(2, -0.9, "Timor-Babar / Eastern Timor changes", ha="center", fontsize=8.5, color=INK2)
    ax.text(6, -0.9, "Central Timor changes", ha="center", fontsize=8.5, color=INK2)
    ax.axis("off")
    ax.legend(handles=[Patch(facecolor=ON, label="has the change"), Patch(facecolor=OFF, label="does not"),
                       Patch(facecolor=SURF, edgecolor=GRID, label="no data (fewer than 2 expert tokens)")],
              loc="upper center", bbox_to_anchor=(0.42, -0.03), ncol=3, frameon=False, fontsize=8.5)
    ax.set_title("Diagnostic sound changes, from Grimes & Edwards (2026) tables", loc="left", fontsize=11,
                 color=INK, pad=70)
    out = os.path.join(RES, "figures", "innovation_profiles.png")
    fig.savefig(out, dpi=170, bbox_inches="tight")
    print(out)


if __name__ == "__main__":
    main()
