from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import sys
import json
from app1.models import ejemplo
import pyrebase
import mne
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import io, base64
from io import StringIO
encoding = sys.getdefaultencoding()

config={
    "apiKey": "AIzaSyCkH6_-ZFtvwCgX7OAkMRPsa05bdeaE0RU",
    "authDomain": "test-71363.firebaseapp.com",
    "databaseURL": "https://test-71363-default-rtdb.firebaseio.com",
    "projectId": "test-71363",
    "storageBucket": "test-71363.appspot.com",
    "messagingSenderId": "331246731829",
    "appId": "1:331246731829:web:05815c77eda1d79568277c"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database= firebase.database()
electrodos= ['FP2', 'FP1', 'F3', 'F4', 'F8', 'F7', 'C3', 'C4', 'T3', 'T4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2']
matplotlib.use('agg')




@csrf_exempt
def index(request):
    data = []
    for n in range(len(electrodos)):
        elecdata = database.child(electrodos[n]).get().val()
        data.append(elecdata)
        #obj = ejemplo.objects.get(id=n+8)
        #obj.pieces = data["FP1"]
        #obj.save()
        context = {"a": ejemplo.objects.all}
    data = np.array(data)
    ch_names = ['FP2', 'FP1', 'F3', 'F4', 'F8', 'F7', 'C3', 'C4', 'T3', 'T4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2']
    ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
    info = mne.create_info(ch_names=ch_names, sfreq=1000, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    raw.plot(scalings="auto", n_channels=16)

    plt.savefig("C:/Users/fedep/OneDrive/Documentos/GitHub/Brainstream/brainstream/static/img/figure1.png")
    return render(request, "result.html", context)

def bciin(request):
    return render(request, "bci.html")

def contactoin(request):
    return render(request, "contacto.html")

def iniin(request):
    return render(request, "iniciarsesion.html")

def acercain(request):
    return render(request, "acercade.html")

def inicio(request):
    return render(request, "pagina.html")
