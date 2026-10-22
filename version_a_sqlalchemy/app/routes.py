"""Routes CRUD des albums."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import utilisateur_courant
from .database import get_db
from .models import Album, Utilisateur
from .schemas import AlbumCreate, AlbumOut, AlbumUpdate

router = APIRouter(prefix="/albums", tags=["Albums"])


def _get_ou_404(db: Session, album_id: int) -> Album:
    album = db.get(Album, album_id)
    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album {album_id} introuvable.",
        )
    return album


# --- Lecture : ouverte à tout le monde ---

@router.get("", response_model=list[AlbumOut])
def lister_albums(db: Session = Depends(get_db)):
    return db.query(Album).all()


@router.get("/{album_id}", response_model=AlbumOut)
def lire_album(album_id: int, db: Session = Depends(get_db)):
    return _get_ou_404(db, album_id)


# --- Écriture : réservée aux utilisateurs connectés ---

@router.post("", response_model=AlbumOut, status_code=status.HTTP_201_CREATED)
def creer_album(
    data: AlbumCreate,
    db: Session = Depends(get_db),
    user: Utilisateur = Depends(utilisateur_courant),
):
    album = Album(**data.model_dump(), ajoute_par=user.nom)
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@router.put("/{album_id}", response_model=AlbumOut)
def modifier_album(
    album_id: int,
    data: AlbumUpdate,
    db: Session = Depends(get_db),
    user: Utilisateur = Depends(utilisateur_courant),
):
    album = _get_ou_404(db, album_id)
    for champ, valeur in data.model_dump().items():
        setattr(album, champ, valeur)
    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_album(
    album_id: int,
    db: Session = Depends(get_db),
    user: Utilisateur = Depends(utilisateur_courant),
):
    album = _get_ou_404(db, album_id)
    db.delete(album)
    db.commit()
    return None
