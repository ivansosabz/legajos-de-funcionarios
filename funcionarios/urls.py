from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_funcionarios, name='lista_funcionarios'),
    path('nuevo/', views.insertar_funcionario, name='insertar_funcionario'),
    path('<int:id>/editar/', views.editar_funcionario, name='editar_funcionario'),
    path('<int:id>/eliminar/', views.eliminar_funcionario, name='eliminar_funcionario'),
]
