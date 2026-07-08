from pydantic import BaseModel, Field


class Exemple(BaseModel):
    label: str
    input: str


class CasUsage(BaseModel):
    enonce: str
    exemples: list[Exemple] = []


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
    input_text: str | None = Field(default=None, max_length=2000)
