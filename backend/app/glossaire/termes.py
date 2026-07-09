TERMES = [
    {
        "terme": "LLM (grand modèle de langage)",
        "categorie": "Général IA",
        "definition_simple": (
            "Un programme entraîné sur d'énormes quantités de texte, qui a appris à deviner le mot "
            "suivant le plus probable dans une phrase. C'est ce mécanisme, répété des milliers de fois, "
            "qui donne l'impression qu'il « comprend » et « répond »."
        ),
        "ou_le_voir": "Catalogue — llama3.2:3b, qwen2.5:7b-instruct",
    },
    {
        "terme": "Prompt",
        "categorie": "Général IA",
        "definition_simple": "Le texte qu'on envoie au modèle pour lui demander quelque chose — sa seule façon de recevoir une instruction.",
        "ou_le_voir": "Constructeur — champ « Prompt » de chaque brique",
    },
    {
        "terme": "Token",
        "categorie": "Général IA",
        "definition_simple": (
            "Le modèle ne lit pas des mots entiers mais des petits morceaux de texte (souvent une "
            "syllabe ou un mot court). Le prix et la vitesse d'un modèle se comptent en tokens, pas en mots."
        ),
        "ou_le_voir": None,
    },
    {
        "terme": "Hallucination",
        "categorie": "Général IA",
        "definition_simple": (
            "Une réponse inventée, présentée avec la même assurance qu'une réponse vraie. Le modèle ne "
            "« sait » pas qu'il se trompe : il génère toujours le mot le plus probable, vrai ou faux."
        ),
        "ou_le_voir": "Stratégie de tests — famille LLM génératif",
    },
    {
        "terme": "Fenêtre de contexte",
        "categorie": "Général IA",
        "definition_simple": "La quantité de texte (en tokens) que le modèle peut « garder en tête » en même temps pour répondre. Au-delà, il oublie le début.",
        "ou_le_voir": None,
    },
    {
        "terme": "Inférence",
        "categorie": "Général IA",
        "definition_simple": "Le moment où un modèle déjà entraîné produit une réponse. On dit « inférence » et pas « calcul » car le modèle ne sait rien avec certitude, il estime la réponse la plus probable.",
        "ou_le_voir": None,
    },
    {
        "terme": "Paramètres (d'un modèle)",
        "categorie": "Général IA",
        "definition_simple": (
            "Les millions ou milliards de « réglages internes » ajustés pendant l'entraînement. Plus il y "
            "en a, plus le modèle peut représenter de nuances — mais plus il est lourd et lent à faire tourner."
        ),
        "ou_le_voir": "Catalogue — champ « taille » de chaque modèle",
    },
    {
        "terme": "CPU vs GPU",
        "categorie": "Général IA",
        "definition_simple": (
            "Le GPU (carte graphique) calcule beaucoup d'opérations en parallèle et accélère énormément "
            "l'IA. Ce site tourne volontairement en CPU pur (sans GPU) pour rester simple à héberger soi-même."
        ),
        "ou_le_voir": None,
    },
    {
        "terme": "IA souveraine",
        "categorie": "Général IA",
        "definition_simple": (
            "Une IA qu'on héberge et qu'on contrôle soi-même (modèles open-source, serveur perso), plutôt "
            "que d'envoyer ses données à un service tiers dans le cloud. C'est le principe de ce site entier."
        ),
        "ou_le_voir": "Toute la plateforme iaeasy",
    },
    {
        "terme": "Embedding (vecteur)",
        "categorie": "Architecture / agents",
        "definition_simple": (
            "Une façon de transformer un texte en une liste de nombres qui capture son SENS. Deux textes "
            "au sens proche ont des listes de nombres proches, même s'ils n'ont aucun mot en commun."
        ),
        "ou_le_voir": "Catalogue — famille Embeddings ; Constructeur — brique Base vectorielle",
    },
    {
        "terme": "Similarité cosinus",
        "categorie": "Architecture / agents",
        "definition_simple": "La formule mathématique qui mesure à quel point deux vecteurs (deux embeddings) « pointent dans la même direction » — c'est ce score qui dit si deux textes se ressemblent en sens.",
        "ou_le_voir": "Constructeur — brique Base vectorielle",
    },
    {
        "terme": "RAG (Retrieval Augmented Generation)",
        "categorie": "Architecture / agents",
        "definition_simple": (
            "Au lieu de faire confiance uniquement à la mémoire du modèle, on va d'abord chercher les "
            "passages pertinents dans de vrais documents, puis on les donne au modèle avant qu'il réponde. "
            "Réduit fortement le risque d'hallucination."
        ),
        "ou_le_voir": "Constructeur — templates « Assistant RAG documentaire », « RAG simplifié »",
    },
    {
        "terme": "Chunking (découpage)",
        "categorie": "Architecture / agents",
        "definition_simple": "Couper un long document en petits morceaux avant de le comparer à une question — un document entier est trop gros pour être comparé efficacement d'un coup.",
        "ou_le_voir": "Constructeur — brique Découpage (chunking)",
    },
    {
        "terme": "Agent (IA agentique)",
        "categorie": "Architecture / agents",
        "definition_simple": "Un LLM à qui on donne la possibilité d'utiliser des outils (calculatrice, recherche...) et qui décide lui-même, étape par étape, ce qu'il doit faire pour répondre.",
        "ou_le_voir": "Constructeur — brique Agent (boucle ReAct)",
    },
    {
        "terme": "ReAct (Reason + Act)",
        "categorie": "Architecture / agents",
        "definition_simple": "Le principe derrière la plupart des agents IA : le modèle alterne des étapes de raisonnement (« que dois-je faire ? ») et d'action (appeler un outil), jusqu'à pouvoir répondre.",
        "ou_le_voir": "Constructeur — brique Agent (boucle ReAct)",
    },
    {
        "terme": "Multi-agent",
        "categorie": "Architecture / agents",
        "definition_simple": "Plusieurs agents spécialisés qui collaborent en séquence (ex : un « chercheur » qui rassemble les faits, un « rédacteur » qui les met en forme) plutôt qu'un seul agent qui fait tout.",
        "ou_le_voir": "Constructeur — brique Pipeline multi-agent",
    },
    {
        "terme": "MCP (Model Context Protocol)",
        "categorie": "Architecture / agents",
        "definition_simple": "Un standard qui définit comment un modèle IA appelle des outils et des sources de données externes de façon homogène, plutôt que chaque fournisseur ait son propre système incompatible.",
        "ou_le_voir": "Constructeur — brique Outil / MCP",
    },
    {
        "terme": "Modération (filtre de contenu)",
        "categorie": "Architecture / agents",
        "definition_simple": "Une vérification de la requête avant même d'appeler le modèle, pour bloquer les demandes inappropriées sans dépenser un appel IA inutile.",
        "ou_le_voir": "Constructeur — brique Filtre de modération",
    },
    {
        "terme": "Vérificateur / auto-critique",
        "categorie": "Architecture / agents",
        "definition_simple": "Le modèle génère une première réponse, puis un second appel la relit et la corrige si besoin — une façon simple d'améliorer la fiabilité sur les tâches à risque d'erreur (calculs, faits précis).",
        "ou_le_voir": "Constructeur — brique Vérificateur / auto-critique",
    },
    {
        "terme": "Entraînement (fine-tuning)",
        "categorie": "Entraînement",
        "definition_simple": "Ajuster un modèle déjà existant sur un petit jeu de données spécifique, plutôt que de tout ré-apprendre depuis zéro — beaucoup plus rapide et moins coûteux.",
        "ou_le_voir": "Module Entraînement — les 3 scénarios",
    },
    {
        "terme": "Loss (perte)",
        "categorie": "Entraînement",
        "definition_simple": "Un chiffre qui mesure à quel point le modèle se trompe pendant l'entraînement. Plus il descend, mieux le modèle apprend — s'il stagne ou oscille, quelque chose ne va pas.",
        "ou_le_voir": "Module Entraînement — courbe affichée en direct",
    },
    {
        "terme": "Epoch",
        "categorie": "Entraînement",
        "definition_simple": "Un passage complet sur l'ensemble des données d'entraînement. On répète souvent plusieurs epochs pour que le modèle ait le temps de bien apprendre.",
        "ou_le_voir": "Module Entraînement",
    },
    {
        "terme": "Taux d'apprentissage (learning rate)",
        "categorie": "Entraînement",
        "definition_simple": (
            "La taille des pas que le modèle fait à chaque correction pendant l'entraînement. Trop grand, "
            "il peut « rater » la bonne solution en oscillant ; trop petit, il apprend trop lentement."
        ),
        "ou_le_voir": "Module Entraînement — scénario sentiment (bug réel corrigé sur ce site)",
    },
    {
        "terme": "Surapprentissage (overfitting)",
        "categorie": "Entraînement",
        "definition_simple": "Quand un modèle apprend « par cœur » ses exemples d'entraînement au lieu de comprendre la logique générale — il devient très bon sur ces exemples précis, mais mauvais sur des cas nouveaux.",
        "ou_le_voir": None,
    },
    {
        "terme": "Classification",
        "categorie": "Entraînement",
        "definition_simple": "Faire ranger par un modèle chaque exemple dans une catégorie prédéfinie (spam/légitime, positif/négatif...), plutôt que générer du texte libre.",
        "ou_le_voir": "Module Entraînement — scénarios sentiment et spam",
    },
    {
        "terme": "Régression",
        "categorie": "Entraînement",
        "definition_simple": "Faire prédire à un modèle une valeur numérique continue (un prix, un chiffre d'affaires) plutôt qu'une catégorie fixe.",
        "ou_le_voir": "Module Entraînement — scénario prévision de CA",
    },
    {
        "terme": "Détection d'anomalie",
        "categorie": "Général IA",
        "definition_simple": "Repérer automatiquement une valeur qui sort de la normale (une transaction suspecte, une machine qui vibre anormalement), sans avoir défini de règle fixe à l'avance.",
        "ou_le_voir": "Catalogue — Isolation Forest (fraude, maintenance)",
    },
    {
        "terme": "Extraction d'entités (NER)",
        "categorie": "Général IA",
        "definition_simple": "Repérer automatiquement dans un texte les noms de personnes, de lieux ou d'organisations, pour les extraire sans avoir à les relire soi-même.",
        "ou_le_voir": "Catalogue — CamemBERT NER",
    },
    {
        "terme": "Biais algorithmique",
        "categorie": "Général IA",
        "definition_simple": "Quand un modèle reproduit ou amplifie, sans le vouloir, un déséquilibre présent dans ses données d'entraînement (ex : moins fiable sur un sous-groupe de la population que sur un autre).",
        "ou_le_voir": "Stratégie de tests — famille Classification classique",
    },
 {'terme': 'LLM génératif',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier que le modèle reste cohérent, factuellement correct et suit bien les '
                      'instructions — sans se fier uniquement à la fluidité apparente de sa réponse.',
 'ou_le_voir': 'Catalogue — 7 modèles de cette famille'},
 {'terme': 'Embeddings',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier que la similarité mesurée reflète vraiment le SENS des phrases, et pas '
                      "seulement les mots qu'elles ont en commun.",
 'ou_le_voir': 'Catalogue — Nomic Embed Text, Mxbai Embed Large, All-MiniLM'},
 {'terme': 'Classification de texte',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier la précision sur des cas clairs ET la robustesse sur des cas ambigus ou dont '
                      "la forme diffère de celle des données d'entraînement.",
 'ou_le_voir': 'Catalogue — CamemBERT (sentiment FR)'},
 {'terme': 'Traduction',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier la fidélité du sens, la fluidité, et la gestion du vocabulaire technique '
                      'métier.',
 'ou_le_voir': 'Catalogue — Helsinki-NLP OPUS-MT (FR→EN)'},
 {'terme': 'Résumé automatique',
 'categorie': 'Famille de modèle',
 'definition_simple': "Vérifier la fidélité (pas d'invention), la concision, et la conservation des éléments "
                      'factuels précis.',
 'ou_le_voir': 'Catalogue — T5 (résumé automatique FR)'},
 {'terme': 'Question-réponse extractive',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier que la réponse est un extrait EXACT et correct du contexte fourni — jamais '
                      'inventée.',
 'ou_le_voir': 'Catalogue — CamemBERT Question-Réponse'},
 {'terme': 'Détection de langue',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier la robustesse sur les textes courts et les langues proches.',
 'ou_le_voir': 'Catalogue — py3langid — détection de langue'},
 {'terme': "Détection d'objets (vision)",
 'categorie': 'Famille de modèle',
 'definition_simple': 'Détecter tous les objets pertinents (rappel) sans en inventer (précision), et rester '
                      'robuste aux conditions réelles (angle, luminosité, occlusion).',
 'ou_le_voir': 'Catalogue — YOLOv8 (détection, nano), YOLOv8 (détection, small)'},
 {'terme': "Classification d'image",
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier si la bonne catégorie ressort en top-1, ou au moins dans le top-5.',
 'ou_le_voir': 'Catalogue — YOLOv8 (classification, nano), YOLOv8 (classification, small)'},
 {'terme': 'Transcription audio',
 'categorie': 'Famille de modèle',
 'definition_simple': "Vérifier l'exactitude du texte transcrit (taux d'erreur de mots) et la robustesse au "
                      "bruit et à l'accent.",
 'ou_le_voir': 'Catalogue — Whisper Tiny'},
 {'terme': 'Prévision de séries temporelles',
 'categorie': 'Famille de modèle',
 'definition_simple': "Vérifier la qualité de la prévision et la fiabilité de l'intervalle de confiance "
                      'associé.',
 'ou_le_voir': 'Catalogue — Chronos Bolt (tiny)'},
 {'terme': 'Classification classique (algorithmes traditionnels)',
 'categorie': 'Famille de modèle',
 'definition_simple': "Vérifier la précision globale, mais aussi l'explicabilité (quelle variable pèse dans "
                      'la décision).',
 'ou_le_voir': 'Catalogue — Régression logistique — scoring crédit, Arbre de décision — scoring prêt '
               'immobilier'},
 {'terme': 'Recommandation',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier la pertinence des recommandations, leur diversité, et la gestion des '
                      'nouveaux utilisateurs/produits sans historique.',
 'ou_le_voir': 'Catalogue — Factorisation de matrice (NMF) — recommandation, Factorisation de matrice (NMF) '
               '— matériaux artisan'},
 {'terme': "Segmentation d'image (vision)",
 'categorie': 'Famille de modèle',
 'definition_simple': 'Il faut vérifier non seulement que le bon objet est détecté (comme en détection '
                      'classique), mais que le contour du masque colle précisément aux bords réels de '
                      "l'objet — car toute imprécision de quelques pixels sur le pourtour fausse directement "
                      'un calcul de surface (toiture, parcelle, zone à peindre).',
 'ou_le_voir': 'Catalogue — YOLOv8 (segmentation)'},
 {'terme': 'Estimation de pose (vision)',
 'categorie': 'Famille de modèle',
 'definition_simple': "Pour l'estimation de pose, il ne suffit pas de vérifier qu'une personne est détectée "
                      ': il faut vérifier la précision et la stabilité de la localisation de chaque point '
                      'clé (épaules, coudes, genoux...), et surtout la robustesse du modèle face aux '
                      "occlusions et aux chevauchements entre personnes. Le cas d'usage sécurité le plus "
                      'important - la chute au sol - est souvent le moins bien couvert par les données '
                      "d'entraînement standard, il mérite donc une attention particulière.",
 'ou_le_voir': 'Catalogue — YOLOv8 (estimation de pose)'},
 {'terme': 'Clustering non supervisé',
 'categorie': 'Famille de modèle',
 'definition_simple': "Contrairement à la classification, il n'existe aucune étiquette de référence à "
                      'comparer : on ne peut pas mesurer un taux de bonnes réponses. Il faut donc vérifier '
                      'la cohérence géométrique des groupes formés (compacité, séparation), leur stabilité '
                      "quand on relance l'algorithme, et leur sensibilité au choix du nombre K et à "
                      "l'échelle des variables.",
 'ou_le_voir': 'Catalogue — KMeans — segmentation de clientèle'},
 {'terme': "Recherche d'image par similarité",
 'categorie': 'Famille de modèle',
 'definition_simple': 'Vérifier que le score de similarité reflète une vraie ressemblance de contenu ou de '
                      'style (même objet, même type de bien, même ambiance) et non un artefact superficiel '
                      'comme une couleur dominante ou un fond similaire par hasard.',
 'ou_le_voir': 'Catalogue — ResNet-18 — similarité visuelle'},
 {'terme': 'Reconnaissance de texte (OCR)',
 'categorie': 'Famille de modèle',
 'definition_simple': "Vérifier l'exactitude caractère par caractère du texte extrait, pas seulement une "
                      'impression générale de lisibilité : un OCR utilisé en comptabilité doit être jugé sur '
                      'sa capacité à restituer exactement les montants, dates et références, où une seule '
                      'confusion de caractère change le sens du document.',
 'ou_le_voir': 'Catalogue — Tesseract OCR'},
 {'terme': 'Synthèse vocale (texte vers audio)',
 'categorie': 'Famille de modèle',
 'definition_simple': 'Pour un moteur à règles phonétiques comme eSpeak NG, il faut vérifier que le texte '
                      'est correctement transformé en sons prononçables et compréhensibles (nombres, sigles, '
                      'noms propres, ponctuation), pas juger la qualité audio ou le naturel de la voix comme '
                      'on le ferait pour un moteur neuronal.',
 'ou_le_voir': 'Catalogue — eSpeak NG — synthèse vocale'},
 {'terme': 'Llama 3.2 (3B)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle de langage génératif : il prédit le mot suivant, un par un, à partir de '
                      'tout le texte déjà écrit avant lui. Sa taille réduite (3B) le rend rapide même sans '
                      "carte graphique, au prix d'un raisonnement moins fin qu'un très gros modèle.",
 'ou_le_voir': 'Catalogue — Généraliste (LLM génératif)'},
 {'terme': 'Qwen 2.5 Instruct (7B)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Même famille de modèle que Llama (génératif, mot par mot), mais plus gros : il suit '
                      "mieux des instructions précises et enchaîne plusieurs étapes de raisonnement. C'est "
                      'aussi le modèle utilisé plus loin pour la brique "agent" (il sait appeler des '
                      'outils).',
 'ou_le_voir': 'Catalogue — Raisonnement / généraliste renforcé (LLM génératif)'},
 {'terme': 'DeepSeek Coder (6.7B)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle génératif spécialisé : entraîné en majorité sur du code source plutôt que '
                      'sur du texte généraliste. Il illustre l\'idée de "spécialisation par les données '
                      'd\'entraînement" plutôt que par l\'architecture elle-même.',
 'ou_le_voir': 'Catalogue — Code / développement (LLM génératif)'},
 {'terme': 'Nomic Embed Text',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Ce modèle ne génère pas de texte : il transforme une phrase en une liste de nombres '
                      '(un "vecteur") qui capture son sens. Deux phrases proches en sens ont des vecteurs '
                      "proches. C'est la brique de base de la recherche sémantique et du RAG (module 3).",
 'ou_le_voir': 'Catalogue — Recherche sémantique / RAG (Embeddings)'},
 {'terme': 'Mxbai Embed Large',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Le même principe que Nomic Embed (transformer une phrase en vecteur), mais un modèle '
                      'différent et plus gros. En comparant les deux sur la même paire de phrases, on voit '
                      "que deux modèles d'embeddings ne donnent pas exactement le même score de similarité — "
                      'il n\'existe pas "un seul bon vecteur", chaque modèle a appris sa propre '
                      'représentation.',
 'ou_le_voir': 'Catalogue — Recherche sémantique (comparatif) (Embeddings)'},
 {'terme': 'CamemBERT (sentiment FR)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Contrairement aux modèles génératifs, un encodeur comme CamemBERT ne "rédige" rien : '
                      'il lit un texte en entier puis rend une seule étiquette (ici une note de 1 à 5 '
                      "étoiles). Modèle souverain français (Inria/CNRS), beaucoup plus rapide et léger qu'un "
                      'LLM pour cette tâche précise — utile pour trier des avis clients ou des réclamations '
                      "d'assurance.",
 'ou_le_voir': 'Catalogue — Assurance / Banque — analyse de retours clients (Classification de texte)'},
 {'terme': 'Helsinki-NLP OPUS-MT (FR→EN)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle de traduction dédié à une seule paire de langues (français vers anglais). '
                      "Beaucoup plus petit et rapide qu'un LLM généraliste utilisé pour traduire, car il n'a "
                      "qu'une seule tâche à apprendre.",
 'ou_le_voir': 'Catalogue — International / export (Traduction)'},
 {'terme': 'T5 (résumé automatique FR)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Comme la traduction, le résumé est une tâche "texte vers texte" : le modèle lit un '
                      "texte long et en génère un plus court qui garde l'essentiel. Ce modèle est un T5 "
                      "(même famille d'architecture que beaucoup de LLM actuels) fine-tuné spécifiquement "
                      'sur des articles de presse français pour cette tâche.',
 'ou_le_voir': 'Catalogue — Presse / veille documentaire (Résumé automatique)'},
 {'terme': 'CamemBERT NER',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Un encodeur spécialisé dans la reconnaissance d'entités nommées (NER) : il repère et "
                      'catégorise les personnes, lieux, organisations et dates dans un texte, sans jamais '
                      "rien générer. Utile pour extraire automatiquement des informations structurées d'un "
                      "contrat, d'un CV ou d'un compte-rendu.",
 'ou_le_voir': "Catalogue — Juridique / RH — extraction d'informations (Extraction d'entités (NER))"},
 {'terme': 'CamemBERT Question-Réponse',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle de question-réponse extractive : il ne invente pas de réponse, il repère le '
                      "passage exact d'un texte de référence qui répond à la question posée. Très différent "
                      "d'un LLM qui, lui, reformule et peut inventer — ici la réponse est toujours un "
                      'extrait vérifiable du contexte fourni.',
 'ou_le_voir': 'Catalogue — Support client / documentation (Question-réponse extractive)'},
 {'terme': 'py3langid — détection de langue',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'L\'exemple parfait qu\'"IA" ne veut pas dire "gros modèle génératif" : ce modèle '
                      'tient en quelques mégaoctets et répond en quelques millisecondes. Il sert à détecter '
                      "la langue d'un texte, une brique utile avant de router vers le bon modèle spécialisé.",
 'ou_le_voir': 'Catalogue — Modération / routage multilingue (Détection de langue)'},
 {'terme': 'YOLOv8 (détection, nano)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle de vision par ordinateur : il ne lit pas du texte mais une image, et '
                      'localise des objets avec un rectangle (bounding box) + une étiquette. Base des usages '
                      '"drone" (repérage de personnes/véhicules) ou "agriculture" (comptage, détection sur '
                      'une parcelle).',
 'ou_le_voir': "Catalogue — Agriculture / Drone — détection depuis une vue aérienne (Détection d'objets "
               '(vision))'},
 {'terme': 'YOLOv8 (classification, nano)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Même famille d'algorithme que YOLOv8 détection, mais une tâche différente : ici le "
                      "modèle ne localise rien, il attribue une seule étiquette à l'image entière. C'est la "
                      'distinction "détection" (où sont les objets ?) vs "classification" (à quoi ressemble '
                      'cette image ?) — deux tâches de vision très différentes en pratique.',
 'ou_le_voir': "Catalogue — Agriculture — identification visuelle (Classification d'image)"},
 {'terme': 'Whisper Tiny',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Premier modèle du catalogue qui ne lit ni texte ni image mais du son : il transforme '
                      "un signal audio en texte. Base des usages de transcription d'appels ou de messages "
                      "vocaux pour un service client, avant d'enchaîner avec un modèle de classification ou "
                      'un LLM sur le texte obtenu.',
 'ou_le_voir': "Catalogue — Service client — transcription d'appels et messages vocaux (Transcription audio)"},
 {'terme': 'Chronos Bolt (tiny)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Ici le modèle ne manipule ni texte ni image mais une courbe de chiffres dans le temps '
                      "(ex. chiffre d'affaires mensuel) : il apprend le motif de la courbe pour prédire les "
                      'valeurs suivantes. Bon exemple qu\'un "modèle" peut être un tout autre type de '
                      'prédicteur.',
 'ou_le_voir': 'Catalogue — Économie / Finance — prévision (Prévision de séries temporelles)'},
 {'terme': 'Isolation Forest — maintenance',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Il n\'existe pas de modèle "mécanique" pré-entraîné universel : le vrai cas d\'usage '
                      "terrain (maintenance prédictive) s'apprend sur les données spécifiques d'une machine. "
                      "Ce modèle s'entraîne donc en direct, sous vos yeux, sur des données de capteurs "
                      'jouets — pont naturel vers le module 2 (entraînement).',
 'ou_le_voir': "Catalogue — Mécanique — maintenance prédictive (Détection d'anomalie)"},
 {'terme': 'Isolation Forest — fraude bancaire',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Le même algorithme que pour la maintenance mécanique, mais appliqué à un historique '
                      "de montants de transactions bancaires : preuve qu'un même type de modèle (détection "
                      "d'anomalie) sert des secteurs très différents dès lors qu'on lui donne les bonnes "
                      "données d'entraînement.",
 'ou_le_voir': "Catalogue — Banque — détection de fraude transactionnelle (Détection d'anomalie)"},
 {'terme': 'Régression logistique — scoring crédit',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un algorithme de classification "classique" (pas un réseau de neurones) : il apprend '
                      'une frontière simple entre dossiers à risque et dossiers sains à partir de quelques '
                      "variables chiffrées. Beaucoup plus interprétable qu'un LLM — on peut dire précisément "
                      'quelle variable a pesé dans la décision.',
 'ou_le_voir': 'Catalogue — Banque / Assurance — scoring de risque (Classification classique (algorithmes '
               'traditionnels))'},
 {'terme': 'Factorisation de matrice (NMF) — recommandation',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Un système de recommandation n'est pas toujours un LLM : ici, un algorithme de "
                      'factorisation de matrice apprend les goûts de chaque utilisateur à partir de ses '
                      "notes passées, et devine celles qu'il n'a pas encore données — le principe derrière "
                      '"les utilisateurs qui ont aimé X ont aussi aimé Y".',
 'ou_le_voir': 'Catalogue — E-commerce / Streaming — recommandation (Recommandation)'},
 {'terme': 'Llama 3 (8B)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Le grand frère de Llama 3.2 (3B) : même famille de modèle, plus de paramètres. À '
                      "poser la même question aux deux pour comparer directement l'effet de la taille sur la "
                      'qualité de réponse — voir aussi le Simulateur coût/latence pour comparer leur '
                      'vitesse.',
 'ou_le_voir': 'Catalogue — Généraliste (comparatif de taille) (LLM génératif)'},
 {'terme': 'Mistral 7B Instruct',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Encore un modèle génératif de taille comparable à Qwen 2.5 (7B), mais d'un éditeur et "
                      "d'un entraînement différents — la meilleure preuve qu'à taille équivalente, deux "
                      'modèles ne répondent jamais exactement pareil à la même question. Bon candidat pour '
                      'le Simulateur coût/latence en complément des trois modèles déjà comparés.',
 'ou_le_voir': 'Catalogue — Généraliste (comparatif) (LLM génératif)'},
 {'terme': 'Gemma 2 (2B)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle de Google, plus petit encore que Llama 3.2 (3B) : bon exemple pour voir '
                      'qu\'un modèle "léger" reste tout à fait utilisable en pratique sur des tâches '
                      "simples, avec une vitesse de réponse encore meilleure — au prix de plus d'erreurs sur "
                      'les raisonnements longs.',
 'ou_le_voir': 'Catalogue — Généraliste — modèle très léger (LLM génératif)'},
 {'terme': 'Phi-3 Mini',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un modèle de Microsoft entraîné sur des données très sélectionnées plutôt que sur un '
                      "immense volume brut — preuve qu'un choix rigoureux des données d'entraînement peut "
                      'compenser en partie une taille plus petite, une autre façon de penser la '
                      '"spécialisation" qu\'un simple nombre de paramètres.',
 'ou_le_voir': 'Catalogue — Généraliste — modèle compact orienté raisonnement (LLM génératif)'},
 {'terme': 'All-MiniLM',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Le plus petit modèle d'embeddings du catalogue — à comparer avec Nomic Embed (137M) "
                      'et Mxbai Embed (335M) sur la même paire de phrases : un score de similarité correct '
                      'ne nécessite pas forcément un gros modèle, mais la finesse de la représentation peut '
                      'varier sur des cas plus subtils.',
 'ou_le_voir': 'Catalogue — Recherche sémantique (le plus petit du catalogue) (Embeddings)'},
 {'terme': 'YOLOv8 (détection, small)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'La version "small" du même YOLOv8 nano vu plus haut — presque 4 fois plus de '
                      "paramètres. À essayer sur la même image d'exemple pour voir concrètement si la "
                      'détection change (objets supplémentaires détectés, confiance différente).',
 'ou_le_voir': "Catalogue — Agriculture / Drone — comparatif de taille (Détection d'objets (vision))"},
 {'terme': 'YOLOv8 (classification, small)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'La version "small" du classifieur YOLOv8 nano vu plus haut. Comparer le top-1 des '
                      "deux tailles sur la même image d'exemple montre qu'un plus gros modèle peut changer "
                      'la catégorie prédite, pas seulement affiner un peu le score.',
 'ou_le_voir': "Catalogue — Agriculture — comparatif de taille (Classification d'image)"},
 {'terme': 'Isolation Forest — four industriel',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Un troisième secteur pour le même algorithme de détection d'anomalie (après la "
                      "mécanique et la fraude bancaire) : la température d'un four industriel. Confirme "
                      "qu'un même type de modèle se transpose à des données très différentes, tant que le "
                      'signal (une mesure qui varie dans le temps) a la même forme statistique.',
 'ou_le_voir': "Catalogue — Industrie — surveillance de four (Détection d'anomalie)"},
 {'terme': 'Arbre de décision — scoring prêt immobilier',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Un autre algorithme "classique" que la régression logistique du scoring crédit : un '
                      'arbre de décision. Sa décision se lit comme une suite de questions simples (ex : '
                      'apport &lt; 10% ET durée &gt; 25 ans → refus), encore plus directement explicable '
                      "qu'une régression logistique.",
 'ou_le_voir': 'Catalogue — Banque — crédit immobilier (Classification classique (algorithmes '
               'traditionnels))'},
 {'terme': 'Factorisation de matrice (NMF) — matériaux artisan',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Le même algorithme que la recommandation de films, appliqué cette fois aux '
                      "préférences de matériaux d'un artisan à partir de ses chantiers passés — la "
                      'recommandation ne se limite pas au e-commerce grand public.',
 'ou_le_voir': 'Catalogue — BTP — recommandation de matériaux (Recommandation)'},
 {'terme': 'YOLOv8 (segmentation)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "Contrairement à la détection (un simple rectangle autour de l'objet), la segmentation "
                      "délimite le contour exact de chaque objet, pixel par pixel. Utile dès qu'on a besoin "
                      'de mesurer une surface réelle (une toiture, une parcelle) plutôt que juste repérer '
                      'une présence.',
 'ou_le_voir': "Catalogue — BTP / Agriculture — mesure de surface (Segmentation d'image (vision))"},
 {'terme': 'YOLOv8 (estimation de pose)',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Une tâche de vision différente de la détection ou la classification : repérer les '
                      'points clés du corps humain (épaules, coudes, genoux...). Base de nombreux usages de '
                      'sécurité au travail (détecter une chute, une position à risque) ou de sport.',
 'ou_le_voir': 'Catalogue — BTP / Industrie — sécurité au travail (Estimation de pose (vision))'},
 {'terme': 'KMeans — segmentation de clientèle',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Différence fondamentale avec le scoring crédit ou la classification classique : ici '
                      "aucune étiquette n'est fournie au modèle. Il découvre lui-même des groupes de clients "
                      "cohérents à partir de leurs seules habitudes (montant moyen, fréquence), sans qu'on "
                      "lui dise à l'avance ce que ces groupes représentent.",
 'ou_le_voir': 'Catalogue — Artisanat — segmentation de clientèle (Clustering non supervisé)'},
 {'terme': 'ResNet-18 — similarité visuelle',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "L'équivalent visuel des embeddings de texte (module Embeddings) : chaque image est "
                      'transformée en un vecteur de nombres qui capture son contenu visuel, ce qui permet de '
                      'comparer deux images par leur sens plutôt que pixel par pixel — base de la recherche '
                      'd\'image ("trouver des produits similaires à cette photo").',
 'ou_le_voir': "Catalogue — E-commerce / Immobilier — recherche visuelle (Recherche d'image par similarité)"},
 {'terme': 'Tesseract OCR',
 'categorie': 'Modèle du catalogue',
 'definition_simple': 'Extraire le texte contenu dans une image (une facture scannée, une photo de document) '
                      "plutôt que de le taper à la main. Un moteur mature et éprouvé plutôt qu'un tout "
                      "nouveau modèle — bon rappel que beaucoup d'IA utile au quotidien n'est pas un LLM.",
 'ou_le_voir': 'Catalogue — Comptabilité / Administratif — numérisation de documents (Reconnaissance de '
               'texte (OCR))'},
 {'terme': 'eSpeak NG — synthèse vocale',
 'categorie': 'Modèle du catalogue',
 'definition_simple': "L'inverse de Whisper (texte → son au lieu de son → texte). Ce moteur classique "
                      '(règles phonétiques codées à la main) est très léger et rapide, avec une voix '
                      "nettement plus robotique qu'un moteur neuronal moderne — bon exemple pour discuter du "
                      'compromis légèreté/qualité, au-delà du seul cas des LLM.',
 'ou_le_voir': 'Catalogue — Accessibilité — lecture à voix haute (Synthèse vocale (texte vers audio))'},
]


def get_termes() -> list[dict]:
    return TERMES
