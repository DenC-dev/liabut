"""Step 6: treelikeness (delta scores, Q-residuals) and a NeighborNet (PROTOCOL.md section 7, Addendum 2 A2.3).

    python3 src/08_network.py
"""
import importlib.util
import itertools
import json
import os

import numpy as np

from common import REF, RES, read_csv, write_csv
from pipeline import build, lect_names, roles

spec = importlib.util.spec_from_file_location("bayes", os.path.join(os.path.dirname(__file__), "09_bayes.py"))
bayes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bayes)


def delta_q(d):
    """Mean delta score and Q-residual (Holland et al. 2002; Gray et al. 2010), plus per-taxon means.
    Distances are normalised by their mean before computing Q-residuals."""
    n = d.shape[0]
    dn = d / np.nanmean(d[np.triu_indices(n, 1)])
    quads = np.array(list(itertools.combinations(range(n), 4)))
    i, j, k, l = quads.T
    s = np.stack([dn[i, j] + dn[k, l], dn[i, k] + dn[j, l], dn[i, l] + dn[j, k]], 1)
    s.sort(1)
    m3, m2, m1 = s[:, 0], s[:, 1], s[:, 2]
    den = m1 - m3
    delta = np.where(den > 0, (m1 - m2) / np.where(den > 0, den, 1), 0.0)
    q = (m1 - m2) ** 2
    per_d, per_q = np.zeros(n), np.zeros(n)
    cnt = np.zeros(n)
    for c in range(4):
        np.add.at(per_d, quads[:, c], delta)
        np.add.at(per_q, quads[:, c], q)
        np.add.at(cnt, quads[:, c], 1)
    return float(delta.mean()), float(q.mean()), per_d / cnt, per_q / cnt


def neighbornet(lects, d, names, groups, out_png, out_nex):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import splitspy.nnet.nnet_algo as nnet
    import splitspy.outlines.outline_algo as outline
    from splitspy.nnet import distances
    from splitspy.splits import splits_io
    from splitspy.splits.basic_split import split_dist

    labels = [names[l] for l in lects]
    mat = [list(map(float, row)) for row in d]
    cycle, splits = nnet.neighbor_net(labels, mat)
    # least-squares fit (SplitsTree definition). SplitsPy 0.0.10's ls_fit multiplies instead of summing the
    # residuals and always returns 100, so it is computed here.
    n = len(labels)
    sd = np.zeros((n, n))
    for sp in splits:
        a = [t - 1 for t in sp.part1()]
        b = [t - 1 for t in sp.part2()]
        for x in a:
            for y in b:
                sd[x, y] += sp.get_weight()
                sd[y, x] += sp.get_weight()
    dm = np.array(mat)
    fit = 100.0 * (1.0 - ((dm - sd) ** 2).sum() / (dm ** 2).sum())
    splits_io.print_splits_nexus(labels, splits, cycle, fit, filename=out_nex)
    graph, angles = outline.compute(labels, cycle, splits)

    colours = {"Central Timor": "#b5523b", "Lakalei-Idate": "#7a4fa3", "Eastern Timor": "#2f7d6d",
               "Wetar-Atauro": "#3a6ea5", "Rote-Meto": "#a07b1f", "Helong": "#8a8a3a",
               "Southwest Maluku": "#5b7f99", "Flores-Lembata (root)": "#777777"}
    fig, ax = plt.subplots(figsize=(11, 11))
    for e in graph.edges():
        a, b = e.src().pos, e.tar().pos
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#333333", lw=0.8)
    xs = [v.pos[0] for v in graph.nodes()]
    ys = [v.pos[1] for v in graph.nodes()]
    cx, cy = np.mean(xs), np.mean(ys)
    for v in graph.nodes():
        if v.label:
            x, y = v.pos
            ang = np.arctan2(y - cy, x - cx)
            g = groups.get(v.label, "")
            ax.text(x + 0.012 * np.cos(ang), y + 0.012 * np.sin(ang), v.label, fontsize=10,
                    color=colours.get(g, "#222222"), ha="left" if np.cos(ang) >= 0 else "right", va="center")
    for g, c in colours.items():
        ax.plot([], [], color=c, lw=6, label=g)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=9, title="Grimes & Edwards (2026) subgroup")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"NeighborNet, 24 lects, LexStat cognates (LexiRumah). Least-squares fit {fit:.1f}%", fontsize=11)
    ax.margins(0.18)
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    return fit


def main():
    os.makedirs(os.path.join(RES, "network"), exist_ok=True)
    os.makedirs(os.path.join(RES, "figures"), exist_ok=True)
    b = build("d1", "lexstat", "primary")
    lects, d = b["lects"], b["d"]
    role = roles()
    names = lect_names("d1")
    out, per_rows = {}, []
    sets = {"timor_an_37": [l for l in lects if role[l] == "Timor AN"],
            "austronesian_64": [l for l in lects if role[l] != "TAP"],
            "bayes_taxa_24": bayes.BAYES_TAXA}
    for key, sub in sets.items():
        idx = [lects.index(l) for l in sub]
        dm, qm, pd_, pq = delta_q(d[np.ix_(idx, idx)])
        out[key] = dict(lects=len(sub), mean_delta=round(dm, 4), mean_q_residual=round(qm, 5))
        if key == "timor_an_37":
            for l, a, q in zip(sub, pd_, pq):
                per_rows.append(dict(Lect_ID=l, Name=names[l], Delta=round(float(a), 4), Q_Residual=round(float(q), 5)))
    write_csv(os.path.join(RES, "network", "per_lect_delta_timor_an.csv"),
              sorted(per_rows, key=lambda r: -r["Delta"]))

    ge = {"Central Timor": ["mamb1306-Slete", "kema1243-kaila", "tuku1254", "west2547-welaun"],
          "Lakalei-Idate": ["idat1237-cribas", "laka1255"],
          "Eastern Timor": ["tetu1245-suai", "habu1241", "waim1252", "midi1237", "naue1237"],
          "Wetar-Atauro": ["galo1243", "dadu1237", "ilma1240", "kaha1239"],
          "Rote-Meto": ["koto1251", "term1237", "dela1252"], "Helong": ["funa1237"],
          "Southwest Maluku": ["kisa1266", "luan1264", "tela1241"],
          "Flores-Lembata (root)": ["lama1277-lewoi", "sika1262-hewa"]}
    short = {l: names[l].replace("Ile Mandiri Lamaholot, ", "Lamaholot ").replace("Southern Mambae, ", "Mambae ")
             .replace("South Mambae, ", "Mambae ") for l in lects}
    groups = {short[l]: g for g, ls in ge.items() for l in ls}
    idx = [lects.index(l) for l in bayes.BAYES_TAXA]
    fit = neighbornet(bayes.BAYES_TAXA, d[np.ix_(idx, idx)], short, groups,
                      os.path.join(RES, "figures", "neighbornet_24.png"),
                      os.path.join(RES, "network", "neighbornet_24.nex"))
    out["neighbornet_fit_percent"] = round(fit, 2)
    json.dump(out, open(os.path.join(RES, "network", "treelikeness.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("most reticulate Timor lects:", [(r["Name"], r["Delta"]) for r in sorted(per_rows, key=lambda r: -r["Delta"])[:8]])


if __name__ == "__main__":
    main()
