from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import DocumentoFuncionario, PerfilFuncionario, TipoDocumento
from django.db.models import Q, ProtectedError
from .forms import DocumentoForm, TipoDocumentoForm
from django.contrib import messages
import os
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def lista_documentos(request):
    documentos = DocumentoFuncionario.objects.select_related("funcionario", "tipo_documento")

    query = request.GET.get("q")
    estado = request.GET.get("estado")
    funcionario_id = request.GET.get("funcionario")
    tipo_documento_id = request.GET.get("tipo_documento")
    vencido = request.GET.get("vencido")

    if query:
        documentos = documentos.filter(
            Q(observaciones__icontains=query)
            | Q(funcionario__nombre__icontains=query)
            | Q(tipo_documento__nombre__icontains=query)
        )
    if estado:
        documentos = documentos.filter(estado=estado)
    if funcionario_id:
        documentos = documentos.filter(funcionario_id=funcionario_id)
    if tipo_documento_id:
        documentos = documentos.filter(tipo_documento_id=tipo_documento_id)

    if vencido == "1":
        documentos = documentos.filter(fecha_vencimiento__lt=timezone.now().date())
    elif vencido == "0":
        documentos = documentos.filter(
            Q(fecha_vencimiento__gte=timezone.now().date())
            | Q(fecha_vencimiento__isnull=True)
        )

    from django.core.paginator import Paginator
    paginator = Paginator(documentos.order_by("-fecha_presentacion"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    estados = {
        "APROBADO": "Aprobado",
        "PENDIENTE": "Pendiente",
        "RECHAZADO": "Rechazado",
    }

    return render(
        request,
        "documentos/index.html",
        {
            "page_obj": page_obj,
            "funcionarios": PerfilFuncionario.objects.all(),
            "tipos_documento": TipoDocumento.objects.all(),
            "estados": estados,
        },
    )


@login_required(login_url="login")
def nuevo_documento(request):
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Documento agregado exitosamente.")
            return redirect("lista_documentos")
        messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = DocumentoForm()
    return render(request, "documentos/insertar.html", {"form": form})


@login_required(login_url="login")
def editar_documento(request, pk):
    documento = get_object_or_404(DocumentoFuncionario, pk=pk)

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES, instance=documento)

        # 1) ¿Pidió eliminar el archivo actual?
        if request.POST.get("archivo-clear"):
            if documento.archivo:
                # borra el archivo físico sin guardar todavía
                documento.archivo.delete(save=False)
            documento.archivo = None  # limpia el campo en memoria

        # 2) ¿Subió un archivo nuevo? entonces borra el anterior
        elif request.FILES.get("archivo") and documento.archivo:
            # si existe, eliminar el anterior antes de guardar el nuevo
            documento.archivo.delete(save=False)

        if form.is_valid():
            form.save()
            messages.success(request, "Documento actualizado exitosamente.")
            return redirect("lista_documentos")
        messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = DocumentoForm(instance=documento)

    return render(
        request,
        "documentos/editar.html",
        {
            "form": form,
            "documento": documento,
            "archivo_nombre": os.path.basename(documento.archivo.name) if documento.archivo else "",
        },
    )


@login_required(login_url="login")
def eliminar_documento(request, pk):
    documento = get_object_or_404(DocumentoFuncionario, pk=pk)

    if request.method == "POST":
        if documento.archivo:
            documento.archivo.delete(save=False)
        documento.delete()
        messages.success(request, 'Documento eliminado correctamente.')
        return redirect("lista_documentos")

    return render(request, "documentos/eliminar.html", {"documento": documento})


# ----- Tipos de documento -----

@login_required(login_url="login")
def lista_tipos_documento(request):
    tipos = TipoDocumento.objects.all().order_by("nombre")
    return render(request, "documentos/tipos/index.html", {"tipos": tipos})


@login_required(login_url="login")
def nuevo_tipo_documento(request):
    if request.method == "POST":
        form = TipoDocumentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de documento agregado exitosamente.")
            return redirect("lista_tipos_documento")
    else:
        form = TipoDocumentoForm()
    return render(request, "documentos/tipos/insertar.html", {"form": form})


@login_required(login_url="login")
def editar_tipo_documento(request, pk):
    tipo = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == "POST":
        form = TipoDocumentoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de documento actualizado exitosamente.")
            return redirect("lista_tipos_documento")
    else:
        form = TipoDocumentoForm(instance=tipo)
    return render(request, "documentos/tipos/editar.html", {"form": form})


@login_required(login_url="login")
def eliminar_tipo_documento(request, pk):
    tipo = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == "POST":
        try:
            tipo.delete()
            messages.success(request, "✅ Tipo de documento eliminado exitosamente.")
        except ProtectedError:
            messages.error(
                request,
                "⚠️ No se puede eliminar este tipo porque tiene documentos asociados.",
            )
        return redirect("lista_tipos_documento")
    return render(request, "documentos/tipos/eliminar.html", {"tipo": tipo})
