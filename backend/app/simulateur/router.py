import time

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.ollama_client import ollama

router = APIRouter(prefix="/simulateur", tags=["simulateur"])

# Tailles approximatives en milliards de paramètres — chiffres publics arrondis, à but
# uniquement pédagogique (l'estimation d'énergie qui en découle est une approximation
# proportionnelle, PAS une mesure réelle de consommation).
_MODELES = [
    {"id": "llama3.2:3b", "nom": "Llama 3.2 (3B)", "parametres_milliards": 3.2},
    {"id": "deepseek-coder:6.7b", "nom": "DeepSeek Coder (6.7B)", "parametres_milliards": 6.7},
    {"id": "qwen2.5:7b-instruct", "nom": "Qwen 2.5 7B Instruct", "parametres_milliards": 7.6},
]

_PROMPT_DEFAUT = "Explique en 3 phrases ce qu'est la garantie décennale."
_LONGUEUR_MAX_PROMPT = 300


class ComparerRequest(BaseModel):
    prompt: str | None = Field(default=None, max_length=_LONGUEUR_MAX_PROMPT)


@router.get("/modeles")
def modeles():
    return _MODELES


@router.post("/comparer")
async def comparer(requete: ComparerRequest):
    prompt = (requete.prompt or "").strip() or _PROMPT_DEFAUT
    plus_gros = max(m["parametres_milliards"] for m in _MODELES)

    resultats = []
    for m in _MODELES:
        debut = time.monotonic()
        reponse = await ollama.generate(m["id"], prompt)
        duree = time.monotonic() - debut
        resultats.append(
            {
                "id": m["id"],
                "nom": m["nom"],
                "parametres_milliards": m["parametres_milliards"],
                "duree_secondes": round(duree, 2),
                "longueur_reponse": len(reponse),
                "reponse": reponse[:400],
                "estimation_energie_relative_pourcent": round(100 * m["parametres_milliards"] / plus_gros),
            }
        )

    return {"prompt": prompt, "resultats": resultats}
