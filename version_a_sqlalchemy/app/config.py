"""Configuration centrale de l'application (Version A)."""
from datetime import timedelta

# --- Sécurité / JWT ---
SECRET_KEY = "version-a-secret-change-en-prod-1a2b3c4d5e6f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)

# --- Base de données ---
DATABASE_URL = "sqlite:///./mediatheque.db"

# --- Compte créé au démarrage ---
DEFAULT_USER = "bibliothecaire"
DEFAULT_PASSWORD = "mediatheque2026"

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
