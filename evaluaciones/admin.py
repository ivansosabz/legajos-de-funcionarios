from django.contrib import admin
from django.utils.html import format_html
from .models import Evaluacion


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "id_funcionario",
        "tipo_personal",
        "periodo_evaluacion",
        "fecha_evaluacion",
        "acta_link",
    )
    list_filter = ("tipo_personal", "periodo_evaluacion", "fecha_evaluacion")
    search_fields = ("id_funcionario__nombre", "id_funcionario__apellido")
    date_hierarchy = "fecha_evaluacion"
    ordering = ("-fecha_evaluacion",)

    def acta_link(self, obj):
        if obj.acta_evaluacion:
            return format_html('<a href="{}" target="_blank">Ver</a>', obj.acta_evaluacion.url)
        return "—"
    acta_link.short_description = "Acta"
