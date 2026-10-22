# Médiathèque — API de gestion (TP final)

API de gestion d'une médiathèque (albums, utilisateurs, authentification), livrée en **deux implémentations** pour comparer deux approches d'accès aux données en **FastAPI / Python**.

## 📦 Deux versions

| Version | Accès données | Dossier |
|---|---|---|
| **A — SQLAlchemy** | ORM SQLAlchemy | [`version_a_sqlalchemy/`](version_a_sqlalchemy/) |
| **B — SQLite brut** | SQL direct (sqlite3) | [`version_b_sqlite_brut/`](version_b_sqlite_brut/) |

Chaque version contient son propre `README.md`, ses tests et son `requirements.txt`.

## ✨ Fonctionnalités

- CRUD des albums / médias
- Authentification et hachage sécurisé des mots de passe
- Couche sécurité (contrôle d'accès)
- Tests d'API

## 🚀 Lancer (exemple version A)

```bash
cd version_a_sqlalchemy
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🛠️ Stack

Python · FastAPI · SQLAlchemy / SQLite · Pytest

## 👤 Auteur

Konaté Adama (**[@DaskoStudio](https://github.com/DaskoStudio)**) — Ynov Campus
