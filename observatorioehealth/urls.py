from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gerenciamento/', include('gerenciamento.urls', namespace='gerenciamento')),
    path('pesquisa/', include('pesquisa.urls', namespace='pesquisa')),
    path("select2/", include("django_select2.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
