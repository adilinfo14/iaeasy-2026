import { useEffect, useState } from 'react'
import { debloquerBrique, executerGraphe, lireProgression, listerBriques } from '../api/client'

export default function Parcours() {
  const [briques, setBriques] = useState<any[]>([])
  const [debloquees, setDebloquees] = useState<string[]>([])
  const [resultats, setResultats] = useState<Record<string, any>>({})
  const [enCours, setEnCours] = useState<string | null>(null)

  useEffect(() => {
    listerBriques().then(setBriques)
    lireProgression().then((p) => setDebloquees(p.debloquees))
  }, [])

  async function essayerBrique(brique: any) {
    setEnCours(brique.id)
    try {
      const graphe = construireGraphePourBrique(brique.id)
      const resultat = await executerGraphe(graphe.nodes, graphe.edges)
      setResultats((r) => ({ ...r, [brique.id]: resultat }))
      const suivante = nextBriqueId(briques, brique.id)
      const p = await debloquerBrique(suivante)
      setDebloquees(p.debloquees)
    } catch (e: any) {
      setResultats((r) => ({ ...r, [brique.id]: { erreur: e.message } }))
    } finally {
      setEnCours(null)
    }
  }

  return (
    <div className="page">
      <h1>Parcours — débloquer les briques une à une</h1>
      <p className="page-intro">
        Chaque étape débloque la brique suivante : impossible de passer au multi-agent avant
        d'avoir vu ce qu'apporte chaque brique précédente.
      </p>

      <ol className="parcours-liste">
        {briques.map((b) => {
          const debloquee = debloquees.includes(b.id)
          const prerequisOk = (b.prerequis as string[]).every((p) => debloquees.includes(p))
          return (
            <li
              key={b.id}
              className={debloquee ? 'etape debloquee' : prerequisOk ? 'etape disponible' : 'etape verrouillee'}
            >
              <h3>
                {b.ordre}. {b.titre}
              </h3>
              <p>{b.description_pedagogique}</p>
              {prerequisOk && (
                <button onClick={() => essayerBrique(b)} disabled={enCours === b.id}>
                  {enCours === b.id ? 'Exécution…' : 'Essayer cette brique'}
                </button>
              )}
              {!prerequisOk && <p className="verrou">🔒 Termine l'étape précédente pour débloquer.</p>}
              {resultats[b.id] && <pre className="resultat">{JSON.stringify(resultats[b.id], null, 2)}</pre>}
            </li>
          )
        })}
      </ol>
    </div>
  )
}

function nextBriqueId(briques: any[], courant: string): string {
  const idx = briques.findIndex((b) => b.id === courant)
  return briques[idx + 1]?.id ?? courant
}

function construireGraphePourBrique(id: string) {
  switch (id) {
    case 'llm_seul':
      return {
        nodes: [{ id: '1', type: 'llm_seul', config: { prompt: "Explique en une phrase ce qu'est un LLM." } }],
        edges: [],
      }
    case 'rag':
      return {
        nodes: [{ id: '1', type: 'rag', config: { prompt: "Qu'est-ce que le RAG ?" } }],
        edges: [],
      }
    case 'outil_mcp':
      return {
        nodes: [{ id: '1', type: 'outil_mcp', config: { outil: 'calculatrice', expression: '12 * (3 + 4)' } }],
        edges: [],
      }
    case 'agent_unique':
      return {
        nodes: [{ id: '1', type: 'agent_unique', config: { prompt: 'Combien font 15 fois (2 + 6) ?' } }],
        edges: [],
      }
    case 'multi_agent':
      return {
        nodes: [
          { id: '1', type: 'multi_agent', config: { prompt: "Résume ce qu'est un agent IA pour un débutant." } },
        ],
        edges: [],
      }
    default:
      return { nodes: [], edges: [] }
  }
}
