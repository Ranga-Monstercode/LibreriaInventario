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
});

function confirmDelete(nombre) {
    if (confirm(`¿Estás seguro de que deseas eliminar la editorial "${nombre}"?`)) {
        // Add delete functionality here
        alert('Funcionalidad de eliminación pendiente de implementar');
    }
}

// Add hover effects to action buttons
document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px) scale(1.05)';
    });
    
    btn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});