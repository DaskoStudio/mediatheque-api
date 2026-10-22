"""Hachage des mots de passe (bcrypt) et jetons JWT (python-jose)."""
from datetime import datetime, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import ACCESS_TOKEN_EXPIRE, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    return pwd_context.hash(mot_de_passe)


def verifier_mot_de_passe(clair: str, hache: str) -> bool:
    return pwd_context.verify(clair, hache)


def creer_token(sujet: str) -> str:
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    payload = {"sub": sujet, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def lire_token(token: str) -> str | None:
    """Renvoie le login contenu dans le jeton, ou None si invalide/expiré."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
