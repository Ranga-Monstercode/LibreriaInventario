document.addEventListener('DOMContentLoaded', function() {
    // Agregar clases de Bootstrap a los campos del formulario
    const formFields = document.querySelectorAll('input, select');
    formFields.forEach(field => {
        if (field.tagName.toLowerCase() === 'select') {
            field.classList.add('form-select');
        } else {
            field.classList.add('form-control');
        }
    });

    // Agregar placeholder a los campos para que funcione el floating label
    const inputs = document.querySelectorAll('.form-floating input');
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
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    requiredFields.forEach(field => {
        field.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.style.borderColor = '#007bff';
                this.style.boxShadow = '0 0 0 0.2rem rgba(0, 123, 255, 0.25)';
            } else {
                this.style.borderColor = 'var(--border-color)';
                this.style.boxShadow = 'none';
            }
        });
    });

    // Efecto de animación en el icono de usuario
    const userIcon = document.querySelector('.user-icon');
    if (userIcon) {
        userIcon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
            this.style.color = '#6610f2';
        });
        
        userIcon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.color = '#007bff';
        });
    }

    // Medidor de fortaleza de contraseña
    const passwordField = document.querySelector('input[name="password1"]');
    const strengthContainer = document.getElementById('passwordStrength');
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');

    if (passwordField && strengthContainer) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            
            if (password.length > 0) {
                strengthContainer.style.display = 'block';
                updateStrengthIndicator(strength);
            } else {
                strengthContainer.style.display = 'none';
            }
        });
    }

    function calculatePasswordStrength(password) {
        let score = 0;
        
        if (password.length >= 8) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^A-Za-z0-9]/.test(password)) score++;
        
        return score;
    }

    function updateStrengthIndicator(strength) {
        strengthFill.className = 'strength-fill';
        
        switch(strength) {
            case 0:
            case 1:
                strengthFill.classList.add('strength-weak');
                strengthText.textContent = 'Contraseña débil';
                strengthText.style.color = '#dc3545';
                break;
            case 2:
                strengthFill.classList.add('strength-fair');
                strengthText.textContent = 'Contraseña regular';
                strengthText.style.color = '#ffc107';
                break;
            case 3:
            case 4:
                strengthFill.classList.add('strength-good');
                strengthText.textContent = 'Contraseña buena';
                strengthText.style.color = '#007bff';
                break;
            case 5:
                strengthFill.classList.add('strength-strong');
                strengthText.textContent = 'Contraseña fuerte';
                strengthText.style.color = '#6610f2';
                break;
        }
    }

    // Validación de confirmación de contraseña
    const confirmPasswordField = document.querySelector('input[name="password2"]');
    if (passwordField && confirmPasswordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (this.value === passwordField.value && this.value.length > 0) {
                this.style.borderColor = '#007bff';
                this.style.boxShadow = '0 0 0 0.2rem rgba(0, 123, 255, 0.25)';
            } else if (this.value.length > 0) {
                this.style.borderColor = '#dc3545';
                this.style.boxShadow = '0 0 0 0.2rem rgba(220, 53, 69, 0.25)';
            } else {
                this.style.borderColor = 'var(--border-color)';
                this.style.boxShadow = 'none';
            }
        });
    }

    // Efecto hover en las cards de roles
    const roleCards = document.querySelectorAll('.role-card');
    roleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0) scale(1)';
        });
    });
});