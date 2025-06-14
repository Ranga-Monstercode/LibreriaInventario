document.addEventListener('DOMContentLoaded', function() {
    // Efecto de hover mejorado para las filas
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        if (!row.querySelector('.empty-state')) {
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.01)';
                this.style.zIndex = '10';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.zIndex = '1';
            });
        }
    });

    // Manejo de descripciones truncadas
    const descriptions = document.querySelectorAll('.editorial-description');
    descriptions.forEach(desc => {
        const fullText = desc.getAttribute('title');
        const truncatedText = desc.textContent;
        
        desc.addEventListener('mouseenter', function() {
            if (fullText && fullText !== truncatedText) {
                this.textContent = fullText;
                this.classList.remove('truncated');
            }
        });
        
        desc.addEventListener('mouseleave', function() {
            if (fullText && fullText !== truncatedText) {
                this.textContent = truncatedText;
                this.classList.add('truncated');
            }
        });
    });

    // Animación de entrada para las cards
    const cards = document.querySelectorAll('.editorials-card, .stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });

    // Contador de editoriales
    const editorialCount = document.querySelectorAll('.table tbody tr').length;
    if (editorialCount > 0 && !document.querySelector('.empty-state')) {
        const header = document.querySelector('.editorials-card .card-header h5');
        if (header) {
            header.innerHTML += ` <span class="badge bg-light text-dark ms-2">${editorialCount}</span>`;
        }
    }

    // Efecto de clic en las filas (opcional)
    tableRows.forEach(row => {
        if (!row.querySelector('.empty-state')) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(e) {
                // Solo si no se hizo clic en un botón de acción
                if (!e.target.closest('.action-btn')) {
                    const name = this.querySelector('.editorial-name').textContent.trim();
                    console.log('Editorial seleccionada:', name);
                }
            });
        }
    });

    // Animación para los iconos de estadísticas
    const statIcons = document.querySelectorAll('.stat-icon');
    statIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2) rotate(10deg)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });

    // Add hover effects to action buttons
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// FUNCIONALIDAD DE ELIMINACIÓN ACTUALIZADA
function confirmDelete(button) {
    const editorialId = button.getAttribute('data-editorial-id');
    const editorialName = button.getAttribute('data-editorial-name');
    
    // Actualizar el contenido del modal
    document.getElementById('editorialNameToDelete').textContent = editorialName;
    
    // Configurar el formulario de eliminación
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = deleteForm.action.replace(/\/\d+\/$/, `/${editorialId}/`);
    
    // Mostrar el modal
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// MANEJO DEL FORMULARIO DE ELIMINACIÓN
document.addEventListener('DOMContentLoaded', function() {
    const deleteForm = document.getElementById('deleteForm');
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const form = this;
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Cerrar modal
                    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
                    
                    // Mostrar mensaje de éxito
                    showAlert('success', 'Editorial eliminada correctamente');
                    
                    // Recargar la página después de un breve delay
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    showAlert('error', data.message || 'Error al eliminar la editorial');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('error', 'Error de conexión al eliminar la editorial');
            });
        });
    }
});

// FUNCIÓN PARA MOSTRAR ALERTAS
function showAlert(type, message) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
            <i class="fas ${iconClass}"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}