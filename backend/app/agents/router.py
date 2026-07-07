from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import engine
from .bricks import get_briques

router = APIRouter(prefix="/agents", tags=["agents"])


class Noeud(BaseModel):
    id: str
    type: str
    config: dict = {}


class Arete(BaseModel):
    source: str
    target: str


class GrapheRequest(BaseModel):
    nodes: list[Noeud]
    edges: list[Arete]


@router.get("/briques")
def briques():
    return get_briques()


@router.post("/run")
async def executer(requete: GrapheRequest):
    try:
        resultat = await engine.executer_graphe(
            [n.model_dump() for n in requete.nodes],
            [e.model_dump() for e in requete.edges],
        )
        return resultat
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(400, str(exc)) from exc
