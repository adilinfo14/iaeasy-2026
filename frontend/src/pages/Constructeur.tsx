import { useEffect, useState } from 'react'
import { executerGraphe, listerComposants, listerTemplates } from '../api/client'
import BrickCanvas from '../components/BrickCanvas'

export default function Constructeur() {
  const [composants, setComposants] = useState<any[]>([])
  const [templates, setTemplates] = useState<any[]>([])
  const [templateACharger, setTemplateACharger] = useState<any | null>(null)
  const [resultat, setResultat] = useState<any>(null)
  const [noeudSelectionne, setNoeudSelectionne] = useState<{ id: string; brique: string } | null>(null)
  const [erreur, setErreur] = useState<string | null>(null)

  useEffect(() => {
    listerComposants().then(setComposants)
    listerTemplates().then(setTemplates)
  }, [])

  async function executer(
    nodes: { id: string; type: string; config: Record<string, unknown> }[],
    edges: { source: string; target: string }[],
  ) {
    setErreur(null)
    setResultat(null)
    setNoeudSelectionne(null)
    try {
      const r = await executerGraphe(nodes, edges)
      setResultat(r)
    } catch (e: any) {
      setErreur(e.message)
    }
  }

  const artefactNoeud = noeudSelectionne && resultat?.resultats_par_noeud?.[noeudSelectionne.id]

  return (
    <div className="page page-constructeur">
      <h1>Constructeur d'architecture</h1>
      <p className="page-intro">
        Le mode « architecte » : chargez un modèle d'architecture réel (RAG documentaire, agent
        avec outils, pipeline multi-agent) ou construisez le vôtre à partir des briques
        granulaires, puis exécutez et inspectez ce que produit chaque étape intermédiaire.
      </p>

      <div className="templates-liste">
        {templates.map((t) => (
          <button key={t.id} className="template-carte" onClick={() => setTemplateACharger({ ...t, _n: Date.now() })}>
            <strong>{t.titre}</strong>
            <span>{t.description}</span>
          </button>
        ))}
      </div>

      <BrickCanvas
        composants={composants}
        templateACharger={templateACharger}
        resultatsParNoeud={resultat?.resultats_par_noeud || null}
        onExecuter={executer}
        onNodeClick={(id, brique) => setNoeudSelectionne({ id, brique })}
      />

      {erreur && <p className="erreur">{erreur}</p>}

      {artefactNoeud && (
        <div className="explication-bloc">
          <h4>Ce qu'a produit ce nœud ({noeudSelectionne!.brique})</h4>
          <pre className="resultat">{JSON.stringify(artefactNoeud, null, 2)}</pre>
        </div>
      )}

      {resultat && (
        <div className="explication-bloc">
          <h4>Déroulé complet</h4>
          <ol>
            {resultat.etapes.map((e: any, i: number) => (
              <li key={i}>
                <strong>{e.brique}</strong> — {e.detail}
              </li>
            ))}
          </ol>
          {resultat.reponse_finale && (
            <>
              <h4>Réponse finale</h4>
              <p className="traduction-cible">{resultat.reponse_finale}</p>
            </>
          )}
        </div>
      )}
    </div>
  )
}
