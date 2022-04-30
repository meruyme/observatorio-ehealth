from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models

from gerenciamento.choices import TipoUsuario


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
