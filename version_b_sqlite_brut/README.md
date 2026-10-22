# Album Library — Version B (raw sqlite3 + itsdangerous)

REST API for a music-album library, built with FastAPI. This version uses **no ORM**: it talks to the database through native **`sqlite3`**, hashes passwords with **PBKDF2 (hashlib)** and authenticates with a **time-limited signed token** (itsdangerous) sent as an **HTTP Bearer** header.

## Run the API

```bash
pip install -r requirements.txt
uvicorn main:app --reload     # or: python main.py
```

Interactive docs (Swagger): <http://127.0.0.1:8000/docs>

## Configuration

Copy `.env.example` to `.env` and set your own values.

| Variable | Purpose | Default |
|---|---|---|
| `CLE_SIGNATURE` | Token signing key | `dev-only-change-me` (development only) |
| `DUREE_JETON` | Token lifetime in seconds | `1800` |
| `BASE_FICHIER` | SQLite file name | `mediatheque_b.db` |
| `COMPTE_DEFAUT` | Account created at start-up | `admin` |
| `MDP_DEFAUT` | Password of that account | `change-me` |

Passwords are never stored in clear text: PBKDF2-SHA256, 200,000 iterations, random salt per user. Always set your own key and password outside local development.

## Authenticate (Swagger demo)

1. Call `POST /connexion` with JSON `{ "nom": "...", "mot_de_passe": "..." }`. It returns a `jeton` field.
2. Click **Authorize** at the top of Swagger and paste the token (Bearer scheme).
3. Write routes are now available. The token expires after 30 minutes (checked with itsdangerous `max_age`).

## Routes

| Method | Path | Access | Description |
|---|---|---|---|
| GET | `/albums` | public | List all albums |
| GET | `/albums/{id}` | public | Read one album (`404` if missing) |
| POST | `/albums` | authenticated | Create an album (`201`) |
| PUT | `/albums/{id}` | authenticated | Update an album |
| DELETE | `/albums/{id}` | authenticated | Delete an album (`204`) |
| POST | `/connexion` | public | Log in and get a token |

## Album model

```json
{
  "titre": "Discovery",
  "artiste": "Daft Punk",
  "genre": "Electro",
  "annee": 2001,
  "note": 9.0
}
```

Allowed genres: Rock, Pop, Jazz, Rap, Classique, Electro, Metal, Funk, Soul, Variété.

## Validation

- Empty or whitespace-only title or artist → `422`.
- Rating outside 0–10 → `422`.
- Year outside 1900–2026 → `422`.
- Genre outside the fixed list → `422`.
- Internal field `date_ajout`: filled in by the API at creation, stored in the database but **never returned** (absent from the `AlbumSortie` model).

> Without a token, write routes are refused with `401` or `403` depending on the Bearer guard — in both cases access is denied.

## Persistence

Albums are stored in the SQLite file `mediatheque_b.db` and survive restarts.

## Code layout

```text
main.py        Entry point, router mounting, start-up initialisation
settings.py    Settings read from environment variables
database.py    Raw sqlite3 access (table creation, CRUD queries)
models.py      Pydantic models (input validation / output shape)
security.py    PBKDF2 hashing and itsdangerous signed tokens
auth.py        /connexion route and HTTP Bearer guard
albums.py      Album CRUD routes
test_api.py    Creation test and rejection-without-token test
```

## Status

All the requirements are covered: multi-file layout, one-command start, validation, hidden internal field, persistent storage with native sqlite3 (no ORM), full CRUD with proper status codes, hashed password with expiring token, public reads and protected writes, two passing tests (`pytest`).

Possible improvements: multiple user accounts, search index, pagination.
