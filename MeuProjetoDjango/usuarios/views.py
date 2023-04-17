from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from django.urls import reverse


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não coincidem.')
            return redirect(reverse('cadastro'))
        
        #para fazer: validar força da senha

        user = User.objects.filter(username=username)
        email_criado = User.objects.filter(email=email)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existente.')
            return redirect(reverse('cadastro'))
        
        if email_criado.exists():
            messages.add_message(request, constants.ERROR, 'Email já existente.')
            return redirect(reverse('cadastro'))
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Usuário salvo com sucesso.')

        return redirect(reverse('login'))
    


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

    user = auth.authenticate(username=username, password=senha)

    if not user:
        messages.add_message(request, constants.ERROR, "Username ou senha inválidos.")
        return redirect(reverse('login'))
    
    auth.login(request, user)

    return redirect('/eventos/novo_evento/')