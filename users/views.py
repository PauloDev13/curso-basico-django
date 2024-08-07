from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        confirmar_senha = request.POST['confirmar_senha']

        if username == '':
            messages.add_message(
                request,
                messages.WARNING,
                'Nome do usuário é obrigatório'
            )
            return redirect('/users/register')

        if senha == '':
            messages.add_message(
                request,
                messages.WARNING,
                'Senha é obrigatório'
            )
            return redirect('/users/register')

        if confirmar_senha == '':
            messages.add_message(
                request,
                messages.WARNING,
                'Confirme a senha'
            )
            return redirect('/users/register')

        if senha != confirmar_senha:
            messages.add_message(request, messages.ERROR, 'As senhas não conferem')
            return redirect('/users/register')

        if len(senha) < 6:
            messages.add_message(
                request,
                messages.ERROR,
                'A senha deve ter o mínimo de 6 caracteres'
            )
            return redirect('/users/register')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(
                request,
                messages.ERROR,
                f'Usuário "{users[0]}" já cadastrado'
            )
            return redirect('/users/register')

        user = User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('/users/login')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']

        user = auth.authenticate(
            username=username,
            password=senha
        )

        if user is not None:
            auth.login(request, user)
            return redirect('/company/add_company')

        messages.add_message(
            request,
            messages.ERROR,
            'Credenciais inválidas'
        )
        return redirect('/users/login')
