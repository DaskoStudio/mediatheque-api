"""Modèles Pydantic : validation des entrées et forme des sorties.

Approche différente de la Version A : les contraintes sont écrites à la main
dans des validateurs, et le genre est vérifié par appartenance à la liste.
"""
from pydantic import BaseModel, field_validator

import settings


class AlbumEntree(BaseModel):
    """Données envoyées par le client (création / modification)."""
    titre: str
    artiste: str
    genre: str
    annee: int
    note: float

    @field_validator("titre", "artiste")
    @classmethod
    def non_vide(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Ce champ est obligatoire et ne peut pas être vide.")
        return v.strip()

    @field_validator("genre")
    @classmethod
    def genre_valide(cls, v: str) -> str:
        if v not in settings.GENRES_AUTORISES:
            raise ValueError(
                f"Genre invalide. Choisir parmi : {', '.join(settings.GENRES_AUTORISES)}"
            )
        return v

    @field_validator("annee")
    @classmethod
    def annee_plausible(cls, v: int) -> int:
        if v < settings.ANNEE_MIN or v > settings.ANNEE_MAX:
            raise ValueError(
                f"Année invalide (attendu entre {settings.ANNEE_MIN} et {settings.ANNEE_MAX})."
            )
        return v

    @field_validator("note")
    @classmethod
    def note_sur_dix(cls, v: float) -> float:
        if v < 0 or v > 10:
            raise ValueError("La note doit être comprise entre 0 et 10.")
        return v


class AlbumSortie(BaseModel):
    """Données renvoyées par l'API. `date_ajout` (interne) est volontairement absent."""
    id: int
    titre: str
    artiste: str
    genre: str
    annee: int
    note: float


class Identifiants(BaseModel):
    nom: str
    mot_de_passe: str


class Jeton(BaseModel):
    jeton: str
    type: str = "bearer"
    expire_dans_secondes: int = settings.DUREE_JETON
