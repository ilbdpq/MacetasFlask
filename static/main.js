function agregarFila() {
    const fila = document.querySelector('.agregarFila');
    const nuevaFila = fila.cloneNode(true);

    // Limpiar los valores de los inputs/selects en la nueva fila
    nuevaFila.querySelectorAll('input, select').forEach(el => {
        if (el.type === 'number' || el.type === 'text' || el.type === 'date') {
            el.value = '';
        }
    });

    // Insertar la nueva fila antes del botón "Subir"
    const tabla = fila.closest('tbody');
    const submitRow = tabla.querySelector('tr:last-child');
    tabla.insertBefore(nuevaFila, submitRow);
}

function controlRueda(e, input, step) {
    e.preventDefault();

    let value = parseFloat(input.value) || 0;
    let multiplier = e.shiftKey && e.ctrlKey ? 100 : e.shiftKey ? 10 : 1;
    let delta = (e.deltaY < 0 ? 1 : -1) * step * multiplier;
    let newValue = value + delta;

    if (input.min !== undefined && newValue < parseFloat(input.min)) newValue = parseFloat(input.min);
    
    input.value = Math.round(newValue * 100000) / 100000;
    input.dispatchEvent(new Event('input'));
}