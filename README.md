# iaeasy — apprendre l'IA en la construisant

Plateforme pédagogique 100% souveraine (auto-hébergée, modèles open-source, CPU uniquement) :

1. **Catalogue** — 10 modèles couvrant 5 familles d'IA (LLM génératif, embeddings, NLP encodeur,
   vision, séries temporelles/anomalie), chacun avec une fiche pédagogique et un cas d'usage à
   essayer en direct.
2. **Entraînement** — fine-tuning léger en direct d'un petit modèle, avec la courbe de loss
   affichée en temps réel et expliquée.
3. **Parcours / Constructeur** — un parcours débloque progressivement 5 briques (LLM seul → RAG →
   Outil/MCP → Agent unique → Multi-agent) ; une fois débloquées, elles sont assemblables
   librement dans un canvas visuel (constructeur d'architecture), exécutable pour de vrai.

## Développement local

```bash
# backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend (autre terminal)
cd frontend
npm install
npm run dev
```

Le frontend proxy `/api` vers `http://127.0.0.1:8000` (voir `frontend/vite.config.ts`).
Ollama doit être joignable via la variable d'environnement `OLLAMA_URL`
(par défaut `http://127.0.0.1:11434`).

## Déploiement (homelab)

```bash
docker compose up -d --build
```

Le conteneur `iaeasy` rejoint le réseau externe `proxy-net` pour atteindre le conteneur `ollama`
déjà présent sur le homelab. Vhost nginx et route Cloudflare Tunnel : voir la documentation interne.
