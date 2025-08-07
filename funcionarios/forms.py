from django import forms
from .models import PerfilFuncionario
from datetime import date
import re

DEPARTAMENTOS = [
    ('RRHH', 'RRHH'),
    ('Tic', 'Tic'),
    ('Academico', 'Académico'),
    ('Finanzas', 'Finanzas')
]

CARGOS = [
    ('Secretario/a', 'Secretario/a'),
    ('Auxiliar contable', 'Auxiliar contable'),
    ('Ingeniero/a', 'Ingeniero/a'),
    ('Tecnico Informatico/a', 'Técnico Informático/a')
]

ESTADOS = [
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo')
]

ESTADOS_CIVILES = [
    ('Soltero/a', 'Soltero/a'),
    ('Casado/a', 'Casado/a'),
    ('Divorciado/a', 'Divorciado/a'),
    ('Viudo/a', 'Viudo/a')
]


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = PerfilFuncionario
        fields = ['nombre', 'apellido', 'cedula', 'cargo', 'fecha_ingreso', 'departamento', 'estado', 'estado_civil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Apellido'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Cédula'}),
            'cargo': forms.Select(choices=CARGOS, attrs={'class': 'form-select form-control-dark'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control form-control-dark', 'type': 'date'}),
            'departamento': forms.Select(choices=DEPARTAMENTOS, attrs={'class': 'form-select form-control-dark'}),
            'estado': forms.Select(choices=ESTADOS, attrs={'class': 'form-select form-control-dark'}),
            'estado_civil': forms.Select(choices=ESTADOS_CIVILES, attrs={'class': 'form-select form-control-dark'})
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if any(char.isdigit() for char in apellido):
            raise forms.ValidationError("El apellido no puede contener números.")
        return apellido

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
        return cedula

    def clean_fecha_ingreso(self):
        fecha = self.cleaned_data.get('fecha_ingreso')
        if fecha > date.today():
            raise forms.ValidationError("La fecha de ingreso no puede ser futura.")
        return fecha
