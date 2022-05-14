from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from gerenciamento.forms import SalvarAlunoForm, SalvarHospitalForm, SalvarCoordenadorForm, RedefinirSenhaForm
from django.contrib.auth import get_user_model

from gerenciamento.choices import TipoUsuario
from gerenciamento.decorators import tipo_usuario_required
from gerenciamento.models import Aluno, Hospital, Coordenador

User = get_user_model()


def home(request):
    return render(request, 'home.html', locals())


@login_required
@transaction.atomic
def perfil(request):
    user = request.user
    if user.is_coordenador:
        form = SalvarCoordenadorForm(request.POST or None, instance=user.pessoa)
    else:
        form = SalvarAlunoForm(request.POST or None, instance=user.pessoa)
    form_senha = RedefinirSenhaForm(user, request.POST or None, request=request)
    if request.POST:
        if form.is_valid() and form_senha.is_valid():
            pessoa = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            if form_senha.cleaned_data.get('senha'):
                form_senha.save()
    return render(request, 'perfil.html', locals())


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def salvar_coordenador(request, coordenador_id=None):
    if coordenador_id:
        try:
            coordenador = Coordenador.objects.get(pk=coordenador_id)
            form = SalvarCoordenadorForm(request.POST or None, instance=coordenador)
        except:
            messages.error(request, 'Coordenador não existe.')
            return redirect('gerenciamento:home')
    else:
        form = SalvarCoordenadorForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            coordenador = form.save(commit=False)
            if coordenador_id:
                user = coordenador.auth_user
                user.email = form.cleaned_data['email']
                user.save()
            else:
                user = User.objects.create_user(email=form.cleaned_data['email'],
                                                password=form.cleaned_data['cpf'],
                                                tipo_usuario=TipoUsuario.COORDENADOR)
                coordenador.auth_user = user
            coordenador.save()

    return render(request, 'coordenador/salvar_coordenador.html', locals())


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def salvar_aluno(request, aluno_id=None):
    if aluno_id:
        try:
            aluno = Aluno.objects.get(pk=aluno_id)
            form = SalvarAlunoForm(request.POST or None, instance=aluno)
        except:
            messages.error(request, 'Aluno não existe.')
            return redirect('gerenciamento:home')
    else:
        form = SalvarAlunoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            aluno = form.save(commit=False)
            if aluno_id:
                user = aluno.auth_user
                user.email = form.cleaned_data['email']
                user.save()
            else:
                aluno.coordenador_responsavel = request.user.coordenador
                user = User.objects.create_user(email=form.cleaned_data['email'],
                                                password=form.cleaned_data['cpf'],
                                                tipo_usuario=TipoUsuario.ALUNO)
                aluno.auth_user = user
            aluno.save()

    return render(request, 'aluno/salvar_aluno.html', locals())


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def excluir_aluno(request, aluno_id):
    try:
        aluno = Aluno.objects.get(pk=aluno_id)
    except:
        messages.error(request, 'Aluno não existe.')
        return redirect('gerenciamento:home')
    user = aluno.auth_user
    aluno.ativo = False
    user.is_active = False
    aluno.save()
    user.save()
    return redirect('gerenciamento:home')


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def salvar_hospital(request, hospital_id=None):
    if hospital_id:
        try:
            hospital = Hospital.objects.get(pk=hospital_id)
            form = SalvarHospitalForm(request.POST or None, instance=hospital)
        except:
            messages.error(request, 'Hospital não existe.')
            return redirect('gerenciamento:home')
    else:
        form = SalvarHospitalForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            hospital = form.save()

    return render(request, 'hospital/salvar_hospital.html', locals())
