from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import DocumentoFuncionario, PerfilFuncionario, TipoDocumento
from django.db.models import Q
from .forms import DocumentoForm
from django.contrib import messages
import os
from django.conf import settings

def lista_documentos(request):
    documentos = DocumentoFuncionario.objects.select_related('funcionario', 'tipo_documento')

    # Filtros desde GET
    query = request.GET.get('q')
    estado = request.GET.get('estado')
    funcionario_id = request.GET.get('funcionario')
    tipo_documento_id = request.GET.get('tipo_documento')

    if query:
        documentos = documentos.filter(
            Q(observaciones__icontains=query) |
            Q(funcionario__nombre__icontains=query) |
            Q(tipo_documento__nombre__icontains=query)
        )

    if estado:
        documentos = documentos.filter(estado=estado)

    if funcionario_id:
        documentos = documentos.filter(funcionario_id=funcionario_id)

    if tipo_documento_id:
        documentos = documentos.filter(tipo_documento_id=tipo_documento_id)

    # Opcional: paginar si ya usás paginación
    from django.core.paginator import Paginator
    paginator = Paginator(documentos.order_by('-fecha_presentacion'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Diccionario de estados
    estados = {
        'APROBADO': 'Aprobado',
        'PENDIENTE': 'Pendiente',
        'RECHAZADO': 'Rechazado',
        'VENCIDO': 'Vencido',
    }

    return render(request, 'documentos/index.html', {
        'page_obj': page_obj,
        'funcionarios': PerfilFuncionario.objects.all(),
        'tipos_documento': TipoDocumento.objects.all(),
        'estados': estados,
    })

def nuevo_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento agregado exitosamente.')
            return redirect('lista_documentos')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = DocumentoForm()

    return render(request, 'documentos/insertar.html', {'form': form})

def editar_documento(request, pk):
    documento = get_object_or_404(DocumentoFuncionario, pk=pk)

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, "Documento actualizado exitosamente.")
            return redirect("lista_documentos")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = DocumentoForm(instance=documento)

    return render(request, "documentos/editar.html", {"form": form})

def eliminar_documento(request, pk):
    documento = get_object_or_404(DocumentoFuncionario, pk=pk)

    if request.method == "POST":
        # Eliminar archivo físico si existe
        if documento.archivo and os.path.isfile(documento.archivo.path):
            os.remove(documento.archivo.path)

        documento.delete()
        return redirect("lista_documentos")

    return render(
        request, "documentos/eliminar.html", {"documento": documento}
    )
