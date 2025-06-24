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

    // Animación de entrada para las cards
    const cards = document.querySelectorAll('.warehouses-card, .stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });

    // Contador de bodegas
    const warehouseCount = document.querySelectorAll('.table tbody tr').length;
    if (warehouseCount > 0 && !document.querySelector('.empty-state')) {
        const header = document.querySelector('.warehouses-card .card-header h5');
        if (header) {
            header.innerHTML += ` <span class="badge bg-light text-dark ms-2">${warehouseCount}</span>`;
        }
    }

    // Efecto de clic en las filas (opcional)
    tableRows.forEach(row => {
        if (!row.querySelector('.empty-state')) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function() {
                // Aquí podrías agregar funcionalidad para ver detalles de la bodega
                const name = this.querySelector('.warehouse-name').textContent.trim();
                console.log('Bodega seleccionada:', name);
            });
        }
    });

    // Animación para los iconos de estadísticas
    const statIcons = document.querySelectorAll('.stat-icon');
    statIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2) rotate(10deg)';
            this.style.color = '#20c997';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.color = '#28a745';
        });
    });
});