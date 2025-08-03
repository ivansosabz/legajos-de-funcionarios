from django.db import models

class PerfilFuncionario(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    cedula = models.CharField(max_length=45, unique=True)
    cargo = models.CharField(max_length=80)
    fecha_ingreso = models.DateField()
    departamento = models.CharField(max_length=100)
    estado = models.CharField(max_length=45)
    estado_civil = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# Create your models here.
