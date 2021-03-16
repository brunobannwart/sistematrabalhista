from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import os, requests
from .models import Associado
from .forms import FormCadastro, FormEditar

# Create your views here.
@login_required(login_url='login')
def associatedlist_view(request):
	associados = Associado.objects.all()

	contexto = {
		'associados': associados,
	}

	return render(request, 'associated/list.html', contexto)

@login_required(login_url='login')
@csrf_protect
def associatedcreate_view(request):
	os.environ['NO_PROXY'] = '127.0.0.1'
	editar = False

	if request.method == 'POST':
		formulario = FormCadastro(request.POST, request.FILES)

		if formulario.is_valid():
			campos = formulario.clean_form()

			if Associado.objects.filter(email=campos['email']) | Associado.objects.filter(cpf=campos['cpf']):
				formulario = request.POST
				
				if Associado.objects.filter(email=campos['email']):
					erro = 'Já existe aluno com esse email cadastrado'
				else:
					erro = 'Já existe aluno com esse CPF'
			else:
				try:
					resposta = requests.post('http://127.0.0.1:5000/api/treino', data={'grupo': 'associado'}, files={ 'file': campos['foto'] })

					if resposta.status_code == 200:
						resposta = resposta.json()

						novo_associado = Associado.objects.create(foto=campos['foto'], nome=campos['nome'], cpf=campos['cpf'], 
											celular=campos['celular'], cep=campos['cep'], data_nascimento=campos['data_nascimento'], 
											numero=campos['numero'], email=campos['email'], senha_hash=campos['senha_hash'], treino=resposta['treino'],
											pcd=campos['pcd'], outras_informacoes=campos['outras_informacoes'], acessibilidade=campos['acessibilidade'])

						novo_associado.save()
						return redirect('associatedlist')

					else:
						formulario = request.POST
						erro = 'Foto inválida'
				except:
					formulario = request.POST
					erro = 'Não foi possível cadastrar novo associado'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		formulario = {
			'foto': None,
			'nome': '', 
			'data_nascimento': '',
			'cpf': '', 
			'email': '', 
			'senha': '', 
			'celular': '',
			'cep': '',  
			'numero': '',
			'pcd': '',
			'outras_informacoes': '',
			'acessibilidade': 'nenhum',
		}

		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	contexto.update(csrf(request))
	return render(request, 'associated/form.html', contexto)

@login_required(login_url='login')
@csrf_protect
def associatededit_view(request, id=0):
	if id == 0:
		return redirect('associatedlist')

	editar = True

	if request.method == 'POST':
		formulario = FormEditar(request.POST, request.FILES or None)

		if formulario.is_valid():
			campos = formulario.clean_form()

			try:
				editar_associado = Associado.objects.get(id=id)

				if 'foto' in request.FILES:
					editar_associado.removePhoto()
					editar_associado.foto = campos['foto']

				editar_associado.nome = campos['nome']
				editar_associado.data_nascimento = campos['data_nascimento']
				editar_associado.celular = campos['celular']
				editar_associado.cep = campos['cep']
				editar_associado.cpf = campos['cpf']
				editar_associado.numero = campos['numero']
				editar_associado.pcd = campos['pcd']
				editar_associado.outras_informacoes = campos['outras_informacoes']
				editar_associado.acessibilidade = campos['acessibilidade']

				if request.POST.get('senha') != '':
					editar_associado.senha_hash = campos['senha_hash']

				if editar_associado.email != campos['email']:
					if not Associado.objects.filter(email=campos['email']):
						editar_associado.email = campos['email']
						editar_associado.save()
						return redirect('associatedlist')

					else:
						formulario = request.POST
						erro = 'Já existe aluno com esse email cadastrado'
				else:
					editar_associado.email = campos['email']
					editar_associado.save()
					return redirect('associatedlist')

			except:
				formulario = request.POST
				erro = 'Não foi possível atualizar este associado'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		try:
			formulario = Associado.objects.get(id=id)
			erro = None

		except:
			return redirect('associatedlist')

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	contexto.update(csrf(request))
	return render(request, 'associated/form.html', contexto)

@login_required(login_url='login')
@csrf_protect
def associateddelete_view(request, id=0):
	if id == 0:
		return redirect('associatedlist')

	if request.method == 'POST':
		try:
			associado = Associado.objects.get(id=id)
			treino = associado.treino
			resposta = requests.post('http://127.0.0.1:5000/api/remover', data={'treino': treino})
			
			if resposta.status_code == 200:
				associado.delete()

		finally:
			return redirect('associatedlist')
	else:
		return redirect('associatedlist')