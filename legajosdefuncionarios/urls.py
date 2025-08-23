from django.contrib import admin
from django.urls import path, include
from legajosdefuncionarios import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("funcionarios/", include("funcionarios.urls")),
    path("documentos/", include("documentos.urls")),
    path("eventoslaborales/", include("eventoslaborales.urls")),
    path("evaluaciones/", include("evaluaciones.urls")),
    path("usuarios/", include("usuarios.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
