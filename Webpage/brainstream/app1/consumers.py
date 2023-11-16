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
        try: 
            ultimo_registro = Datos.objects.latest('id')
            ultimo_id = ultimo_registro.id
            self.bases = ultimo_id+1
        except Datos.DoesNotExist:
            self.bases = 0
        print(self.bases)
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
        inicio = time()
        fin = time()
        counter = 0
        vsend = []
        value = 0
        sfreq = 0
        v1send = []
        v2send = []
        v3send = []
        v4send = []
        v5send = []
        v6send = []
        v7send = []
        v8send = []
        v9send = []
        v10send = []
        v11send = []
        v12send = []
        v13send = []
        v14send = []
        v15send = []
        v16send = []
        while fin-inicio <= 0.1:
            data = serial_port.readline().decode('utf-8', errors="ignore").strip()
            ndata = [s for s in data if s != '\x00']
            ndata = ''.join(ndata)
            ndata = ndata.split('\t')
            sfreq = ndata[16]
            try:
                v1send.append(float(ndata[0]))
                v2send.append(float(ndata[1]))
                v3send.append(float(ndata[2]))
                v4send.append(float(ndata[3]))
                v5send.append(float(ndata[4]))
                v6send.append(float(ndata[5]))
                v7send.append(float(ndata[6]))
                v8send.append(float(ndata[7]))
                v9send.append(float(ndata[8]))
                v10send.append(float(ndata[9]))
                v11send.append(float(ndata[10]))
                v12send.append(float(ndata[11]))
                v13send.append(float(ndata[12]))
                v14send.append(float(ndata[13]))
                v15send.append(float(ndata[14]))
                v16send.append(float(ndata[15]))
                # v1send = (np.random.random(100))
                # v2send = (np.random.random(100))
                # v3send = (np.random.random(100))
                # v4send = (np.random.random(100))
                # v5send = (np.random.random(100))
                # v6send = (np.random.random(100))
                # v7send = (np.random.random(100))
                # v8send = (np.random.random(100))
                # v9send = (np.random.random(100))
                # v10send = (np.random.random(100))
                # v11send = (np.random.random(100))
                # v12send = (np.random.random(100))
                # v13send = (np.random.random(100))
                # v14send = (np.random.random(100))
                # v15send = (np.random.random(100))
                # v16send = (np.random.random(100))
                # v1send.append(1)
                # v2send.append(2)
                # v3send.append(1)
                # v4send.append(1)
                # v5send.append(2)
                # v6send.append(1)
                # v7send.append(1)
                # v8send.append(1)
                # v9send.append(1)
                # v10send.append(2)
                # v11send.append(1)
                # v12send.append(2)
                # v13send.append(2)
                # v14send.append(1)
                # v15send.append(2)
                # v16send.append(2)
            except ValueError:
                v1send.append(0)
                v2send.append(0)
                v3send.append(0)
                v4send.append(0)
                v5send.append(0)
                v6send.append(0)
                v7send.append(0)
                v8send.append(0)
                v9send.append(0)
                v10send.append(0)
                v11send.append(0)
                v12send.append(0)
                v13send.append(0)
                v14send.append(0)
                v15send.append(0)
                v16send.append(0)
            # v1send = v1send.tolist()
            # v2send = v2send.tolist()
            # v3send = v3send.tolist()
            # v4send = v4send.tolist()
            # v5send = v5send.tolist()
            # v6send = v6send.tolist()
            # v7send = v7send.tolist()
            # v8send = v8send.tolist()
            # v9send = v9send.tolist()
            # v10send = v10send.tolist()
            # v11send = v11send.tolist()
            # v12send = v12send.tolist()
            # v13send = v13send.tolist()
            # v14send = v14send.tolist()
            # v15send = v15send.tolist()
            # v16send = v16send.tolist()
            # sfreq = 0
            contador = 0
            fin = time()
        if text_data_json["presion"] == 1:
            instancia, creado = Datos.objects.get_or_create(id=self.bases, defaults={'valores0': [], 'valores1': [],
                                                                                     'valores2': [], 'valores3': [],
                                                                                     'valores4': [], 'valores5': [],
                                                                                     'valores6': [], 'valores7': [],
                                                                                     'valores8': [], 'valores9': [],
                                                                                     'valores10': [], 'valores11': [],
                                                                                     'valores12': [], 'valores13': [],
                                                                                     'valores14': [], 'valores15': [],} )
            instancia.valores0.append(v1send)
            instancia.valores1.append(v2send)
            instancia.valores2.append(v3send)
            instancia.valores3.append(v4send)
            instancia.valores4.append(v5send)
            instancia.valores5.append(v6send)
            instancia.valores6.append(v7send)
            instancia.valores7.append(v8send)
            instancia.valores8.append(v9send)
            instancia.valores9.append(v10send)
            instancia.valores10.append(v11send)
            instancia.valores11.append(v12send)
            instancia.valores12.append(v13send)
            instancia.valores13.append(v14send)
            instancia.valores14.append(v15send)
            instancia.valores15.append(v16send)
            instancia.save()
            self.recording = True
        if text_data_json["presion"] == 0 and self.recording:
            instancia, creado = Datos.objects.get_or_create(id=self.bases, defaults={'valores0': [], 'valores1': [],
                                                                                     'valores2': [], 'valores3': [],
                                                                                     'valores4': [], 'valores5': [],
                                                                                     'valores6': [], 'valores7': [],
                                                                                     'valores8': [], 'valores9': [],
                                                                                     'valores10': [], 'valores11': [],
                                                                                     'valores12': [], 'valores13': [],
                                                                                     'valores14': [], 'valores15': [],})
            self.bases += 1
            self.recording = False
            data_recording = [instancia.valores0,instancia.valores1,instancia.valores2,instancia.valores3,instancia.valores4,
                              instancia.valores5,instancia.valores6,instancia.valores7,instancia.valores8,instancia.valores9,
                              instancia.valores10,instancia.valores11,instancia.valores12,instancia.valores13,instancia.valores14,
                              instancia.valores15]
            for i,a in enumerate(data_recording):
                data_recording[i] = np.concatenate(a)
            data_recording = np.array(data_recording)
            now = datetime.datetime.now()
            nombre_usuario = text_data_json["username"]
            now = now.strftime("%Y-%m-%d_%H-%M-%S_") + nombre_usuario
            current_dir = os.getcwd()
            save_dir = current_dir + "\\static\\img\\historial\\" + nombre_usuario + "\\"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            arr_dir = save_dir + "array\\"
            if not os.path.exists(arr_dir):
                os.mkdir(arr_dir)
            np.save(arr=data_recording, file=f"{arr_dir}{now}")
            # self.GenerarImagen(data_recording, f"{save_dir}", now, sfreq)
            # self.GenerarInforme(data_recording, f"{save_dir}", sfreq, now)
            self.GenerarEdf(data_recording, f"{save_dir}", sfreq, now)
        self.send(json.dumps(
            {"value1": v1send, "value2": v2send,"value3": v3send, "value4": v4send,
             "value5": v5send, "value6": v6send,"value7": v7send, "value8": v8send,
              "value9": v9send, "value10": v10send,"value11": v11send, "value12": v12send,
               "value13": v13send, "value14": v14send,"value15": v15send, "value16": v16send,
                 "sfreq": sfreq, "counter": counter}))
    def GenerarImagen(self, array, save_dir, now, sfreq):
        num_channels = 16
        sampling_frequency = int(sfreq)
        short_time = 1
        try: 
            total_time = array.shape[1]//sampling_frequency  # segundos
        except Exception:
            total_time = 1
        short_data_lenght = (short_time * array.shape[1])//total_time
        print(array.shape)
        print(total_time, short_data_lenght)
        array = array[:short_data_lenght]
        print(array.shape)
        # Crear un arreglo de tiempo
        time = np.linspace(0, short_time, array.shape[1])
        print(array.shape)
        print(time.shape)
        # Crear la figura y el eje
        plt.figure(figsize=(10, 6))

        # Ciclo para graficar cada canal separadamente
        for i,channel in enumerate(range(num_channels)):
            offset = channel * 1.5  # Ajusta el espacio vertical entre canales
            plt.plot(time, array[i] + offset, label=f'Canal {channel+1}')

        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Valor')
        plt.title('Datos de todos los canales')
        plt.legend()
        plt.grid()
        img_dir = save_dir + "preview\\"
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        plt.savefig(f"{img_dir}{now}")

    def GenerarInforme(self, array, save_dir, sfreq, now):
        ch_names = [str(a) for a in range(16)]
        ch_types = ["eeg"] * len(ch_names)
        info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
        raw = mne.io.RawArray(array, info, verbose=False)

        # raw.pick_types(eeg=True).load_data()
        report = mne.Report()
        report.add_raw(raw, title="Raw", scalings="auto", psd=True,)
        report_dir = save_dir + "informes\\"
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)
        report.save(f"{report_dir}{now}.html", overwrite=True, open_browser=False,)

    def GenerarEdf(self, array, save_dir, sqfreq, now):
        n_channels = 16
        edf_dir = save_dir + "download\\"
        if not os.path.exists(edf_dir):
            os.mkdir(edf_dir)
        edf_writer = pyedflib.EdfWriter(f"{edf_dir}{now}.edf", n_channels=n_channels, file_type=pyedflib.FILETYPE_EDFPLUS)
        for i in range(n_channels):
            channel_info = {
                'label': f"Channel {i+1}",
                'dimension': 'mV',
                'sample_rate': sqfreq,
                'physical_max': 100.0,     # Rango máximo en el archivo EDF
                'physical_min': 0.0,       # Rango mínimo en el archivo EDF
                'digital_max': 32767,      # Máximo valor digital para int16
                'digital_min': -32768      # Mínimo valor digital para int16
            }
            edf_writer.setSignalHeader(i, channel_info)

        data_mapped = (array * (100 / 1.15)).astype(np.int16)  # Realizar la transformación y convertir a int16
        edf_writer.writeSamples(data_mapped)
        # Escribir los datos en el archivo
        edf_writer.writeSamples(array.astype(np.int16))  # Convertir datos a int16 antes de escribi
        # Cerrar el archivo
        edf_writer.close()