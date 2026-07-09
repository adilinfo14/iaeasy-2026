import { useState } from 'react'
import { lireReglagesAdmin, modifierReglagesAdmin, type ReglagesChat } from '../api/client'

export default function AdminReglages() {
  const [motDePasse, setMotDePasse] = useState('')
  const [connecte, setConnecte] = useState(false)
  const [reglages, setReglages] = useState<ReglagesChat | null>(null)
  const [enCours, setEnCours] = useState(false)
  const [erreur, setErreur] = useState<string | null>(null)
  const [messageOk, setMessageOk] = useState<string | null>(null)

  async function connexion() {
    setEnCours(true)
    setErreur(null)
    try {
      const r = await lireReglagesAdmin(motDePasse)
      setReglages(r)
      setConnecte(true)
    } catch (e: any) {
      setErreur(e.message)
    } finally {
      setEnCours(false)
    }
  }

  async function enregistrer() {
    if (!reglages) return
    setEnCours(true)
    setErreur(null)
    setMessageOk(null)
    try {
      const r = await modifierReglagesAdmin(motDePasse, reglages)
      setReglages(r)
      setMessageOk('Réglages enregistrés — pris en compte immédiatement, sans redémarrage.')
    } catch (e: any) {
      setErreur(e.message)
    } finally {
      setEnCours(false)
    }
  }

  function champ(cle: keyof ReglagesChat, valeur: number) {
    if (!reglages) return
    setReglages({ ...reglages, [cle]: valeur })
  }

  if (!connecte) {
    return (
      <div className="page page-admin">
        <h1>🔒 Administration</h1>
        <p className="page-intro">Accès réservé — saisissez le mot de passe pour continuer.</p>
        <div className="admin-connexion">
          <input
            type="password"
            value={motDePasse}
            onChange={(e) => setMotDePasse(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && connexion()}
            placeholder="Mot de passe"
          />
          <button onClick={connexion} disabled={enCours || !motDePasse}>
            {enCours ? 'Vérification…' : 'Se connecter'}
          </button>
        </div>
        {erreur && <p className="erreur">{erreur}</p>}
      </div>
    )
  }

  return (
    <div className="page page-admin">
      <h1>🔒 Administration — Réglages du chatbot</h1>
      <p className="page-intro">
        Ces réglages sont pris en compte immédiatement, à la prochaine question posée au chatbot —
        aucun redémarrage n'est nécessaire.
      </p>

      {reglages && (
        <div className="admin-formulaire">
          <label>
            Messages conservés en mémoire de conversation
            <input
              type="number"
              min={2}
              max={30}
              value={reglages.chat_max_historique}
              onChange={(e) => champ('chat_max_historique', Number(e.target.value))}
            />
            <span className="texte-muted">
              Nombre de messages (question + réponse) que le modèle garde en mémoire dans une même
              conversation. Plus haut = le chatbot se souvient plus longtemps, mais chaque question
              devient plus lente à traiter.
            </span>
          </label>

          <label>
            Longueur max. d'un message envoyé par le visiteur
            <input
              type="number"
              min={50}
              max={2000}
              value={reglages.chat_longueur_max_message}
              onChange={(e) => champ('chat_longueur_max_message', Number(e.target.value))}
            />
            <span className="texte-muted">En caractères.</span>
          </label>

          <label>
            Longueur max. d'un message d'historique (réponse du chatbot)
            <input
              type="number"
              min={200}
              max={5000}
              value={reglages.chat_longueur_max_message_historique}
              onChange={(e) => champ('chat_longueur_max_message_historique', Number(e.target.value))}
            />
            <span className="texte-muted">
              En caractères — doit rester généreux, une réponse du chatbot dépasse facilement 500
              caractères.
            </span>
          </label>

          <label>
            Conversations simultanées maximum (tous visiteurs confondus)
            <input
              type="number"
              min={1}
              max={20}
              value={reglages.chat_max_conversations_simultanees}
              onChange={(e) => champ('chat_max_conversations_simultanees', Number(e.target.value))}
            />
            <span className="texte-muted">
              Protège le serveur (CPU partagé du homelab) contre une surcharge si trop de visiteurs
              discutent en même temps.
            </span>
          </label>

          <button onClick={enregistrer} disabled={enCours}>
            {enCours ? 'Enregistrement…' : 'Enregistrer'}
          </button>
          {messageOk && <p className="admin-ok">{messageOk}</p>}
          {erreur && <p className="erreur">{erreur}</p>}
        </div>
      )}
    </div>
  )
}
