from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection

from administradores.models import Administrador
from empresas.models import Empresa
from .backend import BackendLogin
from .forms import FormLogin, FormTrocar
from .utils import rebuild_image, render_to_pdf

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
					return redirect('adminlist')

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
			resposta = requests.post('http://127.0.0.1:5000/api/reconhecimento', data={'grupo': 'administrador'}, files={ 'file': ('foto.png', foto, 'image/png')})

			if resposta.status_code  == 200:
				resposta = resposta.json()

				try:
					administrador = Administrador.objects.get(treino=resposta['reconhecimento'])
					administrador.is_authenticated = True
					administrador.save()

					login(request, administrador, backend='administrador.backend.BackendLogin')
					return redirect('adminlist')

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

def readmore_view(request):
	return render(request, 'login/readmore.html', {})

def logout_view(request):
	try:
		email = request.user.email
		logout(request)
		administrador = Administrador.objects.get(email=email)
		administrador.is_authenticated = False
		administrador.save()
	finally:
		return redirect('login')

@login_required(login_url='login')
@csrf_protect
def changepassword_view(request):
	if request.method == 'POST':
		formulario = FormTrocar(request.POST)

		if formulario.is_valid():
			campos = formulario.clean_form()

			try:
				administrador = Administrador.objects.get(email=campos['email'])

				if campos['senha_hash'] == campos['confirma_hash']:
					administrador.senha_hash = campos['senha_hash']
					administrador.save()
					return redirect('adminlist')

				else:
					formulario = request.POST
					erro = 'Senhas não são idênticas'

			except:
				formulario = request.POST
				erro = 'Email não cadastrado'
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

@login_required(login_url='login')
def joblist_view(request):
	vagas = []

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM vaga WHERE data_exp >= CURDATE() ORDER BY titulo ASC")
		resultados = cursor.fetchall()

		for resultado in resultados:
			try:
				empresa = Empresa.objects.get(id=resultado[1])

			except:
				empresa = None

			if empresa:
				vaga = {
					'id': resultado[0],
					'razao_social': empresa.razao_social,
					'email': empresa.email,
					'logo': settings.MEDIA_URL + resultado[2],
					'titulo': resultado[3],
					'data_exp': resultado[4],
					'descricao': resultado[5],
				}

				vagas.append(vaga)

	contexto = {
		'vagas': vagas
	}

	return render(request, 'job/list.html', contexto)

@login_required(login_url='login')
def jobread_view(request, id=0):
	if id == 0:
		return redirect('joblist')

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM vaga WHERE id=%s", [id])
		resultado = cursor.fetchone()

		if resultado:
			try:
				empresa = Empresa.objects.get(id=resultado[1])

				formulario = {
					'id': resultado[0],
					'razao_social': empresa.razao_social,
					'email': empresa.email,
					'logo': settings.MEDIA_URL + resultado[2],
					'titulo': resultado[3],
					'data_exp': resultado[4],
					'descricao': resultado[5],
				}

				contexto = {
					'form': formulario
				}

				return render(request, 'job/read.html', contexto)

			except:
				return redirect('joblist')
		else:
			return redirect('joblist')

@login_required(login_url='login')
def jobpdf_view(request, id=0):
	if id == 0:
		return redirect('joblist')

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM vaga WHERE id=%s", [id])
		resultado = cursor.fetchone()

		if resultado:
			try:
				empresa = Empresa.objects.get(id=resultado[1])

				formulario = {
					'id': resultado[0],
					'razao_social': empresa.razao_social,
					'email': empresa.email,
					'logo': settings.MEDIA_ROOT + '/' + resultado[2],
					'titulo': resultado[3],
					'data_exp': resultado[4],
					'descricao': resultado[5],
				}

				contexto = {
					'form': formulario
				}

				pdf = render_to_pdf('job/pdf.html', contexto)

				if pdf:
					resposta = HttpResponse(pdf, content_type='application/pdf')
					nomearquivo = resultado[3].replace(' ', '_').lower() + '.pdf'
					conteudo = 'inline; filename=%s' % (nomearquivo)
					resposta['Content-Disposition'] = conteudo
					return resposta

				else:
					return redirect('jobread', id=id)
			except:
				return redirect('joblist')
		else:
			return redirect('joblist')