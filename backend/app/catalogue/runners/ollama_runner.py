from ...core.ollama_client import ollama


async def run_generatif(model_ref: str, input_text: str) -> dict:
    output = await ollama.generate(model_ref, input_text)
    return {"type": "texte", "sortie": output}


async def run_embeddings(model_ref: str, input_text: str) -> dict:
    phrases = [p.strip() for p in input_text.split("Phrase B:")]
    if len(phrases) == 2:
        phrase_a = phrases[0].replace("Phrase A:", "").strip()
        phrase_b = phrases[1].strip()
    else:
        phrase_a, phrase_b = input_text, input_text

    vec_a = await ollama.embed(model_ref, phrase_a)
    vec_b = await ollama.embed(model_ref, phrase_b)

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    similarite = dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    return {
        "type": "similarite",
        "phrase_a": phrase_a,
        "phrase_b": phrase_b,
        "dimension_vecteur": len(vec_a),
        "similarite_cosinus": round(similarite, 4),
        "explication": "1.0 = sens identique, 0.0 = sens sans rapport. Les vecteurs ont "
        f"{len(vec_a)} dimensions chacun.",
    }
