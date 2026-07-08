import asyncio
import base64
import os
import subprocess
import tempfile

_LONGUEUR_MAX_TEXTE = 300


def _tts_sync(texte: str) -> dict:
    texte = (texte or "").strip()[:_LONGUEUR_MAX_TEXTE] or "Bonjour, ceci est un test de synthèse vocale."

    chemin = tempfile.mktemp(suffix=".wav")
    try:
        subprocess.run(
            ["espeak-ng", "-v", "fr", "-w", chemin, texte],
            capture_output=True,
            timeout=15,
            check=True,
        )
        with open(chemin, "rb") as f:
            audio_bytes = f.read()
    finally:
        if os.path.exists(chemin):
            os.remove(chemin)

    return {
        "type": "synthese_vocale",
        "texte_source": texte,
        "audio_base64": base64.b64encode(audio_bytes).decode(),
        "note": "Moteur de synthèse vocale « classique » (règles phonétiques codées à la main, pas "
        "un réseau de neurones) — très léger et quasi instantané, mais avec une voix nettement plus "
        "robotique qu'un moteur neuronal moderne. Preuve que toute IA n'est pas un réseau de "
        "neurones, y compris pour une tâche que l'on associe aujourd'hui presque toujours à un modèle appris.",
    }


async def run_tts(texte: str) -> dict:
    return await asyncio.to_thread(_tts_sync, texte)
