import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from . import trainer

router = APIRouter(prefix="/training", tags=["training"])


@router.post("/start")
def demarrer():
    job_id = trainer.demarrer_entrainement()
    return {"job_id": job_id}


@router.get("/{job_id}")
def etat(job_id: str):
    job = trainer.get_job(job_id)
    if job is None:
        return {"status": "inconnu"}
    return job


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
