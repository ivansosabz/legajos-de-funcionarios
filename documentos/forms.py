from django import forms
from .models import DocumentoFuncionario, TipoDocumento


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoFuncionario
        fields = [
            "funcionario",
            "tipo_documento",
            "fecha_presentacion",
            "fecha_vencimiento",
            "archivo",
            "estado",
            "observaciones",
        ]
        widgets = {
            "funcionario": forms.Select(
                attrs={"class": "form-select bg-dark text-light border-secondary"}
            ),
            "tipo_documento": forms.Select(
                attrs={"class": "form-select bg-dark text-light border-secondary"}
            ),
            "fecha_presentacion": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control bg-dark text-light border-secondary",
                },
                format="%Y-%m-%d",
            ),
            "fecha_vencimiento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control bg-dark text-light border-secondary",
                },
                format="%Y-%m-%d",
            ),
            # FileInput simple: el “clear” lo manejamos nosotros en la plantilla + view
            "archivo": forms.FileInput(
                attrs={"class": "form-control bg-dark text-light border-secondary"}
            ),
            "estado": forms.Select(
                attrs={"class": "form-select bg-dark text-light border-secondary"}
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control bg-dark text-light border-secondary",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formatear fechas en edición
        for field_name in ["fecha_presentacion", "fecha_vencimiento"]:
            fecha = getattr(self.instance, field_name, None)
            if fecha:
                self.initial[field_name] = fecha.strftime("%Y-%m-%d")


class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = ["nombre", "descripcion", "obligatorio"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }
