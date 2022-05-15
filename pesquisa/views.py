from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect

from gerenciamento.choices import TipoUsuario
from gerenciamento.decorators import tipo_usuario_required
from gerenciamento.utils import paginar_registros
from pesquisa.forms import SalvarPesquisaForm, SalvarPerguntaForm
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
    form_pergunta = SalvarPerguntaForm()
    if request.POST:
        if form.is_valid():
            pesquisa = form.save(commit=False)
            if not pesquisa_id:
                pesquisa.coordenador_responsavel = request.user.coordenador
            pesquisa.save()
            form.save_m2m()
            messages.success(request, 'Pesquisa salva com sucesso!')
            return redirect('pesquisa:listar_pesquisas')

    return render(request, 'pesquisa/salvar_pesquisa.html', locals())


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def listar_pesquisas(request):
    queryset = Pesquisa.objects.all().order_by('data_inicio', 'titulo')
    pesquisas = paginar_registros(request, queryset, 10)
    return render(request, 'pesquisa/listar_pesquisas.html', locals())


def salvar_pergunta(request):
    if request.is_ajax():
        form_pergunta = SalvarPerguntaForm(QueryDict(request.POST.get('form')).dict())
        if form_pergunta.is_valid():
            pergunta = form_pergunta.save()
            return JsonResponse({'id': pergunta.pk, 'titulo': pergunta.titulo})
    return JsonResponse({})


@tipo_usuario_required(TipoUsuario.COORDENADOR)
@transaction.atomic
def excluir_pesquisa(request, pesquisa_id):
    try:
        pesquisa = Pesquisa.objects.get(pk=pesquisa_id)
    except:
        messages.error(request, 'Pesquisa não existe.')
        return redirect('pesquisa:listar_pesquisas')
    pesquisa.delete()
    messages.success(request, 'Pesquisa excluído com sucesso!')
    return redirect('pesquisa:listar_pesquisas')
