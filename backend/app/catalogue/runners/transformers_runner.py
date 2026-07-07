import asyncio
import base64
import io

_pipeline_cache: dict = {}
_langid_model = None
_ner_pipeline_cache: dict = {}
_qa_pipeline_cache: dict = {}
_whisper_pipeline_cache: dict = {}
_sample_audio_cache = None


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
    # Le task générique "translation" du pipeline transformers a été retiré dans les
    # versions récentes ; on appelle donc directement le modèle seq2seq sous-jacent.
    key = ("seq2seq", model_ref)
    if key not in _pipeline_cache:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_ref)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_ref)
        _pipeline_cache[key] = (tokenizer, model)

    tokenizer, model = _pipeline_cache[key]
    entrees = tokenizer(input_text, return_tensors="pt", truncation=True)
    sortie = model.generate(**entrees, max_new_tokens=128)
    texte = tokenizer.decode(sortie[0], skip_special_tokens=True)
    return {"type": "traduction", "sortie": texte}


def _resume_sync(model_ref: str, input_text: str) -> dict:
    key = ("resume", model_ref)
    if key not in _pipeline_cache:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_ref)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_ref)
        _pipeline_cache[key] = (tokenizer, model)

    tokenizer, model = _pipeline_cache[key]
    entree = f"summarize: {input_text}" if "t5" in model_ref.lower() else input_text
    entrees = tokenizer(entree, return_tensors="pt", truncation=True, max_length=512)
    sortie = model.generate(**entrees, max_new_tokens=80, num_beams=4)
    texte = tokenizer.decode(sortie[0], skip_special_tokens=True)
    return {"type": "resume", "texte_original": input_text, "sortie": texte}


def _ner_sync(model_ref: str, input_text: str) -> dict:
    if model_ref not in _ner_pipeline_cache:
        from transformers import pipeline

        _ner_pipeline_cache[model_ref] = pipeline("ner", model=model_ref, aggregation_strategy="simple")

    entites = _ner_pipeline_cache[model_ref](input_text)
    return {
        "type": "extraction_entites",
        "texte_analyse": input_text,
        "entites": [
            {
                "texte": e["word"],
                "categorie": e["entity_group"],
                "confiance": round(float(e["score"]), 4),
            }
            for e in entites
        ],
    }


def _qa_sync(model_ref: str, input_text: str) -> dict:
    # Le task générique "question-answering" du pipeline transformers a lui aussi été
    # retiré dans les versions récentes ; on appelle donc directement le modèle sous-jacent.
    if model_ref not in _qa_pipeline_cache:
        import torch
        from transformers import AutoModelForQuestionAnswering, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_ref)
        model = AutoModelForQuestionAnswering.from_pretrained(model_ref)
        _qa_pipeline_cache[model_ref] = (tokenizer, model)

    tokenizer, model = _qa_pipeline_cache[model_ref]

    if "Contexte :" in input_text and "Question :" in input_text:
        contexte = input_text.split("Contexte :")[1].split("Question :")[0].strip()
        question = input_text.split("Question :")[1].strip()
    else:
        contexte, question = input_text, "Quel est le sujet principal ?"

    entrees = tokenizer(question, contexte, return_tensors="pt", truncation=True)
    with torch.no_grad():
        sortie = model(**entrees)

    debut = int(torch.argmax(sortie.start_logits))
    fin = int(torch.argmax(sortie.end_logits)) + 1
    confiance = float(
        torch.softmax(sortie.start_logits, dim=-1)[0, debut]
        * torch.softmax(sortie.end_logits, dim=-1)[0, fin - 1]
    )
    reponse = tokenizer.decode(entrees["input_ids"][0, debut:fin], skip_special_tokens=True)

    return {
        "type": "question_reponse",
        "contexte": contexte,
        "question": question,
        "reponse": reponse or "(aucune réponse trouvée dans le contexte)",
        "confiance": round(confiance, 4),
    }


def _get_sample_audio():
    # decode=False + lecture manuelle via soundfile : le backend de décodage audio par
    # défaut de `datasets` exige `torchcodec`, qui lui-même exige FFmpeg (absent de cette
    # image, coûteux à ajouter). On lit donc les octets bruts nous-mêmes.
    global _sample_audio_cache
    if _sample_audio_cache is None:
        import soundfile as sf
        from datasets import Audio, load_dataset

        jeu = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
        jeu = jeu.cast_column("audio", Audio(decode=False))
        entree = jeu[0]["audio"]
        if entree.get("bytes"):
            array, sampling_rate = sf.read(io.BytesIO(entree["bytes"]))
        else:
            array, sampling_rate = sf.read(entree["path"])
        _sample_audio_cache = {"array": array, "sampling_rate": sampling_rate}
    return _sample_audio_cache


def _transcription_sync(model_ref: str) -> dict:
    if model_ref not in _whisper_pipeline_cache:
        from transformers import pipeline

        _whisper_pipeline_cache[model_ref] = pipeline("automatic-speech-recognition", model=model_ref)

    echantillon = _get_sample_audio()
    resultat = _whisper_pipeline_cache[model_ref](echantillon["array"].copy())

    import soundfile as sf

    tampon = io.BytesIO()
    sf.write(tampon, echantillon["array"], echantillon["sampling_rate"], format="WAV")
    audio_b64 = base64.b64encode(tampon.getvalue()).decode()

    return {
        "type": "transcription_audio",
        "texte_transcrit": resultat["text"].strip(),
        "audio_base64": audio_b64,
        "note": "Échantillon audio en anglais fourni par le jeu de test standard de Whisper "
        "(librispeech_asr_dummy) — Whisper gère aussi le français, ce n'est qu'un exemple de démonstration fiable.",
    }


def _langid_sync(input_text: str) -> dict:
    # Le binding Python officiel de fastText est incompatible avec numpy>=2 (bug connu,
    # non corrigé en amont : `np.array(obj, copy=False)` sur les probabilités renvoyées).
    # py3langid est un portage pur Python du même principe (modèle statistique minuscule,
    # pas un LLM) sans cette dépendance fragile.
    from py3langid.langid import MODEL_FILE, LanguageIdentifier

    global _langid_model
    if _langid_model is None:
        _langid_model = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)

    code, confiance = _langid_model.classify(input_text)
    return {
        "type": "detection_langue",
        "langue_detectee": code,
        "confiance": round(float(confiance), 4),
    }


async def run_sentiment(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_sentiment_sync, model_ref, input_text)


async def run_traduction(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_traduction_sync, model_ref, input_text)


async def run_langid(input_text: str) -> dict:
    return await asyncio.to_thread(_langid_sync, input_text)


async def run_resume(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_resume_sync, model_ref, input_text)


async def run_ner(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_ner_sync, model_ref, input_text)


async def run_qa(model_ref: str, input_text: str) -> dict:
    return await asyncio.to_thread(_qa_sync, model_ref, input_text)


async def run_transcription(model_ref: str) -> dict:
    return await asyncio.to_thread(_transcription_sync, model_ref)
