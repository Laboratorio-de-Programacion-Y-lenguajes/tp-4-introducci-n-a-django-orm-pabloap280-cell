from __future__ import annotations

from django.db.models import Count, Q

from .models import Autor, Libro
from catalogo import models


def libros_por_categoria(nombre_categoria: str):
    libros = Libro.objects.filter(categorias__nombre=nombre_categoria)
    return libros

def autores_con_mas_de_n_libros(n: int):
    autores = Autor.objects.annotate(cantidad_libros=Count("libro")).filter(cantidad_libros__gt=n)
    return autores

def libros_sin_disponibilidad():
    libro = Libro.objects.annotate(
        activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
    ).filter(activos=models.F("cantidad_total"))
    return libro
    

def top_n_libros_mas_prestados(n: int):
    librosPrestados = Libro.objects.annotate(total_prestamos=Count("prestamo")).order_by("-total_prestamos")[:n]
    return librosPrestados

