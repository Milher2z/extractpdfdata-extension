let preguntas = [];
let preguntaSeleccionada = null;
let remediacionSeleccionada = null;

const apiUrlInput = document.getElementById('apiUrl');
const searchInput = document.getElementById('searchInput');
const preguntasList = document.getElementById('preguntasList');
const remediacionesSection = document.getElementById('remediacionesSection');
const remediacionesList = document.getElementById('remediacionesList');
const btnFill = document.getElementById('btnFill');
const errorDiv = document.getElementById('error');

async function loadAPIUrl() {
    const result = await chrome.storage.local.get('apiUrl');
    if (result.apiUrl) {
        apiUrlInput.value = result.apiUrl;
    }
}

apiUrlInput.addEventListener('change', async () => {
    await chrome.storage.local.set({ apiUrl: apiUrlInput.value });
    loadPreguntas();
});

async function loadPreguntas() {
    const apiUrl = apiUrlInput.value;
    preguntasList.innerHTML = '<div class="loading">Cargando...</div>';
    errorDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${apiUrl}/preguntas/`);
        if (!response.ok) throw new Error('Error al conectar con la API');
        
        preguntas = await response.json();
        renderPreguntas(preguntas);
    } catch (error) {
        preguntasList.innerHTML = '';
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

function renderPreguntas(lista) {
    preguntasList.innerHTML = '';
    
    if (lista.length === 0) {
        preguntasList.innerHTML = '<div class="empty">No se encontraron preguntas</div>';
        return;
    }
    
    lista.forEach(p => {
        const div = document.createElement('div');
        div.className = 'pregunta-item';
        div.innerHTML = `
            <div class="pregunta-numero">Pregunta ${p.numero}</div>
            <div class="pregunta-titulo">${p.titulo || 'Sin título'}</div>
        `;
        div.addEventListener('click', () => selectPregunta(p));
        preguntasList.appendChild(div);
    });
}

async function selectPregunta(pregunta) {
    preguntaSeleccionada = pregunta;
    remediacionSeleccionada = null;
    btnFill.disabled = true;
    
    const apiUrl = apiUrlInput.value;
    remediacionesList.innerHTML = '<div class="loading">Cargando...</div>';
    remediacionesSection.style.display = 'block';
    
    try {
        const response = await fetch(`${apiUrl}/preguntas/${pregunta.id}/formulario`);
        if (!response.ok) throw new Error('Error al cargar remediaciones');
        
        const data = await response.json();
        renderRemediaciones(data);
    } catch (error) {
        remediacionesList.innerHTML = '';
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

function renderRemediaciones(data) {
    remediacionesList.innerHTML = '';
    
    if (!data.remediaciones || data.remediaciones.length === 0) {
        remediacionesList.innerHTML = '<div class="empty">Sin remediaciones</div>';
        return;
    }
    
    data.remediaciones.forEach((rem, index) => {
        const div = document.createElement('div');
        div.className = 'remediacion-item';
        div.innerHTML = `
            <div class="remediacion-numero">Fila ${rem.fila}</div>
            <div class="remediacion-preview">${rem.medida || 'Sin medida'}</div>
        `;
        div.addEventListener('click', () => {
            document.querySelectorAll('.remediacion-item').forEach(el => el.classList.remove('selected'));
            div.classList.add('selected');
            remediacionSeleccionada = rem;
            btnFill.disabled = false;
        });
        remediacionesList.appendChild(div);
    });
}

searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const filtered = preguntas.filter(p => 
        p.numero.includes(query) || 
        (p.titulo && p.titulo.toLowerCase().includes(query))
    );
    renderPreguntas(filtered);
});

btnFill.addEventListener('click', async () => {
    if (!remediacionSeleccionada) return;
    
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, {
        action: 'fillForm',
        medida: remediacionSeleccionada.medida,
        organo: remediacionSeleccionada.organo,
        medioVerificacion: remediacionSeleccionada.medio_verificacion,
        comentarios: remediacionSeleccionada.comentarios,
        fechaInicio: remediacionSeleccionada.fecha_inicio,
        fechaFin: remediacionSeleccionada.fecha_fin
    });
});

loadAPIUrl().then(loadPreguntas);
