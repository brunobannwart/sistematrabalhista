"""administrador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from administrador.views import login_view, camera_view, forgot_view, readmore_view, logout_view
from administrador.views import changepassword_view, joblist_view, jobread_view, jobpdf_view
from administrador.views import resumelist_view, resumeread_view, resumedelete_view
from administradores.views import adminlist_view, admincreate_view, adminedit_view, admindelete_view
from associados.views import associatedlist_view, associatedcreate_view, associatededit_view, associateddelete_view
from cursos.views import courselist_view, coursecreate_view, courseedit_view, coursedelete_view
from empresas.views import companylist_view, companycreate_view, companyedit_view, companydelete_view
from eventos.views import eventlist_view, eventcreate_view, eventedit_view, eventdelete_view
from jogos.views import gamelist_view, gamecreate_view, gameedit_view, gamedelete_view
from videoaulas.views import videolessonlist_view, videolessoncreate_view, videolessonedit_view, videolessondelete_view

urlpatterns = [
	path('vitalita/', admin.site.urls),

	path('', login_view, name='login'),
	path('camera/', camera_view, name='camera'),
	path('esquecidados/', forgot_view, name='forgot'),
	path('saibamais/', readmore_view, name='readmore'),
	path('trocarsenha/', changepassword_view, name='changepassword'),
	path('sair/', logout_view, name='logout'),

	path('administradores/', adminlist_view, name='adminlist'),
	path('administradores/formulario/', admincreate_view, name='admincreate'),
	path('administradores/formulario/<int:id>/', adminedit_view, name='adminedit'),
	path('administradores/excluir/<int:id>/', admindelete_view, name='admindelete'),

	path('alunos/', associatedlist_view, name='associatedlist'),
	path('alunos/formulario/', associatedcreate_view, name='associatedcreate'),
	path('alunos/formulario/<int:id>/', associatededit_view, name='associatededit'),
	path('alunos/excluir/<int:id>/', associateddelete_view, name='associateddelete'),

	path('curriculos/', resumelist_view, name='resumelist'),
	path('curriculos/<int:id>/', resumeread_view, name='resumeread'),
	path('curriculos/excluir/<int:id>/', resumedelete_view, name='resumedelete'),

	path('cursos/', courselist_view, name='courselist'),
	path('cursos/formulario/', coursecreate_view, name='coursecreate'),
	path('cursos/formulario/<int:id>/', courseedit_view, name='courseedit'),
	path('cursos/excluir/<int:id>/', coursedelete_view, name='coursedelete'),

	path('empresas/', companylist_view, name='companylist'),
	path('empresas/formulario/', companycreate_view, name='companycreate'),
	path('empresas/formulario/<int:id>/', companyedit_view, name='companyedit'),
	path('empresas/excluir/<int:id>/', companydelete_view, name='companydelete'),

	path('eventos/', eventlist_view, name='eventlist'),
	path('eventos/formulario/', eventcreate_view, name='eventcreate'),
	path('eventos/formulario/<int:id>/', eventedit_view, name='eventedit'),
	path('eventos/excluir/<int:id>/', eventdelete_view, name='eventdelete'),

	path('jogos/', gamelist_view, name='gamelist'),
	path('jogos/formulario/', gamecreate_view, name='gamecreate'),
	path('jogos/formulario/<int:id>/', gameedit_view, name='gameedit'),
	path('jogos/excluir/<int:id>/', gamedelete_view, name='gamedelete'),

	path('vagas/', joblist_view, name='joblist'),
	path('vagas/<int:id>/', jobread_view, name='jobread'),
	path('vagas/pdf/<int:id>/', jobpdf_view, name='jobpdf'),

	path('videoaulas/', videolessonlist_view, name='videolessonlist'),
	path('videoaulas/formulario/', videolessoncreate_view, name='videolessoncreate'),
	path('videoaulas/formulario/<int:id>/', videolessonedit_view, name='videolessonedit'),
	path('videoaulas/excluir/<int:id>/', videolessondelete_view, name='videolessondelete'),

	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT }),
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT }),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)