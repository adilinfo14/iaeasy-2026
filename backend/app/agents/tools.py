import ast
import operator

_MINI_CORPUS = [
    "Le RAG (Retrieval Augmented Generation) consiste à retrouver des passages pertinents "
    "dans un corpus avant de les donner en contexte à un LLM.",
    "Le protocole MCP (Model Context Protocol) standardise la façon dont un modèle appelle "
    "des outils et des sources de données externes.",
    "Une boucle ReAct alterne des étapes de raisonnement (Reason) et d'action (Act) jusqu'à "
    "obtenir une réponse finale.",
    "En maintenance prédictive, un modèle de détection d'anomalie comme Isolation Forest "
    "s'entraîne directement sur les données de la machine à surveiller.",
    "Un système multi-agent répartit une tâche complexe entre plusieurs agents spécialisés "
    "qui collaborent, par exemple un agent chercheur et un agent rédacteur.",
]

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

# Cette calculatrice est appelée en synchrone dans une boucle asyncio mono-worker : un calcul
# trop coûteux (ex: un exposant énorme sur un grand entier) bloquerait le processus entier pour
# TOUS les visiteurs, pas seulement l'auteur de la requête. D'où ces bornes strictes.
_LONGUEUR_MAX_EXPRESSION = 200
_MAGNITUDE_MAX = 10**12
_EXPOSANT_MAX = 64


def _nombre_valide(valeur) -> bool:
    return isinstance(valeur, (int, float)) and not isinstance(valeur, bool) and abs(valeur) <= _MAGNITUDE_MAX


def _eval_noeud(noeud):
    if isinstance(noeud, ast.Constant):
        if not _nombre_valide(noeud.value):
            raise ValueError("Seuls des nombres raisonnables (|x| ≤ 10^12) sont autorisés")
        return noeud.value
    if isinstance(noeud, ast.BinOp) and type(noeud.op) in _OPS:
        gauche, droite = _eval_noeud(noeud.left), _eval_noeud(noeud.right)
        if isinstance(noeud.op, ast.Pow) and abs(droite) > _EXPOSANT_MAX:
            raise ValueError(f"Exposant trop grand (max {_EXPOSANT_MAX})")
        resultat = _OPS[type(noeud.op)](gauche, droite)
        if not _nombre_valide(resultat):
            raise ValueError("Résultat intermédiaire trop grand (|x| ≤ 10^12)")
        return resultat
    if isinstance(noeud, ast.UnaryOp) and type(noeud.op) in _OPS:
        return _OPS[type(noeud.op)](_eval_noeud(noeud.operand))
    raise ValueError("Expression non supportée (seuls +,-,*,/,** sur des nombres sont autorisés)")


def calculatrice(expression: str) -> dict:
    if not isinstance(expression, str) or len(expression) > _LONGUEUR_MAX_EXPRESSION:
        return {"ok": False, "resultat": None, "erreur": f"Expression trop longue (max {_LONGUEUR_MAX_EXPRESSION} caractères)"}
    try:
        arbre = ast.parse(expression, mode="eval").body
        resultat = _eval_noeud(arbre)
        return {"ok": True, "resultat": resultat, "erreur": None}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "resultat": None, "erreur": str(exc)}


def recherche_mini_corpus(requete: str) -> dict:
    mots_requete = set(requete.lower().split())
    meilleur, meilleur_score = _MINI_CORPUS[0], -1
    for passage in _MINI_CORPUS:
        score = len(mots_requete & set(passage.lower().replace(",", "").split()))
        if score > meilleur_score:
            meilleur, meilleur_score = passage, score
    return {"passage": meilleur, "score_correspondance": meilleur_score}
