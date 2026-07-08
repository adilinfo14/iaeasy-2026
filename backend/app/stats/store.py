import json
from pathlib import Path

from ..core.config import settings

_FICHIER = Path(settings.data_dir) / "visiteurs.json"

# Plafond défensif : au-delà, on arrête d'accepter de nouveaux identifiants (un vrai visiteur
# unique de plus ne changera rien de notable à l'affichage) pour empêcher un abus scripté de
# gonfler indéfiniment ce fichier (déni de service par remplissage disque).
_MAX_VISITEURS = 500_000


def _lire() -> set[str]:
    if not _FICHIER.exists():
        return set()
    return set(json.loads(_FICHIER.read_text(encoding="utf-8")))


def _ecrire(visiteurs: set[str]) -> None:
    _FICHIER.write_text(json.dumps(sorted(visiteurs)), encoding="utf-8")


def enregistrer_visiteur(visiteur_id: str) -> int:
    visiteurs = _lire()
    if visiteur_id not in visiteurs and len(visiteurs) >= _MAX_VISITEURS:
        return len(visiteurs)
    visiteurs.add(visiteur_id)
    _ecrire(visiteurs)
    return len(visiteurs)


def compter_visiteurs() -> int:
    return len(_lire())
