function agregarFila() {
    const fila = document.querySelector('.agregarFila');
    if (!fila) return;

    const nuevaFila = fila.cloneNode(true);

    limpiarCampos(nuevaFila);
    prepararBotonEliminar(nuevaFila);

    const tabla = fila.closest('tbody');
    const submitRow = tabla?.querySelector('tr:last-child');
    if (tabla && submitRow) {
        tabla.insertBefore(nuevaFila, submitRow);
    }
}

function limpiarCampos(fila) {
    fila.querySelectorAll('input[type="number"], input[type="text"], input[type="date"]')
        .forEach(el => el.value = '');

    fila.querySelectorAll('select').forEach(select => {
        select.selectedIndex = 0; // vuelve a la primera opción
    });
}

function prepararBotonEliminar(fila) {
    const boton = fila.querySelector('input[type="button"]');
    if (boton) {
        boton.value = '-';
        boton.onclick = () => eliminarFila(fila);
    }
}

function eliminarFila(fila) {
    fila.remove();
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