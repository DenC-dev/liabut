"""Build the Sanak website (one self-contained page in the Phaistos Labs design).

    python3 paper/make_site.py

Writes docs/index.html (for GitHub Pages, with docs/sanak.pdf beside it) and paper/build/site.html (the same page
without the document wrapper, for publishing as an artifact). Run paper/make_figures.py first.
"""
import base64
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
GH = "https://github.com/DenC-dev/sanak"

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


# ---------------------------------------------------------------- triplet bars (HTML)
def triplet_bars():
    D = mf.triplet_data()
    names = {"Welaun": "Welaun", "LI": "Lakalei-Idate"}
    rows = []
    for d in D:
        cells = []
        for stratum, lab in (("stable", "Stable"), ("other", "Borrowable")):
            v = d[stratum]
            tot = sum(v)
            focal = names[d["A"]]
            pair = [f"{focal} + Nuclear Central Timor", f"{focal} + {d['X']}", f"Nuclear Central Timor + {d['X']}"]
            segs = []
            for k, (val, p) in enumerate(zip(v, pair)):
                w = 100 * val / tot
                tip = f"<b>{esc(p)}</b><br>{val} of {tot} {lab.lower()} concepts ({w:.0f}%)"
                segs.append(f'<span class="seg s{k}" style="width:{w:.2f}%" tabindex="0" data-tip="{esc(tip)}" '
                            f'aria-label="{esc(p)}: {val}">{val if w >= 6 else ""}</span>')
            cells.append(f'<div class="bar-cell"><span class="stratum">{lab}</span>'
                         f'<div class="stack">{"".join(segs)}</div></div>')
        cls = "trow control" if d["control"] else "trow"
        rows.append(f'<div class="{cls}"><div class="tlabel">{esc(d["label"])}</div>{"".join(cells)}</div>')
    return "\n".join(rows)


# ---------------------------------------------------------------- page
def build():
    logo = base64.b64encode(open(os.path.join(HERE, "figures", "phaistos_logo.png"), "rb").read()).decode()
    logo = f"data:image/png;base64,{logo}"
    page = open(os.path.join(HERE, "site_template.html"), encoding="utf-8").read()
    abc = json.load(open(os.path.join(LIT, "e21_borrowing_abc.json")))
    assert abc["model_posterior"]["G"] == 0.875
    subs = {"{{LOGO}}": logo, "{{ZOOM_MAP}}": zoom_svg(), "{{OVERVIEW_MAP}}": overview_svg(),
            "{{TREE}}": mpl_svg("tree", "tree", "fig-svg tree"), "{{SOUNDS}}": mpl_svg("sounds", "snd", "fig-svg sounds"),
            "{{TRIPLETS}}": triplet_bars(), "{{GH}}": GH}
    for k, v in subs.items():
        page = page.replace(k, v)
    head, body = page.split("<!--BODY-->")
    full = ("<!doctype html>\n<html lang=\"en-GB\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            f"<link rel=\"icon\" type=\"image/png\" href=\"{logo}\">\n{head}</head>\n<body>\n{body}</body>\n</html>\n")
    os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
    open(os.path.join(REPO, "docs", "index.html"), "w", encoding="utf-8").write(full)
    shutil.copy(os.path.join(HERE, "sanak.pdf"), os.path.join(REPO, "docs", "sanak.pdf"))
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    head_artifact = head.replace("<title>Sanak · Phaistos Labs</title>", "<title>Sanak</title>")
    open(os.path.join(HERE, "build", "site.html"), "w", encoding="utf-8").write(head_artifact + body)
    print("wrote docs/index.html and paper/build/site.html", len(full) // 1024, "KB")


if __name__ == "__main__":
    build()
