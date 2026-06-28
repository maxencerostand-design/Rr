"""Raccord Y 2-en-1 réducteur pour circuit de refroidissement automobile.

- Deux entrees cannelees pour durite souple Ø int. 10 mm (a +-30 deg de l'axe)
- Une sortie cannelee pour durite souple Ø int. 8 mm (axe central)
- Embouts males canneles type "sapin" : epaulement raide cote corps (anti-arrachage),
  rampe douce cote pointe (enfilage facile). A maintenir avec un collier.

A IMPRIMER en PETG / ABS-ASA / Nylon (PAS en PLA : ramollit a ~55 C).
Conseil d'impression : parois pleines / 100% remplissage pour l'etancheite,
buse 0.4, couches 0.16, sans support (le Y est auto-portant a +-30 deg).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cadquery as cq

from lib.export import save

# ---------------------------------------------------------------------------
# Parametres (mm)
# ---------------------------------------------------------------------------
FORME = "T"         # "Y" (deux entrees a +-DEMI_ANGLE) ou "T" (run droit + branche a 90 deg)
DEMI_ANGLE = 30.0   # (forme Y) angle de chaque entree par rapport a l'axe de sortie
RAYON_HUB = 6.0     # rayon de la sphere centrale qui fusionne les 3 conduits

# Embout pour durite Ø int. 10 mm (les deux entrees)
PORT_10 = dict(
    r_root=4.6,     # rayon en creux de barbe  (Ø9.2)
    r_crest=5.4,    # rayon en crete de barbe  (Ø10.8, serre la durite de 10)
    r_tip=4.0,      # rayon de l'amorce en pointe
    bore_r=3.0,     # rayon du canal interne   (Ø6)
    neck=5.0,       # longueur de col lisse pres du hub
    n_barbs=3,
    barb_len=4.0,
    tip_len=2.0,
)

# Embout pour durite Ø int. 8 mm (la sortie)
PORT_8 = dict(
    r_root=3.6,     # (Ø7.2)
    r_crest=4.4,    # (Ø8.8, serre la durite de 8)
    r_tip=3.0,
    bore_r=2.2,     # (Ø4.4)
    neck=5.0,
    n_barbs=3,
    barb_len=4.0,
    tip_len=2.0,
)


def nipple_profile(p: dict):
    """Points (r, z) du profil de revolution, base en z=0, pointe en z=H."""
    pts = [(0.0, 0.0), (p["r_root"], 0.0)]
    z = p["neck"]
    pts.append((p["r_root"], z))            # haut du col lisse
    for _ in range(p["n_barbs"]):
        pts.append((p["r_crest"], z))       # marche raide -> crete (cote corps)
        z += p["barb_len"]
        pts.append((p["r_root"], z))        # rampe douce -> creux (cote pointe)
    z += p["tip_len"]
    pts.append((p["r_tip"], z))             # amorce conique en pointe
    pts.append((0.0, z))                    # retour sur l'axe
    H = z
    return pts, H


def make_nipple(p: dict):
    pts, H = nipple_profile(p)
    solid = (
        cq.Workplane("XZ")
        .polyline(pts)
        .close()
        .revolve(360, (0, 0, 0), (0, 1, 0))
    )
    return solid, H


def make_bore(p: dict, H: float):
    """Canal cylindrique le long de +Z, de z=-4 (chevauche le hub) a z=H+1."""
    return (
        cq.Workplane("XY")
        .workplane(offset=-4.0)
        .circle(p["bore_r"])
        .extrude(H + 5.0)
    )


def oriented(solid, kind: str):
    """Place un solide construit le long de +Z (base a l'origine) sur son axe final.

    'out' : sortie Ø8, pointe vers -Z
    'inA' / 'inB' : les deux entrees Ø10, selon FORME.
      - Y : inA a +DEMI_ANGLE, inB a -DEMI_ANGLE (deux bras en biais)
      - T : inA dans l'axe (+Z, run droit avec la sortie), inB a 90 deg (+X)
    """
    if kind == "out":
        return solid.rotate((0, 0, 0), (1, 0, 0), 180)
    if FORME == "Y":
        if kind == "inA":
            return solid.rotate((0, 0, 0), (0, 1, 0), DEMI_ANGLE)
        if kind == "inB":
            return solid.rotate((0, 0, 0), (0, 1, 0), -DEMI_ANGLE)
    elif FORME == "T":
        if kind == "inA":
            return solid                                    # run droit, +Z
        if kind == "inB":
            return solid.rotate((0, 0, 0), (0, 1, 0), 90)   # branche laterale, +X
    raise ValueError(f"{FORME}/{kind}")


def build():
    n10, H10 = make_nipple(PORT_10)
    n8, H8 = make_nipple(PORT_8)
    b10 = make_bore(PORT_10, H10)
    b8 = make_bore(PORT_8, H8)

    # Corps : hub + 3 embouts
    body = cq.Workplane().sphere(RAYON_HUB)
    body = body.union(oriented(n8, "out"))
    body = body.union(oriented(n10, "inA"))
    body = body.union(oriented(n10, "inB"))

    # Cavite : 3 canaux qui se rejoignent au centre
    bores = oriented(b8, "out")
    bores = bores.union(oriented(b10, "inA"))
    bores = bores.union(oriented(b10, "inB"))

    return body.cut(bores)


if __name__ == "__main__":
    model = build()
    bb = model.val().BoundingBox()
    print(f"Forme {FORME} - Encombrement (mm): X {bb.xlen:.1f}  Y {bb.ylen:.1f}  Z {bb.zlen:.1f}")
    save(model, f"raccord_{FORME}_refroidissement")
