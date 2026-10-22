# Album Library — Version A (SQLAlchemy + JWT)

REST API for a music-album library, built with FastAPI. This version uses the **SQLAlchemy ORM**, **Pydantic v2** validation and **JWT** authentication (python-jose) with **bcrypt**-hashed passwords.

## Run the API

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload     # or: python -m app.main
```

Interactive docs (Swagger): <http://127.0.0.1:8000/docs>

## Configuration

Copy `.env.example` to `.env` and set your own values.

| Variable | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing key | `dev-only-change-me` (development only) |
| `ACCESS_TOKEN_EXPIRE_MIN` | Token lifetime in minutes | `30` |
| `DATABASE_URL` | Database URL | `sqlite:///./mediatheque.db` |
| `DEFAULT_USER` | Account created at start-up | `bibliothecaire` |
| `DEFAULT_PASSWORD` | Password of that account | `change-me` |

The password is never stored in clear text (bcrypt hash in the database). Always set your own `SECRET_KEY` and `DEFAULT_PASSWORD` outside local development.

## Authenticate (Swagger demo)

1. Call `POST /login` with `username` and `password` (OAuth2 form). It returns an `access_token`.
2. Click **Authorize** at the top of Swagger and paste the token.
3. Write routes are now available. The token expires after 30 minutes.

## Routes

| Method | Path | Access | Description |
|---|---|---|---|
| GET | `/albums` | public | List all albums |
| GET | `/albums/{id}` | public | Read one album (`404` if missing) |
| POST | `/albums` | authenticated | Create an album (`201`) |
| PUT | `/albums/{id}` | authenticated | Update an album |
| DELETE | `/albums/{id}` | authenticated | Delete an album (`204`) |
| POST | `/login` | public | Log in and get a token |

## Album model

```json
{
  "titre": "Random Access Memories",
  "artiste": "Daft Punk",
  "genre": "Electro",
  "annee": 2013,
  "note": 9.5
}
```

Allowed genres: Rock, Pop, Jazz, Hip-Hop, Classique, Electro, Metal, Reggae, Blues, RnB.

## Validation

- Empty or whitespace-only title or artist → `422`.
- Rating outside 0–10 → `422`.
- Year before 1900 or too far in the future → `422`.
- Genre outside the fixed list → `422`.
- Internal field `ajoute_par`: filled in by the API (login of the creator), stored in the database but **never returned** (absent from the `AlbumOut` schema).

## Persistence

Albums are stored in the SQLite file `mediatheque.db` and survive restarts.

## Code layout

```text
app/
├── main.py       Entry point, app creation, default account
├── config.py     Settings read from environment variables
├── database.py   SQLAlchemy engine and session
├── models.py     ORM models (User, Album)
├── schemas.py    Pydantic schemas (input / output / token)
├── security.py   bcrypt hashing and JWT creation / decoding
├── auth.py       /login route and "current user" dependency
└── routes.py     Album CRUD routes
tests/
└── test_api.py   Creation test and rejection-without-token test
```

## Status

All the requirements are covered: multi-file layout, one-command start, validation, hidden internal field, persistent storage, full CRUD with proper status codes, hashed password with expiring JWT, public reads and protected writes, two passing tests (`pytest`).

Possible improvements: token refresh, pagination, multiple accounts.
