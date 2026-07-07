import csv
import threading
import uuid
from pathlib import Path

_jobs: dict[str, dict] = {}

_DATASET_PATH = Path(__file__).parent / "datasets" / "toy_sentiment_fr.csv"
_BASE_MODEL = "cmarkea/distilcamembert-base"


def _load_dataset() -> tuple[list[str], list[int]]:
    textes, labels = [], []
    with open(_DATASET_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            textes.append(row["texte"])
            labels.append(int(row["label"]))
    return textes, labels


def _entrainer(job_id: str) -> None:
    try:
        from datasets import Dataset
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            Trainer,
            TrainerCallback,
            TrainingArguments,
        )

        class LossCallback(TrainerCallback):
            def on_log(self, args, state, control, logs=None, **kwargs):
                if logs and "loss" in logs:
                    _jobs[job_id]["history"].append(
                        {
                            "step": state.global_step,
                            "epoch": round(state.epoch or 0, 2),
                            "loss": round(logs["loss"], 4),
                        }
                    )

        textes, labels = _load_dataset()
        tokenizer = AutoTokenizer.from_pretrained(_BASE_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(_BASE_MODEL, num_labels=2)

        encodings = tokenizer(textes, truncation=True, padding=True, max_length=64)
        dataset = Dataset.from_dict({**encodings, "labels": labels})

        args = TrainingArguments(
            output_dir=f"/tmp/iaeasy-training-{job_id}",
            per_device_train_batch_size=8,
            num_train_epochs=4,
            logging_steps=1,
            save_strategy="no",
            report_to=[],
            disable_tqdm=True,
        )

        trainer = Trainer(model=model, args=args, train_dataset=dataset, callbacks=[LossCallback()])
        trainer.train()

        _jobs[job_id]["status"] = "termine"
    except Exception as exc:  # noqa: BLE001 — l'erreur doit remonter côté IHM, pas planter le thread
        _jobs[job_id]["status"] = "erreur"
        _jobs[job_id]["erreur"] = str(exc)


def demarrer_entrainement() -> str:
    job_id = uuid.uuid4().hex[:8]
    _jobs[job_id] = {"status": "en_cours", "history": [], "erreur": None}
    threading.Thread(target=_entrainer, args=(job_id,), daemon=True).start()
    return job_id


def get_job(job_id: str) -> dict | None:
    return _jobs.get(job_id)
