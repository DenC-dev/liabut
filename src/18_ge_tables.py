"""New data D-GE: a machine-readable version of the comparative tables in Grimes and Edwards (2026).

The book (CC-BY 4.0, LaTeX source at github.com/langsci/526) prints its evidence as tables: a gloss row, a PMP row
with the target segment in bold red (\\tbr{}), optional intermediate proto-rows (**), then one row per language with
the reflex of the target in bold red. Words that are not cognate are greyed (\\cg{}, \\tcg{}). This script reads
every such table and writes one row per language form, with the expert-highlighted reflex of each PMP target.

Output (derived/ge2026_tables/):
  forms.csv      one row per (table, column, language, variant)
  reflexes.csv   one row per highlighted PMP target and its reflex in that form
  languages.csv  table language names mapped to Glottocodes via the book's Appendix A (plus a short alias list)

    python3 src/18_ge_tables.py /path/to/langsci-526-repo
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

from common import REPO, write_csv

OUT = os.path.join(REPO, "derived", "ge2026_tables")
PROTO_ROW = re.compile(r"^(PMP|PAN|PCEMP|PCMP|PEMP|PWMP|POc)$")
GLOSS_ROW = re.compile(r"(^|\s)(\*?gloss|local gl\.?|local gloss|PMP gloss|gl\.)$", re.I)
ALIASES = {  # table row labels -> Glottocode, where Appendix A uses a different label or none
    "C. Mambae": "mamb1306", "S. Mambae": "mamb1306", "NW. Mambae": "mamb1306", "S. Mambae (H.)": "mamb1306",
    "S. Mambae (B.)": "mamb1306", "Mamb.": "mamb1306", "NW. Mam.": "mamb1306", "Mambae": "mamb1306",
    "Kailaku Kemak": "kema1243", "Kutubaba Kemak": "kema1243", "Marobo Kemak": "kema1243",
    "Saneri Kemak": "kema1243", "Liquiçá Tokodede": "tuku1254", "Maubara Tokodede": "tuku1254",
    "East Tetun": "east2473", "Kotos": "koto1251", "Roiʔis": "rois1241", "Kusa-M.": "kusa1252",
    "Dela-O.": "dela1251", "Oenale": "dela1251", "Molo": "moll1242", "Kisar": "kisa1266", "Tela": "tela1241",
    "Dawera": "dawe1237", "Midiki": "kair1265", "Waimaha": "waim1252", "E.Marsela": "east2462",
    "E. Damer": "east2472", "Bima": "bima1247", "Geser": "gese1240", "Geser-G.": "gese1240", "Kuri": "kuri1260",
    "Uruang.": "urua1244", "Sika, Hewa": "sika1262", "Sika, Tana Ai": "sika1262", "Lewoingu": "lama1277",
    "Kola": "kola1285", "East Kola": "kola1285", "West Kola": "kola1285", "N. Wemale": "nort2864",
    "N.Wemale": "nort2864", "S. Wemale": "sout2892", "Erokw.": "erok1237", "Masiwang": "masi1266",
    "Kamb.": "kamb1299", "Watub.": "watu1247",
}
NOT_LANGUAGE = re.compile(r"^(\d(sg|pl).*|Blust|Wolff|PRM gloss|change|gloss|local gl\.?)$", re.I)

def strip_cmd(s, name):
    """Replace \\name{X} by X, handling nested braces."""
    out, i, key = [], 0, "\\" + name + "{"
    while True:
        j = s.find(key, i)
        if j < 0:
            out.append(s[i:])
            return "".join(out)
        out.append(s[i:j])
        k, depth = j + len(key), 1
        while k < len(s) and depth:
            depth += {"{": 1, "}": -1}.get(s[k], 0)
            k += 1
        out.append(s[j + len(key):k - 1])
        i = k


def clean(cell):
    """LaTeX cell -> (plain text with ⟦⟧ around highlighted segments, non-cognate flag)."""
    c = cell.strip()
    noncog = "\\cg{" in c or "\\tcg{" in c
    c = re.sub(r"\\su\{[^}]*\}", "", c)
    c = re.sub(r"\\(hr|hqa|hq|hp\{[^}]*\}|st\{[^}]*\}|hphantom\{[^}]*\}|,|;|quad|enspace)", "", c)
    c = c.replace("{\\tl}", "~").replace("\\tl", "~").replace("{\\Q}", "ʔ").replace("\\Q", "ʔ")
    c = c.replace("{\\0}", "∅").replace("\\0", "∅")
    c = re.sub(r"\\tbr\{", "⟦{", c)
    # mark the end of highlighted spans: replace the matching brace of ⟦{ with }⟧
    out, depth_stack = [], []
    i = 0
    while i < len(c):
        if c.startswith("⟦{", i):
            out.append("⟦")
            depth_stack.append(0)
            i += 2
            continue
        ch = c[i]
        if depth_stack:
            if ch == "{":
                depth_stack[-1] += 1
            elif ch == "}":
                if depth_stack[-1] == 0:
                    depth_stack.pop()
                    out.append("⟧")
                    i += 1
                    continue
                depth_stack[-1] -= 1
        out.append(ch)
        i += 1
    c = "".join(out)
    for cmd in ("it", "tsc", "textit", "textbf", "cg", "tcg", "mc\\{[^}]*\\}\\{[^}]*\\}", "textsc", "emph"):
        if "\\" in cmd:
            c = re.sub(r"\\" + cmd + r"\{", "{", c)
        else:
            c = strip_cmd(c, cmd)
    c = re.sub(r"\\[a-zA-Z]+\*?", "", c)
    c = c.replace("{", "").replace("}", "").replace("$", "")
    c = re.sub(r"\s+", " ", c).strip()
    if noncog:
        c = c.strip("()")
    return c, noncog


def split_rows(body):
    body = re.sub(r"(?m)%.*$", "", body)
    rows = []
    for raw in re.split(r"\\\\", body):
        raw = re.sub(r"\\(midrule|lsptoprule|lspbottomrule|hline|toprule|bottomrule|cline\{[^}]*\}|hhline\{[^}]*\}|"
                     r"endhead|endfirsthead|endfoot|endlastfoot)", "", raw)
        if "&" not in raw:
            continue
        cells = re.split(r"(?<!\\)&", raw)
        rows.append([x.strip() for x in cells])
    return rows


def segments(text):
    """'**a⟦p⟧i' -> list of (segment string, highlighted?) splitting on highlight markers."""
    parts, hl = [], False
    for tok in re.split(r"(⟦|⟧)", text):
        if tok == "⟦":
            hl = True
        elif tok == "⟧":
            hl = False
        elif tok:
            parts.append((tok, hl))
    return parts


def lookup(name, langs):
    if name in ALIASES:
        return dict(Glottocode=ALIASES[name])
    for cand in (name, re.sub(r"\s*\(.*\)$", "", name), name.rstrip(".,")):
        if cand in langs:
            return langs[cand]
    return None


def appendix_languages(root):
    names = {}
    for fn in sorted(os.listdir(os.path.join(root, "chapters", "A-LanLis"))):
        for line in open(os.path.join(root, "chapters", "A-LanLis", fn), encoding="utf-8"):
            p = [x.strip() for x in line.split("&")]
            if len(p) >= 5 and re.fullmatch(r"\(?[a-z]{4}\d{4}\)?", p[2] or ""):
                nm, _ = clean(p[0].lstrip("%"))
                nm = nm.rstrip("-,").strip()
                names[nm] = dict(Glottocode=p[2].strip("()"), ISO=p[1].strip("()"), Latitude=p[3], Longitude=p[4])
    return names


def main(root):
    langs = appendix_languages(root)
    forms, reflexes, unknown = [], [], Counter()
    table_count = 0
    for dirpath, _, files in os.walk(os.path.join(root, "chapters")):
        for fn in sorted(files):
            if not fn.endswith(".tex") or "A-LanLis" in dirpath:
                continue
            src = open(os.path.join(dirpath, fn), encoding="utf-8").read()
            for m in re.finditer(r"\\begin\{(tabular|xltabular)\}(.*?)\\end\{\1\}", src, re.S):
                rows = split_rows(m.group(2))
                pi = next((i for i, r in enumerate(rows) if PROTO_ROW.match(clean(r[0])[0])), None)
                if pi is None:
                    continue
                before = src[:m.start()]
                lab = re.findall(r"\\tcp\{(.*?)\}\{([^}]*)\}", before[-600:], re.S)
                table_id = lab[-1][1] if lab else f"{fn}:{m.start()}"
                caption = clean(lab[-1][0])[0] if lab else ""
                gloss_row = rows[pi - 1] if pi > 0 and GLOSS_ROW.search(clean(rows[pi - 1][0])[0]) else None
                proto = [clean(c)[0] for c in rows[pi]]
                table_count += 1
                for r in rows[pi + 1:]:
                    name, _ = clean(r[0])
                    name = re.sub(r"^(-?[\d.]+(ex|mm)\s*|array[-\d.mm]*\\?\s*|\d+\s+)", "", name).strip()
                    if not name or name.startswith("*") or NOT_LANGUAGE.match(name) or \
                            (name.startswith("P") and "**" in "".join(r)):
                        continue
                    meta = lookup(name, langs)
                    if not meta:
                        unknown[name] += 1
                    for col in range(1, min(len(r), len(proto))):
                        etym = proto[col]
                        if not etym.startswith("*"):
                            continue
                        raw = r[col]
                        if not raw.strip():
                            continue
                        text, noncog = clean(raw)
                        if not text or text in ("-", "–"):
                            continue
                        gloss = clean(gloss_row[col])[0] if gloss_row and col < len(gloss_row) else ""
                        targets = [s for s, h in segments(etym) if h]
                        for vi, variant in enumerate(re.split(r"\s*[~,]\s*", text)):
                            if not variant:
                                continue
                            hl = [s for s, h in segments(variant) if h]
                            plain = variant.replace("⟦", "").replace("⟧", "")
                            fid = f"{table_id}-{col}-{len(forms)}"
                            forms.append(dict(ID=fid, Table=table_id, Caption=caption, File=fn, Column=col,
                                              Gloss=gloss, Etymon=etym.replace("⟦", "").replace("⟧", ""),
                                              Etymon_Marked=etym, Targets=" ".join(targets),
                                              Language=name, Glottocode=(meta or {}).get("Glottocode", ""),
                                              Form=plain, Form_Marked=variant, Cognate=not noncog,
                                              Highlighted=" ".join(hl)))
                            if noncog or not targets:
                                continue
                            if len(targets) == len(hl):
                                pairs = list(zip(targets, hl))
                            elif len(targets) == 1 and not hl:
                                pairs = [(targets[0], "")]  # cognate form, target not highlighted
                            else:
                                pairs = []
                            for t, x in pairs:
                                reflexes.append(dict(Form_ID=fid, Table=table_id, Caption=caption, Language=name,
                                                     Glottocode=(meta or {}).get("Glottocode", ""),
                                                     Etymon=etym.replace("⟦", "").replace("⟧", ""), Target=t,
                                                     Reflex=x if x else "(unmarked)", Form=plain))
    os.makedirs(OUT, exist_ok=True)
    write_csv(os.path.join(OUT, "forms.csv"), forms)
    write_csv(os.path.join(OUT, "reflexes.csv"), reflexes)
    used = Counter(f["Language"] for f in forms)
    write_csv(os.path.join(OUT, "languages.csv"),
              [dict(Name=n, Forms=c, Glottocode=(lookup(n, langs) or {}).get("Glottocode", ""))
               for n, c in used.most_common()])
    print(f"{table_count} tables, {len(forms)} forms, {len(reflexes)} reflexes, {len(used)} language labels; "
          f"unmapped labels: {len(unknown)} ({sum(unknown.values())} rows)")
    print("most common unmapped:", unknown.most_common(15))


if __name__ == "__main__":
    main(sys.argv[1])
