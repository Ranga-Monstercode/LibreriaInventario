from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.db.models import OuterRef, Exists
import json


from .models import (
    Perfil, Editorial, Autor, Producto, Bodega, 
    InventarioBodega, Movimiento, DetalleMovimiento
)

from .forms import (
    UsuarioForm,ProductoForm,MovimientoForm,BodegaForm,AutorForm,EditorialForm,
    InformeMovimientosForm,InformeProductosForm,EditarUsuarioForm,CambiarPasswordForm,InventarioBodegaForm,DetalleMovimientoFormSet
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

    InventarioFormSet = modelformset_factory(
    InventarioBodega,
    form=InventarioBodegaForm,
    extra=1,
    can_delete=True,
    fields=['bodega', 'cantidad'],  # este es obligatorio
)


    if request.method == 'POST':
        form = ProductoForm(request.POST)
        formset = InventarioFormSet(request.POST, queryset=InventarioBodega.objects.none())

        if form.is_valid() and formset.is_valid():
            producto = form.save()

            for inventario_form in formset:
                if inventario_form.cleaned_data and not inventario_form.cleaned_data.get('DELETE', False):
                    inventario = inventario_form.save(commit=False)
                    inventario.producto = producto
                    inventario.save()

            messages.success(request, 'Producto creado y stock asignado exitosamente')
            return redirect('listar_productos')

    else:
        form = ProductoForm()
        formset = InventarioFormSet(queryset=InventarioBodega.objects.none())

    return render(request, 'inventario/productos/crear_producto.html', {
        'form': form,
        'formset': formset,
    })

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
    print("Ingreso a la vista crear_movimiento")
    
    if not es_bodeguero(request.user):
        print(f"Usuario {request.user} no tiene permisos de bodeguero")
        messages.error(request, 'No tiene permisos para crear movimientos')
        return redirect('dashboard')
    
    if request.method == 'POST':
        print("Método POST recibido")
        form_movimiento = MovimientoForm(request.POST)
        formset_detalles = DetalleMovimientoFormSet(request.POST, prefix='detalles')
        
        print(f"form_movimiento es válido? {form_movimiento.is_valid()}")
        print(f"formset_detalles es válido? {formset_detalles.is_valid()}")
        
        if form_movimiento.is_valid() and formset_detalles.is_valid():
            print("Ambos formularios válidos, comenzando transacción atómica")
            with transaction.atomic():
                movimiento = form_movimiento.save(commit=False)
                movimiento.usuario = request.user
                movimiento.save()
                print(f"Movimiento creado con ID: {movimiento.id}")
                
                for idx, form_detalle in enumerate(formset_detalles):
                    print(f"Procesando detalle {idx + 1}")
                    if form_detalle.cleaned_data and not form_detalle.cleaned_data.get('DELETE', False):
                        producto = form_detalle.cleaned_data['producto']
                        cantidad = form_detalle.cleaned_data['cantidad']
                        print(f"Producto: {producto.titulo}, Cantidad: {cantidad}")
                        
                        try:
                            inventario_origen = InventarioBodega.objects.get(
                                bodega=movimiento.bodega_origen,
                                producto=producto
                            )
                            print(f"Stock en bodega origen: {inventario_origen.cantidad}")
                            
                            if inventario_origen.cantidad < cantidad:
                                print("Error: stock insuficiente")
                                raise forms.ValidationError(
                                    f"No hay suficiente stock de {producto.titulo} en la bodega de origen."
                                )
                            
                            inventario_origen.cantidad -= cantidad
                            inventario_origen.save()
                            print(f"Stock actualizado en bodega origen: {inventario_origen.cantidad}")
                            
                            if inventario_origen.cantidad == 0:
                                inventario_origen.delete()
                                print("Inventario eliminado por cantidad cero")
                            
                        except InventarioBodega.DoesNotExist:
                            print("Error: producto no existe en la bodega origen")
                            raise forms.ValidationError(
                                f"El producto {producto.titulo} no existe en la bodega de origen."
                            )
                        
                        inventario_destino, created = InventarioBodega.objects.get_or_create(
                            bodega=movimiento.bodega_destino,
                            producto=producto,
                            defaults={'cantidad': 0}
                        )
                        print(f"Stock actual en bodega destino antes de suma: {inventario_destino.cantidad}")
                        inventario_destino.cantidad += cantidad
                        inventario_destino.save()
                        print(f"Stock actualizado en bodega destino: {inventario_destino.cantidad}")
                        
                        DetalleMovimiento.objects.create(
                            movimiento=movimiento,
                            producto=producto,
                            cantidad=cantidad
                        )
                        print("DetalleMovimiento creado")
                
                messages.success(request, 'Movimiento creado exitosamente')
                return redirect('detalle_movimiento', movimiento_id=movimiento.id)
        else:
            print("Errores en formulario movimiento o detalles:")
            print(form_movimiento.errors)
            print(formset_detalles.errors)
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        print("Método GET, mostrando formularios vacíos")
        form_movimiento = MovimientoForm()
        formset_detalles = DetalleMovimientoFormSet(prefix='detalles')
    
    bodegas = Bodega.objects.all()
    productos_por_bodega = {}

    for bodega in bodegas:
        inventario = InventarioBodega.objects.filter(bodega=bodega)
        productos_por_bodega[bodega.id] = [
            {
                'id': item.producto.id,
                'nombre': item.producto.titulo,
                'cantidad': item.cantidad
            }
            for item in inventario
        ]
    
    # Productos sin ninguna bodega asignada (sin stock)
    productos_sin_bodega = Producto.objects.annotate(
        tiene_stock=Exists(InventarioBodega.objects.filter(producto=OuterRef('pk')))
    ).filter(tiene_stock=False)

    productos_por_bodega['sin_bodega'] = [
        {'id': p.id, 'nombre': p.titulo, 'cantidad': 0}
        for p in productos_sin_bodega
    ]

    print("Renderizando plantilla con context")

    return render(request, 'inventario/movimientos/crear_movimiento.html', {
        'form_movimiento': form_movimiento,
        'formset_detalles': formset_detalles,
        'productos_por_bodega': json.dumps(productos_por_bodega),  # serializado a JSON para JS
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

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)

    context = {
        'form': form,
        'producto': producto
    }
    return render(request, 'inventario/productos/editar_producto.html', context)

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto_titulo = producto.titulo
        producto.delete()
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Producto "{producto_titulo}" eliminado correctamente.'
            })
        else:
            # Si es una petición normal, redirigir con mensaje
            messages.success(request, 'Producto eliminado correctamente.')
            return redirect('listar_productos')

    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})

@login_required
def editar_editorial(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    
    if request.method == 'POST':
        form = EditorialForm(request.POST, instance=editorial)
        if form.is_valid():
            try:
                editorial_actualizada = form.save()
                messages.success(
                    request, 
                    f'La editorial "{editorial_actualizada.nombre}" ha sido actualizada correctamente.'
                )
                return redirect('listar_editoriales')
            except Exception as e:
                messages.error(
                    request, 
                    f'Error al actualizar la editorial: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Por favor, corrija los errores en el formulario.'
            )
    else:
        form = EditorialForm(instance=editorial)
    
    context = {
        'form': form,
        'editorial': editorial,
        'titulo': f'Editar Editorial: {editorial.nombre}',
        'accion': 'Actualizar'
    }
    
    return render(request, 'inventario/editoriales/editar_editorial.html', context)

@login_required
@require_http_methods(["POST"])
def eliminar_editorial(request, pk):

    editorial = get_object_or_404(Editorial, pk=pk)
    editorial_nombre = editorial.nombre
    
    try:
        # Verificar si la editorial tiene productos asociados
        productos_asociados = editorial.producto_set.count()
        
        if productos_asociados > 0:
            mensaje_error = f'No se puede eliminar la editorial "{editorial_nombre}" porque tiene {productos_asociados} producto(s) asociado(s).'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': mensaje_error
                })
            else:
                messages.error(request, mensaje_error)
                return redirect('listar_editoriales')
        
        # Eliminar la editorial
        editorial.delete()
        
        mensaje_exito = f'La editorial "{editorial_nombre}" ha sido eliminada correctamente.'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': mensaje_exito
            })
        else:
            messages.success(request, mensaje_exito)
            return redirect('listar_editoriales')
            
    except Exception as e:
        mensaje_error = f'Error al eliminar la editorial: {str(e)}'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': mensaje_error
            })
        else:
            messages.error(request, mensaje_error)
            return redirect('listar_editoriales')
        

@login_required
def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            try:
                autor_actualizado = form.save()
                messages.success(
                    request, 
                    f'El autor "{autor_actualizado.nombre} {autor_actualizado.apellido}" ha sido actualizado correctamente.'
                )
                return redirect('listar_autores')
            except Exception as e:
                messages.error(
                    request, 
                    f'Error al actualizar el autor: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Por favor, corrija los errores en el formulario.'
            )
    else:
        form = AutorForm(instance=autor)
    
    context = {
        'form': form,
        'autor': autor,
        'titulo': f'Editar Autor: {autor.nombre} {autor.apellido}',
        'accion': 'Actualizar'
    }
    
    return render(request, 'inventario/autores/editar_autor.html', context)

@login_required
@require_http_methods(["POST"])
def eliminar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    autor_nombre = f"{autor.nombre} {autor.apellido}"
    
    try:
        # Verificar si el autor tiene productos asociados
        productos_asociados = autor.producto_set.count()
        
        if productos_asociados > 0:
            mensaje_error = f'No se puede eliminar el autor "{autor_nombre}" porque tiene {productos_asociados} producto(s) asociado(s).'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': mensaje_error
                })
            else:
                messages.error(request, mensaje_error)
                return redirect('listar_autores')
        
        # Eliminar el autor
        autor.delete()
        
        mensaje_exito = f'El autor "{autor_nombre}" ha sido eliminado correctamente.'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': mensaje_exito
            })
        else:
            messages.success(request, mensaje_exito)
            return redirect('listar_autores')
            
    except Exception as e:
        mensaje_error = f'Error al eliminar el autor: {str(e)}'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': mensaje_error
            })
        else:
            messages.error(request, mensaje_error)
            return redirect('listar_autores')
        

@login_required
def editar_bodega(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    
    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            try:
                bodega_actualizada = form.save()
                messages.success(
                    request, 
                    f'La bodega "{bodega_actualizada.nombre}" ha sido actualizada correctamente.'
                )
                return redirect('listar_bodegas')
            except Exception as e:
                messages.error(
                    request, 
                    f'Error al actualizar la bodega: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Por favor, corrija los errores en el formulario.'
            )
    else:
        form = BodegaForm(instance=bodega)
    
    context = {
        'form': form,
        'bodega': bodega,
        'titulo': f'Editar Bodega: {bodega.nombre}',
        'accion': 'Actualizar'
    }
    
    return render(request, 'inventario/bodegas/editar_bodega.html', context)

@login_required
def eliminar_bodega(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    
    if request.method == 'POST':
        bodega_nombre = bodega.nombre
        
        try:
            # Verificar si la bodega tiene productos asociados
            productos_asociados = bodega.producto_set.count()
            
            if productos_asociados > 0:
                mensaje_error = f'No se puede eliminar la bodega "{bodega_nombre}" porque tiene {productos_asociados} producto(s) almacenado(s).'
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': mensaje_error
                    })
                else:
                    messages.error(request, mensaje_error)
                    return redirect('listar_bodegas')
            
            # Eliminar la bodega
            bodega.delete()
            
            mensaje_exito = f'La bodega "{bodega_nombre}" ha sido eliminada correctamente.'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': mensaje_exito
                })
            else:
                messages.success(request, mensaje_exito)
                return redirect('listar_bodegas')
                
        except Exception as e:
            mensaje_error = f'Error al eliminar la bodega: {str(e)}'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': mensaje_error
                })
            else:
                messages.error(request, mensaje_error)
                return redirect('listar_bodegas')
    
    # Si es GET, mostrar página de confirmación
    return render(request, 'inventario/bodegas/confirmar_eliminar.html', {'bodega': bodega})

@login_required
def editar_usuario(request, pk):

    perfil = get_object_or_404(Perfil, pk=pk)
    usuario = perfil.usuario
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario, perfil=perfil)
        
        if form.is_valid():
            try:
                usuario_actualizado = form.save()
                
                messages.success(
                    request, 
                    f'El usuario "{usuario_actualizado.username}" ha sido actualizado correctamente.'
                )
                return redirect('listar_usuarios')
            except Exception as e:
                messages.error(
                    request, 
                    f'Error al actualizar el usuario: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Por favor, corrija los errores en el formulario.'
            )
    else:
        form = EditarUsuarioForm(instance=usuario, perfil=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
        'usuario': usuario,
        'titulo': f'Editar Usuario: {usuario.username}',
        'accion': 'Actualizar'
    }
    
    return render(request, 'inventario/usuarios/editar_usuario.html', context)

@login_required
def cambiar_password_usuario(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    usuario = perfil.usuario
    
    if request.method == 'POST':
        form = CambiarPasswordForm(request.POST)
        
        if form.is_valid():
            try:
                nueva_password = form.cleaned_data['password1']
                
                # Establecer la contraseña SIN validaciones de Django
                usuario.set_password(nueva_password)
                usuario.save()
                
                # Si es el usuario actual, actualizar la sesión
                if usuario == request.user:
                    update_session_auth_hash(request, usuario)
                    messages.success(
                        request, 
                        'Tu contraseña ha sido cambiada correctamente y tu sesión se mantiene activa.'
                    )
                else:
                    messages.success(
                        request, 
                        f'La contraseña del usuario "{usuario.username}" ha sido cambiada correctamente.'
                    )
                
                return redirect('listar_usuarios')
                
            except Exception as e:
                messages.error(
                    request, 
                    f'Error al cambiar la contraseña: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Por favor, corrija los errores en el formulario.'
            )
    else:
        form = CambiarPasswordForm()
    
    context = {
        'form': form,
        'perfil': perfil,
        'usuario': usuario,
        'titulo': f'Cambiar Contraseña: {usuario.username}',
        'es_propio_usuario': usuario == request.user
    }
    
    return render(request, 'inventario/usuarios/cambiar_password.html', context)

@login_required
def eliminar_usuario(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    usuario = perfil.usuario
    
    # Evitar que el usuario se elimine a sí mismo
    if usuario == request.user:
        mensaje_error = 'No puedes eliminar tu propia cuenta.'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': mensaje_error
            })
        else:
            messages.error(request, mensaje_error)
            return redirect('listar_usuarios')
    
    if request.method == 'POST':
        usuario_username = usuario.username
        
        try:
            # Verificar si es el último administrador
            if perfil.rol == 'administrador':
                admin_count = Perfil.objects.filter(rol='administrador').count()
                if admin_count <= 1:
                    mensaje_error = 'No se puede eliminar el último administrador del sistema.'
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': mensaje_error
                        })
                    else:
                        messages.error(request, mensaje_error)
                        return redirect('listar_usuarios')
            
            # Eliminar el usuario (esto también eliminará el perfil por CASCADE)
            usuario.delete()
            
            mensaje_exito = f'El usuario "{usuario_username}" ha sido eliminado correctamente.'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': mensaje_exito
                })
            else:
                messages.success(request, mensaje_exito)
                return redirect('listar_usuarios')
                
        except Exception as e:
            mensaje_error = f'Error al eliminar el usuario: {str(e)}'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': mensaje_error
                })
            else:
                messages.error(request, mensaje_error)
                return redirect('listar_usuarios')
    
    # Si es GET, redirigir a la lista
    return redirect('listar_usuarios')