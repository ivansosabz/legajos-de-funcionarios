from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FuncionarioForm
from .models import PerfilFuncionario
from django.contrib import messages

def lista_funcionarios(request):
    query = request.GET.get('q')
    funcionarios = PerfilFuncionario.objects.all()

    if query:
        funcionarios = funcionarios.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(cedula__icontains=query) |
            Q(cargo__icontains=query) |
            Q(departamento__icontains=query)
        )

    return render(request, 'funcionarios/index.html', {'funcionarios': funcionarios})

def insertar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_funcionarios')  # redirige a la lista después de guardar
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/insertar.html', {'form': form})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(PerfilFuncionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'funcionarios/editar.html', {'form': form, 'funcionario': funcionario})


def eliminar_funcionario(request, id):
    funcionario = get_object_or_404(PerfilFuncionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionario eliminado correctamente.')
        return redirect('lista_funcionarios')

    return render(request, 'funcionarios/eliminar.html', {'funcionario': funcionario})