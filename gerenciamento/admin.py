from django.contrib import admin

# Register your models here.
from gerenciamento.models import Coordenador, Aluno, Pais, Hospital, User

admin.site.register(Coordenador)
admin.site.register(Aluno)
admin.site.register(Pais)
admin.site.register(Hospital)
admin.site.register(User)
