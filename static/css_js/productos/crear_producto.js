document.addEventListener('DOMContentLoaded', function() {
    // Agregar clases de Bootstrap a los campos del formulario
    const formFields = document.querySelectorAll('input, select, textarea');
    formFields.forEach(field => {
        if (!field.type || field.type !== 'checkbox') {
            if (field.tagName.toLowerCase() === 'select') {
                field.classList.add('form-select');
            } else {
                field.classList.add('form-control');
            }
        }
    });

    // Agregar placeholder a los campos para que funcione el floating label
    const inputs = document.querySelectorAll('.form-floating input, .form-floating textarea');
    inputs.forEach(input => {
        if (!input.placeholder) {
            input.placeholder = ' ';
        }
    });

    // Efecto de focus en los campos
    const allFields = document.querySelectorAll('.form-control, .form-select');
    allFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        field.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });

    // Animación de entrada para las cards
    const cards = document.querySelectorAll('.form-card, .info-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = index === 0 ? 'translateX(-30px)' : 'translateX(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateX(0)';
        }, 100 + (index * 200));
    });

    // Validación visual en tiempo real
    const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredFields.forEach(field => {
        field.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.style.borderColor = '#28a745';
                this.style.boxShadow = '0 0 0 0.2rem rgba(40, 167, 69, 0.25)';
            } else {
                this.style.borderColor = 'var(--border-color)';
                this.style.boxShadow = 'none';
            }
        });
    });
});