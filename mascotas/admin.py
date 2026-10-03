from django.contrib import admin

from .models import Mascota


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'propietario', 'telefono', 'fecha_creacion')
    search_fields = ('nombre', 'propietario', 'telefono')
    list_filter = ('especie',)
