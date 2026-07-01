# Site INSTANTAUTO

Site vitrine (1 seul fichier `index.html`, aucune dépendance) pour le garage,
thème **noir / rouge / blanc**, avec **enregistrement automatique** des demandes de rendez-vous.

## Ouvrir le site
Double-clique sur `index.html` — il s'ouvre dans n'importe quel navigateur.
Pour le mettre en ligne gratuitement : dépose le fichier sur **Netlify Drop**,
**GitHub Pages** ou **Vercel**.

## L'enregistrement automatique des demandes
Chaque formulaire envoyé est **enregistré automatiquement**, de deux façons :

1. **En local (toujours actif, sans rien configurer)**
   La demande est stockée dans le navigateur. Pour voir toutes les demandes :
   ouvre le site et ajoute `#admin` à l'adresse
   (ex. `.../index.html#admin`) ou clique sur **« Accès gérant »** en bas de page.
   Tu peux alors :
   - consulter le tableau des demandes,
   - **Exporter en CSV** (s'ouvre dans Excel),
   - imprimer, ou tout effacer.

2. **Par email (recommandé, pour être prévenu à chaque demande)**
   - Crée un compte gratuit sur <https://formspree.io>
   - Copie l'URL de ton formulaire (ex. `https://formspree.io/f/abcdxyz`)
   - Ouvre `index.html`, cherche le bloc `CONFIG` dans le `<script>`, et colle-la :
     ```js
     FORMSPREE_ENDPOINT: "https://formspree.io/f/abcdxyz",
     ```
   Chaque demande t'arrivera alors par email **en plus** de l'enregistrement local.

## Personnaliser
Dans `index.html`, remplace :
- le numéro de téléphone `01 23 45 67 89`,
- l'email `contact@instantauto.fr`,
- l'adresse `12 rue de l'Atelier, 00000 Ville`,
- les tarifs des services.
