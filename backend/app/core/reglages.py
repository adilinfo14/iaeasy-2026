import json
from pathlib import Path

from .config import settings

# Réglages ajustables en direct depuis /admin, sans redéploiement — persistés dans un fichier
# JSON (survit à un redémarrage du conteneur), lus à chaque requête par les endpoints concernés
# plutôt que mis en cache, pour qu'un changement soit pris en compte immédiatement.
_FICHIER = Path(settings.data_dir) / "reglages.json"

_PAR_DEFAUT = {
    "chat_max_historique": 16,
    "chat_longueur_max_message": 500,
    "chat_longueur_max_message_historique": 2000,
    "chat_max_conversations_simultanees": 5,
}


def _charger() -> dict:
    if _FICHIER.exists():
        try:
            data = json.loads(_FICHIER.read_text(encoding="utf-8"))
            return {**_PAR_DEFAUT, **data}
        except Exception:  # noqa: BLE001 — un fichier corrompu ne doit pas empêcher le site de démarrer
            return dict(_PAR_DEFAUT)
    return dict(_PAR_DEFAUT)


_reglages = _charger()


def get_reglages() -> dict:
    return dict(_reglages)


def set_reglages(nouveaux: dict) -> dict:
    _reglages.update(nouveaux)
    _FICHIER.parent.mkdir(parents=True, exist_ok=True)
    _FICHIER.write_text(json.dumps(_reglages, ensure_ascii=False, indent=2), encoding="utf-8")
    return dict(_reglages)
