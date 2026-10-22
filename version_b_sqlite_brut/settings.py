"""Réglages de la Version B."""

BASE_FICHIER = "mediatheque_b.db"

# Clé de signature des jetons + durée de validité (en secondes).
CLE_SIGNATURE = "version-b-cle-signature-9z8y7x6w5v"
DUREE_JETON = 30 * 60  # 30 minutes

# Compte présent dès le premier démarrage.
COMPTE_DEFAUT = "admin"
MDP_DEFAUT = "albums2026"

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
