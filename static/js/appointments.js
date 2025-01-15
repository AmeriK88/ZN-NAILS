document.addEventListener("DOMContentLoaded", function () {
    const serviceSelect = document.getElementById('id_service');
    const dateInput = document.getElementById('id_date');
    const timeSelect = document.getElementById('id_time');

    function loadAvailableTimes() {
        const serviceId = serviceSelect.value;
        const selectedDate = dateInput.value;

        if (serviceId && selectedDate) {
            // Petición al backend para obtener las horas disponibles
            fetch(`/appointments/load-available-times/?service_id=${serviceId}&date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    // Limpiar opciones previas
                    timeSelect.innerHTML = '<option value="">Selecciona una hora</option>';

                    if (data.times && data.times.length > 0) {
                        data.times.forEach(time => {
                            const option = document.createElement("option");
                            option.value = time;
                            option.textContent = time;
                            timeSelect.appendChild(option);
                        });
                    } else {
                        const option = document.createElement("option");
                        option.value = "";
                        option.textContent = "No hay horarios disponibles";
                        timeSelect.appendChild(option);
                    }
                })
                .catch(error => {
                    console.error('Error al cargar horarios:', error);
                });
        }
    }

    // Escuchar cambios en el servicio y la fecha
    if (serviceSelect) {
        serviceSelect.addEventListener('change', loadAvailableTimes);
    }

    if (dateInput) {
        dateInput.addEventListener('change', loadAvailableTimes);
    }
});
