import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

import pygame
from pygame import gfxdraw
import math
import queue

# constants
BIT_DEPTH = 24
CHANNELS = 2
PLOT = True

CHUNK_SIZE = 512

INPUT_DEVICE_INDEX = 1
CM = int((BIT_DEPTH/8)*CHANNELS)  # Chunk multiplier
CHUNK = CHUNK_SIZE * CM           # Samples per frame
FORMAT = pyaudio.paInt24          # Audio format. Change depending on bit-depth
RATE = 48000                      # Samples per second

ORBIT_RADIUS = 200
CIRCLE_RADIUS = 5

SCREEN_SIZE = 800
WIDTH = SCREEN_SIZE
HEIGHT = SCREEN_SIZE
CX = WIDTH/2
CY = HEIGHT/2
SF = 10 # Scale Factor

SM = 65536 / float(SCREEN_SIZE) # Screen multiplier

theta = 0
thetaDot = 0.1

theta2 = math.pi / 4
theta2Dot = 0.01

resolution = 1
RC = 0

count = 0

enabled = True


def rot(coords, theta):

    x = coords[0]
    y = coords[1]

    xRot = (x-CX) * math.cos(theta) - (y-CY) * math.sin(theta) + CX
    yRot = (x-CX) * math.sin(theta) + (y-CY) * math.cos(theta) + CY

    return int(xRot), int(yRot)


p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
    input_device_index = INPUT_DEVICE_INDEX
)

# variable for plotting
x = np.arange(0, CM * CHUNK, CM) # what is the significance of using this 3?

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

pygame.init()
screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

# Set the title of the window
pygame.display.set_caption('XYTest6')

while enabled:

    # binary data
    data = stream.read(CHUNK)

    data_int = struct.unpack(str(CM * CHUNK) + 'B', data)

    data_np2 = np.array(data_int, dtype='<i2')
    data_np2 = np.delete(data_np2, np.arange(0, data_np2.size, 3))

    data_np3_L = (data_np2[1::4] * 256 + data_np2[0::4]) + 32768
    data_np3_R = (data_np2[3::4] * 256 + data_np2[2::4]) + 32768

    data_np3_L_map = list(map(lambda x: (x / SM)*SF - (SCREEN_SIZE*0.5)*(SF-1), data_np3_L))
    data_np3_R_map = list(map(lambda x: (x / SM)*SF - (SCREEN_SIZE*0.5)*(SF-1), data_np3_R))

    screen.fill((0, 0, 0))

    # TODO add previous chunks to create a more full image

    for i in range(len(data_np3_L_map)):
        if i > 0:
            pygame.draw.line(screen, (180*(i/len(data_np3_L_map)), 50*(i/len(data_np3_L_map)), 255*(i/len(data_np3_L_map))),
                             rot((data_np3_L_map[i - 1], data_np3_R_map[i - 1]), theta2),
                             rot((data_np3_L_map[i], data_np3_R_map[i]), theta2), 1)

    theta2 += theta2Dot

    pygame.display.flip()

    count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enabled = False

pygame.quit()