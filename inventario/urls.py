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
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/cambiar-password/<int:pk>/', views.cambiar_password_usuario, name='cambiar_password_usuario'),
    
    # Editoriales
    path('editoriales/crear/', views.crear_editorial, name='crear_editorial'),
    path('editoriales/', views.listar_editoriales, name='listar_editoriales'),
    path('editoriales/editar/<int:pk>/', views.editar_editorial, name='editar_editorial'),
    path('editoriales/eliminar/<int:pk>/', views.eliminar_editorial, name='eliminar_editorial'),
    
    # Autores
    path('autores/crear/', views.crear_autor, name='crear_autor'),
    path('autores/', views.listar_autores, name='listar_autores'),
    path('autores/editar/<int:pk>/', views.editar_autor, name='editar_autor'),
    path('autores/eliminar/<int:pk>/', views.eliminar_autor, name='eliminar_autor'),
    
    # Productos
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    
    # Bodegas
    path('bodegas/crear/', views.crear_bodega, name='crear_bodega'),
    path('bodegas/', views.listar_bodegas, name='listar_bodegas'),
    path('bodegas/editar/<int:pk>/', views.editar_bodega, name='editar_bodega'),
    path('bodegas/eliminar/<int:pk>/', views.eliminar_bodega, name='eliminar_bodega'),
    
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
