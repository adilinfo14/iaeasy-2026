"""Serveur MCP réel et autonome (pas une simulation), lançable indépendamment de l'IHM
avec n'importe quel client MCP (Claude Desktop, `mcp dev`, etc.) :

    python -m app.agents.mcp_demo_server

Le module `engine.py` appelle les mêmes fonctions Python directement (`tools.py`) plutôt
que de repasser par un aller-retour MCP client/serveur, pour rester simple dans un
processus unique — mais ce fichier prouve que les outils exposés sont de vrais outils MCP.
"""

from mcp.server.fastmcp import FastMCP

from .tools import calculatrice, recherche_mini_corpus

mcp = FastMCP("iaeasy-outils-demo")


@mcp.tool()
def calculer(expression: str) -> str:
    """Évalue une expression arithmétique simple, ex: '12 * (3 + 4)'."""
    resultat = calculatrice(expression)
    if resultat["ok"]:
        return str(resultat["resultat"])
    return f"Erreur: {resultat['erreur']}"


@mcp.tool()
def rechercher(requete: str) -> str:
    """Cherche le passage le plus pertinent dans un petit corpus documentaire de démonstration."""
    return recherche_mini_corpus(requete)["passage"]


if __name__ == "__main__":
    mcp.run()
