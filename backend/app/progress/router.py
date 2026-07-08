from fastapi import APIRouter, Path

from . import store

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("")
def lire():
    return {"debloquees": store.get_debloquees()}


@router.post("/debloquer/{brique_id}")
def debloquer(brique_id: str = Path(max_length=64)):
    return {"debloquees": store.debloquer(brique_id)}


@router.get("/badges")
def badges():
    return {"badges": store.get_badges()}


@router.post("/badges/{brique_id}")
def valider_badge(brique_id: str = Path(max_length=64)):
    return {"badges": store.valider_badge(brique_id)}
