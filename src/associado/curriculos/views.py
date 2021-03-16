from django.conf import settings
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
import os

from .forms import FormCadastro
from .models import Curriculo

# Create your views here.
@login_required(login_url='login')
def resumelist_view(request):
	if request.user.pcd:
		curriculos = Curriculo.objects.filter(associado_id=request.user.id)

		contexto = {
			'curriculos': curriculos
		}

		return render(request, 'session/resume/list.html', contexto)

	else:
		return render(request, 'session/resume/option.html', {})

@login_required(login_url='login')
def resumecreate_view(request):
	if request.method == 'POST':
		formulario = FormCadastro(request.POST, request.FILES or None)
	
		if formulario.is_valid():
			campos = formulario.clean_form()

			try:
				if not request.user.pcd:
					with connection.cursor() as cursor:
						cursor.execute("UPDATE associado SET instituicao_ensino=%s, curso_extra=%s, empresa_trabalhada=%s, cargo_ocupado=%s", 
							[campos['instituicao_ensino'], campos['curso_extra'], campos['empresa_trabalhada'], campos['cargo_ocupado']])

				else:
					if campos['instituicao_ensino'] != '' or campos['curso_extra'] != '' or campos['empresa_trabalhada'] != '' or campos['cargo_ocupado'] != '' or campos['laudo_medico']:
						novo_curriculo = Curriculo.objects.create(associado_id=request.user.id, instituicao_ensino=campos['instituicao_ensino'],
											curso_extra=campos['curso_extra'], empresa_trabalhada=campos['empresa_trabalhada'], cargo_ocupado=campos['cargo_ocupado'],
											laudo_medico=campos['laudo_medico'])

						novo_curriculo.save()

				return redirect('home')
			except:
				formulario = request.POST
				erro = 'Não foi possível cadastrar novo currículo'
		else:
			formulario = request.POST
			erro = 'Alguns campos não foram preenchidos corretamente'
	else:
		formulario = {
			'instituicao_ensino': '',
			'curso_extra': '',
			'empresa_trabalhada': '',
			'cargo_ocupado': '',
			'laudo_medico': '',
		}

		erro = None

	editar = False

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	return render(request, 'session/resume/form.html', contexto)

@login_required(login_url='login')
def resumeedit_view(request, id=0):
	if id == 0 and request.user.pcd:
		return redirect('resumelist')

	if request.user.pcd:
		try:
			formulario = Curriculo.objects.get(id=id)
			erro = None

		except:
			return redirect('resumelist')

	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM associado WHERE id=%s", [request.user.id])
			resultado = cursor.fetchone()

			if resultado:
				formulario = {
					'instituicao_ensino': resultado[12],
					'curso_extra': resultado[13],
					'empresa_trabalhada': resultado[14],
					'cargo_ocupado': resultado[15],
					'laudo_medico': '',
				}
				erro = None

			else:
				return redirect('resumelist')

	editar = True

	contexto = {
		'form': formulario,
		'erro': erro,
		'editar': editar,
	}

	return render(request, 'session/resume/form.html', contexto)