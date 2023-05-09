import os
import numpy as np
import matplotlib.pyplot as plt
import mne
import serial
from mne.channels import montage
from mne.viz import plot_topomap
import mne.datasets


from mpl_toolkits.mplot3d import Axes3D

serial_port = serial.Serial('COM6', baudrate=115200)
serial_port.timeout = None

sfreq = 200
times = np.arange(0, 10, 0.02)



ch1 = []
ch2 = []
ch3 = [] 

for _ in range(1000):
    data = serial_port.readline().decode('utf-8', errors="ignore").strip()
    ldata = list(data)
    ndata = [s for s in data if s != '\x00']
    ndata = ''.join(ndata)
    ndata = ndata.split('\t')
    ch1.append(ndata[0])
    ch2.append(ndata[1])
    ch3.append(ndata[2])

data = np.array([ch1,ch2,ch3])

# Definition of channel types and names.
ch_types = ['eeg', "eeg", "eeg"]
ch_names = ['pote_1', 'pote_2', 'pote_3']

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

raw = mne.io.RawArray(data, info)

raw.save('C:/Users/fedep/OneDrive/Documentos/mne_test/data_sample/data/sub-0/examen.fif', overwrite=True)

raw.plot(n_channels=3, scalings='auto', start=0, duration=10 )
plt.savefig("C:/Users/fedep/OneDrive/Documentos/mne_test/img/Analisis_voltage.png")

raw.plot_psd(fmax=50)
plt.savefig("C:/Users/fedep/OneDrive/Documentos/mne_test/img/Analisis_potencia.png")
spectrum = raw.compute_psd()
spectrum.plot_topomap()
plt.show()