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


_MAX_BRIQUES = 1000


def debloquer(brique_id: str) -> list[str]:
    debloquees = _lire()
    if brique_id not in debloquees and len(debloquees) >= _MAX_BRIQUES:
        return sorted(debloquees)
    debloquees.add(brique_id)
    _ecrire(debloquees)
    return sorted(debloquees)


_FICHIER_BADGES = Path(settings.data_dir) / "badges.json"
_MAX_BADGES = 1000


def _lire_badges() -> set[str]:
    if not _FICHIER_BADGES.exists():
        return set()
    return set(json.loads(_FICHIER_BADGES.read_text(encoding="utf-8")))


def _ecrire_badges(badges: set[str]) -> None:
    _FICHIER_BADGES.write_text(json.dumps(sorted(badges)), encoding="utf-8")


def get_badges() -> list[str]:
    return sorted(_lire_badges())


def valider_badge(brique_id: str) -> list[str]:
    badges = _lire_badges()
    if brique_id not in badges and len(badges) >= _MAX_BADGES:
        return sorted(badges)
    badges.add(brique_id)
    _ecrire_badges(badges)
    return sorted(badges)
