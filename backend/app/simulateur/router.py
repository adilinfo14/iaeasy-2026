import asyncio
import csv
import time
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..catalogue.runners.vision_runner import run_detection
from ..core.ollama_client import ollama

router = APIRouter(prefix="/simulateur", tags=["simulateur"])

# Tailles approximatives en milliards de paramètres — chiffres publics arrondis, à but
# uniquement pédagogique (l'estimation d'énergie qui en découle est une approximation
# proportionnelle, PAS une mesure réelle de consommation).
_MODELES = [
    {"id": "gemma2:2b", "nom": "Gemma 2 (2B)", "parametres_milliards": 2.0},
    {"id": "llama3.2:3b", "nom": "Llama 3.2 (3B)", "parametres_milliards": 3.2},
    {"id": "phi3:mini", "nom": "Phi-3 Mini", "parametres_milliards": 3.8},
    {"id": "deepseek-coder:6.7b", "nom": "DeepSeek Coder (6.7B)", "parametres_milliards": 6.7},
    {"id": "mistral:7b-instruct", "nom": "Mistral 7B Instruct", "parametres_milliards": 7.0},
    {"id": "qwen2.5:7b-instruct", "nom": "Qwen 2.5 7B Instruct", "parametres_milliards": 7.6},
    {"id": "llama3:8b", "nom": "Llama 3 (8B)", "parametres_milliards": 8.0},
]

_PROMPT_DEFAUT = "Explique en 3 phrases ce qu'est la garantie décennale."
_LONGUEUR_MAX_PROMPT = 300
_IDS_AUTORISES = {m["id"] for m in _MODELES}

# Les 3 modèles d'embeddings du Catalogue — comparables entre eux sur la durée et le score de
# similarité, contrairement aux LLM génératifs, mais selon une mécanique différente (2 phrases
# à comparer plutôt qu'un prompt libre).
_MODELES_EMBEDDINGS = [
    {"id": "all-minilm", "nom": "All-MiniLM", "parametres_millions": 23},
    {"id": "nomic-embed-text", "nom": "Nomic Embed Text", "parametres_millions": 137},
    {"id": "mxbai-embed-large", "nom": "Mxbai Embed Large", "parametres_millions": 335},
]
_IDS_EMBEDDINGS_AUTORISES = {m["id"] for m in _MODELES_EMBEDDINGS}
_PHRASE_A_DEFAUT = "Le chat dort sur le canapé."
_PHRASE_B_DEFAUT = "Un félin fait la sieste sur le sofa."
_LONGUEUR_MAX_PHRASE = 300

# 4 algorithmes "classiques" (pas de réseau de neurones), entraînés en direct sur le même
# petit jeu de données (spam/légitime, déjà utilisé par le module Entraînement) — comparables
# sur la durée d'entraînement et la précision, contrairement à un LLM qu'on interroge sans
# jamais l'entraîner soi-même.
_MODELES_CLASSIFICATION = [
    {"id": "regression_logistique", "nom": "Régression logistique"},
    {"id": "arbre_decision", "nom": "Arbre de décision"},
    {"id": "naive_bayes", "nom": "Naïve Bayes"},
    {"id": "knn", "nom": "K plus proches voisins (k=3)"},
]
_IDS_CLASSIFICATION_AUTORISEES = {m["id"] for m in _MODELES_CLASSIFICATION}
_DATASET_SPAM = Path(__file__).resolve().parent.parent / "training" / "datasets" / "toy_spam_fr.csv"
_MESSAGE_CLASSIFICATION_DEFAUT = "Cliquez ici pour gagner un iPhone gratuitement maintenant."
_LONGUEUR_MAX_MESSAGE = 300

# 2 variantes de taille du même modèle de détection d'objets, exécutées sur la même image
# d'exemple fournie par l'outil (aucun upload nécessaire) — comparables sur la durée et les
# objets détectés, contrairement à un LLM qui ne prend pas d'image en entrée.
_MODELES_VISION = [
    {"id": "yolo-vision", "nom": "YOLOv8 Nano (détection)", "moteur_ref": "yolov8n.pt", "parametres_millions": 3.2},
    {"id": "yolo-vision-small", "nom": "YOLOv8 Small (détection)", "moteur_ref": "yolov8s.pt", "parametres_millions": 11.2},
]
_IDS_VISION_AUTORISES = {m["id"] for m in _MODELES_VISION}


class ComparerRequest(BaseModel):
    prompt: str | None = Field(default=None, max_length=_LONGUEUR_MAX_PROMPT)
    # Liste blanche stricte : sans ça, un appel direct pourrait glisser l'id d'un modèle non
    # prévu ici (ex: un modèle bien plus lourd présent sur l'Ollama partagé du homelab).
    modeles_ids: list[str] | None = Field(default=None, max_length=len(_MODELES))


class ComparerEmbeddingsRequest(BaseModel):
    phrase_a: str | None = Field(default=None, max_length=_LONGUEUR_MAX_PHRASE)
    phrase_b: str | None = Field(default=None, max_length=_LONGUEUR_MAX_PHRASE)
    modeles_ids: list[str] | None = Field(default=None, max_length=len(_MODELES_EMBEDDINGS))


class ComparerClassificationRequest(BaseModel):
    message: str | None = Field(default=None, max_length=_LONGUEUR_MAX_MESSAGE)
    modeles_ids: list[str] | None = Field(default=None, max_length=len(_MODELES_CLASSIFICATION))


class ComparerVisionRequest(BaseModel):
    modeles_ids: list[str] | None = Field(default=None, max_length=len(_MODELES_VISION))


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norme_a = sum(x * x for x in a) ** 0.5
    norme_b = sum(y * y for y in b) ** 0.5
    return dot / (norme_a * norme_b) if norme_a and norme_b else 0.0


def _construire_classifieur(algo_id: str):
    if algo_id == "regression_logistique":
        from sklearn.linear_model import LogisticRegression

        return LogisticRegression(max_iter=1000)
    if algo_id == "arbre_decision":
        from sklearn.tree import DecisionTreeClassifier

        return DecisionTreeClassifier(max_depth=5, random_state=0)
    if algo_id == "naive_bayes":
        from sklearn.naive_bayes import MultinomialNB

        return MultinomialNB()
    if algo_id == "knn":
        from sklearn.neighbors import KNeighborsClassifier

        return KNeighborsClassifier(n_neighbors=3)
    raise ValueError(f"Algorithme inconnu : {algo_id}")


def _comparer_classification_sync(message: str, ids_choisis: list[str]) -> dict:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import StratifiedKFold, cross_val_score

    textes, labels = [], []
    with open(_DATASET_SPAM, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            textes.append(row["texte"])
            labels.append(int(row["label"]))
    y = np.array(labels)

    vectorizer = TfidfVectorizer(max_features=200)
    X = vectorizer.fit_transform(textes)
    x_message = vectorizer.transform([message])

    modeles_a_comparer = (
        [m for m in _MODELES_CLASSIFICATION if m["id"] in ids_choisis] if ids_choisis else _MODELES_CLASSIFICATION
    )

    resultats = []
    for m in modeles_a_comparer:
        modele = _construire_classifieur(m["id"])

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        precisions = cross_val_score(modele, X, y, cv=cv)

        debut = time.monotonic()
        modele.fit(X, y)
        duree = time.monotonic() - debut

        proba = modele.predict_proba(x_message)[0]
        prediction = "spam" if proba[1] > proba[0] else "légitime"

        resultats.append(
            {
                "id": m["id"],
                "nom": m["nom"],
                "duree_secondes": round(duree, 4),
                "precision_validation_croisee_pourcent": round(100 * float(precisions.mean())),
                "prediction": prediction,
                "confiance": round(float(proba.max()), 3),
            }
        )

    return {"message": message, "resultats": resultats}


@router.get("/modeles")
def modeles():
    return _MODELES


@router.get("/modeles-embeddings")
def modeles_embeddings():
    return _MODELES_EMBEDDINGS


@router.get("/modeles-classification")
def modeles_classification():
    return _MODELES_CLASSIFICATION


@router.get("/modeles-vision")
def modeles_vision():
    return [{k: v for k, v in m.items() if k != "moteur_ref"} for m in _MODELES_VISION]


@router.post("/comparer")
async def comparer(requete: ComparerRequest):
    prompt = (requete.prompt or "").strip() or _PROMPT_DEFAUT
    plus_gros = max(m["parametres_milliards"] for m in _MODELES)

    ids_choisis = [i for i in (requete.modeles_ids or []) if i in _IDS_AUTORISES]
    modeles_a_comparer = [m for m in _MODELES if m["id"] in ids_choisis] if ids_choisis else _MODELES

    resultats = []
    for m in modeles_a_comparer:
        debut = time.monotonic()
        reponse = await ollama.generate(m["id"], prompt)
        duree = time.monotonic() - debut
        resultats.append(
            {
                "id": m["id"],
                "nom": m["nom"],
                "parametres_milliards": m["parametres_milliards"],
                "duree_secondes": round(duree, 2),
                "longueur_reponse": len(reponse),
                "reponse": reponse[:400],
                "estimation_energie_relative_pourcent": round(100 * m["parametres_milliards"] / plus_gros),
            }
        )

    return {"prompt": prompt, "resultats": resultats}


@router.post("/comparer-embeddings")
async def comparer_embeddings(requete: ComparerEmbeddingsRequest):
    phrase_a = (requete.phrase_a or "").strip() or _PHRASE_A_DEFAUT
    phrase_b = (requete.phrase_b or "").strip() or _PHRASE_B_DEFAUT

    ids_choisis = [i for i in (requete.modeles_ids or []) if i in _IDS_EMBEDDINGS_AUTORISES]
    modeles_a_comparer = (
        [m for m in _MODELES_EMBEDDINGS if m["id"] in ids_choisis] if ids_choisis else _MODELES_EMBEDDINGS
    )

    resultats = []
    for m in modeles_a_comparer:
        debut = time.monotonic()
        vecteur_a = await ollama.embed(m["id"], phrase_a)
        vecteur_b = await ollama.embed(m["id"], phrase_b)
        duree = time.monotonic() - debut
        resultats.append(
            {
                "id": m["id"],
                "nom": m["nom"],
                "parametres_millions": m["parametres_millions"],
                "duree_secondes": round(duree, 2),
                "dimension_vecteur": len(vecteur_a),
                "similarite_cosinus": round(_cosine(vecteur_a, vecteur_b), 4),
            }
        )

    return {"phrase_a": phrase_a, "phrase_b": phrase_b, "resultats": resultats}


@router.post("/comparer-classification")
async def comparer_classification(requete: ComparerClassificationRequest):
    message = (requete.message or "").strip() or _MESSAGE_CLASSIFICATION_DEFAUT
    ids_choisis = [i for i in (requete.modeles_ids or []) if i in _IDS_CLASSIFICATION_AUTORISEES]
    return await asyncio.to_thread(_comparer_classification_sync, message, ids_choisis)


@router.post("/comparer-vision")
async def comparer_vision(requete: ComparerVisionRequest):
    ids_choisis = [i for i in (requete.modeles_ids or []) if i in _IDS_VISION_AUTORISES]
    modeles_a_comparer = [m for m in _MODELES_VISION if m["id"] in ids_choisis] if ids_choisis else _MODELES_VISION

    image_note = None
    resultats = []
    for m in modeles_a_comparer:
        debut = time.monotonic()
        detection = await run_detection(m["moteur_ref"])
        duree = time.monotonic() - debut
        image_note = detection["note"]
        resultats.append(
            {
                "id": m["id"],
                "nom": m["nom"],
                "parametres_millions": m["parametres_millions"],
                "duree_secondes": round(duree, 2),
                "nb_objets": detection["nb_objets"],
                "objets_detectes": detection["objets_detectes"],
                "image_annotee_base64": detection["image_annotee_base64"],
            }
        )

    return {"image_note": image_note, "resultats": resultats}
