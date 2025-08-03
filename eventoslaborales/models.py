from django.db import models
from django.core.validators import FileExtensionValidator
from funcionarios.models import PerfilFuncionario

class EventoLaboral(models.Model):
    funcionario = models.ForeignKey(PerfilFuncionario, on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=100)
    motivo = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    resolucion = models.FileField(
        upload_to='media/eventos/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.tipo_evento} - {self.funcionario}"
