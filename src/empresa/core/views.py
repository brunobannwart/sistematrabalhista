from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.
@login_required(login_url='login')
def associatedlist_view(request):
	associados = []

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM associado ORDER BY nome ASC")
		resultados = cursor.fetchall()

		for resultado in resultados:
			associado = {
				'id': resultado[0],
				'foto': settings.MEDIA_URL,
			}

			associados.append(associado)


	contexto = {
		'associados': associados,
	}

	return render(request, 'core/associated/list.html', contexto)


@login_required(login_url='login')
def associatedread_view(request, id=0):
	if id == 0:
		return redirect('associatedlist')

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM associado WHERE id=%s", [id])
		resultado = cursor.fetchone()

		if resultado != None:
			formulario = {
				'id': resultado[0],
				'foto': settings.MEDIA_URL,
			}

			contexto = {
				'form': formulario,
			}

			return render(request, 'core/associated/read.html', contexto)

		else:
			return redirect('associatedlist')

@login_required(login_url='login')
def associatedpdf_view(request, id=0):
	if id == 0:
		return redirect('associatedlist')

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM associado WHERE id=%s", [id])
		resultado = cursor.fetchone()

		if resultado != None:
			formulario = {
				'id': resultado[0],
				'foto': settings.MEDIA_URL,
			}

			contexto = {
				'form': formulario,
			}

			return render(request, 'core/associated/read.html', contexto)

		else:
			return redirect('associatedlist')