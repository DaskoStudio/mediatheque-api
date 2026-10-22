"""Dépendances d'authentification et route de connexion."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import get_db
from .models import Utilisateur
from .schemas import Token
from .security import creer_token, lire_token, verifier_mot_de_passe

router = APIRouter(tags=["Authentification"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def utilisateur_courant(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Utilisateur:
    """Vérifie le jeton et renvoie l'utilisateur. 401 sinon."""
    erreur = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton invalide ou expiré.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    login = lire_token(token)
    if login is None:
        raise erreur
    user = db.query(Utilisateur).filter(Utilisateur.nom == login).first()
    if user is None:
        raise erreur
    return user


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(Utilisateur).filter(Utilisateur.nom == form.username).first()
    if user is None or not verifier_mot_de_passe(form.password, user.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects.",
        )
    return Token(access_token=creer_token(user.nom))
