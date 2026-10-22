"""Hachage de mot de passe (PBKDF2/hashlib) et jetons signés (itsdangerous)."""
import hashlib
import os

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

import settings

_serializer = URLSafeTimedSerializer(settings.CLE_SIGNATURE, salt="auth")

_ITERATIONS = 200_000


def hacher(mot_de_passe: str) -> str:
    """Renvoie 'sel$hash' — le mot de passe n'est jamais stocké en clair."""
    sel = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode(), sel, _ITERATIONS)
    return f"{sel.hex()}${dk.hex()}"


def verifier(mot_de_passe: str, stocke: str) -> bool:
    try:
        sel_hex, hash_hex = stocke.split("$")
    except ValueError:
        return False
    dk = hashlib.pbkdf2_hmac(
        "sha256", mot_de_passe.encode(), bytes.fromhex(sel_hex), _ITERATIONS
    )
    return dk.hex() == hash_hex


def generer_jeton(nom_utilisateur: str) -> str:
    return _serializer.dumps({"nom": nom_utilisateur})


def valider_jeton(jeton: str) -> str | None:
    """Renvoie le nom d'utilisateur si le jeton est valide et non expiré."""
    try:
        data = _serializer.loads(jeton, max_age=settings.DUREE_JETON)
        return data.get("nom")
    except (BadSignature, SignatureExpired):
        return None
