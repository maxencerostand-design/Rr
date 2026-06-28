# Rr — Objets imprimables en 3D, générés par code

Décris un objet → je le génère en **CadQuery** (CAO paramétrique Python) →
tu récupères un fichier **STL** prêt à imprimer (et un **STEP** ré-éditable).

## Comment ça marche

1. Tu me dictes l'objet (forme, dimensions, usage, contraintes).
2. J'écris un script dans `models/`, je l'exécute, ça produit les fichiers dans `output/`.
3. Tu télécharges le `.stl`, tu le slices (Cura, PrusaSlicer, Bambu Studio…), tu imprimes.

Comme tout est **paramétrique** : tu dis « 1 cm plus large » → je change une
constante et je régénère, sans tout refaire.

## Structure

```
models/   un script .py par objet (paramètres en haut, fonction build())
lib/      utilitaires partagés (export STL + STEP)
output/   fichiers générés (.stl / .step)  — non versionnés
```

## Installation

```bash
pip install -r requirements.txt
```

## Générer un objet

```bash
python models/exemple_porte_cles.py
# -> output/exemple_porte_cles.stl + .step
```

## Note sur les connecteurs MCP

Des serveurs MCP existent pour piloter **Blender** ou **FreeCAD** en direct,
mais ils tournent sur ta machine locale, pas dans l'environnement cloud de
cette session. Ici, la génération par code est autonome et donne directement
des fichiers imprimables — c'est l'approche utilisée dans ce dépôt.
