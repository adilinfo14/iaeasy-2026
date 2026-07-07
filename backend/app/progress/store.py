import json
from pathlib import Path

from ..core.config import settings

_FICHIER = Path(settings.data_dir) / "progression.json"


def _lire() -> set[str]:
    if not _FICHIER.exists():
        return {"llm_seul"}
    return set(json.loads(_FICHIER.read_text(encoding="utf-8")))


def _ecrire(debloquees: set[str]) -> None:
    _FICHIER.write_text(json.dumps(sorted(debloquees)), encoding="utf-8")


def get_debloquees() -> list[str]:
    return sorted(_lire())


def debloquer(brique_id: str) -> list[str]:
    debloquees = _lire()
    debloquees.add(brique_id)
    _ecrire(debloquees)
    return sorted(debloquees)
