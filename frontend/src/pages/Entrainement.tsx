import { useEffect, useState } from 'react'
import {
  apercuDonnees,
  demarrerEntrainement,
  listerScenariosEntrainement,
  suivreEntrainement,
  testerModeleEntraine,
} from '../api/client'
import LossChart from '../components/LossChart'

type Statut = 'inactif' | 'en_cours' | 'termine' | 'erreur'

export default function Entrainement() {
  const [scenarios, setScenarios] = useState<any[]>([])
  const [scenarioId, setScenarioId] = useState<string | null>(null)
  const [apercu, setApercu] = useState<any>(null)
  const [historique, setHistorique] = useState<any[]>([])
  const [statut, setStatut] = useState<Statut>('inactif')
  const [erreur, setErreur] = useState<string | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)
  const [testEntree, setTestEntree] = useState('')
  const [testResultat, setTestResultat] = useState<any>(null)

  useEffect(() => {
    listerScenariosEntrainement().then((s) => {
      setScenarios(s)
      if (s.length > 0) choisirScenario(s[0].id)
    })
  }, [])

  async function choisirScenario(id: string) {
    setScenarioId(id)
    setHistorique([])
    setStatut('inactif')
    setErreur(null)
    setJobId(null)
    setTestResultat(null)
    setApercu(await apercuDonnees(id))
  }

  async function lancer() {
    if (!scenarioId) return
    setHistorique([])
    setErreur(null)
    setTestResultat(null)
    setStatut('en_cours')
    const { job_id } = await demarrerEntrainement(scenarioId)
    setJobId(job_id)
    suivreEntrainement(
      job_id,
      (point) => setHistorique((h) => [...h, point]),
      (fin) => {
        setStatut(fin.status === 'termine' ? 'termine' : 'erreur')
        if (fin.erreur) setErreur(fin.erreur)
      },
    )
  }

  async function tester() {
    if (!jobId) return
    try {
      const r = await testerModeleEntraine(jobId, testEntree)
      setTestResultat(r)
    } catch (e: any) {
      setTestResultat({ erreur: e.message })
    }
  }

  const scenario = scenarios.find((s) => s.id === scenarioId)

  return (
    <div className="page">
      <h1>Entraînement — comprendre la perte (loss)</h1>
      <p className="page-intro">
        Trois scénarios réels, trois familles de modèles différentes. Choisissez-en un pour voir
        exactement quelles données servent à l'entraînement, avant de lancer et de tester le
        résultat vous-même.
      </p>

      <div className="filtres">
        {scenarios.map((s) => (
          <button
            key={s.id}
            className={s.id === scenarioId ? 'filtre actif' : 'filtre'}
            onClick={() => choisirScenario(s.id)}
          >
            {s.titre}
          </button>
        ))}
      </div>

      {scenario && (
        <div className="explication-bloc">
          <h4>Cas d'usage</h4>
          <p>{scenario.cas_usage}</p>
          <p className="texte-muted">
            <strong>Type d'algorithme :</strong> {scenario.famille_algo} — {scenario.modele_base}
          </p>
        </div>
      )}

      {apercu && (
        <div className="explication-bloc">
          <h4>
            Les données d'entraînement ({apercu.total} exemples, {apercu.lignes.length} affichés)
          </h4>
          <div className="table-scroll">
            <table className="table-donnees">
              <thead>
                <tr>
                  {apercu.colonnes.map((c: string) => (
                    <th key={c}>{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {apercu.lignes.map((ligne: any, i: number) => (
                  <tr key={i}>
                    {apercu.colonnes.map((c: string) => (
                      <td key={c}>{String(ligne[c])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <button onClick={lancer} disabled={statut === 'en_cours' || !scenarioId}>
        {statut === 'en_cours' ? 'Entraînement en cours…' : 'Lancer cet entraînement'}
      </button>

      {historique.length > 0 && <LossChart data={historique} />}
      {statut === 'termine' && <p className="succes">Entraînement terminé — testez-le ci-dessous.</p>}
      {erreur && <p className="erreur">{erreur}</p>}

      {statut === 'termine' && jobId && (
        <div className="explication-bloc">
          <h4>Testez le modèle que vous venez d'entraîner</h4>
          <input
            className="input-texte"
            value={testEntree}
            onChange={(e) => setTestEntree(e.target.value)}
            placeholder={
              scenarioId === 'prevision_ca'
                ? 'Numéro du mois à prévoir (ex: 20)'
                : 'Tapez votre propre exemple…'
            }
          />
          <button onClick={tester}>Tester</button>
          {testResultat && !testResultat.erreur && (
            <p className="traduction-cible">
              → {testResultat.prediction}
              {testResultat.confiance != null && ` (confiance ${(testResultat.confiance * 100).toFixed(0)}%)`}
            </p>
          )}
          {testResultat?.erreur && <p className="erreur">{testResultat.erreur}</p>}
        </div>
      )}

      <div className="explication-bloc">
        <h4>Pourquoi la courbe descend (ou pas)</h4>
        <ul>
          <li>
            <strong>Loss</strong> : un nombre qui mesure l'écart entre la prédiction du modèle et
            la bonne réponse. Plus il est petit, mieux c'est — et c'est le même principe, qu'il
            s'agisse d'un réseau de neurones ou d'un algorithme classique comme la régression
            logistique ou linéaire.
          </li>
          <li>
            <strong>Epoch</strong> : un passage complet sur tout le jeu de données.
          </li>
          <li>
            <strong>Surapprentissage (overfitting)</strong> : si on entraînait beaucoup plus
            longtemps sur un aussi petit jeu de données, le modèle finirait par « apprendre par
            cœur » ces exemples précis plutôt que la notion générale recherchée.
          </li>
        </ul>
      </div>
    </div>
  )
}
