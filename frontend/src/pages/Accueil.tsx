import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  lireBadges,
  lireProgression,
  lireStatsAvis,
  lireVisiteurs,
  listerBriques,
  listerModeles,
  StatsAvis,
} from '../api/client'

const MODULES = [
  {
    to: '/catalogue',
    icone: '🗂️',
    titre: 'Catalogue',
    groupe: 'pratiquer',
    // Complété dynamiquement (nombre de modèles/familles réel) une fois le catalogue chargé.
    pitch: "Des dizaines de modèles, des familles d'IA différentes — pas seulement des chatbots.",
  },
  {
    to: '/parcours',
    icone: '🧭',
    titre: 'Parcours',
    groupe: 'pratiquer',
    pitch: 'Construis ton assistant brique par brique, avec une vraie mise en situation.',
    recommande: true,
  },
  {
    to: '/entrainement',
    icone: '📉',
    titre: 'Entraînement',
    groupe: 'pratiquer',
    pitch: 'Regarde une vraie courbe de loss descendre, sur 3 cas d\'usage concrets.',
  },
  {
    to: '/constructeur',
    icone: '🏗️',
    titre: 'Constructeur',
    groupe: 'pratiquer',
    pitch: "Mode architecte : assemble un vrai RAG, un agent, un pipeline multi-agent.",
  },
  {
    to: '/simulateur',
    icone: '⚖️',
    titre: 'Simulateur',
    groupe: 'pratiquer',
    pitch: 'Comparez en direct la vitesse et le coût réel de plusieurs modèles.',
  },
  {
    to: '/strategie-test',
    icone: '🧪',
    titre: 'Stratégie de tests',
    groupe: 'ressources',
    pitch: "Comment vérifier sérieusement chaque famille de modèle — cahiers de test à réutiliser.",
  },
  {
    to: '/securite',
    icone: '🛡️',
    titre: 'Sécurité',
    groupe: 'ressources',
    pitch: "10 risques concrets d'un agent IA (OWASP) et les bonnes pratiques pour s'en protéger.",
  },
  {
    to: '/glossaire',
    icone: '📖',
    titre: 'Glossaire',
    groupe: 'ressources',
    pitch: "Le jargon de l'IA expliqué simplement, un terme à la fois.",
  },
  {
    to: '/metiers',
    icone: '🧭',
    titre: 'Mon métier',
    groupe: 'ressources',
    pitch: "L'IA dans votre métier : des cas d'usage concrets, pas des promesses abstraites.",
  },
  {
    to: '/videos',
    icone: '🎬',
    titre: 'Vidéos',
    groupe: 'ressources',
    pitch: "Des schémas de conférences IA expliqués en français simple.",
  },
  {
    to: '/avis',
    icone: '⭐',
    titre: 'Avis',
    groupe: 'avis',
    pitch: 'Notez le site en 2 secondes et lisez les avis des autres visiteurs.',
  },
]

export default function Accueil() {
  const [debloquees, setDebloquees] = useState(0)
  const [total, setTotal] = useState(5)
  const [visiteurs, setVisiteurs] = useState<number | null>(null)
  const [badges, setBadges] = useState(0)
  const [statsAvis, setStatsAvis] = useState<StatsAvis | null>(null)
  const [catalogue, setCatalogue] = useState<{ nbModeles: number; nbFamilles: number } | null>(null)

  useEffect(() => {
    listerBriques().then((b) => setTotal(b.length))
    lireProgression().then((p) => setDebloquees(p.debloquees.length))
    lireVisiteurs().then((v) => setVisiteurs(v.total_visiteurs_uniques))
    lireBadges().then((b) => setBadges(b.badges.length))
    lireStatsAvis().then(setStatsAvis)
    listerModeles().then((modeles) =>
      setCatalogue({ nbModeles: modeles.length, nbFamilles: new Set(modeles.map((m: any) => m.famille)).size }),
    )
  }, [])

  return (
    <div className="page page-accueil">
      <h1>☕ iaeasy — apprendre l'IA en la construisant</h1>
      <div className="grains-cafe-deco" aria-hidden="true">
        {[-18, 6, -8].map((angle, i) => (
          <svg key={i} viewBox="0 0 60 90" style={{ transform: `rotate(${angle}deg)` }}>
            <ellipse cx="30" cy="45" rx="26" ry="43" fill="#8a5a34" />
            <path
              d="M30 8 C16 22,16 40,30 45 C44 50,44 68,30 82"
              fill="none"
              stroke="#3c2415"
              strokeWidth="6"
              strokeLinecap="round"
            />
          </svg>
        ))}
      </div>
      <p className="page-intro">
        Née de la conviction qu'on ne comprend véritablement l'intelligence artificielle qu'en la
        manipulant soi-même, iaeasy s'attache à porter une pédagogie à la fois exigeante et
        accessible, ouverte à toute personne curieuse — étudiante, artisan, salariée, ou simplement
        désireuse de savoir ce qui se cache derrière un chatbot. La plateforme conjugue rigueur
        technique et souveraineté numérique : hébergée sur un serveur personnel et fondée
        exclusivement sur des modèles ouverts, elle ne transmet jamais la moindre donnée à un
        service tiers. Elle invite à essayer des dizaines de modèles différents, à observer une
        véritable courbe d'apprentissage se former sous ses yeux, puis à assembler, brique par
        brique, sa propre architecture d'agent.
      </p>

      <div className="progression-globale">
        <span>🔓 {debloquees}/{total} briques débloquées dans le Parcours</span>
        <span> · 🏅 {badges}/{total} quiz réussis</span>
        {visiteurs != null && <span> · 👀 {visiteurs} visiteur{visiteurs > 1 ? 's' : ''} unique{visiteurs > 1 ? 's' : ''}</span>}
        {statsAvis?.moyenne != null && (
          <span>
            {' '}
            · <Link to="/avis">⭐ {statsAvis.moyenne.toFixed(2)}/5 ({statsAvis.total} avis)</Link>
          </span>
        )}
      </div>

      <div className="modules-grille">
        {MODULES.map((m) => (
          <Link key={m.to} to={m.to} className={`module-carte module-carte-${m.groupe}`}>
            {m.recommande && <span className="module-badge">Commence ici</span>}
            <div className="module-icone">{m.icone}</div>
            <h3>{m.titre}</h3>
            <p>
              {m.to === '/catalogue' && catalogue
                ? `${catalogue.nbModeles} modèles, ${catalogue.nbFamilles} familles d'IA différentes — pas seulement des chatbots.`
                : m.pitch}
            </p>
          </Link>
        ))}
      </div>
    </div>
  )
}
