from fastapi import APIRouter
from pydantic import BaseModel, Field

from . import store

router = APIRouter(prefix="/stats", tags=["stats"])


class VisiteurRequest(BaseModel):
    visiteur_id: str = Field(min_length=1, max_length=64)


@router.post("/visiteur")
def enregistrer(requete: VisiteurRequest):
    return {"total_visiteurs_uniques": store.enregistrer_visiteur(requete.visiteur_id)}


@router.get("/visiteur")
def lire():
    return {"total_visiteurs_uniques": store.compter_visiteurs()}
