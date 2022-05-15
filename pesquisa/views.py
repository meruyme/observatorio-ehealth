from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from gerenciamento.choices import TipoUsuario
from gerenciamento.decorators import tipo_usuario_required
from gerenciamento.utils import paginar_registros
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
            return redirect('pesquisa:listar_pesquisas')
    else:
        form = SalvarPesquisaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            pesquisa = form.save(commit=False)
            pesquisa.coordenador_responsavel = request.user.coordenador
            pesquisa.save()
            pesquisa.save_m2m()
            messages.success(request, 'Pesquisa salva com sucesso!')
            return redirect('pesquisa:listar_pesquisas')

    return render(request, 'pesquisa/salvar_pesquisa.html', locals())


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def listar_pesquisas(request):
    queryset = Pesquisa.objects.all().order_by('data_inicio', 'titulo')
    pesquisas = paginar_registros(request, queryset, 10)
    return render(request, 'pesquisa/listar_pesquisas.html', locals())
