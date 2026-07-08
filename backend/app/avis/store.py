import json
from pathlib import Path

from ..core.config import settings

_FICHIER = Path(settings.data_dir) / "avis.json"

# Un avis par visiteur_id (upsert, pas d'ajout) — évite qu'un même visiteur gonfle la moyenne
# en soumettant plusieurs fois. Plafond défensif contre un remplissage disque scripté, comme
# pour stats/store.py.
_MAX_AVIS = 50_000


def _lire() -> dict[str, dict]:
    if not _FICHIER.exists():
        return {}
    return json.loads(_FICHIER.read_text(encoding="utf-8"))


def _ecrire(avis: dict[str, dict]) -> None:
    _FICHIER.write_text(json.dumps(avis, ensure_ascii=False), encoding="utf-8")


def enregistrer_avis(visiteur_id: str, note: int, commentaire: str | None, horodatage: str) -> None:
    avis = _lire()
    if visiteur_id not in avis and len(avis) >= _MAX_AVIS:
        return
    avis[visiteur_id] = {"note": note, "commentaire": commentaire, "horodatage": horodatage}
    _ecrire(avis)


def lister_avis() -> list[dict]:
    return list(_lire().values())


def stats_avis() -> dict:
    tous = lister_avis()
    total = len(tous)
    distribution = {str(i): 0 for i in range(1, 6)}
    for a in tous:
        distribution[str(a["note"])] += 1
    moyenne = round(sum(a["note"] for a in tous) / total, 2) if total else None
    return {"total": total, "moyenne": moyenne, "distribution": distribution}
