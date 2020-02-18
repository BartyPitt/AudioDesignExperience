import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

# constants
BIT_DEPTH = 24
CHANNELS = 2
PLOT = True

INPUT_DEVICE_INDEX = 1
CM = int((BIT_DEPTH/8)*CHANNELS)  # Chunk multiplier
CHUNK = 1024 * CM                 # Samples per frame
FORMAT = pyaudio.paInt24          # Audio format. Change depending on bit-depth
RATE = 48000                      # Samples per second

# pyaudio class instance
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

# create matplotlib figure and axes
fig, axs = plt.subplots(2, figsize=(15, 7))

# basic formatting for the axes
if PLOT:
    for i in range(2):
        axs[i].set_title('AUDIO WAVEFORM')
        axs[i].set_xlabel('samples')
        axs[i].set_ylabel('volume')
        axs[i].set_ylim(0, 65536)
        axs[i].set_xlim(0, 2 * CHUNK)
        plt.setp(axs[i], xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 32768, 65536])

    line1, = axs[0].plot(x, np.random.rand(CHUNK), '-', lw=2)
    line2, = axs[1].plot(x, np.random.rand(CHUNK), '-', lw=2)

    # show the plot
    plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:

    # binary data
    data = stream.read(CHUNK)

    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(CM * CHUNK) + 'B', data)

    #print(data_int)

    data_np2 = np.array(data_int, dtype='<i2')
    data_np2 = np.delete(data_np2, np.arange(0, data_np2.size, 3))

    data_np3_L = (data_np2[1::4] * 256 + data_np2[0::4]) * 5 + 32768
    data_np3_R = (data_np2[3::4] * 256 + data_np2[2::4]) * 5 + 32768

    if PLOT:
        line1.set_ydata(data_np3_L)
        line2.set_ydata(data_np3_R)

    # update figure canvas
    if PLOT:
        try:
            fig.canvas.draw()
            fig.canvas.flush_events()
            frame_count += 1

        except TclError:

            # calculate average frame rate
            frame_rate = frame_count / (time.time() - start_time)

            print('stream stopped')
            print('average frame rate = {:.0f} FPS'.format(frame_rate))
            break