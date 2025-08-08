from django import forms
from .models import DocumentoFuncionario, TipoDocumento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoFuncionario
        fields = ['funcionario', 'tipo_documento', 'fecha_presentacion',
                 'fecha_vencimiento', 'archivo', 'estado', 'observaciones']
        widgets = {
            'fecha_presentacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = ['nombre', 'descripcion', 'obligatorio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }