"""Utilitaires d'export partagés pour les modèles CadQuery.

Chaque modèle dans models/ importe `save()` pour exporter en STL (impression)
et STEP (ré-édition CAO) dans le dossier output/ avec une tolérance adaptée
à l'impression 3D.
"""
from pathlib import Path

import cadquery as cq

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def save(model: cq.Workplane, name: str, tolerance: float = 0.05) -> None:
    """Exporte un modèle en STL + STEP dans output/.

    - STL : maillage prêt à slicer (Cura, PrusaSlicer, Bambu Studio...).
      `tolerance` = écart max corde/surface en mm ; 0.05 donne des courbes lisses.
    - STEP : géométrie exacte, utile pour ré-éditer ou modifier les cotes.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    stl_path = OUTPUT_DIR / f"{name}.stl"
    step_path = OUTPUT_DIR / f"{name}.step"
    cq.exporters.export(model, str(stl_path), tolerance=tolerance)
    cq.exporters.export(model, str(step_path))
    print(f"OK  {stl_path}  ({stl_path.stat().st_size} octets)")
    print(f"OK  {step_path}  ({step_path.stat().st_size} octets)")
