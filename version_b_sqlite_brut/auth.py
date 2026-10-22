"""Authentification : route de connexion (JSON) et garde HTTPBearer."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import database
from models import Identifiants, Jeton
from security import generer_jeton, valider_jeton, verifier

router = APIRouter(tags=["Authentification"])
schema_bearer = HTTPBearer(auto_error=True)


def exiger_connexion(
    creds: HTTPAuthorizationCredentials = Depends(schema_bearer),
) -> str:
    """Renvoie le nom d'utilisateur si le jeton Bearer est valide, sinon 401."""
    nom = valider_jeton(creds.credentials)
    if nom is None:
        raise HTTPException(status_code=401, detail="Jeton absent, invalide ou expiré.")
    return nom


@router.post("/connexion", response_model=Jeton)
def connexion(identifiants: Identifiants):
    utilisateur = database.trouver_utilisateur(identifiants.nom)
    if utilisateur is None or not verifier(identifiants.mot_de_passe, utilisateur["mdp_hash"]):
        raise HTTPException(status_code=401, detail="Nom ou mot de passe incorrect.")
    return Jeton(jeton=generer_jeton(utilisateur["nom"]))
