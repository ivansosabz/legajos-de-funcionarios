from django.db import models
from django.core.validators import FileExtensionValidator
from funcionarios.models import PerfilFuncionario

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    obligatorio = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class DocumentoFuncionario(models.Model):
    funcionario = models.ForeignKey(PerfilFuncionario, on_delete=models.CASCADE)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    fecha_presentacion = models.DateField()
    archivo = models.FileField(
        upload_to='media/documentos/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'png', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    estado = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.funcionario} - {self.tipo_documento}"
