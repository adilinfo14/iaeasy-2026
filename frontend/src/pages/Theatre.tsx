import { useCallback, useEffect, useRef, useState } from 'react'
import Decor from '../components/theatre/Decor'
import Personnage from '../components/theatre/Personnage'
import {
  genererEpisodeTheatre,
  genererVoixTheatre,
  listerEpisodesTheatre,
  lireEpisodeTheatre,
} from '../api/client'

const NOMS = { clio: 'Clio', marco: 'Marco' }
const VITESSE_FRAPPE_MS = 22
const PAUSE_APRES_LIGNE_MS = 500

// Le personnage qui écoute réagit lui aussi, plutôt que de rester figé en "neutre" pendant
// toute la réplique de l'autre — dérivé de l'émotion du locuteur (générée par l'IA ou écrite à
// la main), sans données supplémentaires à produire.
const REACTION_AUDITEUR: Record<string, string> = {
  neutre: 'neutre',
  surprise: 'surprise',
  joyeux: 'joyeux',
  triste: 'inquiet',
  inquiet: 'inquiet',
}

export default function Theatre() {
  const [liste, setListe] = useState<any[]>([])
  const [episode, setEpisode] = useState<any>(null)
  const [sceneIndex, setSceneIndex] = useState(0)
  const [ligneIndex, setLigneIndex] = useState(0)
  const [texteAffiche, setTexteAffiche] = useState('')
  const [enPause, setEnPause] = useState(false)
  const [termine, setTermine] = useState(false)
  const [chargement, setChargement] = useState(false)
  const [erreur, setErreur] = useState<string | null>(null)
  const [sonActif, setSonActif] = useState(true)
  const [audioTermine, setAudioTermine] = useState(true)

  const minuteurRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const urlAudioRef = useRef<string | null>(null)

  useEffect(() => {
    listerEpisodesTheatre().then(setListe)
  }, [])

  function nettoyerMinuteur() {
    if (minuteurRef.current) clearTimeout(minuteurRef.current)
    minuteurRef.current = null
  }

  function arreterAudio() {
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current = null
    }
    if (urlAudioRef.current) {
      URL.revokeObjectURL(urlAudioRef.current)
      urlAudioRef.current = null
    }
  }

  const demarrerEpisode = useCallback((e: any) => {
    nettoyerMinuteur()
    arreterAudio()
    setEpisode(e)
    setSceneIndex(0)
    setLigneIndex(0)
    setTexteAffiche('')
    setTermine(false)
    setEnPause(false)
    setErreur(null)
  }, [])

  async function choisirEpisode(id: string) {
    setChargement(true)
    setErreur(null)
    try {
      const e = await lireEpisodeTheatre(id)
      demarrerEpisode(e)
    } catch (err: any) {
      setErreur(err.message)
    } finally {
      setChargement(false)
    }
  }

  async function genererNouvelleHistoire() {
    setChargement(true)
    setErreur(null)
    try {
      const e = await genererEpisodeTheatre()
      demarrerEpisode(e)
    } catch (err: any) {
      setErreur(err.message)
    } finally {
      setChargement(false)
    }
  }

  const ligneCourante = episode?.scenes?.[sceneIndex]?.repliques?.[ligneIndex]
  const decorCourant = episode?.scenes?.[sceneIndex]?.decor

  // Effet machine à écrire + narration vocale (voix neuronale Piper, générée côté serveur) :
  // l'avance automatique n'a lieu qu'une fois le texte ET la voix RÉELLEMENT terminés (voir plus
  // bas) — un délai fixe devinait mal la durée de la voix et la coupait souvent trop tôt.
  useEffect(() => {
    if (!ligneCourante) return
    setTexteAffiche('')
    let i = 0
    const texte = ligneCourante.texte
    const id = setInterval(() => {
      i += 1
      setTexteAffiche(texte.slice(0, i))
      if (i >= texte.length) clearInterval(id)
    }, VITESSE_FRAPPE_MS)

    arreterAudio()
    if (!sonActif) {
      setAudioTermine(true)
      return () => clearInterval(id)
    }

    setAudioTermine(false)
    let annule = false
    genererVoixTheatre(texte, ligneCourante.personnage)
      .then((url) => {
        if (annule) return
        urlAudioRef.current = url
        const audio = new Audio(url)
        audioRef.current = audio
        audio.onended = () => setAudioTermine(true)
        audio.onerror = () => setAudioTermine(true)
        audio.play().catch(() => setAudioTermine(true))
      })
      .catch(() => setAudioTermine(true))

    return () => {
      annule = true
      clearInterval(id)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [episode, sceneIndex, ligneIndex, sonActif])

  function avancer() {
    if (!episode) return
    const scenes = episode.scenes
    const repliquesScene = scenes[sceneIndex].repliques
    if (ligneIndex + 1 < repliquesScene.length) {
      setLigneIndex((i) => i + 1)
    } else if (sceneIndex + 1 < scenes.length) {
      setSceneIndex((i) => i + 1)
      setLigneIndex(0)
    } else {
      setTermine(true)
    }
  }

  function reculer() {
    if (!episode) return
    if (ligneIndex > 0) {
      setLigneIndex((i) => i - 1)
    } else if (sceneIndex > 0) {
      const scenePrecedente = episode.scenes[sceneIndex - 1]
      setSceneIndex((i) => i - 1)
      setLigneIndex(scenePrecedente.repliques.length - 1)
    }
    setTermine(false)
  }

  useEffect(() => {
    if (!audioRef.current) return
    if (enPause) audioRef.current.pause()
    else audioRef.current.play().catch(() => {})
  }, [enPause])

  // Avance automatique une fois le texte affiché en entier ET la voix réellement terminée
  // (ou désactivée) — corrige le son qui se coupait avant la fin du texte.
  useEffect(() => {
    nettoyerMinuteur()
    if (!ligneCourante || enPause || termine) return
    if (texteAffiche.length < ligneCourante.texte.length) return
    if (!audioTermine) return
    minuteurRef.current = setTimeout(avancer, PAUSE_APRES_LIGNE_MS)
    return nettoyerMinuteur
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [texteAffiche, enPause, termine, audioTermine])

  useEffect(() => arreterAudio, [])

  return (
    <div className="page page-theatre">
      <h1>🎭 Le Théâtre de l'Histoire</h1>
      <p className="page-intro">
        Deux personnages, générés et animés par une IA, se racontent des histoires vraies — le
        décor et l'ambiance changent avec le récit, une voix neuronale auto-hébergée (Piper) les
        fait parler, et l'IA associe une émotion réelle à chaque réplique (surprise, joie,
        tristesse, inquiétude...) qui change l'expression du personnage — y compris celle qui
        écoute. Les 5 premières histoires sont écrites à l'avance ; le bouton « Nouvelle histoire »
        en fait générer une nouvelle en direct, sur un sujet historique réel tiré au sort.
      </p>

      {!episode && (
        <div className="theatre-selection">
          <div className="exemples-chips">
            {liste.map((e) => (
              <button key={e.id} className="chip" onClick={() => choisirEpisode(e.id)} disabled={chargement}>
                {e.titre} ({e.annee})
              </button>
            ))}
          </div>
          <button onClick={genererNouvelleHistoire} disabled={chargement}>
            {chargement ? 'Écriture en cours…' : '✨ Nouvelle histoire (générée par une IA)'}
          </button>
          {erreur && <p className="erreur">{erreur}</p>}
        </div>
      )}

      {episode && (
        <div className="theatre-scene">
          {decorCourant && <Decor key={`${sceneIndex}-${decorCourant}`} decor={decorCourant} />}

          <div className="theatre-personnages">
            <Personnage
              type="clio"
              decor={decorCourant}
              parle={ligneCourante?.personnage === 'clio' && !termine}
              actif={!termine}
              variante={ligneIndex % 2 === 0}
              emotion={
                ligneCourante?.personnage === 'clio'
                  ? ligneCourante?.emotion
                  : REACTION_AUDITEUR[ligneCourante?.emotion || 'neutre']
              }
            />
            <Personnage
              type="marco"
              decor={decorCourant}
              parle={ligneCourante?.personnage === 'marco' && !termine}
              actif={!termine}
              variante={ligneIndex % 2 === 0}
              emotion={
                ligneCourante?.personnage === 'marco'
                  ? ligneCourante?.emotion
                  : REACTION_AUDITEUR[ligneCourante?.emotion || 'neutre']
              }
            />
          </div>

          {!termine && ligneCourante && (
            <div className="theatre-dialogue">
              <div className="theatre-dialogue-nom">{NOMS[ligneCourante.personnage as 'clio' | 'marco']}</div>
              <p className="theatre-dialogue-texte">{texteAffiche}</p>
            </div>
          )}

          {termine && (
            <div className="theatre-dialogue theatre-fin">
              <p>— Fin de l'histoire —</p>
            </div>
          )}

          <div className="theatre-controles">
            <button onClick={reculer} disabled={sceneIndex === 0 && ligneIndex === 0}>
              ◀ Précédent
            </button>
            <button onClick={() => setEnPause((p) => !p)}>{enPause ? '▶ Reprendre' : '⏸ Pause'}</button>
            <button onClick={avancer} disabled={termine}>
              Suivant ▶
            </button>
            <button
              onClick={() => {
                arreterAudio()
                setSonActif((s) => !s)
              }}
            >
              {sonActif ? '🔊 Son' : '🔇 Muet'}
            </button>
            <button
              onClick={() => {
                nettoyerMinuteur()
                arreterAudio()
                setEpisode(null)
              }}
            >
              Choisir une autre histoire
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
