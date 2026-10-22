"""Routes CRUD des albums (Version B)."""
from fastapi import APIRouter, Depends, HTTPException, Response

import database
from auth import exiger_connexion
from models import AlbumEntree, AlbumSortie

router = APIRouter(prefix="/albums", tags=["Albums"])


def _en_sortie(row) -> AlbumSortie:
    """Convertit une ligne SQLite en modèle de sortie (sans le champ interne)."""
    return AlbumSortie(
        id=row["id"],
        titre=row["titre"],
        artiste=row["artiste"],
        genre=row["genre"],
        annee=row["annee"],
        note=row["note"],
    )


def _ou_404(album_id: int):
    row = database.obtenir(album_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Album {album_id} introuvable.")
    return row


# --- Consultation libre ---

@router.get("", response_model=list[AlbumSortie])
def lister():
    return [_en_sortie(r) for r in database.lister()]


@router.get("/{album_id}", response_model=AlbumSortie)
def lire(album_id: int):
    return _en_sortie(_ou_404(album_id))


# --- Écriture protégée par jeton ---

@router.post("", response_model=AlbumSortie, status_code=201)
def creer(album: AlbumEntree, _utilisateur: str = Depends(exiger_connexion)):
    nouvel_id = database.inserer(
        album.titre, album.artiste, album.genre, album.annee, album.note
    )
    return _en_sortie(database.obtenir(nouvel_id))


@router.put("/{album_id}", response_model=AlbumSortie)
def modifier(
    album_id: int, album: AlbumEntree, _utilisateur: str = Depends(exiger_connexion)
):
    _ou_404(album_id)
    database.mettre_a_jour(
        album_id, album.titre, album.artiste, album.genre, album.annee, album.note
    )
    return _en_sortie(database.obtenir(album_id))


@router.delete("/{album_id}", status_code=204)
def supprimer(album_id: int, _utilisateur: str = Depends(exiger_connexion)):
    _ou_404(album_id)
    database.supprimer(album_id)
    return Response(status_code=204)
