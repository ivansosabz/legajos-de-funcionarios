from django import forms
from .models import DocumentoFuncionario, TipoDocumento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoFuncionario
        fields = [
            'funcionario', 'tipo_documento', 'fecha_presentacion',
            'fecha_vencimiento', 'archivo', 'estado', 'observaciones'
        ]
        widgets = {
            'funcionario': forms.Select(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'fecha_presentacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'estado': forms.Select(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control bg-dark text-white border-secondary'}),
        }

class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = ['nombre', 'descripcion', 'obligatorio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }