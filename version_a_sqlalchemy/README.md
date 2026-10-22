# Médiathèque d'albums — Version A (SQLAlchemy + JWT)

API REST d'une médiathèque d'albums de musique (FastAPI).
Cette version utilise l'**ORM SQLAlchemy**, la validation **Pydantic v2**, et une
authentification par **jeton JWT** (python-jose) avec mots de passe hachés en **bcrypt**.

## Lancer l'API (une seule commande)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

(ou `python -m app.main`)

Documentation interactive Swagger : http://127.0.0.1:8000/docs

## Lancer les tests

```bash
pytest
```

## Identifiants du compte (créé automatiquement au démarrage)

| Champ         | Valeur            |
|---------------|-------------------|
| Nom d'utilisateur | `bibliothecaire` |
| Mot de passe  | `mediatheque2026` |

Le mot de passe n'est **jamais** stocké en clair (hash bcrypt en base).

## Comment se connecter (démo Swagger)

1. Route `POST /login` — envoyer `username` + `password` (formulaire OAuth2).
   → renvoie un `access_token`.
2. Cliquer sur **Authorize** en haut de Swagger et coller le jeton.
3. Les routes d'écriture sont alors accessibles.

Le jeton **expire au bout de 30 minutes**.

## Routes

| Méthode | Chemin           | Accès          | Description                     |
|---------|------------------|----------------|---------------------------------|
| GET     | `/albums`        | public         | Lister tous les albums          |
| GET     | `/albums/{id}`   | public         | Lire un album (404 si absent)   |
| POST    | `/albums`        | connecté       | Créer un album (**201**)        |
| PUT     | `/albums/{id}`   | connecté       | Modifier un album               |
| DELETE  | `/albums/{id}`   | connecté       | Supprimer un album (204)        |
| POST    | `/login`         | public         | Se connecter, obtenir un jeton  |

## Modèle d'un album

```json
{
  "titre": "Random Access Memories",
  "artiste": "Daft Punk",
  "genre": "Electro",
  "annee": 2013,
  "note": 9.5
}
```

Genres autorisés : Rock, Pop, Jazz, Hip-Hop, Classique, Electro, Metal, Reggae, Blues, RnB.

## Validation des données

- Titre / artiste vides (ou uniquement des espaces) → refusés (422).
- Note hors de l'intervalle 0–10 → refusée (422).
- Année absurde (avant 1900 ou dans le futur) → refusée (422).
- Genre hors de la liste fixe → refusé (422).
- **Champ interne `ajoute_par`** : rempli par l'API (login du créateur), stocké en
  base mais **jamais renvoyé** dans une réponse (absent du schéma `AlbumOut`).

## Persistance

Les albums sont stockés dans le fichier SQLite `mediatheque.db`.
Après un arrêt/relance de l'API, les données sont toujours là.

## Organisation du code

```
app/
├── main.py       Point d'entrée, création de l'app + compte par défaut
├── config.py     Constantes (secret, durée jeton, genres, identifiants)
├── database.py   Connexion + session SQLAlchemy
├── models.py     Modèles ORM (tables Utilisateur, Album)
├── schemas.py    Schémas Pydantic (entrée / sortie / token)
├── security.py   Hachage bcrypt + création/lecture des JWT
├── auth.py       Route /login + dépendance "utilisateur connecté"
└── routes.py     Routes CRUD des albums
tests/
└── test_api.py   Test création + test refus sans connexion
```

## Ce qui fonctionne

- ✅ Organisation multi-fichiers, lancement en une commande
- ✅ Validation (titre vide, note 0–10, année, genre en liste fixe)
- ✅ Champ interne non exposé
- ✅ Stockage SQLite persistant
- ✅ CRUD complet avec bons codes (201 / 404 / 204)
- ✅ Compte au démarrage, mot de passe haché, jeton JWT expirant
- ✅ Lecture publique / écriture protégée
- ✅ Deux tests (création + refus sans jeton) — `pytest` : 2 passés

## Ce qui n'est pas terminé

Rien de bloquant : tous les points du sujet sont couverts. Améliorations possibles
non demandées : rafraîchissement de jeton, pagination de la liste, plusieurs comptes.
