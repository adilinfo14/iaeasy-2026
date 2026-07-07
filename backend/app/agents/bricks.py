BRIQUES = [
    {
        "id": "llm_seul",
        "ordre": 1,
        "titre": "LLM seul",
        "description_pedagogique": (
            "Un modèle de langage reçoit un prompt et répond directement, sans aucune "
            "aide extérieure. C'est la brique de base de tout agent."
        ),
        "prerequis": [],
    },
    {
        "id": "rag",
        "ordre": 2,
        "titre": "RAG (retrieval)",
        "description_pedagogique": (
            "Avant de répondre, on cherche d'abord les passages les plus proches en sens "
            "dans un mini-corpus (via des embeddings), et on les ajoute au prompt du LLM. "
            "Le modèle répond alors avec des informations qu'il n'avait pas apprises par cœur."
        ),
        "prerequis": ["llm_seul"],
    },
    {
        "id": "outil_mcp",
        "ordre": 3,
        "titre": "Outil / MCP",
        "description_pedagogique": (
            "Le modèle peut désormais appeler un vrai outil externe — ici une calculatrice "
            "et une recherche documentaire — exposé via le protocole MCP (Model Context "
            "Protocol), plutôt que de tout deviner par lui-même."
        ),
        "prerequis": ["rag"],
    },
    {
        "id": "agent_unique",
        "ordre": 4,
        "titre": "Agent unique (ReAct)",
        "description_pedagogique": (
            "Le modèle raisonne en boucle : il décide d'utiliser un outil, observe le "
            "résultat, puis décide de la suite — jusqu'à obtenir une réponse finale. "
            "C'est le principe de la boucle ReAct (Reason + Act)."
        ),
        "prerequis": ["outil_mcp"],
    },
    {
        "id": "multi_agent",
        "ordre": 5,
        "titre": "Multi-agent",
        "description_pedagogique": (
            "Deux agents se répartissent le travail : un agent 'chercheur' rassemble "
            "l'information, puis un agent 'rédacteur' la met en forme. Chacun a un rôle "
            "et un prompt différent."
        ),
        "prerequis": ["agent_unique"],
    },
]


def get_briques() -> list[dict]:
    return BRIQUES
