"""Schémas Pydantic v2 : validation des entrées / forme des sorties."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import GENRES

# Type genre restreint à la liste fixe (rejet automatique si hors liste).
GenreLitteral = Literal[GENRES]  # type: ignore[valid-type]

ANNEE_MIN = 1900
ANNEE_MAX = datetime.now().year + 1


class AlbumBase(BaseModel):
    titre: str = Field(min_length=1, max_length=200)
    artiste: str = Field(min_length=1, max_length=200)
    genre: GenreLitteral
    annee: int = Field(ge=ANNEE_MIN, le=ANNEE_MAX)
    note: float = Field(ge=0, le=10)

    @field_validator("titre", "artiste")
    @classmethod
    def pas_que_des_espaces(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Le champ ne peut pas être vide.")
        return v


class AlbumCreate(AlbumBase):
    """Ce que le client envoie pour créer un album."""
    pass


class AlbumUpdate(AlbumBase):
    """Ce que le client envoie pour modifier un album (remplacement complet)."""
    pass


class AlbumOut(AlbumBase):
    """Ce que l'API renvoie. Ne contient PAS le champ interne `ajoute_par`."""
    model_config = ConfigDict(from_attributes=True)
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
