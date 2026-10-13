"""Build the Liabut website (one self-contained page in the Phaistos Labs design).

    python3 paper/make_site.py

Writes docs/index.html (for GitHub Pages, with docs/liabut.pdf beside it) and paper/build/site.html (the same page
without the document wrapper, for publishing as an artifact). Run paper/make_figures.py first.

The PDF links carry a content hash so that browsers never show a stale cached copy: `liabut.pdf?v=<hash>` on GitHub
Pages, and `liabut-<hash>.pdf` for the artifact, whose files are listed in paper/build/artifact_files.json.
"""
import base64
import glob
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("mf", os.path.join(HERE, "make_figures.py"))
mf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mf)
LIT = os.path.join(REPO, "results", "literature")
GH = "https://github.com/DenC-dev/liabut"

GROUP_NAME = {
    "mamb1306-Slete": "Central Timor", "kema1243-kaila": "Central Timor", "tuku1254": "Central Timor",
    "west2547-welaun": "Central Timor", "idat1237-cribas": "Lakalei-Idate", "laka1255": "Lakalei-Idate",
    "tetu1245-suai": "Eastern Timor", "habu1241": "Eastern Timor", "waim1252": "Eastern Timor (Kawaimina)",
    "midi1237": "Eastern Timor (Kawaimina)", "naue1237": "Eastern Timor (Kawaimina)", "galo1243": "Wetar-Atauro",
    "dadu1237": "Wetar-Atauro", "ilma1240": "Wetar-Atauro", "kaha1239": "Wetar-Atauro", "funa1237": "Helong",
    "koto1251": "Meto (Rote-Meto)", "term1237": "Rote (Rote-Meto)", "dela1252": "Rote (Rote-Meto)",
    "kisa1266": "Kisar-Luang", "luan1264": "Kisar-Luang", "tela1241": "Babar",
    "lama1277-lewoi": "Flores, outgroup", "sika1262-hewa": "Flores, outgroup",
}
HULL = {"mamb1306-Slete": "Ramelaic", "kema1243-kaila": "Ramelaic", "tuku1254": "Ramelaic",
        "idat1237-cribas": "Ramelaic", "laka1255": "Ramelaic", "tetu1245-suai": "Fabronic", "habu1241": "Fabronic",
        "waim1252": "Fabronic", "midi1237": "Fabronic", "naue1237": "Fabronic", "galo1243": "Fabronic",
        "west2547-welaun": "Fabronic", "koto1251": "Fabronic"}
CLS = {"CT": "ct", "LI": "li", "ET": "et", "other": "oth"}


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- SVG maps
def proj(box, width):
    x0, x1, y0, y1 = box
    k = 1 / np.cos(np.radians(9))
    s = width / (x1 - x0)
    return (lambda lon, lat: ((lon - x0) * s, (y1 - lat) * s * k)), width, (y1 - y0) * s * k


def land_paths(P):
    from shapely.geometry import shape
    d = []
    for f in json.load(open(os.path.join(HERE, "data", "land.geojson")))["features"]:
        g = shape(f["geometry"])
        for p in getattr(g, "geoms", [g]):
            if p.geom_type != "Polygon":
                continue
            pts = [P(x, y) for x, y in p.exterior.coords]
            d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    border = []
    for f in json.load(open(os.path.join(HERE, "data", "border.geojson")))["features"]:
        g = shape(f["geometry"])
        for ln in getattr(g, "geoms", [g]):
            if ln.geom_type == "LineString":
                border.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in (P(*c) for c in ln.coords)))
    return "".join(d), "".join(border)


def tip_for(t):
    g = mf.GROUP[t]
    hull = HULL.get(t)
    rows = [f"<b>{esc(mf.NAME[t])}</b>", esc(GROUP_NAME[t])]
    if hull:
        rows.append(f"Hull: {hull}")
    rows.append(f"<span class='muted'>LexiRumah {esc(t)}</span>")
    return "<br>".join(rows), g


def dot(x, y, t, r):
    tip, g = tip_for(t)
    label = f"{mf.NAME[t]}, {GROUP_NAME[t]}"
    return (f'<circle class="pt {CLS[g]}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" tabindex="0" role="img" '
            f'aria-label="{esc(label)}" data-tip="{esc(tip)}"></circle>')


def zoom_svg():
    P, W, H = proj(mf.ZOOM, 600)
    land, border = land_paths(P)
    L = mf.lects()
    inside = [t for t, (x, y) in L.items() if mf.ZOOM[0] < x < mf.ZOOM[1] and mf.ZOOM[2] < y < mf.ZOOM[3]]
    out = [f'<svg class="map" viewBox="0 0 {W:.0f} {H:.0f}" role="group" aria-labelledby="map-cap">',
           f'<path class="land" d="{land}"/><path class="border" d="{border}"/>']
    for txt, lon, lat in (("Timor-Leste", 126.3, -8.86), ("Indonesia", 124.9, -9.36), ("Ombai Strait", 125.2, -8.4),
                          ("Timor Sea", 126.3, -9.25)):
        x, y = P(lon, lat)
        out.append(f'<text class="place" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{txt}</text>')
    anchor = {"left": "start", "right": "end", "center": "middle"}
    for t in inside:
        lon, lat = L[t]
        x, y = P(lon, lat)
        lx, ly, ha = mf.ZOOM_LAB[t]
        X, Y = P(lx, ly)
        if abs(lx - lon) > 0.09 or abs(ly - lat) > 0.09:
            ex = X + (3 if ha == "right" else -3 if ha == "left" else 0)
            out.append(f'<line class="leader" x1="{x:.1f}" y1="{y:.1f}" x2="{ex:.1f}" y2="{Y:.1f}"/>')
    for t in inside:
        lon, lat = L[t]
        x, y = P(lon, lat)
        lx, ly, ha = mf.ZOOM_LAB[t]
        X, Y = P(lx, ly)
        g = mf.GROUP[t]
        out.append(f'<text class="lab {CLS[g]}" x="{X:.1f}" y="{Y + 5:.1f}" text-anchor="{anchor[ha]}">'
                   f'{esc(mf.NAME[t])}</text>')
        out.append(dot(x, y, t, 6.5))
    km = 25 / (111.32 * np.cos(np.radians(9)))
    x0, y0 = P(126.55, -9.38)
    x1, _ = P(126.55 + km, -9.38)
    out.append(f'<path class="scale" d="M{x0:.1f},{y0 - 3:.1f}V{y0 + 3:.1f}M{x0:.1f},{y0:.1f}H{x1:.1f}'
               f'M{x1:.1f},{y0 - 3:.1f}V{y0 + 3:.1f}"/>'
               f'<text class="place up" x="{(x0 + x1) / 2:.1f}" y="{y0 - 7:.1f}" text-anchor="middle">25 km</text>')
    out.append("</svg>")
    return "".join(out)


def overview_svg():
    P, W, H = proj(mf.BBOX, 640)
    land, border = land_paths(P)
    L = mf.lects()
    out = [f'<svg class="map" viewBox="0 0 {W:.0f} {H:.0f}" role="group" aria-labelledby="overview-cap">',
           f'<path class="land" d="{land}"/><path class="border" d="{border}"/>']
    zx0, zy0 = P(mf.ZOOM[0], mf.ZOOM[3])
    zx1, zy1 = P(mf.ZOOM[1], mf.ZOOM[2])
    out.append(f'<rect class="zoombox" x="{zx0:.1f}" y="{zy0:.1f}" width="{zx1 - zx0:.1f}" height="{zy1 - zy0:.1f}"/>')
    for txt, lon, lat in (("Flores", 122.55, -8.92), ("Timor", 124.35, -9.75), ("Rote", 122.9, -10.62),
                          ("Wetar", 126.25, -7.55), ("Atauro", 125.55, -8.08), ("Savu Sea", 123.0, -9.6),
                          ("Banda Sea", 127.9, -7.6), ("Timor Sea", 127.0, -9.95)):
        x, y = P(lon, lat)
        out.append(f'<text class="place" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{txt}</text>')
    anchor = {"left": "start", "right": "end", "center": "middle"}
    for t, (lon, lat) in L.items():
        x, y = P(lon, lat)
        if t in mf.OVER_LAB:
            dx, dy, ha = mf.OVER_LAB[t]
            X, Y = P(lon + dx, lat + dy)
            out.append(f'<text class="lab small" x="{X:.1f}" y="{Y + 4:.1f}" text-anchor="{anchor[ha]}">'
                       f'{esc(mf.NAME[t])}</text>')
            out.append(dot(x, y, t, 5))
        else:
            out.append(dot(x, y, t, 3.2))
    out.append("</svg>")
    return "".join(out)


def mpl_svg(name, prefix, cls):
    s = open(os.path.join(HERE, "figures", f"{name}.svg"), encoding="utf-8").read()
    s = s[s.index("<svg"):]
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    s = re.sub(r'\swidth="[^"]+pt"\sheight="[^"]+pt"', "", s, count=1)
    s = s.replace("<svg ", f'<svg class="{cls}" role="img" ', 1)
    s = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', s)
    s = re.sub(r'url\(#([^)]+)\)', lambda m: f"url(#{prefix}-{m.group(1)})", s)
    s = re.sub(r'xlink:href="#([^"]+)"', lambda m: f'xlink:href="#{prefix}-{m.group(1)}"', s)
    s = re.sub(r">\s+<", "><", s)
    return s


# ---------------------------------------------------------------- interactive vocabulary tree (SVG)
GE_GROUP = {t: mf.GROUP[t] for t in mf.NAME}
HULL_GROUP = {t: ("R" if v == "Ramelaic" else "F") for t, v in HULL.items()}


def vocab_tree_svg():
    from io import StringIO
    from Bio import Phylo
    names = dict(mf.NAME, **mf.OUTG)
    txt = open(os.path.join(LIT, "e40", "mb", "primary.con.tre")).read()
    trans = dict(re.findall(r"^\s*(\d+)\s+([^,;\s]+)[,;]?\s*$", txt.split("translate")[1].split(";")[0], re.M))
    nwk = [ln for ln in txt.splitlines() if ln.strip().startswith("tree con_")][0].split("=", 1)[1].strip()
    nwk = re.sub(r"\[&prob=([0-9.eE+-]+)[^\]]*\]", lambda m: f"PP{float(m.group(1)):.3f}", nwk)
    nwk = re.sub(r"\[[^\]]*\]", "", nwk)
    t = Phylo.read(StringIO(nwk), "newick")
    key = {re.sub(r"[^A-Za-z0-9_]", "_", k): k for k in names}
    for c in t.find_clades():
        if c.is_terminal():
            nm = c.name.split("PP")[0]
            c.name = key[trans.get(nm, nm)]
            c.confidence = None
        elif c.name and c.name.startswith("PP"):
            c.confidence = float(c.name[2:])
            c.name = None
        else:
            c.confidence = None
    t.root_with_outgroup([c for c in t.get_terminals() if c.name == "og-tagalog"][0])
    t.ladderize(reverse=True)
    tips = t.get_terminals()
    row, top, x0, xl = 19, 16, 12, 318
    depth, parent = {}, {}

    def walk(c, d):
        depth[id(c)] = d
        for ch in c.clades:
            parent[id(ch)] = c
            walk(ch, d + 1)
    walk(t.root, 0)
    maxd = max(depth[id(c)] for c in tips)
    dx = (xl - x0) / maxd
    ypos = {id(c): top + i * row for i, c in enumerate(tips)}

    def y(c):
        if id(c) not in ypos:
            ypos[id(c)] = (y(c.clades[0]) + y(c.clades[-1])) / 2
        return ypos[id(c)]

    def x(c):
        return xl if c.is_terminal() else x0 + depth[id(c)] * dx
    nodes = list(t.find_clades(order="preorder"))
    nid = {id(c): i for i, c in enumerate(nodes)}
    W, H = 476, top + (len(tips) - 1) * row + 16
    out = [f'<svg class="vt by-ge" id="vt" viewBox="0 0 {W} {H:.0f}" role="group" aria-labelledby="vt-cap">',
           f'<path class="vt-stem" d="M{x0 - 8},{y(t.root):.1f}H{x0}"/>', '<g class="vt-edges">']
    for c in nodes:
        if c is t.root:
            continue
        p = parent[id(c)]
        out.append(f'<path class="vt-e" id="vte{nid[id(c)]}" d="M{x(p):.1f},{y(p):.1f}V{y(c):.1f}H{x(c):.1f}"/>')
    out.append("</g><g class=\"vt-nodes\">")
    for c in nodes:
        if c.is_terminal() or c is t.root or c.confidence is None:
            continue
        pp = c.confidence
        members = [names[l.name] for l in c.get_terminals()]
        desc = " ".join(f"vte{nid[id(d)]}" for d in c.find_clades() if d is not c)
        share = "more than 99%" if pp >= 0.995 else f"{100 * pp:.0f}%"
        if len(members) <= 8:
            mem = ", ".join(members[:-1]) + " and " + members[-1]
        else:
            mem = ", ".join(members[:5]) + f" and {len(members) - 5} more"
        tip = (f"<b>{pp:.2f}</b> posterior<br>{esc(mem)} form a group in {share} of sampled trees")
        lab = f'<text class="vt-pp" x="{x(c) - 3:.1f}" y="{y(c) - 4:.1f}" text-anchor="end">{pp:.2f}</text>'.replace(
            ">0.", ">.") if pp < 0.995 else ""
        out.append(f'<g class="vt-n" tabindex="0" role="img" aria-label="{esc(f"Posterior {pp:.2f}: {mem}")}" '
                   f'data-tip="{esc(tip)}" data-desc="{desc}">{lab}'
                   f'<circle class="vt-hit" cx="{x(c):.1f}" cy="{y(c):.1f}" r="9"/>'
                   f'<circle class="vt-dot" cx="{x(c):.1f}" cy="{y(c):.1f}" r="2.4"/></g>')
    out.append("</g><g class=\"vt-leaves\">")
    for c in tips:
        nm = c.name
        yy = y(c)
        if nm in mf.OUTG:
            tip = f"<b>{esc(mf.OUTG[nm])}</b><br>Outgroup, outside the Timor region"
            out.append(f'<g class="leaf og" data-ge="out" data-hull="out" tabindex="0" data-tip="{esc(tip)}">'
                       f'<circle cx="{xl}" cy="{yy:.1f}" r="3.2"/>'
                       f'<text x="{xl + 9}" y="{yy + 4.2:.1f}">{esc(mf.OUTG[nm])}</text></g>')
            continue
        ge = GE_GROUP[nm]
        hull = HULL_GROUP.get(nm, "none")
        tip = (f"<b>{esc(mf.NAME[nm])}</b><br>Grimes and Edwards: {esc(GROUP_NAME[nm])}"
               f"<br>Hull: {esc(HULL.get(nm, 'not classified here'))}")
        li = " li" if ge == "LI" else ""
        out.append(f'<g class="leaf{li}" data-ge="{ge}" data-hull="{hull}" tabindex="0" data-tip="{esc(tip)}">'
                   f'<circle cx="{xl}" cy="{yy:.1f}" r="4.4"/>'
                   f'<text x="{xl + 9}" y="{yy + 4.2:.1f}">{esc(mf.NAME[nm])}</text></g>')
    out.append("</g></svg>")
    return "".join(out)


# ---------------------------------------------------------------- data for the interactive pieces
WORD_LECTS = [("CT", ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun"]),
              ("LI", ["laka1255", "idat1237-cribas"]),
              ("ET", ["tetu1245-suai", "habu1241", "waim1252", "naue1237", "midi1237"]),
              ("OUT", ["lama1277-lewoi", "sika1262-hewa"])]
# per concept: lect -> (regex to highlight or None, chip text, chip kind); kinds: ct, east, old
WORDS = [
    dict(id="four", gloss="four", pmp="*əpat", look="Look at the *p in the middle of the word.", lean="east",
         lean_text="Points to Timor-Babar",
         take=("Mambae, Kemak and Tokodede keep the old *p. Lakalei, Idaté and the eastern languages have lost it "
               "or weakened it to h. Grimes and Edwards define Timor-Babar by this change. Welaun complicates it: a "
               "Central Timor language on every other count, it has h too, so the change happened at least twice "
               "on Timor."),
         lects={"mamb1306-Slete": ("f", "f", "ct"), "kema1243-kaila": ("p", "p", "ct"), "tuku1254": ("p", "p", "ct"),
                "west2547-welaun": ("h", "h", "east"), "laka1255": ("ʔ", "ʔ", "east"),
                "idat1237-cribas": (None, "lost", "east"), "tetu1245-suai": ("h", "h", "east"),
                "habu1241": ("^h", "h", "east"), "waim1252": ("h", "h", "east"), "naue1237": ("h", "h", "east"),
                "midi1237": ("h", "h", "east"), "lama1277-lewoi": ("p", "p", "ct")}),
    dict(id="name", gloss="name", pmp="*ŋajan", look="Look at the first sound, which was *ŋ (the ng of sing).",
         lean="both", lean_text="Fits both trees",
         take=("Central Timor turned *ŋ into g or k. Lakalei and Idaté have n, like the eastern languages and "
               "Flores. Not sharing Central Timor’s change fits Grimes and Edwards. It also fits a tree in which "
               "Lakalei-Idate branched off just before Central Timor made the change."),
         lects={"mamb1306-Slete": ("^k", "k", "ct"), "kema1243-kaila": ("^g", "g", "ct"),
                "tuku1254": ("^g", "g", "ct"), "west2547-welaun": ("^k", "k", "ct"),
                "laka1255": ("^n", "n", "east"), "idat1237-cribas": ("^n", "n", "east"),
                "tetu1245-suai": ("n", "n", "east"), "habu1241": ("^n", "n", "east"),
                "waim1252": ("^n", "n", "east"), "naue1237": ("^n", "n", "east"), "midi1237": ("^n", "n", "east"),
                "lama1277-lewoi": ("n", "n", "east"), "sika1262-hewa": ("^n", "n", "east")}),
    dict(id="cry", gloss="to cry", pmp="*taŋis", look="Look at which word each language uses.", lean="ct",
         lean_text="Points to Central Timor",
         take=("Only Central Timor and Lakalei-Idate replaced the old word *taŋis. A new word shared by a group is "
               "the kind of clue that points to a common ancestor, and here it points to Hull’s grouping. Such "
               "words are few, though: after review, two (‘cry’ and ‘spit’), against up to nine shared only with "
               "eastern groups that nobody has yet checked by hand."),
         lects={"mamb1306-Slete": (None, "new word", "ct"), "kema1243-kaila": (None, "new word", "ct"),
                "tuku1254": (None, "new word", "ct"), "west2547-welaun": (None, "new word", "ct"),
                "laka1255": (None, "new word", "ct"), "idat1237-cribas": (None, "new word", "ct"),
                "tetu1245-suai": (None, "*taŋis", "old"), "waim1252": (None, "*taŋis", "old"),
                "midi1237": (None, "*taŋis", "old"), "lama1277-lewoi": (None, "*taŋis", "old"),
                "sika1262-hewa": (None, "*taŋis", "old")}),
    dict(id="eye", gloss="eye", pmp="*mata", look="Look at how similar the words are.", lean="none",
         lean_text="Says nothing",
         take=("Nearly every Austronesian language kept *mata. A word that everyone kept says nothing about who "
               "belongs with whom. That is why the study separates old words from new ones, and why mistaking one "
               "for the other is a real source of error."),
         lects={t: (None, "*mata", "old") for t in ["mamb1306-Slete", "kema1243-kaila", "tuku1254",
                                                     "west2547-welaun", "laka1255", "idat1237-cribas",
                                                     "tetu1245-suai", "habu1241", "waim1252", "naue1237",
                                                     "midi1237", "lama1277-lewoi", "sika1262-hewa"]}),
]
WORD_CONCEPT = {"four": "four", "name": "name", "cry": "to_cry", "eye": "eye"}


def word_data():
    import csv
    forms = {}
    for r in csv.DictReader(open(os.path.join(REPO, "data", "d1", "forms.csv"), encoding="utf-8")):
        forms.setdefault((r["Lect_ID"], r["Concept_ID"]), r)   # first form of each list, as in LexiRumah
    out = []
    for w in WORDS:
        cols = []
        for grp, lects in WORD_LECTS:
            items = []
            for t in lects:
                if t not in w["lects"]:
                    continue
                rx, chip, kind = w["lects"][t]
                r = forms[(t, WORD_CONCEPT[w["id"]])]
                form = r["Form"].replace("_", " ").replace("+", "-")
                if rx:
                    m = re.search(rx, form)
                    assert m, (w["id"], t, form, rx)
                    form_html = esc(form[:m.start()]) + f"<mark>{esc(m.group(0))}</mark>" + esc(form[m.end():])
                else:
                    form_html = esc(form)
                items.append(dict(lang=mf.NAME[t], form=form_html, chip=chip, kind=kind, src=r["Source"]))
            cols.append(dict(group=grp, items=items))
        out.append(dict(id=w["id"], gloss=w["gloss"], pmp=w["pmp"], look=w["look"], lean=w["lean"],
                        lean_text=w["lean_text"], take=w["take"], cols=cols))
    return out


def root_data():
    e40 = json.load(open(os.path.join(LIT, "e40_root.json")))
    e41 = json.load(open(os.path.join(LIT, "e41_relaxed_clock.json")))
    rows = [("All seven outgroups, Bayesian", e40["primary MrBayes"]),
            ("All seven outgroups, bootstrap", e40["primary UFBoot"]),
            ("Far outgroups only: Tagalog, Buginese, Uma", e40["far UFBoot"]),
            ("Near outgroups only: Kambera, Bima, Manggarai", e40["near UFBoot"]),
            ("Reconstructed Proto-Malayo-Polynesian only", e40["pmp UFBoot"]),
            ("Relaxed clock, no outgroups", e41["igr"]),
            ("Relaxed clock, without Tela-Masbuar", e41["igr_no_tela"])]
    e57 = json.load(open(os.path.join(LIT, "e57_root_sensitivity.json")))
    names57 = {"without tagalog": "Without Tagalog", "without buginese": "Without Buginese", "without uma": "Without Uma",
               "without kambera": "Without Kambera", "without bima": "Without Bima",
               "without manggarai": "Without Manggarai", "without pmp": "Without the PMP reconstruction",
               "missing coded as absent": "Missing data coded as absence",
               "only concepts attested in all seven outgroups": "Only the 99 concepts all seven outgroups have"}
    rows = [(lab, d, "main") for lab, d in rows] + [(names57[k], e57[k]["UFBoot"], "e57") for k in names57]
    out = []
    for label, d, group in rows:
        c = d["root_categories"]
        fl, rmh = c["Flores pair | rest"], c["Rote-Meto + Helong (with or without Flores) | rest"]
        ct = c["Central Timor (with or without Welaun) | rest"] + c["Lakalei-Idate + Central Timor | rest"]
        assert ct == 0.0
        kl = c["Kisar-Luang-Tela-Masbuar or part | rest"]
        out.append(dict(label=label, group=group, flores=round(fl, 3), rmh=round(rmh, 3), kl=round(kl, 3),
                        other=round(max(0.0, 1 - fl - rmh), 3), ct=ct,
                        clade=round(d["rooted_clades"]["LI + Central Timor (with or without Welaun)"], 2)))
    return out


def triplet_steps():
    e46 = json.load(open(os.path.join(LIT, "e46_triplets_clean.json")))
    e51 = json.load(open(os.path.join(LIT, "e51_partial_cognates.json")))
    steps = [("As first counted", "The validated retention rule, before any review.", e46["R2 baseline"]),
             ("Old words removed", "66 sets reclassified as old words or errors, after review and two "
                                   "etymological checks.", e46["R2 cleaned"]),
             ("Also without words found in Flores, Rote-Meto or Wetar",
              "A word these outside languages also have is probably old, so it is set aside.",
              e46["R2 cleaned and polarised (Flores, Rote-Meto + Helong, Wetar)"]),
             ("Coded by word parts, not checked by hand",
              "Each part of a compound counted as its own word, then set aside as above. Not reviewed, and it "
              "may pick up Tetun loans inside compounds.", e51["triplets R2 polarised"])]
    out = {}
    for X in ("Tetun", "Habu", "Kawaimina"):
        rows = []
        for label, note, d in steps:
            c = d[f"representative (LI, NCT, {X})"]["stable"]["counts"]
            rows.append(dict(label=label, note=note, v=[c["LI+NCT"], c[f"LI+{X}"], c[f"NCT+{X}"]]))
        out[X] = rows
    return out


def reversibility():
    d = json.load(open(os.path.join(LIT, "e56_reversibility.json")))
    sets = {"p": "p lenition", "e42": "eleven E42 characters", "e53": "36 E53 characters"}
    return dict(ratios=d["ratios"], sets={k: [d[v][str(r)]["cost"] for r in d["ratios"]] for k, v in sets.items()})


# ---------------------------------------------------------------- page
def build():
    logo = base64.b64encode(open(os.path.join(HERE, "figures", "phaistos_logo.png"), "rb").read()).decode()
    logo = f"data:image/png;base64,{logo}"
    page = open(os.path.join(HERE, "site_template.html"), encoding="utf-8").read()
    abc = json.load(open(os.path.join(LIT, "e21_borrowing_abc.json")))
    assert abc["model_posterior"]["G"] == 0.875
    data = json.dumps(dict(words=word_data(), root=root_data(), triplets=triplet_steps(), rev=reversibility()),
                      ensure_ascii=False).replace("</", "<\\/")
    subs = {"{{LOGO}}": logo, "{{ZOOM_MAP}}": zoom_svg(), "{{OVERVIEW_MAP}}": overview_svg(),
            "{{VTREE}}": vocab_tree_svg(), "{{SOUNDS}}": mpl_svg("sounds", "snd", "fig-svg sounds"),
            "{{DATA}}": data, "{{GH}}": GH}
    for k, v in subs.items():
        page = page.replace(k, v)
    head, body = page.split("<!--BODY-->")
    full = ("<!doctype html>\n<html lang=\"en-GB\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            f"<link rel=\"icon\" type=\"image/png\" href=\"{logo}\">\n{head}</head>\n<body>\n{body}</body>\n</html>\n")
    pdfs = {k: (f, hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest()[:10])
            for k, f in (("{{PDF}}", "liabut.pdf"), ("{{SUPP}}", "liabut_supplement.pdf"))}
    os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
    docs = full
    for k, (f, h) in pdfs.items():
        docs = docs.replace(k, f"{f}?v={h}")
        shutil.copy(os.path.join(HERE, f), os.path.join(REPO, "docs", f))
    open(os.path.join(REPO, "docs", "index.html"), "w", encoding="utf-8").write(docs)
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    head_artifact = head.replace("<title>Liabut · Phaistos Labs</title>", "<title>Liabut</title>")
    art, files = head_artifact + body, {}
    for old in glob.glob(os.path.join(HERE, "build", "liabut*-*.pdf")):
        os.remove(old)
    for k, (f, h) in pdfs.items():
        name = f.replace(".pdf", f"-{h}.pdf")
        art = art.replace(k, name)
        shutil.copy(os.path.join(HERE, f), os.path.join(HERE, "build", name))
        files[name] = f"paper/build/{name}"
    open(os.path.join(HERE, "build", "site.html"), "w", encoding="utf-8").write(art)
    json.dump(files, open(os.path.join(HERE, "build", "artifact_files.json"), "w"), indent=1)
    print("wrote docs/index.html and paper/build/site.html", len(full) // 1024, "KB")


if __name__ == "__main__":
    build()
