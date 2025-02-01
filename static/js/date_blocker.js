document.addEventListener("DOMContentLoaded", function () {
    const dateField = document.getElementById("id_date");
    const timeField = document.getElementById("id_time");
    const serviceField = document.getElementById("id_service");

    if (dateField && timeField && serviceField) {
        function verificarFechaBloqueada() {
            const selectedDate = dateField.value;
            const serviceId = serviceField.value;

            if (selectedDate && serviceId) {  // Aseguramos que ambos valores existan
                fetch(`/appointments/load-available-times/?service_id=${serviceId}&date=${selectedDate}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.blocked) {
                            showAlert(` Fecha no disponible: ${data.motivo || "Sin motivo especificado"} ⚠️`);
                            timeField.innerHTML = '<option value="">Seleccione otra fecha</option>';
                        } else {
                            timeField.innerHTML = data.times.length > 0 ?
                                data.times.map(time => `<option value="${time}">${time}</option>`).join('') :
                                '<option value="">No hay horarios disponibles</option>';
                        }
                    })
                    .catch(error => console.error("Error al cargar horarios:", error));
            }
        }

        // ** Comprobamos si la cita ya tiene una fecha y un servicio en la edición**
        if (dateField.value && serviceField.value) {
            verificarFechaBloqueada();  // Se ejecuta en la carga de la página si hay valores
        }

        // ** Detectar cambios en la fecha y el servicio**
        dateField.addEventListener("change", verificarFechaBloqueada);
        serviceField.addEventListener("change", verificarFechaBloqueada);
    }
});

/**
 * Muestra una alerta en la pantalla con el motivo del bloqueo.
 */
function showAlert(message) {
    const alertDiv = document.createElement("div");
    alertDiv.classList.add("alert", "alert-warning", "alert-dismissible", "fade", "show");
    alertDiv.setAttribute("role", "alert");
    alertDiv.innerHTML = `
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    document.body.prepend(alertDiv);

    setTimeout(() => {
        alertDiv.classList.remove("show");
        alertDiv.classList.add("fade");
        setTimeout(() => alertDiv.remove(), 500);
    }, 5000);
}
