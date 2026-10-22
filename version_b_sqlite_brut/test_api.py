"""Tests demandés (Version B) : création d'un album + refus sans jeton.
Lancer avec : pytest
"""
import os

import pytest
from fastapi.testclient import TestClient

import settings

# On bascule sur une base de test isolée AVANT d'importer le reste.
settings.BASE_FICHIER = "test_mediatheque_b.db"

import database  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)

ALBUM = {
    "titre": "Discovery",
    "artiste": "Daft Punk",
    "genre": "Electro",
    "annee": 2001,
    "note": 9.0,
}


@pytest.fixture(autouse=True)
def base_neuve():
    if os.path.exists(settings.BASE_FICHIER):
        os.remove(settings.BASE_FICHIER)
    database.initialiser()
    yield
    if os.path.exists(settings.BASE_FICHIER):
        os.remove(settings.BASE_FICHIER)


def _jeton() -> str:
    r = client.post(
        "/connexion",
        json={"nom": settings.COMPTE_DEFAUT, "mot_de_passe": settings.MDP_DEFAUT},
    )
    assert r.status_code == 200
    return r.json()["jeton"]


def test_creation_album_connecte():
    """Connecté -> création acceptée (201) et champ interne absent de la réponse."""
    headers = {"Authorization": f"Bearer {_jeton()}"}
    r = client.post("/albums", json=ALBUM, headers=headers)
    assert r.status_code == 201
    corps = r.json()
    assert corps["titre"] == "Discovery"
    assert "id" in corps
    assert "date_ajout" not in corps  # le champ interne ne doit pas fuiter


def test_creation_refusee_sans_jeton():
    """Sans jeton Bearer -> 401/403, la création est bloquée."""
    r = client.post("/albums", json=ALBUM)
    assert r.status_code in (401, 403)
