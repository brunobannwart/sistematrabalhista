from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout

from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image

from administradores.models import Administrador
from .backend import BackendLogin
from .forms import FormLogin

import os, requests, io
