from pydantic import BaseModel


class CasUsage(BaseModel):
    enonce: str
    input_exemple: str


class ModelCard(BaseModel):
    id: str
    nom: str
    famille: str
    secteur: str
    moteur: str
    moteur_ref: str
    taille: str
    description_pedagogique: str
    cas_usage: CasUsage
    statut: str


class EssaiRequest(BaseModel):
    input_text: str | None = None
