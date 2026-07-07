type ModelCardProps = {
  modele: any
  onOuvrir: (modele: any) => void
}

export default function ModelCard({ modele, onOuvrir }: ModelCardProps) {
  return (
    <button className="model-card" onClick={() => onOuvrir(modele)}>
      <div className="model-card-famille">{modele.famille.replace(/_/g, ' ')}</div>
      <h3>{modele.nom}</h3>
      <p className="model-card-secteur">{modele.secteur}</p>
      <p className="model-card-taille">{modele.taille}</p>
    </button>
  )
}
