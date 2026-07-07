BRIQUES = [
    {
        "id": "llm_seul",
        "ordre": 1,
        "titre": "LLM seul",
        "icone": "🧠",
        "mise_en_situation": (
            "Tu es développeur chez un artisan du bâtiment. Le patron te demande un premier "
            "prototype : un assistant qui répond aux questions générales des clients, sans "
            "rien connaître encore de l'entreprise."
        ),
        "avant": "Rien n'existe encore — chaque question est traitée à la main par un humain.",
        "apres": (
            "L'assistant répond directement à partir de ce qu'il a appris pendant son "
            "entraînement général, mais ne connaît rien de spécifique à l'entreprise."
        ),
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
        "icone": "📚",
        "mise_en_situation": (
            "Un client demande les conditions de garantie exactes de l'entreprise. Un LLM "
            "seul n'a jamais vu ce document interne — il ne peut pas connaître la réponse."
        ),
        "avant": "L'assistant invente ou botte en touche sur les informations propres à l'entreprise.",
        "apres": (
            "Avant de répondre, l'assistant cherche d'abord le passage le plus pertinent "
            "dans les documents de l'entreprise (via des embeddings), puis répond en "
            "s'appuyant dessus."
        ),
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
        "icone": "🛠️",
        "mise_en_situation": (
            "Un client demande de calculer un montant TTC précis. Un LLM peut se tromper "
            "en arithmétique — il vaut mieux qu'il utilise une vraie calculatrice."
        ),
        "avant": "L'assistant peut se tromper sur un calcul ou une recherche précise.",
        "apres": (
            "L'assistant peut désormais appeler un vrai outil externe (calculatrice, "
            "recherche documentaire) exposé via le protocole MCP (Model Context Protocol), "
            "plutôt que de tout deviner par lui-même."
        ),
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
        "icone": "🔁",
        "mise_en_situation": (
            "Le patron veut que l'assistant décide LUI-MÊME quel outil utiliser selon la "
            "question posée, sans qu'on lui dise à l'avance quoi faire."
        ),
        "avant": "Il fallait choisir manuellement RAG ou un outil selon le type de question.",
        "apres": (
            "L'assistant raisonne en boucle : il décide d'utiliser un outil, observe le "
            "résultat, puis décide de la suite — jusqu'à obtenir une réponse finale. "
            "C'est le principe de la boucle ReAct (Reason + Act)."
        ),
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
        "icone": "🤝",
        "mise_en_situation": (
            "Le patron veut maintenant que l'assistant rédige de vrais emails clients, pas "
            "juste des réponses brutes — une seule 'tête' a du mal à bien faire les deux."
        ),
        "avant": "Un seul agent devait à la fois chercher l'information ET bien la formuler.",
        "apres": (
            "Deux agents se répartissent le travail : un agent 'chercheur' rassemble "
            "l'information, puis un agent 'rédacteur' la met en forme claire et "
            "professionnelle. Chacun a un rôle et un prompt différent."
        ),
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
