from fastapi import APIRouter
from pydantic import BaseModel

from . import store

router = APIRouter(prefix="/stats", tags=["stats"])


class VisiteurRequest(BaseModel):
    visiteur_id: str


@router.post("/visiteur")
def enregistrer(requete: VisiteurRequest):
    return {"total_visiteurs_uniques": store.enregistrer_visiteur(requete.visiteur_id)}


@router.get("/visiteur")
def lire():
    return {"total_visiteurs_uniques": store.compter_visiteurs()}
