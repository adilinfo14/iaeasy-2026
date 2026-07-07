import { useState } from 'react'
import { demarrerEntrainement, suivreEntrainement } from '../api/client'
import LossChart from '../components/LossChart'

type Statut = 'inactif' | 'en_cours' | 'termine' | 'erreur'

export default function Entrainement() {
  const [historique, setHistorique] = useState<any[]>([])
  const [statut, setStatut] = useState<Statut>('inactif')
  const [erreur, setErreur] = useState<string | null>(null)

  async function lancer() {
    setHistorique([])
    setErreur(null)
    setStatut('en_cours')
    const { job_id } = await demarrerEntrainement()
    suivreEntrainement(
      job_id,
      (point) => setHistorique((h) => [...h, point]),
      (fin) => {
        setStatut(fin.status === 'termine' ? 'termine' : 'erreur')
        if (fin.erreur) setErreur(fin.erreur)
      },
    )
  }

  return (
    <div className="page">
      <h1>Entraînement — comprendre la perte (loss)</h1>
      <p className="page-intro">
        On entraîne en direct un petit modèle (CamemBERT distillé) à classer des avis clients en
        « positif » / « négatif », sur une quarantaine d'exemples jouets. La courbe ci-dessous
        montre la <strong>loss</strong> : plus elle descend, moins le modèle se trompe sur les
        exemples qu'il vient de voir.
      </p>

      <button onClick={lancer} disabled={statut === 'en_cours'}>
        {statut === 'en_cours' ? 'Entraînement en cours…' : 'Lancer un entraînement'}
      </button>

      {historique.length > 0 && <LossChart data={historique} />}
      {statut === 'termine' && <p className="succes">Entraînement terminé.</p>}
      {erreur && <p className="erreur">{erreur}</p>}

      <div className="explication-bloc">
        <h4>Pourquoi la courbe descend (ou pas)</h4>
        <ul>
          <li>
            <strong>Loss</strong> : un nombre qui mesure l'écart entre la prédiction du modèle et
            la bonne réponse. Plus il est petit, mieux c'est.
          </li>
          <li>
            <strong>Epoch</strong> : un passage complet sur tout le jeu de données. Ici
            l'entraînement fait plusieurs epochs sur les mêmes 40 exemples.
          </li>
          <li>
            <strong>Surapprentissage (overfitting)</strong> : si on entraînait beaucoup plus
            longtemps sur un aussi petit jeu de données, le modèle finirait par « apprendre par
            cœur » ces 40 phrases précises plutôt que la notion générale de sentiment.
          </li>
        </ul>
      </div>
    </div>
  )
}
