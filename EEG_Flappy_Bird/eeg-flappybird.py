import pygame
import sys
import random
import serial
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt
import threading
import time

# Game parameters
PIPE_SEP = 220
FLOOR_SPEED = 1
PIPE_SPEED = 0.001
PIPE_HEIGHT = [200, 300, 400]
PIPE_INTERVAL = 2200
SCORE_RATE = 0.005
INITIAL_BIRD_X = 50
GRAVITY = 0.6  # Added gravity for more realistic motion
CHUNK_SIZE = 128  # Tamaño de la ventana para el análisis de Fourier
N = CHUNK_SIZE // 1  # Tamaño de la mitad del espectro
data_buffer = np.zeros(CHUNK_SIZE)
spectrum_buffer = np.zeros(N)
muestras = 240 # Número de muestras

serial_port = serial.Serial('COM7', baudrate=9600)
serial_port.timeout = None

# Functions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))

def create_pipe():
    random_height = random.choice(PIPE_HEIGHT)
    bottom_pipe = pipe_surface.get_rect(midtop=(350, random_height))
    top_pipe = pipe_surface.get_rect(midbottom=(350, random_height - PIPE_SEP))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_SPEED
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.bottom >= 450:
        return False
    return True

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

    # ...
def rms_voltage_power_spectrum(time_series, min_freq, max_freq, SPS, nsamples, window=None):
    """
    Calculates the RMS voltage of a waveform between two frequency limits using Parseval's Theorem.

    :param time_series: Time series data.
    :param min_freq: Minimum frequency for which to calculate RMS voltage.
    :param max_freq: Maximum frequency for which to calculate RMS voltage.
    :param SPS: Samples per second to computer frequency 
    :param nsamples: Number of samples in original time series data.
    :param window: OPTIONAL window function to apply to time series data before FFT. If None, no window function is applied.

    :return: RMS voltage between freq_min and freq_max, ps power spectrum
    """
    #computing power spectrum
    frequencies = fftfreq(nsamples, d=1.0/SPS)
    
    #subtract the mean to ensure the time series is a zero-mean
    #Fourier assuems that time series is periodic with no DC offset
    time_series_zero_mean = time_series - np.mean(time_series)
    fourier_coeffs = np.fft.fft(time_series_zero_mean)
    ps = np.abs(fourier_coeffs)**2
    #__, ps = welch(time_series, fs=SPS)
    
    if window is not None:
        ps *= window #Apply window function to power spectrum

    freq_mask = (np.abs(frequencies) >= min_freq) & (np.abs(frequencies) <= max_freq)
    ps_range = ps[freq_mask]

    #Calculate RMS voltage using Parseval's Theorem
    rms = (1/nsamples) * np.sqrt(np.sum(ps_range))

    imx = np.argmax(ps)

    pmx = frequencies[imx]

    if rms > 0.01:
        if pmx > 40:
            pmx = 0
        else:
            pass
    else:
        pmx = 0
        rms = 0

    return pmx, ps, rms

def calibration(calibration_time,sps,min_freq=0,max_freq=12):
    nsamples = calibration_time*sps
    # raw_signal = np.zeros(nsamples)
    total_pmx = 0
    total_rms = 0
    for i in range(480*10): #Collects data every interval
        data = serial_port.readline().decode('utf-8', errors="ignore").strip()
        ndata = [s for s in data if s != '\x00']
        ndata = ''.join(ndata)
        ndata = ndata.split('\t')
        try:
            ndata = float(ndata[0])
        except ValueError:
            ndata = 0
                # Agrega el valor a la ventana de datos
        data_buffer[:-1] = data_buffer[1:]
        data_buffer[-1] = ndata

        nsamples = (len(data_buffer))

        pmx, ps, rms = rms_voltage_power_spectrum(data_buffer, min_freq, max_freq, sps, nsamples)

        total_pmx += pmx
        total_rms += rms
    
    promedio_pmx = total_pmx / (480*10)
    promedio_rms = total_rms / (480*10)


    return(promedio_pmx, ps, promedio_rms)

min_freq = 0
max_freq = 40
sps = muestras
calibration_time = 5


input("toca enter para ingresar el valor relajado")
relajado = calibration(calibration_time, sps)

pmxr = relajado[0]
rmsr = relajado[2]

print(pmxr, rmsr)

input("toca enter para ingresar el valor concentrado")
concentrado = calibration(calibration_time, sps)

pmxc = concentrado[0]
rmsc = concentrado[2]

print(pmxc, rmsc)

input("lol")

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((288, 512), pygame.NOFRAME)
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 20)




# Initialize game variables
game_active = True
score = 0
high_score = 0

# Load surfaces/images in the game
bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center=(INITIAL_BIRD_X, 256))
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, PIPE_INTERVAL)
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 256))
bird_velocity = 0

# Main Game Loop
act = 0
flag = 1
while 1:
    data = serial_port.readline().decode('utf-8', errors="ignore").strip()
    ndata = [s for s in data if s != '\x00']
    ndata = ''.join(ndata)
    ndata = ndata.split('\t')
    try:
        ndata = float(ndata[0])
    except ValueError:
        ndata = 0
            # Agrega el valor a la ventana de datos
    data_buffer[:-1] = data_buffer[1:]
    data_buffer[-1] = ndata
    nsamples = (len(data_buffer))
    pmx, ps, rms = rms_voltage_power_spectrum(data_buffer, min_freq, max_freq, sps, nsamples)
    
    # game part
    for event in pygame.event.get(): # all events that pygame can detect
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # press space key to restart the game
            if event.key == pygame.K_SPACE:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (INITIAL_BIRD_X,256)
                score = 0
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # extend allows list to include whatever that is in the tuple
    
    # display background
    screen.blit(bg_surface,(0,0))
    
    # display and create continuously moving floor effect
    floor_x_pos -= FLOOR_SPEED
    draw_floor()

    if floor_x_pos <= -288:
        floor_x_pos = 0
        
    if game_active:
        if abs(pmx - pmxr) > abs(pmx - pmxc):
            if rmsc+1 > rms > rmsc-1:
                if bird_rect.centery > 0:  #
                    bird_rect.centery += -1.7
            else:
                bird_rect.centery += 0
        bird_rect.centery += 1
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)
    
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += SCORE_RATE
        score_display('main_game')
        
    else: # game over state
        screen.blit(game_over_surface, game_over_rect)
        score_display('game_over')
        
    pygame.display.update()
    
    clock.tick(sps)