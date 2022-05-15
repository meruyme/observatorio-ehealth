from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect

from gerenciamento.choices import TipoUsuario
from gerenciamento.decorators import tipo_usuario_required
from gerenciamento.utils import paginar_registros
from pesquisa.forms import SalvarPesquisaForm, SalvarPerguntaForm, SalvarRespostaForm
from pesquisa.models import Pesquisa, Resposta, AlunoPesquisa, HospitalPesquisa, PerguntaPesquisa, RespostaPergunta


@login_required
def pesquisa_acoes(request):
    return render(request, 'pesquisa.html', locals())


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


@tipo_usuario_required(TipoUsuario.ALUNO)
@transaction.atomic
def salvar_resposta(request, pesquisa_id, resposta_id=None):
    resposta = None
    aluno = request.user.aluno
    initial = {}
    try:
        pesquisa = Pesquisa.objects.get(pk=pesquisa_id)
        aluno_pesquisa = AlunoPesquisa.objects.get(aluno=aluno, pesquisa=pesquisa)
    except:
        messages.error(request, 'Pesquisa não existe.')
        return redirect('pesquisa:listar_respostas')
    if resposta_id:
        try:
            resposta = Resposta.objects.get(pk=resposta_id)
            initial = {
                'hospital': resposta.hospital_pesquisa.hospital,
            }
            for resultado in RespostaPergunta.objects.filter(resposta=resposta):
                initial[f'pergunta_{resultado.pergunta_pesquisa.pergunta_id}'] = resultado.resultado
        except:
            messages.error(request, 'Resposta não existe.')
            return redirect('pesquisa:listar_respostas')
    else:
        hoje = date.today()
        if pesquisa.data_inicio > hoje or pesquisa.data_fim < hoje:
            messages.error(request, f"O tempo de coleta dessa pesquisa é entre "
                                    f"{pesquisa.data_inicio.strftime('%d/%m/%Y')} e "
                                    f"{pesquisa.data_fim.strftime('%d/%m/%Y')}.")
            return redirect('pesquisa:listar_respostas')
    form = SalvarRespostaForm(pesquisa, request, request.POST or None, initial=initial)
    if request.POST:
        if form.is_valid():
            hospital = form.cleaned_data.get('hospital')
            hospital_pesquisa = HospitalPesquisa.objects.get(hospital=hospital, pesquisa=pesquisa)
            respostas = {}
            for key, value in form.cleaned_data.items():
                if 'pergunta_' in key:
                    id_pergunta = int(key.replace('pergunta_', ''))
                    id_pergunta_pesquisa = PerguntaPesquisa.objects.get(pergunta_id=id_pergunta, pesquisa=pesquisa).pk
                    respostas[id_pergunta_pesquisa] = value
            if resposta:
                resposta.hospital_pesquisa = hospital_pesquisa
                resposta.save()
                RespostaPergunta.objects.filter(resposta=resposta).delete()
            else:
                resposta = Resposta.objects.create(hospital_pesquisa=hospital_pesquisa, aluno_pesquisa=aluno_pesquisa)
            for pergunta_pesquisa_id, resultado in respostas.items():
                RespostaPergunta.objects.create(resposta=resposta, pergunta_pesquisa_id=pergunta_pesquisa_id,
                                                resultado=resultado)
            messages.success(request, 'Resposta salva com sucesso!')
            return redirect('pesquisa:listar_respostas')
    return render(request, 'resposta/salvar_resposta.html', locals())


@login_required
@transaction.atomic
def listar_respostas(request):
    queryset = Resposta.objects.all()
    if request.user.tipo_usuario == TipoUsuario.ALUNO:
        queryset = queryset.filter(aluno_pesquisa__aluno=request.user.aluno)
    queryset = queryset.order_by('hospital_pesquisa__hospital__nome', 'aluno_pesquisa__aluno__nome')
    respostas = paginar_registros(request, queryset, 10)
    return render(request, 'resposta/listar_respostas.html', locals())


@tipo_usuario_required(TipoUsuario.ALUNO)
@transaction.atomic
def excluir_resposta(request, resposta_id):
    try:
        resposta = Resposta.objects.get(pk=resposta_id)
    except:
        messages.error(request, 'Resposta não existe.')
        return redirect('pesquisa:listar_respostas')
    resposta.delete()
    messages.success(request, 'Resposta excluída com sucesso!')
    return redirect('pesquisa:listar_respostas')
