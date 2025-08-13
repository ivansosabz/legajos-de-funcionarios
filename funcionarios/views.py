from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import PerfilFuncionario
from .forms import FuncionarioForm


# def lista_funcionarios(request):
#     funcionarios = PerfilFuncionario.objects.all()

#     # Parámetros de búsqueda y filtro
#     query = request.GET.get('q')
#     estado = request.GET.get('estado')
#     departamento = request.GET.get('departamento')
#     cargo = request.GET.get('cargo')
#     vista = request.GET.get('vista', 'tarjetas')

#     # Filtro de búsqueda general
#     if query:
#         funcionarios = funcionarios.filter(
#             Q(nombre__icontains=query) |
#             Q(apellido__icontains=query) |
#             Q(cedula__icontains=query) |
#             Q(cargo__icontains=query) |
#             Q(departamento__icontains=query)
#         )

#     # Filtros adicionales
#     if estado:
#         funcionarios = funcionarios.filter(estado=estado)

#     if departamento:
#         funcionarios = funcionarios.filter(departamento=departamento)

#     if cargo:
#         funcionarios = funcionarios.filter(cargo=cargo)

#     # Listas únicas para los filtros
#     departamentos = PerfilFuncionario.objects.values_list('departamento', flat=True).distinct()
#     cargos = PerfilFuncionario.objects.values_list('cargo', flat=True).distinct()

#     context = {
#         'funcionarios': funcionarios,
#         'vista': vista,
#         'estado': estado,
#         'departamento': departamento,
#         'cargo': cargo,
#         'departamentos': departamentos,
#         'cargos': cargos,
#         'query': query,
#     }

#     return render(request, 'funcionarios/index.html', {
#         'funcionarios': funcionarios,
#         'vista': vista,  # importante para que el template sepa qué mostrar
#         'filtros': {
#             'estado': estado,
#             'departamento': departamento,
#             'cargo': cargo,
#         }
#     })

def lista_funcionarios(request):
    funcionarios = PerfilFuncionario.objects.all().order_by("nombre")

    # Parámetros de búsqueda y filtro
    query = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    departamento = request.GET.get("departamento", "").strip()
    cargo = request.GET.get("cargo", "").strip()
    vista = request.GET.get("vista", "tarjetas")

    # Filtro de búsqueda general (case-insensitive)
    if query:
        funcionarios = funcionarios.filter(
            Q(nombre__icontains=query)
            | Q(apellido__icontains=query)
            | Q(cedula__icontains=query)
            | Q(cargo__icontains=query)
            | Q(departamento__icontains=query)
        )

    # Filtros adicionales (case-insensitive)
    if estado:
        funcionarios = funcionarios.filter(estado__iexact=estado)

    if departamento:
        funcionarios = funcionarios.filter(departamento__iexact=departamento)

    if cargo:
        funcionarios = funcionarios.filter(cargo__iexact=cargo)

    # Listas únicas para los filtros (ordenadas)
    departamentos = (
        PerfilFuncionario.objects.order_by("departamento")
        .values_list("departamento", flat=True)
        .distinct()
    )
    cargos = (
        PerfilFuncionario.objects.order_by("cargo")
        .values_list("cargo", flat=True)
        .distinct()
    )
    estados = (
        PerfilFuncionario.objects.order_by("estado")
        .values_list("estado", flat=True)
        .distinct()
    )

    context = {
        "funcionarios": funcionarios,
        "vista": vista,
        "query": query,
        "estado": estado,
        "departamento": departamento,
        "cargo": cargo,
        "departamentos": departamentos,
        "cargos": cargos,
        "estados": estados,
    }

    return render(request, "funcionarios/index.html", context)


def insertar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionario registrado correctamente.')
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/insertar.html', {'form': form})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(PerfilFuncionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionario modificado correctamente.')
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'funcionarios/editar.html', {'form': form, 'funcionario': funcionario})


def eliminar_funcionario(request, id):
    funcionario = get_object_or_404(PerfilFuncionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionario eliminado correctamente.')
        messages.success(request, 'Funcionario eliminado correctamente.')
        return redirect('lista_funcionarios')

    return render(request, 'funcionarios/eliminar.html', {'funcionario': funcionario})
