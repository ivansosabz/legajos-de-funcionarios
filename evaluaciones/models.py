# evaluaciones/models.py
from django.db import models
from funcionarios.models import PerfilFuncionario

class Evaluacion(models.Model):
    TIPO_PERSONAL_CHOICES = [
        ("CONTRATADO", "Contratado"),
        ("PERMANENTE", "Permanente"),
        ("COMISIONADO", "Comisionado"),
    ]
    PERIODO_CHOICES = [
        ("S1", "Primer semestre"),
        ("S2", "Segundo semestre"),
    ]

    id_funcionario = models.ForeignKey(
        PerfilFuncionario,
        on_delete=models.CASCADE,
        related_name="evaluaciones",
        verbose_name="Funcionario",
        null=True, blank=True,   # temporal hasta poblar datos
    )
    tipo_personal = models.CharField(
        max_length=20,
        choices=TIPO_PERSONAL_CHOICES,
        default="CONTRATADO",    # <- default
    )
    periodo_evaluacion = models.CharField(
        max_length=2,
        choices=PERIODO_CHOICES,
        default="S1",            # <- default
    )
    fecha_evaluacion = models.DateField()
    acta_evaluacion = models.FileField(upload_to="evaluaciones/actas/", blank=True, null=True)
