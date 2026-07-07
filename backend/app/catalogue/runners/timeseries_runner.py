import asyncio

import numpy as np

_chronos_pipeline = None


def _toy_serie_economique() -> list[float]:
    mois = np.arange(24)
    tendance = 100 + mois * 2.5
    saison = 8 * np.sin(2 * np.pi * mois / 12)
    bruit = np.random.RandomState(42).normal(0, 3, size=len(mois))
    return (tendance + saison + bruit).tolist()


def _prevoir_sync(model_ref: str) -> dict:
    global _chronos_pipeline
    import torch

    if _chronos_pipeline is None:
        from chronos import BaseChronosPipeline

        _chronos_pipeline = BaseChronosPipeline.from_pretrained(
            model_ref, device_map="cpu", torch_dtype=torch.float32
        )

    historique = _toy_serie_economique()
    context = torch.tensor(historique)
    horizon = 6
    quantiles, mean = _chronos_pipeline.predict_quantiles(
        inputs=context, prediction_length=horizon, quantile_levels=[0.1, 0.5, 0.9]
    )

    return {
        "type": "prevision_serie_temporelle",
        "historique": [round(v, 1) for v in historique],
        "prevision_mediane": [round(v, 1) for v in mean[0].tolist()],
        "intervalle_bas": [round(v, 1) for v in quantiles[0, :, 0].tolist()],
        "intervalle_haut": [round(v, 1) for v in quantiles[0, :, 2].tolist()],
        "explication": "Prévision des 6 prochains mois avec intervalle de confiance (10e-90e centile).",
    }


def _toy_capteur_mecanique() -> list[float]:
    rng = np.random.RandomState(7)
    mesures = rng.normal(loc=0.5, scale=0.05, size=150)
    mesures[60] = 1.4
    mesures[120] = 1.6
    return mesures.tolist()


def _detect_anomalie_sync() -> dict:
    from sklearn.ensemble import IsolationForest

    mesures = _toy_capteur_mecanique()
    X = np.array(mesures).reshape(-1, 1)
    modele = IsolationForest(contamination=0.02, random_state=7)
    modele.fit(X)
    scores = modele.decision_function(X)
    predictions = modele.predict(X)

    anomalies = [
        {"indice": i, "valeur": round(mesures[i], 3), "score": round(float(scores[i]), 3)}
        for i, p in enumerate(predictions)
        if p == -1
    ]

    return {
        "type": "detection_anomalie",
        "nb_mesures": len(mesures),
        "mesures": [round(v, 3) for v in mesures],
        "anomalies_detectees": anomalies,
        "explication": "Modèle entraîné en direct sur ces mesures : les points identifiés comme "
        "anomalie s'écartent statistiquement du comportement vibratoire normal de la machine.",
    }


def _toy_transactions_bancaires() -> list[float]:
    rng = np.random.RandomState(11)
    montants = rng.normal(45, 20, 200).clip(2, 300)
    montants[15] = 2450
    montants[120] = 1875
    return montants.tolist()


def _detect_fraude_sync() -> dict:
    from sklearn.ensemble import IsolationForest

    montants = _toy_transactions_bancaires()
    X = np.array(montants).reshape(-1, 1)
    modele = IsolationForest(contamination=0.015, random_state=11)
    modele.fit(X)
    scores = modele.decision_function(X)
    predictions = modele.predict(X)

    anomalies = [
        {"indice": i, "montant": round(montants[i], 2), "score": round(float(scores[i]), 3)}
        for i, p in enumerate(predictions)
        if p == -1
    ]

    return {
        "type": "detection_anomalie",
        "nb_mesures": len(montants),
        "mesures": [round(v, 2) for v in montants],
        "anomalies_detectees": anomalies,
        "explication": "Modèle entraîné en direct sur l'historique de montants de transactions : les "
        "valeurs identifiées s'écartent statistiquement du comportement d'achat habituel du client.",
    }


async def run_prevision(model_ref: str) -> dict:
    return await asyncio.to_thread(_prevoir_sync, model_ref)


async def run_anomalie() -> dict:
    return await asyncio.to_thread(_detect_anomalie_sync)


async def run_fraude() -> dict:
    return await asyncio.to_thread(_detect_fraude_sync)
