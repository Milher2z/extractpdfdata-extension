import re
from datetime import date, datetime
from typing import Optional


def limpiar_texto(texto: str) -> str:
    if not texto:
        return ""

    texto = texto.replace("\n", " ")
    texto = texto.replace("\r", " ")
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.strip()

    texto = _corregir_problemas_comunes(texto)

    return texto


def _corregir_problemas_comunes(texto: str) -> str:
    texto = texto.replace("\ufffd", "")
    texto = texto.replace("\x00", "")

    fixes = [
        ("Funci", "Función"),
        ("P blica", "Pública"),
        ("P�blica", "Pública"),
        ("�tica", "ética"),
        ("Capacitaci", "Capacitación"),
        ("seglose", "seglose"),
        ("seseguir", "se seguirá"),
        ("seglol", "seglol"),
        ("establezcaque", "establezca que"),
        ("participende", "participen de"),
        ("decapacitaciones", "de capacitaciones"),
        ("capacitacionessobre", "capacitaciones sobre"),
        ("implementaci", "implementación"),
        ("participacion", "participación"),
        ("nformaci", "información"),
        ("Informaci", "Información"),
        ("nformaci", "información"),
        ("lascapacitaciones", "las capacitaciones"),
        ("funcionesde", "funciones de"),
        ("contenidodel", "contenido del"),
        ("conocimiento", "conocimiento"),
        ("conocimientoy", "conocimiento y"),
        ("precisael", "precisa el"),
        ("delacapacitaci", "de la capacitación"),
        ("Certificadode", "Certificado de"),
        ("cursode", "curso de"),
        ("horassobre", "horas sobre"),
        ("materiala", "material a"),
        ("coordinarcon", "coordinar con"),
        ("puntoser", "punto serán"),
        ("elpunto", "el punto"),
        ("serán", "serán"),
        ("exigible", "exigible"),
        ("EscuelaNacional", "Escuela Nacional"),
        ("ContraloríaGeneral", "Contraloría General"),
        ("Reposición", "República"),
        ("organoresponsable", "órgano responsable"),
        ("deinformacion", "de información"),
        ("ejecucionde", "ejecución de"),
        ("porcentajede", "porcentaje de"),
        ("númerototal", "número total"),
        ("fechacorte", "fecha corte"),
        ("cautelar", "cautelar"),
        ("autilizar", "a utilizar"),
    ]

    for wrong, correct in fixes:
        if wrong in texto:
            texto = texto.replace(wrong, correct)

    return texto


def _agregar_espacios(texto: str) -> str:
    texto = re.sub(r"([a-záéíóúñ])([A-ZÁÉÍÓÚÑ])", r"\1 \2", texto)

    word_boundaries = [
        (r"\bde\b(\w)", r"de \1"),
        (r"\bla\b(\w)", r"la \1"),
        (r"\bel\b(\w)", r"el \1"),
        (r"\bdel\b(\w)", r"del \1"),
        (r"\by\b(\w)", r"y \1"),
        (r"\bo\b(\w)", r"o \1"),
        (r"\bque\b(\w)", r"que \1"),
        (r"\bse\b(\w)", r"se \1"),
        (r"\bsu\b(\w)", r"su \1"),
        (r"\bcon\b(\w)", r"con \1"),
        (r"\bsobre\b(\w)", r"sobre \1"),
        (r"\bpara\b(\w)", r"para \1"),
        (r"\bpor\b(\w)", r"por \1"),
    ]

    for pattern, replacement in word_boundaries:
        try:
            texto = re.sub(pattern, replacement, texto)
        except:
            pass

    texto = re.sub(r"\s+", " ", texto)

    return texto


def convertir_fecha(fecha_str: str) -> Optional[date]:
    if not fecha_str:
        return None

    fecha_str = fecha_str.strip()

    formatos = [
        "%d-%m-%y",
        "%d/%m/%y",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
    ]

    for fmt in formatos:
        try:
            fecha = datetime.strptime(fecha_str, fmt).date()
            return fecha
        except ValueError:
            continue

    return None


def formatear_fecha_iso(fecha: Optional[date]) -> Optional[str]:
    if fecha:
        return fecha.isoformat()
    return None
