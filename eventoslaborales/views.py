# eventoslaborales/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import EventoLaboral
from .forms import EventoLaboralForm
from django.contrib import messages
from django.db.models import Q



# Vista para insertar un nuevo evento laboral
def insertar_evento(request):
    if request.method == 'POST':
        form = EventoLaboralForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento laboral registrado correctamente.')
            return redirect('lista_eventos')
    else:
        form = EventoLaboralForm()
    return render(request, 'eventoslaborales/insertar.html', {'form': form})


def lista_eventos(request):
    # Parámetros GET
    q = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo_evento", "").strip()

    # Base queryset
    eventos = (
        EventoLaboral.objects
        .select_related("id_funcionario")
        .order_by("-fecha_inicio")
    )

    # Búsqueda por nombre/apellido de funcionario
    if q:
        eventos = eventos.filter(
            Q(id_funcionario__nombre__icontains=q) |
            Q(id_funcionario__apellido__icontains=q)
        )

    # Filtro por tipo de evento
    if tipo:
        eventos = eventos.filter(tipo_evento=tipo)

    # Para poblar el <select> desde las choices del modelo
    tipos_evento = [{"value": v, "label": l} for v, l in EventoLaboral.TIPO_EVENTO_CHOICES]

    return render(
        request,
        "eventoslaborales/index.html",
        {
            "eventos": eventos,
            "q": q,
            "tipo_evento": tipo,
            "tipos_evento": tipos_evento,
        },
    )


def editar_evento(request, id_evento):
    evento = get_object_or_404(EventoLaboral, pk=id_evento)

    if request.method == 'POST':
        form = EventoLaboralForm(request.POST, request.FILES, instance=evento)

        if form.is_valid():
            # Si el usuario marcó "Clear" en el archivo, bórralo
            if request.POST.get('url_resolucion_evento-clear'):
                if evento.url_resolucion_evento:
                    evento.url_resolucion_evento.delete(save=False)
                evento.url_resolucion_evento = None

            form.save()  # El save del modelo ya limpia el anterior si se reemplaza
            messages.success(request, 'Evento laboral modificado correctamente.')
            return redirect('lista_eventos')
    else:
        form = EventoLaboralForm(instance=evento)

    return render(request, 'eventoslaborales/editar.html', {'form': form, 'evento': evento})


def eliminar_evento(request, id_evento):
    evento = get_object_or_404(EventoLaboral, pk=id_evento)

    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento laboral eliminado correctamente.')
        return redirect('lista_eventos')

    return render(request, 'eventoslaborales/eliminar.html', {'evento': evento})
# Create your views here.
