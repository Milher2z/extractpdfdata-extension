import os
import sys
from app.extractor import PDFExtractor
import json

files = ["Prueba.pdf", "Prueba 2.pdf", "63 preguntas.pdf"]
for f in files:
    path = os.path.join(r"C:\Users\Milher\Documents\03_Work\Freelance\Jonathan\subirdatos", f)
    print(f"--- Processing {f} ---")
    if not os.path.exists(path):
        print("File not found.")
        continue
    extractor = PDFExtractor(path)
    preguntas = extractor.extraer_todas_las_preguntas()
    print(f"Preguntas extracted: {len(preguntas)}")
    for i, p in enumerate(preguntas[:2]): # print first two as sample
        print(f"Pregunta {p.get('numero')}:")
        remediaciones = p.get('remediaciones', [])
        print(f"  Remediaciones extracted: {len(remediaciones)}")
        for i, r in enumerate(remediaciones):
            print(f"    R{i}: deficiencia: {r.get('deficiencia', '')[:50]}...")
            print(f"        organo: {r.get('organo_responsable', '')[:50]}...")
            print(f"        medida: {r.get('medida_remediacion', '')[:50]}...")
            if r.get("medida_remediacion") and " " not in r.get("medida_remediacion"):
                print("        *** WARNING: No spaces in medida:", repr(r.get("medida_remediacion")))
