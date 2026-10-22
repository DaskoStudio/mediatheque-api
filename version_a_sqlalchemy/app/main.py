"""Point d'entrée de l'API. Se lance avec : uvicorn app.main:app --reload
ou directement : python -m app.main
"""
from fastapi import FastAPI

from . import auth, routes
from .config import DEFAULT_PASSWORD, DEFAULT_USER
from .database import Base, SessionLocal, engine
from .models import Utilisateur
from .security import hacher_mot_de_passe


def creer_compte_par_defaut() -> None:
    """Crée le compte de démarrage si la base n'en contient pas encore."""
    db = SessionLocal()
    try:
        existe = db.query(Utilisateur).filter(Utilisateur.nom == DEFAULT_USER).first()
        if existe is None:
            db.add(
                Utilisateur(
                    nom=DEFAULT_USER,
                    mot_de_passe_hash=hacher_mot_de_passe(DEFAULT_PASSWORD),
                )
            )
            db.commit()
    finally:
        db.close()


def creer_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    creer_compte_par_defaut()

    app = FastAPI(
        title="Médiathèque d'albums — Version A (SQLAlchemy + JWT)",
        description="API CRUD d'albums de musique avec authentification par jeton JWT.",
        version="1.0.0",
    )
    app.include_router(auth.router)
    app.include_router(routes.router)

    @app.get("/", tags=["Info"])
    def racine():
        return {"message": "API médiathèque — voir /docs pour Swagger."}

    return app


app = creer_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
