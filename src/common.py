"""Shared helpers: paths, token handling, sound-class distance, lexical distances, trees and clade checks."""
import csv
import os
import re

import numpy as np
from lingpy.sequence.sound_classes import ipa2tokens, tokens2class

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP = os.path.join(REPO, "data", "upstream")
DATA = os.path.join(REPO, "data")
REF = os.path.join(REPO, "reference")
RES = os.path.join(REPO, "results")
WORK = os.path.join(RES, "work")
SEED = 1234


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, header=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rows = list(rows)
    header = header or (list(rows[0].keys()) if rows else [])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# ----------------------------------------------------------------------------------------------- tokens
def clean_abvd(form):
    """ABVD Form -> tokens (protocol section 3). Returns None if unusable."""
    s = form.strip()
    s = re.sub(r"[-|=()\s]", "", s).replace(":", "ː")
    if not s:
        return None
    try:
        toks = ipa2tokens(s, merge_vowels=False, semi_diacritics="hsʃʂʒʐzθɕʑfvθðŋñ")
    except Exception:
        return None
    if not toks:
        return None
    cls = tokens2class(toks, "sca")
    if sum(c == "0" for c in cls) > len(cls) / 3:
        return None
    return toks


def _tie(t):
    return re.sub(r"([td])([ʃʒszɕʑ])", "\\1\u0361\\2", t) if "\u0361" not in t else t


def sca_string(tokens):
    """SCA sound-class string, with untied affricates (dʒ, tʃ, ts) read as affricates."""
    toks = [_tie(t) for t in tokens if t not in ("+", "_")]
    return "".join(tokens2class(toks, "sca"))


def ned(a, b):
    """Normalized edit distance between two strings."""
    if not a and not b:
        return 0.0
    la, lb = len(a), len(b)
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[lb] / max(la, lb)


INDO = [("ng", "ŋ"), ("ny", "ɲ"), ("sy", "ʃ"), ("kh", "x"), ("c", "t\u0361ʃ"), ("j", "d\u0361ʒ"), ("y", "j"), ("é", "e"),
        ("'", "ʔ")]
PORT = [("ção", "sãw"), ("ões", "õjs"), ("ão", "ãw"), ("ch", "ʃ"), ("lh", "ʎ"), ("nh", "ɲ"), ("qu", "k"),
        ("gu", "g"), ("ç", "s"), ("ce", "se"), ("ci", "si"), ("c", "k"), ("j", "ʒ"), ("x", "ʃ"), ("rr", "ʁ"),
        ("ss", "s"), ("h", ""), ("á", "a"), ("â", "a"), ("ã", "ã"), ("é", "e"), ("ê", "e"), ("í", "i"), ("ó", "o"),
        ("ô", "o"), ("õ", "õ"), ("ú", "u"), ("ge", "ʒe"), ("gi", "ʒi")]


def ortho_tokens(word, rules, articles=()):
    """Rough IPA tokens from a standard-orthography word (Indonesian or Portuguese), first variant only."""
    w = word.strip().lower()
    w = re.split(r"[,;/(]", w)[0].strip()
    for art in articles:
        if w.startswith(art + " "):
            w = w[len(art) + 1:]
    w = w.replace(" ", "").replace("-", "")
    for a, b in rules:
        w = w.replace(a, b)
    if not w:
        return None
    try:
        return ipa2tokens(w, merge_vowels=False)
    except Exception:
        return None


# ----------------------------------------------------------------------------------------------- distances
def cognate_tensors(rows, lects, concepts, key="Cognateset_ID"):
    """rows: dicts with Lect_ID, Concept_ID and a cognate-set column. Returns S (shared) and A (both attested)
    as arrays of shape (n_concepts, n_lects, n_lects)."""
    li = {l: i for i, l in enumerate(lects)}
    ci = {c: i for i, c in enumerate(concepts)}
    sets = {}
    for r in rows:
        if r[key] in ("", None) or r["Lect_ID"] not in li or r["Concept_ID"] not in ci:
            continue
        sets.setdefault((ci[r["Concept_ID"]], li[r["Lect_ID"]]), set()).add(r[key])
    n, m = len(concepts), len(lects)
    S = np.zeros((n, m, m), dtype=np.float32)
    A = np.zeros((n, m, m), dtype=np.float32)
    att = np.zeros((n, m), dtype=bool)
    for (c, l) in sets:
        att[c, l] = True
    for c in range(n):
        idx = np.where(att[c])[0]
        for a_ in idx:
            sa = sets[(c, a_)]
            for b_ in idx:
                A[c, a_, b_] = 1
                if sa & sets[(c, b_)]:
                    S[c, a_, b_] = 1
    return S, A


def distance(S, A, weights=None):
    if weights is None:
        s, a = S.sum(0), A.sum(0)
    else:
        s, a = np.tensordot(weights, S, 1), np.tensordot(weights, A, 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = 1 - s / a
    d[a == 0] = np.nan
    np.fill_diagonal(d, 0)
    return d, a


def fill_nan(d):
    """Replace missing distances (no shared concepts) by the row mean, so trees can be built; flagged upstream."""
    d = d.copy()
    if np.isnan(d).any():
        m = np.nanmean(d)
        d[np.isnan(d)] = m
    return d


# ----------------------------------------------------------------------------------------------- trees
def upgma_clusters(d):
    """Average-linkage clusters as frozensets of leaf indices, plus a Newick builder input."""
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import squareform
    n = d.shape[0]
    Z = linkage(squareform(fill_nan(d), checks=False), "average")
    members = {i: frozenset([i]) for i in range(n)}
    heights = {i: 0.0 for i in range(n)}
    children = {}
    clusters = []
    for k, (a, b, h, _) in enumerate(Z):
        node = n + k
        members[node] = members[int(a)] | members[int(b)]
        heights[node] = h / 2
        children[node] = (int(a), int(b))
        clusters.append(members[node])
    return set(clusters), (members, heights, children, n + len(Z) - 1)


def upgma_newick(d, names):
    _, (members, heights, children, root) = upgma_clusters(d)

    def rec(node, parent_h):
        bl = max(parent_h - heights[node], 0)
        if node in children:
            a, b = children[node]
            return f"({rec(a, heights[node])},{rec(b, heights[node])}):{bl:.5f}"
        return f"{names[node]}:{bl:.5f}"
    return rec(root, heights[root]).rsplit(":", 1)[0] + ";"


def nj(d):
    """Neighbour-joining (numpy). Returns the set of splits (leaf sets below each edge), the edge list and the centre."""
    D = fill_nan(d).astype(float).copy()
    n = D.shape[0]
    ids = list(range(n))
    leaves = {i: frozenset([i]) for i in range(n)}
    edges = []
    nxt = n
    while len(ids) > 3:
        r = len(ids)
        tot = D.sum(1)
        Q = (r - 2) * D - tot[:, None] - tot[None, :]
        np.fill_diagonal(Q, np.inf)
        x, y = np.unravel_index(np.argmin(Q), Q.shape)
        if x > y:
            x, y = y, x
        lx = 0.5 * D[x, y] + (tot[x] - tot[y]) / (2 * (r - 2))
        ly = D[x, y] - lx
        u = nxt
        nxt += 1
        i, j = ids[x], ids[y]
        leaves[u] = leaves[i] | leaves[j]
        edges += [(u, i, max(lx, 0)), (u, j, max(ly, 0))]
        newrow = 0.5 * (D[x] + D[y] - D[x, y])
        keep = [k for k in range(r) if k not in (x, y)]
        D2 = np.zeros((r - 1, r - 1))
        D2[:-1, :-1] = D[np.ix_(keep, keep)]
        D2[-1, :-1] = D2[:-1, -1] = newrow[keep]
        D = D2
        ids = [ids[k] for k in keep] + [u]
    a, b, c = ids
    la = 0.5 * (D[0, 1] + D[0, 2] - D[1, 2])
    lb = D[0, 1] - la
    lc = D[0, 2] - la
    centre = nxt
    edges += [(centre, a, max(la, 0)), (centre, b, max(lb, 0)), (centre, c, max(lc, 0))]
    splits = {leaves[child] for _, child, _ in edges}
    return splits, edges, centre


def nj_newick(d, names):
    _, edges, centre = nj(d)
    kids = {}
    for p, c, l in edges:
        kids.setdefault(p, []).append((c, l))

    def rec(node):
        if node not in kids:
            return names[node]
        return "(" + ",".join(f"{rec(c)}:{l:.5f}" for c, l in kids[node]) + ")"
    return rec(centre) + ";"


def recovered_rooted(clusters, group):
    return frozenset(group) in clusters


def recovered_unrooted(splits, group, n):
    g = frozenset(group)
    comp = frozenset(range(n)) - g
    return g in splits or comp in splits


def bootstrap_support(S, A, groups, reps=1000, seed=SEED, method="upgma"):
    """Share of concept-resampled trees that contain each group (list of index lists)."""
    rng = np.random.default_rng(seed)
    n_c, n = S.shape[0], S.shape[1]
    hits = np.zeros(len(groups))
    for _ in range(reps):
        w = np.bincount(rng.integers(0, n_c, n_c), minlength=n_c).astype(np.float32)
        d, _ = distance(S, A, w)
        if method == "upgma":
            cl, _ = upgma_clusters(d)
            hits += [recovered_rooted(cl, g) for g in groups]
        else:
            sp, _, _ = nj(d)
            hits += [recovered_unrooted(sp, g, n) for g in groups]
    return hits / reps
