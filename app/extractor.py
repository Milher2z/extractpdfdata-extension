import pdfplumber
import re
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.utils import limpiar_texto, convertir_fecha


class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extraer_todas_las_preguntas(self) -> List[Dict[str, Any]]:
        preguntas = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for num_pagina, page in enumerate(pdf.pages, start=1):
                pregunta_data = self._extraer_pregunta_de_pagina(page, num_pagina)
                if pregunta_data:
                    preguntas.append(pregunta_data)
        return preguntas

    def _extraer_pregunta_de_pagina(
        self, page, num_pagina: int
    ) -> Optional[Dict[str, Any]]:
        text = page.extract_text()
        if not text:
            return None

        numero = self._extraer_numero_pregunta(text)
        if not numero:
            return None

        titulo = self._extraer_titulo(text)
        texto_pregunta = self._extraer_texto_pregunta(text)
        remediaciones = self._extraer_tabla(page)

        return {
            "numero": numero,
            "titulo": titulo,
            "texto_pregunta": texto_pregunta,
            "remediaciones": remediaciones,
        }

    def _extraer_numero_pregunta(self, text: str) -> Optional[str]:
        match = re.search(r"PREGUNTA\s*(\d+)", text, re.IGNORECASE)
        if match:
            return match.group(1).zfill(2)
        return None

    def _extraer_titulo(self, text: str) -> str:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if "PREGUNTA" in line.upper():
                if i > 0:
                    titulo = lines[i - 1].strip()
                    if titulo:
                        return limpiar_texto(titulo)
        return ""

    def _extraer_texto_pregunta(self, text: str) -> str:
        lines = text.split("\n")
        pregunta_lines = []
        captura = False

        for line in lines:
            if "PREGUNTA" in line.upper():
                captura = True
                continue
            if captura:
                line_stripped = line.strip()
                if line_stripped and "DEFICIENCIA" not in line_stripped.upper():
                    pregunta_lines.append(line_stripped)
                elif "DEFICIENCIA" in line_stripped.upper():
                    break

        texto = " ".join(pregunta_lines)

        texto = re.sub(r"\s+N\s+FECHA DE.*$", "", texto)

        return limpiar_texto(texto)

    def _extraer_tabla(self, page) -> List[Dict[str, Any]]:
        tables = page.extract_tables()
        if not tables:
            return []

        table = tables[0]
        if len(table) < 2:
            return []

        headers = [h.replace("\n", " ").strip() if h else "" for h in table[0]]

        deficiencia_idx = None
        for i, h in enumerate(headers):
            if "DEFICIENCIA" in h.upper():
                deficiencia_idx = i
                break

        remediaciones = []
        deficiencia_actual = None
        num_fila_secuencial = 0

        for row in table[1:]:
            if not row or not any(row):
                continue

            row_clean = [
                cell.replace("\n", " ").strip() if cell else "" for cell in row
            ]

            tiene_contenido = any(cell for cell in row_clean[2:] if cell)
            if not tiene_contenido:
                continue

            num_fila_secuencial += 1
            num_fila = num_fila_secuencial

            if deficiencia_idx is not None and deficiencia_idx < len(row_clean):
                val = row_clean[deficiencia_idx]
                if val and deficiencia_actual is None:
                    deficiencia_actual = limpiar_texto(val)

            medida = self._obtener_valor_columna(
                row_clean, headers, ["MEDIDA", "REMEDIACIÓN", "MEDIDA DE REMEDIACIÓN"]
            )
            organo = self._obtener_valor_columna(
                row_clean, headers, ["ÓRGANO", "RESPONSABLE", "ÓRGANO RESPONSABLE"]
            )
            fecha_inicio = self._obtener_valor_columna(
                row_clean, headers, ["INICIO", "FECHA DE INICIO"]
            )
            fecha_fin = self._obtener_valor_columna(
                row_clean,
                headers,
                ["TÉRMINO", "FECHA DE TÉRMINO", "FECHA DE TÉRMINO (*)"],
            )
            medio = self._obtener_valor_columna(
                row_clean, headers, ["MEDIO", "VERIFICACIÓN", "MEDIO DE VERIFICACIÓN"]
            )
            comentarios = self._obtener_valor_columna(
                row_clean,
                headers,
                ["COMENTARIOS", "OBSERVACIONES", "COMENTARIOS U OBSERVACIONES"],
            )

            if medida or organo or medio:
                remediacion = {
                    "numero_fila": num_fila,
                    "deficiencia": deficiencia_actual if deficiencia_actual else None,
                    "medida_remediacion": limpiar_texto(medida) if medida else "",
                    "organo_responsable": limpiar_texto(organo) if organo else "",
                    "fecha_inicio": convertir_fecha(fecha_inicio)
                    if fecha_inicio
                    else None,
                    "fecha_fin": convertir_fecha(fecha_fin) if fecha_fin else None,
                    "medio_verificacion": limpiar_texto(medio) if medio else "",
                    "comentarios": limpiar_texto(comentarios) if comentarios else None,
                }
                remediaciones.append(remediacion)

        return remediaciones

    def _obtener_numero_fila(
        self, row: List[str], headers: List[str], idx: int
    ) -> Optional[int]:
        if row[0] and row[0].strip().isdigit():
            return int(row[0].strip())

        if idx == 1:
            return 1

        if any(row):
            return idx

        return None

    def _obtener_valor_columna(
        self, row: List[str], headers: List[str], nombres: List[str]
    ) -> Optional[str]:
        for nombre in nombres:
            for i, header in enumerate(headers):
                if nombre.upper() in header.upper():
                    if i < len(row):
                        return row[i]
        return None
