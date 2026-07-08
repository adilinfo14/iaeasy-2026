import { forwardRef, useCallback, useEffect, useImperativeHandle, useState } from 'react'
import {
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Background,
  Controls,
  MarkerType,
  ReactFlow,
  ReactFlowProvider,
  useReactFlow,
  type Edge,
  type Node,
  type OnConnect,
  type OnEdgesChange,
  type OnNodesChange,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'

const OPTIONS_ARETE = {
  type: 'smoothstep' as const,
  animated: true,
  markerEnd: { type: MarkerType.ArrowClosed, color: '#4f7cff' },
}

const CLE_APERCU = ['prompt', 'texte', 'expression']

function apercuConfig(config: Record<string, unknown>): string {
  for (const cle of CLE_APERCU) {
    const valeur = config?.[cle]
    if (typeof valeur === 'string' && valeur.trim()) {
      return valeur.length > 60 ? `${valeur.slice(0, 60)}…` : valeur
    }
  }
  return ''
}

function completerConfig(composant: any, configExistant: Record<string, unknown>) {
  const config = { ...(configExistant || {}) }
  for (const champ of composant?.champs_config || []) {
    if (config[champ.cle] === undefined) {
      config[champ.cle] = champ.defaut !== undefined ? champ.defaut : champ.type === 'select' ? champ.options?.[0] : ''
    }
  }
  return config
}

function construireLabel(titre: string, icone: string, config: Record<string, unknown>) {
  const apercu = apercuConfig(config)
  return (
    <div className="noeud-contenu">
      <strong>{icone} {titre}</strong>
      {apercu ? <div className="noeud-apercu">« {apercu} »</div> : <div className="noeud-apercu noeud-apercu-vide">(aucune entrée définie — cliquez pour en ajouter une)</div>}
    </div>
  )
}

type BriqueNode = Node & { brique: string; config: Record<string, unknown> }

type Props = {
  composants: any[]
  templateACharger: any | null
  resultatsParNoeud: Record<string, any> | null
  onExecuter: (nodes: { id: string; type: string; config: Record<string, unknown> }[], edges: { source: string; target: string }[]) => void
  onComposantInfo: (brique: string, noeudId: string | undefined, config: Record<string, unknown>) => void
}

export type BrickCanvasHandle = {
  modifierConfigNoeud: (noeudId: string, cle: string, valeur: unknown) => void
}

let compteurId = 1

const COULEURS_CATEGORIE: Record<string, string> = {
  source: '#38bdf8',
  traitement: '#a78bfa',
  stockage: '#facc15',
  modele: '#4ade80',
  outil: '#fb923c',
}

const CanvasInterne = forwardRef<BrickCanvasHandle, Props>(function CanvasInterne(
  { composants, templateACharger, resultatsParNoeud, onExecuter, onComposantInfo },
  ref,
) {
  const [nodes, setNodes] = useState<BriqueNode[]>([])
  const [edges, setEdges] = useState<Edge[]>([])
  const { fitView } = useReactFlow()

  useImperativeHandle(ref, () => ({
    modifierConfigNoeud(noeudId, cle, valeur) {
      setNodes((nds) =>
        nds.map((n) => {
          if (n.id !== noeudId) return n
          const composant = composants.find((c) => c.id === n.brique)
          const nouvelleConfig = { ...n.config, [cle]: valeur }
          return { ...n, config: nouvelleConfig, data: { label: construireLabel(composant?.titre || n.brique, composant?.icone || '', nouvelleConfig) } }
        }),
      )
    },
  }))

  useEffect(() => {
    if (!templateACharger) return
    const composantParType = new Map(composants.map((c) => [c.id, c]))
    const nouveauxNoeuds: BriqueNode[] = templateACharger.nodes.map((n: any) => {
      const composant = composantParType.get(n.type)
      const config = completerConfig(composant, n.config || {})
      return {
        id: n.id,
        position: n.position || { x: 100, y: 100 },
        data: { label: construireLabel(composant?.titre || n.type, composant?.icone || '', config) },
        brique: n.type,
        config,
        style: {
          background: COULEURS_CATEGORIE[composant?.categorie] ? `${COULEURS_CATEGORIE[composant.categorie]}22` : undefined,
          borderColor: COULEURS_CATEGORIE[composant?.categorie],
          width: 220,
        },
      }
    })
    const nouvellesAretes: Edge[] = templateACharger.edges.map((e: any, i: number) => ({
      id: `tpl-${i}`,
      source: e.source,
      target: e.target,
      ...OPTIONS_ARETE,
    }))
    setNodes(nouveauxNoeuds)
    setEdges(nouvellesAretes)
    compteurId = nouveauxNoeuds.length + 1
    // Laisse react-flow calculer les positions avant de recentrer la vue.
    requestAnimationFrame(() => fitView({ padding: 0.25, duration: 300 }))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [templateACharger])

  const onNodesChange: OnNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds) as BriqueNode[]),
    [],
  )
  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [],
  )
  const onConnect: OnConnect = useCallback(
    (connexion) => setEdges((eds) => addEdge({ ...connexion, ...OPTIONS_ARETE }, eds)),
    [],
  )

  function ajouterNoeud(composant: any) {
    const id = String(compteurId++)
    const config = completerConfig(composant, {})
    setNodes((nds) => {
      const nouveaux = [
        ...nds,
        {
          id,
          position: { x: 80 + (nds.length % 3) * 220, y: 60 + Math.floor(nds.length / 3) * 140 },
          data: { label: construireLabel(composant.titre, composant.icone, config) },
          brique: composant.id,
          config,
          style: {
            background: COULEURS_CATEGORIE[composant.categorie] ? `${COULEURS_CATEGORIE[composant.categorie]}22` : undefined,
            borderColor: COULEURS_CATEGORIE[composant.categorie],
            width: 220,
          },
        },
      ]
      requestAnimationFrame(() => fitView({ padding: 0.25, duration: 300 }))
      return nouveaux
    })
    onComposantInfo(composant.id, id, config)
  }

  function executer() {
    onExecuter(
      nodes.map((n) => ({ id: n.id, type: n.brique, config: n.config || {} })),
      edges.map((e) => ({ source: e.source, target: e.target })),
    )
  }

  return (
    <div className="canvas-layout">
      <aside className="palette">
        <h4>Briques d'architecture</h4>
        <p className="texte-muted">Cliquez une brique pour l'ajouter au canvas et voir sa définition.</p>
        {composants.map((c) => (
          <button key={c.id} onClick={() => ajouterNoeud(c)}>
            {c.icone} {c.titre}
          </button>
        ))}
        <button className="executer-btn" onClick={executer} disabled={nodes.length === 0}>
          Exécuter le graphe
        </button>
      </aside>
      <div className="canvas">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={(_, node) => {
            const n = node as BriqueNode
            onComposantInfo(n.brique, n.id, n.config || {})
          }}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      {nodes.length > 0 && (
        <div className="canvas-hint">
          💡 Cliquez un nœud pour voir sa définition et <strong>remplir ou modifier son entrée</strong> avant d'exécuter.
          {resultatsParNoeud && ' Un second clic après exécution montre aussi ce que le nœud a produit.'}
        </div>
      )}
    </div>
  )
})

const BrickCanvas = forwardRef<BrickCanvasHandle, Props>(function BrickCanvas(props, ref) {
  return (
    <ReactFlowProvider>
      <CanvasInterne {...props} ref={ref} />
    </ReactFlowProvider>
  )
})

export default BrickCanvas
