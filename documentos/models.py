from django.db import models
from django.core.validators import FileExtensionValidator
from funcionarios.models import PerfilFuncionario

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    obligatorio = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class DocumentoFuncionario(models.Model):
    ESTADO_OPCIONES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('VENCIDO', 'Vencido'),
    ]

    funcionario = models.ForeignKey(
        PerfilFuncionario,
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name='documentos'
    )
    fecha_presentacion = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    archivo = models.FileField(
        upload_to='documentos/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])
        ],
        null=True,
        blank=True
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_OPCIONES,
        default='PENDIENTE'
    )
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documento de Funcionario"
        verbose_name_plural = "Documentos de Funcionarios"
        ordering = ['-fecha_presentacion']
        unique_together = ['funcionario', 'tipo_documento']

    def __str__(self):
        return f"{self.funcionario} - {self.tipo_documento}"

    @property
    def esta_vencido(self):
        if self.fecha_vencimiento:
            from django.utils import timezone
            return timezone.now().date() > self.fecha_vencimiento
        return False