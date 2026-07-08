from fastapi import APIRouter

from .fiches import get_metiers

router = APIRouter(prefix="/metiers", tags=["metiers"])


@router.get("")
def metiers():
    return get_metiers()
