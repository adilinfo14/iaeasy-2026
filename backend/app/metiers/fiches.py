METIERS = [
    {
        "id": "artisan_batiment",
        "titre": "Artisan du bâtiment",
        "icone": "🔨",
        "description": (
            "Plombier, électricien, maçon, couvreur... L'IA ne remplace pas le métier, mais peut "
            "absorber les tâches répétitives autour du chantier : trier les avis, répondre aux "
            "questions courantes, anticiper la trésorerie."
        ),
        "cas_usage": [
            {
                "titre": "Trier automatiquement les avis clients",
                "description": (
                    "Un modèle entraîné en quelques secondes classe chaque avis en positif/négatif, "
                    "pour prioriser les réponses aux clients mécontents sans tout relire soi-même."
                ),
                "page": "/entrainement",
                "texte_lien": "Essayer le scénario « Trier des avis clients » →",
            },
            {
                "titre": "Répondre aux questions sur les devis et garanties, 24h/24",
                "description": (
                    "Un assistant qui va chercher la réponse dans vos vrais documents (conditions de "
                    "garantie, modalités de paiement) plutôt que d'inventer une réponse approximative."
                ),
                "page": "/constructeur",
                "texte_lien": "Voir le template « Assistant RAG documentaire » →",
            },
            {
                "titre": "Anticiper la trésorerie des prochains mois",
                "description": "À partir de l'historique de facturation, un modèle simple prévoit la tendance du chiffre d'affaires à venir.",
                "page": "/entrainement",
                "texte_lien": "Essayer le scénario « Prévoir le chiffre d'affaires » →",
            },
        ],
    },
    {
        "id": "commerce",
        "titre": "Commerçant / e-commerce",
        "icone": "🛍️",
        "description": (
            "Boutique physique ou en ligne : l'IA aide à filtrer le bruit (spam, fraude) et à mieux "
            "orienter chaque client vers ce qui l'intéresse vraiment."
        ),
        "cas_usage": [
            {
                "titre": "Filtrer les emails de spam et de phishing",
                "description": "Un algorithme classique (pas de réseau de neurones) apprend en quelques secondes à distinguer un email légitime d'une tentative d'arnaque.",
                "page": "/entrainement",
                "texte_lien": "Essayer le scénario « Filtrer les emails indésirables » →",
            },
            {
                "titre": "Recommander des produits pertinents",
                "description": "À partir de l'historique d'achats ou de notes, un système de recommandation propose des produits cohérents avec les goûts du client.",
                "page": "/catalogue",
                "texte_lien": "Voir le modèle de recommandation dans le Catalogue →",
            },
            {
                "titre": "Détecter une transaction suspecte",
                "description": "Un modèle de détection d'anomalie repère les montants ou comportements très différents de l'habitude d'un client, sans règle fixe écrite à l'avance.",
                "page": "/catalogue",
                "texte_lien": "Voir Isolation Forest (fraude) dans le Catalogue →",
            },
        ],
    },
    {
        "id": "agriculture",
        "titre": "Agriculteur / agroalimentaire",
        "icone": "🌾",
        "description": (
            "De la maintenance du matériel au suivi des cultures, l'IA aide à repérer un problème "
            "tôt — à condition de rester honnête sur les limites d'un modèle générique non spécialisé."
        ),
        "cas_usage": [
            {
                "titre": "Repérer une machine qui va tomber en panne",
                "description": "Un modèle de maintenance prédictive détecte une vibration ou une température anormale avant la panne réelle, à partir des données du capteur.",
                "page": "/catalogue",
                "texte_lien": "Voir Isolation Forest (maintenance) dans le Catalogue →",
            },
            {
                "titre": "Classer une photo de plante ou de culture",
                "description": (
                    "Un modèle de vision générique peut classer une image, mais ne connaît pas les "
                    "maladies spécifiques d'une culture — une vraie limite à connaître avant tout usage réel."
                ),
                "page": "/catalogue",
                "texte_lien": "Voir la classification d'image dans le Catalogue →",
            },
            {
                "titre": "Prévoir un volume ou une tendance sur plusieurs mois",
                "description": "Un modèle de prévision de séries temporelles projette une tendance à partir d'un historique, avec un intervalle de confiance qui s'élargit avec l'horizon.",
                "page": "/catalogue",
                "texte_lien": "Voir Chronos (prévisions) dans le Catalogue →",
            },
        ],
    },
    {
        "id": "profession_liberale",
        "titre": "Profession libérale / indépendant",
        "icone": "⚖️",
        "description": (
            "Comptable, juriste, consultant... beaucoup de temps passé à lire, résumer et retrouver "
            "une information précise dans des documents longs — exactement ce que le RAG et le "
            "résumé automatique adressent."
        ),
        "cas_usage": [
            {
                "titre": "Résumer un long rapport ou contrat",
                "description": "Un document trop long pour être lu en entier est découpé, résumé morceau par morceau, puis synthétisé en un seul paragraphe cohérent.",
                "page": "/constructeur",
                "texte_lien": "Voir le template « Résumé hiérarchique » →",
            },
            {
                "titre": "Retrouver une réponse exacte dans un document",
                "description": "Un modèle de question-réponse extractive renvoie le passage exact du contexte fourni — jamais une réponse inventée.",
                "page": "/catalogue",
                "texte_lien": "Voir CamemBERT Question-Réponse dans le Catalogue →",
            },
            {
                "titre": "Traduire un document pour un client à l'étranger",
                "description": "Une traduction suivie d'une seconde passe de vérification, utile avant l'envoi d'un contenu contractuel ou technique à un client international.",
                "page": "/constructeur",
                "texte_lien": "Voir le template « Traduction assistée avec double vérification » →",
            },
        ],
    },
    {
        "id": "ressources_humaines",
        "titre": "Ressources humaines / recrutement",
        "icone": "🧑‍💼",
        "description": "Répondre aux questions répétitives des salariés, préparer une offre d'emploi ou un entretien — des tâches rédactionnelles qui se prêtent bien à l'IA.",
        "cas_usage": [
            {
                "titre": "Rédiger une offre d'emploi ou des questions d'entretien",
                "description": "Deux agents collaborent : l'un rassemble les critères du poste, l'autre rédige le texte final.",
                "page": "/constructeur",
                "texte_lien": "Voir le template « Assistant recrutement » →",
            },
            {
                "titre": "Répondre aux questions des nouveaux salariés",
                "description": "Un assistant documentaire répond aux questions courantes (congés, télétravail, arrêt maladie) à partir du livret d'accueil officiel.",
                "page": "/constructeur",
                "texte_lien": "Voir le template « Assistant RH onboarding » →",
            },
            {
                "titre": "Extraire les informations clés d'un CV",
                "description": "Un modèle d'extraction d'entités repère automatiquement les noms de personnes, d'entreprises et de lieux dans un texte.",
                "page": "/catalogue",
                "texte_lien": "Voir CamemBERT NER dans le Catalogue →",
            },
        ],
    },
    {
        "id": "commercial",
        "titre": "Commercial / relation client",
        "icone": "🤝",
        "description": "Préparer un appel, comprendre un message dans une langue inconnue, vérifier une réponse avant de l'envoyer — des gestes du quotidien commercial que l'IA peut accélérer.",
        "cas_usage": [
            {
                "titre": "Préparer un appel grâce à l'historique client",
                "description": "Un agent consulte l'historique disponible avant de préparer un argumentaire de relance personnalisé.",
                "page": "/constructeur",
                "texte_lien": "Voir le template « Assistant commercial (CRM) » →",
            },
            {
                "titre": "Détecter la langue d'un message client international",
                "description": "Un détecteur de langue identifie automatiquement la langue d'un message, y compris sur un texte assez court.",
                "page": "/catalogue",
                "texte_lien": "Voir la détection de langue dans le Catalogue →",
            },
            {
                "titre": "Vérifier une réponse avant de l'envoyer",
                "description": "Le modèle rédige un brouillon, puis une seconde passe le relit et corrige si besoin — utile avant l'envoi d'une réponse sensible à un client.",
                "page": "/constructeur",
                "texte_lien": "Voir le template « Vérificateur / auto-critique » →",
            },
        ],
    },
]


def get_metiers() -> list[dict]:
    return METIERS
