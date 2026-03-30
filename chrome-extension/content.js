// Content script - se ejecuta en la página del formulario
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'fillForm') {
        fillForm(message);
        sendResponse({ success: true });
    }
    return true;
});

function fillForm(data) {
    // Buscar el modal dialogRemediacion
    const modal = document.getElementById('dialogRemediacion');
    
    if (!modal) {
        console.error('No se encontró el modal dialogRemediacion');
        alert('Abre primero el formulario de remediación');
        return;
    }
    
    // Función para esperar a que el modal esté visible
    const waitForModal = () => {
        return new Promise((resolve) => {
            if (modal.classList.contains('hide') || modal.style.display === 'none') {
                // El modal está oculto, intentar abrirlo o notificar
                console.log('Modal oculto, asegura que esté abierto');
                resolve(false);
            } else {
                resolve(true);
            }
        });
    };
    
    // Fechas por defecto
    const FECHA_INICIO_DEFAULT = '03/04/2026';
    const FECHA_FIN_DEFAULT = '31/10/2026';
    
    // Llenar los campos
    setTimeout(() => {
        // Medida de Remediación
        const txtMedidaRemediacion = document.getElementById('txtMedidaRemediacion');
        if (txtMedidaRemediacion) {
            txtMedidaRemediacion.value = data.medida || '';
            triggerChange(txtMedidaRemediacion);
        }
        
        // Órgano o Unidad Orgánica
        const txtUnidadOrganica = document.getElementById('txtUnidadOrganica');
        if (txtUnidadOrganica) {
            txtUnidadOrganica.value = data.organo || '';
            triggerChange(txtUnidadOrganica);
        }
        
        // Fecha Inicio (por defecto)
        const txtFechaInicio = document.getElementById('txtFechaInicio');
        if (txtFechaInicio) {
            txtFechaInicio.value = FECHA_INICIO_DEFAULT;
            triggerChange(txtFechaInicio);
        }
        
        // Fecha Término (por defecto)
        const txtFechaTermino = document.getElementById('txtFechaTermino');
        if (txtFechaTermino) {
            txtFechaTermino.value = FECHA_FIN_DEFAULT;
            triggerChange(txtFechaTermino);
        }
        
        // Medios de Verificación
        const txtMedioVerificacion = document.getElementById('txtMedioVerificacion');
        if (txtMedioVerificacion) {
            txtMedioVerificacion.value = data.medioVerificacion || '';
            triggerChange(txtMedioVerificacion);
        }
        
        // Comentarios
        const txtComentario = document.getElementById('txtComentario');
        if (txtComentario) {
            txtComentario.value = data.comentarios || '';
            triggerChange(txtComentario);
        }
        
        console.log('Formulario llenado correctamente');
    }, 100);
}

function triggerChange(element) {
    // Trigger events para que el formulario detecte los cambios
    const events = ['input', 'change', 'blur'];
    events.forEach(eventType => {
        element.dispatchEvent(new Event(eventType, { bubbles: true }));
    });
}

function formatFecha(fechaStr) {
    // Convierte YYYY-MM-DD a DD/MM/YYYY
    if (!fechaStr) return '';
    
    const fecha = new Date(fechaStr);
    if (isNaN(fecha.getTime())) return fechaStr;
    
    const day = String(fecha.getDate()).padStart(2, '0');
    const month = String(fecha.getMonth() + 1).padStart(2, '0');
    const year = fecha.getFullYear();
    
    return `${day}/${month}/${year}`;
}
