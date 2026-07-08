from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException

from .runners import ml_classique_runner, ollama_runner, timeseries_runner, transformers_runner, vision_runner
from .schemas import EssaiRequest, ModelCard

router = APIRouter(prefix="/catalogue", tags=["catalogue"])

_DATA_PATH = Path(__file__).parent / "data" / "models.yaml"


def _load_models() -> dict[str, dict]:
    with open(_DATA_PATH, encoding="utf-8") as f:
        entries = yaml.safe_load(f)
    return {entry["id"]: entry for entry in entries}


_MODELS = _load_models()


# Chaque entrée : soit une fonction sans argument (modèles à données bundlées/synthétiques),
# soit une fonction (ref, texte) pour les modèles qui prennent une entrée libre.
_DISPATCH_SANS_TEXTE = {
    "yolo-vision": lambda ref: vision_runner.run_detection(ref),
    "yolo-vision-small": lambda ref: vision_runner.run_detection(ref),
    "yolo-classification": lambda ref: vision_runner.run_classification(ref),
    "yolo-classification-small": lambda ref: vision_runner.run_classification(ref),
    "whisper-transcription": lambda ref: transformers_runner.run_transcription(ref),
    "chronos-previsions": lambda ref: timeseries_runner.run_prevision(ref),
    "isolation-forest-maintenance": lambda ref: timeseries_runner.run_anomalie(),
    "isolation-forest-fraude": lambda ref: timeseries_runner.run_fraude(),
    "isolation-forest-four": lambda ref: timeseries_runner.run_anomalie_four(),
    "scoring-credit": lambda ref: ml_classique_runner.run_scoring_credit(),
    "scoring-pret-immobilier": lambda ref: ml_classique_runner.run_scoring_pret(),
    "recommandation-films": lambda ref: ml_classique_runner.run_recommandation(),
    "recommandation-materiaux": lambda ref: ml_classique_runner.run_recommandation_materiaux(),
}

_DISPATCH_AVEC_TEXTE = {
    "nomic-embeddings": lambda ref, texte: ollama_runner.run_embeddings(ref, texte),
    "mxbai-embeddings": lambda ref, texte: ollama_runner.run_embeddings(ref, texte),
    "minilm-embeddings": lambda ref, texte: ollama_runner.run_embeddings(ref, texte),
    "camembert-sentiment": lambda ref, texte: transformers_runner.run_sentiment(ref, texte),
    "helsinki-traduction": lambda ref, texte: transformers_runner.run_traduction(ref, texte),
    "barthez-resume": lambda ref, texte: transformers_runner.run_resume(ref, texte),
    "camembert-ner": lambda ref, texte: transformers_runner.run_ner(ref, texte),
    "camembert-qa": lambda ref, texte: transformers_runner.run_qa(ref, texte),
    "fasttext-langue": lambda ref, texte: transformers_runner.run_langid(texte),
}


@router.get("", response_model=list[ModelCard])
def lister_modeles():
    return list(_MODELS.values())


@router.get("/{model_id}", response_model=ModelCard)
def detail_modele(model_id: str):
    if model_id not in _MODELS:
        raise HTTPException(404, "Modèle inconnu")
    return _MODELS[model_id]


@router.post("/{model_id}/essayer")
async def essayer_modele(model_id: str, requete: EssaiRequest):
    if model_id not in _MODELS:
        raise HTTPException(404, "Modèle inconnu")
    modele = _MODELS[model_id]
    ref = modele["moteur_ref"]

    try:
        if model_id in _DISPATCH_SANS_TEXTE:
            return await _DISPATCH_SANS_TEXTE[model_id](ref)

        exemples = modele["cas_usage"].get("exemples", [])
        defaut = exemples[0]["input"] if exemples else ""
        texte = requete.input_text or defaut

        if model_id in _DISPATCH_AVEC_TEXTE:
            return await _DISPATCH_AVEC_TEXTE[model_id](ref, texte)

        if modele["moteur"] == "ollama":
            return await ollama_runner.run_generatif(ref, texte)
    except Exception as exc:  # noqa: BLE001 — on veut un message pédagogique, pas une 500 brute
        raise HTTPException(500, f"Échec de l'exécution du modèle '{model_id}': {exc}") from exc

    raise HTTPException(500, f"Aucun exécuteur défini pour le modèle '{model_id}'")
