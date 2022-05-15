from django import forms
from django_select2.forms import Select2MultipleWidget

from gerenciamento.models import Hospital
from pesquisa.models import Pesquisa, Pergunta, Resposta


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

    def clean(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_fim = self.cleaned_data.get('data_fim')

        if data_inicio and data_fim and data_inicio > data_fim:
            self.add_error('data_inicio', 'A data de início deve ser menor que a data de fim.')

        return self.cleaned_data


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


class SalvarRespostaForm(forms.Form):
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    def __init__(self, pesquisa, request, *args, **kwargs):
        super(SalvarRespostaForm, self).__init__(*args, **kwargs)
        self.pesquisa = pesquisa
        self.request = request
        self.fields['hospital'].queryset = Hospital.objects.filter(hospitais_pesquisa__pesquisa=self.pesquisa)
        for pergunta in self.pesquisa.perguntas.all():
            self.fields[f'pergunta_{pergunta.pk}'] = forms.CharField(label=pergunta.titulo, required=True,
                                                                     widget=forms.Textarea(attrs={'rows': 2}))


