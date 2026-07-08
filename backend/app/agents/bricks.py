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
        "schema": [
            {"icone": "💬", "label": "Votre question"},
            {"icone": "🧠", "label": "LLM"},
            {"icone": "✅", "label": "Réponse directe"},
        ],
        "prerequis": [],
        "quiz": [
            {
                "question": "Un LLM seul répond à une question en se basant sur...",
                "options": [
                    "Une recherche dans les documents de l'entreprise",
                    "Uniquement ce qu'il a appris pendant son entraînement général",
                    "Le résultat d'une calculatrice externe",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Pourquoi un LLM seul ne peut-il pas connaître les conditions de garantie propres à une entreprise ?",
                "options": [
                    "Parce qu'il n'a jamais vu ce document interne pendant son entraînement",
                    "Parce qu'il refuse de répondre aux questions sur les garanties",
                    "Parce qu'il a besoin d'un outil pour ça",
                ],
                "bonne_reponse": 0,
            },
        ],
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
        "schema": [
            {"icone": "❓", "label": "Votre question"},
            {"icone": "🔎", "label": "Recherche dans les documents"},
            {"icone": "📄", "label": "Passage retrouvé"},
            {"icone": "🧠", "label": "LLM + ce passage"},
            {"icone": "✅", "label": "Réponse"},
        ],
        "prerequis": ["llm_seul"],
        "quiz": [
            {
                "question": "Que fait la brique RAG avant de laisser le LLM répondre ?",
                "options": [
                    "Elle appelle une calculatrice",
                    "Elle cherche d'abord le passage le plus pertinent dans les documents, via des embeddings",
                    "Elle demande à un second agent de vérifier la réponse",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Un embedding sert principalement à...",
                "options": [
                    "Transformer un texte en nombres qui capturent son sens, pour comparer des textes entre eux",
                    "Exécuter un calcul mathématique précis",
                    "Décider quel outil un agent doit utiliser",
                ],
                "bonne_reponse": 0,
            },
        ],
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
        "schema": [
            {"icone": "❓", "label": "Demande"},
            {"icone": "🛠️", "label": "Appel de l'outil (MCP)"},
            {"icone": "📊", "label": "Résultat de l'outil"},
            {"icone": "✅", "label": "Réponse"},
        ],
        "prerequis": ["rag"],
        "quiz": [
            {
                "question": "Pourquoi utiliser une calculatrice plutôt que de laisser le LLM calculer lui-même ?",
                "options": [
                    "Parce qu'un LLM peut se tromper en arithmétique, alors qu'une calculatrice ne se trompe jamais",
                    "Parce que c'est obligatoire pour toutes les questions",
                    "Parce que ça rend la réponse plus longue",
                ],
                "bonne_reponse": 0,
            },
            {
                "question": "MCP signifie...",
                "options": [
                    "Model Context Protocol — un standard pour que les modèles appellent des outils",
                    "Multiple Chat Processing",
                    "Machine Calculation Program",
                ],
                "bonne_reponse": 0,
            },
        ],
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
        "schema": [
            {"icone": "❓", "label": "Tâche"},
            {"icone": "🤔", "label": "Le LLM réfléchit"},
            {"icone": "🛠️", "label": "Appelle un outil si besoin"},
            {"icone": "🔁", "label": "Répète jusqu'à avoir la réponse"},
            {"icone": "✅", "label": "Réponse finale"},
        ],
        "prerequis": ["outil_mcp"],
        "quiz": [
            {
                "question": "Qu'est-ce que la boucle ReAct ?",
                "options": [
                    "Le modèle alterne entre raisonner (Reason) et agir (Act) jusqu'à obtenir une réponse finale",
                    "Le modèle répète toujours la même réponse deux fois",
                    "Le modèle refuse d'utiliser des outils",
                ],
                "bonne_reponse": 0,
            },
            {
                "question": "Quel est l'avantage principal d'un agent unique par rapport à un enchaînement RAG + outil fixé à l'avance ?",
                "options": [
                    "Il décide lui-même quel outil utiliser selon la question, sans qu'on le lui impose",
                    "Il est toujours plus rapide, quelle que soit la question",
                    "Il n'a jamais besoin d'outils",
                ],
                "bonne_reponse": 0,
            },
        ],
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
        "schema": [
            {"icone": "❓", "label": "Tâche"},
            {"icone": "🔍", "label": "Agent chercheur"},
            {"icone": "📝", "label": "Notes brutes"},
            {"icone": "✍️", "label": "Agent rédacteur"},
            {"icone": "✅", "label": "Réponse finale"},
        ],
        "prerequis": ["agent_unique"],
        "quiz": [
            {
                "question": "Dans un pipeline chercheur + rédacteur, quel est le rôle de l'agent rédacteur ?",
                "options": [
                    "Rassembler les faits bruts en cherchant dans un corpus",
                    "Mettre en forme les informations rassemblées en une réponse claire et professionnelle",
                    "Appeler la calculatrice",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Quel est le principal inconvénient d'un pipeline multi-agent par rapport à un agent unique ?",
                "options": [
                    "Il coûte et prend deux fois plus d'appels LLM",
                    "Il ne peut jamais utiliser d'outils",
                    "Il ne fonctionne que sur des questions de calcul",
                ],
                "bonne_reponse": 0,
            },
        ],
    },
]


def get_briques() -> list[dict]:
    return BRIQUES
