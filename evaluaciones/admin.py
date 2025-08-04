from django.contrib import admin
from .models import Evaluacion

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'tipo_evaluacion', 'resultado', 'fecha')
    search_fields = ('funcionario__nombre', 'tipo_evaluacion', 'resultado')
    list_filter = ('tipo_evaluacion', 'resultado')
    date_hierarchy = 'fecha'
