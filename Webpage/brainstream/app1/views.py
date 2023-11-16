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
    username = request.user.username
    superus_img = []
    superus_descarga = []
    superus_arrays = []
    nfile = []
    n1 = []

    ruta_carpeta_imagenes = os.path.join("static", "img", "historial", username, "preview")
    ruta_todos = os.path.join("static", "img", "historial")
    nombres_archivos = os.listdir(ruta_carpeta_imagenes)

    for cadena in nombres_archivos:
        nueva_cadena = cadena.split('.')[0]  # Elimina los últimos 4 caracteres
        n1.append(nueva_cadena)

    todos_archivos = os.listdir(ruta_todos)

    for x in todos_archivos:
        n2 = []
        ruta_usuarios = os.path.join(ruta_todos, x, "preview")
        nombres_archivos_todos = os.listdir(ruta_usuarios)
        for cadena in nombres_archivos_todos:
            nueva_cadena = cadena.split('.')[0]  # Elimina los últimos 4 caracteres
            n2.append(nueva_cadena)

        nfile = n2+nfile

        ruta_final = [os.path.join("img", "historial", x, "preview",  nombre_archivo_todos) for nombre_archivo_todos in nombres_archivos_todos]
        superus_img = ruta_final+superus_img
        
    # for x in todos_archivos:
    #     ruta_usuarios = os.path.join(ruta_todos, x, "informes")
    #     nombres_archivos_todos = os.listdir(ruta_usuarios)

    #     ruta_final = [os.path.join("img", "historial", x, "informes",  nombre_archivo_todos) for nombre_archivo_todos in nombres_archivos_todos]
    #     superus_informe = ruta_final+superus_informe

    for x in todos_archivos:
        ruta_usuarios = os.path.join(ruta_todos, x, "download")
        nombres_archivos_todos = os.listdir(ruta_usuarios)

        ruta_final = [os.path.join("img", "historial", x, "download",  nombre_archivo_todos) for nombre_archivo_todos in nombres_archivos_todos]
        superus_descarga = ruta_final+superus_descarga
        
    imagenes_urls = [os.path.join("img", "historial", username, "preview", nombre_archivo) for nombre_archivo in nombres_archivos]

    for x in todos_archivos:
        ruta_usuarios = os.path.join(ruta_todos, x, "array")
        nombres_archivos_todos = os.listdir(ruta_usuarios)

        ruta_final = [os.path.join("img", "historial", x, "array",  nombre_archivo_todos) for nombre_archivo_todos in nombres_archivos_todos]
        superus_arrays = ruta_final+superus_arrays
        

    #------------informes--------------
    # ruta_carpeta_informes = os.path.join("static", "img", "historial", username, "informes")
    # nombres_informes = os.listdir(ruta_carpeta_informes)
    # informes_urls = [os.path.join("img", "historial", username, "informes", nombre_informe) for nombre_informe in nombres_informes]

    #------------download--------------

    ruta_carpeta_descargas = os.path.join("static", "img", "historial", username, "download")
    nombres_descargas = os.listdir(ruta_carpeta_descargas)
    descargas_urls = [os.path.join("img", "historial", username, "download", nombre_descarga) for nombre_descarga in nombres_descargas]

    #------------array--------------

    ruta_carpeta_arrays = os.path.join("static", "img", "historial", username, "array")
    nombres_arrays = os.listdir(ruta_carpeta_arrays)
    arrays_urls = [os.path.join("static", "img", "historial", username, "array", nombre_descarga) for nombre_descarga in nombres_arrays]



    imagen_nombre = zip(n1, imagenes_urls, descargas_urls, arrays_urls)
    imagen_nombre2 = zip(nfile, superus_img, superus_descarga, superus_arrays)
    print(superus_descarga)


    if request.user.is_superuser:
        return render(request, "content/historial.html", {"nombre": username, "imagenes_urls": imagen_nombre2}) 
    else:
        return render(request, "content/historial.html", {"nombre": username, "imagenes_urls": imagen_nombre}) 
