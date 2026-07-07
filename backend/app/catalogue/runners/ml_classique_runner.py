import asyncio

import numpy as np


def _toy_dossiers_credit():
    rng = np.random.RandomState(3)
    n = 60
    revenu = rng.normal(2800, 700, n).clip(900, 6000)
    endettement = rng.normal(0.32, 0.12, n).clip(0.05, 0.8)
    incidents = rng.poisson(0.6, n)
    risque = (
        (endettement > 0.4).astype(int) + (incidents >= 2).astype(int) + (revenu < 1800).astype(int) >= 2
    ).astype(int)
    return revenu, endettement, incidents, risque


def _scoring_sync() -> dict:
    from sklearn.linear_model import LogisticRegression

    revenu, endettement, incidents, risque = _toy_dossiers_credit()
    X = np.column_stack([revenu, endettement, incidents])
    modele = LogisticRegression()
    modele.fit(X, risque)

    dossier_teste = {"revenu_mensuel": 1900, "taux_endettement": 0.45, "incidents_paiement": 2}
    nouveau = np.array([[dossier_teste["revenu_mensuel"], dossier_teste["taux_endettement"], dossier_teste["incidents_paiement"]]])
    proba_risque = float(modele.predict_proba(nouveau)[0][1])

    return {
        "type": "scoring_credit",
        "nb_dossiers_entrainement": len(risque),
        "nb_dossiers_a_risque": int(risque.sum()),
        "dossier_teste": dossier_teste,
        "probabilite_risque": round(proba_risque, 3),
        "decision_suggeree": "Refus / étude approfondie" if proba_risque > 0.5 else "Accord",
        "explication": "Modèle (régression logistique) entraîné en direct sur 60 dossiers jouets — "
        "variables utilisées : revenu mensuel, taux d'endettement, incidents de paiement.",
    }


def _toy_notes_films():
    matrice = np.array(
        [
            [5, 4, 0, 1, 0],
            [4, 5, 0, 0, 1],
            [0, 0, 5, 4, 0],
            [1, 0, 4, 5, 0],
            [0, 1, 0, 0, 5],
        ],
        dtype=float,
    )
    films = ["Film A (action)", "Film B (action)", "Film C (drame)", "Film D (drame)", "Film E (comédie)"]
    return matrice, films


def _recommandation_sync() -> dict:
    from sklearn.decomposition import NMF

    matrice, films = _toy_notes_films()
    modele = NMF(n_components=2, init="random", random_state=0, max_iter=500)
    W = modele.fit_transform(matrice)
    H = modele.components_
    matrice_reconstruite = W @ H

    utilisateur_idx = 0
    deja_notes = matrice[utilisateur_idx] > 0
    scores = matrice_reconstruite[utilisateur_idx].copy()
    scores[deja_notes] = -1
    recommande_idx = int(np.argmax(scores))

    return {
        "type": "recommandation",
        "utilisateur": "Utilisateur 1",
        "films_deja_notes": [
            {"film": f, "note": int(n)} for f, n in zip(films, matrice[utilisateur_idx]) if n > 0
        ],
        "film_recommande": films[recommande_idx],
        "score_prevu": round(float(scores[recommande_idx]), 2),
        "explication": "Factorisation de matrice (NMF) entraînée en direct sur les notes de 5 utilisateurs "
        "jouets, pour deviner les goûts non exprimés de l'utilisateur 1.",
    }


async def run_scoring_credit() -> dict:
    return await asyncio.to_thread(_scoring_sync)


async def run_recommandation() -> dict:
    return await asyncio.to_thread(_recommandation_sync)
