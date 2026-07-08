from fastapi import APIRouter, Path

from . import store

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("")
def lire():
    return {"debloquees": store.get_debloquees()}


@router.post("/debloquer/{brique_id}")
def debloquer(brique_id: str = Path(max_length=64)):
    return {"debloquees": store.debloquer(brique_id)}
