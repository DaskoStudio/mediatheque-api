"""Configuration centrale de l'application (Version A)."""
import os
from datetime import timedelta

# --- Sécurité / JWT (fournis via variables d'environnement, voir .env.example) ---
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN", "30")))

# --- Base de données ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mediatheque.db")

# --- Compte créé au démarrage ---
DEFAULT_USER = os.getenv("DEFAULT_USER", "bibliothecaire")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "change-me")

# --- Liste fixe des genres autorisés ---
GENRES = (
    "Rock",
    "Pop",
    "Jazz",
    "Hip-Hop",
    "Classique",
    "Electro",
    "Metal",
    "Reggae",
    "Blues",
    "RnB",
)
