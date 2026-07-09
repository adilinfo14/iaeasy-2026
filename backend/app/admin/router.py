import hmac

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..core.config import settings
from ..core.reglages import get_reglages, set_reglages

router = APIRouter(prefix="/admin", tags=["admin"])

# Le mot de passe voyage dans le corps de la requête (POST), jamais en query string, pour ne
# jamais finir en clair dans les logs d'accès nginx. Comparaison à temps constant (hmac) pour
# éviter une attaque par timing sur un mot de passe aussi court.


def _verifier_mot_de_passe(mot_de_passe: str) -> None:
    if not settings.admin_password or not hmac.compare_digest(mot_de_passe, settings.admin_password):
        raise HTTPException(403, "Mot de passe incorrect.")


class AuthRequest(BaseModel):
    mot_de_passe: str = Field(max_length=200)


class ReglagesRequest(BaseModel):
    mot_de_passe: str = Field(max_length=200)
    chat_max_historique: int = Field(ge=2, le=30)
    chat_longueur_max_message: int = Field(ge=50, le=2000)
    chat_longueur_max_message_historique: int = Field(ge=200, le=5000)
    chat_max_conversations_simultanees: int = Field(ge=1, le=20)


@router.post("/verifier")
def verifier(requete: AuthRequest):
    _verifier_mot_de_passe(requete.mot_de_passe)
    return {"ok": True}


@router.post("/reglages")
def lire_reglages(requete: AuthRequest):
    _verifier_mot_de_passe(requete.mot_de_passe)
    return get_reglages()


@router.post("/reglages/modifier")
def modifier_reglages(requete: ReglagesRequest):
    _verifier_mot_de_passe(requete.mot_de_passe)
    nouveaux = requete.model_dump(exclude={"mot_de_passe"})
    return set_reglages(nouveaux)
