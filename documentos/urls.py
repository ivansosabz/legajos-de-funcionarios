from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_documentos, name='lista_documentos'),
    path('nuevo/', views.nuevo_documento, name='nuevo_documento'),
    path('editar/<int:pk>/', views.editar_documento, name='editar_documento'),
    path('eliminar/<int:pk>/', views.eliminar_documento, name='eliminar_documento'),
    # path('tipos/', views.lista_tipos_documento, name='tipos_documento'),
]