"""Figures for the report (results/figures/).

    python3 src/13_figures.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import RES, read_csv  # noqa: E402

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#fcfcfb"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "Inter", "font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "figure.facecolor": SURF, "axes.facecolor": SURF,
                     "savefig.facecolor": SURF})
FIG = os.path.join(RES, "figures")

ROWS = [("HULL-R", "Ramelaic: Mambae, Kemak, Tokodede + Idaté, Lakalei", "Hull"),
        ("HULL-F", "Fabronic / Timoric A", "Hull"),
        ("HULL98-W", "Welaun inside Tetun", "Hull"),
        ("GE-CT", "Central Timor (with Welaun)", "Edwards / G&E"),
        ("GE-NCT", "Nuclear Central Timor (no Welaun)", "Edwards / G&E"),
        ("GE-TB", "Timor-Babar", "Edwards / G&E"),
        ("GE-ET", "Eastern Timor", "Edwards / G&E"),
        ("GE-ETLI", "Eastern Timor + Lakalei-Idate", "Edwards / G&E"),
        ("GE-LI", "Lakalei-Idate", "Edwards / G&E"),
        ("GE-MW", "Kawaimina (Midiki-Waima'a)", "Edwards / G&E"),
        ("GE-WA", "Wetar-Atauro", "Edwards / G&E"),
        ("GE-WET", "Wetar", "Edwards / G&E"),
        ("GE-NR", "Nuclear Rote", "Edwards / G&E"),
        ("GE-WRM", "West Rote-Meto (Dela + Meto)", "Edwards / G&E"),
        ("GE-KL", "Kisar-Luang", "Edwards / G&E"),
        ("GE-BAB", "Babar", "Edwards / G&E")]


def clade_support():
    s = {r["Hypothesis"]: r for r in read_csv(os.path.join(RES, "hypotheses", "summary_d1_lexstat.csv"))}
    e1 = {(r["Hypothesis"], r["Concept_Set"], r["Variant"]): r
          for r in read_csv(os.path.join(RES, "exploratory", "e1_stable_vs_other.csv"))}
    mn = lambda a, b: min(float(a), float(b))
    fig, ax = plt.subplots(figsize=(9, 7.2))
    y = np.arange(len(ROWS))[::-1]
    for yi, (h, label, _) in zip(y, ROWS):
        p = mn(s[h]["Primary_UPGMA"], s[h]["Primary_NJ"])
        t = mn(s[h]["Tetun_UPGMA"], s[h]["Tetun_NJ"])
        st = e1[(h, "stable_LJ", "primary")]
        sv = mn(st["UPGMA_Bootstrap"], st["NJ_Bootstrap"])
        ax.plot([min(p, t, sv), max(p, t, sv)], [yi, yi], color=GRID, lw=2, zorder=1)
        ax.scatter(p, yi, s=70, color=BLUE, marker="o", zorder=3, edgecolor=SURF, linewidth=1.5)
        ax.scatter(t, yi, s=70, color=ORANGE, marker="s", zorder=3, edgecolor=SURF, linewidth=1.5)
        ax.scatter(sv, yi, s=80, color=AQUA, marker="D", zorder=3, edgecolor=SURF, linewidth=1.5)
    ax.axvline(0.7, color=INK2, ls="--", lw=1)
    ax.text(0.705, y[-1] - 0.75, "70% bar", color=INK2, fontsize=9, va="top")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{lab}" for _, lab, _ in ROWS], color=INK)
    ax.axhline(y[2] - 0.5, color=GRID, lw=1)
    ax.text(1.01, (y[0] + y[2]) / 2, "Hull", transform=ax.get_yaxis_transform(), color=INK2, va="center", fontsize=9)
    ax.text(1.01, (y[3] + y[-1]) / 2, "Edwards /\nGrimes & Edwards", transform=ax.get_yaxis_transform(), color=INK2,
            va="center", fontsize=9)
    ax.set_xlim(-0.02, 1.02)
    ax.set_xlabel("Bootstrap support (lower of UPGMA and NJ), LexiRumah, LexStat cognates")
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.scatter([], [], color=BLUE, marker="o", s=60, label="All 152 concepts (pre-registered primary)")
    ax.scatter([], [], color=ORANGE, marker="s", s=60, label="Tetun look-alikes removed (V-tetun)")
    ax.scatter([], [], color=AQUA, marker="D", s=60, label="60 borrowing-resistant concepts only (exploratory)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.09), ncol=1, frameon=False, fontsize=9)
    ax.set_title("How much lexical support does each proposed subgroup get?", loc="left", color=INK, fontsize=12, pad=14)
    fig.savefig(os.path.join(FIG, "clade_support.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


def sound_changes():
    g = read_csv(os.path.join(RES, "exploratory", "e2_by_group_d1concepts.csv"))
    order = ["Mambae", "Kemak", "Tokodede", "Welaun", "Idate", "Lakalei", "Tetun", "Habu", "Galoli",
             "Helong", "Meto", "Rote", "Wetar", "Luangic-Kisaric", "Babar", "Flores-Lembata"]
    rows = {r["Group"]: r for r in g}
    labels = {"Idate": "Idaté", "Luangic-Kisaric": "Kisar-Luang", "Flores-Lembata": "Flores-Lembata (outgroup)"}
    ct = {"Mambae", "Kemak", "Tokodede", "Welaun"}
    fig, ax = plt.subplots(figsize=(8, 6))
    y = np.arange(len(order))[::-1]
    for yi, grp in zip(y, order):
        r = rows[grp]
        n = int(r["p_N"])
        v = float(r["p_kept"]) if r["p_kept"] not in ("", None) else 0
        ax.barh(yi, v, color=BLUE, height=0.62)
        ax.text(v + 0.01, yi, f"{v:.0%}  (n={n})", va="center", fontsize=9, color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels([labels.get(o, o) + (" *" if o in ct else "") for o in order], color=INK)
    ax.set_xlim(0, 1.18)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_xlabel("Share of PMP *p (not word-final, not *ma-p) kept as a labial")
    ax.set_title("Of the Austronesian languages on Timor, only Mambae, Kemak and Tokodede keep PMP *p", loc="left", color=INK, fontsize=12)
    ax.text(0, -0.2, "* Central Timor in Edwards (2021) and Grimes & Edwards (2026). Exploratory analysis E2 on the 152 D1 concepts;\n"
                      "LexiRumah forms aligned to ABVD PMP. Wetar and Rote reflexes are often unclassifiable (prefixes), so their bars are low.",
            transform=ax.transAxes, fontsize=8, color=INK2)
    fig.savefig(os.path.join(FIG, "sound_change_p.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


def tetun_affinity():
    rows = [r for r in read_csv(os.path.join(RES, "exploratory", "e3_tetun_affinity.csv")) if r["Role"] == "Timor AN"]
    fig, ax = plt.subplots(figsize=(7.2, 6.4))
    xs = [float(r["Stable_Shared"]) for r in rows]
    ys = [float(r["Other_Shared"]) for r in rows]
    ax.plot([0.2, 0.75], [0.2, 0.75], color=MUTED, lw=1, ls="--")
    ax.text(0.71, 0.69, "same affinity\nin both sets", color=INK2, fontsize=8, ha="right", va="top")
    ax.scatter(xs, ys, s=46, color=BLUE, edgecolor=SURF, linewidth=1.2, zorder=3)
    lab = {"west2547-welaun": "Welaun", "west2547-mahein": "Welaun (Mahein)", "idat1237": "Idaté",
           "idat1237-cribas": "Idaté (Cribas)", "laka1255": "Lakalei", "dadu1237": "Dadu'a", "habu1241": "Habu",
           "galo1243": "Galoli", "kema1243": "Kemak", "kusa1252": "Meto (Kusa)", "mamb1306": "Mambae (Ainaro)"}
    off = {"west2547-mahein": (6, -10), "idat1237-cribas": (6, -10), "laka1255": (6, 4), "idat1237": (-50, 2), "mamb1306": (-112, 20), "kema1243": (6, 4)}
    for r, x, yv in zip(rows, xs, ys):
        if r["Lect_ID"] in lab:
            dx, dy = off.get(r["Lect_ID"], (6, 2))
            arrow = dict(arrowstyle="-", color=MUTED, lw=0.7) if r["Lect_ID"] == "mamb1306" else None
            ax.annotate(lab[r["Lect_ID"]], (x, yv), xytext=(dx, dy), textcoords="offset points", fontsize=8.5, color=INK,
                        arrowprops=arrow)
    ax.set_xlim(0.2, 0.75)
    ax.set_ylim(0.2, 0.75)
    ax.set_xlabel("Share of concepts with a Tetun cognate: 60 borrowing-resistant concepts")
    ax.set_ylabel("Same, other 92 concepts")
    ax.grid(color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Above the line = Tetun similarity sits in borrowable vocabulary", loc="left", color=INK, fontsize=11)
    fig.savefig(os.path.join(FIG, "tetun_affinity.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


def bayes_tree():
    path = os.path.join(RES, "bayes", "unconstrained.con.tre")
    if not os.path.exists(path):
        print("no consensus tree yet")
        return
    from io import StringIO
    from Bio import Phylo
    txt = open(path).read()
    import re
    trans = dict(re.findall(r"^\s*(\d+)\s+([^,;\s]+)[,;]?\s*$", txt.split("translate")[1].split(";")[0], re.M))
    tree_line = [l for l in txt.splitlines() if l.strip().startswith("tree con_")][0]
    nwk = tree_line.split("=", 1)[1].strip()
    nwk = re.sub(r"\[&prob=([0-9.eE+-]+)[^\]]*\]", lambda m: f"[&&PP={float(m.group(1)):.2f}]", nwk)
    nwk = re.sub(r"\[[^\]]*?\]", lambda m: m.group(0) if "PP=" in m.group(0) else "", nwk)
    nwk = re.sub(r"\[&&PP=([0-9.]+)\]", r"PP\1", nwk)
    t = Phylo.read(StringIO(nwk), "newick")
    names = {r["ID"]: r["Name"] for r in read_csv(os.path.join(os.path.dirname(RES), "data", "d1", "lects.csv"))}
    import re as _re
    for c in t.find_clades():
        if c.name and c.name.startswith("PP") and not c.is_terminal():
            c.confidence = float(c.name[2:])
            c.name = None
        elif c.is_terminal():
            nm = c.name.split("PP")[0]
            orig = trans.get(nm, nm)
            lid = [k for k in names if _re.sub(r"[^A-Za-z0-9_]", "_", k) == orig]
            c.name = names[lid[0]] if lid else orig
    t.root_with_outgroup([c for c in t.get_terminals() if "Lamaholot" in c.name][0])
    t.ladderize()
    for c in t.find_clades():
        c.branch_length = 1.0  # cladogram: topology and posteriors only
    fig, ax = plt.subplots(figsize=(9, 8))
    Phylo.draw(t, axes=ax, do_show=False, label_func=lambda c: c.name if c.is_terminal() else None,
               branch_labels=lambda c: (f"{c.confidence:.2f}" if c.confidence is not None and c.confidence < 0.995 else "")
               if not c.is_terminal() else "")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_yticks([])
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_title("MrBayes consensus (all compatible splits), 24 lects, cladogram. Unlabelled nodes: posterior > 0.99", loc="left",
                 color=INK, fontsize=11)
    fig.savefig(os.path.join(FIG, "bayes_consensus.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    clade_support()
    sound_changes()
    tetun_affinity()
    bayes_tree()
    print("figures written")
