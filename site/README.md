# INSTANTAUTO — Application de gestion d'atelier

Fichier unique `INSTANTAUTO.html` (aucune dépendance, aucun serveur) : ouvre-le
par double-clic dans un navigateur. Thème **noir / rouge / blanc**.

## Ce que fait l'app
- **Tableau de bord** : seuil de rentabilité du jour, CA, main-d'œuvre, bénéfice, à encaisser.
- **Factures** : numérotation continue, lignes main-d'œuvre / pièces, impression / PDF.
- **Clients & véhicules**, **Pièces** (avec marge de revente), **Consommables**.
- **Réglages** : taux horaires, charges, objectif.

## Enregistrement automatique
Toutes tes données sont **enregistrées automatiquement dans le navigateur** à
chaque modification (rien à cliquer).

En plus, tu peux activer la **Sauvegarde auto sur fichier** (bouton en bas de la
colonne de gauche) :
1. Tu choisis **une seule fois** un fichier `.json` (par ex. dans un dossier
   OneDrive / Google Drive / Dropbox pour un double dans le cloud).
2. Ensuite, **chaque modification est réécrite en direct** dans ce fichier.
3. Après un rechargement de la page, un clic sur **« Reconnecter la sauvegarde »**
   réautorise l'écriture (sécurité du navigateur).

> Disponible sur **Chrome** et **Edge** (API File System Access). Sur les autres
> navigateurs, utilise **« Export manuel »** régulièrement — le fichier obtenu se
> ré-importe avec **« Importer »**.

## Palette
Identité **rouge** (`#e21414`) sur fond **noir**, texte **blanc**. Le **vert** est
conservé uniquement pour les signaux financiers positifs (facture payée, objectif
atteint) et le rouge clair pour les alertes / retards.
