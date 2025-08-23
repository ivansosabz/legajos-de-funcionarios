# eventoslaborales/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import EventoLaboral
from .forms import EventoLaboralForm
from funcionarios.models import PerfilFuncionario

from django.contrib.auth.decorators import login_required

@login_required(login_url="login")  # redirige a la página de login si no está autenticado

# Listar + filtros/búsqueda
def lista_eventos(request):
    q = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo_evento", "").strip()
    funcionario_id = request.GET.get("funcionario", "").strip()  # name del <select>

    eventos = (
        EventoLaboral.objects
        .select_related("id_funcionario")
        .order_by("-fecha_inicio")
    )

    if q:
        eventos = eventos.filter(
            Q(id_funcionario__nombre__icontains=q) |
            Q(id_funcionario__apellido__icontains=q) |
            Q(motivo__icontains=q)
        )

    if tipo:
        eventos = eventos.filter(tipo_evento=tipo)

    # filtrar por funcionario (FK llamada id_funcionario)
    if funcionario_id:
        eventos = eventos.filter(id_funcionario_id=funcionario_id)

    tipos_evento = [{"value": v, "label": l} for v, l in EventoLaboral.TIPO_EVENTO_CHOICES]

    return render(
        request,
        "eventoslaborales/index.html",
        {
            "eventos": eventos,
            "q": q,
            "tipo_evento": tipo,
            "tipos_evento": tipos_evento,
            "funcionarios": PerfilFuncionario.objects.all().order_by("apellido", "nombre"),
        },
    )


# Crear
def insertar_evento(request):
    if request.method == "POST":
        form = EventoLaboralForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento laboral registrado correctamente.")
            return redirect("lista_eventos")
    else:
        form = EventoLaboralForm()
    return render(request, "eventoslaborales/insertar.html", {"form": form})


# Editar
def editar_evento(request, id_evento):
    evento = get_object_or_404(EventoLaboral, pk=id_evento)

    if request.method == 'POST':
        form = EventoLaboralForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            if request.POST.get('url_resolucion_evento-clear'):
                if evento.url_resolucion_evento:
                    evento.url_resolucion_evento.delete(save=False)
                evento.url_resolucion_evento = None

            form.save()
            messages.success(request, 'Evento laboral modificado correctamente.')
            return redirect('lista_eventos')
    else:
        form = EventoLaboralForm(instance=evento)

    return render(request, 'eventoslaborales/editar.html', {'form': form, 'evento': evento})


# Eliminar
def eliminar_evento(request, id_evento):
    evento = get_object_or_404(EventoLaboral, pk=id_evento)

    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento laboral eliminado correctamente.')
        return redirect('lista_eventos')

    return render(request, 'eventoslaborales/eliminar.html', {'evento': evento})
