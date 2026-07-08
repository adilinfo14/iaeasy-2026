import { useEffect, useState } from 'react'
import { executerGraphe, listerComposants, listerTemplates } from '../api/client'
import BrickCanvas from '../components/BrickCanvas'

function fusionnerExemple(template: any, exemple: any) {
  const nodes = template.nodes.map((n: any) => {
    const overrides = exemple.valeurs?.[n.id]
    return overrides ? { ...n, config: { ...n.config, ...overrides } } : n
  })
  return { ...template, nodes, _n: Date.now() }
}

export default function Constructeur() {
  const [composants, setComposants] = useState<any[]>([])
  const [templates, setTemplates] = useState<any[]>([])
  const [templateOuvert, setTemplateOuvert] = useState<string | null>(null)
  const [templateACharger, setTemplateACharger] = useState<any | null>(null)
  const [resultat, setResultat] = useState<any>(null)
  const [briqueSelectionnee, setBriqueSelectionnee] = useState<string | null>(null)
  const [noeudSelectionne, setNoeudSelectionne] = useState<string | null>(null)
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
    try {
      const r = await executerGraphe(nodes, edges)
      setResultat(r)
    } catch (e: any) {
      setErreur(e.message)
    }
  }

  function afficherComposant(brique: string, noeudId?: string) {
    setBriqueSelectionnee(brique)
    setNoeudSelectionne(noeudId ?? null)
  }

  function chargerExemple(template: any, exemple: any) {
    setResultat(null)
    setErreur(null)
    setBriqueSelectionnee(null)
    setNoeudSelectionne(null)
    setTemplateACharger(fusionnerExemple(template, exemple))
  }

  const composantAffiche = composants.find((c) => c.id === briqueSelectionnee)
  const artefactNoeud = noeudSelectionne && resultat?.resultats_par_noeud?.[noeudSelectionne]

  return (
    <div className="page page-constructeur">
      <h1>Constructeur d'architecture</h1>
      <p className="page-intro">
        Le mode « architecte » : 10 modèles d'architecture réels, chacun avec ses avantages et ses
        inconvénients. Ouvrez-en un, choisissez un exemple pour le charger sur le canvas, puis
        exécutez et inspectez ce que produit chaque étape intermédiaire.
      </p>

      <div className="templates-liste">
        {templates.map((t) => {
          const ouvert = templateOuvert === t.id
          return (
            <div key={t.id} className={ouvert ? 'template-carte ouverte' : 'template-carte'}>
              <button className="template-entete" onClick={() => setTemplateOuvert(ouvert ? null : t.id)}>
                <strong>{t.titre}</strong>
                <span>{t.description}</span>
              </button>
              {ouvert && (
                <div className="template-details">
                  <div className="avantages-inconvenients">
                    <div>
                      <h5>✅ Avantages</h5>
                      <ul className="liste-simple">
                        {t.avantages.map((a: string, i: number) => (
                          <li key={i}>{a}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5>⚠️ Inconvénients</h5>
                      <ul className="liste-simple">
                        {t.inconvenients.map((a: string, i: number) => (
                          <li key={i}>{a}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  <p className="texte-muted">Charger sur le canvas avec l'exemple :</p>
                  <div className="exemples-chips">
                    {t.exemples.map((ex: any, i: number) => (
                      <button key={i} className="chip" onClick={() => chargerExemple(t, ex)}>
                        {ex.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>

      <BrickCanvas
        composants={composants}
        templateACharger={templateACharger}
        resultatsParNoeud={resultat?.resultats_par_noeud || null}
        onExecuter={executer}
        onComposantInfo={afficherComposant}
      />

      {erreur && <p className="erreur">{erreur}</p>}

      {templateACharger && (
        <div className="explication-bloc">
          <h4>Comment ça marche, étape par étape</h4>
          <p className="texte-muted">
            Ce graphe n'a pas encore été exécuté — voici ce que chaque brique va faire, dans l'ordre,
            avant même de cliquer sur « Exécuter le graphe ».
          </p>
          <ol className="liste-etapes-trace">
            {templateACharger.nodes.map((n: any, i: number) => {
              const c = composants.find((c) => c.id === n.type)
              return (
                <li key={i}>
                  {c?.icone} <strong>{c?.titre || n.type}</strong> — {c?.description}
                </li>
              )
            })}
          </ol>
        </div>
      )}

      {composantAffiche && (
        <div className="explication-bloc">
          <h4>
            {composantAffiche.icone} {composantAffiche.titre}
          </h4>
          <p>{composantAffiche.description}</p>
          <p className="texte-muted">
            <strong>Entrée / sortie :</strong> {composantAffiche.entree_sortie}
          </p>
          {artefactNoeud && (
            <>
              <h4>Ce que ce nœud a produit lors de la dernière exécution</h4>
              <pre className="resultat">{JSON.stringify(artefactNoeud, null, 2)}</pre>
            </>
          )}
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
