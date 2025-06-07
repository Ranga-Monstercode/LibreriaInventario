from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Usuarios
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    
    # Editoriales
    path('editoriales/crear/', views.crear_editorial, name='crear_editorial'),
    path('editoriales/', views.listar_editoriales, name='listar_editoriales'),
    
    # Autores
    path('autores/crear/', views.crear_autor, name='crear_autor'),
    path('autores/', views.listar_autores, name='listar_autores'),
    
    # Productos
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/', views.listar_productos, name='listar_productos'),
    
    # Bodegas
    path('bodegas/crear/', views.crear_bodega, name='crear_bodega'),
    path('bodegas/', views.listar_bodegas, name='listar_bodegas'),
    
    # Movimientos
    path('movimientos/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('movimientos/', views.listar_movimientos, name='listar_movimientos'),
    path('movimientos/<int:movimiento_id>/', views.detalle_movimiento, name='detalle_movimiento'),
    
    # Informes
    path('informes/productos/', views.informe_productos, name='informe_productos'),
    path('informes/movimientos/', views.informe_movimientos, name='informe_movimientos'),
    
    # Ruta principal
    path('', views.login_view, name='index'),
]
