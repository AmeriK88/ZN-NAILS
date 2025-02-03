document.addEventListener("DOMContentLoaded", function () {
    const cookiesModalElement = document.getElementById('cookiesModal');
    const privacyPolicyModalElement = document.getElementById('privacyPolicyModal');

    if (!cookiesModalElement || !privacyPolicyModalElement) {
        console.warn("⚠️ No se encontró el modal de cookies o privacidad en el DOM.");
        return;
    }

    const cookiesModal = new bootstrap.Modal(cookiesModalElement);
    const privacyPolicyModal = new bootstrap.Modal(privacyPolicyModalElement);

    // Función para verificar si localStorage está disponible
    function isLocalStorageAvailable() {
        try {
            localStorage.setItem('test', 'test');
            localStorage.removeItem('test');
            return true;
        } catch (e) {
            console.warn("⚠️ localStorage está bloqueado. No se guardará la preferencia de cookies.");
            return false;
        }
    }

    // Verificar si el usuario ya ha aceptado o rechazado las cookies
    if (isLocalStorageAvailable()) {
        const cookiesPreference = localStorage.getItem('cookiesPreference');
        if (!cookiesPreference) {
            cookiesModal.show();
        }
    }

    // Función para manejar el consentimiento de cookies
    function setCookiePreference(preference) {
        if (isLocalStorageAvailable()) {
            localStorage.setItem('cookiesPreference', preference);
        }
        cookiesModal.hide();
        console.log(`Cookies ${preference}.`);
    }

    // Botón "Aceptar"
    document.querySelector('#cookiesModal .btn-primary').addEventListener('click', function () {
        setCookiePreference('accepted');
    });

    // Botón "Rechazar"
    document.querySelector('#cookiesModal .btn-outline-secondary').addEventListener('click', function () {
        setCookiePreference('rejected');
    });

    // Mostrar enlace a la política de privacidad
    document.getElementById('privacyPolicyLink').addEventListener('click', function (event) {
        event.preventDefault();
        privacyPolicyModal.show();
    });
});
