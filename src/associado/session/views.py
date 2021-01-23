from django.conf import settings
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.
@login_required(login_url='login')
def home_view(request):
	return render(request, 'session/home/index.html', {})

@login_required(login_url='login')
def gamelist_view(request):
	jogos = []

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM jogo ORDER BY titulo ASC")
		resultados = cursor.fetchall()

		for resultado in resultados:
			jogo = {
				'id': resultado[0],
				'logo': settings.MEDIA_URL + resultado[1],
				'titulo': resultado[2],
				'url': resultado[3],
				'descricao': resultado[4],
			}

			jogos.append(jogo)

	contexto = {
		'jogos': jogos
	}

	return render(request, 'session/game/list.html', contexto)

@login_required(login_url='login')
def gameread_view(request, id=0):
	if id == 0:
		return redirect('gamelist')

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM jogo WHERE id=%s", [id])
		resultado = cursor.fetchone()

		if resultado != None:
			formulario = {
				'id': resultado[0],
				'logo': settings.MEDIA_URL + resultado[1],
				'titulo': resultado[2],
				'url': resultado[3],
				'descricao': resultado[4],
			}

			contexto = {
				'form': formulario
			}

			return render(request, 'session/game/read.html', contexto)
		else:
			return redirect('gamelist')

@login_required(login_url='login')
def videolessonlist_view(request):
	videoaulas = []

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM videoaula ORDER BY titulo ASC")
		resultados = cursor.fetchall()

		for resultado in resultados:
			videoaula = {
				'id': resultado[0],
				'logo': settings.MEDIA_URL + resultado[1],
				'titulo': resultado[2],
				'url': resultado[3],
				'descricao': resultado[4],
			}

			videoaulas.append(videoaula)

	contexto = {
		'videoaulas': videoaulas
	}

	return render(request, 'session/videolesson/list.html', contexto)

@login_required(login_url='login')
def videolessonread_view(request, id=0):
	if id == 0:
		return redirect('videolessonlist')

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM videoaula WHERE id=%s", [id])
		resultado = cursor.fetchone()

		if resultado != None:
			formulario = {
				'id': resultado[0],
				'logo': settings.MEDIA_URL + resultado[1],
				'titulo': resultado[2],
				'url': 'https://www.youtube.com/embed/' + resultado[3].split('=')[1],
				'descricao': resultado[4],
			}

			contexto = {
				'form': formulario
			}

			return render(request, 'session/videolesson/read.html', contexto)
		else:
			return redirect('videolessonlist')