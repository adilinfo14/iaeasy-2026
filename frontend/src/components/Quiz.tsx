import { useState } from 'react'

type Question = { question: string; options: string[]; bonne_reponse: number }
type Props = { questions: Question[]; dejaReussi: boolean; onReussite: () => void }

export default function Quiz({ questions, dejaReussi, onReussite }: Props) {
  const [reponses, setReponses] = useState<(number | null)[]>(questions.map(() => null))
  const [valide, setValide] = useState(false)

  function choisir(qIdx: number, optIdx: number) {
    if (valide) return
    setReponses((r) => r.map((v, i) => (i === qIdx ? optIdx : v)))
  }

  function verifier() {
    setValide(true)
    if (questions.every((q, i) => reponses[i] === q.bonne_reponse)) {
      onReussite()
    }
  }

  function recommencer() {
    setReponses(questions.map(() => null))
    setValide(false)
  }

  const toutRepondu = reponses.every((r) => r !== null)
  const toutBon = valide && questions.every((q, i) => reponses[i] === q.bonne_reponse)

  return (
    <div className="quiz-bloc">
      <h4>
        🎯 Quiz de vérification {dejaReussi && <span className="quiz-badge-acquis">🏅 Badge obtenu</span>}
      </h4>
      {questions.map((q, qi) => (
        <div key={qi} className="quiz-question">
          <p>{q.question}</p>
          <div className="quiz-options">
            {q.options.map((opt, oi) => {
              const selectionne = reponses[qi] === oi
              let classe = 'quiz-option'
              if (selectionne) classe += ' selectionne'
              if (valide && oi === q.bonne_reponse) classe += ' correcte'
              if (valide && selectionne && oi !== q.bonne_reponse) classe += ' incorrecte'
              return (
                <button key={oi} type="button" className={classe} onClick={() => choisir(qi, oi)} disabled={valide}>
                  {opt}
                </button>
              )
            })}
          </div>
        </div>
      ))}
      {!valide && (
        <button onClick={verifier} disabled={!toutRepondu}>
          Valider mes réponses
        </button>
      )}
      {toutBon && <p className="quiz-resultat quiz-resultat-ok">✅ Bravo, toutes les réponses sont correctes !</p>}
      {valide && !toutBon && (
        <>
          <p className="quiz-resultat quiz-resultat-ko">
            ❌ Pas tout à fait — la bonne réponse est surlignée en vert. Réessayez ?
          </p>
          <button onClick={recommencer}>Recommencer</button>
        </>
      )}
    </div>
  )
}
