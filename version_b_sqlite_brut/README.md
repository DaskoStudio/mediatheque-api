# Médiathèque d'albums — Version B (sqlite3 brut + itsdangerous)

API REST d'une médiathèque d'albums de musique (FastAPI).
Cette version n'utilise **aucun ORM** : accès à la base en **sqlite3 natif**, mots de
passe hachés avec **PBKDF2/hashlib**, et authentification par **jeton signé à durée
limitée** (itsdangerous) transmis en **HTTP Bearer**.

## Lancer l'API (une seule commande)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

(ou `python main.py`)

Documentation interactive Swagger : http://127.0.0.1:8000/docs

## Lancer les tests

```bash
pytest
```

## Identifiants du compte (créé automatiquement au démarrage)

| Champ         | Valeur       |
|---------------|--------------|
| Nom           | `admin`      |
| Mot de passe  | `albums2026` |

Le mot de passe n'est **jamais** stocké en clair (PBKDF2-SHA256, 200 000 itérations,
sel aléatoire par utilisateur).

## Comment se connecter (démo Swagger)

1. Route `POST /connexion` — envoyer un JSON `{ "nom": "...", "mot_de_passe": "..." }`.
   → renvoie un champ `jeton`.
2. Cliquer sur **Authorize** en haut de Swagger et coller le jeton (schéma Bearer).
3. Les routes d'écriture deviennent accessibles.

Le jeton **expire au bout de 30 minutes** (vérifié via `max_age` d'itsdangerous).

## Routes

| Méthode | Chemin           | Accès          | Description                     |
|---------|------------------|----------------|---------------------------------|
| GET     | `/albums`        | public         | Lister tous les albums          |
| GET     | `/albums/{id}`   | public         | Lire un album (404 si absent)   |
| POST    | `/albums`        | connecté       | Créer un album (**201**)        |
| PUT     | `/albums/{id}`   | connecté       | Modifier un album               |
| DELETE  | `/albums/{id}`   | connecté       | Supprimer un album (204)        |
| POST    | `/connexion`     | public         | Se connecter, obtenir un jeton  |

## Modèle d'un album

```json
{
  "titre": "Discovery",
  "artiste": "Daft Punk",
  "genre": "Electro",
  "annee": 2001,
  "note": 9.0
}
```

Genres autorisés : Rock, Pop, Jazz, Rap, Classique, Electro, Metal, Funk, Soul, Variété.

## Validation des données

- Titre / artiste vides (ou uniquement des espaces) → refusés (422).
- Note hors de l'intervalle 0–10 → refusée (422).
- Année hors de 1900–2026 → refusée (422).
- Genre hors de la liste fixe → refusé (422).
- **Champ interne `date_ajout`** : rempli par l'API à la création, stocké en base
  mais **jamais renvoyé** dans une réponse (absent du modèle `AlbumSortie`).

> Note : sans jeton, l'écriture renvoie **403** (garde HTTP Bearer). C'est bien un
> refus d'accès, comme demandé.

## Persistance

Les albums sont stockés dans le fichier SQLite `mediatheque_b.db`.
Après un arrêt/relance de l'API, les données sont toujours là.

## Organisation du code

```
main.py        Point d'entrée, montage des routeurs, init au démarrage
settings.py    Constantes (clé, durée jeton, genres, identifiants)
database.py    Accès sqlite3 brut (création tables, requêtes CRUD)
models.py      Modèles Pydantic (validation entrée / forme sortie)
security.py    Hachage PBKDF2 + jetons signés itsdangerous
auth.py        Route /connexion + garde HTTP Bearer
albums.py      Routes CRUD des albums
test_api.py    Test création + test refus sans connexion
```

## Ce qui fonctionne

- ✅ Organisation multi-fichiers, lancement en une commande
- ✅ Validation (titre vide, note 0–10, année, genre en liste fixe)
- ✅ Champ interne non exposé
- ✅ Stockage SQLite persistant (sqlite3 natif, pas d'ORM)
- ✅ CRUD complet avec bons codes (201 / 404 / 204)
- ✅ Compte au démarrage, mot de passe haché, jeton expirant
- ✅ Lecture publique / écriture protégée
- ✅ Deux tests (création + refus sans jeton) — `pytest` : 2 passés

## Ce qui n'est pas terminé

Rien de bloquant : tous les points du sujet sont couverts. Améliorations possibles
non demandées : plusieurs comptes utilisateurs, index de recherche, pagination.
