import json

from ..core.ollama_client import ollama
from . import tools

MODELE_LLM = "qwen2.5:7b-instruct"
MODELE_EMBED = "nomic-embed-text"

_MINI_CORPUS_RAG = tools._MINI_CORPUS

_TOOLS_OLLAMA_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "calculer",
            "description": "Évalue une expression arithmétique simple.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rechercher",
            "description": "Cherche un passage pertinent dans un petit corpus documentaire.",
            "parameters": {
                "type": "object",
                "properties": {"requete": {"type": "string"}},
                "required": ["requete"],
            },
        },
    },
]


def _topological_sort(nodes: list[dict], edges: list[dict]) -> list[str]:
    ids = [n["id"] for n in nodes]
    depend_de: dict[str, set[str]] = {i: set() for i in ids}
    for e in edges:
        depend_de[e["target"]].add(e["source"])

    ordre: list[str] = []
    restants = set(ids)
    while restants:
        prets = [i for i in restants if depend_de[i] <= set(ordre)]
        if not prets:
            raise ValueError("Le graphe contient un cycle ou une dépendance manquante")
        prets.sort(key=ids.index)
        ordre.append(prets[0])
        restants.discard(prets[0])
    return ordre


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _normaliser_arguments(arguments) -> dict:
    if isinstance(arguments, str):
        try:
            return json.loads(arguments)
        except json.JSONDecodeError:
            return {}
    return arguments or {}


def _executer_outil(nom: str, arguments: dict) -> str:
    if nom == "calculer":
        return str(tools.calculatrice(arguments.get("expression", ""))["resultat"])
    if nom == "rechercher":
        return tools.recherche_mini_corpus(arguments.get("requete", ""))["passage"]
    return f"Outil inconnu: {nom}"


async def _handler_llm_seul(config: dict, contexte: dict, etapes: list[dict]) -> dict:
    prompt = config.get("prompt") or contexte.get("prompt") or "Explique en une phrase ce qu'est un agent IA."
    reponse = await ollama.generate(MODELE_LLM, prompt)
    etapes.append({"brique": "llm_seul", "detail": f"Prompt envoyé au LLM : « {prompt} »"})
    contexte["derniere_reponse"] = reponse
    return contexte


async def _handler_rag(config: dict, contexte: dict, etapes: list[dict]) -> dict:
    requete = config.get("prompt") or contexte.get("prompt") or "Qu'est-ce que MCP ?"
    vecteur_requete = await ollama.embed(MODELE_EMBED, requete)

    meilleur_passage, meilleur_score = _MINI_CORPUS_RAG[0], -1.0
    for passage in _MINI_CORPUS_RAG:
        vecteur_passage = await ollama.embed(MODELE_EMBED, passage)
        score = _cosine(vecteur_requete, vecteur_passage)
        if score > meilleur_score:
            meilleur_passage, meilleur_score = passage, score

    etapes.append(
        {
            "brique": "rag",
            "detail": f"Passage retrouvé (similarité {meilleur_score:.2f}) : « {meilleur_passage} »",
        }
    )
    prompt_augmente = (
        f"Contexte retrouvé : {meilleur_passage}\n\nQuestion : {requete}\n"
        "Réponds en t'appuyant sur ce contexte."
    )
    reponse = await ollama.generate(MODELE_LLM, prompt_augmente)
    contexte["derniere_reponse"] = reponse
    contexte["passage_retrouve"] = meilleur_passage
    return contexte


async def _handler_outil_mcp(config: dict, contexte: dict, etapes: list[dict]) -> dict:
    outil = config.get("outil", "recherche")
    if outil == "calculatrice":
        expression = config.get("expression", "2 + 2")
        resultat = tools.calculatrice(expression)
        etapes.append(
            {"brique": "outil_mcp", "detail": f"Outil MCP 'calculer' sur « {expression} » -> {resultat}"}
        )
        contexte["resultat_outil"] = resultat
    else:
        requete = config.get("prompt") or contexte.get("prompt") or "MCP"
        resultat = tools.recherche_mini_corpus(requete)
        etapes.append(
            {
                "brique": "outil_mcp",
                "detail": f"Outil MCP 'rechercher' sur « {requete} » -> {resultat['passage']}",
            }
        )
        contexte["resultat_outil"] = resultat
    return contexte


async def _handler_agent_unique(config: dict, contexte: dict, etapes: list[dict]) -> dict:
    tache = config.get("prompt") or contexte.get("prompt") or "Combien font 12 fois (3+4) ?"
    messages = [
        {
            "role": "system",
            "content": "Tu es un agent qui peut utiliser des outils (calculer, rechercher) pour répondre précisément.",
        },
        {"role": "user", "content": tache},
    ]

    for iteration in range(4):
        message = await ollama.chat(MODELE_LLM, messages, tools=_TOOLS_OLLAMA_SCHEMA)
        tool_calls = message.get("tool_calls")
        if not tool_calls:
            etapes.append(
                {"brique": "agent_unique", "detail": f"Étape {iteration + 1} — réponse finale : {message['content']}"}
            )
            contexte["derniere_reponse"] = message["content"]
            return contexte

        messages.append(message)
        for appel in tool_calls:
            nom = appel["function"]["name"]
            arguments = _normaliser_arguments(appel["function"].get("arguments"))
            resultat = _executer_outil(nom, arguments)
            etapes.append(
                {
                    "brique": "agent_unique",
                    "detail": f"Étape {iteration + 1} — appel outil « {nom}({arguments}) » -> {resultat}",
                }
            )
            messages.append({"role": "tool", "content": resultat})

    contexte["derniere_reponse"] = "Nombre maximal d'itérations atteint sans réponse finale."
    return contexte


async def _handler_multi_agent(config: dict, contexte: dict, etapes: list[dict]) -> dict:
    tache = config.get("prompt") or contexte.get("prompt") or "Résume ce qu'est le RAG pour un débutant."

    messages_chercheur = [
        {
            "role": "system",
            "content": (
                "Tu es un agent CHERCHEUR : tu rassembles des faits bruts et précis, sans les "
                "mettre en forme, en t'aidant si besoin de l'outil 'rechercher'."
            ),
        },
        {"role": "user", "content": tache},
    ]
    reponse_chercheur = await ollama.chat(MODELE_LLM, messages_chercheur, tools=_TOOLS_OLLAMA_SCHEMA)
    if reponse_chercheur.get("tool_calls"):
        messages_chercheur.append(reponse_chercheur)
        for appel in reponse_chercheur["tool_calls"]:
            arguments = _normaliser_arguments(appel["function"].get("arguments"))
            resultat = _executer_outil(appel["function"]["name"], arguments)
            messages_chercheur.append({"role": "tool", "content": resultat})
        reponse_chercheur = await ollama.chat(MODELE_LLM, messages_chercheur)

    notes = reponse_chercheur["content"]
    etapes.append({"brique": "multi_agent", "detail": f"Agent chercheur -> notes brutes : {notes}"})

    messages_redacteur = [
        {
            "role": "system",
            "content": (
                "Tu es un agent RÉDACTEUR : tu reformules des notes brutes en une réponse claire "
                "et pédagogique, en 3-4 phrases maximum."
            ),
        },
        {"role": "user", "content": f"Notes du chercheur :\n{notes}\n\nTâche d'origine : {tache}"},
    ]
    reponse_redacteur = await ollama.chat(MODELE_LLM, messages_redacteur)
    etapes.append(
        {"brique": "multi_agent", "detail": f"Agent rédacteur -> réponse finale : {reponse_redacteur['content']}"}
    )

    contexte["derniere_reponse"] = reponse_redacteur["content"]
    return contexte


_HANDLERS = {
    "llm_seul": _handler_llm_seul,
    "rag": _handler_rag,
    "outil_mcp": _handler_outil_mcp,
    "agent_unique": _handler_agent_unique,
    "multi_agent": _handler_multi_agent,
}


async def executer_graphe(nodes: list[dict], edges: list[dict]) -> dict:
    ordre = _topological_sort(nodes, edges)
    noeuds_par_id = {n["id"]: n for n in nodes}

    contexte: dict = {}
    etapes: list[dict] = []

    for node_id in ordre:
        noeud = noeuds_par_id[node_id]
        type_brique = noeud["type"]
        handler = _HANDLERS.get(type_brique)
        if handler is None:
            raise ValueError(f"Type de brique inconnu : {type_brique}")
        contexte = await handler(noeud.get("config", {}), contexte, etapes)

    return {"etapes": etapes, "reponse_finale": contexte.get("derniere_reponse")}
