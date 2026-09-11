# INSTANTAUTO — Application de gestion d'atelier

Fichier unique `INSTANTAUTO.html` (aucune dépendance, aucun build) : ouvre-le
par double-clic dans un navigateur. Thème **noir / rouge / blanc**.

## Ce que fait l'app
- **Tableau de bord** : seuil de rentabilité du jour, CA, main-d'œuvre, bénéfice,
  à encaisser, et **graphique du bénéfice net par mois** (X dès 07/2026, Y dès 500 €).
- **Factures** : numérotation continue, lignes main-d'œuvre / pièces, impression / PDF.
- **Clients & véhicules**, **Pièces** (avec marge de revente), **Consommables**.
- **Réglages** : taux horaires, charges, objectif.

## Enregistrement automatique (3 niveaux)
1. **Navigateur (toujours actif)** — chaque modification est enregistrée localement.
2. **Fichier de secours** — bouton « Sauvegarde auto » : tu choisis un `.json` une
   fois, chaque changement y est réécrit en direct (Chrome/Edge). « Export manuel »
   sinon.
3. **Cloud Firebase (recommandé)** — synchro **permanente** dans Firestore, avec
   connexion par email + mot de passe. Accessible depuis n'importe quel appareil.

---

## Mettre la base dans le cloud avec Firebase

### A. Créer le projet et la base
1. Va sur <https://console.firebase.google.com> → **Ajouter un projet** (nomme-le
   par ex. `mon-garage`).
2. Dans le projet : icône **</>** (« Ajouter une app Web »), donne un surnom,
   valide. Firebase affiche un objet **`firebaseConfig`** — garde-le sous la main.
3. Menu **Build → Authentication → Get started → Sign-in method** : active
   **E-mail/Mot de passe**.
4. Menu **Build → Firestore Database → Create database** → mode **production** →
   choisis une région (europe-west par ex.).

### B. Coller les règles de sécurité Firestore
Onglet **Firestore → Rules**, remplace tout par ceci, puis **Publish** :

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /app_state/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

> Chaque utilisateur ne peut lire/écrire que **sa propre** ligne (`app_state/<son uid>`).

### C. Brancher l'app
Ouvre `INSTANTAUTO.html`, trouve le bloc **`FIREBASE_CONFIG`** en haut du `<script>`
et recopie les valeurs de ton `firebaseConfig` :

```js
const FIREBASE_CONFIG = {
  apiKey: "AIza…",
  authDomain: "mon-garage.firebaseapp.com",
  projectId: "mon-garage",
  storageBucket: "mon-garage.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abcdef…"
};
```

Enregistre, rouvre le fichier : un écran de connexion apparaît. Clique
**« Créer un compte »** (email + mot de passe) la première fois, puis
**« Se connecter »**. À partir de là, tout est synchronisé dans le cloud à
chaque modification (voir l'indicateur **« Cloud : synchronisé ✓ »** en bas à gauche).

> ⚠️ Sécurité : même si le fichier `INSTANTAUTO.html` est partagé, personne ne peut
> voir ni modifier tes données sans ton mot de passe. La clé `apiKey` Firebase n'est
> pas un secret — la protection vient des règles Firestore + de l'authentification.

---

## Mettre l'app en ligne avec Firebase Hosting
Pour y accéder depuis ton téléphone / plusieurs appareils via une adresse `https://`.

1. Installe Node.js, puis dans un terminal :
   ```bash
   npm install -g firebase-tools
   firebase login
   ```
2. Crée un dossier, mets-y `INSTANTAUTO.html` **renommé `index.html`**, puis :
   ```bash
   firebase init hosting
   ```
   - « Use an existing project » → choisis `mon-garage`
   - Dossier public : `.` (le dossier courant)
   - Configurer en single-page app : **No**
   - Ne pas écraser `index.html` : **No**
3. Déploie :
   ```bash
   firebase deploy
   ```
   Firebase te donne une URL du type `https://mon-garage.web.app` — ouvre-la sur
   ton téléphone, connecte-toi, tu retrouves tes données.
4. **Ajoute le domaine autorisé** : Authentication → Settings → **Authorized
   domains** → ajoute `mon-garage.web.app` (déjà présent en général).

> Pour republier après une modif : refais simplement `firebase deploy`.

---

## Palette
Identité **rouge** (`#e21414`) sur fond **noir**, texte **blanc**. Le **vert** est
conservé uniquement pour les signaux financiers positifs (facture payée, objectif
atteint) et le rouge clair pour les alertes / retards.
