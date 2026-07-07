const BASE = '/api'

export async function listerModeles() {
  const r = await fetch(`${BASE}/catalogue`)
  return r.json()
}

export async function essayerModele(id: string, inputText?: string) {
  const r = await fetch(`${BASE}/catalogue/${id}/essayer`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input_text: inputText }),
  })
  if (!r.ok) {
    const err = await r.json().catch(() => ({}))
    throw new Error(err.detail || 'Erreur pendant l’exécution du modèle')
  }
  return r.json()
}

export async function demarrerEntrainement() {
  const r = await fetch(`${BASE}/training/start`, { method: 'POST' })
  return r.json()
}

type PointLoss = { step: number; epoch: number; loss: number }
type FinEntrainement = { status: string; erreur: string | null }

export function suivreEntrainement(
  jobId: string,
  onLoss: (point: PointLoss) => void,
  onFin: (fin: FinEntrainement) => void,
) {
  const source = new EventSource(`${BASE}/training/${jobId}/stream`)
  source.addEventListener('loss', (e) => onLoss(JSON.parse((e as MessageEvent).data)))
  source.addEventListener('fin', (e) => {
    onFin(JSON.parse((e as MessageEvent).data))
    source.close()
  })
  source.addEventListener('erreur', () => source.close())
  return () => source.close()
}

export async function listerBriques() {
  const r = await fetch(`${BASE}/agents/briques`)
  return r.json()
}

export async function executerGraphe(nodes: unknown[], edges: unknown[]) {
  const r = await fetch(`${BASE}/agents/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nodes, edges }),
  })
  if (!r.ok) {
    const err = await r.json().catch(() => ({}))
    throw new Error(err.detail || 'Erreur pendant l’exécution du graphe')
  }
  return r.json()
}

export async function lireProgression() {
  const r = await fetch(`${BASE}/progress`)
  return r.json()
}

export async function debloquerBrique(id: string) {
  const r = await fetch(`${BASE}/progress/debloquer/${id}`, { method: 'POST' })
  return r.json()
}
