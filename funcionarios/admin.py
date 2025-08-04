from django.contrib import admin
from .models import PerfilFuncionario

@admin.register(PerfilFuncionario)
class PerfilFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'cargo', 'departamento', 'estado', 'fecha_ingreso')
    search_fields = ('nombre', 'apellido', 'cedula', 'departamento')
    list_filter = ('estado', 'estado_civil', 'departamento')
