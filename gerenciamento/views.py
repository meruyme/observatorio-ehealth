from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from forms import SalvarAlunoForm
from django.contrib.auth import get_user_model


User = get_user_model()


def home(request):
    return render(request, 'home.html', locals())


def salvar_aluno(request, aluno_id=None):
    form = SalvarAlunoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.coordenador_responsavel = request.user.coordenador
            user = User.objects.create_user(email=form.cleaned_data['email'],
                                            password=form.cleaned_data['cpf'])
            aluno.auth_user = user
            aluno.save()

    return render(request, 'aluno/salvar_aluno.html', locals())
