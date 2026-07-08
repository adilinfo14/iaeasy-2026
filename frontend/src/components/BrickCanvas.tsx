import { useCallback, useEffect, useState } from 'react'
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

type BriqueNode = Node & { brique: string }

type Props = {
  composants: any[]
  templateACharger: any | null
  resultatsParNoeud: Record<string, any> | null
  onExecuter: (nodes: { id: string; type: string; config: Record<string, unknown> }[], edges: { source: string; target: string }[]) => void
  onComposantInfo: (brique: string, noeudId?: string) => void
}

let compteurId = 1

const COULEURS_CATEGORIE: Record<string, string> = {
  source: '#38bdf8',
  traitement: '#a78bfa',
  stockage: '#facc15',
  modele: '#4ade80',
  outil: '#fb923c',
}

function CanvasInterne({ composants, templateACharger, resultatsParNoeud, onExecuter, onComposantInfo }: Props) {
  const [nodes, setNodes] = useState<BriqueNode[]>([])
  const [edges, setEdges] = useState<Edge[]>([])
  const { fitView } = useReactFlow()

  useEffect(() => {
    if (!templateACharger) return
    const composantParType = new Map(composants.map((c) => [c.id, c]))
    const nouveauxNoeuds: BriqueNode[] = templateACharger.nodes.map((n: any) => {
      const composant = composantParType.get(n.type)
      return {
        id: n.id,
        position: n.position || { x: 100, y: 100 },
        data: { label: `${composant?.icone || ''} ${composant?.titre || n.type}` },
        brique: n.type,
        style: {
          background: COULEURS_CATEGORIE[composant?.categorie] ? `${COULEURS_CATEGORIE[composant.categorie]}22` : undefined,
          borderColor: COULEURS_CATEGORIE[composant?.categorie],
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
    setNodes((nds) => {
      const nouveaux = [
        ...nds,
        {
          id,
          position: { x: 80 + (nds.length % 3) * 220, y: 60 + Math.floor(nds.length / 3) * 140 },
          data: { label: `${composant.icone} ${composant.titre}` },
          brique: composant.id,
          style: {
            background: COULEURS_CATEGORIE[composant.categorie] ? `${COULEURS_CATEGORIE[composant.categorie]}22` : undefined,
            borderColor: COULEURS_CATEGORIE[composant.categorie],
          },
        },
      ]
      requestAnimationFrame(() => fitView({ padding: 0.25, duration: 300 }))
      return nouveaux
    })
    onComposantInfo(composant.id)
  }

  function executer() {
    onExecuter(
      nodes.map((n) => ({ id: n.id, type: n.brique, config: {} })),
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
          onNodeClick={(_, node) => onComposantInfo((node as BriqueNode).brique, node.id)}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      {resultatsParNoeud && (
        <div className="canvas-hint">💡 Cliquez un nœud du graphe pour revoir sa définition et ce qu'il a produit.</div>
      )}
    </div>
  )
}

export default function BrickCanvas(props: Props) {
  return (
    <ReactFlowProvider>
      <CanvasInterne {...props} />
    </ReactFlowProvider>
  )
}
