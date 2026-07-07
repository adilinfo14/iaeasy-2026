import asyncio

_pipeline_cache: dict = {}
_fasttext_model = None


def _get_pipeline(task: str, model_ref: str):
    key = (task, model_ref)
    if key not in _pipeline_cache:
        from transformers import pipeline

        _pipeline_cache[key] = pipeline(task, model=model_ref)
    return _pipeline_cache[key]


def _sentiment_sync(model_ref: str, input_text: str) -> dict:
    clf = _get_pipeline("text-classification", model_ref)
    result = clf(input_text)[0]
    return {
        "type": "classification",
        "etiquette": result["label"],
        "confiance": round(result["score"], 4),
    }


def _traduction_sync(model_ref: str, input_text: str) -> dict:
    trad = _get_pipeline("translation", model_ref)
    result = trad(input_text)[0]
    return {"type": "traduction", "sortie": result["translation_text"]}


def _langid_sync(input_text: str) -> dict:
    global _fasttext_model
    if _fasttext_model is None:
        import fasttext
        from huggingface_hub import hf_hub_download

        model_path = hf_hub_download(
            "facebook/fasttext-language-identification", "model.bin"
        )
        _fasttext_model = fasttext.load_model(model_path)

    cleaned = input_text.replace("\n", " ")
    labels, scores = _fasttext_model.predict(cleaned, k=1)
    code = labels[0].replace("__label__", "")
    return {
        "type": "detection_langue",
        "langue_detectee": code,
        "confiance": round(float(scores[0]), 4),
    }


async def run_sentiment(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_sentiment_sync, model_ref, input_text)


async def run_traduction(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_traduction_sync, model_ref, input_text)


async def run_langid(input_text: str) -> dict:
    return await asyncio.to_thread(_langid_sync, input_text)
