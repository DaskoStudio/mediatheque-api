"""Point d'entrée — Version B.

Lancement (une seule commande) :
    uvicorn main:app --reload
ou :
    python main.py
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

import albums
import auth
import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.initialiser()  # crée les tables + le compte par défaut au démarrage
    yield


app = FastAPI(
    title="Médiathèque d'albums — Version B (sqlite3 brut + itsdangerous)",
    description="API CRUD d'albums, stockage SQLite natif et jeton signé à durée limitée.",
    version="1.0.0",
    lifespan=lifespan,
)

# Init dès l'import : garantit que les tables existent quel que soit le mode de
# lancement (uvicorn, python main.py, ou import direct par les tests).
database.initialiser()

app.include_router(auth.router)
app.include_router(albums.router)


@app.get("/", tags=["Info"])
def accueil():
    return {"message": "API médiathèque (Version B). Documentation : /docs"}


if __name__ == "__main__":
    import uvicorn

    database.initialiser()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
