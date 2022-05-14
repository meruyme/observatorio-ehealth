from django.urls import path
from . import views

app_name = 'pesquisa'

urlpatterns = [
    path('pesquisa/salvar/', views.salvar_pesquisa, name='salvar_pesquisa'),
]
