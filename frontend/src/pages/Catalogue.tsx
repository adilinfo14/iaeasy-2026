import { useEffect, useState } from 'react'
import { listerModeles } from '../api/client'
import ModelCard from '../components/ModelCard'
import ModelDetailDrawer from '../components/ModelDetailDrawer'

export default function Catalogue() {
  const [modeles, setModeles] = useState<any[]>([])
  const [selection, setSelection] = useState<any | null>(null)
  const [filtreFamille, setFiltreFamille] = useState<string>('toutes')

  useEffect(() => {
    listerModeles().then(setModeles)
  }, [])

  const familles = ['toutes', ...Array.from(new Set(modeles.map((m) => m.famille)))]
  const visibles = filtreFamille === 'toutes' ? modeles : modeles.filter((m) => m.famille === filtreFamille)

  return (
    <div className="page">
      <h1>Catalogue de modèles</h1>
      <p className="page-intro">
        Dix modèles, cinq familles d'IA différentes (pas seulement des chatbots) : à chaque fiche
        son secteur, sa description pédagogique et un cas d'usage à essayer en direct.
      </p>

      <div className="filtres">
        {familles.map((f) => (
          <button
            key={f}
            className={f === filtreFamille ? 'filtre actif' : 'filtre'}
            onClick={() => setFiltreFamille(f)}
          >
            {f.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      <div className="model-grid">
        {visibles.map((m) => (
          <ModelCard key={m.id} modele={m} onOuvrir={setSelection} />
        ))}
      </div>

      {selection && <ModelDetailDrawer modele={selection} onFermer={() => setSelection(null)} />}
    </div>
  )
}
