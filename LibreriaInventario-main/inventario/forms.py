from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, Editorial, Autor, Producto, Bodega, Movimiento, DetalleMovimiento,InventarioBodega
from django.forms import formset_factory, BaseFormSet

class UsuarioForm(UserCreationForm):
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('jefe_bodega', 'Jefe de Bodega'),
        ('bodeguero', 'Bodeguero'),
    ]
    
    rol = forms.ChoiceField(
        choices=ROL_CHOICES, 
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        }),
        label='Rol del Usuario',
        help_text='Seleccione el rol que tendrá el usuario en el sistema'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña'
            })
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña'
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Solo letras, números y @/./+/-/_ permitidos.',
            'first_name': 'Nombre real del usuario (opcional)',
            'last_name': 'Apellido del usuario (opcional)',
            'email': 'Dirección de correo electrónico del usuario',
            'password1': 'Su contraseña debe tener al menos 8 caracteres',
            'password2': 'Ingrese la misma contraseña para verificación'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de ayuda para las contraseñas
        #self.fields['password1'].help_text = 'Su contraseña debe tener al menos 8 caracteres y no puede ser muy común.'
        self.fields['password2'].help_text = 'Ingrese la misma contraseña para verificación.'
        
        # Hacer email obligatorio
        #self.fields['email'].required = True
        
        # Agregar clases CSS a los campos de contraseña
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip().lower()
            
            # Verificar que no exista otro usuario con el mismo username
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError(
                    f'Ya existe un usuario con el nombre "{username}".'
                )
            
            if len(username) < 3:
                raise forms.ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
            
            return username
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            
            # Verificar que no exista otro usuario con el mismo email
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError(
                    f'Ya existe un usuario con el email "{email}".'
                )
            
            return email
        return email
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Perfil.objects.create(usuario=user, rol=self.cleaned_data['rol'])
        return user
    
class EditarUsuarioForm(forms.ModelForm):
    """Formulario específico para editar usuarios existentes"""
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('jefe_bodega', 'Jefe de Bodega'),
        ('bodeguero', 'Bodeguero'),
    ]
    
    rol = forms.ChoiceField(
        choices=ROL_CHOICES, 
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        }),
        label='Rol del Usuario',
        help_text='Seleccione el rol que tendrá el usuario en el sistema'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'required': True
            })
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico'
        }
        help_texts = {
            'username': 'Nombre único para identificar al usuario en el sistema',
            'first_name': 'Nombre real del usuario',
            'last_name': 'Apellido del usuario',
            'email': 'Dirección de correo electrónico del usuario'
        }
    
    def __init__(self, *args, **kwargs):
        # Extraer el perfil si se pasa como argumento
        self.perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)
        
        # Hacer email obligatorio
        self.fields['email'].required = True
        
        # Si tenemos un perfil, establecer el rol inicial
        if self.perfil:
            self.fields['rol'].initial = self.perfil.rol
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip().lower()
            
            # Verificar que no exista otro usuario con el mismo username
            queryset = User.objects.filter(username__iexact=username)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(
                    f'Ya existe un usuario con el nombre "{username}".'
                )
            
            if len(username) < 3:
                raise forms.ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
            
            return username
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            
            # Verificar que no exista otro usuario con el mismo email
            queryset = User.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(
                    f'Ya existe un usuario con el email "{email}".'
                )
            
            return email
        return email
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and self.perfil:
            # Actualizar el rol del perfil
            self.perfil.rol = self.cleaned_data['rol']
            self.perfil.save()
        return user

class CambiarPasswordForm(forms.Form):
    """Formulario para cambiar contraseña de usuario SIN RESTRICCIONES"""
    password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        }),
        help_text='Ingrese la nueva contraseña (sin restricciones).',
        required=True
    )
    password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        }),
        help_text='Ingrese la misma contraseña para verificación.',
        required=True
    )
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Sin validaciones - acepta cualquier contraseña
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return password2
    
    def clean(self):
        cleaned_data = super().clean()
        # Sin validaciones adicionales
        return cleaned_data

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'biografia']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del autor',
                'required': True
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del autor',
                'required': True
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Biografía del autor (opcional)',
                'rows': 5,
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'biografia': 'Biografía'
        }
        help_texts = {
            'nombre': 'Ingrese el nombre del autor',
            'apellido': 'Ingrese el apellido del autor',
            'biografia': 'Información biográfica del autor (opcional)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos nombre y apellido obligatorios
        self.fields['nombre'].required = True
        self.fields['apellido'].required = True

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            if len(nombre) < 2:
                raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
            return nombre
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            apellido = apellido.strip().title()
            if len(apellido) < 2:
                raise forms.ValidationError('El apellido debe tener al menos 2 caracteres.')
            return apellido
        return apellido

    def clean_biografia(self):
        biografia = self.cleaned_data.get('biografia')
        if biografia:
            biografia = biografia.strip()
            if len(biografia) > 1000:
                raise forms.ValidationError(
                    'La biografía no puede exceder los 1000 caracteres.'
                )
        return biografia

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')
        
        if nombre and apellido:
            # Verificar que no exista otro autor con el mismo nombre y apellido
            queryset = Autor.objects.filter(
                nombre__iexact=nombre,
                apellido__iexact=apellido
            )
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(
                    f'Ya existe un autor con el nombre "{nombre} {apellido}".'
                )
        
        return cleaned_data

class ProductoForm(forms.ModelForm):
    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Producto
        # quitamos 'bodega' y 'cantidad' porque ya no están en Producto o no deben estar para manejar stock separado
        fields = ['titulo', 'tipo', 'descripcion', 'editorial', 'autores']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        autores = cleaned_data.get('autores')
        nuevo_autor_nombre = cleaned_data.get('nuevo_autor_nombre')
        nuevo_autor_apellido = cleaned_data.get('nuevo_autor_apellido')
        
        if not autores and not (nuevo_autor_nombre and nuevo_autor_apellido):
            raise forms.ValidationError("Debe seleccionar al menos un autor existente o crear uno nuevo.")
        
        return cleaned_data
    
    def save(self, commit=True):
        producto = super().save(commit=commit)
        
        if commit:
            nuevo_autor_nombre = self.cleaned_data.get('nuevo_autor_nombre')
            nuevo_autor_apellido = self.cleaned_data.get('nuevo_autor_apellido')
            
            if nuevo_autor_nombre and nuevo_autor_apellido:
                nuevo_autor, created = Autor.objects.get_or_create(
                    nombre=nuevo_autor_nombre,
                    apellido=nuevo_autor_apellido
                )
                producto.autores.add(nuevo_autor)
        
        return producto
    
class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'ubicacion', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la bodega',
                'required': True
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación de la bodega',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la bodega (opcional)',
                'rows': 4,
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'nombre': 'Nombre de la Bodega',
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción'
        }
        help_texts = {
            'nombre': 'Ingrese el nombre identificativo de la bodega',
            'ubicacion': 'Dirección o ubicación física de la bodega',
            'descripcion': 'Descripción opcional sobre la bodega'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos nombre y ubicación obligatorios
        self.fields['nombre'].required = True
        self.fields['ubicacion'].required = True

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            
            # Verificar que no exista otra bodega con el mismo nombre
            queryset = Bodega.objects.filter(nombre__iexact=nombre)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(
                    f'Ya existe una bodega con el nombre "{nombre}".'
                )
            
            if len(nombre) < 2:
                raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
            
            return nombre
        return nombre

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if ubicacion:
            ubicacion = ubicacion.strip()
            if len(ubicacion) < 5:
                raise forms.ValidationError('La ubicación debe tener al menos 5 caracteres.')
            return ubicacion
        return ubicacion

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            descripcion = descripcion.strip()
            if len(descripcion) > 500:
                raise forms.ValidationError(
                    'La descripción no puede exceder los 500 caracteres.'
                )
        return descripcion

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['bodega_origen', 'bodega_destino']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bodega_origen'].queryset = Bodega.objects.all()
        self.fields['bodega_destino'].queryset = Bodega.objects.all()
    
    def clean(self):
        cleaned_data = super().clean()
        bodega_origen = cleaned_data.get('bodega_origen')
        bodega_destino = cleaned_data.get('bodega_destino')
        
        if bodega_origen == bodega_destino:
            raise forms.ValidationError("La bodega de origen y destino no pueden ser la misma.")
        
        return cleaned_data

class DetalleMovimientoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label="Producto")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")

class BaseDetalleMovimientoFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        productos = []
        for form in self.forms:
            if form.cleaned_data:
                producto = form.cleaned_data.get('producto')
                cantidad = form.cleaned_data.get('cantidad')
                
                if producto in productos:
                    raise forms.ValidationError(
                        "No puede incluir el mismo producto más de una vez en el movimiento."
                    )
                
                if cantidad <= 0:
                    raise forms.ValidationError(
                        "La cantidad debe ser mayor que cero."
                    )
                
                productos.append(producto)
        
        if not productos:
            raise forms.ValidationError(
                "Debe incluir al menos un producto en el movimiento."
            )

DetalleMovimientoFormSet = formset_factory(
    DetalleMovimientoForm,
    formset=BaseDetalleMovimientoFormSet,
    extra=1,
    can_delete=True
)

class InformeProductosForm(forms.Form):
    OPCIONES_INFORME = [
        ('todos', 'Todos los productos por bodega'),
        ('tipo', 'Productos por tipo'),
        ('editorial', 'Productos por editorial')
    ]
    
    tipo_informe = forms.ChoiceField(choices=OPCIONES_INFORME, required=True)
    bodega = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=False)
    editorial = forms.ModelChoiceField(queryset=Editorial.objects.all(), required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_informe = cleaned_data.get('tipo_informe')
        bodega = cleaned_data.get('bodega')
        editorial = cleaned_data.get('editorial')
        
        if tipo_informe == 'editorial' and not editorial:
            raise forms.ValidationError("Debe seleccionar una editorial para este tipo de informe.")
        
        return cleaned_data

class InformeMovimientosForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    bodega_origen = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=False)
    bodega_destino = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=False)

class InventarioBodegaForm(forms.ModelForm):
    class Meta:
        model = InventarioBodega
        fields = ['producto','bodega']

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la editorial',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la editorial (opcional)',
                'rows': 4,
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'nombre': 'Nombre de la Editorial',
            'descripcion': 'Descripción'
        }
        help_texts = {
            'nombre': 'Ingrese el nombre oficial de la editorial',
            'descripcion': 'Descripción opcional sobre la editorial'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo nombre obligatorio
        self.fields['nombre'].required = True
        
        # Agregar clases CSS adicionales
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' form-control'
            })

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            
            # Verificar que no exista otra editorial con el mismo nombre
            # (excluyendo la instancia actual si estamos editando)
            queryset = Editorial.objects.filter(nombre__iexact=nombre)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(
                    f'Ya existe una editorial con el nombre "{nombre}".'
                )
            
            return nombre
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            descripcion = descripcion.strip()
            if len(descripcion) > 500:
                raise forms.ValidationError(
                    'La descripción no puede exceder los 500 caracteres.'
                )
        return descripcion