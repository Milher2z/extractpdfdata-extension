# SCI Form Filler

Este proyecto consta de dos partes principales diseñadas para automatizar y facilitar la carga de medidas de remediación y deficiencias del Sistema de Control Interno (SCI) a la plataforma web de la Contraloría: un backend en Python (FastAPI) que procesa archivos PDF y una extensión de Google Chrome que extrae estos datos e inyecta la información en el formulario web.

## Componentes del Proyecto

### 1. Backend (Python + FastAPI)
Una API RESTful que recibe documentos PDF, extrae su texto, analiza las tablas de preguntas, deficiencias y medidas de remediación empleando `pdfplumber`, y guarda los resultados estructurados en una base de datos local SQLite.

**Principales características:**
- Extrae con precisión las tablas del PDF original preservando los espacios y evitando truncamientos de filas.
- Guarda la información localmente de forma persistente.
- Expone los datos ("Preguntas" y sus "Remediaciones") a través de endpoints REST.

**Cómo ejecutarlo:**
1. Instala las dependencias: `pip install -r requirements.txt`
2. Inicia el servidor de desarrollo: `uvicorn app.main:app --reload` (Correrá por defecto en `http://127.0.0.1:8000`).

### 2. Extensión de Google Chrome
Una extensión cliente diseñada para interactuar directamente con la plataforma web del SCI.

**Principales características:**
- **Panel de Interfaz (Popup)**: Permite visualizar las preguntas y sus medidas de remediación extraídas, con función de búsqueda integrada.
- **Inyector Automático (Content Script)**: Se conecta a la página activa del formulario del SCI y "escribe" (inyecta) toda la información de la medida de remediación seleccionada directamente en los inputs del DOM, evadiendo restricciones de enmascaramiento como InputMask.

**Cómo instalarla:**
1. Abre tu navegador Google Chrome y dirígete a `chrome://extensions/`.
2. Activa el **Modo Desarrollador** arriba a la derecha.
3. Haz clic en **Cargar Descomprimida** ("Load unpacked").
4. Selecciona la carpeta `chrome-extension` de este repositorio.

## Flujo de Trabajo

1. Mantén la API ejecutándose en segundo plano (e.g., puerto `8000`).
2. Sube los archivos PDF correspondientes al backend (puedes usar un cliente REST o scripts automatizados).
3. Abre la Extensión desde la ventana donde tengas la web del SCI.
4. Verifica que la extensión apunta a la URL correcta de la API en el cuadro de configuración superior.
5. Selecciona la pregunta/remediación en la lista y presiona **Fill** para inyectar los datos en el diálogo web activo.
