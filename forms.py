from django import forms

from gerenciamento.models import Aluno


class SalvarAlunoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'cpf', 'data_nascimento', 'email', 'telefone']
