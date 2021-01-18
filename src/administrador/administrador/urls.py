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

from administrador.views import login_view, camera_view, forgot_view, reset_view
from administradores.views import adminlist_view, admindelete_view
from cursos.views import courselist_view, coursecreate_view, courseedit_view, coursedelete_view

urlpatterns = [
	path('extcomp/', admin.site.urls),

	path('', login_view, name='login'),
	path('camera/', camera_view, name='camera'),
	path('esquecidados/', forgot_view, name='forgot'),
	path('redefinir/', reset_view, name='reset'),

	path('administradores/', adminlist_view, name='adminlist'),
	path('administradores/excluir/<int:id>', admindelete_view, name='admindelete'),

	path('cursos/', courselist_view, name='courselist'),
	path('cursos/formulario/', coursecreate_view, name='coursecreate'),
	path('cursos/formulario/<int:id>/', courseedit_view, name='courseedit'),
	path('cursos/excluir/<int:id>/', coursedelete_view, name='coursedelete'),

	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT }),
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT }),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)