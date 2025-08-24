# evaluaciones/forms.py
from django import forms
from datetime import date
from .models import Evaluacion

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = "__all__"
        widgets = {
            "id_funcionario": forms.Select(attrs={
                "class": "form-select bg-dark text-light border-secondary"
            }),
            "tipo_personal": forms.Select(attrs={
                "class": "form-select bg-dark text-light border-secondary"
            }),
            "periodo_evaluacion": forms.Select(attrs={
                "class": "form-select bg-dark text-light border-secondary"
            }),
            "fecha_evaluacion": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control bg-dark text-light border-secondary w-100",
                },
            ),
            "acta_evaluacion": forms.ClearableFileInput(attrs={
                "class": "form-control bg-dark text-light border-secondary"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar bien la fecha al editar
        if self.instance and self.instance.pk and self.instance.fecha_evaluacion:
            self.fields["fecha_evaluacion"].initial = self.instance.fecha_evaluacion.strftime("%Y-%m-%d")
        # Bloquear fechas futuras en el datepicker (cliente)
        self.fields["fecha_evaluacion"].widget.attrs["max"] = date.today().strftime("%Y-%m-%d")

    def clean_fecha_evaluacion(self):
        fecha = self.cleaned_data.get("fecha_evaluacion")
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de evaluación no puede ser futura.")
        return fecha
