document.addEventListener('DOMContentLoaded', function() {
    // Efecto de hover mejorado para las filas
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.zIndex = '10';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.zIndex = '1';
        });
    });

    // Tooltip para autores truncados
    const authorsList = document.querySelectorAll('.authors-list');
    authorsList.forEach(list => {
        if (list.scrollWidth > list.clientWidth) {
            list.style.cursor = 'help';
            list.addEventListener('mouseenter', function() {
                this.style.whiteSpace = 'normal';
                this.style.overflow = 'visible';
                this.style.position = 'relative';
                this.style.zIndex = '100';
                this.style.background = 'var(--card-bg)';
                this.style.padding = '0.5rem';
                this.style.borderRadius = '8px';
                this.style.boxShadow = '0 4px 12px var(--shadow-medium)';
            });
            
            list.addEventListener('mouseleave', function() {
                this.style.whiteSpace = 'nowrap';
                this.style.overflow = 'hidden';
                this.style.position = 'static';
                this.style.zIndex = '1';
                this.style.background = 'transparent';
                this.style.padding = '0';
                this.style.borderRadius = '0';
                this.style.boxShadow = 'none';
            });
        }
    });

    // Animación de entrada para la tabla
    const table = document.querySelector('.products-card');
    if (table) {
        table.style.opacity = '0';
        table.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            table.style.transition = 'all 0.6s ease';
            table.style.opacity = '1';
            table.style.transform = 'translateY(0)';
        }, 200);
    }

    // Contador de productos
    const productCount = document.querySelectorAll('.table tbody tr').length;
    if (productCount > 0 && !document.querySelector('.empty-state')) {
        const header = document.querySelector('.products-card .card-header h5');
        if (header) {
            header.innerHTML += ` <span class="badge bg-light text-dark ms-2">${productCount}</span>`;
        }
    }

    // Efecto de clic en las filas (opcional)
    tableRows.forEach(row => {
        if (!row.querySelector('.empty-state')) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function() {
                // Aquí podrías agregar funcionalidad para ver detalles del producto
                const title = this.querySelector('td:first-child strong').textContent;
                console.log('Producto seleccionado:', title);
            });
        }
    });
});