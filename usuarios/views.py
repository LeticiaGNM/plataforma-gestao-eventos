from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CadastroForm


def cadastro(request):
    # Quem já está logado não precisa se cadastrar de novo.
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # já deixa o usuário logado
            messages.success(request, f'Bem-vindo(a), {usuario.first_name}! Seu cadastro foi concluído.')
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})