from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(unique=True) 
    biografia = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    fecha_publicacion = models.DateField()
    cantidad_total = models.PositiveIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)
   

    def prestamos_activos(self) -> int:
        return self.prestamo_set.filter(fecha_devolucion__isnull=True).count()

    def disponibles(self) -> int:
        return self.cantidad_total - self.prestamos_activos()

    def tiene_disponibles(self) -> bool:
        return self.disponibles() > 0


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_prestatario = models.CharField(max_length=120)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)

