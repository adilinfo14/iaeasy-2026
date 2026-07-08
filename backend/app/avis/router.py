from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

from . import store

router = APIRouter(prefix="/avis", tags=["avis"])


class AvisRequest(BaseModel):
    visiteur_id: str = Field(min_length=1, max_length=64)
    note: int = Field(ge=1, le=5)
    commentaire: str | None = Field(default=None, max_length=500)


@router.post("")
def enregistrer(requete: AvisRequest):
    commentaire = (requete.commentaire or "").strip() or None
    store.enregistrer_avis(
        requete.visiteur_id,
        requete.note,
        commentaire,
        datetime.now(timezone.utc).isoformat(),
    )
    return store.stats_avis()


@router.get("/stats")
def stats():
    return store.stats_avis()


@router.get("")
def lister():
    tous = store.lister_avis()
    tous.sort(key=lambda a: a["horodatage"], reverse=True)
    return tous
