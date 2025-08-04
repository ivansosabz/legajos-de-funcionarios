from django import forms
from .models import PerfilFuncionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = PerfilFuncionario
        fields = ['nombre', 'apellido', 'cedula', 'cargo', 'fecha_ingreso', 'departamento', 'estado', 'estado_civil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Apellido'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Cédula'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Cargo'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control form-control-dark', 'type': 'date'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Departamento'}),
            'estado': forms.Select(attrs={'class': 'form-select form-control-dark'}, choices=[
                ('Activo', 'Activo'),
                ('Inactivo', 'Inactivo')
            ]),
            'estado_civil': forms.Select(attrs={'class': 'form-select form-control-dark'}, choices=[
                ('Soltero/a', 'Soltero/a'),
                ('Casado/a', 'Casado/a'),
                ('Divorciado/a', 'Divorciado/a'),
                ('Viudo/a', 'Viudo/a')
            ])
        }
