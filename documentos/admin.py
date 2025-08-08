from django.contrib import admin
from .models import TipoDocumento, DocumentoFuncionario

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'obligatorio')
    search_fields = ('nombre',)
    list_filter = ('obligatorio',)

@admin.register(DocumentoFuncionario)
class DocumentoFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'tipo_documento', 'fecha_presentacion', 'estado')
    search_fields = ('funcionario__nombre', 'tipo_documento__nombre')
    list_filter = ('tipo_documento', 'estado')
    date_hierarchy = 'fecha_presentacion'

