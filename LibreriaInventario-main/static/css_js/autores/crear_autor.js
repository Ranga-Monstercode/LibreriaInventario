document.addEventListener('DOMContentLoaded', function() {
    // Agregar clases de Bootstrap a los campos del formulario
    const formFields = document.querySelectorAll('input, textarea');
    formFields.forEach(field => {
        field.classList.add('form-control');
    });

    // Agregar placeholder a los campos para que funcione el floating label
    const inputs = document.querySelectorAll('.form-floating input, .form-floating textarea');
    inputs.forEach(input => {
        if (!input.placeholder) {
            input.placeholder = ' ';
        }
    });

    // Configurar textarea
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.style.minHeight = '120px';
        textarea.style.resize = 'vertical';
    }

    // Efecto de focus en los campos
    const allFields = document.querySelectorAll('.form-control');
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
    const requiredFields = document.querySelectorAll('input[required], textarea[required]');
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

    // Efecto de animación en el icono de autor
    const authorIcon = document.querySelector('.author-icon');
    if (authorIcon) {
        authorIcon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
            this.style.color = '#20c997';
        });
        
        authorIcon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.color = '#28a745';
        });
    }

    // Contador de caracteres para biografía
    const biografiaField = document.querySelector('textarea[name="biografia"]');
    if (biografiaField) {
        const maxLength = biografiaField.getAttribute('maxlength') || 1000;
        const counter = document.createElement('div');
        counter.className = 'text-muted small mt-1';
        counter.style.textAlign = 'right';
        
        function updateCounter() {
            const remaining = maxLength - biografiaField.value.length;
            counter.textContent = `${biografiaField.value.length}/${maxLength} caracteres`;
            
            if (remaining < 100) {
                counter.style.color = '#dc3545';
            } else if (remaining < 200) {
                counter.style.color = '#ffc107';
            } else {
                counter.style.color = 'var(--text-secondary)';
            }
        }
        
        biografiaField.parentElement.appendChild(counter);
        biografiaField.addEventListener('input', updateCounter);
        updateCounter();
    }
});