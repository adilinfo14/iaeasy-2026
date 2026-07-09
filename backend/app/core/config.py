import os


class Settings:
    ollama_url: str = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
    data_dir: str = os.environ.get("IAEASY_DATA_DIR", "/data")
    hf_cache_dir: str = os.environ.get("HF_HOME", "/data/hf_cache")
    # Pas de valeur par défaut en dur ici : ce dépôt est public, le mot de passe ne vit que dans
    # un fichier .env non versionné sur le serveur. Vide = panneau admin inaccessible.
    admin_password: str = os.environ.get("IAEASY_ADMIN_PASSWORD", "")


settings = Settings()

os.makedirs(settings.data_dir, exist_ok=True)
os.makedirs(settings.hf_cache_dir, exist_ok=True)
os.environ.setdefault("HF_HOME", settings.hf_cache_dir)
