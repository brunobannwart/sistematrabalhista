from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout

from administradores.models import Administrador
from .backend import BackendLogin
from .forms import FormLogin, FormRedefinir
from .utils import rebuild_image, send_mail, hash_password, random_password

import os, requests

@csrf_protect
def login_view(request):
	if request.method == 'POST':
		try:
			formulario = FormLogin(request.POST)

			if formulario.is_valid():
				campos = formulario.clean_form()

				administrador = BackendLogin.authenticate(request, campos['email'], campos['senha_hash'])

				if administrador != None and administrador != False:
					administrador.is_authenticated = True
					administrador.save()

					login(request, administrador, backend='administrador.backend.BackendLogin')
					return redirect('cids')

				else:
					formulario = request.POST

					if administrador == False:
						erro = 'Senha não confere'

					else:
						erro = 'Não existe administrador com esse email'
			else:
				formulario = request.POST
				erro = 'Preencher campos corretamente'
		except:
			formulario = request.POST
			erro = 'Não foi possível realizar o login. Tente novamente'
	else:
		formulario = { 'email': '', 'senha': '' }
		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
	}

	contexto.update(csrf(request))
	return render(request, 'login/index.html', contexto)

@csrf_protect
def camera_view(request):
	os.environ['NO_PROXY'] = '127.0.0.1'

	if request.method == 'POST':
		endereco = request.POST.get('url')
		foto = rebuild_image(endereco)

		try:
			resposta = request.post('http://127.0.0.1:5000/api/reconhecimento', data={'grupo': 'administrador'}, files={ 'file': ('foto.png', foto, 'image/png')})

			if resposta.status_code  == 200:
				resposta = resposta.json()

				try:
					administrador = Administrador.objects.get(treino=resposta['reconhecimento'])
					administrador.is_authenticated = True
					administrador.save()

					login(request, administrador, backend='administrador.backend.BackendLogin')
					return redirect('cids')

				except:
					return redirect('login')
			else:
				return redirect('login')
		except:
			return redirect('login')
	else:
		return render(request, 'login/camera.html', {})

def forgot_view(request):
	return render(request, 'login/forgot.html', {})

@csrf_protect
def reset_view(request):
	if request.method == 'POST':
		formulario = FormRedefinir(request.POST)

		if formulario.is_valid():
			campos = formulario.clean_form()

			try:
				administrador = Administrador.objects.get(email=campos['email'])
				
				contexto = {
					'nome':	administrador.nome.upper(),
					'senha': random_password('0123456789', 6)
				}

				send_mail('Esqueci minha senha', 'option/email.html', 
					contexto, [administrador.email], settings.DEFAULT_FROM_EMAIL
				)

				administrador.senha_hash = hash_password(contexto['senha'])
				administrador.save()

				return redirect('login')

			except Exception as e:
				formulario = request.POST
				erro = 'Alguma falha ocorreu'

		else:
			formulario = request.POST
			erro = 'Preencher campos corretamente'

	else:
		formulario = {
			'cpf': '',
		}

		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
	}

	contexto.update(csrf(request))
	return render(request, 'login/reset.html', contexto)