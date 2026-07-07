import { useCallback, useState } from 'react'
import {
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Background,
  Controls,
  ReactFlow,
  type Edge,
  type Node,
  type OnConnect,
  type OnEdgesChange,
  type OnNodesChange,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'

type BriqueNode = Node & { brique: string }

type Props = {
  briquesDisponibles: any[]
  onExecuter: (nodes: { id: string; type: string; config: Record<string, unknown> }[], edges: { source: string; target: string }[]) => void
}

let compteurId = 1

export default function BrickCanvas({ briquesDisponibles, onExecuter }: Props) {
  const [nodes, setNodes] = useState<BriqueNode[]>([])
  const [edges, setEdges] = useState<Edge[]>([])

  const onNodesChange: OnNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds) as BriqueNode[]),
    [],
  )
  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [],
  )
  const onConnect: OnConnect = useCallback(
    (connexion) => setEdges((eds) => addEdge(connexion, eds)),
    [],
  )

  function ajouterNoeud(brique: any) {
    const id = String(compteurId++)
    setNodes((nds) => [
      ...nds,
      {
        id,
        position: { x: 80 + (nds.length % 3) * 220, y: 60 + Math.floor(nds.length / 3) * 140 },
        data: { label: brique.titre },
        brique: brique.id,
      },
    ])
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
        <h4>Briques débloquées</h4>
        {briquesDisponibles.map((b) => (
          <button key={b.id} onClick={() => ajouterNoeud(b)}>
            + {b.titre}
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
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  )
}
