# SCI Form Filler - Extensión Chrome

Extensión para automatizar el llenado de formularios de medidas de remediación del Sistema de Control Interno (SCI) de la Contraloría Perú.

## Requisitos

1. **API corriendo**: El servidor FastAPI debe estar ejecutándose
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **PDF procesado**: El PDF con las 63 preguntas debe estar subido a la API

## Instalación

1. Abre Chrome y navega a `chrome://extensions/`
2. Activa el **"Modo de desarrollador"** (esquina superior derecha)
3. Haz clic en **"Cargar descomprimida"**
4. Selecciona la carpeta `chrome-extension/`

## Uso

1. Asegúrate de que la API esté corriendo en `http://127.0.0.1:8000`
2. Abre el aplicativo SCI de la Contraloría Perú
3. Navega a la sección de Medidas de Remediación
4. Haz clic en "Nuevo" o selecciona una fila para editar (esto abre el modal `dialogRemediacion`)
5. Haz clic en el icono de la extensión en Chrome
6. Busca la pregunta y selecciona la fila de remediación
7. Haz clic en "Llenar Formulario"

## Cómo funciona

- La extensión se conecta a la API para obtener las preguntas y remediaciones
- Cuando haces clic en "Llenar", envía los datos al content script
- El content script llena los campos del formulario:
  - `txtDeficiencia`
  - `txtMedidaRemediacion`
  - `txtUnidadOrganica`
  - `txtFechaInicio`
  - `txtFechaTermino`
  - `txtMedioVerificacion`
  - `txtComentario`

## Solución de problemas

- **API no conecta**: Verifica que el servidor esté corriendo y la URL sea correcta
- **Formulario no se llena**: Asegúrate de que el modal `dialogRemediacion` esté abierto
- **Fechas incorrectas**: El formulario usa formato DD/MM/AAAA

## Archivos

- `manifest.json` - Configuración de la extensión
- `popup.html` - Interfaz de usuario
- `popup.js` - Lógica del popup
- `content.js` - Script que interactúa con la página
- `icon.svg` - Icono de la extensión
