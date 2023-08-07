import json
from random import randint
from time import sleep
from time import time
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache  # This is the memcache cache.
import serial
from django.shortcuts import render, redirect
from django.urls import reverse
import asyncio
serial_port = serial.Serial('COM7', baudrate=115200)
serial_port.timeout = None


class GraphConsumer(WebsocketConsumer):
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
            ndata = float(ndata[0])
            counter += 1
            fin = time()
            vsend.append(ndata)

        # data = serial_port.readline().decode('utf-8', errors="ignore").strip()
        # ndata = [s for s in data if s != '\x00']
        # ndata = ''.join(ndata)
        # ndata = ndata.split('\t')
        # # print(type(ndata))
        # sfreq = ndata[1]
        # ndata = float(ndata[0])
        # fin = time()
        # print(fin-inicio)
        # vsend = vsend[:len(vsend)//100:]
        # print(len(vsend))
        self.send(json.dumps(
            {"value": vsend, "sfreq": sfreq, "counter": counter}))
