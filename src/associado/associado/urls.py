"""associado URL Configuration

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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from associado.views import login_view, camera_view, forgot_view, reset_view, changepassword_view, logout_view
from session.views import home_view, gamelist_view, gameread_view, videolessonlist_view, videolessonread_view

urlpatterns = [
	path('', login_view, name='login'),
	path('camera/', camera_view, name='camera'),
	path('esquecidados/', forgot_view, name='forgot'),
	path('redefinir/', reset_view, name='reset'),
	path('trocarsenha/', changepassword_view, name='changepassword'),
	path('sair/', logout_view, name='logout'),

	path('inicio/', home_view, name='home'),

	path('jogos/', gamelist_view, name='gamelist'),
	path('jogos/<int:id>/', gameread_view, name='gameread'),

	path('videoaulas/', videolessonlist_view, name='videolessonlist'),
	path('videoaulas/<int:id>/', videolessonread_view, name='videolessonread'),

	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT }),
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT }),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
