from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(10), nullable=False)
    titulo = Column(Text, nullable=False)
    texto_pregunta = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    remediaciones = relationship(
        "Remediacion", back_populates="pregunta", cascade="all, delete-orphan"
    )


class Remediacion(Base):
    __tablename__ = "remediaciones"

    id = Column(Integer, primary_key=True, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False)
    numero_fila = Column(Integer, nullable=False)
    deficiencia = Column(Text, nullable=True)
    medida_remediacion = Column(Text, nullable=False)
    organo_responsable = Column(Text, nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    medio_verificacion = Column(Text, nullable=False)
    comentarios = Column(Text, nullable=True)

    pregunta = relationship("Pregunta", back_populates="remediaciones")
