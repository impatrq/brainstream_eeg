from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import sys
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import login
import os
import numpy as np
encoding = sys.getdefaultencoding()

def inicio(request):
    if request.user.is_authenticated:
        username = request.user.username
        ruta_carpeta_imagenes_prev = os.path.join("static", "img", "historial", username, "preview")
        # ruta_carpeta_np = os.path.join("static", "img", "historial", username, "informes")
        ruta_carpeta_edf= os.path.join("static", "img", "historial", username, "download")
        ruta_carpeta_np= os.path.join("static", "img", "historial", username, "array")
        for directory_path in [ruta_carpeta_imagenes_prev, ruta_carpeta_np, ruta_carpeta_edf]:
            os.makedirs(directory_path, exist_ok=True)
        return render(request, "content/inicio.html")
    else:
        return redirect(reverse("welcome"))


def result(request):
    if request.user.is_authenticated:
        username = request.user.username
        information = {"username": username}
        # login(request, user)
        return render(request, "eeg/result.html", information)
    else:
        return redirect(reverse("welcome"))

def bciin(request):
    if request.user.is_authenticated:
        return render(request, "content/bci.html")
    else:
        return redirect(reverse("welcome"))

def contactoin(request):
    if request.user.is_authenticated:
        return render(request, "content/contacto.html")
    else:
        return redirect(reverse("welcome"))

def acercain(request):
    if request.user.is_authenticated:
        return render(request, "content/acercade.html")
    else:
        return redirect(reverse("welcome"))

def cognitive(request):
    if request.user.is_authenticated:
        return render(request, "content/cognitive.html")
    else:
        return redirect(reverse("welcome"))

def historial(request):
    if request.user.is_authenticated:
        return render(request, "content/historial.html")
    else:
        return redirect(reverse("welcome"))
