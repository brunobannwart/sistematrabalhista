from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import os, requests
from .models import Administrador
from .forms import FormCadastro, FormEditar

# Create your views here.
@login_required(login_url='login')
def adminlist_view(request):
	administradores = Administrador.objects.all()

	contexto = {
		'administradores': administradores,
	}

	return render(request, 'administrator/list.html', contexto)

@login_required(login_url='login')
@csrf_protect
def admincreate_view(request):
	os.environ['NO_PROXY'] = '127.0.0.1'
	editar = False

	if request.method == 'POST':
		formulario = FormCadastro(request.POST, request.FILES)

		if formulario.is_valid():
			campos = formulario.clean_form()

			if Administrador.objects.filter(email=campos['email']):
				formulario = request.POST
				erro = 'Já existe administrador com esse email cadastrado'

			else:
				try:
					resposta = requests.post('http://127.0.0.1:5000/api/treino', data={'grupo': 'administrador'}, files={ 'file': campos['foto'] })

					if resposta.status_code == 200:
						resposta = resposta.json()

						novo_administrador = Administrador.objects.create(foto=campos['foto'], nome=campos['nome'], 
												email=campos['email'], senha_hash=campos['senha_hash'], treino=resposta['treino'])

						novo_administrador.save()
						return redirect('adminlist')

					else:
						formulario = request.POST
						erro = 'Foto inválida'
				except:
					formulario = request.POST
					erro = 'Não foi possível cadastrar novo administrador'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		formulario = {
			'foto': None,
			'nome': '',
			'email': '',
			'senha': '',
		}

		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	contexto.update(csrf(request))
	return render(request, 'administrator/form.html', contexto)

@login_required(login_url='login')
@csrf_protect
def adminedit_view(request, id=0):
	if id == 0:
		return redirect('adminlist')

	editar = True

	if request.method == 'POST':
		formulario = FormEditar(request.POST, request.FILES or None)

		if formulario.is_valid():
			campos = formulario.clean_form()

			try:
				editar_administrador = Administrador.objects.get(id=id)
				
				if 'foto' in request.FILES:
					editar_administrador.removePhoto()
					editar_administrador.foto = campos['foto']

				editar_administrador.nome = campos['nome']
				editar_administrador.email = campos['email']

				if request.POST.get('senha') != '':
					editar_administrador.senha_hash = campos['senha_hash']

				editar_administrador.save()
				return redirect('adminlist')

			except:
				formulario = request.POST
				erro = 'Não foi possível atualizar este administrador'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		try:
			formulario = Administrador.objects.get(id=id)
			erro = None

		except:
			return redirect('adminlist')

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	contexto.update(csrf(request))
	return render(request, 'administrator/form.html', contexto)

@login_required(login_url='login')
@csrf_protect
def admindelete_view(request, id=0):
	if id == 0:
		return redirect('adminlist')

	if request.method == 'POST':
		try:
			administrador = Administrador.objects.get(id=id)
			treino = administrador.treino
			resposta = requests.post('http://127.0.0.1:5000/api/remover', data={'treino': treino})
			
			if resposta.status_code == 200:
				administrador.delete()

		finally:
			return redirect('adminlist')
	else:
		return redirect('adminlist')