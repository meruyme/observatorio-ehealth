from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gerenciamento/', include('gerenciamento.urls', namespace='gerenciamento')),
    path('pesquisa/', include('pesquisa.urls', namespace='pesquisa')),
    path("select2/", include("django_select2.urls")),
    path('', RedirectView.as_view(url='gerenciamento/')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
