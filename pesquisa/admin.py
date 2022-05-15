from django.contrib import admin

from pesquisa.models import Pesquisa, Pergunta, Resposta, RespostaPergunta, AlunoPesquisa, HospitalPesquisa, \
    PerguntaPesquisa

admin.site.register(Pesquisa)
admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(RespostaPergunta)
admin.site.register(AlunoPesquisa)
admin.site.register(HospitalPesquisa)
admin.site.register(PerguntaPesquisa)
