from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    def delete(self, *args, **kwargs):
        # Verificar si hay productos en esta bodega
        if self.inventariobodega_set.exists():
            raise ValidationError("No se puede eliminar la bodega porque contiene productos.")
        super().delete(*args, **kwargs)

class Perfil(models.Model):
    ADMIN = 'administrador'
    JEFE_BODEGA = 'jefe_bodega'
    BODEGUERO = 'bodeguero'
    
    ROLES = [
        (ADMIN, 'Administrador'),
        (JEFE_BODEGA, 'Jefe de Bodega'),
        (BODEGUERO, 'Bodeguero'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
    def clean(self):
        # Validar que un usuario no pueda ser jefe de bodega y bodeguero al mismo tiempo
        if self.rol == self.JEFE_BODEGA:
            if Perfil.objects.filter(usuario=self.usuario, rol=self.BODEGUERO).exists():
                raise ValidationError("Un usuario no puede ser Jefe de Bodega y Bodeguero al mismo tiempo.")
        elif self.rol == self.BODEGUERO:
            if Perfil.objects.filter(usuario=self.usuario, rol=self.JEFE_BODEGA).exists():
                raise ValidationError("Un usuario no puede ser Bodeguero y Jefe de Bodega al mismo tiempo.")

class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    def delete(self, *args, **kwargs):
        # Verificar si hay productos asociados a esta editorial
        if self.producto_set.exists():
            raise ValidationError("No se puede eliminar la editorial porque tiene productos asociados.")
        super().delete(*args, **kwargs)

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def delete(self, *args, **kwargs):
        # Verificar si hay productos asociados a este autor
        if self.producto_set.exists():
            raise ValidationError("No se puede eliminar el autor porque tiene productos asociados.")
        super().delete(*args, **kwargs)

class Producto(models.Model):
    LIBRO = 'libro'
    REVISTA = 'revista'
    ENCICLOPEDIA = 'enciclopedia'
    
    TIPOS = [
        (LIBRO, 'Libro'),
        (REVISTA, 'Revista'),
        (ENCICLOPEDIA, 'Enciclopedia'),
    ]
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True, null=True)
    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT)
    autores = models.ManyToManyField(Autor)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
    
    def delete(self, *args, **kwargs):
        # Verificar si el producto está en alguna bodega
        if self.inventariobodega_set.exists():
            raise ValidationError("No se puede eliminar el producto porque está asignado a una bodega.")
        super().delete(*args, **kwargs)

class InventarioBodega(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('bodega', 'producto')
    
    def __str__(self):
        return f"{self.producto.titulo} en {self.bodega.nombre}: {self.cantidad} unidades"

class Movimiento(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    bodega_origen = models.ForeignKey(Bodega, related_name='movimientos_origen', on_delete=models.PROTECT)
    bodega_destino = models.ForeignKey(Bodega, related_name='movimientos_destino', on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Movimiento #{self.id} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.producto.titulo}: {self.cantidad} unidades"
    
class InventarioBodega(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'bodega')  # evita duplicados