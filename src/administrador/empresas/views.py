from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import os, requests
from .models import Empresa
from .forms import FormCadastro, FormEditar

# Create your views here.
@login_required(login_url='login')
def companylist_view(request):
	empresas = Empresa.objects.all()

	contexto = {
		'empresas': empresas,
	}

	return render(request, 'company/list.html', contexto)

@login_required(login_url='login')
@csrf_protect
def companycreate_view(request):
	os.environ['NO_PROXY'] = '127.0.0.1'
	editar = False

	if request.method == 'POST':
		formulario = FormCadastro(request.POST, request.FILES)

		if formulario.is_valid():
			campos = formulario.clean_form()

			if Empresa.objects.filter(email=campos['email']) | Empresa.objects.filter(cnpj=campos['cnpj']):
				formulario = request.POST
				
				if Empresa.objects.filter(email=campos['email']):
					erro = 'Já existe empresa com esse email cadastrado'
				else:
					erro = 'Já existe empresa com esse CNPJ'
			else:
				try:
					resposta = requests.post('http://127.0.0.1:5000/api/treino', data={'grupo': 'empresa'}, files={ 'file': campos['foto'] })

					if resposta.status_code == 200:
						resposta = resposta.json()

						nova_empresa = Empresa.objects.create(foto=campos['foto'], logo=campos['logo'], razao_social=campos['razao_social'],
											nome_contato=campos['nome_contato'], cnpj=campos['cnpj'], telefone=campos['telefone'], cep=campos['cep'], 
											numero=campos['numero'], email=campos['email'], senha_hash=campos['senha_hash'], treino=resposta['treino'])

						nova_empresa.save()
						return redirect('companylist')

					else:
						formulario = request.POST
						erro = 'Foto inválida'
				except:
					formulario = request.POST
					erro = 'Não foi possível cadastrar nova empresa'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		formulario = {
			'logo': None,
			'foto': None,
			'razao_social': '', 
			'cnpj': '', 
			'nome_contato': '', 
			'email': '', 
			'senha': '', 
			'telefone': '',
			'cep': '',  
			'numero': '',
		}

		erro = None

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	contexto.update(csrf(request))
	return render(request, 'company/form.html', contexto)

@login_required(login_url='login')
@csrf_protect
def companyedit_view(request, id=0):
	if id == 0:
		return redirect('companylist')

	editar = True

	if request.method == 'POST':
		formulario = FormEditar(request.POST, request.FILES or None)

		if formulario.is_valid():
			campos = formulario.clean_form()

			try:
				editar_empresa = Empresa.objects.get(id=id)

				if 'foto' in request.FILES:
					editar_empresa.removePhoto()
					editar_empresa.foto = campos['foto']

				if 'logo' in request.FILES:
					editar_empresa.removeLogo()
					editar_empresa.logo = campos['logo']

				editar_empresa.razao_social = campos['razao_social']
				editar_empresa.email = campos['email']
				editar_empresa.nome_contato = campos['nome_contato']
				editar_empresa.telefone = campos['telefone']
				editar_empresa.cep = campos['cep']
				editar_empresa.cnpj = campos['cnpj']
				editar_empresa.numero = campos['numero']

				if request.POST.get('senha') != '':
					editar_empresa.senha_hash = campos['senha_hash']

				editar_empresa.save()
				return redirect('companylist')

			except:
				formulario = request.POST
				erro = 'Não foi possível atualizar este empresa'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		try:
			formulario = Empresa.objects.get(id=id)
			erro = None

		except:
			return redirect('companylist')

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	contexto.update(csrf(request))
	return render(request, 'company/form.html', contexto)

@login_required(login_url='login')
@csrf_protect
def companydelete_view(request, id=0):
	if id == 0:
		return redirect('companylist')

	if request.method == 'POST':
		try:
			empresa = Empresa.objects.get(id=id)
			treino = empresa.treino
			resposta = requests.post('http://127.0.0.1:5000/api/remover', data={'treino': treino})
			
			if resposta.status_code == 200:
				empresa.delete()

		finally:
			return redirect('companylist')
	else:
		return redirect('companylist')