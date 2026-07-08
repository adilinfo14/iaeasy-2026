import { useEffect, useState } from 'react'
import { listerStrategiesTest } from '../api/client'

const TAILLE_PAGE = 10

export default function StrategieTest() {
  const [strategies, setStrategies] = useState<any[]>([])
  const [ouverte, setOuverte] = useState<string | null>(null)
  const [page, setPage] = useState(0)

  useEffect(() => {
    listerStrategiesTest().then(setStrategies)
  }, [])

  function basculer(famille: string) {
    setPage(0)
    setOuverte(ouverte === famille ? null : famille)
  }

  return (
    <div className="page page-strategie-test">
      <h1>☕ Stratégie de tests par famille de modèle</h1>
      <p className="page-intro">
        Un modèle qui répond avec assurance n'est pas forcément un modèle qui répond juste. Pour
        chacune des {strategies.length || 15} familles du catalogue, voici comment la vérifier
        sérieusement : les catégories de test à couvrir, les métriques à suivre, le piège le plus
        fréquent, et un cahier de test concret (une centaine de cas par famille) dont vous pouvez
        vous inspirer directement.
      </p>

      <div className="templates-liste">
        {strategies.map((s) => {
          const ouvert = ouverte === s.famille
          const total = s.cahier_exemple?.length || 0
          const nbPages = Math.max(1, Math.ceil(total / TAILLE_PAGE))
          const pageCourante = Math.min(page, nbPages - 1)
          const debut = pageCourante * TAILLE_PAGE
          const cahierPage = s.cahier_exemple?.slice(debut, debut + TAILLE_PAGE) || []

          return (
            <div key={s.famille} className={ouvert ? 'template-carte ouverte' : 'template-carte'}>
              <button className="template-entete" onClick={() => basculer(s.famille)}>
                <strong>{s.titre}</strong>
                <span>{s.objectif}</span>
              </button>
              {ouvert && (
                <div className="template-details">
                  <h5>🧪 Catégories de test à couvrir</h5>
                  <ul className="liste-simple">
                    {s.categories_test.map((c: any, i: number) => (
                      <li key={i}>
                        <strong>{c.nom}</strong> — {c.description}
                      </li>
                    ))}
                  </ul>

                  <h5>📏 Métriques à suivre</h5>
                  <ul className="liste-simple">
                    {s.metriques.map((m: string, i: number) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>

                  <h5>⚠️ Piège fréquent</h5>
                  <p>{s.piege_frequent}</p>

                  <h5>📋 Cahier de test — exemples à reproduire</h5>
                  <div className="cahier-test-table-wrap">
                    <table className="cahier-test-table">
                      <thead>
                        <tr>
                          <th>Cas</th>
                          <th>Entrée</th>
                          <th>Attendu</th>
                          <th>Constat</th>
                        </tr>
                      </thead>
                      <tbody>
                        {cahierPage.map((c: any, i: number) => (
                          <tr key={debut + i}>
                            <td>{c.cas}</td>
                            <td>{c.entree}</td>
                            <td>{c.attendu}</td>
                            <td>{c.constat}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {nbPages > 1 && (
                    <div className="cahier-pagination">
                      <button
                        className="chip"
                        disabled={pageCourante === 0}
                        onClick={() => setPage(pageCourante - 1)}
                      >
                        ← Précédent
                      </button>
                      <span className="texte-muted">
                        Page {pageCourante + 1} / {nbPages} — {total} cas au total
                      </span>
                      <button
                        className="chip"
                        disabled={pageCourante >= nbPages - 1}
                        onClick={() => setPage(pageCourante + 1)}
                      >
                        Suivant →
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
