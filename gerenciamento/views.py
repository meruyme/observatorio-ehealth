from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from forms import SalvarAlunoForm
from django.contrib.auth import get_user_model

from gerenciamento.choices import TipoUsuario
from gerenciamento.decorators import tipo_usuario_required
from gerenciamento.models import Aluno

User = get_user_model()


def home(request):
    return render(request, 'home.html', locals())


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
