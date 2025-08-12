from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('insertar/', views.insertar_evento, name='insertar_evento'),
    path('editar/<int:id_evento>/', views.editar_evento, name='editar_evento'),
    path('eliminar/<int:id_evento>/', views.eliminar_evento, name='eliminar_evento'),
]
