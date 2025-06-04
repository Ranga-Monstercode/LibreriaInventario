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
    Perfil
)

from .forms import (
    UsuarioForm
)




# Create your views here.
def inicio(request):
    return render(request, 'inventario/login.html')


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
    # Si es superusuario, redirigir al panel de administración
    if request.user.is_superuser:
        return render(request, 'inventario/dashboard_admin.html')
    
    try:
        if es_administrador(request.user):
            return render(request, 'inventario/dashboard_admin.html')
        elif es_jefe_bodega(request.user):
            return render(request, 'inventario/dashboard_jefe.html')
        elif es_bodeguero(request.user):
            return render(request, 'inventario/dashboard_bodeguero.html')
        else:
            messages.error(request, 'No tiene un rol asignado en el sistema')
            return redirect('logout')
    except Perfil.DoesNotExist:
        messages.error(request, 'No tiene un perfil asignado en el sistema')
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