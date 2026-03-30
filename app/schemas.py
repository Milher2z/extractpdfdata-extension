from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class RemediacionBase(BaseModel):
    numero_fila: int
    deficiencia: Optional[str] = None
    medida_remediacion: str
    organo_responsable: str
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    medio_verificacion: str
    comentarios: Optional[str] = None


class RemediacionCreate(RemediacionBase):
    pass


class RemediacionResponse(RemediacionBase):
    id: int

    class Config:
        from_attributes = True


class PreguntaBase(BaseModel):
    numero: str
    titulo: str
    texto_pregunta: str


class PreguntaCreate(PreguntaBase):
    remediaciones: List[RemediacionCreate]


class PreguntaResponse(PreguntaBase):
    id: int
    created_at: datetime
    remediaciones: List[RemediacionResponse] = []

    class Config:
        from_attributes = True


class PreguntaListResponse(BaseModel):
    id: int
    numero: str
    titulo: str

    class Config:
        from_attributes = True


class FormularioResponse(BaseModel):
    pregunta: str
    titulo: str
    deficiencia: Optional[str]
    remediaciones: List[dict]
