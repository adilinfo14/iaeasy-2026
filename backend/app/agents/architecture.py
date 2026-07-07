COMPOSANTS = [
    {"id": "source_document", "titre": "Source de documents", "icone": "📄", "categorie": "source",
     "description": "Le document brut à traiter (contrat, FAQ, notice…)."},
    {"id": "chunking", "titre": "Découpage (chunking)", "icone": "✂️", "categorie": "traitement",
     "description": "Découpe un document long en petits morceaux exploitables par la base vectorielle."},
    {"id": "base_vectorielle", "titre": "Base vectorielle", "icone": "🗄️", "categorie": "stockage",
     "description": "Indexe les chunks sous forme de vecteurs et retrouve les plus pertinents pour une question."},
    {"id": "llm_agent", "titre": "LLM", "icone": "🧠", "categorie": "modele",
     "description": "Génère la réponse finale, avec ou sans contexte augmenté par le retrieval."},
    {"id": "outil_mcp", "titre": "Outil / MCP", "icone": "🛠️", "categorie": "outil",
     "description": "Un outil externe (calculatrice, recherche) appelable via MCP."},
    {"id": "agent_unique", "titre": "Agent (boucle ReAct)", "icone": "🔁", "categorie": "modele",
     "description": "Un LLM qui décide seul quels outils utiliser, en plusieurs étapes."},
    {"id": "multi_agent", "titre": "Pipeline multi-agent", "icone": "🤝", "categorie": "modele",
     "description": "Deux agents spécialisés qui collaborent (chercheur → rédacteur)."},
    {"id": "llm_seul", "titre": "LLM seul (sans contexte)", "icone": "💬", "categorie": "modele",
     "description": "Un LLM répond directement à un prompt, sans document ni outil."},
    {"id": "rag", "titre": "RAG simplifié", "icone": "📚", "categorie": "modele",
     "description": "Version tout-en-un du RAG (retrieval + génération en un seul nœud)."},
]

TEMPLATES = [
    {
        "id": "assistant_rag",
        "titre": "Assistant RAG documentaire",
        "description": (
            "L'architecture qu'un architecte IA mettrait en place pour un assistant qui répond à "
            "partir des documents de l'entreprise : Document → Découpage → Base vectorielle → LLM."
        ),
        "nodes": [
            {"id": "1", "type": "source_document", "config": {}, "position": {"x": 40, "y": 120}},
            {"id": "2", "type": "chunking", "config": {}, "position": {"x": 280, "y": 120}},
            {"id": "3", "type": "base_vectorielle", "config": {"prompt": "Quelles sont les conditions de garantie ?"}, "position": {"x": 520, "y": 120}},
            {"id": "4", "type": "llm_agent", "config": {}, "position": {"x": 760, "y": 120}},
        ],
        "edges": [
            {"source": "1", "target": "2"},
            {"source": "2", "target": "3"},
            {"source": "3", "target": "4"},
        ],
    },
    {
        "id": "agent_outils",
        "titre": "Agent avec outils",
        "description": (
            "Un agent unique qui décide lui-même quel outil (calculatrice, recherche) appeler "
            "pour répondre, en plusieurs étapes de raisonnement."
        ),
        "nodes": [
            {"id": "1", "type": "agent_unique", "config": {"prompt": "Combien font 15 fois (2 + 6) ?"}, "position": {"x": 200, "y": 120}},
        ],
        "edges": [],
    },
    {
        "id": "pipeline_multi_agent",
        "titre": "Pipeline multi-agent",
        "description": (
            "Deux agents spécialisés qui collaborent : un chercheur rassemble l'information, "
            "un rédacteur la transforme en réponse claire."
        ),
        "nodes": [
            {"id": "1", "type": "multi_agent", "config": {"prompt": "Explique ce qu'est un agent IA à un client non technique."}, "position": {"x": 200, "y": 120}},
        ],
        "edges": [],
    },
]


def get_composants() -> list[dict]:
    return COMPOSANTS


def get_templates() -> list[dict]:
    return TEMPLATES
