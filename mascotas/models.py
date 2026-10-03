from django.db import models
from django.utils import timezone


class Mascota(models.Model):
    ESPECIES_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Conejo', 'Conejo'),
        ('Ave', 'Ave'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    especie = models.CharField(max_length=20, choices=ESPECIES_CHOICES, verbose_name='Especie')
    raza = models.CharField(max_length=80, verbose_name='Raza')
    edad = models.PositiveIntegerField(verbose_name='Edad (años)')
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso (kg)')
    propietario = models.CharField(max_length=150, verbose_name='Dueño')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    correo = models.EmailField(max_length=150, verbose_name='Correo electrónico')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.nombre} ({self.especie})'
