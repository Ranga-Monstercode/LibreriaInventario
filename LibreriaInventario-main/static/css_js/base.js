// Función para inicializar el toggle de tema
function initThemeToggle() {
    const html = document.documentElement;
    const toggle = document.getElementById('darkModeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    if (!toggle || !themeIcon) return;
    
    // Cargar tema guardado o detectar preferencia del sistema
    let savedTheme = localStorage.getItem('libreria-theme');
    
    // Si no hay tema guardado, detectar preferencia del sistema
    if (!savedTheme) {
        savedTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    
    html.setAttribute('data-bs-theme', savedTheme);
    toggle.checked = savedTheme === 'dark';
    updateThemeIcon(savedTheme);
    
    // Event listener para el cambio de tema
    toggle.addEventListener('change', function() {
        const newTheme = this.checked ? 'dark' : 'light';
        html.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('libreria-theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Animación del icono
        themeIcon.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            themeIcon.style.transform = 'rotate(0deg)';
        }, 300);
        
        // Efecto de ondas
        createRippleEffect();
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun theme-icon';
            themeIcon.title = 'Cambiar a modo claro';
        } else {
            themeIcon.className = 'fas fa-moon theme-icon';
            themeIcon.title = 'Cambiar a modo oscuro';
        }
    }
    
    function createRippleEffect() {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            background: rgba(13, 110, 253, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
            z-index: 9999;
        `;
        
        document.body.appendChild(ripple);
        
        setTimeout(() => {
            document.body.removeChild(ripple);
        }, 600);
    }
    
    // CSS para la animación de ondas
    if (!document.getElementById('ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    width: 200px;
                    height: 200px;
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Detectar cambios en la preferencia del sistema
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem('libreria-theme')) {
        const newTheme = e.matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        const toggle = document.getElementById('darkModeToggle');
        if (toggle) {
            toggle.checked = newTheme === 'dark';
        }
    }
});

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initThemeToggle);

// También ejecutar inmediatamente para evitar flash
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeToggle);
} else {
    initThemeToggle();
}
