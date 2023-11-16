import json
from random import randint
import os
from time import sleep
from time import time
import datetime
import array
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache  # This is the memcache cache.
import serial
from django.shortcuts import render, redirect
from django.urls import reverse
import asyncio
import matplotlib.pyplot as plt
from app1.models import Datos  # Ajusta la ruta a tu modelo
import numpy as np
import mne
from django.contrib.auth.decorators import login_required
from channels.auth import login
import pyedflib
serial_port = serial.Serial('COM3', baudrate=115200)
serial_port.timeout = None


class GraphConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bases = 0
        self.recording = False
        # self.user = 0

    def connect(self):
        self.accept()
        self.send(json.dumps(
            {"value": 0, "sfreq": 0, "counter": 0}))
        # sleep(1)
    # redirect(reverse("welcome"))

    def disconnect(self, close_code):
        # Código de desconexión
        self.close()

    def receive(self, text_data):
        # User has changed the URL
        # validation = False
        text_data_json = json.loads(text_data)
        print(text_data_json)
        inicio = time()
        fin = time()
        counter = 0
        vsend = []
        sfreq = 0
        while fin-inicio <= 0.05:
            data = serial_port.readline().decode('utf-8', errors="ignore").strip()
            ndata = [s for s in data if s != '\x00']
            ndata = ''.join(ndata)
            ndata = ndata.split('\t')
            sfreq = ndata[1]
            try:
                ndata = float(ndata[0])
            except ValueError:
                ndata = 0
            counter += 1
            fin = time()
            vsend.append(ndata)
        if text_data_json:
            instancia, creado = Datos.objects.get_or_create(id=1, defaults={'valores': [0]})
            # instancia.valores.append("ZURDOS DE MIERDAAA")
            # instancia.save()
            ultimo_valor = instancia.valores[-1]
            nuevo_valor_int = int(ultimo_valor) + 1
            instancia.valores.append(int(nuevo_valor_int))
            instancia.save()
        self.send(json.dumps(
            {"value": vsend, "sfreq": sfreq, "counter": counter}))
