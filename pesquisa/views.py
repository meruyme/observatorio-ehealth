from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from gerenciamento.choices import TipoUsuario
from gerenciamento.decorators import tipo_usuario_required
from pesquisa.forms import SalvarPesquisaForm
from pesquisa.models import Pesquisa


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def salvar_pesquisa(request, pesquisa_id=None):
    if pesquisa_id:
        try:
            pesquisa = Pesquisa.objects.get(pk=pesquisa_id)
            form = SalvarPesquisaForm(request.POST or None, instance=pesquisa)
        except:
            messages.error(request, 'Pesquisa não existe.')
            return redirect('gerenciamento:home')
    else:
        form = SalvarPesquisaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            pesquisa = form.save()
            messages.success(request, 'Pesquisa salva com sucesso!')
            return redirect('gerenciamento:home')

    return render(request, 'pesquisa/salvar_pesquisa.html', locals())
