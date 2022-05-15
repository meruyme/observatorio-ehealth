from django.urls import path
from . import views

app_name = 'pesquisa'

urlpatterns = [
    path('acoes/', views.pesquisa_acoes, name='acoes'),
    path('pesquisa/importar/', views.importar_pesquisa, name='importar_pesquisa'),
    path('pesquisa/salvar/', views.salvar_pesquisa, name='cadastrar_pesquisa'),
    path('pesquisa/salvar/<int:pesquisa_id>/', views.salvar_pesquisa, name='editar_pesquisa'),
    path('pesquisas/', views.listar_pesquisas, name='listar_pesquisas'),
    path('pesquisa/excluir/<int:pesquisa_id>/', views.excluir_pesquisa, name='excluir_pesquisa'),
    path('pergunta/salvar/', views.salvar_pergunta, name='salvar_pergunta'),
    path('resposta/salvar/<int:pesquisa_id>/', views.salvar_resposta, name='cadastrar_resposta'),
    path('resposta/salvar/<int:pesquisa_id>/<int:resposta_id>/', views.salvar_resposta, name='editar_resposta'),
    path('respostas/', views.listar_respostas, name='listar_respostas'),
    path('resposta/excluir/<int:resposta_id>/', views.excluir_resposta, name='excluir_resposta'),
]
