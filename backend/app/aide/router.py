from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..core.ollama_client import ollama
from ..glossaire.termes import get_termes

router = APIRouter(prefix="/aide", tags=["aide"])

# Un petit modèle (3B) improvisait de fausses définitions de termes techniques (ex: RAG confondu
# avec "Random Agent") plutôt que d'admettre ne pas savoir — exactement le piège d'hallucination
# que ce site enseigne par ailleurs. On utilise donc le modèle le plus capable disponible ET on
# l'ancre sur le vrai glossaire du site (voir _contexte_glossaire), au lieu de compter uniquement
# sur sa mémoire paramétrique.
_MODELE_AIDE = "qwen2.5:7b-instruct"


def _contexte_glossaire() -> str:
    lignes = [f"- {t['terme']} : {t['definition_simple']}" for t in get_termes()]
    return "\n".join(lignes)


def _systeme() -> str:
    return (
        "Tu es l'assistant pédagogique du site iaeasy, une plateforme française d'apprentissage de "
        "l'intelligence artificielle 100% souveraine (auto-hébergée, modèles open-source), destinée à "
        "un public souvent débutant. Ton rôle : aider à comprendre un terme technique ou une notion "
        "d'IA rencontrée sur le site, en langage simple, sans jargon inutile, en 2 à 4 phrases maximum.\n\n"
        "Voici le glossaire officiel du site, à utiliser en PRIORITÉ absolue si la question porte sur "
        "l'un de ces termes — ne t'écarte pas de ces définitions et ne les remplace jamais par une "
        "connaissance générale différente :\n"
        f"{_contexte_glossaire()}\n\n"
        "Si la question porte sur un terme d'IA qui n'est PAS dans cette liste, tu peux répondre avec "
        "tes connaissances générales, mais dis clairement si tu n'es pas certain plutôt que d'inventer "
        "une définition. Si la question sort du sujet de l'IA ou du site, recadre poliment vers ce sujet.\n\n"
        "Réponds TOUJOURS entièrement en français, du début à la fin, sans jamais basculer même "
        "brièvement dans une autre langue (pas de mot ni de caractère en anglais, chinois ou autre)."
    )


_LONGUEUR_MAX_MESSAGE = 500
_MAX_HISTORIQUE = 8


class MessageHistorique(BaseModel):
    role: str = Field(max_length=16)
    content: str = Field(max_length=_LONGUEUR_MAX_MESSAGE)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=_LONGUEUR_MAX_MESSAGE)
    historique: list[MessageHistorique] = Field(default_factory=list, max_length=_MAX_HISTORIQUE)


@router.post("/chat")
async def chat(requete: ChatRequest):
    messages = [{"role": "system", "content": _systeme()}]
    for m in requete.historique[-_MAX_HISTORIQUE:]:
        role = m.role if m.role in ("user", "assistant") else "user"
        messages.append({"role": role, "content": m.content})
    messages.append({"role": "user", "content": requete.message})

    reponse = await ollama.chat(_MODELE_AIDE, messages)
    return {"reponse": reponse.get("content", "")}
