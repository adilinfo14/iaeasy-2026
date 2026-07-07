import { useEffect, useState } from 'react'
import { executerGraphe, lireProgression, listerBriques } from '../api/client'
import BrickCanvas from '../components/BrickCanvas'

export default function Constructeur() {
  const [briques, setBriques] = useState<any[]>([])
  const [debloquees, setDebloquees] = useState<string[]>([])
  const [resultat, setResultat] = useState<any>(null)
  const [erreur, setErreur] = useState<string | null>(null)

  useEffect(() => {
    listerBriques().then(setBriques)
    lireProgression().then((p) => setDebloquees(p.debloquees))
  }, [])

  const disponibles = briques.filter((b) => debloquees.includes(b.id))

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

  return (
    <div className="page page-constructeur">
      <h1>Constructeur d'architecture</h1>
      <p className="page-intro">
        Ajoutez des briques débloquées sur le canvas, reliez-les, puis exécutez le graphe pour de
        vrai — ce n'est pas un schéma, chaque brique appelle réellement un modèle ou un outil.
      </p>

      {disponibles.length === 0 && (
        <p className="verrou">Aucune brique débloquée pour l'instant — commencez par le Parcours.</p>
      )}

      <BrickCanvas briquesDisponibles={disponibles} onExecuter={executer} />

      {erreur && <p className="erreur">{erreur}</p>}
      {resultat && (
        <div className="explication-bloc">
          <h4>Déroulé pas à pas</h4>
          <ol>
            {resultat.etapes.map((e: any, i: number) => (
              <li key={i}>
                <strong>{e.brique}</strong> — {e.detail}
              </li>
            ))}
          </ol>
          <h4>Réponse finale</h4>
          <p>{resultat.reponse_finale}</p>
        </div>
      )}
    </div>
  )
}
