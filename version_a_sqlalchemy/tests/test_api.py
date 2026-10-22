"""Tests demandés : création d'un album (connecté) + refus si non connecté.
Lancer avec : pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DEFAULT_PASSWORD, DEFAULT_USER
from app.database import Base, get_db
from app.main import app
from app.models import Utilisateur
from app.security import hacher_mot_de_passe

# Base de test isolée (fichier séparé, on ne touche pas à la vraie base).
engine_test = create_engine(
    "sqlite:///./test_mediatheque.db",
    connect_args={"check_same_thread": False},
)
SessionTest = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)


def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def base_propre():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    db = SessionTest()
    db.add(
        Utilisateur(nom=DEFAULT_USER, mot_de_passe_hash=hacher_mot_de_passe(DEFAULT_PASSWORD))
    )
    db.commit()
    db.close()
    yield


client = TestClient(app)

ALBUM = {
    "titre": "Random Access Memories",
    "artiste": "Daft Punk",
    "genre": "Electro",
    "annee": 2013,
    "note": 9.5,
}


def _token() -> str:
    r = client.post("/login", data={"username": DEFAULT_USER, "password": DEFAULT_PASSWORD})
    assert r.status_code == 200
    return r.json()["access_token"]


def test_creation_album_connecte():
    """Un utilisateur connecté peut créer un album -> 201, sans champ interne."""
    headers = {"Authorization": f"Bearer {_token()}"}
    r = client.post("/albums", json=ALBUM, headers=headers)
    assert r.status_code == 201
    corps = r.json()
    assert corps["titre"] == "Random Access Memories"
    assert "id" in corps
    assert "ajoute_par" not in corps  # le champ interne ne fuite pas


def test_creation_refusee_si_non_connecte():
    """Sans jeton, la création est refusée (401)."""
    r = client.post("/albums", json=ALBUM)
    assert r.status_code == 401
