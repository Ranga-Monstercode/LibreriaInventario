
// Script específico para la página de login
document.addEventListener('DOMContentLoaded', function() {
    const html = document.documentElement;
    const loginToggle = document.getElementById('loginDarkModeToggle');
    const loginThemeIcon = document.getElementById('loginThemeIcon');
    const loginThemeText = document.getElementById('loginThemeText');
    
    if (loginToggle && loginThemeIcon && loginThemeText) {
        // Cargar tema guardado o detectar preferencia del sistema
        let savedTheme = localStorage.getItem('libreria-theme');
        
        if (!savedTheme) {
            savedTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        
        html.setAttribute('data-bs-theme', savedTheme);
        loginToggle.checked = savedTheme === 'dark';
        updateLoginThemeUI(savedTheme);
        
        // Event listener para el toggle de login
        loginToggle.addEventListener('change', function() {
            const newTheme = this.checked ? 'dark' : 'light';
            html.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('libreria-theme', newTheme);
            updateLoginThemeUI(newTheme);
            
            // Animación del icono
            loginThemeIcon.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                loginThemeIcon.style.transform = 'rotate(0deg)';
            }, 300);
        });
        
        function updateLoginThemeUI(theme) {
            if (theme === 'dark') {
                loginThemeIcon.className = 'fas fa-sun';
                loginThemeText.textContent = 'Modo Claro';
            } else {
                loginThemeIcon.className = 'fas fa-moon';
                loginThemeText.textContent = 'Modo Oscuro';
            }
        }
    }
    
    // Animación de entrada para los campos del formulario
    const formElements = document.querySelectorAll('.form-floating');
    formElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
    });
    
    // Efecto de focus en los inputs
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
});
