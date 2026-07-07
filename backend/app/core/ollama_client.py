import httpx

from .config import settings


class OllamaClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.ollama_url

    async def generate(self, model: str, prompt: str, stream: bool = False) -> str:
        # num_predict borne la longueur de réponse : sur CPU pur, un modèle 7B sans limite
        # peut mettre plusieurs minutes à générer une réponse — inacceptable dans un outil
        # pédagogique interactif.
        async with httpx.AsyncClient(timeout=280) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": 300},
                },
            )
            resp.raise_for_status()
            return resp.json()["response"]

    async def chat(self, model: str, messages: list[dict], tools: list[dict] | None = None) -> dict:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": 300},
        }
        if tools:
            payload["tools"] = tools
        async with httpx.AsyncClient(timeout=280) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            return resp.json()["message"]

    async def embed(self, model: str, text: str) -> list[float]:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{self.base_url}/api/embeddings",
                json={"model": model, "prompt": text},
            )
            resp.raise_for_status()
            return resp.json()["embedding"]


ollama = OllamaClient()
