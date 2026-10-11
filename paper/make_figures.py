"""Figures for the Liabut paper, in the Phaistos Labs palette.

    python3 paper/make_figures.py            # uses paper/data/*.geojson (already clipped)
    NE_DIR=/path/to/natural-earth/geojson python3 paper/make_figures.py clip   # re-clip from Natural Earth 10m

Writes paper/figures/map.pdf, tree.pdf, sounds.pdf and triplets.pdf, plus PNG and SVG copies for the website.
"""
import csv
import importlib.util
import json
import os
import re
import sys
from io import StringIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures")
DATA = os.path.join(HERE, "data")

for f in os.listdir(os.path.join(HERE, "fonts")):
    if f.endswith(".ttf"):
        fm.fontManager.addfont(os.path.join(HERE, "fonts", f))

PAPER, PAPER_DEEP, PAPER_LIGHT = "#ede5d0", "#e3d8bd", "#f4eedf"
INK, INK2, INK3, RULE = "#2a2723", "#57514a", "#6b6458", "#c9bc9b"
BLUE, OCHRE, OCHRE_TEXT = "#1f6a9e", "#b5451f", "#963a1c"
COAST = "#a8987a"

plt.rcParams.update({
    "font.family": "Gentium Book Plus", "font.size": 8.5, "text.color": INK, "axes.edgecolor": RULE,
    "axes.labelcolor": INK2, "xtick.color": INK3, "ytick.color": INK3, "figure.facecolor": "white",
    "savefig.facecolor": "white", "pdf.fonttype": 42,
})

# ---------------------------------------------------------------- the 24 lects
NAME = {
    "mamb1306-Slete": "Mambae", "kema1243-kaila": "Kemak", "tuku1254": "Tokodede", "west2547-welaun": "Welaun",
    "idat1237-cribas": "Idaté", "laka1255": "Lakalei", "tetu1245-suai": "Tetun", "habu1241": "Habu",
    "waim1252": "Waima’a", "midi1237": "Midiki", "naue1237": "Naueti", "galo1243": "Galoli",
    "dadu1237": "Dadu’a", "funa1237": "Helong", "koto1251": "Amarasi", "term1237": "Termanu", "dela1252": "Dela",
    "ilma1240": "Ili’uun", "kaha1239": "Tugun", "kisa1266": "Kisar", "luan1264": "Luang",
    "tela1241": "Tela-Masbuar", "lama1277-lewoi": "Lamaholot", "sika1262-hewa": "Sika",
}
GROUP = {t: "other" for t in NAME}
GROUP.update({t: "CT" for t in ("mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun")})
GROUP.update({t: "LI" for t in ("idat1237-cribas", "laka1255")})
GROUP.update({t: "ET" for t in ("tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237")})
COLOR = {"CT": BLUE, "LI": OCHRE, "ET": INK2, "other": INK}
LEGEND = [("LI", "Lakalei-Idate"), ("CT", "Central Timor"), ("ET", "Eastern Timor (Grimes and Edwards)"),
          ("other", "Other Timor-Babar and outgroups")]


def lects():
    out = {}
    for r in csv.DictReader(open(os.path.join(REPO, "data", "d1", "lects.csv"), encoding="utf-8")):
        if r["ID"] in NAME:
            out[r["ID"]] = (float(r["Longitude"]), float(r["Latitude"]))
    return out


def marker(ax, x, y, g, s=34, z=5):
    if g == "other":
        ax.scatter([x], [y], s=s * 0.8, facecolor="white", edgecolor=INK, linewidth=1.0, zorder=z)
    else:
        ax.scatter([x], [y], s=s, facecolor=COLOR[g], edgecolor="white", linewidth=0.8, zorder=z)


# ---------------------------------------------------------------- map
BBOX = (122.3, 130.2, -11.25, -7.35)
ZOOM = (124.78, 126.95, -9.425, -8.355)
OVER_LAB = {  # label offsets (dx, dy, ha)
    "lama1277-lewoi": (0.0, 0.17, "center"), "sika1262-hewa": (-0.02, -0.17, "center"),
    "funa1237": (-0.08, -0.16, "right"), "koto1251": (0.08, -0.16, "left"),
    "term1237": (0.1, -0.05, "left"), "dela1252": (0.1, -0.05, "left"),
    "ilma1240": (-0.1, 0.0, "right"), "kaha1239": (0.1, 0.0, "left"), "kisa1266": (0.1, -0.05, "left"),
    "luan1264": (0.0, -0.17, "center"), "tela1241": (0.0, -0.17, "center"),
}
ZOOM_LAB = {  # label position (x, y, ha)
    "dadu1237": (125.80, -8.43, "right"), "galo1243": (125.80, -8.555, "right"),
    "idat1237-cribas": (125.80, -8.66, "right"), "habu1241": (125.80, -8.775, "right"),
    "midi1237": (126.15, -8.57, "center"), "waim1252": (126.37, -8.585, "left"),
    "naue1237": (126.74, -8.79, "center"), "laka1255": (125.80, -9.07, "left"),
    "mamb1306-Slete": (125.60, -9.07, "right"), "kema1243-kaila": (125.13, -8.915, "center"),
    "tuku1254": (125.20, -8.53, "center"), "west2547-welaun": (124.985, -9.175, "center"),
    "tetu1245-suai": (125.33, -9.31, "left"),
}


def clip():
    from shapely.geometry import box, mapping, shape
    ne = os.environ["NE_DIR"]
    b = box(BBOX[0] - 0.2, BBOX[2] - 0.2, BBOX[1] + 0.2, BBOX[3] + 0.2)
    os.makedirs(DATA, exist_ok=True)
    land = json.load(open(os.path.join(ne, "ne_10m_land.geojson")))
    feats = []
    for f in land["features"]:
        g = shape(f["geometry"]).intersection(b)
        if not g.is_empty:
            feats.append({"type": "Feature", "properties": {}, "geometry": mapping(g.simplify(0.003))})
    json.dump({"type": "FeatureCollection", "features": feats}, open(os.path.join(DATA, "land.geojson"), "w"))
    cty = json.load(open(os.path.join(ne, "ne_10m_admin_0_countries.geojson")))
    geo = {f["properties"]["ADM0_A3"]: shape(f["geometry"]) for f in cty["features"]
           if f["properties"].get("ADM0_A3") in ("TLS", "IDN")}
    border = geo["TLS"].boundary.intersection(geo["IDN"].buffer(0.01)).intersection(b)
    json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "TLS-IDN"},
              "geometry": mapping(border.simplify(0.002))}]}, open(os.path.join(DATA, "border.geojson"), "w"))
    print("clipped", os.listdir(DATA))


def polys(path):
    from shapely.geometry import shape
    out = []
    for f in json.load(open(path))["features"]:
        g = shape(f["geometry"])
        for p in getattr(g, "geoms", [g]):
            if p.geom_type == "Polygon":
                out.append(p)
    return out


def lines(path):
    from shapely.geometry import shape
    out = []
    for f in json.load(open(path))["features"]:
        g = shape(f["geometry"])
        out.extend(getattr(g, "geoms", [g]))
    return [g for g in out if g.geom_type == "LineString"]


def draw_land(ax, land, border):
    for p in land:
        x, y = p.exterior.xy
        ax.fill(x, y, facecolor=PAPER_DEEP, edgecolor=COAST, linewidth=0.45, zorder=1)
    for ln in border:
        x, y = ln.xy
        ax.plot(x, y, color=INK3, linewidth=0.6, linestyle=(0, (2.5, 1.6)), zorder=2)


def place(ax, txt, x, y, size=8.2, color=INK, ha="left", va="center", italic=False, font="Gentium Book Plus"):
    ax.text(x, y, txt, fontsize=size, color=color, ha=ha, va=va, zorder=6, family=font,
            style="italic" if italic else "normal")


def map_figure():
    import numpy as np
    land, tl = polys(os.path.join(DATA, "land.geojson")), lines(os.path.join(DATA, "border.geojson"))
    L = lects()
    fig = plt.figure(figsize=(6.5, 6.75))
    ax1 = fig.add_axes([0.0, 0.515, 1.0, 0.485])
    ax2 = fig.add_axes([0.0, 0.0, 1.0, 0.485])
    k = 1 / np.cos(np.radians(9))
    for ax, (x0, x1, y0, y1) in ((ax1, BBOX), (ax2, ZOOM)):
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.set_aspect(k)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(RULE)
            s.set_linewidth(0.8)
        draw_land(ax, land, tl)

    # overview
    zoom_box = Rectangle((ZOOM[0], ZOOM[2]), ZOOM[1] - ZOOM[0], ZOOM[3] - ZOOM[2], fill=False, edgecolor=INK2,
                         linewidth=0.7, zorder=4)
    ax1.add_patch(zoom_box)
    ax1.text(ZOOM[1], ZOOM[2] - 0.06, "enlarged below", fontsize=7.5, color=INK2, style="italic",
             va="top", ha="right", family="Alegreya")
    inside = lambda t: ZOOM[0] < L[t][0] < ZOOM[1] and ZOOM[2] < L[t][1] < ZOOM[3]  # noqa: E731
    for t, (x, y) in L.items():
        if inside(t):
            marker(ax1, x, y, GROUP[t], s=14)
        else:
            marker(ax1, x, y, GROUP[t])
            dx, dy, ha = OVER_LAB[t]
            place(ax1, NAME[t], x + dx, y + dy, ha=ha)
    for txt, x, y in (("Flores", 121.95 + 0.6, -8.92), ("Timor", 124.35, -9.75), ("Rote", 122.9, -10.95 + 0.33),
                      ("Wetar", 126.25, -7.55), ("Atauro", 125.55, -8.08), ("Savu Sea", 123.0, -9.6),
                      ("Banda Sea", 127.9, -7.6), ("Timor Sea", 127.0, -9.95)):
        place(ax1, txt, x, y, size=8, color=INK3, ha="center", italic=True, font="Alegreya")
    handles = [Line2D([], [], marker="o", linestyle="", markersize=6,
                      markerfacecolor=("white" if g == "other" else COLOR[g]),
                      markeredgecolor=(INK if g == "other" else "white"), label=lab) for g, lab in LEGEND]
    leg = ax1.legend(handles=handles, loc="lower right", frameon=False, fontsize=8, handletextpad=0.3,
                     borderaxespad=0.6, labelspacing=0.35)
    for t in leg.get_texts():
        t.set_family("Alegreya")

    # zoom
    for t, (x, y) in L.items():
        if not inside(t):
            continue
        g = GROUP[t]
        marker(ax2, x, y, g, s=48)
        lx, ly, ha = ZOOM_LAB[t]
        col = OCHRE_TEXT if g == "LI" else BLUE if g == "CT" else INK
        place(ax2, NAME[t], lx, ly, size=9.5, ha=ha, color=col)
        if abs(lx - x) > 0.09 or abs(ly - y) > 0.09:
            ex = lx + (0.012 if ha == "right" else -0.012 if ha == "left" else 0)
            ax2.plot([x, ex], [y, ly], color=RULE, lw=0.6, zorder=3)
    for txt, x, y in (("Timor-Leste", 126.3, -8.86), ("Indonesia", 124.9, -9.36),
                      ("Ombai Strait", 125.2, -8.4), ("Timor Sea", 126.3, -9.25)):
        place(ax2, txt, x, y, size=8.5, color=INK3, ha="center", italic=True, font="Alegreya")
    # 25 km scale bar
    km = 25 / (111.32 * np.cos(np.radians(9)))
    xs, ys = 126.55, -9.38
    ax2.plot([xs, xs + km], [ys, ys], color=INK2, lw=1.2, zorder=6, solid_capstyle="butt")
    for xx in (xs, xs + km):
        ax2.plot([xx, xx], [ys - 0.012, ys + 0.012], color=INK2, lw=1, zorder=6)
    place(ax2, "25 km", xs + km / 2, ys + 0.04, size=7.5, color=INK2, ha="center", font="Alegreya")
    fig.savefig(os.path.join(FIG, "map.pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(FIG, "map.png"), dpi=200, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# ---------------------------------------------------------------- tree
def tree_figure():
    from Bio import Phylo
    txt = open(os.path.join(REPO, "results", "bayes", "unconstrained.con.tre")).read()
    trans = dict(re.findall(r"^\s*(\d+)\s+([^,;\s]+)[,;]?\s*$", txt.split("translate")[1].split(";")[0], re.M))
    nwk = [ln for ln in txt.splitlines() if ln.strip().startswith("tree con_")][0].split("=", 1)[1].strip()
    nwk = re.sub(r"\[&prob=([0-9.eE+-]+)[^\]]*\]", lambda m: f"PP{float(m.group(1)):.3f}", nwk)
    nwk = re.sub(r"\[[^\]]*\]", "", nwk)
    t = Phylo.read(StringIO(nwk), "newick")
    key = {re.sub(r"[^A-Za-z0-9_]", "_", k): k for k in NAME}
    for c in t.find_clades():
        if c.is_terminal():
            nm = c.name.split("PP")[0]
            c.name = key[trans.get(nm, nm)]
        elif c.name and c.name.startswith("PP"):
            c.confidence = float(c.name[2:])
            c.name = None
        elif c.confidence is not None and c.confidence > 1:
            c.confidence = None
    t.root_with_outgroup([c for c in t.get_terminals() if c.name == "lama1277-lewoi"][0])
    t.ladderize(reverse=True)
    tips = t.get_terminals()
    ypos = {id(c): i for i, c in enumerate(tips)}
    depth = {}

    def setdepth(c, d):
        depth[id(c)] = d
        for ch in c.clades:
            setdepth(ch, d + 1)
    setdepth(t.root, 0)
    maxd = max(depth.values())

    def y(c):
        if id(c) not in ypos:
            ypos[id(c)] = (y(c.clades[0]) + y(c.clades[-1])) / 2
        return ypos[id(c)]

    def x(c):
        return maxd if c.is_terminal() else depth[id(c)]
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    for c in t.find_clades():
        if c.is_terminal():
            continue
        ys = [y(ch) for ch in c.clades]
        col = INK
        ax.plot([x(c), x(c)], [min(ys), max(ys)], color=col, lw=1.0, solid_capstyle="round")
        for ch in c.clades:
            ax.plot([x(c), x(ch)], [y(ch), y(ch)], color=col, lw=1.0, solid_capstyle="round")
        pp = c.confidence
        if c is not t.root and pp is not None and pp < 0.995:
            ax.text(x(c) - 0.08, y(c) - 0.18, f"{pp:.2f}".lstrip("0"), fontsize=7.2, color=INK2, ha="right",
                    va="bottom", family="Alegreya", style="italic")
    ax.plot([x(t.root) - 0.5, x(t.root)], [y(t.root)] * 2, color=INK, lw=1.0)
    for c in tips:
        g = GROUP[c.name]
        marker(ax, maxd, y(c), g, s=22)
        col = OCHRE_TEXT if g == "LI" else BLUE if g == "CT" else INK
        ax.text(maxd + 0.28, y(c), NAME[c.name], va="center", fontsize=8.8, color=col)
    ax.set_xlim(-0.6, maxd + 2.6)
    ax.set_ylim(len(tips) - 0.4, -0.6)
    ax.axis("off")
    fig.savefig(os.path.join(FIG, "tree.pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(FIG, "tree.png"), dpi=200, bbox_inches="tight", pad_inches=0.02)
    with plt.rc_context({"svg.fonttype": "none"}):
        fig.savefig(os.path.join(FIG, "tree.svg"), bbox_inches="tight", pad_inches=0.02, transparent=True)
    plt.close(fig)


# ---------------------------------------------------------------- sound changes
def sounds_figure():
    spec = importlib.util.spec_from_file_location("f24", os.path.join(REPO, "src", "24_figures_expansion.py"))
    sys.path.insert(0, os.path.join(REPO, "src"))
    f24 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f24)
    plt.rcParams.update({"font.family": "Gentium Book Plus", "figure.facecolor": "white",
                         "savefig.facecolor": "white", "axes.facecolor": "white", "text.color": INK})
    prof = {r["Glottocode"]: r for r in csv.DictReader(open(os.path.join(
        REPO, "derived", "sound_change_matrix", "innovation_profiles.csv"), encoding="utf-8"))}
    groups = [g for g in f24.GROUPS if g[0] != "Southwest Maluku"]
    rows = [(gn, c) for gn, cs in groups for c in cs if c in prof]
    n, m = len(rows), len(f24.CHARS)
    gcol = {"Central Timor": BLUE, "Lakalei-Idate": OCHRE}
    fig, ax = plt.subplots(figsize=(5.2, 0.205 * n + 1.25))
    for i, (gn, g) in enumerate(rows):
        yy = n - 1 - i
        on = gcol.get(gn, INK2)
        for j, (c, _) in enumerate(f24.CHARS):
            v = prof[g][c]
            if v == "?":
                ax.add_patch(Rectangle((j + 0.08, yy + 0.12), 0.84, 0.76, facecolor="white", edgecolor=RULE, lw=0.6))
            else:
                ax.add_patch(Rectangle((j + 0.08, yy + 0.12), 0.84, 0.76, lw=0,
                                       facecolor=on if v == "1" else PAPER_DEEP))
        name = f24.NAMES.get(g, g).replace("'", "’")
        ax.text(-0.15, yy + 0.5, name, ha="right", va="center", fontsize=8.3,
                color=OCHRE_TEXT if gn == "Lakalei-Idate" else BLUE if gn == "Central Timor" else INK)
    start = 0
    for gn, codes in groups:
        k = sum(1 for g_, _ in rows if g_ == gn)
        top, bot = n - start, n - start - k
        ax.plot([m + 0.2] * 2, [bot + 0.15, top - 0.15], color=INK3, lw=0.9)
        ax.text(m + 0.35, (top + bot) / 2, gn, va="center", fontsize=8.3, color=INK2, family="Alegreya",
                style="italic")
        if start:
            ax.plot([-2.6, m + 2.9], [top, top], color=RULE, lw=0.5)
        start += k
    for j, (_, lab) in enumerate(f24.CHARS):
        ax.text(j + 0.5, n + 0.25, lab, rotation=50, ha="left", va="bottom", fontsize=8.3, color=INK)
    ax.plot([4, 4], [-0.1, n + 0.1], color=INK3, lw=0.8, ls=(0, (2, 2)))
    ax.text(2, -0.55, "Timor-Babar changes", ha="center", va="top", fontsize=8, color=INK2, family="Alegreya",
            style="italic")
    ax.text(6, -0.55, "Central Timor changes", ha="center", va="top", fontsize=8, color=INK2, family="Alegreya",
            style="italic")
    lx = 0.08
    for face, edge, lab in ((INK2, None, "has the change"), (PAPER_DEEP, None, "does not"),
                            ("white", RULE, "fewer than two tokens")):
        ax.add_patch(Rectangle((lx, -2.45), 0.5, 0.55, facecolor=face, edgecolor=edge or face, lw=0.6))
        ax.text(lx + 0.65, -2.17, lab, va="center", fontsize=7.8, color=INK2, family="Alegreya")
        lx += {"has the change": 3.1, "does not": 2.4}.get(lab, 0)
    ax.set_xlim(-2.6, m + 2.9)
    ax.set_ylim(-2.6, n + 2.2)
    ax.set_aspect("auto")
    ax.axis("off")
    fig.savefig(os.path.join(FIG, "sounds.pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(FIG, "sounds.png"), dpi=200, bbox_inches="tight", pad_inches=0.02)
    with plt.rc_context({"svg.fonttype": "none"}):
        fig.savefig(os.path.join(FIG, "sounds.svg"), bbox_inches="tight", pad_inches=0.02, transparent=True)
    plt.close(fig)


# ---------------------------------------------------------------- triplets
TRIPLETS = [("(Welaun, NCT, Tetun)", "Welaun", "Tetun", "Welaun, with Tetun (control)", True),
            ("(LI, NCT, Tetun)", "LI", "Tetun", "Lakalei-Idate, with Tetun", False),
            ("(LI, NCT, Habu)", "LI", "Habu", "Lakalei-Idate, with Habu", False),
            ("(LI, NCT, Kawaimina)", "LI", "Kawaimina", "Lakalei-Idate, with Kawaimina", False),
            ("(LI, NCT, Galoli)", "LI", "Galoli", "Lakalei-Idate, with Galoli", False)]


def triplet_data():
    r = json.load(open(os.path.join(REPO, "results", "literature", "e18_triplets.json"), encoding="utf-8"))
    out = []
    for key, A, X, label, control in TRIPLETS:
        row = {}
        for stratum in ("stable", "other"):
            c = r[key][stratum]["counts"]
            row[stratum] = (c[f"{A}+NCT"], c[f"{A}+{X}"], c[f"NCT+{X}"])
        out.append(dict(label=label, A=A, X=X, control=control, **row))
    return out


def triplets_figure():
    D = triplet_data()
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.55), sharey=True, gridspec_kw=dict(wspace=0.06))
    cols = (BLUE, INK2, PAPER_DEEP)
    for ax, stratum, title in ((axes[0], "stable", "Stable concepts (Leipzig-Jakarta, 60)"),
                               (axes[1], "other", "Borrowable concepts (the other 92)")):
        for i, d in enumerate(D):
            v = d[stratum]
            tot = sum(v)
            left = 0
            for k, (val, col) in enumerate(zip(v, cols)):
                w = val / tot
                ax.barh(i, w, left=left, height=0.62, color=col, edgecolor="white", linewidth=1.2)
                if val:
                    ax.text(left + w / 2, i, str(val), ha="center", va="center", fontsize=7.6,
                            color="white" if k < 2 else INK, family="Alegreya")
                left += w
        ax.set_title(title, loc="left", fontsize=9, color=INK, family="Alegreya", pad=4)
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1])
        tl = ax.set_xticklabels(["0", "50%", "100%"], fontsize=7.5, family="Alegreya", color=INK3)
        tl[0].set_ha("left")
        tl[2].set_ha("right")
        ax.tick_params(length=0)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(RULE)
        ax.axvline(0.5, color=RULE, lw=0.6, zorder=0)
    axes[0].set_yticks(range(len(D)))
    axes[0].set_yticklabels([d["label"] for d in D], fontsize=8.6, color=INK)
    axes[0].invert_yaxis()
    axes[0].axhline(0.5, color=RULE, lw=0.6)
    axes[1].axhline(0.5, color=RULE, lw=0.6)
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in cols]
    labs = ["Focal group + Nuclear Central Timor", "Focal group + third group",
            "Nuclear Central Timor + third group"]
    fig.legend(handles, labs, loc="lower center", ncol=3, frameon=False, fontsize=7.8, bbox_to_anchor=(0.42, -0.1),
               handlelength=1.1, columnspacing=1.4, prop={"family": "Alegreya", "size": 7.8})
    fig.savefig(os.path.join(FIG, "triplets.pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(FIG, "triplets.png"), dpi=200, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    json.dump(D, open(os.path.join(DATA, "triplets.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    if sys.argv[1:] == ["clip"]:
        clip()
    map_figure()
    tree_figure()
    sounds_figure()
    triplets_figure()
    print("figures written to", FIG)
