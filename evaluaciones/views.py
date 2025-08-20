from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Evaluacion
from .forms import EvaluacionForm
from funcionarios.models import PerfilFuncionario


def lista_evaluaciones(request):
    q = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo_personal", "").strip()
    periodo = request.GET.get("periodo", "").strip()
    func_id = request.GET.get("funcionario", "").strip()

    evaluaciones = Evaluacion.objects.select_related("id_funcionario")

    if q:
        evaluaciones = evaluaciones.filter(
            Q(id_funcionario__nombre__icontains=q) |
            Q(id_funcionario__apellido__icontains=q)
        )
    if tipo:
        evaluaciones = evaluaciones.filter(tipo_personal=tipo)
    if periodo:
        evaluaciones = evaluaciones.filter(periodo_evaluacion=periodo)
    if func_id:
        evaluaciones = evaluaciones.filter(id_funcionario_id=func_id)

    return render(request, "evaluaciones/index.html", {
        "evaluaciones": evaluaciones,
        "q": q,
        "tipo": tipo,
        "periodo": periodo,
        "funcionarios": PerfilFuncionario.objects.all().order_by("apellido", "nombre"),
        "TIPO_PERSONAL_CHOICES": Evaluacion.TIPO_PERSONAL_CHOICES,
        "PERIODO_CHOICES": Evaluacion.PERIODO_CHOICES,
    })


def nueva_evaluacion(request):
    if request.method == "POST":
        form = EvaluacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Evaluación registrada correctamente.")
            return redirect("lista_evaluaciones")
    else:
        form = EvaluacionForm()
    return render(request, "evaluaciones/insertar.html", {"form": form})


def editar_evaluacion(request, pk):
    eva = get_object_or_404(Evaluacion, pk=pk)
    if request.method == "POST":
        form = EvaluacionForm(request.POST, request.FILES, instance=eva)

        # Soporte “eliminar archivo actual”
        if request.POST.get("acta_evaluacion-clear"):
            if eva.acta_evaluacion:
                eva.acta_evaluacion.delete(save=False)
            eva.acta_evaluacion = None

        if form.is_valid():
            form.save()
            messages.success(request, "Evaluación actualizada correctamente.")
            return redirect("lista_evaluaciones")
    else:
        form = EvaluacionForm(instance=eva)
    return render(request, "evaluaciones/editar.html", {"form": form, "evaluacion": eva})


def eliminar_evaluacion(request, pk):
    eva = get_object_or_404(Evaluacion, pk=pk)
    if request.method == "POST":
        eva.delete()
        messages.success(request, "Evaluación eliminada correctamente.")
        return redirect("lista_evaluaciones")
    return render(request, "evaluaciones/eliminar.html", {"evaluacion": eva})
