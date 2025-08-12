from django.contrib import admin
from .models import EventoLaboral

@admin.register(EventoLaboral)
class EventoLaboralAdmin(admin.ModelAdmin):
    list_display = ('id_funcionario', 'tipo_evento', 'fecha_inicio', 'fecha_fin')
    search_fields = ('funcionario__nombre', 'tipo_evento')
    list_filter = ('tipo_evento',)
    date_hierarchy = 'fecha_inicio'
