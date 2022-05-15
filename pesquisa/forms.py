from django import forms
from django_select2.forms import Select2MultipleWidget

from pesquisa.models import Pesquisa, Pergunta


class SalvarPesquisaForm(forms.ModelForm):
    class Meta:
        model = Pesquisa
        fields = ['titulo', 'data_inicio', 'data_fim', 'alunos', 'hospitais', 'perguntas']
        widgets = {
            'hospitais': Select2MultipleWidget,
            'perguntas': Select2MultipleWidget,
            'alunos': Select2MultipleWidget,
            'data_inicio': forms.DateInput(
                format='%Y-%m-%d', attrs={
                    "required": True,
                    "type": "date"
                }),
            'data_fim': forms.DateInput(
                format='%Y-%m-%d', attrs={
                    "required": True,
                    "type": "date"
                }),
        }


class SalvarPerguntaForm(forms.ModelForm):

    class Meta:
        model = Pergunta
        fields = ['titulo']

        labels = {
            'titulo': 'Pergunta'
        }

        widgets = {
            'titulo': forms.Textarea(attrs={'rows': 2})
        }
