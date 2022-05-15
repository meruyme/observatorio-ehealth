from django import forms
from django.contrib.auth import get_user_model, update_session_auth_hash

from gerenciamento.models import Aluno, Hospital, Coordenador

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
        if email:
            instance = self.instance
            users = User.objects.filter(email=email)
            if instance.pk:
                users = users.exclude(pk=instance.auth_user.pk)
            if users.exists():
                self.add_error('email', 'E-mail já está em uso.')
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = cpf.replace('.', '').replace('-', '')
            instance = self.instance
            alunos = Aluno.objects.filter(ativo=True, cpf=cpf)
            if instance.pk:
                alunos = alunos.exclude(pk=instance.pk)
            if alunos.exists():
                self.add_error('cpf', 'Aluno com esse CPF já existe.')
        return cpf

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if matricula:
            instance = self.instance
            alunos = Aluno.objects.filter(ativo=True, matricula=matricula)
            if instance.pk:
                alunos = alunos.exclude(pk=instance.pk)
            if alunos.exists():
                self.add_error('cpf', 'Aluno com essa matrícula já existe.')
        return matricula

    def __init__(self, *args, **kwargs):
        aluno = kwargs.get('instance')
        super(SalvarAlunoForm, self).__init__(*args, **kwargs)
        if aluno:
            self.fields['email'].initial = aluno.auth_user.email


class SalvarCoordenadorForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = Coordenador
        fields = ['nome', 'cpf', 'data_nascimento', 'email', 'telefone']
        widgets = {
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d', attrs={
                    "required": True,
                    "type": "date"
                }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            instance = self.instance
            users = User.objects.filter(email=email)
            if instance.pk:
                users = users.exclude(pk=instance.auth_user.pk)
            if users.exists():
                self.add_error('email', 'E-mail já está em uso.')
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = cpf.replace('.', '').replace('-', '')
            instance = self.instance
            coordenadores = Coordenador.objects.filter(ativo=True, cpf=cpf)
            if instance.pk:
                coordenadores = coordenadores.exclude(pk=instance.pk)
            if coordenadores.exists():
                self.add_error('cpf', 'Coordenador com esse CPF já existe.')
        return cpf

    def __init__(self, *args, **kwargs):
        coordenador = kwargs.get('instance')
        super(SalvarCoordenadorForm, self).__init__(*args, **kwargs)
        if coordenador:
            self.fields['email'].initial = coordenador.auth_user.email


class RedefinirSenhaForm(forms.Form):
    senha = forms.CharField(label='Nova senha', widget=forms.PasswordInput(), min_length=6,
                            max_length=20, help_text='A nova senha deve ter entre 6 e 20 dígitos', required=False)
    confirmacao = forms.CharField(widget=forms.PasswordInput(), label='Confirmação de senha',
                                  min_length=6, max_length=20, required=False)

    def __init__(self, user, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RedefinirSenhaForm, self).__init__(*args, **kwargs)
        self.usuario = user

    def clean(self):
        senha = self.cleaned_data.get('senha')
        confirmacao = self.cleaned_data.get('confirmacao')

        if senha and not confirmacao:
            self.add_error('confirmacao', "Este campo é obrigatório ao redefinir a senha.")
        if not senha and confirmacao:
            self.add_error('senha', "Este campo é obrigatório ao redefinir a senha.")
        if senha and confirmacao:
            if senha != confirmacao:
                self.add_error('confirmacao', "A senha e a confirmação precisam ser iguais.")
                self.add_error('senha', "A senha e a confirmação precisam ser iguais.")

        return self.cleaned_data

    def save(self):
        self.usuario.set_password(self.cleaned_data['senha'])
        self.usuario.save()
        if self.request:
            update_session_auth_hash(self.request, self.usuario)
        return self.usuario


class SalvarHospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
