from django.urls import path
from . import views

app_name = 'pesquisa'

urlpatterns = [
    path('pesquisa/salvar/', views.salvar_pesquisa, name='cadastrar_pesquisa'),
    path('pesquisa/salvar/<int:pesquisa_id>/', views.salvar_pesquisa, name='editar_pesquisa'),
    path('pesquisas/', views.listar_pesquisas, name='listar_pesquisas'),
    path('pergunta/salvar/', views.salvar_pergunta, name='salvar_pergunta'),
]
