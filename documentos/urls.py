from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_documentos, name="lista_documentos"),
    path("nuevo/", views.nuevo_documento, name="nuevo_documento"),
    path("editar/<int:pk>/", views.editar_documento, name="editar_documento"),
    path("eliminar/<int:pk>/", views.eliminar_documento, name="eliminar_documento"),
    # CRUD Tipos de Documento
    path("tipos/", views.lista_tipos_documento, name="lista_tipos_documento"),
    path("tipos/nuevo/", views.nuevo_tipo_documento, name="nuevo_tipo_documento"),
    path("tipos/editar/<int:pk>/", views.editar_tipo_documento, name="editar_tipo_documento"),
    path("tipos/eliminar/<int:pk>/", views.eliminar_tipo_documento, name="eliminar_tipo_documento"),
]