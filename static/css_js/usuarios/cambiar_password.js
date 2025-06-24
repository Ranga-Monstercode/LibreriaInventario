// ===== FUNCIONALIDAD PARA CAMBIO DE CONTRASEÑA (SIN RESTRICCIONES) =====

document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos
    const password1Field = document.getElementById(window.passwordFormData.password1FieldId);
    const password2Field = document.getElementById(window.passwordFormData.password2FieldId);
    const submitBtn = document.getElementById('submitBtn');
    
    // Inicializar validaciones
    initPasswordValidation();
    
    function initPasswordValidation() {
        if (!password1Field || !password2Field || !submitBtn) {
            console.error('No se encontraron los campos de contraseña');
            return;
        }
        
        // Event listeners para validación en tiempo real
        password1Field.addEventListener('input', function() {
            checkPasswordMatch();
            updateSubmitButton();
        });
        
        password2Field.addEventListener('input', function() {
            checkPasswordMatch();
            updateSubmitButton();
        });
        
        // Event listener para el formulario
        document.querySelector('form').addEventListener('submit', handleFormSubmit);
        
        // Habilitar botón inicialmente
        updateSubmitButton();
    }
    
    /**
     * Verifica si las contraseñas coinciden
     */
    function checkPasswordMatch() {
        const password1 = password1Field.value;
        const password2 = password2Field.value;
        const matchDiv = document.getElementById('passwordMatch');
        const noMatchDiv = document.getElementById('passwordNoMatch');
        
        if (!matchDiv || !noMatchDiv) return;
        
        if (password2.length === 0) {
            matchDiv.style.display = 'none';
            noMatchDiv.style.display = 'none';
        } else if (password1 === password2) {
            matchDiv.style.display = 'block';
            noMatchDiv.style.display = 'none';
        } else {
            matchDiv.style.display = 'none';
            noMatchDiv.style.display = 'block';
        }
    }
    
    /**
     * Actualiza el estado del botón de envío
     * SOLO requiere que las contraseñas coincidan (pueden estar vacías)
     */
    function updateSubmitButton() {
        const password1 = password1Field.value;
        const password2 = password2Field.value;
        
        // Permitir contraseñas vacías y solo verificar que coincidan
        const isValid = password1 === password2;
        
        submitBtn.disabled = !isValid;
        
        if (isValid) {
            submitBtn.classList.remove('btn-secondary');
            submitBtn.classList.add('btn-warning');
        } else {
            submitBtn.classList.remove('btn-warning');
            submitBtn.classList.add('btn-secondary');
        }
    }
    
    /**
     * Maneja el envío del formulario con modal personalizado
     */
    function handleFormSubmit(e) {
        e.preventDefault(); // Prevenir envío automático
        
        const username = window.passwordFormData.username;
        const isOwnAccount = window.passwordFormData.isOwnAccount;
        const password1 = password1Field.value;
        
        // Crear y mostrar modal de confirmación
        showPasswordChangeModal(username, isOwnAccount, password1);
    }
    
    /**
     * Muestra modal de confirmación personalizado
     */
    function showPasswordChangeModal(username, isOwnAccount, password) {
        // Remover modal existente si existe
        const existingModal = document.getElementById('passwordChangeModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Determinar el tipo de advertencia
        let warningContent = '';
        let warningClass = 'alert-info';
        
        if (password.length === 0) {
            warningContent = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>¡ADVERTENCIA CRÍTICA!</strong><br>
                    La contraseña estará <strong>VACÍA</strong>. El usuario no necesitará contraseña para iniciar sesión.
                </div>
            `;
        } else if (password.length < 4) {
            warningContent = `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Advertencia:</strong> La contraseña es muy corta (${password.length} carácter${password.length > 1 ? 'es' : ''}).
                </div>
            `;
        }
        
        const accountTypeContent = isOwnAccount ? 
            `<div class="alert alert-warning">
                <i class="fas fa-user-circle"></i>
                <strong>Cuenta Propia:</strong> Está cambiando su propia contraseña. Su sesión se mantendrá activa.
            </div>` :
            `<div class="alert alert-info">
                <i class="fas fa-user-friends"></i>
                <strong>Otro Usuario:</strong> El usuario deberá usar la nueva contraseña en su próximo inicio de sesión.
            </div>`;
        
        // Crear modal HTML
        const modalHtml = `
            <div class="modal fade" id="passwordChangeModal" tabindex="-1" aria-labelledby="passwordChangeModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-warning text-dark">
                            <h5 class="modal-title" id="passwordChangeModalLabel">
                                <i class="fas fa-key"></i> Confirmar Cambio de Contraseña
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="text-center mb-3">
                                <i class="fas fa-key text-warning" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                                <h6>¿Está seguro que desea cambiar la contraseña?</h6>
                                <p class="text-muted mb-2">
                                    <strong>Usuario:</strong> ${username}
                                </p>
                            </div>
                            
                            ${warningContent}
                            ${accountTypeContent}
                            
                            <div class="alert alert-secondary">
                                <i class="fas fa-info-circle"></i>
                                <strong>Información:</strong><br>
                                Esta acción cambiará inmediatamente la contraseña del usuario en el sistema.
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times"></i> Cancelar
                            </button>
                            <button type="button" class="btn btn-warning" id="confirmPasswordChange">
                                <i class="fas fa-key"></i> Cambiar Contraseña
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('passwordChangeModal'));
        modal.show();
        
        // Manejar confirmación
        document.getElementById('confirmPasswordChange').addEventListener('click', function() {
            modal.hide();
            
            // Mostrar loading
            showLoadingAlert();
            
            // Enviar formulario
            setTimeout(() => {
                document.querySelector('form').submit();
            }, 500);
        });
        
        // Limpiar modal cuando se cierre
        document.getElementById('passwordChangeModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
    
    /**
     * Muestra alerta de carga
     */
    function showLoadingAlert() {
        showAlert('info', '<i class="fas fa-spinner fa-spin"></i> Cambiando contraseña...', false);
    }
});

/**
 * Función global para alternar visibilidad de contraseña
 */
function togglePassword(fieldId, button) {
    const field = document.getElementById(fieldId);
    const icon = button.querySelector('i');
    
    if (!field || !icon) return;
    
    if (field.type === 'password') {
        field.type = 'text';
        icon.className = 'fas fa-eye-slash';
        button.setAttribute('title', 'Ocultar contraseña');
    } else {
        field.type = 'password';
        icon.className = 'fas fa-eye';
        button.setAttribute('title', 'Mostrar contraseña');
    }
}

/**
 * Función para mostrar alertas consistentes
 */
function showAlert(type, message, autoHide = true) {
    // Remover alertas existentes
    const existingAlerts = document.querySelectorAll('.alert.position-fixed');
    existingAlerts.forEach(alert => alert.remove());
    
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    const iconClass = type === 'success' ? 'fa-check-circle' : 
                     type === 'error' ? 'fa-exclamation-triangle' : 
                     type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 500px;" role="alert">
            <i class="fas ${iconClass}"></i> ${message}
            ${autoHide ? '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' : ''}
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-remover después de 5 segundos si autoHide es true
    if (autoHide) {
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert.position-fixed');
            alerts.forEach(alert => {
                if (alert && alert.parentNode) {
                    alert.remove();
                }
            });
        }, 5000);
    }
}