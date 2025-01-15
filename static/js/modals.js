document.addEventListener('DOMContentLoaded', function () {
    // Botón para abrir el modal de login desde el registro
    const loginButtons = document.querySelectorAll('.open-login-modal');

    loginButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Cerrar el modal de registro si está abierto
            const registerModalEl = document.getElementById('registerModal');
            const registerModal = bootstrap.Modal.getInstance(registerModalEl);
            if (registerModal) {
                registerModal.hide();
            }

            // Abrir el modal de login
            const loginModalEl = document.getElementById('loginModal');
            const loginModal = new bootstrap.Modal(loginModalEl);
            loginModal.show();
        });
    });
});
