"""Modèles ORM SQLAlchemy (tables de la base)."""
from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)
    mot_de_passe_hash = Column(String, nullable=False)


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    artiste = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    annee = Column(Integer, nullable=False)
    note = Column(Float, nullable=False)

    # Champ interne : rempli par l'API (login de celui qui a créé l'album).
    # Il n'apparaît JAMAIS dans une réponse (absent du schéma AlbumOut).
    ajoute_par = Column(String, nullable=True)
