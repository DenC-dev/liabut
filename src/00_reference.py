"""Write the frozen reference tables: lect selection, known-answer clades, hypothesis clades, ABVD-LexiRumah lect map.

Everything here is fixed before any cognate detection, distance or tree is computed. The CSVs it writes are
part of the pre-registration and are hashed in PROTOCOL.sha256.

    python3 src/00_reference.py
"""
import csv
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "reference")

# ---------------------------------------------------------------- D1: LexiRumah lects, by group
MAMBAE = ["mamb1306", "mamb1306-NWbar", "mamb1306-NWhat", "mamb1306-NWrai", "mamb1306-Claul", "mamb1306-Caile",
          "mamb1306-Cliqu", "mamb1306-Chatu", "mamb1306-Sudo", "mamb1306-Sbeta", "mamb1306-Slete"]
KEMAK = ["kema1243", "kema1243-kaila", "kema1243-kutu", "kema1243-leol", "kema1243-lemi", "kema1243-sane",
         "kema1243-leos", "kema1243-diir"]
TOKODEDE = ["tuku1254"]
WELAUN = ["west2547-welaun", "west2547-mahein"]
IDATE = ["idat1237", "idat1237-cribas"]
LAKALEI = ["laka1255"]
TETUN = ["tetu1246", "tetu1245-suai"]
HABU = ["habu1241"]
KAWAIMINA = ["waim1252", "midi1237", "naue1237"]
GALOLI = ["galo1243"]
DADUA = ["dadu1237"]
HELONG = ["funa1237"]
METO = ["koto1251", "rois1241", "kusa1252"]
AMARASI = ["koto1251", "rois1241"]
ROTE = ["term1237", "tiii1241", "dela1252", "lole1239", "ring1244"]
WETAR = ["eray1237", "ilma1240", "uhak1237", "ilpu1239", "kaha1239"]
ILIUUN = ["eray1237", "ilma1240"]
SWM_LK = ["kisa1266", "roma1332", "luan1264", "weta1243"]
LUANG = ["luan1264", "weta1243"]
BABAR = ["imro1237", "tela1241", "daii1240", "nort2860", "empl1237", "east2462", "sout2883", "cent2072", "seri1255",
         "dawe1237"]
FLORES_LEMBATA = ["sika1262-hewa", "lama1277-lewoi", "keda1252"]
BUNAK = ["buna1278-bobon", "buna1278-malia", "buna1278-suai"]
EAST_TAP = ["fata1247", "maka1316", "oira1263"]
FAT_OIR = ["fata1247", "oira1263"]

CENTRAL_TIMOR = MAMBAE + KEMAK + TOKODEDE + WELAUN
TIMOR_AN = MAMBAE + KEMAK + TOKODEDE + WELAUN + IDATE + LAKALEI + TETUN + HABU + KAWAIMINA + GALOLI + DADUA + HELONG + METO
TAP = BUNAK + EAST_TAP

GROUPS = [
    ("Mambae", "Timor AN", MAMBAE), ("Kemak", "Timor AN", KEMAK), ("Tokodede", "Timor AN", TOKODEDE),
    ("Welaun", "Timor AN", WELAUN), ("Idate", "Timor AN", IDATE), ("Lakalei", "Timor AN", LAKALEI),
    ("Tetun", "Timor AN", TETUN), ("Habu", "Timor AN", HABU), ("Kawaimina", "Timor AN", KAWAIMINA),
    ("Galoli", "Timor AN", GALOLI), ("Dadu'a", "Timor AN", DADUA), ("Helong", "Timor AN", HELONG),
    ("Meto", "Timor AN", METO), ("Rote", "Outgroup AN", ROTE), ("Wetar", "Outgroup AN", WETAR),
    ("Luangic-Kisaric", "Outgroup AN", SWM_LK), ("Babar", "Outgroup AN", BABAR),
    ("Flores-Lembata", "Root AN", FLORES_LEMBATA), ("Bunak", "TAP", BUNAK), ("East Timor TAP", "TAP", EAST_TAP),
]

# ---------------------------------------------------------------- D2: ABVD languages (IDs), by group
A = dict(tetum=134, tetun_terik=403, tetun_fehan=1366, mambai=167, kemak=61, tokodede=1367, galolen=300,
         waimaa=1368, naueti=1365, dadua=1362, atoni=42, termanu=115, kisar=160, roma=332, leti=70, luang=301,
         wetan=853, iliun=296, iliun_erai=35, tugun=297, perai=298, aputai=299, dawera=307, dai=308,
         north_babar=309, se_babar=310, serili=311, east_masela=312, central_masela=313, emplawas=314,
         tela_masbuar=315, imroing=316, lamaholot=34, kedang=236, lamalera=486)


def a(*names):
    return [str(A[n]) for n in names]


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    os.makedirs(OUT, exist_ok=True)

    write("d1_lects.csv", ["Lect_ID", "Group", "Role"],
          [(lid, g, role) for g, role, ids in GROUPS for lid in ids])

    # Known-answer clades: dialect groups of one language, and low-level groups no one disputes.
    # Tier 1 = dialects of one Glottolog language; Tier 2 = established low-level groups and the family split.
    ka = [
        ("KA1-mambae", "D1", 1, "Mambae dialects", MAMBAE, "Glottolog 5.3: all mamb1306"),
        ("KA1-kemak", "D1", 1, "Kemak dialects", KEMAK, "Glottolog 5.3: all kema1243"),
        ("KA1-bunak", "D1", 1, "Bunak dialects", BUNAK, "Glottolog 5.3: all buna1278"),
        ("KA1-idate", "D1", 1, "Idate varieties", IDATE, "Glottolog 5.3: idat1237"),
        ("KA1-welaun", "D1", 1, "Welaun varieties", WELAUN, "Glottolog 5.3: wela1235"),
        ("KA1-tetun", "D1", 1, "Tetun Dili + Southern Tetun", TETUN, "Glottolog 5.3: Tetunic"),
        ("KA1-amarasi", "D1", 1, "Amarasi (Kotos, Ro'is)", AMARASI, "Glottolog 5.3: amar1273"),
        ("KA1-iliuun", "D1", 1, "Ili'uun (Eray, Ilmaumau)", ILIUUN, "Glottolog 5.3: iliu1237"),
        ("KA1-luang", "D1", 1, "Luang (Luang island, Wetan)", LUANG, "Glottolog 5.3: luan1263"),
        ("KA2-meto", "D1", 2, "Meto", METO, "Glottolog 5.3: Meto"),
        ("KA2-rotemeto", "D1", 2, "Rote-Meto", ROTE + METO, "Glottolog 5.3: Rote-Meto"),
        ("KA2-fatoir", "D1", 2, "Fataluku-Oirata", FAT_OIR, "Glottolog 5.3: Fataluku-Oirata"),
        ("KA2-eastTAP", "D1", 2, "East Timor TAP", EAST_TAP, "Glottolog 5.3: East Timor (TAP)"),
        ("KA2-TAP", "D1", 2, "Timor-Alor-Pantar lects form one clade", TAP, "different family from the rest"),
        ("KA2-floreslembata", "D1", 2, "Flores-Lembata", FLORES_LEMBATA, "Glottolog 5.3: Flores-Lembata"),
        ("KA1-tetun", "D2", 1, "Tetun varieties", a("tetum", "tetun_terik", "tetun_fehan"), "Glottolog 5.3: Tetunic"),
        ("KA1-iliuun", "D2", 1, "Ili'uun", a("iliun", "iliun_erai"), "Glottolog 5.3: iliu1237"),
        ("KA1-luang", "D2", 1, "Luang + Wetan", a("luang", "wetan"), "Glottolog 5.3: luan1263"),
        ("KA2-rotemeto", "D2", 2, "Rote-Meto", a("atoni", "termanu"), "Glottolog 5.3: Rote-Meto"),
        ("KA2-floreslembata", "D2", 2, "Flores-Lembata", a("lamaholot", "kedang", "lamalera"),
         "Glottolog 5.3: Flores-Lembata"),
        ("KA2-perai-aputai", "D2", 2, "Perai-Aputai", a("perai", "aputai"), "Glottolog 5.3: Perai-Aputai"),
    ]
    write("known_answers.csv", ["ID", "Dataset", "Tier", "Name", "Members", "Basis"],
          [(i, d, t, n, " ".join(m), b) for i, d, t, n, m, b in ka])

    # Hypothesis clades (tested only after the gate, steps 5-8). Prune = lects whose position the hypothesis
    # does not fix; they are removed before checking that clade.
    hull_prune = WELAUN + HELONG + ROTE + DADUA + BABAR
    hyp = [
        ("HULL-R", "Hull 1998, 2001", "Ramelaic (Timoric B)", MAMBAE + KEMAK + TOKODEDE + IDATE + LAKALEI, hull_prune,
         "C1"),
        ("HULL-F", "Hull 2001; van Engelenhoven 2009", "Fabronic / Extra-Ramelaic (Timoric A)",
         TETUN + HABU + KAWAIMINA + GALOLI + WETAR + METO + SWM_LK, hull_prune, "C1"),
        ("HULL98-W", "Hull 1998 (withdrawn 2003)", "Welaun inside Tetun", TETUN + WELAUN, [], "C2"),
        ("EDW-CT", "Edwards 2021; Glottolog 5.3", "Central Timor", CENTRAL_TIMOR, [], "C1 C2"),
        ("EDW-TB", "Edwards 2021; Glottolog 5.3", "Timor-Babar",
         IDATE + LAKALEI + TETUN + HABU + KAWAIMINA + GALOLI + DADUA + WETAR + HELONG + METO + ROTE + SWM_LK + BABAR,
         [], "C1"),
        ("EDW-LI", "Edwards 2021; Glottolog 5.3", "Lakalei-Idate", IDATE + LAKALEI, [], "C1"),
        ("EDW-ET", "Glottolog 5.3", "Eastern Timor", TETUN + HABU + KAWAIMINA, [], ""),
        ("EDW-CTA", "Glottolog 5.3", "Central Timoric A", TETUN + HABU, [], ""),
        ("EDW-KW", "Hull 2001; Edwards 2021; Glottolog 5.3", "Kawaimina", KAWAIMINA, [], ""),
        ("EDW-WA", "Edwards 2021; Glottolog 5.3", "Wetar-Atauro", GALOLI + DADUA + WETAR, [], ""),
        ("EDW-SWM", "Glottolog 5.3", "Southwest Maluku", SWM_LK + BABAR, [], ""),
    ]
    write("hypotheses.csv", ["ID", "Source", "Name", "Members", "Prune", "Contrast"],
          [(i, s, n, " ".join(m), " ".join(p), c) for i, s, n, m, p, c in hyp])

    lect_map = [(A["tetum"], "tetu1246"), (A["tetun_terik"], "tetu1245-suai"), (A["mambai"], "mamb1306"),
                (A["kemak"], "kema1243"), (A["tokodede"], "tuku1254"), (A["galolen"], "galo1243"),
                (A["waimaa"], "waim1252"), (A["naueti"], "naue1237"), (A["dadua"], "dadu1237"),
                (A["atoni"], "kusa1252"), (A["termanu"], "term1237"), (A["kisar"], "kisa1266"),
                (A["roma"], "roma1332"), (A["luang"], "luan1264"), (A["wetan"], "weta1243"),
                (A["iliun"], "ilma1240"), (A["iliun_erai"], "eray1237"), (A["tugun"], "kaha1239"),
                (A["perai"], "uhak1237"), (A["aputai"], "ilpu1239"), (A["dawera"], "dawe1237"),
                (A["dai"], "daii1240"), (A["north_babar"], "nort2860"), (A["se_babar"], "sout2883"),
                (A["serili"], "seri1255"), (A["east_masela"], "east2462"), (A["central_masela"], "cent2072"),
                (A["emplawas"], "empl1237"), (A["tela_masbuar"], "tela1241"), (A["imroing"], "imro1237"),
                (A["lamaholot"], "lama1277-lewoi"), (A["kedang"], "keda1252")]
    write("lect_map.csv", ["ABVD_ID", "LexiRumah_ID"], lect_map)
    print("reference tables written:", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
