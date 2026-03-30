from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import shutil
import os

from app.config import settings
from app.database import get_db, init_db
from app.models import Pregunta, Remediacion
from app.schemas import (
    PreguntaResponse,
    PreguntaListResponse,
    FormularioResponse,
    RemediacionCreate,
)
from app.extractor import PDFExtractor
from app.utils import formatear_fecha_iso

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

init_db()


@app.on_event("startup")
async def startup_event():
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def root():
    return {"message": "PDF Extractor API", "version": settings.APP_VERSION}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    file_path = settings.UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extractor = PDFExtractor(str(file_path))
        preguntas_data = extractor.extraer_todas_las_preguntas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al extraer PDF: {str(e)}")

    preguntas_creadas = []
    for data in preguntas_data:
        pregunta = Pregunta(
            numero=data["numero"],
            titulo=data["titulo"],
            texto_pregunta=data["texto_pregunta"],
        )
        db.add(pregunta)
        db.flush()

        for rem_data in data["remediaciones"]:
            remediacion = Remediacion(
                pregunta_id=pregunta.id,
                numero_fila=rem_data["numero_fila"],
                deficiencia=rem_data["deficiencia"],
                medida_remediacion=rem_data["medida_remediacion"],
                organo_responsable=rem_data["organo_responsable"],
                fecha_inicio=rem_data["fecha_inicio"],
                fecha_fin=rem_data["fecha_fin"],
                medio_verificacion=rem_data["medio_verificacion"],
                comentarios=rem_data["comentarios"],
            )
            db.add(remediacion)

        preguntas_creadas.append(pregunta.id)

    db.commit()

    return {
        "message": "PDF procesado exitosamente",
        "preguntas_extraidas": len(preguntas_creadas),
        "preguntas_ids": preguntas_creadas,
    }


@app.get("/preguntas/", response_model=List[PreguntaListResponse])
def listar_preguntas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    preguntas = db.query(Pregunta).offset(skip).limit(limit).all()
    return preguntas


@app.get("/preguntas/{pregunta_id}", response_model=PreguntaResponse)
def obtener_pregunta(pregunta_id: int, db: Session = Depends(get_db)):
    pregunta = db.query(Pregunta).filter(Pregunta.id == pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return pregunta


@app.get("/preguntas/{pregunta_id}/formulario", response_model=FormularioResponse)
def obtener_formulario(pregunta_id: int, db: Session = Depends(get_db)):
    pregunta = db.query(Pregunta).filter(Pregunta.id == pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    remediaciones_form = []
    deficiencia = None

    for rem in pregunta.remediaciones:
        if deficiencia is None and rem.deficiencia:
            deficiencia = rem.deficiencia

        remediaciones_form.append(
            {
                "fila": rem.numero_fila,
                "medida": rem.medida_remediacion,
                "organo": rem.organo_responsable,
                "fecha_inicio": formatear_fecha_iso(rem.fecha_inicio),
                "fecha_fin": formatear_fecha_iso(rem.fecha_fin),
                "medio_verificacion": rem.medio_verificacion,
                "comentarios": rem.comentarios,
            }
        )

    return {
        "pregunta": pregunta.numero,
        "titulo": pregunta.titulo,
        "deficiencia": deficiencia,
        "remediaciones": remediaciones_form,
    }


@app.delete("/preguntas/limpiar")
def limpiar_base_datos(db: Session = Depends(get_db)):
    db.query(Remediacion).delete()
    db.query(Pregunta).delete()
    db.commit()
    return {"message": "Base de datos limpiada"}
