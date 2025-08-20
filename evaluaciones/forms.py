from django import forms
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
            # Fuerza el formato correcto y el ancho completo
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
        # Asegura que al editar se vea el valor en el input date
        if self.instance and self.instance.pk and self.instance.fecha_evaluacion:
            self.fields["fecha_evaluacion"].initial = self.instance.fecha_evaluacion.strftime("%Y-%m-%d")
