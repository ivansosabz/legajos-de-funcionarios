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

    # ⬇️ Campos de fecha explícitos, con formato ISO para HTML5 y múltiples input_formats
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control bg-dark text-light border-secondary w-100',
                'id': 'id_fecha_inicio',
                'style': 'width:100%',
            }
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        required=True,
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control bg-dark text-light border-secondary w-100',
                'id': 'id_fecha_fin',
                'style': 'width:100%',
            }
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        required=False,
    )

    class Meta:
        model = EventoLaboral
        fields = '__all__'
        widgets = {
            'tipo_evento': forms.Select(attrs={'class': 'form-select form-control-dark', 'id': 'id_tipo_evento'}),
            'beneficio': forms.Select(attrs={'class': 'form-select form-control-dark', 'id': 'id_beneficio'}),
            'id_funcionario': forms.Select(attrs={'class': 'form-select form-control-dark'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control form-control-dark', 'rows': 3}),
            # ⚠️ OJO: quita aquí cualquier 'fecha_inicio' / 'fecha_fin' para no pisar lo de arriba
            'url_resolucion_evento': forms.ClearableFileInput(attrs={'class': 'form-control form-control-dark'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance and instance.fecha_fin is None:
            self.fields['no_end_date'].initial = True

        # si viene marcado, deshabilitar visualmente fecha_fin
        if 'no_end_date' in self.data:
            no_end = self.data.get('no_end_date') in ('on', 'true', 'True', '1')
            if no_end:
                self.fields['fecha_fin'].widget.attrs['disabled'] = 'disabled'
        else:
            if self.fields['no_end_date'].initial:
                self.fields['fecha_fin'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo_evento')
        beneficio = cleaned.get('beneficio')
        fecha_inicio = cleaned.get('fecha_inicio')
        fecha_fin = cleaned.get('fecha_fin')
        no_end = cleaned.get('no_end_date')

        if tipo == 'beneficios':
            if not beneficio:
                raise ValidationError({'beneficio': 'Selecciona el tipo de beneficio.'})
        else:
            cleaned['beneficio'] = None

        if no_end:
            cleaned['fecha_fin'] = None
        else:
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                raise ValidationError({'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'})

        return cleaned
