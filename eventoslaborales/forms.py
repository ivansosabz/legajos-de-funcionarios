from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import EventoLaboral


class EventoLaboralForm(forms.ModelForm):
    # Campo extra del form (no está en el modelo)
    no_end_date = forms.BooleanField(
        required=False,
        label='Sin fecha de fin',
        help_text='Marcar si este evento no tiene fecha de finalización.'
    )

    class Meta:
        model = EventoLaboral
        fields = '__all__'  # incluye todos los del modelo; no_end_date se maneja aparte
        widgets = {
            'tipo_evento': forms.Select(attrs={'class': 'form-select form-control-dark', 'id': 'id_tipo_evento'}),
            'beneficio': forms.Select(attrs={'class': 'form-select form-control-dark', 'id': 'id_beneficio'}),
            'id_funcionario': forms.Select(attrs={'class': 'form-select form-control-dark'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control form-control-dark', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control form-control-dark', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control form-control-dark', 'type': 'date', 'id': 'id_fecha_fin'}),
            'url_resolucion_evento': forms.ClearableFileInput(attrs={'class': 'form-control form-control-dark'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si el evento ya guardado NO tiene fecha_fin, marcamos el checkbox por defecto
        instance = kwargs.get('instance')
        if instance and instance.fecha_fin is None:
            self.fields['no_end_date'].initial = True

        # Si nos llegan datos del POST, también respetamos ese valor
        if 'no_end_date' in self.data:
            no_end = self.data.get('no_end_date') in ('on', 'true', 'True', '1')
            if no_end:
                # visualmente desactivar el campo (el JS también lo hará)
                self.fields['fecha_fin'].widget.attrs['disabled'] = 'disabled'
        else:
            # Primer render: si initial del check está marcado, desactivar
            if self.fields['no_end_date'].initial:
                self.fields['fecha_fin'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned = super().clean()

        tipo = cleaned.get('tipo_evento')
        beneficio = cleaned.get('beneficio')
        fecha_inicio = cleaned.get('fecha_inicio')
        fecha_fin = cleaned.get('fecha_fin')
        no_end = cleaned.get('no_end_date')

        # Reglas “beneficios”
        if tipo == 'beneficios':
            if not beneficio:
                raise ValidationError({'beneficio': 'Selecciona el tipo de beneficio.'})
        else:
            # Si NO es beneficios, limpiamos beneficio para no guardar valores residuales
            cleaned['beneficio'] = None

        # Manejo de fecha fin opcional
        if no_end:
            cleaned['fecha_fin'] = None
        else:
            # Si no es "sin fecha fin", entonces debe venir fecha_fin y debe ser >= fecha_inicio
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                raise ValidationError({'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'})

        return cleaned
