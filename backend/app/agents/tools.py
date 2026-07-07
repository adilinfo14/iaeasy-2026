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


def _eval_noeud(noeud):
    if isinstance(noeud, ast.Constant):
        return noeud.value
    if isinstance(noeud, ast.BinOp) and type(noeud.op) in _OPS:
        return _OPS[type(noeud.op)](_eval_noeud(noeud.left), _eval_noeud(noeud.right))
    if isinstance(noeud, ast.UnaryOp) and type(noeud.op) in _OPS:
        return _OPS[type(noeud.op)](_eval_noeud(noeud.operand))
    raise ValueError("Expression non supportée (seuls +,-,*,/,** sur des nombres sont autorisés)")


def calculatrice(expression: str) -> dict:
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
