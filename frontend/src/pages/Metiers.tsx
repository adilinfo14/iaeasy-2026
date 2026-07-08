import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listerMetiers } from '../api/client'

export default function Metiers() {
  const [metiers, setMetiers] = useState<any[]>([])
  const [ouvert, setOuvert] = useState<string | null>(null)

  useEffect(() => {
    listerMetiers().then(setMetiers)
  }, [])

  return (
    <div className="page page-metiers">
      <h1>🧭 L'IA dans mon métier</h1>
      <p className="page-intro">
        Pas de jargon, pas de promesse abstraite : pour chaque métier, 3 cas d'usage concrets déjà
        présents sur ce site, avec un lien direct pour aller les essayer soi-même.
      </p>

      <div className="templates-liste">
        {metiers.map((m) => {
          const estOuvert = ouvert === m.id
          return (
            <div key={m.id} className={estOuvert ? 'template-carte ouverte' : 'template-carte'}>
              <button className="template-entete" onClick={() => setOuvert(estOuvert ? null : m.id)}>
                <strong>{m.icone} {m.titre}</strong>
                <span>{m.description}</span>
              </button>
              {estOuvert && (
                <div className="template-details">
                  {m.cas_usage.map((c: any, i: number) => (
                    <div key={i} className="metier-cas">
                      <h5>{c.titre}</h5>
                      <p>{c.description}</p>
                      <Link to={c.page} className="metier-lien">
                        {c.texte_lien}
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
