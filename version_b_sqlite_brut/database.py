"""Accès base de données en sqlite3 « brut » (pas d'ORM).

Chaque fonction ouvre une connexion courte. Les tables sont créées au
démarrage et le compte par défaut est inséré s'il manque.
"""
import sqlite3
from datetime import datetime, timezone

import settings
from security import hacher


def connexion() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.BASE_FICHIER)
    conn.row_factory = sqlite3.Row  # accès aux colonnes par nom
    return conn


def initialiser() -> None:
    conn = connexion()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            mdp_hash TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            artiste TEXT NOT NULL,
            genre TEXT NOT NULL,
            annee INTEGER NOT NULL,
            note REAL NOT NULL,
            date_ajout TEXT NOT NULL   -- champ interne, jamais renvoyé au client
        )
        """
    )
    # Compte par défaut
    cur.execute("SELECT id FROM utilisateurs WHERE nom = ?", (settings.COMPTE_DEFAUT,))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO utilisateurs (nom, mdp_hash) VALUES (?, ?)",
            (settings.COMPTE_DEFAUT, hacher(settings.MDP_DEFAUT)),
        )
    conn.commit()
    conn.close()


# --- Utilisateurs ---

def trouver_utilisateur(nom: str):
    conn = connexion()
    row = conn.execute(
        "SELECT * FROM utilisateurs WHERE nom = ?", (nom,)
    ).fetchone()
    conn.close()
    return row


# --- Albums ---

def lister() -> list[sqlite3.Row]:
    conn = connexion()
    rows = conn.execute("SELECT * FROM albums ORDER BY id").fetchall()
    conn.close()
    return rows


def obtenir(album_id: int):
    conn = connexion()
    row = conn.execute("SELECT * FROM albums WHERE id = ?", (album_id,)).fetchone()
    conn.close()
    return row


def inserer(titre, artiste, genre, annee, note) -> int:
    conn = connexion()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO albums (titre, artiste, genre, annee, note, date_ajout)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (titre, artiste, genre, annee, note, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    nouvel_id = cur.lastrowid
    conn.close()
    return nouvel_id


def mettre_a_jour(album_id, titre, artiste, genre, annee, note) -> None:
    conn = connexion()
    conn.execute(
        """UPDATE albums SET titre = ?, artiste = ?, genre = ?, annee = ?, note = ?
           WHERE id = ?""",
        (titre, artiste, genre, annee, note, album_id),
    )
    conn.commit()
    conn.close()


def supprimer(album_id: int) -> None:
    conn = connexion()
    conn.execute("DELETE FROM albums WHERE id = ?", (album_id,))
    conn.commit()
    conn.close()
