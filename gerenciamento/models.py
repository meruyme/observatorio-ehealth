from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models
from localflavor.br.models import BRCPFField

from gerenciamento.choices import TipoUsuario, TipoLocal, TipoOrganizacao


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, verbose_name="Administrador")
    tipo_usuario = models.CharField(max_length=2, choices=TipoUsuario.CHOICES)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Coordenador(models.Model):
    nome = models.CharField(max_length=255)
    cpf = BRCPFField(verbose_name='CPF', unique=True)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    telefone = models.CharField(max_length=13, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coordenador')

    def __str__(self):
        return f'{self.nome} - {self.cpf}'


class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(verbose_name="Matrícula", max_length=13, unique=True)
    cpf = BRCPFField(verbose_name='CPF', unique=True)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    telefone = models.CharField(max_length=13, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aluno')
    coordenador_responsavel = models.ForeignKey(Coordenador, on_delete=models.PROTECT, related_name='alunos',
                                                verbose_name="Coordenador responsável")
    pesquisas = models.ManyToManyField('pesquisa.Pesquisa', through='pesquisa.AlunoPesquisa')

    def __str__(self):
        return f'{self.nome} - {self.cpf}'


class Pais(models.Model):
    nome = models.CharField(max_length=500)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.nome


class Hospital(models.Model):
    nome = models.CharField(max_length=500)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='hospitais', verbose_name='País')
    estado = models.CharField(max_length=300)
    cidade = models.CharField(max_length=300)
    tipo_local = models.CharField(max_length=2, choices=TipoLocal.CHOICES, verbose_name='Tipo do local')
    tipo_organizacao = models.CharField(max_length=2, choices=TipoOrganizacao.CHOICES,
                                        verbose_name='Tipo de organização')
