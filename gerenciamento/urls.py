from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'gerenciamento'

urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login", ),
    path('sair/', auth_views.LogoutView.as_view(), name="logout"),
    path('', views.home, name='home'),
    path('gestao/', views.gestao, name='gestao'),
    path('perfil/', views.perfil, name='perfil'),
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('aluno/salvar/', views.salvar_aluno, name='cadastrar_aluno'),
    path('aluno/salvar/<int:aluno_id>/', views.salvar_aluno, name='editar_aluno'),
    path('aluno/excluir/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),
    path('coordenadores/', views.listar_coordenadores, name='listar_coordenadores'),
    path('coordenador/salvar/', views.salvar_coordenador, name='cadastrar_coordenador'),
    path('coordenador/salvar/<int:coordenador_id>/', views.salvar_coordenador, name='editar_coordenador'),
    path('coordenador/excluir/<int:coordenador_id>/', views.excluir_coordenador, name='excluir_coordenador'),
    path('hospitais/', views.listar_hospitais, name='listar_hospitais'),
    path('hospital/salvar/', views.salvar_hospital, name='cadastrar_hospital'),
    path('hospital/salvar/<int:hospital_id>/', views.salvar_hospital, name='editar_hospital'),
    path('hospital/excluir/<int:hospital_id>/', views.excluir_hospital, name='excluir_hospital'),
]
