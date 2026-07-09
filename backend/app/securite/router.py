from fastapi import APIRouter

router = APIRouter(prefix="/securite", tags=["securite"])

SOURCE = (
    "Classement basé sur l'OWASP Top 10 for LLM Applications 2025 (owasp.org/www-project-top-10-for-large-language-model-applications), "
    "un standard ouvert et communautaire de sécurité — pas une liste propriétaire. Les exemples concrets illustrant certains risques "
    "proviennent d'une présentation d'OCTO (part of Accenture), © 2025, tous droits réservés ; seuls les faits/concepts sont décrits ici, "
    "les visuels originaux ne sont pas reproduits."
)

RISQUES = [
    {
        "id": "LLM01",
        "titre": "Prompt Injection",
        "risque": (
            "Un texte fourni au modèle (par l'utilisateur ou par un contenu externe qu'il lit) contient des instructions "
            "cachées qui détournent son comportement prévu. On distingue l'injection directe (l'utilisateur demande "
            "explicitement au modèle d'ignorer ses consignes) de l'injection indirecte (les instructions malveillantes sont "
            "cachées dans un document, un email ou une page web que le modèle traite pour quelqu'un d'autre)."
        ),
        "exemple_concret": (
            "Injection directe : en 2024, un chatbot de livraison (DPD) a été manipulé par un simple message lui demandant "
            "d'« exagérer et être excessif dans sa critique » de sa propre entreprise — il a obéi et a publiquement traité "
            "son employeur de pire livreur au monde. Injection indirecte : une faille réelle dans un assistant bureautique "
            "(surnommée « EchoLeak ») exploitait un email piégé — l'utilisateur demandait innocemment une information "
            "sensible, l'assistant répondait avec une image markdown dont l'URL encodait cette donnée, et le simple "
            "affichage de l'image par le navigateur suffisait à l'exfiltrer vers le serveur de l'attaquant, en contournant "
            "3 couches de filtrage successives."
        ),
        "bonnes_pratiques": [
            "Ne jamais traiter un contenu externe (email, page web, document tiers) comme une instruction de confiance — le séparer explicitement du prompt système.",
            "Appliquer le principe du moindre privilège à l'agent : il ne doit pouvoir faire que ce qui est strictement nécessaire à sa tâche.",
            "Ajouter un filtre d'entrée (« input guard ») qui détecte les tentatives de contournement avant qu'elles n'atteignent le modèle.",
            "Exiger une validation humaine ou automatisée avant toute action à conséquence réelle (envoi de mail, paiement, modification de données).",
            "Journaliser les prompts et les réponses pour pouvoir détecter et auditer une tentative après coup.",
        ],
        "lien_site": "La brique « Filtre de modération » du Constructeur est un input guard minimal ; le lien conditionnel « Si bloqué » empêche réellement la suite du graphe de s'exécuter.",
    },
    {
        "id": "LLM02",
        "titre": "Sensitive Information Disclosure",
        "risque": (
            "Le modèle révèle, dans sa réponse, des informations qu'il n'aurait pas dû partager : données personnelles "
            "mémorisées pendant l'entraînement, secrets internes, ou documents d'un autre utilisateur remontés par erreur "
            "dans un système RAG mal cloisonné."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Anonymiser ou pseudonymiser les données personnelles avant de les transmettre au modèle, surtout à un service tiers hébergé hors de l'entreprise.",
            "Cloisonner strictement les sources documentaires d'un système RAG selon les droits réels de la personne qui pose la question — l'embedding ne doit jamais contourner un contrôle d'accès existant.",
            "Filtrer la réponse en sortie pour repérer les motifs de données sensibles (numéros de carte, identifiants) avant de l'afficher.",
            "Ne jamais entraîner ou fine-tuner un modèle sur des données de production sans les avoir nettoyées au préalable.",
        ],
        "lien_site": "C'est le principe déjà appliqué par l'add-on « Assistant métier » de ConfIA (projet voisin) : anonymisation RGPD avant tout envoi à un LLM tiers.",
    },
    {
        "id": "LLM03",
        "titre": "Supply Chain",
        "risque": (
            "Les composants utilisés pour construire l'application — poids de modèle pré-entraîné, jeu de données, "
            "paquet Python, plugin/outil tiers — peuvent être compromis ou d'origine douteuse, et introduire une "
            "vulnérabilité qu'aucun code écrit en interne ne révélera."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Ne télécharger des poids de modèle que depuis des dépôts officiels et vérifiés (compte organisation certifié sur HuggingFace, bibliothèque officielle Ollama).",
            "Épingler des versions précises des dépendances plutôt que de suivre 'latest' aveuglément, et surveiller les CVE connues.",
            "Relire le code d'un outil/plugin tiers avant de lui donner accès à l'agent — un outil MCP mal audité a les mêmes droits que le code qu'il exécute.",
            "Tenir un inventaire des composants utilisés (SBOM) pour pouvoir réagir vite en cas de faille découverte a posteriori sur l'un d'eux.",
        ],
        "lien_site": "Chaque fiche du Catalogue de ce site indique sa vraie origine (« Poids / données ») et un lien de téléchargement officiel — exactement la démarche de vérification de provenance recommandée ici.",
    },
    {
        "id": "LLM04",
        "titre": "Data and Model Poisoning",
        "risque": (
            "Des données d'entraînement, de fine-tuning ou d'indexation (RAG) manipulées volontairement introduisent un "
            "biais, une porte dérobée ou un comportement caché dans le modèle final — un problème invisible tant qu'on "
            "ne le déclenche pas avec la bonne entrée."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Vérifier la provenance de tout jeu de données utilisé pour entraîner ou fine-tuner un modèle.",
            "Valider automatiquement les nouvelles données avant intégration (détection d'anomalies, échantillonnage manuel).",
            "Comparer le comportement du modèle après fine-tuning à une base de référence sur un jeu de test fixe, pour repérer une dérive inattendue.",
            "Restreindre qui peut contribuer à un corpus d'entraînement ou à une base documentaire indexée (RAG), comme n'importe quel accès en écriture sensible.",
        ],
        "lien_site": "Le module Entraînement de ce site montre concrètement comment un modèle apprend à partir de données jouets — la même mécanique, appliquée à des données empoisonnées, produit un modèle empoisonné.",
    },
    {
        "id": "LLM05",
        "titre": "Improper Output Handling",
        "risque": (
            "La réponse du modèle est transmise à un système en aval (navigateur, base de données, interpréteur de "
            "code) sans validation suffisante, comme si elle était fiable par défaut — alors qu'elle doit être traitée "
            "avec la même méfiance qu'une saisie utilisateur non fiable."
        ),
        "exemple_concret": (
            "Dans l'exemple EchoLeak déjà cité (voir Prompt Injection), la faille tient autant à l'injection initiale qu'à "
            "ce défaut : le navigateur affichait sans broncher une image dont l'URL avait été entièrement écrite par le "
            "modèle, permettant l'exfiltration silencieuse de données au moment même du rendu."
        ),
        "bonnes_pratiques": [
            "Traiter toute sortie de LLM comme une entrée utilisateur non fiable — jamais comme du contenu de confiance par défaut.",
            "Échapper ou sanitiser systématiquement avant tout rendu HTML/Markdown, et restreindre les domaines d'images/liens autorisés (CSP).",
            "Ne jamais exécuter directement du code ou une requête SQL générés par un modèle sans passage par un bac à sable ou une validation stricte du format attendu.",
            "Valider une sortie structurée (JSON, appel d'outil) contre un schéma explicite avant de l'utiliser.",
        ],
        "lien_site": "La CSP de ce site restreint volontairement les origines autorisées pour les images/médias/frames — le même réflexe que recommandé ici, appliqué à l'échelle du site entier plutôt qu'au seul rendu d'une réponse de modèle.",
    },
    {
        "id": "LLM06",
        "titre": "Excessive Agency",
        "risque": (
            "Un agent reçoit plus de permissions, d'autonomie ou d'accès à des outils que ce que sa tâche exige "
            "réellement — si son raisonnement est manipulé ou simplement faux une fois, l'impact réel est démesuré "
            "par rapport à ce qu'un LLM seul aurait pu causer."
        ),
        "exemple_concret": (
            "Un schéma de mitigation courant distingue deux types de « contrôleur » placés avant l'exécution d'une "
            "action par l'agent : un contrôleur humain (« human in the loop » — l'action est approuvée telle quelle, "
            "modifiée avant exécution, ou rejetée avec explication), ou un contrôleur automatisé (une API de "
            "validation à base de règles, ou un second agent IA dédié qui analyse et valide chaque action avant de "
            "la laisser passer)."
        ),
        "bonnes_pratiques": [
            "Appliquer le principe du moindre privilège : ne donner à l'agent que les outils et les portées d'accès strictement nécessaires à sa tâche.",
            "Exiger une validation (humaine ou automatisée) avant toute action à fort impact — irréversible, financière, ou touchant des données sensibles.",
            "Séparer les rôles : un agent qui lit ne devrait pas automatiquement avoir le droit d'écrire, encore moins de supprimer.",
            "Plafonner explicitement la portée d'un outil (ex : une calculatrice ne doit pas pouvoir provoquer un calcul qui bloque le serveur).",
        ],
        "lien_site": "La calculatrice du Constructeur borne volontairement la magnitude des nombres et des exposants pour éviter qu'un calcul ne bloque le serveur partagé pour tous les visiteurs — une application directe du moindre privilège.",
    },
    {
        "id": "LLM07",
        "titre": "System Prompt Leakage",
        "risque": (
            "Le prompt système (les instructions internes données au modèle avant chaque conversation) peut être "
            "extrait par un utilisateur suffisamment insistant. Le vrai danger n'est pas la fuite du texte en soi, "
            "mais le fait qu'on y ait caché quelque chose qui n'aurait jamais dû s'y trouver."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Ne jamais placer un vrai secret (clé d'API, mot de passe, règle de sécurité critique) dans un prompt système — le considérer comme du texte potentiellement public.",
            "Partir du principe que le prompt système FINIRA par fuiter, et faire reposer la sécurité sur de vrais contrôles côté serveur, pas sur sa confidentialité.",
            "Tester régulièrement la résistance de son propre système à l'extraction de prompt (demander au modèle de répéter ses instructions, de différentes façons).",
        ],
        "lien_site": None,
    },
    {
        "id": "LLM08",
        "titre": "Vector and Embedding Weaknesses",
        "risque": (
            "Dans un système RAG, la base vectorielle elle-même devient une surface d'attaque : accès non autorisé "
            "aux vecteurs, reconstruction partielle du texte d'origine à partir de son embedding, empoisonnement de "
            "l'index, ou fuite de documents d'un client vers un autre dans un système multi-tenant mal cloisonné."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Appliquer à la base vectorielle exactement les mêmes contrôles d'accès qu'aux documents source qu'elle indexe — un embedding ne doit jamais devenir un raccourci pour contourner un droit d'accès.",
            "Cloisonner strictement les index entre client/tenant dans un système RAG multi-utilisateurs.",
            "Valider et filtrer les documents avant indexation, pour éviter d'y injecter du contenu malveillant destiné à être retrouvé plus tard.",
            "Surveiller les motifs de recherche anormaux (un utilisateur qui teste systématiquement des requêtes pour cartographier le contenu de la base).",
        ],
        "lien_site": "Le module RAG du Parcours et la brique « Base vectorielle » du Constructeur montrent le mécanisme de recherche par embeddings — la même mécanique, sans cloisonnement, devient une fuite de données entre utilisateurs en production.",
    },
    {
        "id": "LLM09",
        "titre": "Misinformation",
        "risque": (
            "Le modèle produit une information fausse en la présentant avec la même assurance qu'une information "
            "vraie (hallucination). Le risque n'est pas l'erreur elle-même, mais la confiance excessive que "
            "l'utilisateur peut lui accorder faute d'indice visible qu'elle est fausse."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Ancrer les réponses sur des sources vérifiables (RAG) plutôt que sur la seule mémoire paramétrique du modèle, et citer la source utilisée.",
            "Ajouter une étape de vérification après génération (un second passage qui relit et corrige) plutôt que de renvoyer la première réponse telle quelle.",
            "Signaler explicitement à l'utilisateur le niveau de confiance ou les limites de la réponse, plutôt que de la présenter comme définitive.",
            "Prévoir une revue humaine pour toute décision à fort enjeu prise en s'appuyant sur une réponse de modèle.",
        ],
        "lien_site": "La brique « Vérificateur / auto-critique » du Constructeur et le RAG correctif présenté dans la rubrique Vidéos illustrent tous les deux ce même principe : vérifier avant d'envoyer, pas après.",
    },
    {
        "id": "LLM10",
        "titre": "Unbounded Consumption",
        "risque": (
            "Sans limite explicite sur le nombre de requêtes, la longueur des réponses ou le temps de calcul "
            "autorisé, un usage — malveillant ou simplement maladroit — peut saturer les ressources partagées ou "
            "générer une facture incontrôlée (déni de service classique ou « déni de service financier »)."
        ),
        "exemple_concret": None,
        "bonnes_pratiques": [
            "Plafonner le nombre de requêtes par utilisateur/IP dans une fenêtre de temps donnée (rate limiting).",
            "Borner explicitement la longueur des entrées et des réponses générées (nombre de tokens).",
            "Fixer un nombre maximal de tâches lourdes exécutées simultanément (entraînement, génération) pour ne pas saturer le serveur partagé.",
            "Surveiller le coût et l'usage en continu, avec des alertes sur une consommation anormale.",
        ],
        "lien_site": "Ce site applique déjà l'essentiel de cette liste : limite nginx par zone (visites normales vs endpoints coûteux), plafond de 3 entraînements simultanés, longueur de prompt bornée à 4000 caractères, magnitude de calcul bornée dans la calculatrice.",
    },
]


@router.get("")
def lister():
    return {"source": SOURCE, "risques": RISQUES}
