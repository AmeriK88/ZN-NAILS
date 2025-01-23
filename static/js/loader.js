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
    hideLoader(); 
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
    // Ocultar loader si el formulario tiene errores después de un tiempo
    setTimeout(() => {
        hideLoader();
    }, 1000); 
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
            }, 300); 
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

// Forzar el ocultamiento del loader al salir de la página
window.addEventListener('beforeunload', () => {
    hideLoader(); // Limpia cualquier estado residual
});
