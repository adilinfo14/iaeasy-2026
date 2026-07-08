import json
from pathlib import Path

from ..core.config import settings

_FICHIER = Path(settings.data_dir) / "visiteurs.json"


def _lire() -> set[str]:
    if not _FICHIER.exists():
        return set()
    return set(json.loads(_FICHIER.read_text(encoding="utf-8")))


def _ecrire(visiteurs: set[str]) -> None:
    _FICHIER.write_text(json.dumps(sorted(visiteurs)), encoding="utf-8")


def enregistrer_visiteur(visiteur_id: str) -> int:
    visiteurs = _lire()
    visiteurs.add(visiteur_id)
    _ecrire(visiteurs)
    return len(visiteurs)


def compter_visiteurs() -> int:
    return len(_lire())
