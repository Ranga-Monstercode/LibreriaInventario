from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.forms import formset_factory
from django.db.models import Sum, Count, Q
from .models import *

from .models import (
    Perfil, Editorial, Autor, Producto, Bodega, 
    InventarioBodega, Movimiento, DetalleMovimiento
)

from .forms import (
    UsuarioForm,ProductoForm,MovimientoForm,BodegaForm,AutorForm,EditorialForm,InformeMovimientosForm,InformeProductosForm
)

#Para verificar roles de usuario
def es_administrador(user):
    # Los superusuarios siempre son considerados administradores
    if user.is_superuser:
        return True
    
    try:
        return user.perfil.rol == Perfil.ADMIN
    except Perfil.DoesNotExist:
        return False

def es_jefe_bodega(user):
    try:
        return user.perfil.rol == Perfil.JEFE_BODEGA
    except Perfil.DoesNotExist:
        return False

def es_bodeguero(user):
    try:
        return user.perfil.rol == Perfil.BODEGUERO
    except Perfil.DoesNotExist:
        return False
    
# Vistas de autenticación
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'inventario/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if es_administrador(request.user):
        return render(request, 'inventario/dashboard_admin.html')
    elif es_jefe_bodega(request.user):
        return render(request, 'inventario/dashboard_jefe.html')
    elif es_bodeguero(request.user):
        return render(request, 'inventario/dashboard_bodeguero.html')
    else:
        messages.error(request, 'No tiene un rol asignado en el sistema')
        return redirect('logout')

@login_required
def dashboard(request):
    if es_administrador(request.user):
        return render(request, 'inventario/dashboard_admin.html')
    elif es_jefe_bodega(request.user):
        return render(request, 'inventario/dashboard_jefe.html')
    elif es_bodeguero(request.user):
        return render(request, 'inventario/dashboard_bodeguero.html')
    else:
        messages.error(request, 'No tiene un rol asignado en el sistema')
        return redirect('logout')

@login_required
def crear_usuario(request):
    if not es_administrador(request.user):
        messages.error(request, 'No tiene permisos para crear usuarios')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'inventario/usuarios/crear_usuario.html', {'form': form})

@login_required
def listar_usuarios(request):
    if not es_administrador(request.user):
        messages.error(request, 'No tiene permisos para ver usuarios')
        return redirect('dashboard')
    
    usuarios = Perfil.objects.all()
    return render(request, 'inventario/usuarios/listar_usuarios.html', {'usuarios': usuarios})



# Vistas de editoriales
@login_required
def crear_editorial(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para crear editoriales')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editorial creada exitosamente')
            return redirect('listar_editoriales')
    else:
        form = EditorialForm()
    
    return render(request, 'inventario/editoriales/crear_editorial.html', {'form': form})

@login_required
def listar_editoriales(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para ver editoriales')
        return redirect('dashboard')
    
    editoriales = Editorial.objects.all()
    return render(request, 'inventario/editoriales/listar_editoriales.html', {'editoriales': editoriales})

# Vistas de autores
@login_required
def crear_autor(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para crear autores')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor creado exitosamente')
            return redirect('listar_autores')
    else:
        form = AutorForm()
    
    return render(request, 'inventario/autores/crear_autor.html', {'form': form})

@login_required
def listar_autores(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para ver autores')
        return redirect('dashboard')
    
    autores = Autor.objects.all()
    return render(request, 'inventario/autores/listar_autores.html', {'autores': autores})

# Vistas de productos
@login_required
def crear_producto(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para crear productos')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            bodega = form.cleaned_data['bodega']
            messages.success(request, 'Producto creado exitosamente')
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/productos/crear_producto.html', {'form': form})

@login_required
def listar_productos(request):
    if not es_jefe_bodega(request.user) and not es_bodeguero(request.user):
        messages.error(request, 'No tiene permisos para ver productos')
        return redirect('dashboard')
    
    productos = Producto.objects.all()
    return render(request, 'inventario/productos/listar_productos.html', {'productos': productos})

# Vistas de bodegas
@login_required
def crear_bodega(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para crear bodegas')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega creada exitosamente')
            return redirect('listar_bodegas')
    else:
        form = BodegaForm()
    
    return render(request, 'inventario/bodegas/crear_bodega.html', {'form': form})

@login_required
def listar_bodegas(request):
    if not es_jefe_bodega(request.user) and not es_bodeguero(request.user):
        messages.error(request, 'No tiene permisos para ver bodegas')
        return redirect('dashboard')
    
    bodegas = Bodega.objects.all()
    return render(request, 'inventario/bodegas/listar_bodegas.html', {'bodegas': bodegas})

# Vistas de movimientos
@login_required
def crear_movimiento(request):
    if not es_bodeguero(request.user):
        messages.error(request, 'No tiene permisos para crear movimientos')
        return redirect('dashboard')
    
    DetalleFormSet = formset_factory(MovimientoForm, extra=1)
    
    if request.method == 'POST':
        form_movimiento = MovimientoForm(request.POST)
        formset_detalles = DetalleFormSet(request.POST, prefix='detalles')
        
        if form_movimiento.is_valid() and formset_detalles.is_valid():
            with transaction.atomic():
                # Crear el movimiento
                movimiento = form_movimiento.save(commit=False)
                movimiento.usuario = request.user
                movimiento.save()
                
                # Procesar cada detalle
                for form_detalle in formset_detalles:
                    if form_detalle.cleaned_data:
                        producto_id = form_detalle.cleaned_data.get('producto')
                        cantidad = form_detalle.cleaned_data.get('cantidad')
                        
                        if producto_id and cantidad:
                            producto = Producto.objects.get(id=producto_id)
                            
                            # Verificar stock en bodega origen
                            try:
                                inventario_origen = InventarioBodega.objects.get(
                                    bodega=movimiento.bodega_origen,
                                    producto=producto
                                )
                                
                                if inventario_origen.cantidad < cantidad:
                                    raise ValidationError(f"No hay suficiente stock de {producto.titulo} en la bodega de origen.")
                                
                                # Restar de bodega origen
                                inventario_origen.cantidad -= cantidad
                                inventario_origen.save()
                                
                                # Si la cantidad llega a 0, eliminar el registro
                                if inventario_origen.cantidad == 0:
                                    inventario_origen.delete()
                                
                            except InventarioBodega.DoesNotExist:
                                raise ValidationError(f"El producto {producto.titulo} no existe en la bodega de origen.")
                            
                            # Agregar a bodega destino
                            inventario_destino, created = InventarioBodega.objects.get_or_create(
                                bodega=movimiento.bodega_destino,
                                producto=producto,
                                defaults={'cantidad': 0}
                            )
                            
                            inventario_destino.cantidad += cantidad
                            inventario_destino.save()
                            
                            # Crear detalle de movimiento
                            DetalleMovimiento.objects.create(
                                movimiento=movimiento,
                                producto=producto,
                                cantidad=cantidad
                            )
                
                messages.success(request, 'Movimiento creado exitosamente')
                return redirect('detalle_movimiento', movimiento_id=movimiento.id)
    else:
        form_movimiento = MovimientoForm()
        formset_detalles = DetalleFormSet(prefix='detalles')
    
    # Obtener productos disponibles por bodega
    bodegas = Bodega.objects.all()
    productos_por_bodega = {}
    
    for bodega in bodegas:
        inventario = InventarioBodega.objects.filter(bodega=bodega)
        productos_por_bodega[bodega.id] = [
            {
                'id': item.producto.id,
                'nombre': item.producto.titulo,
                'cantidad': item.producto.cantidad
            }
            for item in inventario
        ]
    
    return render(request, 'inventario/movimientos/crear_movimiento.html', {
        'form_movimiento': form_movimiento,
        'formset_detalles': formset_detalles,
        'productos_por_bodega': productos_por_bodega
    })

@login_required
def listar_movimientos(request):
    if not es_jefe_bodega(request.user) and not es_bodeguero(request.user):
        messages.error(request, 'No tiene permisos para ver movimientos')
        return redirect('dashboard')
    
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'inventario/movimientos/listar_movimientos.html', {'movimientos': movimientos})

@login_required
def detalle_movimiento(request, movimiento_id):
    if not es_jefe_bodega(request.user) and not es_bodeguero(request.user):
        messages.error(request, 'No tiene permisos para ver detalles de movimientos')
        return redirect('dashboard')
    
    movimiento = get_object_or_404(Movimiento, id=movimiento_id)
    detalles = DetalleMovimiento.objects.filter(movimiento=movimiento)
    
    return render(request, 'inventario/movimientos/detalle_movimiento.html', {
        'movimiento': movimiento,
        'detalles': detalles
    })

# Vistas de informes
@login_required
def informe_productos(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para ver informes')
        return redirect('dashboard')
    
    resultados = None
    
    if request.method == 'POST':
        form = InformeProductosForm(request.POST)
        if form.is_valid():
            tipo_informe = form.cleaned_data['tipo_informe']
            bodega = form.cleaned_data.get('bodega')
            editorial = form.cleaned_data.get('editorial')
            
            if tipo_informe == 'todos':
                # Cantidad de productos por bodega
                if bodega:
                    resultados = InventarioBodega.objects.filter(bodega=bodega)
                else:
                    resultados = InventarioBodega.objects.all()
            
            elif tipo_informe == 'tipo':
                # Productos por tipo
                query = Q()
                if bodega:
                    inventario_ids = InventarioBodega.objects.filter(bodega=bodega).values_list('producto_id', flat=True)
                    query &= Q(id__in=inventario_ids)
                
                resultados = {
                    'Libros': Producto.objects.filter(query & Q(tipo=Producto.LIBRO)).count(),
                    'Revistas': Producto.objects.filter(query & Q(tipo=Producto.REVISTA)).count(),
                    'Enciclopedias': Producto.objects.filter(query & Q(tipo=Producto.ENCICLOPEDIA)).count()
                }
            
            elif tipo_informe == 'editorial':
                # Productos por editorial específica
                query = Q(editorial=editorial)
                if bodega:
                    inventario_ids = InventarioBodega.objects.filter(bodega=bodega).values_list('producto_id', flat=True)
                    query &= Q(id__in=inventario_ids)
                
                resultados = Producto.objects.filter(query)
    else:
        form = InformeProductosForm()
    
    return render(request, 'inventario/informes/informe_productos.html', {
        'form': form,
        'resultados': resultados
    })

@login_required
def informe_movimientos(request):
    if not es_jefe_bodega(request.user):
        messages.error(request, 'No tiene permisos para ver informes')
        return redirect('dashboard')
    
    resultados = None
    
    if request.method == 'POST':
        form = InformeMovimientosForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')
            bodega_origen = form.cleaned_data.get('bodega_origen')
            bodega_destino = form.cleaned_data.get('bodega_destino')
            
            query = Q()
            
            if fecha_inicio:
                query &= Q(fecha__gte=fecha_inicio)
            if fecha_fin:
                query &= Q(fecha__lte=fecha_fin)
            if bodega_origen:
                query &= Q(bodega_origen=bodega_origen)
            if bodega_destino:
                query &= Q(bodega_destino=bodega_destino)
            
            resultados = Movimiento.objects.filter(query).order_by('-fecha')
    else:
        form = InformeMovimientosForm()
    
    return render(request, 'inventario/informes/informe_movimientos.html', {
        'form': form,
        'resultados': resultados
    })