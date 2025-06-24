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

    // Manejo de biografías truncadas
    const biographies = document.querySelectorAll('.author-biography');
    biographies.forEach(bio => {
        const fullText = bio.getAttribute('title');
        const truncatedText = bio.textContent;
        
        bio.addEventListener('mouseenter', function() {
            if (fullText && fullText !== truncatedText) {
                this.textContent = fullText;
                this.classList.remove('truncated');
            }
        });
        
        bio.addEventListener('mouseleave', function() {
            if (fullText && fullText !== truncatedText) {
                this.textContent = truncatedText;
                this.classList.add('truncated');
            }
        });
    });

    // Animación de entrada para las cards
    const cards = document.querySelectorAll('.authors-card, .stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });

    // Contador de autores
    const authorCount = document.querySelectorAll('.table tbody tr').length;
    if (authorCount > 0 && !document.querySelector('.empty-state')) {
        const header = document.querySelector('.authors-card .card-header h5');
        if (header) {
            header.innerHTML += ` <span class="badge bg-light text-dark ms-2">${authorCount}</span>`;
        }
    }

    // Efecto de clic en las filas (opcional)
    tableRows.forEach(row => {
        if (!row.querySelector('.empty-state')) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function() {
                // Aquí podrías agregar funcionalidad para ver detalles del autor
                const name = this.querySelector('.author-name').textContent.trim();
                const lastname = this.querySelector('.author-lastname').textContent.trim();
                console.log('Autor seleccionado:', name, lastname);
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