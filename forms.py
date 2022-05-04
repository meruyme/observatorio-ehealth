from django import forms
from django.contrib.auth import get_user_model

from gerenciamento.models import Aluno


User = get_user_model()


class SalvarAlunoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'cpf', 'data_nascimento', 'email', 'telefone']
        widgets = {
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d', attrs={
                    "required": True,
                    "type": "date"
                }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        instance = self.instance
        users = User.objects.filter(email=email)
        if instance:
            users = users.exclude(pk=instance.auth_user.pk)
        if users.exists():
            self.add_error('email', 'E-mail já está em uso.')
        return email

    def __init__(self, *args, **kwargs):
        aluno = kwargs.get('instance')
        super(SalvarAlunoForm, self).__init__(*args, **kwargs)
        if aluno:
            self.fields['email'].initial = aluno.auth_user.email
