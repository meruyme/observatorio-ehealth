from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


def tipo_usuario_required(tipo_usuario=None):
    def decorator(func, **args):
        def newfn(request, **kwargs):
            if request.user.is_authenticated:
                if tipo_usuario:
                    if request.user.tipo_usuario != tipo_usuario:
                        return redirect('gerenciamento:home')
            else:
                return redirect('gerenciamento:login')
            return func(request, **kwargs)
        return newfn
    return decorator
