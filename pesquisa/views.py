import csv
import traceback
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect

from gerenciamento.choices import TipoUsuario, TipoLocal, TipoOrganizacao
from gerenciamento.decorators import tipo_usuario_required
from gerenciamento.models import Aluno, Hospital, Pais
from gerenciamento.utils import paginar_registros, decode_utf8, get_id
from pesquisa.forms import SalvarPesquisaForm, SalvarPerguntaForm, SalvarRespostaForm, SelecionarPesquisaForm, \
    ImportarPesquisaForm
from pesquisa.models import Pesquisa, Resposta, AlunoPesquisa, HospitalPesquisa, PerguntaPesquisa, RespostaPergunta, \
    Pergunta


@login_required
def pesquisa_acoes(request):
    return render(request, 'pesquisa.html', locals())


@tipo_usuario_required(TipoUsuario.COORDENADOR)
def importar_pesquisa(request):
    form = ImportarPesquisaForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            header_inicial = {
                'titulo': 0, 'data_inicio': 1, 'data_fim': 2, 'matricula': 3
            }
            header = {
                'hospital': 0, 'pais': 1, 'estado': 2, 'cidade': 3, 'tipo_local': 4,
                'tipo_organizacao': 5
            }
            perguntas_pesquisa = []
            try:
                with transaction.atomic():
                    arquivo = decode_utf8(form.cleaned_data.get('arquivo'))
                    df = csv.reader(arquivo, delimiter=";")
                    next(df)
                    linha_pesquisa = next(df)
                    aluno = Aluno.objects.filter(ativo=True, matricula=linha_pesquisa[header_inicial['matricula']])\
                        .first()
                    if not aluno:
                        raise Exception('O aluno informado não está cadastrado no sistema.')
                    data_inicio = datetime.strptime(linha_pesquisa[header_inicial['data_inicio']], '%d/%m/%Y')
                    data_fim = datetime.strptime(linha_pesquisa[header_inicial['data_fim']], '%d/%m/%Y')
                    pesquisa = Pesquisa.objects.filter(titulo=linha_pesquisa[header_inicial['titulo']],
                                                       data_inicio=data_inicio, data_fim=data_fim,
                                                       coordenador_responsavel=request.user.coordenador).first()
                    if not pesquisa:
                        pesquisa = Pesquisa.objects.create(titulo=linha_pesquisa[header_inicial['titulo']],
                                                           data_inicio=data_inicio, data_fim=data_fim,
                                                           coordenador_responsavel=request.user.coordenador)
                    aluno_pesquisa = AlunoPesquisa.objects.filter(pesquisa=pesquisa, aluno=aluno).first()
                    if not aluno_pesquisa:
                        aluno_pesquisa = AlunoPesquisa.objects.create(pesquisa=pesquisa, aluno=aluno)
                    next(df)
                    linha_perguntas = next(df)
                    perguntas = linha_perguntas[6:]
                    for nome_pergunta in perguntas:
                        pergunta = Pergunta.objects.filter(titulo=nome_pergunta).first()
                        if not pergunta:
                            pergunta = Pergunta.objects.create(titulo=nome_pergunta)
                        pergunta_pesquisa = PerguntaPesquisa.objects.filter(pesquisa=pesquisa, pergunta=pergunta)\
                            .first()
                        if not pergunta_pesquisa:
                            pergunta_pesquisa = PerguntaPesquisa.objects.create(pesquisa=pesquisa, pergunta=pergunta)
                        perguntas_pesquisa.append(pergunta_pesquisa.pk)
                    for row in df:
                        pais = Pais.objects.get(nome=row[header['pais']])
                        tipo_local = get_id(TipoLocal, row[header['tipo_local']])
                        tipo_organizacao = get_id(TipoOrganizacao, row[header['tipo_organizacao']])
                        hospital = Hospital.objects.filter(pais=pais, nome=row[header['hospital']],
                                                           estado=row[header['estado']], cidade=row[header['cidade']],
                                                           tipo_local=tipo_local, tipo_organizacao=tipo_organizacao
                                                           ).first()
                        if not hospital:
                            hospital = Hospital.objects.create(pais=pais, nome=row[header['hospital']],
                                                               estado=row[header['estado']],
                                                               cidade=row[header['cidade']],
                                                               tipo_local=tipo_local, tipo_organizacao=tipo_organizacao)
                        hospital_pesquisa = HospitalPesquisa.objects.filter(hospital=hospital, pesquisa=pesquisa)\
                            .first()
                        if not hospital_pesquisa:
                            hospital_pesquisa = HospitalPesquisa.objects.create(hospital=hospital, pesquisa=pesquisa)
                        resposta = Resposta.objects.create(aluno_pesquisa=aluno_pesquisa,
                                                           hospital_pesquisa=hospital_pesquisa)
                        for index, value in enumerate(perguntas_pesquisa):
                            resultado = row[6 + index]
                            RespostaPergunta.objects.create(pergunta_pesquisa_id=value, resposta=resposta,
                                                            resultado=resultado)
                    messages.success(request, 'Importação realizada com sucesso!')
                    return redirect('pesquisa:listar_pesquisas')
            except Exception as e:
                if hasattr(e, 'message'):
                    mensagem = e.message
                else:
                    mensagem = e
                print(traceback.format_exc())
                messages.error(request, 'Ocorreu um erro durante a importação. Detalhes do erro: ' + str(mensagem))
                return redirect('pesquisa:importar_pesquisa')
    return render(request, 'pesquisa/importar_pesquisa.html', locals())


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


@login_required
@transaction.atomic
def salvar_resposta(request, pesquisa_id, resposta_id=None):
    resposta = None
    aluno = None
    initial = {}
    try:
        pesquisa = Pesquisa.objects.get(pk=pesquisa_id)
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
    aluno = request.user.aluno if request.user.is_aluno else resposta.aluno_pesquisa.aluno
    aluno_pesquisa = AlunoPesquisa.objects.get(aluno=aluno, pesquisa=pesquisa)
    form = SalvarRespostaForm(pesquisa, request, request.POST or None, initial=initial, resposta=resposta)
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
    form = SelecionarPesquisaForm(request, request.POST or None)
    if request.user.is_aluno:
        queryset = queryset.filter(aluno_pesquisa__aluno=request.user.aluno)
    queryset = queryset.order_by('hospital_pesquisa__hospital__nome', 'aluno_pesquisa__aluno__nome')
    respostas = paginar_registros(request, queryset, 10)
    if request.POST:
        if form.is_valid():
            pesquisa = form.cleaned_data.get('pesquisa')
            return redirect('pesquisa:cadastrar_resposta', pesquisa_id=pesquisa.pk)
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
