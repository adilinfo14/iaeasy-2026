from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException

from .runners import ollama_runner, timeseries_runner, transformers_runner, vision_runner
from .schemas import EssaiRequest, ModelCard

router = APIRouter(prefix="/catalogue", tags=["catalogue"])

_DATA_PATH = Path(__file__).parent / "data" / "models.yaml"


def _load_models() -> dict[str, dict]:
    with open(_DATA_PATH, encoding="utf-8") as f:
        entries = yaml.safe_load(f)
    return {entry["id"]: entry for entry in entries}


_MODELS = _load_models()


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
    texte = requete.input_text or modele["cas_usage"]["input_exemple"]

    try:
        if model_id == "nomic-embeddings":
            return await ollama_runner.run_embeddings(ref, texte)
        if modele["moteur"] == "ollama":
            return await ollama_runner.run_generatif(ref, texte)
        if model_id == "camembert-sentiment":
            return await transformers_runner.run_sentiment(ref, texte)
        if model_id == "helsinki-traduction":
            return await transformers_runner.run_traduction(ref, texte)
        if model_id == "fasttext-langue":
            return await transformers_runner.run_langid(texte)
        if modele["moteur"] == "ultralytics":
            return await vision_runner.run_detection(ref)
        if modele["moteur"] == "chronos":
            return await timeseries_runner.run_prevision(ref)
        if modele["moteur"] == "sklearn":
            return await timeseries_runner.run_anomalie()
    except Exception as exc:  # noqa: BLE001 — on veut un message pédagogique, pas une 500 brute
        raise HTTPException(500, f"Échec de l'exécution du modèle '{model_id}': {exc}") from exc

    raise HTTPException(500, f"Aucun exécuteur défini pour le modèle '{model_id}'")
