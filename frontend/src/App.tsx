import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import Catalogue from './pages/Catalogue'
import Constructeur from './pages/Constructeur'
import Entrainement from './pages/Entrainement'
import Parcours from './pages/Parcours'

export default function App() {
  return (
    <div className="app">
      <header className="topnav">
        <div className="brand">iaeasy</div>
        <nav>
          <NavLink to="/catalogue">Catalogue</NavLink>
          <NavLink to="/entrainement">Entraînement</NavLink>
          <NavLink to="/parcours">Parcours</NavLink>
          <NavLink to="/constructeur">Constructeur</NavLink>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/catalogue" replace />} />
          <Route path="/catalogue" element={<Catalogue />} />
          <Route path="/entrainement" element={<Entrainement />} />
          <Route path="/parcours" element={<Parcours />} />
          <Route path="/constructeur" element={<Constructeur />} />
        </Routes>
      </main>
    </div>
  )
}
