from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_evaluaciones, name="lista_evaluaciones"),
    path("nuevo/", views.nueva_evaluacion, name="nueva_evaluacion"),
    path("editar/<int:pk>/", views.editar_evaluacion, name="editar_evaluacion"),
    path("eliminar/<int:pk>/", views.eliminar_evaluacion, name="eliminar_evaluacion"),
]
