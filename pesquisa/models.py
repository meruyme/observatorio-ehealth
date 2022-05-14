from django.db import models


class Pesquisa(models.Model):
    titulo = models.CharField(max_length=500, verbose_name='Título')
    coordenador_responsavel = models.ForeignKey('gerenciamento.Coordenador', on_delete=models.PROTECT,
                                                related_name='pesquisas', verbose_name='Coordenador responsável')
    data_inicio = models.DateField(verbose_name='Data de início')
    data_fim = models.DateField(verbose_name='Data de fim')
    hospitais = models.ManyToManyField('gerenciamento.Hospital', through='HospitalPesquisa')
    perguntas = models.ManyToManyField('Pergunta', through='PerguntaPesquisa')

    def __str__(self):
        return self.titulo


class Pergunta(models.Model):
    titulo = models.CharField(max_length=700, verbose_name='Título')
    multipla_escolha = models.BooleanField(default=False, verbose_name='Múltipla escolha')
    opcoes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.titulo


class PerguntaPesquisa(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='perguntas_pesquisa')
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE, related_name='perguntas_pesquisa')


class HospitalPesquisa(models.Model):
    hospital = models.ForeignKey('gerenciamento.Hospital', on_delete=models.CASCADE, related_name='hospitais_pesquisa')
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE, related_name='hospitais_pesquisa')


class AlunoPesquisa(models.Model):
    aluno = models.ForeignKey('gerenciamento.Aluno', on_delete=models.PROTECT, related_name='alunos_pesquisa')
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE, related_name='alunos_pesquisa')


class Resposta(models.Model):
    aluno_pesquisa = models.ForeignKey(AlunoPesquisa, on_delete=models.CASCADE, related_name='respostas')
    hospital_pesquisa = models.ForeignKey(HospitalPesquisa, on_delete=models.CASCADE, related_name='respostas')
    respostas = models.ManyToManyField(PerguntaPesquisa, through='RespostaPergunta')


class RespostaPergunta(models.Model):
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE, related_name='respostas_pergunta')
    pergunta_pesquisa = models.ForeignKey(PerguntaPesquisa, on_delete=models.CASCADE,
                                          related_name='respostas_pergunta')
    resultado = models.TextField()
