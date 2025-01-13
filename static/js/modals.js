document.addEventListener('DOMContentLoaded', function () {
    if (window.showLoginModal) {
        var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
        loginModal.show();
    }

    if (window.showRegisterModal) {
        var registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
        registerModal.show();
    }
});
