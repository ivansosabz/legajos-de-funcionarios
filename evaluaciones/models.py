from django.db import models
from funcionarios.models import PerfilFuncionario

class Evaluacion(models.Model):
    funcionario = models.ForeignKey(PerfilFuncionario, on_delete=models.CASCADE)
    tipo_evaluacion = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.tipo_evaluacion} - {self.funcionario}"
