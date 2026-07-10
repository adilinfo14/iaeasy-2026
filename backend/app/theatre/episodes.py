# Les décors sont une liste FERMÉE (allowlist) : le frontend a un thème CSS/SVG précis pour
# chacun d'eux. Un épisode généré par l'IA (voir router.py) doit obligatoirement piocher dedans —
# jamais un id inventé, qui n'aurait aucun rendu visuel prévu.
DECORS = [
    "plaine_venteuse",
    "chantier_urbain",
    "siege_medieval",
    "espace_etoiles",
    "ville_medievale_sombre",
    "temple_antique",
    "ocean_exploration",
    "revolution_industrielle",
]

# Émotion par réplique — change réellement l'expression du personnage qui parle (sourcils,
# bouche au repos) plutôt qu'une simple animation de "parole" identique pour toute la scène.
EMOTIONS = ["neutre", "surprise", "joyeux", "triste", "inquiet"]

PERSONNAGES = {
    "clio": {"nom": "Clio", "role": "la curieuse — pose les questions, s'étonne, s'inquiète"},
    "marco": {"nom": "Marco", "role": "le conteur — sait, explique, dramatise avec plaisir"},
}

# 5 épisodes rédigés à la main : contenu garanti (aucun risque d'hallucination), pensé pour
# montrer la palette complète des décors dès le premier chargement de la page. Le bouton
# "Nouvelle histoire" (voir router.py:generer) complète cette liste avec des épisodes générés en
# direct par un modèle Ollama, pour la variété — mais la qualité de base ne dépend jamais de lui.
EPISODES: list[dict] = [
    {
        "id": "wright",
        "titre": "Le premier vol des frères Wright",
        "annee": "1903",
        "scenes": [
            {
                "decor": "plaine_venteuse",
                "repliques": [
                    {"personnage": "clio", "emotion": "surprise", "texte": "Marco, pourquoi sommes-nous plantés au milieu de nulle part, sur cette plage balayée par le vent ?"},
                    {"personnage": "marco", "emotion": "neutre", "texte": "Kitty Hawk, en Caroline du Nord. Le 17 décembre 1903. Le vent y souffle presque toujours à la même vitesse — parfait pour ce qu'Orville et Wilbur Wright s'apprêtent à tenter."},
                    {"personnage": "clio", "emotion": "surprise", "texte": "Deux frères qui réparaient des vélos, non ? Qu'est-ce qui leur donne l'idée de voler ?"},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "Justement : des mécaniciens, pas des rêveurs. Ils ont passé trois ans à tester des ailes dans une soufflerie qu'ils ont eux-mêmes bricolée, à corriger chaque calcul faux des pionniers avant eux."},
                ],
            },
            {
                "decor": "plaine_venteuse",
                "repliques": [
                    {"personnage": "clio", "emotion": "surprise", "texte": "Regarde ! L'engin de toile et de bois avance sur son rail... il décolle !"},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "Douze secondes. Trente-six mètres. Orville est allongé à plat ventre aux commandes, le moteur crachote — et pourtant, c'est fait : un vol motorisé, contrôlé, plus lourd que l'air."},
                    {"personnage": "clio", "emotion": "neutre", "texte": "Trente-six mètres, c'est presque rien !"},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "C'est moins long que l'envergure d'un avion de ligne aujourd'hui. Mais ce jour-là, sur cette plage, cinq témoins seulement regardent naître tout le vingtième siècle du transport."},
                ],
            },
        ],
    },
    {
        "id": "tour-eiffel",
        "titre": "La tour qui devait être démontée",
        "annee": "1889",
        "scenes": [
            {
                "decor": "chantier_urbain",
                "repliques": [
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Ce squelette de fer qui grandit au-dessus de Paris... les gens l'aiment vraiment ?"},
                    {"personnage": "marco", "emotion": "surprise", "texte": "Pas du tout, au début ! En 1887, trois cents artistes et écrivains — Maupassant en tête — signent une pétition contre cette \"tour de fer\" qui, selon eux, va défigurer la capitale."},
                    {"personnage": "clio", "emotion": "neutre", "texte": "Et Gustave Eiffel, qu'est-ce qu'il répond ?"},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "Il construit. Deux ans, deux mois, cinq jours : ses ouvriers assemblent plus de dix-huit mille pièces de métal, rivetées une par une, sans qu'un seul ne meure sur le chantier — un exploit pour l'époque."},
                ],
            },
            {
                "decor": "chantier_urbain",
                "repliques": [
                    {"personnage": "clio", "emotion": "surprise", "texte": "Trois cents mètres de haut... personne n'a jamais construit aussi haut ?"},
                    {"personnage": "marco", "emotion": "neutre", "texte": "Elle devient le plus haut édifice du monde, et le restera quarante et un ans. Elle n'a même été conçue que pour dix ans — une simple attraction pour l'Exposition universelle de 1889, ensuite promise à la démolition."},
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Alors pourquoi est-elle toujours debout ?"},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "Une antenne. On y installe la radio militaire, puis la télévision. La tour qu'on voulait raser est devenue trop utile pour disparaître — et, entre-temps, tout le monde avait fini par l'aimer."},
                ],
            },
        ],
    },
    {
        "id": "constantinople",
        "titre": "La chute de Constantinople",
        "annee": "1453",
        "scenes": [
            {
                "decor": "siege_medieval",
                "repliques": [
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Ces murailles sont immenses, Marco. Comment une ville peut-elle tomber derrière des remparts pareils ?"},
                    {"personnage": "marco", "emotion": "inquiet", "texte": "Les murailles théodosiennes tiennent depuis mille ans, Clio. Mais le sultan Mehmed II, vingt et un ans à peine, a fait fondre un canon géant, conçu par un ingénieur hongrois nommé Orban — capable de tirer un boulet de plus de cinq cents kilos."},
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Et la ville, comment se défend-elle ?"},
                    {"personnage": "marco", "emotion": "triste", "texte": "L'empereur Constantin XI n'a que quelques milliers d'hommes contre une armée de plus de cinquante mille. Il tend même une chaîne géante en travers de la Corne d'Or pour bloquer la flotte ottomane."},
                ],
            },
            {
                "decor": "siege_medieval",
                "repliques": [
                    {"personnage": "clio", "emotion": "surprise", "texte": "Cette chaîne suffit à arrêter des navires entiers ?"},
                    {"personnage": "marco", "emotion": "surprise", "texte": "Un temps. Alors Mehmed fait une chose folle : il fait transporter ses navires par voie de terre, la nuit, sur des rondins graissés, pour les remettre à l'eau derrière la chaîne."},
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Après cinquante-trois jours de siège..."},
                    {"personnage": "marco", "emotion": "triste", "texte": "Le 29 mai 1453, la ville tombe. Constantin XI meurt au combat, dit-on, en arrachant les insignes impériaux pour se battre comme un simple soldat. Mille ans d'Empire romain d'Orient s'achèvent en une matinée."},
                ],
            },
        ],
    },
    {
        "id": "lune",
        "titre": "Le premier pas sur la Lune",
        "annee": "1969",
        "scenes": [
            {
                "decor": "espace_etoiles",
                "repliques": [
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Trois hommes, dans cette capsule minuscule, à des centaines de milliers de kilomètres de tout secours..."},
                    {"personnage": "marco", "emotion": "inquiet", "texte": "Neil Armstrong, Buzz Aldrin, et Michael Collins qui reste seul en orbite lunaire, dans le module de commande — le passage le plus solitaire de toute l'histoire humaine, littéralement à l'écart de toute l'espèce."},
                    {"personnage": "clio", "emotion": "neutre", "texte": "Et les deux autres, ils descendent comment ?"},
                    {"personnage": "marco", "emotion": "inquiet", "texte": "Le module lunaire Eagle. À quelques secondes de l'alunissage, l'ordinateur de bord sature d'alarmes — et Armstrong doit reprendre les commandes à la main pour éviter un champ de rochers, avec à peine vingt secondes de carburant restant."},
                ],
            },
            {
                "decor": "espace_etoiles",
                "repliques": [
                    {"personnage": "clio", "emotion": "surprise", "texte": "Et cette phrase qu'on cite toujours... il l'a préparée à l'avance ?"},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "\"C'est un petit pas pour l'homme, un pas de géant pour l'humanité.\" Personne ne sait vraiment s'il l'a improvisée ou répétée en secret — lui-même a toujours affirmé qu'elle lui était venue sur le moment."},
                    {"personnage": "clio", "emotion": "surprise", "texte": "Vingt juillet 1969. Six cents millions de personnes devant leur télévision, dit-on."},
                    {"personnage": "marco", "emotion": "joyeux", "texte": "Un cinquième de l'humanité, les yeux levés vers le même petit point gris dans le ciel, en même temps. Ça ne s'était jamais produit avant. Et ça ne s'est peut-être jamais reproduit depuis."},
                ],
            },
        ],
    },
    {
        "id": "peste-noire",
        "titre": "La Peste Noire",
        "annee": "1347",
        "scenes": [
            {
                "decor": "ville_medievale_sombre",
                "repliques": [
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Ces navires qui accostent à Gênes en 1347... pourquoi tout le monde recule d'horreur ?"},
                    {"personnage": "marco", "emotion": "triste", "texte": "Parce que leurs équipages sont déjà morts ou mourants. La peste a voyagé depuis l'Asie centrale le long des routes commerciales, portée par des puces qui vivent sur des rats — personne ne le sait encore à l'époque."},
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Et on ne comprend vraiment pas comment elle se propage ?"},
                    {"personnage": "marco", "emotion": "triste", "texte": "On l'ignore totalement. Certains accusent l'air corrompu, d'autres les astres, d'autres encore des boucs émissaires innocents — les vraies causes ne seront comprises que des siècles plus tard."},
                ],
            },
            {
                "decor": "ville_medievale_sombre",
                "repliques": [
                    {"personnage": "clio", "emotion": "inquiet", "texte": "En combien de temps la maladie traverse-t-elle l'Europe entière ?"},
                    {"personnage": "marco", "emotion": "triste", "texte": "À peine quatre ans, entre 1347 et 1351. Et le bilan dépasse l'imaginable : environ un tiers de la population européenne disparaît — jusqu'à la moitié dans certaines régions."},
                    {"personnage": "clio", "emotion": "inquiet", "texte": "Comment une société se relève-t-elle d'une perte pareille ?"},
                    {"personnage": "marco", "emotion": "neutre", "texte": "Lentement, et transformée. La main-d'œuvre devient si rare que les paysans survivants peuvent enfin négocier de meilleures conditions — l'épidémie a, malgré l'horreur, ébranlé tout l'ordre féodal européen."},
                ],
            },
        ],
    },
]
