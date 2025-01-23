// Mostrar el loader
function showLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.add('show');
    }
}

// Ocultar el loader
function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.remove('show');
    }
}

// Ocultar el loader al cargar la página
window.addEventListener('load', () => {
    hideLoader();
});

// Ocultar el loader al regresar a la página (desde caché o enlaces externos)
window.addEventListener('pageshow', (event) => {
    if (event.persisted || document.readyState === 'complete') {
        hideLoader(); // Asegura que el loader desaparezca al volver
    }
});

// Manejo de visibilidad de la pestaña
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        hideLoader(); // Oculta el loader si se regresa a la pestaña
    }
});

// Mostrar el loader al enviar formularios
document.addEventListener('submit', (event) => {
    showLoader();
    // Si hay errores en el formulario, oculta el loader después de un breve tiempo
    setTimeout(() => {
        hideLoader();
    }, 1000); // Ajusta el tiempo según tus necesidades
});

// Mostrar el loader al hacer clic en enlaces o botones
document.querySelectorAll('a, button').forEach((el) => {
    el.addEventListener('click', (event) => {
        const href = el.getAttribute('href');

        if (href && href.startsWith('#')) {
            // Si es un anclaje, mostrar el loader brevemente
            showLoader();
            setTimeout(() => {
                hideLoader();
            }, 300); // Ajusta el tiempo según la animación
        } else if (
            (el.tagName === 'A' && href && href !== '#' && !href.startsWith('javascript:')) ||
            (el.tagName === 'BUTTON' && el.type === 'submit')
        ) {
            // Evitar mostrar el loader para enlaces externos con target="_blank"
            const target = el.getAttribute('target');
            if (!target || target !== '_blank') {
                showLoader();
            }
        }
    });
});

// Mostrar el loader antes de redirecciones específicas (formularios de inicio y cierre de sesión)
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', () => {
        showLoader();
    });
}

const logoutLink = document.getElementById('logout-link');
if (logoutLink) {
    logoutLink.addEventListener('click', () => {
        showLoader();
    });
}

// Forzar el ocultamiento del loader al salir de la página
window.addEventListener('beforeunload', () => {
    showLoader(); // Limpia cualquier estado residual
});
