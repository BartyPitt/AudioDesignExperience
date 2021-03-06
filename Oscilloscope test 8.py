import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

# constants
BIT_DEPTH = 24
CHANNELS = 1

CM = int((BIT_DEPTH/8)*CHANNELS)  # Chunk multiplier

CHUNK = 1024 * CM            # samples per frame
FORMAT = pyaudio.paInt24     # audio format. Change depending on bit-depth
RATE = 48000                 # samples per second

# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))

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
    input_device_index = 3
)

# variable for plotting
x = np.arange(0, CM * CHUNK, CM) # what is the significance of using this 3?

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 65536)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 32768, 65536])

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
    data_int = struct.unpack(str(CM * CHUNK) + 'B', data) #B

    data_np2 = np.array(data_int, dtype='<i2')
    data_np2 = np.delete(data_np2, np.arange(0, data_np2.size, 3))

    data_np3 = (data_np2[1::2]*256 + data_np2[::2])*5 + 32768

    line.set_ydata(data_np3)

    # update figure canvas
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
