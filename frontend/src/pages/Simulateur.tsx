import { useState } from 'react'
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { comparerModeles } from '../api/client'

const EXEMPLES = [
  "Explique en 3 phrases ce qu'est la garantie décennale.",
  'Rédige un message pour prévenir un client d\'un retard de chantier.',
  'Combien font 17 fois 23 ?',
]

export default function Simulateur() {
  const [prompt, setPrompt] = useState(EXEMPLES[0])
  const [enCours, setEnCours] = useState(false)
  const [resultat, setResultat] = useState<any>(null)
  const [erreur, setErreur] = useState<string | null>(null)

  async function lancer() {
    setEnCours(true)
    setErreur(null)
    setResultat(null)
    try {
      const r = await comparerModeles(prompt)
      setResultat(r)
    } catch (e: any) {
      setErreur(e.message)
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="page page-simulateur">
      <h1>⚖️ Simulateur coût / latence des modèles</h1>
      <p className="page-intro">
        Le même prompt est envoyé, l'un après l'autre, aux 3 modèles disponibles sur ce serveur. La
        <strong> durée est une vraie mesure</strong>, prise en direct sur cette machine — pas une
        estimation. L'énergie affichée, elle, est une <strong>approximation illustrative</strong>{' '}
        proportionnelle au nombre de paramètres, pas une mesure réelle de consommation.
      </p>

      <div className="exemples-chips">
        {EXEMPLES.map((ex, i) => (
          <button key={i} className={ex === prompt ? 'chip actif' : 'chip'} onClick={() => setPrompt(ex)}>
            {ex.length > 40 ? `${ex.slice(0, 40)}…` : ex}
          </button>
        ))}
      </div>

      <textarea
        className="simulateur-prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={3}
        maxLength={300}
      />

      <button onClick={lancer} disabled={enCours || !prompt.trim()}>
        {enCours ? 'Comparaison en cours (environ 1 minute)…' : 'Lancer la comparaison'}
      </button>

      {erreur && <p className="erreur">{erreur}</p>}

      {resultat && (
        <>
          <div className="simulateur-graphique">
            <h4>Durée de réponse mesurée (secondes)</h4>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={resultat.resultats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="nom" />
                <YAxis label={{ value: 'secondes', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Bar dataKey="duree_secondes" name="Durée (s)" fill="#4f7cff" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="simulateur-graphique">
            <h4>Estimation d'énergie relative (illustrative, % du plus gros modèle)</h4>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={resultat.resultats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="nom" />
                <YAxis label={{ value: '%', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="estimation_energie_relative_pourcent" name="Énergie estimée (%)" fill="#fb923c" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="explication-bloc">
            <h4>Détail par modèle</h4>
            {resultat.resultats.map((r: any) => (
              <div key={r.id} className="simulateur-detail">
                <h5>{r.nom} — ~{r.parametres_milliards} milliards de paramètres</h5>
                <p className="texte-muted">
                  {r.duree_secondes}s pour {r.longueur_reponse} caractères de réponse
                </p>
                <p className="traduction-cible">{r.reponse}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
