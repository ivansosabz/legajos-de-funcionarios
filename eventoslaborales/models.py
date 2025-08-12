from django.db import models
from django.core.validators import FileExtensionValidator
from funcionarios.models import PerfilFuncionario

class EventoLaboral(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('vacaciones', 'Vacaciones'),
        ('sanciones', 'Sanciones'),
        ('traslados', 'Traslados'),
        ('permisos', 'Permisos'),
        ('beneficios', 'Beneficios'),
    ]

    BENEFICIOS_CHOICES = [
        ('bonos', 'Bonos'),
        ('subsidios', 'Subsidios'),
        ('becas', 'Becas'),
    ]

    id_funcionario = models.ForeignKey(PerfilFuncionario, on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=100, choices=TIPO_EVENTO_CHOICES)
    beneficio = models.CharField(max_length=50, choices=BENEFICIOS_CHOICES, blank=True, null=True)
    motivo = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  # <— ahora opcional
    url_resolucion_evento = models.FileField(
        upload_to='resoluciones/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.tipo_evento} - {self.id_funcionario}"

    # --- NUEVO: borrar archivo viejo al reemplazar y al eliminar ---
    def save(self, *args, **kwargs):
        old_file = None
        if self.pk:
            try:
                old_file = EventoLaboral.objects.get(pk=self.pk).url_resolucion_evento
            except EventoLaboral.DoesNotExist:
                old_file = None

        super().save(*args, **kwargs)

        # si cambió el archivo, borramos el anterior del storage
        if old_file and old_file.name and old_file != self.url_resolucion_evento:
            old_file.delete(save=False)

    def delete(self, *args, **kwargs):
        if self.url_resolucion_evento:
            self.url_resolucion_evento.delete(save=False)
        super().delete(*args, **kwargs)
