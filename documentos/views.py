from django.shortcuts import render
from .models import DocumentoFuncionario, PerfilFuncionario, TipoDocumento
from django.db.models import Q

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
