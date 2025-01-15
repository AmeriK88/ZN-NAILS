document.addEventListener('DOMContentLoaded', function() {
    // 1️⃣ Selecciona todos los elementos con la clase 'fade-in'
    const fadeElements = document.querySelectorAll('.fade-in');

    // 2️⃣ Crea un observer que vigila si el elemento entra en la vista
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            // 3️⃣ Si el elemento es visible, se le añade la clase 'visible'
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    });

    // 4️⃣ Aplica el observer a cada elemento con 'fade-in'
    fadeElements.forEach(el => observer.observe(el));
});
