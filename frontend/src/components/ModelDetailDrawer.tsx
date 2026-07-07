import { useState } from 'react'
import { essayerModele } from '../api/client'

type Props = {
  modele: any
  onFermer: () => void
}

export default function ModelDetailDrawer({ modele, onFermer }: Props) {
  const [input, setInput] = useState(modele.cas_usage.input_exemple)
  const [resultat, setResultat] = useState<any>(null)
  const [enCours, setEnCours] = useState(false)
  const [erreur, setErreur] = useState<string | null>(null)

  async function essayer() {
    setEnCours(true)
    setErreur(null)
    setResultat(null)
    try {
      const r = await essayerModele(modele.id, input)
      setResultat(r)
    } catch (e: any) {
      setErreur(e.message)
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="drawer-overlay" onClick={onFermer}>
      <div className="drawer" onClick={(e) => e.stopPropagation()}>
        <button className="drawer-close" onClick={onFermer} aria-label="Fermer">×</button>
        <h2>{modele.nom}</h2>
        <p className="drawer-meta">
          {modele.famille.replace(/_/g, ' ')} · {modele.secteur} · {modele.taille}
        </p>
        <p className="drawer-description">{modele.description_pedagogique}</p>

        <h4>Cas d'usage</h4>
        <p>{modele.cas_usage.enonce}</p>

        <textarea value={input} onChange={(e) => setInput(e.target.value)} rows={3} />
        <button onClick={essayer} disabled={enCours}>
          {enCours ? 'Exécution en cours…' : 'Essayer ce modèle'}
        </button>

        {erreur && <div className="erreur">{erreur}</div>}
        {resultat && <pre className="resultat">{JSON.stringify(resultat, null, 2)}</pre>}
      </div>
    </div>
  )
}
