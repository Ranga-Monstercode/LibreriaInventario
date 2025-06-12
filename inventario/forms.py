from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, Editorial, Autor, Producto, Bodega, Movimiento, DetalleMovimiento,InventarioBodega

class UsuarioForm(UserCreationForm):
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('jefe_bodega', 'Jefe de Bodega'),
        ('bodeguero', 'Bodeguero'),
    ]
    
    rol = forms.ChoiceField(choices=ROL_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Perfil.objects.create(usuario=user, rol=self.cleaned_data['rol'])
        return user

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
            'biografia': forms.Textarea(attrs={'rows': 3}),
        }

class ProductoForm(forms.ModelForm):
    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.all(),
        required=False,
        label='Bodega',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    nuevo_autor_nombre = forms.CharField(required=False, label="Nombre del nuevo autor")
    nuevo_autor_apellido = forms.CharField(required=False, label="Apellido del nuevo autor")
    
    class Meta:
        model = Producto
        fields = ['titulo', 'tipo', 'descripcion', 'editorial', 'autores','bodega','cantidad']
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
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

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

class DetalleMovimientoFormSet(forms.BaseFormSet):
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

DetalleMovimientoFormSet = forms.formset_factory(
    forms.Form,
    formset=DetalleMovimientoFormSet,
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

class InventarioBodega(forms.ModelForm):
    class Meta:
        model = InventarioBodega
        fields = ['producto','bodega']