from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'gerenciamento'

urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login", ),
    path('sair/', auth_views.LogoutView.as_view(), name="logout"),
    path('', views.home, name='home'),
    path('aluno/salvar/', views.salvar_aluno, name='cadastrar_aluno'),
    path('aluno/salvar/<int:aluno_id>/', views.salvar_aluno, name='editar_aluno'),
    path('hospital/salvar/', views.salvar_hospital, name='cadastrar_hospital'),
    path('hospital/salvar/<int:hospital_id>/', views.salvar_hospital, name='editar_hospital'),
]
