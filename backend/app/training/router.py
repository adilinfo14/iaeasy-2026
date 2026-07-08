import asyncio
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from . import trainer

router = APIRouter(prefix="/training", tags=["training"])


class DemarrerRequest(BaseModel):
    scenario_id: str = Field(max_length=64)


class TesterRequest(BaseModel):
    entree: str | None = Field(default=None, max_length=500)


@router.get("/scenarios")
def scenarios():
    return trainer.lister_scenarios()


@router.get("/scenarios/{scenario_id}/apercu")
def apercu(scenario_id: str):
    try:
        return trainer.apercu_donnees(scenario_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/start")
def demarrer(requete: DemarrerRequest):
    try:
        job_id = trainer.demarrer_entrainement(requete.scenario_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"job_id": job_id}


@router.get("/{job_id}")
def etat(job_id: str):
    job = trainer.get_job(job_id)
    if job is None:
        return {"status": "inconnu"}
    return job


@router.post("/{job_id}/tester")
def tester(job_id: str, requete: TesterRequest):
    try:
        return trainer.tester_modele(job_id, requete.entree)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/{job_id}/stream")
async def stream(job_id: str):
    async def event_generator():
        envoyes = 0
        while True:
            job = trainer.get_job(job_id)
            if job is None:
                yield "event: erreur\ndata: job inconnu\n\n"
                break

            history = job["history"]
            while envoyes < len(history):
                yield f"event: loss\ndata: {json.dumps(history[envoyes])}\n\n"
                envoyes += 1

            if job["status"] != "en_cours":
                payload = json.dumps({"status": job["status"], "erreur": job.get("erreur")})
                yield f"event: fin\ndata: {payload}\n\n"
                break

            await asyncio.sleep(0.4)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
