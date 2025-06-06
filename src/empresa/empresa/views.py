from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection

from core.models import LoginEmpresa
from .backend import BackendLogin
from .forms import FormLogin, FormRedefinir, FormTrocar
from .utils import rebuild_image, send_mail, hash_password, random_password

import os, requests

@csrf_protect
def login_view(request):
	if request.method == 'POST':
		try:
			formulario = FormLogin(request.POST)

			if formulario.is_valid():
				campos = formulario.clean_form()

				empresa = BackendLogin.authenticate(request, campos['email'], campos['senha_hash'])

				if empresa != None and empresa != False:
					empresa.is_authenticated = True
					empresa.save()

					login(request, empresa, backend='empresa.backend.BackendLogin')
					return redirect('joblist')

				else:
					formulario = request.POST

					if empresa == False:
						erro = 'Senha não confere'

					else:
						erro = 'Não existe empresa com esse email'
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
			resposta = requests.post('http://127.0.0.1:5000/api/reconhecimento', data={'grupo': 'empresa'}, files={ 'file': ('foto.png', foto, 'image/png')})

			if resposta.status_code  == 200:
				resposta = resposta.json()

				try:
					with connection.cursor() as cursor:
						cursor.execute("SELECT email, senha_hash FROM empresa WHERE treino=%s", [resposta['reconhecimento']])
						resultado = cursor.fetchone()

						if resultado != None:
							campos = {
								'email': resultado[0],
								'senha_hash': resultado[1],
							}

							empresa = BackendLogin.authenticate(request, campos['email'], campos['senha_hash'])

							if empresa != None and empresa != False:
								empresa.is_authenticated = True
								empresa.save()
								login(request, empresa, backend='empresa.backend.BackendLogin')
								return redirect('joblist')

							else:
								return redirect('login')
						else:
							return redirect('login')
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
				with connection.cursor() as cursor:
					cursor.execute("SELECT razao_social FROM empresa WHERE email=%s", [campos['email']])
					resultado = cursor.fetchone()
				
					contexto = {
						'nome': resultado[0],
						'senha': random_password('0123456789', 6)
					}

					send_mail('Esqueci minha senha', 'option/email.html', 
						contexto, [campos['email']], settings.DEFAULT_FROM_EMAIL
					)

					cursor.execute("UPDATE empresa SET senha_hash=%s WHERE email=%s", 
						[hash_password(contexto['senha']), campos['email']]
					)

					return redirect('login')

			except:
				formulario = request.POST
				erro = 'Alguma falha ocorreu'
		else:
			formulario = request.POST
			erro = 'Preencher campos corretamente'
	else:
		formulario = {
			'email': '',
		}

		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
	}

	contexto.update(csrf(request))
	return render(request, 'login/reset.html', contexto)

@login_required(login_url='login')
@csrf_protect
def changepassword_view(request):
	if request.method == 'POST':
		formulario = FormTrocar(request.POST)

		if formulario.is_valid():
			campos = formulario.clean_form()

			if campos['senha_hash'] == campos['confirma_hash']:
				try:
					with connection.cursor as cursor:
						cursor.execute("UPDATE empresa SET senha_hash=%s WHERE email=%s", [campos['senha_hash'], campos['email']])

					return redirect('joblist')

				except:
					formulario = request.POST
					erro = 'Email não cadastrado'
			else:
				formulario = request.POST
				erro = 'Senhas não conferem'
		else:
			formulario = request.POST
			erro = 'Preencher campos corretamente'
	else:
		formulario = {
			'email': '',
			'senha': '',
			'confirma': ''
		}

		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
	}

	contexto.update(csrf(request))
	return render(request, 'option/changepassword.html', contexto)

def logout_view(request):
	try:
		email = request.user.email
		logout(request)
		empresa = LoginEmpresa.objects.get(email=email)
		empresa.delete()
	finally:
		return redirect('login')