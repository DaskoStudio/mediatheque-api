"""Réglages de la Version B."""
import os

BASE_FICHIER = os.getenv("BASE_FICHIER", "mediatheque_b.db")

# Clé de signature des jetons + durée de validité (en secondes).
# Fournies via variables d'environnement (voir .env.example).
CLE_SIGNATURE = os.getenv("CLE_SIGNATURE", "dev-only-change-me")
DUREE_JETON = int(os.getenv("DUREE_JETON", str(30 * 60)))  # 30 minutes

# Compte présent dès le premier démarrage.
COMPTE_DEFAUT = os.getenv("COMPTE_DEFAUT", "admin")
MDP_DEFAUT = os.getenv("MDP_DEFAUT", "change-me")

# Liste fixe des genres acceptés.
GENRES_AUTORISES = [
    "Rock",
    "Pop",
    "Jazz",
    "Rap",
    "Classique",
    "Electro",
    "Metal",
    "Funk",
    "Soul",
    "Variété",
]

ANNEE_MIN = 1900
ANNEE_MAX = 2026
